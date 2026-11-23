# Mini-Courier Planner

## 1. Abstract

The Mini-Courier Planner is a Python application that combines sorting, dynamic programming and graph algorithms to produce a parcel-loading plan and a round-trip delivery route. Given a set of parcels, a vehicle weight capacity and a weighted road network, the application:

1. orders parcels by delivery deadline and priority;
2. selects a high-value subset that does not exceed the vehicle's weight capacity;
3. calculates shortest road paths between the depot and selected delivery locations; and
4. constructs a delivery tour using the Nearest-Neighbor heuristic.

The project demonstrates how multiple algorithmic techniques can be integrated into one practical workflow. The route-ordering stage is heuristic: the application does not claim to find a globally optimal Traveling Salesperson tour.

## 2. Problem Definition

A courier has a collection of parcels. Each parcel has an identifier, weight, priority value, deadline and destination node. The road network is represented as a weighted graph, where vertices represent junctions and edge weights represent road distances. Node `0` is the depot.

The planner has three main objectives:

- **Order the inventory:** sort parcels by earliest deadline, then by higher priority, with a deterministic identifier tie-break where applicable.
- **Respect vehicle capacity:** choose parcels whose combined weight is at most the vehicle capacity while maximizing the sum of their priority values.
- **Plan a delivery circuit:** visit the distinct destinations of the selected parcels and return to the depot, using shortest road paths between consecutive stops.

These objectives are related but distinct. Sorting determines the displayed evaluation order; the 0/1 Knapsack algorithm chooses the subset that maximizes total priority value. Therefore, the selected subset is not necessarily the set of earliest-deadline parcels. The current model does not enforce delivery time windows or guarantee that every selected parcel can be delivered before its deadline.

## 3. System Workflow and Design

```text
Parcel data + weighted road graph
                |
                v
     Merge Sort (deadline, priority)
                |
                v
       0/1 Knapsack (capacity)
                |
                v
   Extract distinct selected destinations
                |
                v
 Dijkstra from depot and delivery stops
                |
                v
 Build shortest-path distance/path matrix
                |
                v
 Nearest-Neighbor TSP tour construction
                |
                v
 Parcel manifest + road route + distance
```

The implementation is divided into focused modules:

| Module | Responsibility |
|---|---|
| `parcels.py` | Parcel data structures, dataset loading and generation utilities |
| `sorting.py` | Custom Merge Sort for parcel ordering |
| `knapsack.py` | 0/1 Knapsack dynamic programming and selected-item recovery |
| `graph.py` | Weighted graph representation and Dijkstra shortest paths |
| `tsp.py` | Nearest-Neighbor delivery-stop ordering and route construction |
| `main.py` | Integration of the complete planning pipeline |
| `benchmark.py` | Runtime measurement and chart generation |
| `data/small.json` | Small demonstration instance: 10 parcels and 8 nodes |
| `data/large.json` | Larger demonstration instance: 500 parcels and 100 nodes |

## 4. Algorithm Design and Analysis

### 4.1 Parcel Ordering – Merge Sort

**Paradigm:** Divide and Conquer  
**Module:** `sorting.py`

Merge Sort recursively divides the parcel list into smaller sublists, sorts each sublist and merges the sorted results. The comparison order is deadline ascending and priority descending; the implementation also uses a deterministic identifier tie-break.

For an input of `N` parcels, the recurrence is:

\[
T(N) = 2T(N/2) + \Theta(N)
\]

By the Master Theorem, the time complexity is:

\[
\boxed{\Theta(N\log N)}
\]

The auxiliary space complexity is `O(N)` for the temporary lists used during merging. Merge Sort is stable when equal-key elements are merged without changing their relative order. The implementation avoids relying on Python's built-in sorting routine for the core algorithm.

### 4.2 Parcel Selection – 0/1 Knapsack

**Paradigm:** Dynamic Programming  
**Module:** `knapsack.py`

A parcel must either be selected in full or not selected. Let:

- `N` be the number of parcels;
- `W` be the vehicle's integer weight capacity;
- `w_i` be the weight of parcel `i`;
- `v_i` be the priority value of parcel `i`;
- `DP[i][c]` be the maximum priority value obtainable from the first `i` parcels with capacity at most `c`.

The recurrence is:

\[
DP[i][c] =
\begin{cases}
0 & i=0\text{ or }c=0\\
DP[i-1][c] & w_i > c\\
\max(DP[i-1][c],\; DP[i-1][c-w_i]+v_i) & w_i\le c
\end{cases}
\]

The table is filled row by row. The selected parcels are then recovered by tracing backwards through the table and identifying rows where the optimal value changes.

- **Time complexity:** `O(NW)`.
- **Space complexity:** `O(NW)` for the two-dimensional table retained for reconstruction and display.

This is pseudo-polynomial because the running time depends on the numeric capacity `W`, not only on the number of input parcels. The method assumes parcel weights and capacity are represented in compatible integer units.

