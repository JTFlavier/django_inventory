from django.db import models

class Item(models.Model):
    sku = models.CharField(max_length=8, unique=True)
    quantity = models.IntegerField()

    def __str__(self):
        return str(self.sku)

class Customer(models.Model):
    email = models.CharField(max_length=200, unique=True)
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)

    def __str__(self):
        return str(self.email)
    
class Order(models.Model):
    order_number = models.IntegerField()
    items = models.ManyToManyField(Item)
    customer = models.ForeignKey('Customer', on_delete = models.DO_NOTHING, null=False)

    def __str__(self):
        return str(self.order_number)
