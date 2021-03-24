from django.db import models
from couriers.services import serializer


class Region(models.Model):
    """
    Representing a region as a number.
    It should be bound to Courier model.
    Use it to count earned money and reputation of courier.
    """
    total_time: int = models.IntegerField(verbose_name='total time to deliver sweets in this region', blank=True,
                                          default=0)

    num: int = models.IntegerField(verbose_name='region num')
    average_time: float = models.FloatField(verbose_name='average time of deliver in region', default=0.0, blank=True)
    completed_tasks: int = models.IntegerField(verbose_name='the total number of orders completed in the region',
                                               blank=True, default=0)

    def get_average_time(self) -> float:
        self.average_time = self.total_time / self.completed_tasks
        self.save()
        return self.average_time

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
        verbose_name = 'Hours of Working'


class Courier(models.Model):
    """
    Main entity in the app.
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

    working_hours: list = models.ManyToManyField(to=WorkingHours, verbose_name='Hours of Working', blank=True,
                                                 null=True)
    regions: list = models.ManyToManyField(to=Region, verbose_name='Active regions', blank=True)
    earned_money: int = models.IntegerField(verbose_name='earned money', default=0, blank=True)
    rating: float = models.FloatField(verbose_name="courier's rating", default=0, blank=True)
    completed_tasks: int = models.IntegerField(verbose_name='total delivered orders', default=0, blank=True)

    def count_money(self):
        n_courier_type = self.courier_types[self.courier_type]
        for i in range(self.completed_tasks):
            self.total_sum += 500 * n_courier_type
            self.save()

    def count_rating(self) -> float:
        """
        This function counts rating of Courier instance.
        If it returns zero, then in JSON will be retured empty list.
        :return int:
        """
        if self.completed_tasks > 0:
            pass
        else:
            return 0
        average_time = list()
        for region in self.regions:
            average_time.append(region.average_time)

        min_time = min(average_time)
        self.rating = (60 * 60 - min(min_time, 60 * 60)) / (60 * 60) * 5
        self.save()
        return self.rating

    @classmethod
    def create(cls, dantic_object) -> str:
        """
        This function creates 'Courier' object by 'Pydantic'
        object.Also ts creates all depend-object of 'Courier' object and save it.
        :param dantic_object:
        :return str:
        """
        try:
            cls.objects.get(courier_id=dantic_object.courier_id)
        except:
            pass
        else:
            pass
        courier_object = cls(courier_id=dantic_object.courier_id, courier_type=dantic_object.courier_type)
        courier_object.save()

        # Creating 'Workingours' and 'Region' objects to bind that
        # to new 'Courier' instance
        for timetable in dantic_object.working_hours:
            since, to = timetable.split('-')
            timetable_inst = WorkingHours(since=since, to=to)
            timetable_inst.save()
            courier_object.working_hours.add(timetable_inst)

        for region in dantic_object.regions:
            i_region = Region(num=region)
            i_region.save()
            courier_object.regions.add(i_region)

        courier_object.save()
        return "OK"

    @classmethod
    def get_py_dantic_from_django_model(cls, courier_id, advanced=False) -> serializer.Courier:
        """
        This function return Pydantic 'Courier' object
        from Django 'Courier object'
        """
        courier_inst: Courier = cls.objects.get(courier_id=courier_id)
        wh: list[str] = [str(time.since) + '-' + str(time.to) for time in
                         courier_inst.working_hours.filter(courier=courier_inst)]
        regions: list[int] = [region.num for region in courier_inst.regions.filter(courier=courier_inst)]
        courier_type: str = courier_inst.courier_type
        if advanced:
            return serializer.AdvancedCourier(courier_id=courier_id, working_hours=wh, regions=regions,
                                              courier_type=courier_type, earning=courier_inst.earned_money,
                                              rating=courier_inst.rating)

        else:
            return serializer.Courier(courier_id=courier_id, working_hours=wh, regions=regions,
                                      courier_type=courier_type)

    def __str__(self):
        return f'Courier({self.courier_id})'
