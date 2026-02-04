# VerificationBuchiAliceBob

Ce fichier est généré automatiquement par `verify_buchi_all_alice_bob.py`.

Une violation Büchi est un **cycle acceptant** dans le produit (système × propriété).
Le contre-exemple est donné sous forme :
- **prefix-trace** : mène à une SCC acceptante
- **cyclic-suffix-trace** : boucle à l’intérieur de la SCC acceptante

## AB1 — P1

Commande reproductible :
```bash
python verify_buchi_alice_bob.py --model AB1 --prop P1
```

- visited: **7**
- RESULT: **VIOLÉ** (cycle acceptant trouvé)

### Prefix-trace (projection système)
```text
('I', 'I', 'DOWN', 'DOWN', 'Alice') --init||!cond--> ('I', 'I', 'DOWN', 'DOWN', 'Alice')
('I', 'I', 'DOWN', 'DOWN', 'Alice') --a1||!cond--> ('CS', 'I', 'DOWN', 'DOWN', 'Alice')
('CS', 'I', 'DOWN', 'DOWN', 'Alice') --b1||cond--> ('CS', 'CS', 'DOWN', 'DOWN', 'Alice')
```

### Cyclic-suffix-trace (projection système)
```text
('CS', 'CS', 'DOWN', 'DOWN', 'Alice') --b2||true--> ('CS', 'I', 'DOWN', 'DOWN', 'Alice')
('CS', 'I', 'DOWN', 'DOWN', 'Alice') --b1||true--> ('CS', 'CS', 'DOWN', 'DOWN', 'Alice')
```

## AB1 — P2

Commande reproductible :
```bash
python verify_buchi_alice_bob.py --model AB1 --prop P2
```

- visited: **4**
- RESULT: **SAT** (pas de cycle acceptant)

## AB1 — P3

Commande reproductible :
```bash
python verify_buchi_alice_bob.py --model AB1 --prop P3
```

- visited: **5**
- RESULT: **SAT** (pas de cycle acceptant)

## AB1 — P4

Commande reproductible :
```bash
python verify_buchi_alice_bob.py --model AB1 --prop P4
```

- visited: **4**
- RESULT: **SAT** (pas de cycle acceptant)

## AB1 — P5

Commande reproductible :
```bash
python verify_buchi_alice_bob.py --model AB1 --prop P5
```

- visited: **4**
- RESULT: **SAT** (pas de cycle acceptant)

## AB2 — P1

Commande reproductible :
```bash
python verify_buchi_alice_bob.py --model AB2 --prop P1
```

- visited: **8**
- RESULT: **SAT** (pas de cycle acceptant)

## AB2 — P2

Commande reproductible :
```bash
python verify_buchi_alice_bob.py --model AB2 --prop P2
```

- visited: **8**
- RESULT: **VIOLÉ** (cycle acceptant trouvé)

### Prefix-trace (projection système)
```text
('I', 'I', 'DOWN', 'DOWN', 'Alice') --init||!deadlock--> ('I', 'I', 'DOWN', 'DOWN', 'Alice')
('I', 'I', 'DOWN', 'DOWN', 'Alice') --a1||!deadlock--> ('W', 'I', 'UP', 'DOWN', 'Alice')
('W', 'I', 'UP', 'DOWN', 'Alice') --b1||deadlock--> ('W', 'W', 'UP', 'UP', 'Alice')
```

### Cyclic-suffix-trace (projection système)
```text
('W', 'W', 'UP', 'UP', 'Alice') --stutter||true--> ('W', 'W', 'UP', 'UP', 'Alice')
```

## AB2 — P3

Commande reproductible :
```bash
python verify_buchi_alice_bob.py --model AB2 --prop P3
```

- visited: **12**
- RESULT: **VIOLÉ** (cycle acceptant trouvé)