### 4.3 Shortest Road Paths – Dijkstra's Algorithm

**Paradigm:** Greedy shortest-path algorithm  
**Module:** `graph.py`

The road network is a weighted graph. Dijkstra's algorithm repeatedly selects the unsettled vertex with the smallest known tentative distance and relaxes its outgoing edges. A min-priority queue implemented with Python's `heapq` is used to select the next vertex efficiently. Predecessor information is retained so that a shortest path can be reconstructed, including intermediate road junctions.

Dijkstra's algorithm requires non-negative edge weights. With an adjacency-list representation and a binary heap, the commonly stated time complexity per source is:

\[
O((V+E)\log V)
\]

where `V` is the number of graph vertices and `E` is the number of edges. The application runs Dijkstra from the depot and the distinct selected delivery nodes to obtain the pairwise distances needed by the route planner. If there are `K` distinct delivery nodes, this requires up to `K+1` single-source runs, giving the bound:

\[
O((K+1)(V+E)\log V)
\]

The distance and predecessor/path results are stored for later route construction. This is a repeated single-source computation over selected locations, not a full all-pairs computation over every possible source unless every graph vertex is selected.

### 4.4 Delivery-Stop Ordering – Nearest-Neighbor TSP

**Paradigm:** Greedy approximation heuristic  
**Module:** `tsp.py`

The Traveling Salesperson Problem asks for a minimum-cost closed tour that visits each required stop. Finding an optimal tour is computationally expensive as the number of stops grows. The project uses the Nearest-Neighbor heuristic:

1. Start at depot node `0`.
2. Among unvisited delivery stops, choose the stop with the smallest distance from the current stop.
3. Move to that stop and mark it visited.
4. Repeat until all required stops have been visited.
5. Return to the depot.

If the distance matrix contains `K` delivery stops, repeatedly scanning the unvisited stops gives `O(K^2)` route-selection time. The planner uses the shortest-path distances produced by Dijkstra, and the corresponding road paths are concatenated to produce a junction-by-junction navigation sequence.

Nearest Neighbor is a heuristic, not an exact TSP solver. It can produce a valid tour without proving that the tour is globally shortest. Its result depends on the distance matrix and the order in which ties are resolved. The route should therefore be described as a **Nearest-Neighbor approximate tour**, not an optimal route.

## 5. Experimental Setup

The following results were captured from the user's Windows command-line execution on 13 November 2026. The Python executable path shown in the command output was `C:\Python314`, indicating Python 3.14. The command output did not identify the processor model, so no specific CPU model is claimed here.

The benchmark uses `time.perf_counter()` and measures each algorithmic stage separately. The benchmark code runs five trials per problem size and reports the arithmetic mean for each stage. It evaluates generated problem instances with five parcel counts: 10, 50, 100, 200 and 500.

**Important measurement note:** the reported pipeline total is calculated by adding the mean stage times. It is not a separately timed end-to-end execution of the complete application. Small timing differences are expected across machines and repeated runs.

## 6. Experimental Results

### 6.1 Generated-Instance Scaling Benchmark

The following values are transcribed from the execution output produced by:

```bash
python -m courier_planner.benchmark
```

| Parcels (N) | Nodes (V) | Capacity (W) | Merge Sort (ms) | Knapsack (ms) | Dijkstra (ms) | TSP NN (ms) | Sum of stage means (ms) |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 10 | 8 | 25 | 0.0174 | 0.0444 | 0.0539 | 0.0075 | 0.1232 |
| 50 | 10 | 25 | 0.0560 | 0.1114 | 0.0564 | 0.0054 | 0.2292 |
| 100 | 20 | 33 | 0.0854 | 0.2079 | 0.2007 | 0.0107 | 0.5046 |
| 200 | 40 | 66 | 0.1885 | 0.8744 | 0.9360 | 0.0312 | 2.0300 |
| 500 | 100 | 166 | 0.5972 | 6.1248 | 9.4065 | 0.1579 | 16.2863 |

The generated 500-parcel case uses a capacity of 166 kg because the benchmark generator derives capacity from the requested parcel count. This is a separate experiment from the saved `large.json` dataset, whose capacity is 150 kg.

### 6.2 Saved Dataset Results

The benchmark also loads the two saved JSON datasets and measures their algorithm stages. The values below are from the same command execution:

| Dataset | Available parcels | Graph nodes | Capacity | Merge Sort (ms) | Knapsack (ms) | Dijkstra (ms) | TSP NN (ms) | Sum of stage means (ms) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `small.json` | 10 | 8 | 25 kg | 0.0088 | 0.0200 | 0.0445 | 0.0072 | 0.0805 |
| `large.json` | 500 | 100 | 150 kg | 0.5580 | 5.1797 | 8.6152 | 0.1401 | 14.4930 |

