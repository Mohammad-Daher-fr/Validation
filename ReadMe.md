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


