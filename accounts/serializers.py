from rest_framework import serializers
from rest_framework_simplejwt.tokens import Token
from .models import User
from rest_framework import  response
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer  
from . import models




class UserRegisterSerializer(serializers.ModelSerializer):
    groups = [('doctors','doctors') , ('patient', 'patient')]

    password = serializers.CharField(write_only = True)
    group_name = serializers.ChoiceField(choices=groups , write_only = True)
    class Meta:
        model = User
        fields = ('id','username' , 'first_name' , 'last_name' , 'password' , 'email' , 'group_name')
        
        extra_kwargs = {'password': {'write_only': True},
                        'group_name': {'write_only': True}}
    def create(self, validated_data):
        email = validated_data['email']
        username  = validated_data['username']
        if email == User.objects.filter(email= email).first():
            return ({'massage':'this email is taken'})
        if username == User.objects.filter(username= username).first():
            return response.Response({'massage':'this username is taken'})
        validated_data['password'] = make_password(validated_data.pop('password'))
        chunk = validated_data.pop('group_name')
        user = User.objects.create_user(**validated_data)
        return user



class Userdataserislizer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('id','username' , 'first_name' , 'last_name' , 'email')
        

class MyTokenSerializers(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['user'] = Userdataserislizer(user).data
        if hasattr(user, 'profile'):
            token['profile_id'] = user.profile.pk
            if hasattr(user.profile, 'patient'):
                token['patient_id'] = user.profile.patient.pk
            if hasattr(user.profile, 'doctor'):
                token['doctor_id'] = user.profile.doctor.pk
        x = user.groups.all()
        token['groups'] = [n.name for n in x]
        return token
        
class ProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model=models.Profile
        exclude=('id' , 'user')
        
        
class UpdatePasswordSerializers(serializers.ModelSerializer):
    class Meta:
        model=User
        fields= ('password' , )
        extra_kwargs={
            'password':{'write_only':True , 'required':True }
        }
    def update(self , instince , valid):
        if 'password' in valid:
            valid['password']=make_password(valid['password'])
                
        return super().update(instince , valid)
        
        
class DoctorDataSerializers(serializers.ModelSerializer):
    class Meta:
        model=models.Doctor
        fields='__all__'
        
        
class DrugDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Drugs_Data
        exclude = ('supplier' , )
    
    
class DrugCategorySerializers(serializers.ModelSerializer):
    class Meta:
        model=models.DrugCategory
        fields='__all__'