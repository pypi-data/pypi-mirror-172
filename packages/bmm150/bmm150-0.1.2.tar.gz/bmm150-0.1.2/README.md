# BMM150

A pure python API for the bmm150 magnetic sensor.

> Note : Most code logic comes from one of the following repos : [Seed-Studio/Grove_3_Axis_Compass_V2.0_BMM150](https://github.com/Seeed-Studio/Grove_3_Axis_Compass_V2.0_BMM150) or [BoschSensortec/BMM150-Sensor-API](https://github.com/BoschSensortec/BMM150-Sensor-API) . This is mostly a transpilation and a python packaging of this code.

# Installation

The easiest way to install this library is using pip:

```bash
pip install bmm150
```

# Documentation

The documentation is built using sphinx and the readthedocs theme. You can find it on the [readthedocs official website](https://bmm150.readthedocs.io/).

# Usage

The following code initializes the sensor, and prints the magnetic field values for x, y and z.
Then, using the `atan2` function from the `math` standard library, it retrieves the heading of the sensor.

```python
import bmm150
import math

device = bmm150.BMM150(bus=1)  # Bus number will default to 1

device.initialize()

x, y, z = device.read_mag_data()

heading = math.atan2(x, y)

print("X : {x}µT")
print("Y : {y}µT")
print("Z : {z}µT")

print("Heading: {heading}°")
```

# Development

This library uses poetry as a development tool.

You can start development by running :

```bash
poetry install
```

# Testing

You can test this library using :

```bash
poetry run pytest
```

# Tox

You cant test multiple python versions using tox :

```bash
poetry run tox
```