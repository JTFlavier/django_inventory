# Create your tasks here
from celery import shared_task
from django.core.mail import EmailMessage
from django_inventory_api import settings

from .models import Item, Order, Customer

@shared_task
def update_item_stock(items, name, email, address):
    
    #update inventory 
    sku_ids = [x["sku"] for x in items]

    for item in items: 
        curr_item = Item.objects.get(sku=item["sku"])
        curr_item.quantity = curr_item.quantity  - item["quantity"]
        curr_item.save()

    #email
    text = f"""Hello {name},
    You have successfully ordered the following items:

    """

    for item in items:
        to_append = f"""{item["quantity"]} units of {item["sku"]}
        """

        text = text + to_append

    text = text + """
    """
    text = text + f"""We will deliver to the following address: {address}."""

    mail_subject = "Thank you for ordering!"

    msg = EmailMessage(mail_subject, text, settings.EMAIL_HOST_USER, [email])
    msg.content_subtype = 'html'
    msg.send()