These saved-dataset measurements are not expected to match the generated-instance measurements exactly. In particular, the large saved dataset has a capacity of 150 kg, while the generated 500-parcel benchmark has a capacity of 166 kg. The inputs and therefore the selected destinations and routing workload differ.

### 6.3 Functional Output from the Saved Datasets

The application was also run directly on both saved datasets:

```bash
python -m courier_planner.main --dataset small
python -m courier_planner.main --dataset large
```

The captured outputs reported:

| Result | `small.json` | `large.json` |
|---|---:|---:|
| Available parcels | 10 | 500 |
| Selected parcels | 7 | 85 |
| Total selected priority | 129 points | 2,914 points |
| Vehicle capacity used | 25 / 25 kg | 150 / 150 kg |
| Distinct delivery destinations | 6 | 55 |
| Round-trip tour distance | 122 km | 259 km |

For the small dataset, the reported stop order was:

`Depot(0) → Node 1 → Node 6 → Node 2 → Node 3 → Node 7 → Node 4 → Depot(0)`

For the large dataset, the application reported a tour visiting 55 distinct delivery destinations before returning to depot node `0`. The full stop sequence and road-junction traversal are printed by the application during execution.

The output label `READY FOR DISPATCH` is the application's current summary message. It should be interpreted as the pipeline having generated a parcel selection and route; the current model does not independently prove deadline feasibility or real-world delivery feasibility.

## 7. Interpretation of Results

1. **Runtime increases with input scale.** The generated-instance stage-time sum rises from `0.1232 ms` for 10 parcels to `16.2863 ms` for 500 parcels in the captured run.
2. **Knapsack cost increases with both parcel count and capacity.** Its theoretical work is proportional to `N × W`; therefore, changing capacity between benchmark sizes affects the measured time as well as changing the number of parcels.
3. **Dijkstra is the largest measured stage in the larger generated cases.** For the 500-parcel generated case, Dijkstra accounts for approximately 57.8% of the sum of stage means (`9.4065 / 16.2863`). In the saved `large.json` run, it accounts for approximately 59.4% (`8.6152 / 14.4930`).
4. **Nearest-Neighbor route selection is comparatively inexpensive in these tests.** It takes `0.1579 ms` in the generated 500-parcel case and `0.1401 ms` for the saved large dataset. The cost of constructing the shortest-path matrix is measured separately under Dijkstra.
5. **The tour is approximate.** The reported distances are the distances of the tours produced by the current heuristic. No exact TSP baseline was run, so the percentage gap from an optimal tour is not known.

The benchmark chart `runtime.png` is generated by the existing benchmark script. The script plots measured stage runtimes against parcel count and a stacked view of the stage-time contributions. The chart should be interpreted as an empirical view of these particular test instances, not as proof of asymptotic complexity by itself.

## 8. Limitations and Possible Future Improvements

The current prototype demonstrates the required algorithmic building blocks, but it simplifies several real courier-planning constraints:

- **Deadlines are used for sorting, not enforced as time windows.** The current Knapsack objective maximizes priority value and does not calculate whether each parcel can arrive before its deadline.
- **The route is heuristic.** Nearest Neighbor does not guarantee the shortest possible TSP tour. A 2-Opt improvement pass could be implemented and evaluated as future work, but it is not part of the current measured implementation.
- **Travel costs are static.** The graph uses fixed edge distances and does not model traffic, time-dependent travel, road closures or service times.
- **Vehicle constraints are simplified.** The current selection model uses a single weight capacity and does not model parcel dimensions, vehicle volume, multiple vehicles or pickup-and-delivery constraints.
- **Benchmark results are environment-dependent.** Timings are very small and can be affected by processor load, Python version, caching and measurement overhead. Repeated trials and consistent hardware/software conditions are important for fair comparisons.
- **No exact-route comparison was measured.** The current report therefore does not claim a numerical optimality gap for Nearest Neighbor.

Potential extensions include time-window-aware routing, multiple vehicles, traffic-aware edge weights, 2-Opt post-processing and comparisons against an exact TSP solver on small instances. These should be implemented and measured before being reported as completed features.

## 9. Conclusion

The Mini-Courier Planner integrates four important algorithmic techniques into a single courier-planning workflow: Merge Sort for parcel ordering, 0/1 Knapsack dynamic programming for capacity-constrained parcel selection, Dijkstra's algorithm for shortest road paths and Nearest-Neighbor TSP for approximate delivery-stop ordering.

In the captured Windows execution, the application processed the saved 500-parcel dataset, selected 85 parcels within a 150 kg capacity, identified 55 distinct delivery destinations and generated a 259 km round-trip tour. The generated 500-parcel benchmark reported a sum of stage means of 16.2863 ms; the saved large dataset benchmark reported 14.4930 ms. These are separate experiments with different capacities and input instances.

The project demonstrates the integration and practical behavior of the selected algorithms while making the limitations of the simplified model explicit. In particular, the generated Nearest-Neighbor tour is an approximation, and parcel deadlines are not currently enforced as delivery time windows.
