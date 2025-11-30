from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .models import Account
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email_address = form.cleaned_data['email']
            password = form.cleaned_data['password']
            country = form.cleaned_data['country']
            phone_number = form.cleaned_data['phone_number']
            username = email_address.split('@')[0]

            user = Account.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email_address,
                username=username,
                country=country,
                phone_number=phone_number,
                password=password
            )

            domain_name = get_current_site(request)
            mail_subject = 'Activate your E-commerce account'
            message = render_to_string('account/activate_account.html', {
                'user': user,
                'domain': domain_name,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })

            email_message = EmailMessage(
                subject=mail_subject,
                body=message,
                from_email=f"E-commerce <{settings.EMAIL_HOST_USER}>",
                to=[email_address],
            )
            email_message.content_subtype = "html"
            email_message.send()

            messages.success(request, "Your account has been created! Check your email to activate it.")
            return redirect(f'/accounts/login/?command=verification&email={email_address}')
    else:
        form = RegistrationForm()
    
    return render(request, 'account/register.html', {'form': form})


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)

        if user is not None:
            if user.is_active:
                auth_login(request, user)
                messages.success(request, 'Logged in successfully!')
                return redirect('store:home')
            else:
                messages.warning(request, 'Please activate your account first via email.')
                return redirect('accounts:login')
        else:
            messages.error(request, 'Invalid login credentials.')
            return redirect('accounts:login')
            
    return render(request, 'account/login.html')


def activate_account(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
        
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been activated! You can now log in.')
        return redirect('accounts:login')
    else:
        messages.error(request, 'Activation link is invalid or has expired.')
        return redirect('accounts:register')
