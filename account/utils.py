from django.core.mail import send_mail


def send_activation_email(email, activation_code):
    activation_url = f'http://localhost:8000/v1/api/account/activate/{activation_code}'
    message = f'Thank you for registration!\n To activate your account please click link here {activation_url}'
    send_mail(
        'Online Shop Activation',
        message,
        'admin@gmail.com',
        [email, ],
        fail_silently=False
    )
