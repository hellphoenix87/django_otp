from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from .forms import LoginForm
from django_otp.plugins.otp_totp.models import TOTPDevice
import qrcode
import io
import base64
from django.http import HttpResponse


# Create your views here.

class Login(LoginView):
    template_name = 'login.html'
    authentication_form = LoginForm
    
    def form_valid(self, form):
        response = super().form_valid(form)
        
        # Check if the user has a TOTP device
        otp_token = form.cleaned_data['otp_token']
        user = form.get_user()
        totp_device = TOTPDevice.objects.get(user=user)
        
        if totp_device.verify_token(otp_token):
            return redirect('login_successful')
        else:
            return HttpResponse('Invalid OTP token', status=401)

    
def login_successful_view(request):
    return render(request, 'login_successful.html')
    



def create_user_view(request):
    if request.method == 'POST':
        # Check if the user already exists
        if not User.objects.filter(username='test').exists():
            # Create a new user
            user = User.objects.create_user('test', '', 'test')

            # Create a new TOTP device for the user
            totp_device = TOTPDevice.objects.create(user=user)
            totp_device.save()
            


            img = qrcode.make(totp_device.config_url)
            print(img)
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            image_data = buffer.getvalue()
            base64_image = base64.b64encode(image_data).decode()


            # Generate a QR code for the device's secret key


            # Pass the base64 image to the template
            return render(request, 'create_user.html', {'message': 'User created successfully!', 'qr_code': base64_image})
        else:
            return render(request, 'create_user.html', {'message': 'User already exists!'})
    else:
        # Handle 'GET' request
        return render(request, 'create_user.html')
