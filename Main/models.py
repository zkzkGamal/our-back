from django.db import models
from accounts.models import Profile , Doctor ,Patient , Drugs_Data
 
# Create your models here.

class Schedule_Reservations(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    date = models.DateTimeField()
    duration = models.TimeField()

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)  # ForeignKey relationship

    def __str__(self):
        return self.doctor.profiles.name
    
    
class Reservations(models.Model):
    date = models.DateTimeField()
    time = models.TimeField()
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)  # ForeignKey relationship

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)  # ForeignKey relationship
    
    def __str__(self):
        return self.patient.profiles.name
    
    
    
class Drugs_Order(models.Model):
    date = models.DateTimeField()
    status = models.BooleanField()

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)  # ForeignKey relationship
    def __str__(self):
        return f"order for {self.profile.name}"
    @property
    def get_cart_total(self):
         orderitems = self.order_items_set.all()
         total = sum([item.get_total for item in orderitems])
         return total 

    @property
    def get_cart_items(self):
        orderitems = self.order_items_set.all()
        total = sum([item.quantity for item in orderitems])
        return total   
    
class Order_Items(models.Model):
    quantity = models.IntegerField()
    date = models.DateTimeField()
    product = models.ForeignKey(Drugs_Data ,on_delete=models.CASCADE )
    drugs_order = models.ForeignKey(Drugs_Order, on_delete=models.CASCADE)  # ForeignKey relationship
    def __str__(self):
        return f"item {self.product.name} in order {self.drugs_order}"
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
    
    
    
class Message_Chats(models.Model):
    date = models.DateTimeField()
    message = models.TextField()
    last_message = models.TextField()

    sender = models.ForeignKey(Profile,related_name='sender', on_delete=models.CASCADE)  # ForeignKey relationship
    receiver = models.ForeignKey(Profile,related_name='receiver', on_delete=models.CASCADE)  # ForeignKey relationship
    def __str__(self):
        return self.sender.name   
    
    
    
    

class Blog_Posts(models.Model):
    category_id = models.IntegerField()
    title = models.CharField(max_length=255)
    sub_title = models.CharField(max_length=255)
    body = models.TextField()
    create_date = models.DateTimeField()
    image = models.ImageField('media/blogposts/')

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)  # ForeignKey relationship
    def __str__(self):
        return self.doctor.profiles.name
    
    
    
class Comment_Posts(models.Model):
    date = models.DateTimeField()
    body = models.TextField()
    
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)  # ForeignKey relationship

    blog_post = models.ForeignKey(Blog_Posts, on_delete=models.CASCADE)  # ForeignKey relationship

    def __str__(self):
        return self.profile.name
    
    
    




class Prescriptions(models.Model):
    description = models.CharField(max_length=255)
    date = models.DateTimeField()
    consult_date = models.DateTimeField()
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)  # ForeignKey relationship
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)  # ForeignKey relationship
    def __str__(self):
        return self.doctor.profiles.name
