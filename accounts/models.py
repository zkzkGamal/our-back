from django.db import models
from django.contrib.auth.models import   AbstractBaseUser , PermissionsMixin
from .managers import UserManager
from django.utils.text import slugify


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length = 250 , unique = True , null = True , blank = True)
    email = models.EmailField(max_length = 250 , unique= True)
    first_name = models.CharField(max_length = 100)
    last_name = models.CharField(max_length = 100)
    is_staff = models.BooleanField(default = False)
    is_superuser = models.BooleanField(default = False)
    is_active = models.BooleanField(default = True)
    is_verified = models.BooleanField(default = False)
    date_joined = models.DateTimeField(auto_now_add = True)
    last_login = models.DateTimeField(auto_now = True)

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="user_set",
        related_query_name="user",
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name' , 'last_name']

    objects = UserManager()

    def str(self):
        return self.username

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    def save(self , *args , **kwargs):
        if not self.username:
            username = self.first_name
            has_username = User.objects.filter(username=username).exists()
            count = 1
            while has_username:
                count += 1
                username = f"{self.first_name}-{count}"
                has_username = User.objects.filter(username=username).exists()

            self.username = username
        super().save(*args , **kwargs)
        

class Profile(models.Model):
    sex = [('female','female') , ('male', 'male')]
    user = models.OneToOneField(User , null=True, blank=True, on_delete=models.CASCADE)  # ForeignKey relationship
    name = models.CharField(max_length=255,null = True , blank= True)
    age = models.IntegerField(null = True , blank= True)
    address = models.CharField(max_length=255,null = True , blank= True)
    phone = models.CharField(max_length=11,null = True , blank= True)
    blood_type = models.CharField(max_length=255,null = True , blank= True)
    emgo_phone = models.CharField(max_length=11 , null = True , blank= True)
    photo = models.ImageField(upload_to='media/users/' , null = True , blank= True)
    gender = models.TextField(choices= sex, null = True , blank= True)
    
    def __str__(self):
        return self.name
    
    def save(self , *args , **kwargs):
        if not self.name:
            name = self.user.first_name + ' ' + self.user.last_name
            has_name = Profile.objects.filter(name=name).exists()
            count = 1
            while has_name:
                count += 1
                name = self.user.first_name + ' ' + self.user.last_name +  '-' + str(count)
                has_name = Profile.objects.filter(name=name).exists()

            self.name = name
        super().save(*args , **kwargs)
    
class Organizations(models.Model):
    name = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='media/organizations/')
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=11)



    def __str__(self):
        return self.name
    
class Specialites(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null = True , blank= True)
    
    
    def __str__(self):
        return self.name    

class Doctor(models.Model):
    license_id = models.IntegerField(null = True , blank= True)
    description = models.TextField(null = True , blank= True)
    price = models.DecimalField(max_digits=10, decimal_places=2,null = True , blank= True)
    email = models.EmailField(null = True , blank= True)
    profiles =   models.OneToOneField(Profile,null=True, blank=True, on_delete=models.CASCADE)
    organizations = models.ForeignKey(Organizations, on_delete=models.CASCADE,null = True , blank= True)  
    specialites = models.ManyToManyField(Specialites,null = True , blank= True)  
    slug=models.CharField(max_length= 20)

    def __str__(self):
        return self.profiles.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(self.profiles.name)
            has_slug = Doctor.objects.filter(slug=slug).exists()
            count = 1

            while has_slug:
                count += 1
                slug = f"{slugify(self.profiles.name)}-{count}"
                has_slug = Doctor.objects.filter(slug=slug).exists()

            self.slug = slug

        super().save(*args, **kwargs)
    
    
    
class Patient(models.Model):
    profiles =  models.OneToOneField(Profile,null=True, blank=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.profiles.name
    
    
    
class Suppliers(models.Model):
    supplier_card_licence = models.IntegerField()
    profiles =  models.OneToOneField(Profile,null=True, blank=True, on_delete=models.CASCADE)
    organizations = models.ForeignKey(Organizations, on_delete=models.CASCADE)
   
    def __str__(self):
        return self.profiles.name
    
class DrugCategory(models.Model):
    name = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='media/drug/category/',null = True , blank= True)
    description = models.TextField(null = True , blank= True)
    
    
    def __str__(self):
        return self.name    
class Drugs_Data(models.Model):
    name = models.CharField(max_length=255    ,null = True , blank= True)
    price = models.DecimalField(max_digits=10, decimal_places=2 ,null = True , blank= True)
    description = models.TextField(null = True , blank= True)
    photo = models.ImageField(upload_to='media/drug/',null = True , blank= True)
    quantity = models.IntegerField(null = True , blank= True)
    production_date = models.DateTimeField(null = True , blank= True)
    add_date = models.DateTimeField(null = True , blank= True , auto_now=True)
    expire_date = models.DateTimeField(null = True , blank= True)
    serial_num = models.IntegerField(null = True , blank= True)
    category=models.ManyToManyField(DrugCategory , null=True , blank=True)
    supplier = models.ForeignKey(Suppliers, on_delete=models.CASCADE ,null = True , blank= True)  # ForeignKey relationship


    def __str__(self):
        return self.name
    
class Warhouse_Managments(models.Model):
    card_code = models.CharField(max_length=20)
    profiles =  models.OneToOneField(Profile,null=True, blank=True, on_delete=models.CASCADE)
    organizations = models.ForeignKey(Organizations, on_delete=models.CASCADE)     
    
    def __str__(self):
        return self.profiles.name    
    
   
    
class Warhouse_Places(models.Model):
    address = models.CharField(max_length=255)
    drug_add_date = models.DateTimeField()
    drug_status = models.BooleanField()
   
    warhouse_Managments = models.ForeignKey(Warhouse_Managments, on_delete=models.CASCADE)  # ForeignKey relationship

    drugs_Data = models.ForeignKey(Drugs_Data, on_delete=models.CASCADE)  # ForeignKey relationship

    def __str__(self):
        return self.warhouse_Managments.profiles.name
    
    
    
# class OneTimePassword(models.Model):

#     user=models.OneToOneField(User,on_delete=models.CASCADE)
#     code=models.CharField(max_length=6 , unique=True)
    
#     def __str__(self):
#         return f"{self.user.first_name}-Password"
    
    
    

    

    












