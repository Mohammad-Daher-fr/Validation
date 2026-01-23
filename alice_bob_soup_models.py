from __future__ import annotations
from typing import Callable, List, Tuple
from soup_lang import Piece, Soup

"""Encodage des modèles AB1..AB5 en Soup.

Configuration = (a_loc, b_loc, flagAlice, flagBob, turn)

Même si certains modèles n'utilisent pas tous les champs (ex: AB1 n'utilise pas
les flags/turn), on les conserve avec des valeurs stables.
"""

# Domaine des configurations

# Locations
I = "I"
W = "W"
CS = "CS"
R = "R"  # utilisé par AB4 (Bob)

# Flags
UP = "UP"
DOWN = "DOWN"

# Turn (AB5)
ALICE = "Alice"
BOB = "Bob"

Config = Tuple[str, str, str, str, str]


def mk(
    a_loc: str, b_loc: str, flag_a: str = DOWN, flag_b: str = DOWN, turn: str = ALICE
) -> Config:
    return (a_loc, b_loc, flag_a, flag_b, turn)


def upd(
    cfg: Config, *, a_loc=None, b_loc=None, flag_a=None, flag_b=None, turn=None
) -> Config:
    a, b, fa, fb, t = cfg
    return (
        a if a_loc is None else a_loc,
        b if b_loc is None else b_loc,
        fa if flag_a is None else flag_a,
        fb if flag_b is None else flag_b,
        t if turn is None else turn,
    )


# Helpers: création de pièces
Guard = Callable[[Config], bool]
Effect = Callable[[Config], Config]


def piece(name: str, guard: Guard, effect: Effect) -> Piece:
    return Piece(name=name, guard=guard, effect=effect)


def a_loc_is(x: str) -> Guard:
    return lambda c: c[0] == x


def b_loc_is(x: str) -> Guard:
    return lambda c: c[1] == x


# Modèles AB1..AB5


def make_ab1() -> Soup:
    """AB1: pas de flags.

    Alice: I --a1--> CS ; CS --a2--> I
    Bob:   I --b1--> CS ; CS --b2--> I
    """
    pieces: List[Piece] = [
        # Alice
        piece("a1", a_loc_is(I), lambda c: upd(c, a_loc=CS)),
        piece("a2", a_loc_is(CS), lambda c: upd(c, a_loc=I)),
        # Bob
        piece("b1", b_loc_is(I), lambda c: upd(c, b_loc=CS)),
        piece("b2", b_loc_is(CS), lambda c: upd(c, b_loc=I)),
    ]
    return Soup(pieces=pieces, init=[mk(I, I, DOWN, DOWN, ALICE)])


def make_ab2() -> Soup:
    """AB2: stratégie par drapeaux.

    Alice:
      I  --a1 / flagA=UP-->    W
      W  --a2 [flagB==DOWN]--> CS
      CS --a3 / flagA=DOWN-->  I

    Bob:
      I  --b1 / flagB=UP-->    W
      W  --b2 [flagA==DOWN]--> CS
      CS --b3 / flagB=DOWN-->  I
    """
    pieces: List[Piece] = [
        # Alice
        piece("a1", a_loc_is(I), lambda c: upd(c, a_loc=W, flag_a=UP)),
        piece("a2", lambda c: c[0] == W and c[3] == DOWN, lambda c: upd(c, a_loc=CS)),
        piece("a3", a_loc_is(CS), lambda c: upd(c, a_loc=I, flag_a=DOWN)),
        # Bob
        piece("b1", b_loc_is(I), lambda c: upd(c, b_loc=W, flag_b=UP)),
        piece("b2", lambda c: c[1] == W and c[2] == DOWN, lambda c: upd(c, b_loc=CS)),
        piece("b3", b_loc_is(CS), lambda c: upd(c, b_loc=I, flag_b=DOWN)),
    ]
    return Soup(pieces=pieces, init=[mk(I, I, DOWN, DOWN, ALICE)])


