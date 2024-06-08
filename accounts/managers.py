from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator

class UserManager(BaseUserManager):
    def email_vlaidator(self , email):
        try:
            EmailValidator(email)
        except ValidationError:
            raise ValueError('enter valid email')

    def create_user(self , email , first_name , last_name , password , **extra):
        user = self.model(email = email  , first_name = first_name  , last_name = last_name ,**extra)
        user.set_password(password)
        user.save(using = self._db)
        return user
    def create_superuser(self , email , first_name , last_name , password , **extra):
        extra.setdefault('is_staff', True)
        extra.setdefault('is_superuser', True)
        extra.setdefault('is_verified', True)

        user = self.create_user(
             email , first_name , last_name , password , **extra
        )
        user.save(using = self._db)
        return user