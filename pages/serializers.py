# serializers.py

from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token as AuthToken

from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


# Create serializer for Task
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['task_name', 'task_description', 'due_date', 'status']


# Create serializer for GrowthRecord
class GrowthRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = GrowthRecord
        fields = ['record_date', 'weight', 'height', 'head_circumference']
# Create serializer for Child
class ChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Child
        fields = ['baby', 'birth_date', 'type', 'feedings', 'sleeping', 'Diapers', 'weight', 'height', 'photo']


class PrChildSerializer(serializers.Serializer):
    type = serializers.ChoiceField(choices=[('male', 'Male'), ('female', 'Female')])
    birth_date = serializers.DateField()


import re
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Mother


class MotherSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = Mother
        fields = ['id', 'first_name', 'last_name', 'email', 'password', 'confirm_password']

    def validate(self, data):
        # تحقق من تطابق كلمة المرور
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})

        # تحقق من وجود المستخدم مسبقًا
        if User.objects.filter(username=data['email']).exists():
            raise serializers.ValidationError({"email": "This email is already registered."})

        # تحقق من صحة كلمة المرور
        self.validate_password(data['password'])

        return data

    def validate_password(self, password):
        # تحقق من وجود حرف كبير
        if not re.search(r'[A-Z]', password):
            raise serializers.ValidationError("Password must include at least one uppercase letter.")
        
        # تحقق من وجود حرف صغير
        if not re.search(r'[a-z]', password):
            raise serializers.ValidationError("Password must include at least one lowercase letter.")
        
        # تحقق من وجود رقم
        if not re.search(r'\d', password):
            raise serializers.ValidationError("Password must include at least one number.")
        
        # تحقق من وجود رمز خاص
        if not re.search(r'[@$!%*#?&]', password):
            raise serializers.ValidationError("Password must include at least one special character (@$!%*#?&).")

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('confirm_password')

        # إنشاء المستخدم أولاً
        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=password,
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )

        # إنشاء الأم بعد ربطها بالمستخدم
        mother = Mother.objects.create(
            user=user,
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
        )

        return mother


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password']  # بدون الأطفال
        extra_kwargs = {
            'password': {'write_only': True}  # حتى لا يظهر الباسورد في الرد
        }

    def create(self, validated_data):
        # إنشاء مستخدم جديد
        user = User.objects.create_user(**validated_data)
        return user




# Create serializers for Advice models
class AdviceBabySerializer(serializers.ModelSerializer):
    class Meta:
        model = AdviceBaby
        fields = '__all__'

class AdviceBadSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdviceBad
        fields = '__all__'

class AdviceMotherSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdviceMother
        fields = '__all__'

class BabyBottleAdviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdviceBottel
        fields = '__all__'

class AdviceMoonSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdviceMoon
        fields = '__all__'

# Serializer for HowTo
class HowToSerializer(serializers.ModelSerializer):
    class Meta:
        model = HowTo
        fields = '__all__'
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        # التحقق من صحة بيانات المستخدم
        user = authenticate(username=data['username'], password=data['password'])
        
        if user:
            # توليد الـ JWT Tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            
            # إرجاع الـ response
            return {
                'message': 'Login successful',
                'access': access_token,  # توكن الوصول
                'refresh': str(refresh),  # توكن التحديث
                'user_id': user.id,
                'username': user.username
            }
        else:
            raise serializers.ValidationError({'message': 'Invalid credentials'})

import re
class PasswordResetSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    new_password = serializers.CharField(min_length=8)

    def validate_new_password(self, value):
        # لازم يكون فيه على الأقل حرف كبير، صغير، رقم
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError("Password must include at least one uppercase letter.")
        if not re.search(r'[a-z]', value):
            raise serializers.ValidationError("Password must include at least one lowercase letter.")
        if not re.search(r'\d', value):
            raise serializers.ValidationError("Password must include at least one number.")
        if not re.search(r'[@$!%*#?&]', value):
            raise serializers.ValidationError("Password must include at least one special character (@$!%*#?&).")
        return value

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        # يمكن إضافة تحقق إضافي للبريد الإلكتروني إذا لزم الأمر
        return value

# ✅ تسجيل الخروج
class LogoutSerializer(serializers.Serializer):
    def logout(self, request):
        from django.contrib.auth import logout
        logout(request)
        return {'message': 'Logout successful'}
