from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.Reservations)
admin.site.register(models.Drugs_Order)
admin.site.register(models.Blog_Posts)
admin.site.register(models.Comment_Posts)
admin.site.register(models.Order_Items)
admin.site.register(models.Schedule_Reservations)
admin.site.register(models.Message_Chats)
admin.site.register(models.Prescriptions)

# Register your models here.
