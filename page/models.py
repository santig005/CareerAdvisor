# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
import numpy as np
def get_default_array():
  default_arr = np.random.rand(1536)  # Adjust this to your desired default array
  return default_arr.tobytes()

class Applicant(models.Model):
    idapplicant = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=45, blank=True, null=True)
    email = models.CharField(max_length=45, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'applicant'


class College(models.Model):
    idcollege = models.IntegerField(db_column='idCollege', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=45, blank=True, null=True)
    email = models.CharField(max_length=45, blank=True, null=True)
    password = models.CharField(max_length=45, blank=True, null=True)
    logo = models.ImageField(upload_to='logos/',max_length=45, blank=True, null=True)
    description = models.CharField(max_length=400, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'college'


class Courses(models.Model):
    idcourse = models.AutoField(db_column='idCourse', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=45, blank=True, null=True)
    modality = models.CharField(max_length=45, blank=True, null=True)
    academic_level = models.CharField(max_length=45, blank=True, null=True)
    time_type = models.CharField(max_length=45, blank=True, null=True)
    time = models.IntegerField(blank=True, null=True)
    requirements = models.JSONField(blank=True, null=True)
    labels = models.JSONField(blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    college_idcollege = models.ForeignKey(College, models.DO_NOTHING, db_column='College_idCollege')  # Field name made lowercase.
    emb = models.BinaryField(blank=True, null=True,default=get_default_array())

    class Meta:
        managed = False
        db_table = 'courses'
        unique_together = (('idcourse', 'college_idcollege'),)
    def get_labels(self):
        return self.labels.get('labels', [])


class Profiling(models.Model):
    idprofiling = models.AutoField(db_column='idProfiling', primary_key=True)  # Field name made lowercase.
    studies = models.JSONField(blank=True, null=True)
    preferences = models.JSONField(blank=True, null=True)
    interest = models.JSONField(blank=True, null=True)
    applicant_idappilicant = models.ForeignKey(Applicant, models.DO_NOTHING, db_column='Applicant_idAppilicant')  # Field name made lowercase.
    emb = models.BinaryField(blank=True, null=True,default=get_default_array())

    class Meta:
        managed = False
        db_table = 'profiling'
        unique_together = (('idprofiling', 'applicant_idappilicant'),)


class Recommendation(models.Model):
    idrecommendation = models.AutoField(db_column='idRecommendation', primary_key=True)  # Field name made lowercase.
    match = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    college_idcollege = models.ForeignKey(Courses, models.DO_NOTHING, db_column='College_idCollege')  # Field name made lowercase.
    profiling_idprofiling = models.ForeignKey(Profiling, models.DO_NOTHING, db_column='Profiling_idProfiling')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'recommendation'
        unique_together = (('idrecommendation', 'college_idcollege', 'profiling_idprofiling'),)
