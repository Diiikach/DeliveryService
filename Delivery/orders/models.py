from django.db import models
from couriers.models import WorkingHours, Region, Courier


class DeliveryHours(WorkingHours):

    class Meta:
        db_table = "delivery_hours"
        verbose_name = "delivery_hours"


class Order(models.Model):
    """
    Entity 'Order' should be a bound object to Entity courier.
    """
    order_id: int = models.IntegerField(primary_key=True, unique=True)
    weight: float = models.FloatField()
    region = models.ManyToManyField(to=Region, verbose_name='Active regions')
    delivery_hours: list = models.ManyToManyField(to=DeliveryHours, verbose_name="delivery_hours")
    executor: Courier = models.ForeignKey(to=Courier, on_delete=models.CASCADE,
                                          verbose_name='Courier that execute order')

    def __str__(self) -> str:
        return f'Order({self.order_id})'
