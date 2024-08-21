from rest_framework import serializers
from .models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(style={'input_type':'password'}, write_only=True)
    class Meta:
        model=User
        fields=['email', 'name', 'password', 'password2', 'tc']
        extra_kwargs={
            'password':{'write_only':True}
        }
        
    def validate(self, attrs):
        password=attrs.get('password')
        password2=attrs.get('password2')
        if password!=password2:
            raise serializers.ValidationError("Password <> Password2")
        return attrs
    
    def create(self, validate_data):
        return User.objects.create_user(**validate_data)
    
class UserLoginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=255)
    class Meta:
        model=User
        fields=['email', 'password', ]
        
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','email','name','created_at','updated_at']
        
class UserPassWordChangeSerializer(serializers.ModelSerializer):
    password=serializers.CharField(max_length=255,
                                   style={'input_type':'password'},
                                   write_only=True)
    password2=serializers.CharField(max_length=255,
                                style={'input_type':'password2'},
                                write_only=True)
    class Meta:
        model=User
        fields=['password','password2']
        
    def validate(self, attrs):
        password=attrs.get('password')
        password2=attrs.get('password2')
        user=self.context.get('user')
        if password!=password2:
            raise serializers.ValidationError("Password <> Password2")
        user.set_password(password)
        user.save()
        return attrs
    