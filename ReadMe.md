This repository contains a small model-checking style project built around a generic **Breadth-First Search (BFS)** implementation and a **RootedGraph** abstraction. It includes:

- A reusable BFS 
- A RootedGraph interface used to encode different state-space systems
- A Tower of Hanoi example encoded as a rooted graph and solved with BFS
- Three Alice/Bob protocol variants (AB1, AB2, AB3) encoded as rooted graphs
- Automated checks for two safety/liveness properties:
  - Exclusion: Alice and Bob are never simultaneously in the critical section (CS)
  - Deadlock: no reachable state has zero outgoing transitions
- Counterexample traces reconstructed from BFS parent pointers and labeled transitions

## Repository Structure and Role of Each File

### rooted_graph.py
Defines the RootedGraph abstract interface that all explored systems must implement:

- roots(): returns initial state(s)
- neighbors(node): returns successor state(s)


### bfs.py
Contains the generic Breadth-First Search implementation:

- bfs(graph, opaque, on_entry) performs BFS from graph.roots() using graph.neighbors(node)
- Calls on_entry(parent, node, opaque) the first time each node is discovered
- Supports early stop when on_entry(...) returns True
- Returns (opaque, visited_set) so results can be extracted from opaque


### hanoi.py
Encodes the Tower of Hanoi problem as a rooted state-space graph:

- `HanoiGraph(RootedGraph) provides:
  - roots() = initial configuration
  - neighbors(state) = all legal one-disk moves
- solve_hanoi_bfs(n) runs BFS to find a shortest solution path and reconstructs it via parent pointers

This file demonstrates how BFS + RootedGraph can solve a classical search problem.


### alice_bob.py
Encodes three Alice/Bob protocol variants as rooted graphs:

- AB1Graph: minimal protocol (expected to violate exclusion, no deadlock)
- AB2Graph: flag-based protocol (expected to enforce exclusion, but may deadlock)
- AB3Graph: improved protocol (expected to enforce exclusion and avoid deadlock)

Key details:
- States are tuples (locations + flags depending on the variant)
- Transitions are labeled (a1, b2, b4) using LabeledRootedGraph
- Labels enable reconstruction of human-readable counterexample traces


### test_graphs.py
Verification utilities and automated property checks:

- explore_all_states(graph) explores the full reachable state-space via BFS
- check_exclusion(graph) searches for a reachable state where:
  - AliceLoc == CS and BobLoc == CS
- check_deadlock(graph) searches for a reachable state with:
  - len(neighbors(state)) == 0
- If a violation is found, it reconstructs:
  - the sequence of states (path)
  - the sequence of transition labels (actions)

This file is effectively the “model checker” for the Alice/Bob graphs.


### main.py
Entry point that runs:

1. A BFS sanity demo on a small toy graph
2. A Tower of Hanoi BFS solve (default n=3)
3. The Alice/Bob verification suite for AB1 / AB2 / AB3

Run this file to reproduce the expected behavior and generate traces.


## How the Alice/Bob Verification Works

1. Each protocol variant (AB1/AB2/AB3) defines a state-space:
   - states represent the combined configuration of Alice and Bob
   - transitions represent one atomic step by either Alice or Bob
2. BFS explores all reachable states from the initial root state.
3. Properties are checked by stopping BFS as soon as a bad state is discovered:
   - Exclusion violation: (CS, CS, ...)
   - Deadlock: a state with no outgoing transitions
4. The counterexample path is reconstructed using a BFS parent map and edge labels.


## Expected High-Level Results

When running the verification:
- AB1
  - Exclusion: fails
  - Deadlock: passes
- AB2
  - Exclusion: passes
  - Deadlock: fails (deadlock reachable)
- AB3
  - Exclusion: passes
  - Deadlock: passes

## New Abstraction Layer: Language Semantics (LS)

To model systems at a higher level than a plain rooted graph, the repository adds Language Semantics:

A LanguageSemantics object exposes:
- initials(): initial states (same idea as roots())
- actions(state): actions enabled from state (can represent labeled arcs, weighted transitions, etc.)
- execute(state, action): applies an action and returns the successor state(s)

This separates:
- “what actions are possible from a state”
from
- “how these actions produce new states”

This is useful when transitions are better expressed as **actions** (with optional weights/costs), rather than directly listing neighbors.

---

### languagesemantics.py
Defines the LS abstraction:

- LanguageSemantics base class with:
  - initials()
  - actions(state)
  - execute(state, action)
- Typically also includes an Action structure (label + optional payload/weight)

---

### ls2rg.py
Adapter Language Semantics → RootedGraph.

- Takes a LanguageSemantics instance and exposes:
  - roots() by calling initials()
  - neighbors(state) by enumerating actions(state) and applying execute(state, action)

This adapter allows reusing the **same BFS** implementation without modification.

---

### hanoilanguagesemantics.py
A modified Tower of Hanoi implementation based on LanguageSemantics instead of RootedGraph.

- Defines Hanoi in terms of:
  - enabled moves (actions) from each state
  - execution of a move producing the next state(s)
- Uses deepcopy when building successor configurations (explicit independent copies)

This provides a direct example of how to switch from RootedGraph modeling to LS modeling.

---

### validation_ls.py
A small validation script to test the LS-based Hanoi:

- Builds the Hanoi LanguageSemantics
- Wraps it with LS2RG
- Runs BFS to find a solution (and optionally prints steps / moves depending on the script)

---

## How the Alice/Bob Verification Works

1. Each protocol variant (AB1/AB2/AB3) defines a state-space:
   - states represent the combined configuration of Alice and Bob
   - transitions represent one atomic step by either Alice or Bob
2. BFS explores all reachable states from the initial root state.
3. Properties are checked by stopping BFS as soon as a bad state is discovered:
   - Exclusion violation: (CS, CS, ...)
   - Deadlock: a state with no outgoing transitions
4. The counterexample path is reconstructed using a BFS parent map and edge labels.
---

## Soup DSL (Python-like Domain Specific Language)

In addition to Hanoi and Alice/Bob, the repository includes a small DSL called **Soup**.  
The goal is to represent a program as a set of **rules** (pieces), each rule having:

- a **guard**: a condition that decides when the rule can be applied
- an **effect**: a function that computes the next state when the rule is applied

This matches the style of operational semantics: from a state, you list enabled actions, then execute one.

---

### `soup_lang.py`
Defines the Soup DSL and its semantics:

- Piece: a named rule with (guard, effect)
- Soup: a program containing:
  - pieces: a list of Piece
  - init: a list of initial states
- SoupSemantics(LanguageSemantics):
  - initials() returns init
  - actions(state) returns the enabled Piece objects
  - execute(state, piece) applies the piece effect and returns successor state(s)
  - uses deepcopy in execute to avoid side effects when states are mutable

This file is the runtime semantics of the Soup language.

---

### `soup_example.py`
Demonstrates how to use the Soup DSL:
- Example 1: a binary clock (0 → 1 → 0)
- Example 2: a cyclic counter (0 → 1 → 2 → 0)
- Example 3: BFS exploration of a Soup program by converting it to a rooted graph using LS2RG