### Prefix-trace (projection système)
```text
('I', 'I', 'DOWN', 'DOWN', 'Alice') --init||!q--> ('I', 'I', 'DOWN', 'DOWN', 'Alice')
('I', 'I', 'DOWN', 'DOWN', 'Alice') --a1||!q--> ('W', 'I', 'UP', 'DOWN', 'Alice')
('W', 'I', 'UP', 'DOWN', 'Alice') --b1||!q--> ('W', 'W', 'UP', 'UP', 'Alice')
```

### Cyclic-suffix-trace (projection système)
```text
('W', 'W', 'UP', 'UP', 'Alice') --stutter||!q--> ('W', 'W', 'UP', 'UP', 'Alice')
```

## AB2 — P4

Commande reproductible :
```bash
python verify_buchi_alice_bob.py --model AB2 --prop P4
```

- visited: **14**
- RESULT: **VIOLÉ** (cycle acceptant trouvé)

### Prefix-trace (projection système)
```text
('I', 'I', 'DOWN', 'DOWN', 'Alice') --init||true--> ('I', 'I', 'DOWN', 'DOWN', 'Alice')
('I', 'I', 'DOWN', 'DOWN', 'Alice') --a1||p0&!q0--> ('W', 'I', 'UP', 'DOWN', 'Alice')
('W', 'I', 'UP', 'DOWN', 'Alice') --b1||!q0--> ('W', 'W', 'UP', 'UP', 'Alice')
```

### Cyclic-suffix-trace (projection système)
```text
('W', 'W', 'UP', 'UP', 'Alice') --stutter||!q0--> ('W', 'W', 'UP', 'UP', 'Alice')
```

## AB2 — P5

Commande reproductible :
```bash
python verify_buchi_alice_bob.py --model AB2 --prop P5
```

- visited: **12**
- RESULT: **VIOLÉ** (cycle acceptant trouvé)

### Prefix-trace (projection système)
```text
('I', 'I', 'DOWN', 'DOWN', 'Alice') --init||true--> ('I', 'I', 'DOWN', 'DOWN', 'Alice')
('I', 'I', 'DOWN', 'DOWN', 'Alice') --a1||!aCS&aW&bNI--> ('W', 'I', 'UP', 'DOWN', 'Alice')
('W', 'I', 'UP', 'DOWN', 'Alice') --b1||!aCS--> ('W', 'W', 'UP', 'UP', 'Alice')
```

### Cyclic-suffix-trace (projection système)
```text
('W', 'W', 'UP', 'UP', 'Alice') --stutter||!aCS--> ('W', 'W', 'UP', 'UP', 'Alice')
```

## AB3 — P1

Commande reproductible :
```bash
python verify_buchi_alice_bob.py --model AB3 --prop P1
```

- visited: **8**
- RESULT: **SAT** (pas de cycle acceptant)

## AB3 — P2

Commande reproductible :
```bash
python verify_buchi_alice_bob.py --model AB3 --prop P2
```

- visited: **8**
- RESULT: **SAT** (pas de cycle acceptant)

## AB3 — P3

Commande reproductible :
```bash
python verify_buchi_alice_bob.py --model AB3 --prop P3
```

- visited: **12**
- RESULT: **VIOLÉ** (cycle acceptant trouvé)

### Prefix-trace (projection système)
```text
('I', 'I', 'DOWN', 'DOWN', 'Alice') --init||!q--> ('I', 'I', 'DOWN', 'DOWN', 'Alice')
('I', 'I', 'DOWN', 'DOWN', 'Alice') --a1||!q--> ('W', 'I', 'UP', 'DOWN', 'Alice')
```

### Cyclic-suffix-trace (projection système)
```text
('W', 'I', 'UP', 'DOWN', 'Alice') --b1||!q--> ('W', 'W', 'UP', 'UP', 'Alice')
('W', 'W', 'UP', 'UP', 'Alice') --b4||!q--> ('W', 'I', 'UP', 'DOWN', 'Alice')
```

