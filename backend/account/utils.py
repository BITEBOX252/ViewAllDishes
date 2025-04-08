# from django.core.mail import EmailMessage
# import os

# class Util:
#     @staticmethod
#     def send_email(data):
#         try:
#             print(data)
#             print(os.environ.get('EMAIL_FROM'))
#             email = EmailMessage(
#                 subject=data['subject'],
#                 body=data['body'],
#                 from_email=os.environ.get('EMAIL_FROM'),

#                 to=[data['to_email']]
#             )
#             email.send(fail_silently=False)  # Ensures errors are raised
#             print("Email sent successfully to:", data['to_email'])
#         except Exception as e:
#             print("Error sending email:", e)




from django.core.mail import EmailMultiAlternatives
import os

class Util:
    @staticmethod
    def send_email(data):
        try:
            email = EmailMultiAlternatives(
                subject=data['subject'],
                body=data['body'],  # Plain text
                from_email=os.environ.get('EMAIL_FROM'),
                to=[data['to_email']]
            )
            email.send(fail_silently=False)
            print("Email sent successfully to:", data['to_email'])
        except Exception as e:
            print("Error sending email:", e)
