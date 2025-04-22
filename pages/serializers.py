# serializers.py

from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token as AuthToken


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

    def create(self, validated_data):
        mother = self.context.get('mother')  # الحصول على الأم من السياق
        child = Child.objects.create(mother=mother, **validated_data)
        return child
from django.contrib.auth.models import User

from django.contrib.auth.models import User
from rest_framework import serializers
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
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})

        # ✅ التحقق من عدم وجود المستخدم مسبقًا
        if User.objects.filter(username=data['email']).exists():
            raise serializers.ValidationError({"email": "This email is already registered."})

        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('confirm_password')

        # ✅ إنشاء المستخدم أولًا
        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=password,
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )

        # ✅ بعد كده أنشئ الأم بدون ربط بـ user
        mother = Mother.objects.create(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
        )

        return mother


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']  # بدون الأطفال
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


# ✅ تسجيل الدخول
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        from django.contrib.auth import authenticate
        user = authenticate(username=data['username'], password=data['password'])
        if user:
            return {
                'message': 'Login successful',
               
            }
        else:
            raise serializers.ValidationError({'message': 'Invalid credentials'})


# ✅ تسجيل الخروج
class LogoutSerializer(serializers.Serializer):
    def logout(self, request):
        from django.contrib.auth import logout
        logout(request)
        return {'message': 'Logout successful'}
