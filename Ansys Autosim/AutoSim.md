# Ansys AutoSim

[![Static Badge](https://img.shields.io/badge/ansys-PyAEDT-green)](https://github.com/ansys/pyaedt/)

```sh
pip install pyaedt
```

## Usage


`sleepSlot`: Time interval between simulations, in seconds. May be necessary if CPU heat dissipation is a problem.

`outputDir`: Where to put the output data.

`planPath`: Where to find the the simulation plan. An example is given as `AutoSimPlan_exp.csv`

`projectPath`: Where to locate the .aedt Ansys project file.

`designName`: Name of the target design under the project.

`setupName`: Name of the analyse setup, the default name is "Setup1".

`plotName`: Name of the plot to extract simulation result.