from email.message import EmailMessage
from django.shortcuts import get_object_or_404, render
from rest_framework.response import Response
from rest_framework import status
from .serializers import CategorySerializer,ProductSerializer,RegistertionSerializer
from store.models import Category,Product
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from accounts.models import Account
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode



@csrf_exempt
@api_view(['GET','POST','PUT','PATCH','DELETE'])
def catagroy_api(request,slug=None):
    if request.method == 'GET':
        if slug is not None:
            cat=get_object_or_404(Category,slug=slug)
            serializer=CategorySerializer(cat)
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:    
          cat=Category.objects.all()
          serializer=CategorySerializer(cat,many=True)
          return Response(serializer.data,status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer=CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':"Object created successfully"},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
    elif request.method in ['PUT','PATCH']:
        qs=get_object_or_404(Category,slug=slug)
        serializer=CategorySerializer(qs,data=request.data,partial=(request.method=='PATCH'))
        if serializer.is_valid():
            serializer.save()
            return Response({'message':"Object updated successfully"},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        if slug is None:
            return Response({'message':"Slug is required for delete operation"},status=status.HTTP_400_BAD_REQUEST)
        qs=get_object_or_404(Category,slug=slug)
        qs.delete()
        return Response({'message':"Object deleted successfully"},status=status.HTTP_204_NO_CONTENT)
    return Response({'message':"Invalid request"},status=status.HTTP_400_BAD_REQUEST)
        



@api_view(['GET','POST','PUT','PATCH','DELETE'])
def product_api(request,slug=None):
    if request.method == 'GET':
        if slug is not None:
            product=get_object_or_404(Product,slug=slug)
            serializer=ProductSerializer(product)
            return Response(serializer.data,status=status.HTTP_200_OK)
        products=Product.objects.filter(status='available')
        serializer=ProductSerializer(products,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    elif request.method == 'POST':
        sarializer=ProductSerializer(data=request.data)
        if sarializer.is_valid():
            sarializer.save()
            return Response({'message':"Object created successfully"},status=status.HTTP_201_CREATED)
        return Response(sarializer.errors,status=status.HTTP_400_BAD_REQUEST)
    elif request.method in ['PUT','PATCH']:
        qs=get_object_or_404(Product,slug=slug)
        serializer=ProductSerializer(qs,data=request.data,partial=(request.method=='PATCH'))
        if serializer.is_valid():
            serializer.save()
            return Response({'message':"Object updated successfully"},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        if slug is None:
            return Response({'message':"Slug is required for delete operation"},status=status.HTTP_400_BAD_REQUEST)
        qs=get_object_or_404(Product,slug=slug)
        qs.delete()
        return Response({'message':"Object deleted successfully"},status=status.HTTP_204_NO_CONTENT)
    

@api_view(['POST']) 
def regeister_api(request):
    serializer = RegistertionSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.save()
        user.is_active = False
        user.save()

        # generate uid & token
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        activation_link = f"http://127.0.0.1:8000/api/activate/{uid}/{token}/"

        # Send activation email
        send_mail(
            subject='Activate your account',
            message=f'Hi {user.first_name}, Please use the link below to activate your account:\n{activation_link}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
        )

        return Response(
            {'message': "User registered successfully. Please check your email to activate your account."},
            status=status.HTTP_201_CREATED
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 

def activation_view(request, uidb64, token):
    try:
        # Decode the UID
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Account.objects.get(pk=uid)

    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    # Check the token
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()

        return Response(
            {"message": "Account activated successfully"},
            status=status.HTTP_200_OK
        )

    else:
        return Response(
            {"message": "Activation link is invalid!"},
            status=status.HTTP_400_BAD_REQUEST
        )