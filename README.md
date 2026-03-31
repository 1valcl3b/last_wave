# WAVE - Multiple load generator for computer network experimentation

Experimentation is fundamental in computer networks research, especially for validating hypotheses in controlled scenarios. In this context, this work presents a new version of WAVE (Workload Assay for Verified Experiments) integrated with Mininet, a widely used network emulator. This integration allows researchers to have greater control over the network environment where the generated traffic will be evaluated, enabling the configuration of network characteristics such as delay and packet loss. Currently, WAVE supports the linear and tree topologies, which are configured through user-defined parameters, allowing greater flexibility in the creation of experimental scenarios.

##  README Structure

- **Seals Considered**: describes the artifact evaluation criteria.
- **Project information**: useful links, including user manual, previous work, and demonstration videos.
- **Basic information**: presents the hardware and software requirements needed for execution.
- **Dependencies**: lists the tools and libraries used.
- **Installation and running**: describes how to configure and start the environment.
- **Security concerns**: describes potential risks and safe execution practices.
- **Minimum Test**: presents a simple scenario to validate the installation.
- **Ending the WAVE Execution**: describes how to properly terminate the environment.

## Seals Considered

The seals considered for this artifact are:

- **Available**
- **Functional**
- **Reproducible**

## Project information

This section provides useful resources related to the WAVE tool, including documentation, previous publications, and demonstration videos 

[WAVE User Manual](WAVE_User_Manual.pdf)

[Salão de Ferramentas SBRC 2025 (previous work)](https://doi.org/10.5753/sbrc_estendido.2025.6301)

[Demonstrative videos of the WAVE tool](https://drive.google.com/drive/folders/1E3_Gj1HX8jhLEx9tRARIDYxlm8bzkNN3?usp=drive_link)

## Basic information

- CPU: 4 cores or higher
- Memory: at least 8 GB RAM
- Storage: at least 10 GB of free space

### Operating System

WAVE has been tested on Linux-based systems, especially:

- Ubuntu 22.04 or higher

### Environment Overview

WAVE integrates multiple technologies for network experimentation:

- Docker containers for service orchestration
- Mininet for network emulation
- Grafana for metrics visualization
- Vagrant and VirtualBox for optional virtual machine provisioning

## Dependencies

To run WAVE, the following dependencies are required:

- **Python 3** (version 3.11 or higher)
- **Virtualenv** (version 3.11 or higher)
- **Docker** (version 27.x or higher)
- **Docker Compose** (version 2.32.x or higher)
- **Mininet** (installation via the official website is recommended)
- **VirtualBox** (version 7.1.6 or higher)
- **Vagrant** (version 2.3.4 or higher)

## Security concerns

WAVE uses technologies that may impact the host system, such as Docker and Mininet.

- Mininet may modify system network configurations.
- Docker may run with elevated privileges depending on the configuration.

### Recommendations

- Avoid running in production environments
- Ensure the user has appropriate permissions
- Monitor CPU and memory usage during experiments

No critical risks were identified, provided that the best practices above are followed.

## Checking the Required Requirements

### Checking if Python3 is installed and it's version:

![wave-version-python3](./screenshots/wave-version-python32.png)

### Additionally, the VirtualEnv virtual environment is required:

![wave-version-venv](./screenshots/wave-version-venv2.png)

### Checking the Docker and docker compose components:

![wave-version-docker](./screenshots/wave-version-docker2.png)

![wave-version-docker-compose](./screenshots/wave-version-docker-compose2.png)

### Checking what version of Virtualbox is installed:

![wave-version-virtualbox](./screenshots/wave-version-virtualbox2.png)

### Checking what version of Vagrant is installed:

![wave-version-vagrant](./screenshots/wave-version-vagrant2.png)

### Checking what version of Mininet is installed

![wave-version-mininet](./screenshots/wave-version-mininet.png)

We recommend installing Mininet from the official website, as it provides the most up-to-date version:  
https://mininet.org/download/

Although Mininet can also be installed using `apt install mininet`, the version available in the distribution repositories may not be the most recent one.


The versions shown in the figures were those tested at the time of this manual's creation.

## Installation and running

### Cloning the official repository and starting the system:

```
$ git clone https://github.com/1valcl3b/last_wave.git
$ cd last_wave/wave
$ ./app-compose.sh --start
```

### Checking the execution in a Docker enviroment:

![wave-cli-docker](./screenshots/wave-cli-docker2.png)

As can be seen in the figure above, the WAVE Initialization module uses two containers for its execution: wave-app and grafana-oss. On the left side of the figure, we have the output of the WAVE startup command.

### The WAVE Web module can be accessed via a browser. We recommend using Google Chrome or another Chromium-based browser for better compatibility.

![wave-web-home](./screenshots/wave-configurator-2026.png)

The form contains fields for entering network data for both the traffic load source and destination. In addition to specifying the IP address, the user can choose how the environment will be provisioned, either through a container or a virtual machine, with configurable memory size and number of virtual CPUs. It is also possible to configure the network topology through user-defined parameters. Currently, the WAVE supports linear and tree topologies. Finally, the user can select which workload model to apply, such as sinusoid, flashcrowd, or step, and optionally enable the use of micro-burst traffic.

## Minimum Test

This test aims to validate whether the environment has been correctly configured.

### Procedure

1. Clone the repository:

```
$ git clone https://github.com/1valcl3b/last_wave.git
$ cd last_wave/wave
```

2. Start the environment:

```
$ ./app-compose.sh --start
```

3. Verify that the containers are running:

```
$ docker ps
```

It is expected that the containers `wave_app`, `node-exporter`, and `grafana-oss` are active.

4. Access the web interface in the browser (use Chrome or Brave):

```
http://localhost
```

5. Configure a simple experiment:

- Platform: VM
- Topology: Linear
- Number of switches: 5
- Workload model: stair step

6. Execute the experiment.

7. Return to the terminal to enter the root password (Mininet requires root privileges; you can configure the visudo file to avoid password prompts)

8. After entering the password, you can return to the WEB interface

### Expected result

- The environment will be provisioned (this may take some time)
- The results web interface should appear
- Metrics should be visualized through charts

If all steps are completed successfully, the environment is ready for use. If any issues are encountered while starting or terminating the environment, we recommend consulting the demonstration videos available in the Project Information section. In particular, the first video provides a complete walkthrough of the tool execution.

## Ending the WAVE Execution

### Finalizing and removing the container environment:

```
$ ./app-compose.sh --destroy
```

By running the command above, the user terminates the WAVE WEB module and removes the containers responsible for the other initiated modules. To restart the entire system, simply execute the same command, replacing the --destroy argument with --start.
