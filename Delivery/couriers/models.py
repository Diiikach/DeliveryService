from django.db import models


class Region(models.Model):
    """
    Representing a region as a number.
    """
    num: int = models.IntegerField(verbose_name='region num')
    average_time: int = models.IntegerField(verbose_name='average time of deliver in region', default=0)
    completed_tasks: int = models.IntegerField(verbose_name='the total number of orders completed in the region',
                                               default=0)

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
    It should be serialized to json.
    """
    courier_id: int = models.IntegerField(primary_key=True, unique=True)

    # Courier can be of three types - foot, bike, car
    courier_type: str = models.CharField(max_length=4)
    courier_types = {
        'car': 9,
        'bike': 5,
        'foot': 2,
    }

    working_hours: list = models.ManyToManyField(to=WorkingHours, verbose_name='Hours of Working')
    regions: list = models.ManyToManyField(to=Region, verbose_name='Active regions', blank=True)
    earned_money: int = models.IntegerField(verbose_name='earned money', default=0, blank=True)
    rating: float = models.FloatField(verbose_name="courier's rating", default=0, blank=True)
    completed_tasks: int = models.IntegerField(verbose_name='total delivered orders', default=0, blank=True)

    def count_money(self):
        n_courier_type = self.courier_types[self.courier_type]
        for i in range(self.completed_tasks):
            self.total_sum += 500 * n_courier_type

    def count_rating(self):
        if self.completed_tasks > 0:
            pass
        else:
            return 0
        average_time = list()
        for region in self.regions:
            average_time.append(region.average_time)

        min_time = min(average_time)
        self.rating = (60*60 - min(min_time, 60*60)) / (60*60) * 5

    def __str__(self):
        return f'Courier({self.courier_id})'
