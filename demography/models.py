from django.db import models

class LocationLevel(models.Model):
    name = models.CharField(max_length=200)
    location_code = models.PositiveIntegerField(unique=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return f'{self.name} - {self.location_code}'


class Location(models.Model):
    name = models.CharField(max_length=200)
    location_level = models.ForeignKey(LocationLevel, on_delete=models.CASCADE, related_name='LocationLevel')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return f'{self.name} - {self.location_level}'