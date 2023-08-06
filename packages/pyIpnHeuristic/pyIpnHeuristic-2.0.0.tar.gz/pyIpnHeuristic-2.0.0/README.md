# PyIpnHeuristic

pyIpnHeuristic is a pure Python implementation of some heuristic algorithms for the National
Polytechnic Institute of Mexico. For more information on pyIpnHeuristic, visit the GitHub project page
[pyIpnHeuristic](https://github.com/niortizva/pyIpnHeuristic)

## Pip Install

```
pip install pyIpnHeuristic
```

## Benchmark 

Benchmark problems were taken from [Liang et al. 2006](https://www.researchgate.net/publication/216301032_Problem_definitions_and_evaluation_criteria_for_the_CEC_2006_special_session_on_constrained_real-parameter_optimization).
Check out the benchmark [doc](BENCHMARK.md) for a deatiled description.

Import benchmark problems as follows:

```python
# Import the benchmark problem methods
# get_pg01, get_pg02, get_pg03, get_pg04, get_pg05,
# get_pg06, get_pg07, get_pg08, get_pg09, get_pg10,
# get_pg11, get_pg12, get_pg13, get_pg14, get_pg15,
# get_pg16, get_pg17, get_pg18, get_pg19, get_pg20,
# get_pg21, get_pg22, get_pg23, get_pg24
from pyIpnHeuristic.benchmark import get_pg01

# get_pg[*problem]() returns problem parameters as:
#    {
#        objective_function": <class 'function'>,
#        "gx": [<class 'function'>, <class 'function'>, ...], # Soft Restrictions
#        "hx": [<class 'function'>, <class 'function'>, ...], # Hard Restrictions
#        "ranges": [[inf(x1), sup(x1)], ..., [inf(xd), sup(xd)]], # List of Ranges for each variable
#        "markdown": "PROBLEM X", # Markdown Problem description 
#        "x": x_best, # Best values
#        "fx": fx_best # Best solution value
#    }
problem = get_pg01()

objective_function = problem.get("objective_function")
gx = problem.get("gx")
hx = problem.get("hx")
ranges = problem.get("ranges")
markdown = problem.get("markdown")
x_best = problem.get("x")
fx_best = problem.get("fx")
```

## Released Algorithms

- Harmony Search

```python
from pyIpnHeuristic.harmonySearch import HarmonySearch
    
harmonySearch = HarmonySearch(
    objective_function, # e.g, def f(*x): return x[0]**2 + x[1] **2
    soft_constrains=g, # e.g, [def g(*x): return x[0], def g(*x): return x[0]**2]
    hard_constrains=h, # e.g, [def h(*x): return x[1], def h(*x): return x[1]**2]
    ranges=ranges, # e.g, [[0, 1], [0, 1]]
    population_size=population_size, # e.g, 4
    smooth=False, # If True, hard restrictions will be treated as soft restrictions
    epsilon=10**-4, # If smmooth is True, then h(x) = 0 --> |h(x)| - epsilon <= 0
    # Harmony Search Parameters
    hcmr=hcmr,
    par=par,
    alpha=alpha
)

harmonySearch.search(
    iterations=T, # Number of iterations to be made
    save_history=True # Save the results for each iteration. Default False
)
```
- Modified Harmony Search

```python
from pyIpnHeuristic.modifiedHarmonySearch import ModifiedHarmonySearch
    
harmonySearch = ModifiedHarmonySearch(
    objective_function, # e.g, def f(*x): return x[0]**2 + x[1] **2
    soft_constrains=g, # e.g, [def g(*x): return x[0], def g(*x): return x[0]**2]
    hard_constrains=h, # e.g, [def h(*x): return x[1], def h(*x): return x[1]**2]
    ranges=ranges, # e.g, [[0, 1], [0, 1]]
    population_size=population_size, # e.g, 4
    smooth=False, # If True, hard restrictions will be treated as soft restrictions
    epsilon=10**-4, # If smmooth is True, then h(x) = 0 --> |h(x)| - epsilon <= 0
    # Harmony Search Parameters
    hcmr=hcmr,
    par=par,
    alpha=alpha
)

harmonySearch.search(
    iterations=T, # Number of iterations to be made
    save_history=True # Save the results for each iteration. Default False
)
```
- Differential Evolution:
    - DE/rand/1/ bin
    - DE/best/1
    - DE/current-to-best/1
    - DE/best/2
    - DE/rand/2
    
```python
from pyIpnHeuristic.differentialEvolution import DifferentialEvolution

differentialEvolution = DifferentialEvolution(
    objective_function, # e.g, def f(*x): return x[0]**2 + x[1] **2
    soft_constrains=g, # e.g, [def g(*x): return x[0], def g(*x): return x[0]**2]
    hard_constrains=h, # e.g, [def h(*x): return x[1], def h(*x): return x[1]**2]
    ranges=ranges, # e.g, [[0, 1], [0, 1]]
    population_size=population_size, # e.g, 4
    smooth=False, # If True, hard restrictions will be treated as soft restrictions
    epsilon=10**-4, # If smooth is True, then h(x) = 0 --> |h(x)| - epsilon <= 0
    # Differential Evolution Parameters
    type=de_type, # Types: "rand-1", "best-1", "current-to-best-1", "best-2, "rand-2", default: "rand-1"
    f=0.9,
    cr=0.05,
)

differentialEvolution.search(
    iterations=T, # Number of iterations to be made
    save_history=True # Save the results for each iteration. Default False
)
```
- Particle Swarm Optimization

```python
from pyIpnHeuristic.particleSwarmOptimization import ParticleSwarmOptimization

particleSwarmOptimization = ParticleSwarmOptimization(
    objective_function, # e.g, def f(*x): return x[0]**2 + x[1] **2
    soft_constrains=g, # e.g, [def g(*x): return x[0], def g(*x): return x[0]**2]
    hard_constrains=h, # e.g, [def h(*x): return x[1], def h(*x): return x[1]**2]
    ranges=ranges, # e.g, [[0, 1], [0, 1]]
    population_size=population_size, # e.g, 4
    smooth=False, # If True, hard restrictions will be treated as soft restrictions
    epsilon=10**-4, # If smmooth is True, then h(x) = 0 --> |h(x)| - epsilon <= 0
    # Particle Swarm Parameters
    w=0.3,
    c1=0.1,
    c2=1.9
)

particleSwarmOptimization.search(
    iterations=T, # Number of iterations to be made
    save_history=True # Save the results for each iteration. Default False
)
```
- Artificial Bee Colony

```python
from pyIpnHeuristic.artificialBeeColony import ArtificialBeeColony

artificialBeeColony = ArtificialBeeColony(
    objective_function, # e.g, def f(*x): return x[0]**2 + x[1] **2
    soft_constrains=g, # e.g, [def g(*x): return x[0], def g(*x): return x[0]**2]
    hard_constrains=h, # e.g, [def h(*x): return x[1], def h(*x): return x[1]**2]
    ranges=ranges, # e.g, [[0, 1], [0, 1]]
    population_size=population_size, # e.g, 4
    smooth=False, # If True, hard restrictions will be treated as soft restrictions
    epsilon=10**-4, # If smmooth is True, then h(x) = 0 --> |h(x)| - epsilon <= 0
    # Artificial Bee Colony Parameters
    mr=0.3,
    max_trials=3,
)

artificialBeeColony.search(
    iterations=T, # Number of iterations to be made
    save_history=True # Save the results for each iteration. Default False
)
```
