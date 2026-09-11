# Markov Chain Room Occupancy Simulation

## Overview

This project simulates the evolution of a probability distribution across a set of connected rooms using **transition matrices** and **Markov chain principles**.

The main objective is to model how the probability of presence moves from one room to another through doors. Each door is associated with a weight representing its width, which is then used to construct a normalized transition matrix.

The project also explores different configurations of the environment, including:

* A base configuration
* A configuration with a structural break
* An oscillating configuration
* A stationary distribution computed using the power method
* A step-by-step probability evolution through a graphical interface

A simple **Tkinter graphical interface** allows the user to interact with the simulation directly using the keyboard.

---

## Features

* Construction of transition matrices from weighted connections
* Automatic normalization of transition probabilities
* Simulation of probability evolution over a fixed number of iterations
* Computation of a stationary probability distribution using the power method
* Comparison between different room configurations
* Simulation of an oscillating system
* Simulation of a system after a structural break
* Interactive Tkinter visualization
* Keyboard-based controls
* Real-time display of room occupancy probabilities

---

## Mathematical Model

The environment is represented as a graph:

* Each **room** is represented by a state.
* Each **door** represents a connection between two rooms.
* The **width of a door** is used as the weight of the connection.
* The weights are normalized to obtain transition probabilities.

For a room \(i\), the transition probability toward room \(j\) is:

$$
P_{ij} = \frac{w_{ij}}{\sum_k w_{ik}}
$$

where \(w_{ij}\) is the weight associated with the connection between rooms \(i\) and \(j\).

If a room has no connection, it becomes an absorbing state by setting:

$$
P_{ii} = 1
$$

This ensures that every row of the transition matrix represents a valid probability distribution.

---

## Probability Evolution

The initial probability distribution is represented by a vector:

$$
V_0
$$

For example:

```text
V0 = [1, 0, 0, 0, 0]
```

This means that the entire initial probability is located in the first room.

At each iteration, the probability distribution is updated according to the transition matrix:

$$
V_{n+1} = V_n T
$$

The implementation computes the corresponding matrix-vector product and produces the probability distribution for the next state.

---

## Stationary Distribution

The project also implements a power-method approach to approximate a stationary distribution.

A stationary distribution \(V\) satisfies:

$$
V T = V
$$

The algorithm repeatedly applies the transition matrix and normalizes the resulting vector until convergence.

The convergence criterion is based on the difference between two successive estimates of the eigenvalue:

$$
|q_n - q_{n-1}| < \varepsilon
$$

The default precision is:

```text
ε = 10⁻⁶
```

with a maximum of:

```text
1000 iterations
```

---

## Simulated Configurations

### 1. Base Configuration

The initial environment contains five rooms and the following weighted connections:

```text
Room 0 ↔ Room 1 : 100
Room 0 ↔ Room 3 : 70
Room 1 ↔ Room 2 : 120
Room 3 ↔ Room 4 : 70
Room 4 ↔ Room 2 : 50
```

This configuration represents the original environment.

The initial probability distribution is:

```text
[1, 0, 0, 0, 0]
```

meaning that the simulation starts entirely in Room 0.

---

### 2. Oscillation Configuration

The oscillation configuration contains four rooms connected in a cycle:

```text
Room 0 ↔ Room 1
Room 1 ↔ Room 2
Room 2 ↔ Room 3
Room 3 ↔ Room 0
```

All connections have the same weight.

This configuration is designed to demonstrate periodic probability behavior.

---

### 3. Structural Break Configuration

The structural break configuration modifies the original environment by introducing additional connections:

```text
Room 0 ↔ Room 1
Room 1 ↔ Room 2
Room 2 ↔ Room 3
Room 3 ↔ Room 0
Room 0 ↔ Room 2
Room 3 ↔ Room 4
```

This allows the project to study how modifying the topology of the system affects its long-term probability distribution.

---

## Graphical Interface

The project includes a simple graphical interface built with **Tkinter**.

Each room is represented by a circle.

The size of each circle depends on its current probability:

```text
radius = probability × 50 + 10
```

The current probability is displayed inside the circle.

The visualization is updated after each iteration or when switching between configurations.

---

## Controls

The simulation can be controlled using the keyboard.

| Key | Action                                  |
| --- | --------------------------------------- |
| `→` | Perform one iteration                   |
| `1` | Load the base configuration             |
| `2` | Load the structural break configuration |
| `3` | Load the oscillation configuration      |
| `0` | Compute the stationary distribution     |

### Example

Pressing:

```text
1
```

loads the base configuration.

Then pressing:

```text
→
```

advances the simulation by one iteration.

Pressing:

```text
0
```

runs the power method until convergence.

---

## Project Structure

A recommended project structure is:

```text
markov-chain-room-simulation/
│
├── main.py
├── README.md
├── requirements.txt
├── .gitignore
│
└── assets/
    └── ...
```

---

## Requirements

The project uses Python's standard library and does not require external numerical libraries.

The main dependency is:

```text
tkinter
```

Tkinter is included with most standard Python installations.

You can verify that Tkinter is available with:

```bash
python -m tkinter
```

