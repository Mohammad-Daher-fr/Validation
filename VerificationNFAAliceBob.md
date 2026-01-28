# VerificationNFAAliceBob

Ce fichier est généré par `verify_nfa_alice_bob.py`.

## Exécution rapide

Pour lancer **tous** les scénarios (AB1..AB5 × (P1,P2) × (Patron 1,2)) :
```bash
python verify_nfa_alice_bob.py --all
```

## Différence entre Patron 1 et Patron 2

- **Patron 1** : boucle `true` sur l’état T. Le produit contient potentiellement plus de transitions (non-déterminisme supplémentaire).
- **Patron 2** : boucle `!cond` sur T. Le produit est plus *contraint* : une seule transition depuis T selon la valeur de `cond` (souvent moins de branchements).
- Les deux reconnaissent l’idée « `cond` arrive au moins une fois », mais l’**impact pratique** se voit via `visited` (nombre d’états explorés) et parfois le **contre-exemple** trouvé en premier (à cause de l’ordre des actions).

## Résultats

### AB1 — P1 — Patron 1

Commande reproductible :
```bash
python verify_nfa_alice_bob.py --model AB1 --prop P1 --pattern 1
```

- États explorés (visited) : **5**
- Résultat : **VIOLÉ** (contre-exemple trouvé)

Trace (projection système) :
```text
('I', 'I', 'DOWN', 'DOWN', 'Alice') --init--> ('I', 'I', 'DOWN', 'DOWN', 'Alice')
('I', 'I', 'DOWN', 'DOWN', 'Alice') --a1--> ('CS', 'I', 'DOWN', 'DOWN', 'Alice')
('CS', 'I', 'DOWN', 'DOWN', 'Alice') --b1--> ('CS', 'CS', 'DOWN', 'DOWN', 'Alice')
```

Labels du produit :
```text
init||true
a1||true
b1||cond
```

### AB1 — P1 — Patron 2

Commande reproductible :
```bash
python verify_nfa_alice_bob.py --model AB1 --prop P1 --pattern 2
```

- États explorés (visited) : **5**
- Résultat : **VIOLÉ** (contre-exemple trouvé)

Trace (projection système) :
```text
('I', 'I', 'DOWN', 'DOWN', 'Alice') --init--> ('I', 'I', 'DOWN', 'DOWN', 'Alice')
('I', 'I', 'DOWN', 'DOWN', 'Alice') --a1--> ('CS', 'I', 'DOWN', 'DOWN', 'Alice')
('CS', 'I', 'DOWN', 'DOWN', 'Alice') --b1--> ('CS', 'CS', 'DOWN', 'DOWN', 'Alice')
```

Labels du produit :
```text
init||!cond
a1||!cond
b1||cond
```

### AB1 — P2 — Patron 1

Commande reproductible :
```bash
python verify_nfa_alice_bob.py --model AB1 --prop P2 --pattern 1
```

- États explorés (visited) : **5**
- Résultat : **SAT** (pas de contre-exemple)

### AB1 — P2 — Patron 2

Commande reproductible :
```bash
python verify_nfa_alice_bob.py --model AB1 --prop P2 --pattern 2
```

- États explorés (visited) : **5**
- Résultat : **SAT** (pas de contre-exemple)

### AB2 — P1 — Patron 1

Commande reproductible :
```bash
python verify_nfa_alice_bob.py --model AB2 --prop P1 --pattern 1
```

- États explorés (visited) : **9**
- Résultat : **SAT** (pas de contre-exemple)

### AB2 — P1 — Patron 2

Commande reproductible :
```bash
python verify_nfa_alice_bob.py --model AB2 --prop P1 --pattern 2
```

- États explorés (visited) : **9**
- Résultat : **SAT** (pas de contre-exemple)

### AB2 — P2 — Patron 1

Commande reproductible :
```bash
python verify_nfa_alice_bob.py --model AB2 --prop P2 --pattern 1
```

- États explorés (visited) : **6**
- Résultat : **VIOLÉ** (contre-exemple trouvé)

