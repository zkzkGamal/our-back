# import random
# from django.core.mail import EmailMessage
# from .models import User , OneTimePassword
# from django.conf import settings

# def generateOtp():
#     otp=''
#     for i in range(6):
#         otp +=str(random.randint(1,9))
#     return otp

# def send_code_to_user(email):
#     subject="One Time Password For Email Verification"
#     otp_code=generateOtp()
#     print(otp_code)
#     user = User.objects.get(email = email)
#     current_site="myAuth.com"
#     email_body=f"HAI {User.first_name} Thanks For Signing Up On {current_site} Please Verify Your Email With the \n One Time PassCode {otp_code}"
#     from_email=settings.Default_From_Email
    
#     OneTimePassword.objects.create(user=user , code=otp_code)
    
#     d_email=EmailMessage(subject=subject , body=email_body , from_email=from_email ,to={email} )
#     d_email.send(fail_silently=True)