If a small test window appears, Tkinter is correctly installed.

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/markov-chain-room-simulation.git
```

Move into the project directory:

```bash
cd markov-chain-room-simulation
```

### 2. Run the program

```bash
python main.py
```

No external package installation is required if Tkinter is already included in your Python installation.

---

## Implementation

The project is organized around two main functions.

### Transition Matrix Construction

```python
creation_matrice_transition(nb_pieces, portes)
```

This function:

1. Creates a square matrix initialized with zeros.
2. Adds the weights associated with each door.
3. Makes the matrix symmetric.
4. Normalizes each row.
5. Creates a self-transition for isolated rooms.

---

### Probability Evolution

```python
evolution_presence(T, V0, k=None, precision=1e-6, max_iter=1000)
```

This function supports two modes.

#### Fixed Iteration Mode

When `k` is provided, the function performs exactly `k` iterations.

Example:

```python
evolution_presence(T_base, V0_base, k=50)
```

#### Convergence Mode

When `k=None`, the function applies the power method until the convergence criterion is reached.

Example:

```python
evolution_presence(
    T_base,
    V0_base,
    k=None,
    precision=1e-6,
    max_iter=1000
)
```

---

## Example Output

When the program starts, it prints the transition matrices for the different configurations.

It then computes:

* The stationary distribution of the base configuration
* The distribution after 50 iterations
* The stationary distribution after the structural break
* The stationary distribution of the oscillation configuration

Example console output:

```text
Matrice de transition du probleme initial :

[0.0, 0.5882352941176471, 0.0, 0.4117647058823529, 0.0]
[0.45454545454545453, 0.0, 0.5454545454545454, 0.0, 0.0]
[0.0, 0.7058823529411765, 0.0, 0.0, 0.29411764705882354]
[0.5, 0.0, 0.0, 0.0, 0.5]
[0.0, 0.0, 0.4166666666666667, 0.5833333333333334, 0.0]

Matrice de transition (rupture): 

[0.0, 0.5, 0.0, 0.5]
[0.5, 0.0, 0.5, 0.0]
[0.0, 0.5, 0.0, 0.5]
[0.5, 0.0, 0.5, 0.0]

Matrice de transition (oscillation) : 

[0.0, 0.3333333333333333, 0.3333333333333333, 0.3333333333333333, 0.0]
[0.5, 0.0, 0.5, 0.0, 0.0]
[0.3333333333333333, 0.3333333333333333, 0.0, 0.3333333333333333, 0.0]
[0.3333333333333333, 0.0, 0.3333333333333333, 0.0, 0.3333333333333333]
[0.0, 0.0, 0.0, 1.0, 0.0]

 vecteur propre de la situation de base par cauchy et le nombre d'iteration necessaire : 
([0.20726829038664937, 0.26836317852938424, 0.2072710051058734, 0.17075233992731242, 0.14634518605078062], 60)

vecteur propre de la situation de base par iteration et le nombre d'iteration : 
([0.20754762520312542, 0.26795961234456867, 0.2075346782040477, 0.17063411789262967, 0.14632396635562894], 50)

vecteur propre de la situation (rupture) par cauchy et le nombre d'iteration necessaire: 
([0.25002245435524967, 0.166647164675717, 0.2500224543552491, 0.24995509128950136, 0.08335283532428285], 31)

vecteur propre de la situation (oscillation) par cauchy et le nombre d'iteration necessaire: 
([0.5, 0.0, 0.5, 0.0, 0.0], 1)

```

The exact numerical values depend on the transition matrices defined in the program.

---

** A view of the interface **
<img width="501" height="279" alt="image" src="https://github.com/user-attachments/assets/d9ba4882-18b8-4731-b7a6-3e372678bc80" />


## Concepts Demonstrated

This project provides a practical introduction to several mathematical and computational concepts:

* Markov chains
* Transition matrices
* Probability distributions
* Matrix-vector multiplication
* Eigenvectors and eigenvalues
* Stationary distributions
* The power method
* Convergence criteria
* Graph-based modeling
* Numerical simulation
* Interactive visualization

---

## Possible Improvements

Several improvements could make the project more robust and scalable:

### Code Improvements

* Replace manual matrix operations with NumPy
* Use dedicated classes for rooms and connections
* Separate the mathematical model from the graphical interface
* Add type hints
* Improve error handling
* Add unit tests

### Visualization Improvements

* Display room names directly in the interface
* Draw doors and connections between rooms
* Display transition probabilities
* Add animation between iterations
* Add probability evolution graphs
* Add controls directly in the GUI instead of relying only on keyboard shortcuts

### Mathematical Improvements

* Implement additional convergence criteria
* Compare different numerical methods
* Compute eigenvalues explicitly
* Analyze periodic and absorbing states
* Study the effect of changing door weights
* Allow users to create custom room networks

---

## Educational Purpose

This project was developed as an educational exercise to understand how transition matrices and Markov chains can be used to model the evolution of probabilities in a connected environment.

The graphical interface provides an intuitive way to observe how an initial probability distribution evolves over time and how changes in the underlying network affect its long-term behavior.

---

## License

This project is intended for educational and academic purposes.

You may modify and reuse the code for learning, experimentation, and further development.
