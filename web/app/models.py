from django.db import models

meter_types = (('1', 'Mains'),
               ('2', 'Appliance'),)

class Reading(models.Model):
    """
    A Reading from the CC meter
    """
    time = models.DateTimeField()
    temperature = models.DecimalField(max_digits = 8, decimal_places = 2)
    meter_id = models.CharField(max_length = 5)
    meter_type = models.IntegerField()
    ch1_wattage = models.DecimalField(max_digits = 8, decimal_places = 2)
    ch2_wattage = models.DecimalField(max_digits = 8, decimal_places = 2)
    ch3_wattage = models.DecimalField(max_digits = 8, decimal_places = 2)
  
