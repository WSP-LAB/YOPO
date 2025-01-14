YOPO Artifact
========

YOPO is an attack framework designed to generate a universal adversarial
perturbation that deceives machine learning-based ATS blockers in a
cost-effective manner. YOPO acheives high attack success rates agaisnt
four ML-based ATS blockers with a single perturbation. For more details,
please refer to our [paper](https://godeastone.github.io/papers/shin-acsac24.pdf),
"You Only Perturb Once: Bypassing (Robust) Ad-Blockers Using Universal 
Adversarial Perturbations", which appeared in ACSAC 2024.

## Hardware requirements

YOPO requires a Linux machine with an NVIDIA GPU. Due to its use of multiple
processes for parallel HTML file manipulation, we recommend a machine with at
least 32 CPU cores, 256 GB of system memory, and 300 GB of disk space. Our tests were conducted on a machine running Ubuntu 22.04 (64-bit).

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

## Usage

### Step 1: Launch the Docker container

Build the Docker image using the provided Dockerfile and start a Docker
container.

```
$ git clone https://github.com/WSP-LAB/YOPO.git
$ cd scripts
$ ./build.sh && ./launch_container.sh
```

### Step 2: Install the mitmproxy CA certificate

Install the CA certificate for `mitmproxy`, which we use to test
whether modified HTML/JS files can bypass the target ATS blockers.

```
$ cd scripts
$ ./apply_mitmproxy_certificates.sh
```

### Step 3: Save HTML files

Before crawling webpages, save the HTML files, as YOPO needs them for perturbation.

```
$ cd scripts/crawler
$ ./save_html.sh
```

### Step 4: Run ML-based ATS blockers

Run the target ATS blockers by executing the `crawl_adblocker.sh` script,
passing the name of the target ATS blocker.
Each ATS blocker crawls the saved HTML files and extracts features.
  * TARGET: `adgraph`, `webgraph`, `adflush`, `pagegraph`
```
$ cd scripts/crawler
$ ./crawl_adblocker.sh [TARGET]
```

### Step 5: Train ML-based ATS blockers

Train the target ATS blockers using extracted features by running the `train_adblocker.sh` script.
```
$ cd scripts/crawler
$ ./train_adblocker.sh [TARGET]
```

### Step 6: Train surrogate models

Generate training data and train a surrogate model for each target ATS blocker by execute the `train_surrogate.sh` script.

```
$ cd scripts
$ ./train_surrogate.sh [TARGET]
```

### Step 7: Perform the attack
To run the attack pipeline, execute the script `run_attack` by passing the following arguments:
  * EPSILON: `5`, `10`, `20`, `40`
  * COST_MODEL_TYPE: `DC`, `HSC`, `HCC`, `HJC`
  * TARGET: `adgraph`, `webgraph`, `adflush`, `pagegraph`

The attack success rates and costs are saved in the `/yopo-artifact/result` directory.
```
$ cd scripts
$ ./attack_pipeline_one_setting.sh [EPSILON] [COST_MODEL_TYPE] [TARGET]
```


## Authors
This research project has been conducted by [WSP Lab](https://wsp-lab.github.io/)
at KAIST.

* [Dongwon Shin](https://godeastone.github.io/)
* [Suyoung Lee](https://leeswimming.com/)
* [Sanghyun Hong](https://sanghyun-hong.com/index.html)
* [Sooel Son](https://sites.google.com/site/ssonkaist/home)

## Citation
To cite our paper:
```bibtex
@INPROCEEDINGS{shin:acsac:2024,
  author = {Dongwon Shin and Suyoung Lee and Sanghyun Hong and Sooel Son},
  title = {You Only Perturb Once: Bypassing (Robust) Ad-Blockers Using Universal Adversarial Perturbations},
  booktitle = {Proceedings of the Annual Computer Security Applications Conference},
  pages = {190--206},
  year = 2024
}
```
