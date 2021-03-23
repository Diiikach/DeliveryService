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
    order_id: int = models.IntegerField(primary_key=True, unique=True)
    weight: float = models.FloatField()
    region = models.ManyToManyField(to=Region, verbose_name='Active regions')
    delivery_hours: list = models.ManyToManyField(to=DeliveryHours, verbose_name="delivery_hours")
    executor: Courier = models.ForeignKey(to=Courier, on_delete=models.CASCADE,
                                          verbose_name='Courier that execute order')

    started: bool = models.BooleanField(blank=True, default=False)
    asign_date: str = models.DateTimeField(blank=True, null=True)

    def assign(self, courier_inst):
        self.executor = courier_inst
        self.asign_date = timezone.now()
        self.save()
        return self.asign_date

    def __str__(self) -> str:
        return f'Order({self.order_id})'