Trace (projection système) :
```text
('I', 'I', 'DOWN', 'DOWN', 'Alice') --init--> ('I', 'I', 'DOWN', 'DOWN', 'Alice')
('I', 'I', 'DOWN', 'DOWN', 'Alice') --b1--> ('I', 'W', 'DOWN', 'UP', 'Alice')
('I', 'W', 'DOWN', 'UP', 'Alice') --a1--> ('W', 'W', 'UP', 'UP', 'Alice')
```

Labels du produit :
```text
init||true
b1||true
a1||cond
```

### AB2 — P2 — Patron 2

Commande reproductible :
```bash
python verify_nfa_alice_bob.py --model AB2 --prop P2 --pattern 2
```

- États explorés (visited) : **6**
- Résultat : **VIOLÉ** (contre-exemple trouvé)

Trace (projection système) :
```text
('I', 'I', 'DOWN', 'DOWN', 'Alice') --init--> ('I', 'I', 'DOWN', 'DOWN', 'Alice')
('I', 'I', 'DOWN', 'DOWN', 'Alice') --b1--> ('I', 'W', 'DOWN', 'UP', 'Alice')
('I', 'W', 'DOWN', 'UP', 'Alice') --a1--> ('W', 'W', 'UP', 'UP', 'Alice')
```

Labels du produit :
```text
init||!cond
b1||!cond
a1||cond
```

### AB3 — P1 — Patron 1

Commande reproductible :
```bash
python verify_nfa_alice_bob.py --model AB3 --prop P1 --pattern 1
```

- États explorés (visited) : **9**
- Résultat : **SAT** (pas de contre-exemple)

### AB3 — P1 — Patron 2

Commande reproductible :
```bash
python verify_nfa_alice_bob.py --model AB3 --prop P1 --pattern 2
```

- États explorés (visited) : **9**
- Résultat : **SAT** (pas de contre-exemple)

### AB3 — P2 — Patron 1

Commande reproductible :
```bash
python verify_nfa_alice_bob.py --model AB3 --prop P2 --pattern 1
```

- États explorés (visited) : **9**
- Résultat : **SAT** (pas de contre-exemple)

### AB3 — P2 — Patron 2

Commande reproductible :
```bash
python verify_nfa_alice_bob.py --model AB3 --prop P2 --pattern 2
```

- États explorés (visited) : **9**
- Résultat : **SAT** (pas de contre-exemple)

### AB4 — P1 — Patron 1

Commande reproductible :
```bash
python verify_nfa_alice_bob.py --model AB4 --prop P1 --pattern 1
```

- États explorés (visited) : **12**
- Résultat : **SAT** (pas de contre-exemple)

### AB4 — P1 — Patron 2

Commande reproductible :
```bash
python verify_nfa_alice_bob.py --model AB4 --prop P1 --pattern 2
```

- États explorés (visited) : **12**
- Résultat : **SAT** (pas de contre-exemple)

### AB4 — P2 — Patron 1

Commande reproductible :
```bash
python verify_nfa_alice_bob.py --model AB4 --prop P2 --pattern 1
```

- États explorés (visited) : **12**
- Résultat : **SAT** (pas de contre-exemple)

### AB4 — P2 — Patron 2

Commande reproductible :
```bash
python verify_nfa_alice_bob.py --model AB4 --prop P2 --pattern 2
```

- États explorés (visited) : **12**
- Résultat : **SAT** (pas de contre-exemple)

### AB5 — P1 — Patron 1

Commande reproductible :
```bash
python verify_nfa_alice_bob.py --model AB5 --prop P1 --pattern 1
```

- États explorés (visited) : **11**
- Résultat : **SAT** (pas de contre-exemple)

### AB5 — P1 — Patron 2

Commande reproductible :
```bash
python verify_nfa_alice_bob.py --model AB5 --prop P1 --pattern 2
```

- États explorés (visited) : **11**
- Résultat : **SAT** (pas de contre-exemple)

### AB5 — P2 — Patron 1

Commande reproductible :
```bash
python verify_nfa_alice_bob.py --model AB5 --prop P2 --pattern 1
```

- États explorés (visited) : **11**
- Résultat : **SAT** (pas de contre-exemple)

### AB5 — P2 — Patron 2

Commande reproductible :
```bash
python verify_nfa_alice_bob.py --model AB5 --prop P2 --pattern 2
```

- États explorés (visited) : **11**
- Résultat : **SAT** (pas de contre-exemple)

