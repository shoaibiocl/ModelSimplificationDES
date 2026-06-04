## Data Generation & Simulation Testbeds

This repository utilises discrete-event simulation (DES) models built with the `salabim` library to generate empirical data. 
These datasets capture how changes in server utilisation and network architecture impact event trace counts and wall-clock execution times. 

The following two core "parent" models represent baseline complex systems before runtime reduction or simplification frameworks are applied:

### 1. 2-Stage Tandem Queue Generator (`generate_data_2stage_parent.py`)
This script executes an automated parameter sweep across a sequential queueing pipeline to measure **event trace density** as a proxy for structural computational load.

* **Systems:** $M/M/1, M/G/1, & G/G/1$
* **Experimental Setup:** Sweeps through target server utilisation values from **20% to 92%** (in 1% steps), running **n replications** per step. Each run discards a 200-day warmup period before collecting event data over a 5-day window.
* **Target Metric Extracted:** Parses the `salabim` environment trace logs and calculates the mean **Instructions per Arrival**.
* **Output:** Saves the results to `data/raw/2StageMG1_v1.xlsx`.


### 2. 3-Stage Branched Network Generator (`generate_data_3stage_branched_parent.py`)
This script models a complex network topology featuring stochastic routing and alternative service distributions to directly record true **wall-clock execution runtimes**.

* **System:** 3-stage tandem queuing system with two parallel subsystems in the third stage.
* * **Arrivals:** Any distribution can be used. 
  * **Stages 1 & 2:** Two single servers in tandem, users can input any distribution of choice.
  * **Branching Mechanics:** Entities split stochastically post-Stage 2 based on a $40 / 60$ probability split. Users can custom change the split.
* **Experimental Setup:** Evaluates different utilisation values ranging from ($20\%$) to high saturation ($92\%$), running **30 independent replications** per profile. Each run uses a 180-day warmup phase followed by a massive **365-day production window**.
* **Target Metric Extracted:** Uses Python's `time` library to measure empirical **CPU execution runtime** (seconds) alongside server physical occupancy and path throughput.
* **Output Asset:** Saves the dataset matrix to `3-stage-GG1-parent.xlsx`.

---

## Generated Dataset Schemas

The scripts output highly structured matrices containing the following operational features:

| Output Data File | Feature Name | Description | Role in Prediction |
| :--- | :--- | :--- | :--- |
| **`2StageMG1_v1.xlsx`** | `Inter arrival time` | Input traffic intensity factor. | Predictor (Feature) |
| | `Server 1/2 utilisation` | Mean operational occupancy of servers. | Predictor (Feature) |
| | `Instructions per arrival` | Processed event trace log density. | **Target Variable** |
| **`3-stage-GG1-parent.xlsx`** | `Server 1/2/3/4 utilisation`| Measured physical load across all nodes. | Predictor (Feature) |
| | `Total / System 3 / System 4 Arrivals` | Total throughput and route-specific entity counts. | Predictor (Feature) |
| | `Run time` | Empirical wall-clock execution speed (seconds). | **Target Variable** |

