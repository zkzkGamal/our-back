from django.shortcuts import render
from .serializers import *
from rest_framework import status , response , mixins , generics , viewsets
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import Group
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from . import models
from . import permissions
# Create your views here.

    
class RegisterUserView(viewsets.ViewSet):
    serializer_class = UserRegisterSerializer
    def create(self , request):
        # create user
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(request.data.get('password'))
            user.save()

            # assign groupe to the user
            group_name = request.data['group_name']
            groups = [Group.objects.get(name=group_name)]
            if group_name == 'Doctors':
                group1 = Group.objects.get(name='Patients')
                groups.append(group1)
                models.Doctor.objects.create(profile = user.profile)
            user.groups.set(groups)  # Assign the appropriate group
            
            # get the tokens for the user
            refresh = self.create_custom_claims(user ,RefreshToken.for_user(user))
            access_token = self.create_custom_claims(user , refresh.access_token)
            # put the user data 
            response_data = {
                'access_token': str(access_token),
                'refresh_token': str(refresh),
                'success': True,
            }
            return response.Response(response_data , status= status.HTTP_201_CREATED)
        return response.Response({'message':'user creatain fialed', 'success':False} , status=status.HTTP_400_BAD_REQUEST)
    # to make custem token for registerd user
    def create_custom_claims(self, user , token):
       # refresh = RefreshToken.for_user(user)
       # access_token = refresh.access_token

        token['user_id'] = user.id
        token['group_name'] = [group.name for group in user.groups.all()]
        token['profile_id'] = user.profile.id
        token['patient_id'] = user.profile.patient.id if user.profile.patient else None
        token['doctor_id'] = user.profile.doctor.id if user.profile.doctor else None
        token['user_data'] = Userdataserislizer(user).data

        return token
        
class LoginUser(TokenObtainPairView, generics.GenericAPIView):
    serializer_class = MyTokenSerializers
    
    
    
class ProfileData(mixins.UpdateModelMixin , mixins.ListModelMixin , mixins.DestroyModelMixin , generics.GenericAPIView):
    def get_queryset(self):
        if self.request.user.is_authenticated:
            profile= self.request.user.profile
            if profile.exists():
                return profile
            return None
        raise PermissionDenied('user must be authenticated')
            
    permission_classes = [permissions.AUTH_ONLY]
    serializer_class=ProfileSerializers
    def get(self , request ,  *args, **kwargs):
        data=self.get_queryset()
        if data is None :
            return response.Response({'Message':'User Dosent Have Profile '})
        data=self.serializer_class(data , many=True)
        return response.Response(data.data)
    
    def put(self , request ,  *args, **kwargs):
        return self.update(request ,  *args, **kwargs)
    
    def delete(self , request ,  *args, **kwargs):
        return self.destroy(request ,  *args, **kwargs)
    
        
class UpdatePassword(generics.GenericAPIView , mixins.UpdateModelMixin ,mixins.RetrieveModelMixin):
    serializer_class=UpdatePasswordSerializers
    permission_classes=[permissions.AUTH_ONLY]
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.request.user
        raise PermissionDenied('user must be authenticated')
    def put(self , request ,  *args, **kwargs):
        return self.update(request ,  *args, **kwargs)
    
    def get(self , request ,  *args, **kwargs):
        return self.retrieve(request ,  *args, **kwargs)
        
        
        
class DoctorData(generics.GenericAPIView, mixins.ListModelMixin , mixins.UpdateModelMixin ,
                 mixins.DestroyModelMixin , mixins.RetrieveModelMixin) :
    def get_queryset(self):
        if 'slug' in self.kwargs:
            doctor = models.Doctor.objects.filter(slug=self.kwargs['slug'])
            if doctor.exists():
                return doctor
            return models.Doctor.objects.none()
        
        elif 'pk' in self.kwargs:
            if self.request.user.is_authenticated:
                doctor = models.Doctor.objects.filter(id=self.kwargs['pk'], user=self.request.user)
                if doctor.exists():
                    return doctor
                raise PermissionDenied('The authenticated user doesn\'t have access to this id')
            raise PermissionDenied('User must be authenticated')
                
        return models.Doctor.objects.all()

                
    serializer_class=DoctorDataSerializers
    permission_classes=[permissions.DoctorOnly]
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset.exists():
            serializer = self.serializer_class(queryset, many=True)
            ser_doctor = serializer.data
            for doctor in ser_doctor:
                profile=models.Profile.objects.filter(id=doctor['profiles'])
                print(doctor['profiles'])
                doctor['profile'] = ProfileSerializers(profile , many=True).data
                
            return response.Response(ser_doctor)
        return response.Response({'message': 'doctor not found'}, status=status.HTTP_404_NOT_FOUND) 
        
    def put(self , request ,  *args, **kwargs):
        return self.update(request ,  *args, **kwargs)
    
    def delete(self , request ,  *args, **kwargs):
        return self.destroy(request ,  *args, **kwargs) 
        




class DrugViewDetail(mixins.ListModelMixin,
                     generics.GenericAPIView):
    def get_queryset(self):
         if 'name' in self.kwargs:
             drug=models.Drugs_Data.objects.filter(name=self.kwargs['name'])
             if drug.exists():
                 return drug
             return models.Drugs_Data.objects.none()
         elif 'category' in self.kwargs:
             drug=models.Drugs_Data.objects.filter(category__name=self.kwargs['category'])
             if drug.exists():
                 return drug
             return models.Drugs_Data.objects.none()
         return models.Drugs_Data.objects.all()
    

    serializer_class = DrugDetailSerializer
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset.exists():
            serializer = self.get_serializer(queryset, many=True)
            return response.Response(serializer.data)
        return response.Response({'message': 'drug not found'}, status=status.HTTP_404_NOT_FOUND)
                
    
class DrugCategoryData(generics.GenericAPIView , mixins.ListModelMixin )   :
    def get_queryset(self):
        if 'pk' in self.kwargs:
            drugcategory=models.DrugCategory.objects.filter(id=self.kwargs['pk'])
            if drugcategory.exists():
                return drugcategory
            return models.DrugCategory.objects.none()
        return models.DrugCategory.objects.all()
    
    serializer_class = DrugCategorySerializers
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset.exists():
            serializer = self.get_serializer(queryset, many=True)
            return response.Response(serializer.data)
        return response.Response({'message': 'Drug Category not found'}, status=status.HTTP_404_NOT_FOUND)

        
    



