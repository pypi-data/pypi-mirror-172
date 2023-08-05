[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![linting](https://github.com/bacrossland/thermometerb/actions/workflows/lint.yml/badge.svg?event=push)
![testing](https://github.com/bacrossland/thermometerb/actions/workflows/python-app.yml/badge.svg?event=push)

# Thermometer B 
Thermometer B is a Python package example of a Thermometer class that has
notifications on reaching temperature thresholds. Boiling and freezing point
thresholds plus when to trigger notifications can be customized when an instance
of the class is instantiated or after when providing a temperature reading.

Documentation for the 
[Thermometer class](https://bacrossland.github.io/thermometerb/thermometer.html#thermometerb.Thermometer)

# Install and Usage

```shell
pip install theremometerb
```

In your Python application, import Thermometer and configure the notification
thresholds you want.

The thresholds can be set when the object is created or after.

```python
from thermometerb import Thermometer

when_created = Thermometer(full_degree=True, increase=True)
after_created = Thermometer()
after_created(10.0, decrease=True, boil=101.0)

```

Threshold options are as follows:

| Option      | Description                                                                                                                      | Default |
|-------------|----------------------------------------------------------------------------------------------------------------------------------|---------|
| boil        | Float of temperature threshold in Celsius for boiling.                                                                           | 0.0     |
| freeze      | Float of temperature threshold in Celsius for freezing.                                                                          | 100.0   |
| full_degree | Bool if a notification should only be sent when a threshold has been exceeded by a full degree point (whole number not decimal). | False   |
| increase    | Bool if a notification should only be sent if previous temp was an increase to reach boil/freeze threshold.                      | False   |
| decrease    | Bool if a notification should only be sent if previous temp was a decrease to reach boil/freeze threshold.                       | False   |

** Note **
If the temperature is unchanged, no notification is sent as the threshold 
was already met.


Example application (more can be found in the [examples](examples) folder):

```python
"""Basic Thermometer that prints out when it hits the
    default boiling and freezing points.
"""
from thermometerb import Thermometer

temp_range = [99.0, 97.0, 98.0, 100.0, 101.5, 20.0, 5.0, 0.0, -10.0]
thermometer = Thermometer()

for temp in temp_range:
    thermometer(temp)
    if thermometer.notification():
        print(thermometer.notification())

```

# Development

To develop on Thermometer B, you will need to install python, clone this 
repository locally, then install requirements.

Python version: 3.10+

#### installing requirements

```shell
pip install -r requirements.txt
```

#### installing local develop package

Installing the Thermometer B package in development mode is not necessary
for develop. However, it can come in handy when working on additional example
applications or debugging an issue not reproducible through testing.

After cloning this repository, run at the root of the project:

```shell
pip install -e .
```

To uninstall, follow the same uninstall as for a regularly install pip package.

```shell
pip uninstall -y thermometerb
```


# Testing

Tests are written in [Pytest](https://docs.pytest.org/en/7.1.x/) and stored 
in the [tests](tests) folder. 

To run them [install requirements](#installing-requirements) as described 
above then run pytest.

```shell
pytest
```



