from django.db import models


class Application(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('N', 'Not selected'),
    ]
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    date_created = models.DateTimeField(auto_now_add=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=1, default='N')

    def __str__(self):
        return f'{self.id}: {self.name}'


# To import data, run the command in sqlite3:
# .import --csv immunization_legal_entities.csv immunization_legal_entities
# To generate Model from the existing table:
# ./manage.py inspectdb immunization_legal_entities

class ImmunizationLegalEntities(models.Model):
    legal_entity_id = models.UUIDField(primary_key=True)
    legal_entity_name = models.TextField(blank=True, null=True)
    legal_entity_edrpou = models.TextField(blank=True, null=True)
    care_type = models.TextField(blank=True, null=True)
    property_type = models.TextField(blank=True, null=True)
    legal_entity_email = models.EmailField()
    legal_entity_phone = models.TextField(blank=True, null=True)
    legal_entity_owner_name = models.TextField(blank=True, null=True)
    registration_area = models.TextField(blank=True, null=True)
    registration_settlement = models.TextField(blank=True, null=True)
    registration_addresses = models.TextField(blank=True, null=True)
    lat = models.TextField(blank=True, null=True)
    lng = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'immunization_legal_entities'
