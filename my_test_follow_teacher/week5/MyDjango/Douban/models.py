from django.db import models


class T1(models.Model):
    n_star = models.IntegerField(blank=True, null=True)
    short = models.CharField(max_length=40, blank=True, null=True)
    sentiment = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'T1'
