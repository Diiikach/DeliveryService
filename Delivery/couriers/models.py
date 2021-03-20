from django.db import models


class Region(models.Model):
    """
    Representing a region as a number.
    """
    num: int = models.IntegerField(verbose_name='Region num', unique=True)

    class Meta:
        verbose_name = 'Region'
        verbose_name_plural = 'Regions'


class WorkingHours(models.Model):
    """
    This model should be added to 'Courier.working_hours' list.
    """
    # 'since' and 'to' fields  determine  time
    #  what from courier can deliver orders.
    since: str = models.TimeField(blank=False, null=False, verbose_name='start of job')
    to: str = models.TimeField(blank=False, null=False, verbose_name='end of job')

    def __str__(self):
        return self.since + self.to

    class Meta:
        db_table = 'working_hours'
        verbose_name = 'Hours of Working'


class Courier(models.Model):
    """
    Main entity in app.
    """
    courier_id: int = models.IntegerField(primary_key=True, unique=True)

    # Courier can be of three types - foot, bike, car
    courier_type: str = models.CharField(max_length=4)

    working_hours: list = models.ManyToManyField(to=WorkingHours, verbose_name='Hours of Working')
    regions: list = models.ManyToManyField(to=Region, verbose_name='Active regions')
    total_sum: int = models.IntegerField(verbose_name='earned money')
    rating: float = models.FloatField(verbose_name="courier's rating")

    def __str__(self):
        return f'Courier({self.courier_id})'
