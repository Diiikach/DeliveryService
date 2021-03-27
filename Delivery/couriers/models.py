import datetime
from django.db import models
from django.apps import apps
from django.utils import timezone
from .services import serializer


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

    class Meta:
        verbose_name = 'Hours of Working'


class Delivery(models.Model):
    """
    Delivery model groups ordders by
    assign. It depends by Courier object.
    """
    assign_time = models.DateTimeField(blank=True, default=timezone.now())
    orders = models.ManyToManyField(to='orders.Order')
    weight = models.IntegerField(blank=True, null=True)
    last_completed_time = models.DateTimeField(blank=True, default=timezone.now())

    def remove_order_by_weight(self):
        order = self.orders.objects.get(order_id=order_id)
        self.weight -= order.weight
        order.started = False
        self.orders.objects.remove(self.orders.objects.order_by('weight')[0])

    def complete_order(self, order_id, date_of_complete, courier_id):
        courier = Courier.objects.get(courier_id=courier_id)
        order = self.orders.get(order_id=order_id)
        self.weight -= order.weight
        order.complete_time = datetime.datetime.strptime(date_of_complete, '%Y-%m-%dT%H:%M:%S.%fZ')
        order.copleted = True
        order.save()

        # Parse datetime string
        start_hours = self.last_completed_time.hour
        end_hours = order.complete_time.hour
        start_minutes = self.last_completed_time.minute
        end_minutes = order.complete_time.minute
        start_seconds = self.last_completed_time.second
        end_seconds = order.complete_time.second

        started = datetime.timedelta(hours=start_hours, minutes=start_minutes, seconds=start_seconds)
        ended = datetime.timedelta(hours=end_hours, minutes=end_minutes, seconds=end_seconds)

        order.region.total_time += (ended.seconds - started.seconds)
        order.region.completed_tasks += 1
        self.last_completed_time = order.complete_time
        self.orders.remove(order)
        self.save()
        if len(self.orders.all()) == 0:
            courier.copleted_deliveryes.add(self)
            courier.save()

        return "OK"

    def get_delivery_weight(self):
        self.weight = sum([order.wright for order in orders.objects.all()])
        return self.weight

    @classmethod
    def assign_orders(cls, courier_id):
        try:
            courier = Courier.objects.get(courier_id=courier_id)
        except Exception:
            return None, None

        if courier.delivery:
            if len(courier.delivery.orders.all()) > 0:
                return [{"id": order.order_id} for order in courier.delivery.orders.all()], \
                       courier.delivery.assign_time
        total_weight = 0
        success_orders = []
        Order = apps.get_model(app_label='orders', model_name='Order')
        orders = Order.objects.order_by('-weight')
        delivery = Delivery()
        delivery.save()
        courier.delivery = delivery
        courier.save()
        for order in orders:
            if order.started is True:
                continue

            for wh in courier.working_hours.all():
                for order_dh in order.delivery_hours.all():
                    if order_dh.since <= wh.since and order_dh.to >= wh.to:
                        if total_weight + order.weight <= courier.max_weight:
                            for region in courier.regions.all():
                                if region.num == order.region.num:
                                    total_weight += order.weight
                                    order.region = region
                                    delivery.orders.add(order)
                                    order.started = True
                                    order.save()
        delivery.weight = total_weight
        delivery.save()
        success_orders = [{"id": order.order_id} for order in courier.delivery.orders.all()]
        return success_orders, str(delivery.assign_time)


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
    max_weight = models.IntegerField(blank=True, null=True)
    working_hours: list = models.ManyToManyField(to=WorkingHours, verbose_name='Hours of Working', blank=True,
                                                 null=True)
    regions: list = models.ManyToManyField(to=Region, verbose_name='Active regions', blank=True)
    earned_money: int = models.IntegerField(verbose_name='earned money', default=0, blank=True)
    rating: float = models.FloatField(verbose_name="courier's rating", default=0, blank=True)
    delivery: Delivery = models.ForeignKey(to=Delivery, on_delete=models.CASCADE, blank=True, null=True,
                                           related_name='NowDelivery')
    copleted_deliveryes = models.ManyToManyField(to=Delivery)

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
        if len(self.copleted_deliveryess.all()) > 0:
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
    def create_or_change(cls, dantic_object, courier_id=None) -> str:
        """
        This function creates 'Courier' object by 'Pydantic'
        object.Also ts creates all depend-object of 'Courier' object and save it.
        :param courier_id:
        :param dantic_object:
        :return str:
        """
        if not courier_id:
            courier_object = cls(courier_id=dantic_object.courier_id, courier_type=dantic_object.courier_type)
            courier_object.save()

        else:
            courier_object = cls.objects.get(courier_id=courier_id)

        # Creating 'WorkinHours' and 'Region' objects to bind that
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

        courier_weights = {
            'car': 50,
            'bike': 15,
            'foot': 10,
        }
        courier_object.save()
        courier_object.max_weight = courier_weights[courier_object.courier_type]
        courier_object.save()
        return "OK"

    @classmethod
    def get_py_dantic_from_django_model(cls, courier_id, advanced=False) -> serializer.Courier:
        """
        This function return Pydantic 'Courier' object
        from Django 'Courier object'
        :param advanced:
        :param courier_id:
        """
        courier_inst: Courier = cls.objects.get(courier_id=courier_id)
        wh: list[str] = [str(time.since) + '-' + str(time.to) for time in
                         courier_inst.working_hours.all()]
        regions: list[int] = [region.num for region in courier_inst.regions.all()]
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
