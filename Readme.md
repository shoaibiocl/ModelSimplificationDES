## Data Generation & Simulation Testbeds

This repository utilises discrete-event simulation (DES) models built with the `salabim` library to generate empirical data. 
These datasets capture how changes in server utilisation and network architecture impact event trace counts and wall-clock execution times. 

## Description of each file is detailed below.

### 1. 2-Stage Tandem Queue Number of Instructions Generator (`generate_data_2stage_parent.py`)
This script executes an automated parameter sweep across a sequential queueing pipeline to measure **event trace density** as a proxy for structural computational load.

* **Systems:** $M/M/1, M/G/1,$ and $G/G/1$
* **Experimental Setup:** Sweeps through target server utilisation values from **20% to 92%** (in 1% steps), running **n replications** per step. Each run discards a 200-day warmup period before collecting event data over a 5-day window.
* **Target Metric Extracted:** Parses the `salabim` environment trace logs and calculates the mean **Instructions per Arrival**.
* **Output:** Saves the results to `data/raw/2StageMG1_v1.xlsx`.


### 2. 3-Stage System for Validation Experiment 2 (`generate_data_3stage_branched_parent.py`)
This script models a complex network topology featuring stochastic routing and alternative service distributions to directly record true **wall-clock execution runtimes**.

* **System:** 3-stage tandem queuing system with two parallel subsystems in the third stage.
* * **Arrivals:** Any distribution can be used. 
  * **Stages 1 & 2:** Two single servers in tandem, users can input any distribution of choice.
  * **Branching Mechanics:** Entities split stochastically post-Stage 2 based on a $40 / 60$ probability split. Users can custom change the split.
* **Experimental Setup:** Evaluates different utilisation values ranging from ($20\%$) to high saturation ($92\%$), running **30 independent replications** per profile. Each run uses a 180-day warmup phase followed by a massive **365-day production window**.
* **Target Metric Extracted:** Uses Python's `time` library to measure empirical **CPU execution runtime** (seconds) alongside server physical occupancy and path throughput.
* **Output Asset:** Saves the dataset matrix to `3-stage-GG1-parent.xlsx`.

## Statistical Validation & Sensitivity Analysis

### 3. Sampling Sensitivity Engine (`test-sampling-sensitivity.py`)
Before using the generated event trace logs to train predictive frameworks, this script runs a sensitivity experiment. It verifies whether changing the scale of entity sampling significantly affects the: **Instructions per Arrival**.

* **Statistical Methodology:** * **One-Way ANOVA:** Executes a parametric analysis of variance across different sampling tiers to test the null hypothesis ($H_0$) that the sample size does not inherently bias the recorded instruction means.
  * **95% Confidence Interval (CI) Estimation:** Computes the standard error of the mean (SEM) for each sample bracket and applies a Student’s t-distribution critical value to map precise interval bounds:
  $$\text{CI} = \bar{x} \pm \left(t_{\alpha/2, \, df} \times \text{SEM}\right)$$
* **Input Data:** Reads empirical tracking categories from `data/raw/ModelSimplification-NI-Sensitivity.xlsx` (Sheet 2), where each column represents a different sample size threshold.
* **Visual Artifact:** Automates the creation of a high-contrast validation plot detailing the variance, mean markers, and overlapping interval whiskers for each group.


