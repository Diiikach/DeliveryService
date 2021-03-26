from django.db import models
from couriers.models import WorkingHours, Region, Courier
from django.utils import timezone


class DeliveryHours(WorkingHours):
    class Meta:
        verbose_name = "delivery_hours"


class Order(models.Model):
    """
    Entity 'Order' should be a bound object to Entity courier.
    It should be serialized to json.
    """
    order_id: int = models.IntegerField(primary_key=True)
    weight: float = models.FloatField()
    region = models.ForeignKey(to=Region, verbose_name='Active regions', on_delete=models.CASCADE)
    delivery_hours: list = models.ManyToManyField(to=DeliveryHours, verbose_name="delivery_hours", blank=True)

    started: bool = models.BooleanField(blank=True, default=False)

    @classmethod
    def create(cls, dataobject) -> str:
        order_id = dataobject.order_id
        weight = dataobject.weight
        region = Region(num=dataobject.region)
        region.save()
        django_order = cls(order_id=order_id, weight=weight)
        django_order.region = region
        django_order.save()
        for timetable in dataobject.delivery_hours:
            since, to = timetable.split('-')
            timetable_inst = DeliveryHours(since=since, to=to)
            timetable_inst.save()
            django_order.delivery_hours.add(timetable_inst)

    def __str__(self) -> str:
        return f'Order({self.order_id})'
