# Mini-Courier Planner

An algorithm-based courier planning application developed for the Design and Analysis of Algorithms (ADA) capstone. The application combines parcel sorting, capacity-constrained parcel selection, shortest-path computation, and approximate delivery-route construction.

## Project Overview

The system processes parcel orders and a weighted road network through the following stages:

1. **Parcel ordering — Merge Sort:** orders parcels by ascending delivery deadline, then descending priority.
2. **Cargo selection — 0/1 Knapsack:** selects a subset of parcels that maximizes total priority value without exceeding the vehicle's weight capacity.
3. **Shortest paths — Dijkstra's Algorithm:** computes shortest road distances and reconstructs road paths between relevant delivery locations.
4. **Route construction — Nearest-Neighbor TSP heuristic:** builds a round-trip sequence through the selected delivery locations, starting and ending at the depot.

The route produced by Nearest-Neighbor is a heuristic solution. It is not guaranteed to be the globally shortest possible TSP tour.

## Project Structure

```text
capstone_project/
├── README.md
├── report.md
├── runtime.png
└── courier_planner/
    ├── __init__.py
    ├── main.py
    ├── parcels.py
    ├── sorting.py
    ├── knapsack.py
    ├── graph.py
    ├── tsp.py
    ├── benchmark.py
    ├── README.md
    ├── report.md
    ├── SUMMARY.md
    ├── runtime.png
    └── data/
        ├── small.json
        └── large.json
```

## Requirements

- Python 3.10 or later
- No third-party packages are required to run the main courier-planning pipeline.
- `matplotlib` is required by the benchmark module to generate the runtime chart.

If Matplotlib is not installed, install it with:

```bash
python -m pip install matplotlib
```

## How to Run

Run the commands below from the repository's root directory (`capstone_project`).

### Small dataset

```bash
python -m courier_planner.main --dataset small
```

The small dataset contains 10 parcels, 8 road-network nodes, and a vehicle capacity of 25 kg. The application displays the complete Knapsack DP table for this small instance.

### Large dataset

```bash
python -m courier_planner.main --dataset large
```

The large dataset contains 500 parcels, 100 road-network nodes, and a vehicle capacity of 150 kg.

### Run the benchmark

```bash
python -m courier_planner.benchmark
```

The benchmark measures the algorithm stages on the predefined datasets and on generated input sizes. It also generates runtime chart output. Execution times depend on the computer, Python version, and system load, so results may vary between runs.

## Recorded Execution Results

The following results were recorded from a local Windows execution on 13 November 2026. They are example observations from that run, not guaranteed timings for other systems.

### Pre-generated datasets

| Dataset | Parcels | Road nodes | Capacity | Selected parcels | Priority value | Route distance | Total measured runtime |
|---|---:|---:|---:|---:|---:|---:|---:|
| Small | 10 | 8 | 25 kg | 7 | 129 | 122 km | 0.0805 ms |
| Large | 500 | 100 | 150 kg | 85 | 2,914 | 259 km | 14.4930 ms |

### Generated benchmark sizes

| Parcels (N) | Nodes (V) | Capacity (W) | Merge Sort (ms) | Knapsack (ms) | Dijkstra (ms) | TSP (ms) | Total (ms) |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 10 | 8 | 25 | 0.0174 | 0.0444 | 0.0539 | 0.0075 | 0.1232 |
| 50 | 10 | 25 | 0.0560 | 0.1114 | 0.0564 | 0.0054 | 0.2292 |
| 100 | 20 | 33 | 0.0854 | 0.2079 | 0.2007 | 0.0107 | 0.5046 |
| 200 | 40 | 66 | 0.1885 | 0.8744 | 0.9360 | 0.0312 | 2.0300 |
| 500 | 100 | 166 | 0.5972 | 6.1248 | 9.4065 | 0.1579 | 16.2863 |

**Important:** The generated 500-parcel benchmark uses a capacity of 166 kg, while the pre-generated `large.json` dataset uses 150 kg. These are separate test configurations and should not be compared as if they were identical inputs. The benchmark's five-iteration measurements are environment-dependent.

## Algorithmic Complexity

Let:
- `N` = number of parcels
- `W` = vehicle capacity (in the integer weight units used by the DP)
- `V` = number of road-network vertices
- `E` = number of road-network edges
- `K` = number of distinct selected delivery locations

| Stage | Algorithm | Time complexity | Space complexity |
|---|---|---|---|
| Parcel ordering | Merge Sort | Θ(N log N) | O(N) |
| Cargo selection | 0/1 Knapsack DP | O(NW) | O(NW) |
| Shortest paths | Heap-based Dijkstra, per source | O((V + E) log V) | O(V) |
| Multiple-source shortest paths | Dijkstra from each required source | O(K(V + E) log V) | Depends on stored distance/path matrices |
| Delivery sequence | Nearest-Neighbor over K locations | O(K²) | O(K) |

The Knapsack complexity is pseudo-polynomial because it depends on the numeric capacity `W`, not only on the number of parcels. The exact routing workload also depends on how many source locations require Dijkstra runs.

## Output Produced

The command-line application reports:

- Parcel ordering by deadline and priority
- Knapsack selection, total selected weight, and total priority value
- Delivery-stop sequence
- Shortest road path for each route leg
- Cumulative and total round-trip distance
- Final dispatch summary

## Limitations

- The Knapsack objective maximizes total priority value under the weight constraint; it does not itself guarantee that every selected parcel's deadline will be met.
- Nearest-Neighbor is a heuristic and does not guarantee an optimal TSP route.
- The model uses a static weighted road graph; it does not account for live traffic, changing road conditions, or time-dependent travel.
- The benchmark timings are machine-dependent and should be interpreted as observations from the recorded test environment.
- The generated benchmark and the pre-generated JSON datasets use different capacity settings at the 500-parcel scale.

## Further Scope

Possible extensions include deadline-feasibility checks using estimated arrival times, comparison of Nearest-Neighbor with local-search methods such as 2-Opt, and modelling the problem as a Vehicle Routing Problem with Time Windows (VRPTW).

## Detailed Report

See [`report.md`](report.md) for the detailed problem formulation, algorithm design, complexity discussion, and experimental analysis.