def make_ab3() -> Soup:
    """AB3: AB2 + backoff de Bob.

    Ajout: b4 depuis W -> I si flagA==UP, et flagB=DOWN.
    """
    pieces: List[Piece] = [
        # Alice (AB2)
        piece("a1", a_loc_is(I), lambda c: upd(c, a_loc=W, flag_a=UP)),
        piece("a2", lambda c: c[0] == W and c[3] == DOWN, lambda c: upd(c, a_loc=CS)),
        piece("a3", a_loc_is(CS), lambda c: upd(c, a_loc=I, flag_a=DOWN)),
        # Bob (AB2 + b4)
        piece("b1", b_loc_is(I), lambda c: upd(c, b_loc=W, flag_b=UP)),
        piece("b2", lambda c: c[1] == W and c[2] == DOWN, lambda c: upd(c, b_loc=CS)),
        piece(
            "b4",
            lambda c: c[1] == W and c[2] == UP,
            lambda c: upd(c, b_loc=I, flag_b=DOWN),
        ),
        piece("b3", b_loc_is(CS), lambda c: upd(c, b_loc=I, flag_b=DOWN)),
    ]
    return Soup(pieces=pieces, init=[mk(I, I, DOWN, DOWN, ALICE)])


def make_ab4() -> Soup:
    """AB4: AB2 côté Alice, Bob avec état R (retry).

    Bob:
      I  --b1 / flagB=UP-->    W
      W  --b2 [flagA==DOWN]--> CS
      W  --b4 [flagA==UP] / flagB=DOWN--> R
      R  --b5 [flagA==DOWN] / flagB=UP--> CS
      CS --b3 / flagB=DOWN-->  I
    """
    pieces: List[Piece] = [
        # Alice (AB2)
        piece("a1", a_loc_is(I), lambda c: upd(c, a_loc=W, flag_a=UP)),
        piece("a2", lambda c: c[0] == W and c[3] == DOWN, lambda c: upd(c, a_loc=CS)),
        piece("a3", a_loc_is(CS), lambda c: upd(c, a_loc=I, flag_a=DOWN)),
        # Bob
        piece("b1", b_loc_is(I), lambda c: upd(c, b_loc=W, flag_b=UP)),
        piece("b2", lambda c: c[1] == W and c[2] == DOWN, lambda c: upd(c, b_loc=CS)),
        piece(
            "b4",
            lambda c: c[1] == W and c[2] == UP,
            lambda c: upd(c, b_loc=R, flag_b=DOWN),
        ),
        piece(
            "b5",
            lambda c: c[1] == R and c[2] == DOWN,
            lambda c: upd(c, b_loc=CS, flag_b=UP),
        ),
        piece("b3", b_loc_is(CS), lambda c: upd(c, b_loc=I, flag_b=DOWN)),
    ]
    return Soup(pieces=pieces, init=[mk(I, I, DOWN, DOWN, ALICE)])


def make_ab5() -> Soup:
    """AB5: Peterson (flags + turn).

    Alice:
      I  --a1 / flagA=UP; turn=Bob--> W
      W  --a2 [turn=Alice || flagB==DOWN]--> CS
      CS --a3 / flagA=DOWN--> I

    Bob:
      I  --b1 / flagB=UP; turn=Alice--> W
      W  --b2 [turn=Bob || flagA==DOWN]--> CS
      CS --b3 / flagB=DOWN--> I
    """
    pieces: List[Piece] = [
        # Alice
        piece("a1", a_loc_is(I), lambda c: upd(c, a_loc=W, flag_a=UP, turn=BOB)),
        piece(
            "a2",
            lambda c: c[0] == W and (c[4] == ALICE or c[3] == DOWN),
            lambda c: upd(c, a_loc=CS),
        ),
        piece("a3", a_loc_is(CS), lambda c: upd(c, a_loc=I, flag_a=DOWN)),
        # Bob
        piece("b1", b_loc_is(I), lambda c: upd(c, b_loc=W, flag_b=UP, turn=ALICE)),
        piece(
            "b2",
            lambda c: c[1] == W and (c[4] == BOB or c[2] == DOWN),
            lambda c: upd(c, b_loc=CS),
        ),
        piece("b3", b_loc_is(CS), lambda c: upd(c, b_loc=I, flag_b=DOWN)),
    ]
    return Soup(pieces=pieces, init=[mk(I, I, DOWN, DOWN, ALICE)])


def get_model(name: str) -> Soup:
    """Accès simple par identifiant 'AB1'..'AB5'."""
    n = name.strip().upper()
    if n == "AB1":
        return make_ab1()
    if n == "AB2":
        return make_ab2()
    if n == "AB3":
        return make_ab3()
    if n == "AB4":
        return make_ab4()
    if n == "AB5":
        return make_ab5()
    raise ValueError(f"Modèle inconnu: {name}")
