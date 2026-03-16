# WAVE - Multiple load generator for computer network experimentation

[WAVE User Manual](WAVE_User_Manual.pdf)

[Salão de Ferramentas SBRC 2025 (previous work)](https://doi.org/10.5753/sbrc_estendido.2025.6301)

[Demonstrative videos of the WAVE tool](https://drive.google.com/drive/folders/1E3_Gj1HX8jhLEx9tRARIDYxlm8bzkNN3?usp=drive_link)

Experimentation is fundamental in computer networks research, especially for validating hypotheses in controlled scenarios. In this context, this work presents a new version of WAVE (Workload Assay for Verified Experiments) integrated with Mininet, a widely used network emulator. This integration allows researchers to have greater control over the network environment where the generated traffic will be evaluated, enabling the configuration of network characteristics such as delay and packet loss. Currently, WAVE supports the linear and tree topologies, which are configured through user-defined parameters, allowing greater flexibility in the creation of experimental scenarios.

This repository is organized into three main sections: requirements, download and initialization, and finalization of the new WAVE tool.

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

## Downloading the Code and Starting the Environment

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

![wave-web-home](./screenshots/wave-configurator2026.png)

The form contains fields for entering network data for both the traffic load source and destination. In addition to specifying the IP address, the user can choose how the environment will be provisioned, either through a container or a virtual machine, with configurable memory size and number of virtual CPUs. It is also possible to configure the network topology through user-defined parameters. Currently, the WAVE supports linear and tree topologies. Finally, the user can select which workload model to apply, such as sinusoid, flashcrowd, or step, and optionally enable the use of micro-burst traffic.

## Ending the WAVE Execution

### Finalizing and removing the container environment:

```
$ ./app-compose.sh --destroy
```

By running the command above, the user terminates the WAVE WEB module and removes the containers responsible for the other initiated modules. To restart the entire system, simply execute the same command, replacing the --destroy argument with --start.
