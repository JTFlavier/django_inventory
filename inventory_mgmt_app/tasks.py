# Create your tasks here
from celery import shared_task

from .models import Item, Order, Customer

@shared_task
def update_item_stock(items):
    sku_ids = [x["sku"] for x in items]

    for item in items: 
        curr_item = Item.objects.get(sku=item["sku"])
        curr_item.quantity = curr_item.quantity  - item["quantity"]
        curr_item.save()

#@shared_task
#def send_email(name, email, address):
