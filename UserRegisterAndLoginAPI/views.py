from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import (UserRegistrationSerializer, 
                          UserLoginSerializer, 
                          UserProfileSerializer,
                          UserPassWordChangeSerializer)
from django.contrib.auth import authenticate
from .renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

# Create your views here.

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh':str(refresh),
        'access':str(refresh.access_token)
    }

class UserRegistration(APIView):
    renderer_classes=[UserRenderer]
    def post(self, request, format=None):
        serializer=UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user=serializer.save()
            token=get_tokens_for_user(user)
            return Response({'message':'Register Successful.','token':token}, 
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserLogin(APIView):
    def post(self, request, format=None):
        serializer=UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email=serializer.data.get('email')
            password=serializer.data.get('password')
            user=authenticate(email=email, password=password)
            if user is not None:
                token=get_tokens_for_user(user)
                return Response({'message':'Login Successful.','token':token}, 
                                status=status.HTTP_200_OK)
            else:
                return Response({'errors':{
                    'non_field_errors':['Email or Password is not valid.']
                    }}, 
                                status=status.HTTP_400_BAD_REQUEST)
                
class UserProfileView(APIView):
    renderer_classes=[UserRenderer]
    permission_classes=[IsAuthenticated]
    def get(self, request, format=None):
        serealizer=UserProfileSerializer(request.user)
        return Response(serealizer.data, status=status.HTTP_200_OK)
    
class UserPasswordChangeView(APIView):
    renderer_classes=[UserRenderer]
    permission_classes=[IsAuthenticated]
    def put(self, request, format=None):
        serializer=UserPassWordChangeSerializer(data=request.data, context={'user':request.user})
        if serializer.is_valid(raise_exception=True):
            return Response({'message':'Password Change Successfuly.'}, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
        