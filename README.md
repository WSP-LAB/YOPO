YOPO Artifact
========

YOPO is an attack framework designed to generate a universal adversarial
perturbation that deceives machine learning-based ATS blockers in a
cost-effective manner. This repository provides a Docker image to facilitate the
evaluation processes outlined in Section 5.2 of our paper, enabling the
reproduction of Table 3 and Figure 2. This artifact includes crawled HTML files,
features extracted from these HTML files, pre-trained target ATS blockers, and
the YOPO source. The Docker image and scripts were tested on an Ubuntu 22.04
host machine.

## Hardware requirements

YOPO requires a Linux machine with an NVIDIA GPU. Due to its use of multiple
processes for parallel HTML file manipulation, we recommend a machine with at
least 32 CPU cores, 256 GB of system memory, and 300 GB of disk space. For
surrogate model training and UAP optimization, a GPU with a minimum of 12 GB
memory is required. Our tests were conducted on a machine equipped with two
Intel Xeon Gold 6348 CPUs (112 cores total), four NVIDIA RTX 3090 GPUs (each
with 24 GB memory), and 768 GB DRAM, running Ubuntu 22.04 (64-bit).


## Installation

To run our scripts, the following software dependencies must be installed:

1. Docker

  Install Docker by following the instructions
  [here](https://docs.docker.com/engine/install/).

2. Run Docker without root privileges

  Our scripts are designed to avoid requiring root privileges. To manage Docker
  as a non-root user, follow the instructions
  [here](https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user).

3. CUDA Toolkit 12.4

  YOPO is tested with CUDA Toolkit 12.4. Please install CUDA Toolkit 12.4 from
  this [link](https://developer.nvidia.com/cuda-12-4-0-download-archive). If
  using a different CUDA version, update the base image in the Dockerfile
  accordingly. Available base images can be found
  [here](https://hub.docker.com/r/pytorch/pytorch/tags).

4. NVIDIA Container Toolkit

  To enable GPU access within Docker containers, install the NVIDIA Container
  Toolkit by following the guide
  [here](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html).


## Dataset

1. HTML files

  We crawled HTML files from Tranco’s Top-10K websites, resulting in 7,907 HTML
  files stored in the `data/rendering_stream/html` directory.

2. Extracted features

  Since extracting features from the entire 450K+ network requests in our
  dataset is time-consuming, we conduct this process in advance and provide a
  separate CSV file where each line contains the features extracted from a
  network request. These files can be found in the
  `scripts/dataset/from_adgraph`, `scripts/dataset/from_webgraph`, and
  `scripts/dataset/from_adflush` directory.

3. Target ATS blockers

  We trained the AdGraph, WebGraph, and AdFlush classifiers using our dataset
  of HTML files crawled from Tranco’s Top-10K websites. The trained models are
  included in the `scripts/saved_model_adgraph`, `scripts/saved_model_webgraph`,
  and `scripts/saved_model_adflush` directory.


## Running Experiments

Our artifact is designed to facilitate the evaluation processes in Section 5.2
and to reproduce Table 3 and Figure 2 from our paper.


### Step 1: Launch the Docker container

Build the Docker image using the provided Dockerfile and start a Docker
container. This step takes approximately 30 minutes on our machine.

```
$ cd scripts
$ ./build.sh && ./launch_container.sh
```

### Step 2: Install the mitmproxy CA certificate

Assuming you are inside the Docker container, install the CA certificate for
`mitmproxy`, which we use to test whether modified HTML/JS files can bypass the
target ATS blockers. This step finishes instantly.

```
$ cd scripts
$ ./apply_mitmproxy_certificates.sh
```

### Step 3: Train surrogate models

Generate training data and train a surrogate model for each target ATS blocker.
This process, detailed in Sections 4.1 and 4.2 of our paper, takes approximately
30 minutes on our machine.

```
$ cd scripts
$ ./train_surrogate_model.sh
```

### Step 4-1: Perform the attack using all configurations

For all configurations in Table 3, this step crafts a UAP, manipulates the HTML
files associated with each target network request, and extracts features from
the modified HTML files. Please note that this step takes about 480 hours on our
machine.

```
$ cd scripts
$ ./attack_pipeline_all.sh
```

### Step 4-2: Perform the attack using one configuration
To reduce execution time, this script runs the UAP attack for a single
configuration. Depending on the attack configuration, this step takes up to 20
hours on our machine. To run this script, use the following arguments:
  * EPSILON: 5, 10, 20, 40
  * COST_MODEL_TYPE: DC, HSC, HCC, HJC
  * TARGET: adgraph, webgraph, adflush

```
$ cd scripts
$ ./attack_pipeline_one_setting.sh [EPSILON] [COST_MODEL_TYPE] [TARGET]
```

### Step 5: Compute the data for Table 3
Summarize the results of all conducted attacks, writing the summary to
`result/table_3.txt`. Ensure that all 36 attack configurations in Table 3 are
completed before running this script.

```
$ cd scripts
$ python compute_attack_result.py
```

### Step 6: Compute the data for Figure 2
Summarize the perturbation size of generated UAPs for the configurations in
Figure 2, writing the results to `result/figure_2.txt`. Ensure that all nine
attack configurations in Figure 2 are completed before running this script.

```
$ cd scripts
$ python compute_perturbation_size.py
```

## Threats to reproducibility

There are challenges in precisely replicating the experimental results. For
instance, features extracted from the same webpage may vary due to time lags, as
changes in remote resources can affect feature extraction. Additionally, the
surrogate model training and perturbation optimization processes may be
influenced by random factors, such as instances sampled for UAP optimization or
the CUDA seed.
