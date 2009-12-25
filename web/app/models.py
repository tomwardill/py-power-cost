from django.db import models

meter_types = (('1', 'Mains'),
               ('2', 'Appliance'),)

class Reading(models.Model):
    """
    A Reading from the CC meter
    """
    time = models.DateTimeField()
    temperature = models.DecimalField()

class SensorReading(models.Model):
    """
    A value from a sensor, related to a reading taken at a particular time
    """
    meter_id = models.CharField(max_length = 5)
    meter_type = models.IntegerField()
    wattage = models.DecimalField()
    reading = models.ForeignKey(Reading)    
