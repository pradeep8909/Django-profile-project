from django.db import models

class BeneficiaryType(models.Model):
    
    beneficiarytype= models.CharField(max_length=100)
    beneficiarycode = models.PositiveIntegerField(unique=True)

    def __str__(self):
        return f'{self.beneficiarytype} - {self.beneficiarycode}'

class Grade(models.Model):
    GRADE_CHOICES = [
        ('1st', '1st'),
        ('2nd', '2nd'),
        ('3rd', '3rd'),
        ('4th', '4th'),
        ('5th', '5th'),
        ('6th', '6th'),
        ('7th', '7th'),
        ('8th', '8th'),
        ('9th', '9th'),
        ('10th', '10th'),
        ('11th', '11th'),
        ('12th', '12th'),
    ] 

    grade = models.CharField(max_length=4, choices=GRADE_CHOICES, blank=True, null=True)

    def __str__(self):
        return f'{self.grade }'
    

from demography.models import Location,LocationLevel
class School(models.Model):
    School_Name = models.CharField(max_length=300)
    School_Code = models.PositiveIntegerField(unique=True)
    School_Locaion = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='Location' )

    def __str__(self):
        return f'{self.School_Name} - {self.School_Code} - {self.School_Locaion}'    


class Beneficiary(models.Model):
    type = models.ForeignKey(BeneficiaryType, on_delete=models.CASCADE, related_name='Beneficiarytype')
    beneficiaryname = models.CharField(max_length=100)
    gradechoice = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='grdechoice')
    location = models.ForeignKey(School,on_delete=models.CASCADE, related_name='School',null=True,blank=True)

    def __str__(self):
        return f'{self.type} - {self.beneficiaryname} - {self.gradechoice} - - {self.location}'
    

    