## AB3 — P4

Commande reproductible :
```bash
python verify_buchi_alice_bob.py --model AB3 --prop P4
```

- visited: **17**
- RESULT: **VIOLÉ** (cycle acceptant trouvé)

### Prefix-trace (projection système)
```text
('I', 'I', 'DOWN', 'DOWN', 'Alice') --init||true--> ('I', 'I', 'DOWN', 'DOWN', 'Alice')
('I', 'I', 'DOWN', 'DOWN', 'Alice') --a1||true--> ('W', 'I', 'UP', 'DOWN', 'Alice')
('W', 'I', 'UP', 'DOWN', 'Alice') --a2||true--> ('CS', 'I', 'UP', 'DOWN', 'Alice')
('CS', 'I', 'UP', 'DOWN', 'Alice') --b1||p1&!q1--> ('CS', 'W', 'UP', 'UP', 'Alice')
('CS', 'W', 'UP', 'UP', 'Alice') --b4||!q1--> ('CS', 'I', 'UP', 'DOWN', 'Alice')
```

### Cyclic-suffix-trace (projection système)
```text
('CS', 'I', 'UP', 'DOWN', 'Alice') --b1||!q1--> ('CS', 'W', 'UP', 'UP', 'Alice')
('CS', 'W', 'UP', 'UP', 'Alice') --b4||!q1--> ('CS', 'I', 'UP', 'DOWN', 'Alice')
```

## AB3 — P5

Commande reproductible :
```bash
python verify_buchi_alice_bob.py --model AB3 --prop P5
```

- visited: **16**
- RESULT: **VIOLÉ** (cycle acceptant trouvé)

### Prefix-trace (projection système)
```text
('I', 'I', 'DOWN', 'DOWN', 'Alice') --init||true--> ('I', 'I', 'DOWN', 'DOWN', 'Alice')
('I', 'I', 'DOWN', 'DOWN', 'Alice') --b1||aNI&!bCS&bW--> ('I', 'W', 'DOWN', 'UP', 'Alice')
('I', 'W', 'DOWN', 'UP', 'Alice') --a1||!bCS--> ('W', 'W', 'UP', 'UP', 'Alice')
('W', 'W', 'UP', 'UP', 'Alice') --b4||!bCS--> ('W', 'I', 'UP', 'DOWN', 'Alice')
('W', 'I', 'UP', 'DOWN', 'Alice') --a2||!bCS--> ('CS', 'I', 'UP', 'DOWN', 'Alice')
```

### Cyclic-suffix-trace (projection système)
```text
('CS', 'I', 'UP', 'DOWN', 'Alice') --b1||!bCS--> ('CS', 'W', 'UP', 'UP', 'Alice')
('CS', 'W', 'UP', 'UP', 'Alice') --b4||!bCS--> ('CS', 'I', 'UP', 'DOWN', 'Alice')
```

## AB4 — P1

Commande reproductible :
```bash
python verify_buchi_alice_bob.py --model AB4 --prop P1
```

- visited: **11**
- RESULT: **SAT** (pas de cycle acceptant)

## AB4 — P2

Commande reproductible :
```bash
python verify_buchi_alice_bob.py --model AB4 --prop P2
```

- visited: **11**
- RESULT: **SAT** (pas de cycle acceptant)

## AB4 — P3

Commande reproductible :
```bash
python verify_buchi_alice_bob.py --model AB4 --prop P3
```

- visited: **17**
- RESULT: **SAT** (pas de cycle acceptant)

## AB4 — P4

Commande reproductible :
```bash
python verify_buchi_alice_bob.py --model AB4 --prop P4
```

- visited: **21**
- RESULT: **VIOLÉ** (cycle acceptant trouvé)

