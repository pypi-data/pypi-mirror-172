.. thermometerb documentation master file, created by
   sphinx-quickstart on Sun Oct 16 11:55:21 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Thermometer B
========================================

Thermometer B is a Python package example of a Thermometer class that has
notifications on reaching temperature thresholds. Boiling and freezing point
thresholds plus when to trigger notifications can be customized when an instance
of the class is instantiated or after when providing a temperature reading.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   thermometer

Install
-------

.. code-block:: shell

   pip install theremometerb


In your Python application, import Thermometer and configure the notification
thresholds you want.

The thresholds can be set when the object is created or after.

.. code-block:: python

   from thermometerb import Thermometer

   when_created = Thermometer(full_degree=True, increase=True)
   after_created = Thermometer()
   after_created(10.0, decrease=True, boil=101.0)



Threshold Options
------------------
+-------------+----------------------------------------------------------------------------------------------------------------------------------+---------+
| Option      | Description                                                                                                                      | Default |
+=============+==================================================================================================================================+=========+
| boil        | Float of temperature threshold in Celsius for boiling.                                                                           | 0.0     |
+-------------+----------------------------------------------------------------------------------------------------------------------------------+---------+
| freeze      | Float of temperature threshold in Celsius for freezing.                                                                          | 100.0   |
+-------------+----------------------------------------------------------------------------------------------------------------------------------+---------+
| full_degree | Bool if a notification should only be sent when a threshold has been exceeded by a full degree point (whole number not decimal). | False   |
+-------------+----------------------------------------------------------------------------------------------------------------------------------+---------+
| increase    | Bool if a notification should only be sent if previous temp was an increase to reach boil/freeze threshold.                      | False   |
+-------------+----------------------------------------------------------------------------------------------------------------------------------+---------+
| decrease    | Bool if a notification should only be sent if previous temp was a decrease to reach boil/freeze threshold.                       | False   |
+-------------+----------------------------------------------------------------------------------------------------------------------------------+---------+

** Note **
If the temperature is unchanged, no notification is sent as the threshold
was already met.

Example Application
-------------------

.. code-block:: python

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


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
