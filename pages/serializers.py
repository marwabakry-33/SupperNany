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


class MotherSerializer(serializers.ModelSerializer):
    # تضمين فقط الحقول المتعلقة بالأم
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Mother
        fields = ['id', 'first_name', 'last_name', 'email', 'username', 'password']

    def validate_email(self, value):
        if Mother.objects.filter(email=value).exists():
            raise serializers.ValidationError("البريد الإلكتروني مسجل مسبقًا")
        return value

    def validate(self, data):
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({"username": "اسم المستخدم مستخدم من قبل."})
        return data

    def create(self, validated_data):
        username = validated_data.pop('username')
        password = validated_data.pop('password')

        # إنشاء مستخدم الأم
        user = User.objects.create_user(username=username, password=password)

        # إنشاء الأم وربطها بالمستخدم
        mother = Mother.objects.create(user=user, **validated_data)

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