### Prefix-trace (projection système)
```text
('I', 'I', 'DOWN', 'DOWN', 'Alice') --init||true--> ('I', 'I', 'DOWN', 'DOWN', 'Alice')
('I', 'I', 'DOWN', 'DOWN', 'Alice') --a1||true--> ('W', 'I', 'UP', 'DOWN', 'Alice')
('W', 'I', 'UP', 'DOWN', 'Alice') --a2||true--> ('CS', 'I', 'UP', 'DOWN', 'Alice')
('CS', 'I', 'UP', 'DOWN', 'Alice') --b1||p1&!q1--> ('CS', 'W', 'UP', 'UP', 'Alice')
('CS', 'W', 'UP', 'UP', 'Alice') --b4||!q1--> ('CS', 'R', 'UP', 'DOWN', 'Alice')
```

### Cyclic-suffix-trace (projection système)
```text
('CS', 'R', 'UP', 'DOWN', 'Alice') --a3||!q1--> ('I', 'R', 'DOWN', 'DOWN', 'Alice')
('I', 'R', 'DOWN', 'DOWN', 'Alice') --a1||!q1--> ('W', 'R', 'UP', 'DOWN', 'Alice')
('W', 'R', 'UP', 'DOWN', 'Alice') --a2||!q1--> ('CS', 'R', 'UP', 'DOWN', 'Alice')
```

## AB4 — P5

Commande reproductible :
```bash
python verify_buchi_alice_bob.py --model AB4 --prop P5
```

- visited: **19**
- RESULT: **VIOLÉ** (cycle acceptant trouvé)

### Prefix-trace (projection système)
```text
('I', 'I', 'DOWN', 'DOWN', 'Alice') --init||true--> ('I', 'I', 'DOWN', 'DOWN', 'Alice')
('I', 'I', 'DOWN', 'DOWN', 'Alice') --b1||aNI&!bCS&bW--> ('I', 'W', 'DOWN', 'UP', 'Alice')
('I', 'W', 'DOWN', 'UP', 'Alice') --a1||!bCS--> ('W', 'W', 'UP', 'UP', 'Alice')
('W', 'W', 'UP', 'UP', 'Alice') --b4||!bCS--> ('W', 'R', 'UP', 'DOWN', 'Alice')
('W', 'R', 'UP', 'DOWN', 'Alice') --a2||!bCS--> ('CS', 'R', 'UP', 'DOWN', 'Alice')
```

### Cyclic-suffix-trace (projection système)
```text
('CS', 'R', 'UP', 'DOWN', 'Alice') --a3||!bCS--> ('I', 'R', 'DOWN', 'DOWN', 'Alice')
('I', 'R', 'DOWN', 'DOWN', 'Alice') --a1||!bCS--> ('W', 'R', 'UP', 'DOWN', 'Alice')
('W', 'R', 'UP', 'DOWN', 'Alice') --a2||!bCS--> ('CS', 'R', 'UP', 'DOWN', 'Alice')
```

## AB5 — P1

Commande reproductible :
```bash
python verify_buchi_alice_bob.py --model AB5 --prop P1
```

- visited: **10**
- RESULT: **SAT** (pas de cycle acceptant)

## AB5 — P2

Commande reproductible :
```bash
python verify_buchi_alice_bob.py --model AB5 --prop P2
```

- visited: **10**
- RESULT: **SAT** (pas de cycle acceptant)

## AB5 — P3

Commande reproductible :
```bash
python verify_buchi_alice_bob.py --model AB5 --prop P3
```

- visited: **16**
- RESULT: **SAT** (pas de cycle acceptant)

## AB5 — P4

Commande reproductible :
```bash
python verify_buchi_alice_bob.py --model AB5 --prop P4
```

- visited: **18**
- RESULT: **SAT** (pas de cycle acceptant)

## AB5 — P5

Commande reproductible :
```bash
python verify_buchi_alice_bob.py --model AB5 --prop P5
```

- visited: **14**
- RESULT: **SAT** (pas de cycle acceptant)

