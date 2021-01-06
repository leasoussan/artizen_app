from django.db import models
from django.urls import reverse

from artists.models import Profile
from artists.models import  Item





class Order(models.Model):
    buyer = models.ForeignKey(Profile, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total_price = models.DecimalField(max_digits=9, decimal_places=0)
    date = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.buyer.user.first_name}, {self.item.title}"

    def get_absolute_url(self):
        return reverse('confirm_order_item', kwargs={'pk': self.pk})


class PaymentDetail(models.Model):
    order = models.ForeignKey(Order, on_delete = models.CASCADE) 
    first_name_cc = models.CharField(max_length=30) 
    last_name_cc =models.CharField(max_length=30)
    credit_card = models.CharField(max_length=16)
    expiration = models.CharField(max_length=5)
    digits_3 = models.CharField(max_length=3)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.payment.id}"

    def get_absolute_url(self):
        return reverse('success_order_confirmation', kwargs={'pk': self.pk})




class MessageBox(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="outbox", null=True)
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="inbox")
    email = models.EmailField(null=True, blank=True)
    subject = models.CharField(max_length=200)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f"Message from: {self.sender or self.email} Received on: {self.date}"

    def get_absolute_url(self):
         return reverse('my_messages_panel')
