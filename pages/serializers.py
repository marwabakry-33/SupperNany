# serializers.py

from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token as AuthToken

from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
import json
class TaskSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Task
        fields = ['id', 'child', 'content']

# Create serializer for GrowthRecord
class GrowthRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = GrowthRecord
        fields = ['record_date', 'weight', 'height', 'head_circumference']
# Create serializer for Child
class ChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Child
        fields = ['baby', 'feedings', 'sleeping', 'Diapers', 'weight', 'height', 'photo']

class PrChildSerializer(serializers.Serializer):
    
    gender = serializers.ChoiceField(choices=[('male', 'Male'), ('female', 'Female')])
    birth_date = serializers.DateField()



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
        password = data['password']  # إزالة المسافات الزائدة
        confirm_password = data['confirm_password']  # إزالة المسافات الزائدة

        if password != confirm_password:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})

        # ✅ التحقق من عدم وجود المستخدم مسبقًا
        if User.objects.filter(username=data['email']).exists():
            raise serializers.ValidationError({"email": "This email is already registered."})
         

        return data

    
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
    advice_baby_ar = serializers.CharField(read_only=True)
    advice_baby_en = serializers.CharField(read_only=True)

    class Meta:
        model = AdviceBaby
        fields = ['id', 'advice_baby', 'advice_baby_ar', 'advice_baby_en']


class AdviceBadSerializer(serializers.ModelSerializer):
    advice_bad_ar = serializers.CharField(read_only=True)
    advice_bad_en = serializers.CharField(read_only=True)

    class Meta:
        model = AdviceBad
        fields = ['id', 'advice_bad', 'advice_bad_ar', 'advice_bad_en']


class AdviceMotherSerializer(serializers.ModelSerializer):
    advice_mather_ar = serializers.CharField(read_only=True)
    advice_mather_en = serializers.CharField(read_only=True)

    class Meta:
        model = AdviceMother
        fields = ['id', 'advice_mather', 'advice_mather_ar', 'advice_mather_en']

class BabyBottleAdviceSerializer(serializers.ModelSerializer):
    advice_baby_ar = serializers.CharField(read_only=True)
    advice_baby_en = serializers.CharField(read_only=True)

    class Meta:
        model = AdviceBottel
        fields = ['id', 'advice_baby', 'advice_baby_ar', 'advice_baby_en']

class AdviceMoonSerializer(serializers.ModelSerializer):
    advice_baby_ar = serializers.CharField(read_only=True)
    advice_baby_en = serializers.CharField(read_only=True)

    class Meta:
        model = AdviceMoon
        fields = ['id', 'advice_baby', 'advice_baby_ar', 'advice_baby_en']


# Serializer for HowTo
class HowToSerializer(serializers.ModelSerializer):
    content_ar = serializers.SerializerMethodField()
    content_en = serializers.SerializerMethodField()
    advice_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = HowTo
        fields = ['id', 'category', 'content', 'advice_id']

    def get_content_ar(self, obj):
        try:
            content_json = json.loads(obj.content)
            return content_json.get("ar", "")
        except Exception:
            return ""

    def get_content_en(self, obj):
        try:
            content_json = json.loads(obj.content)
            return content_json.get("en", "")
        except Exception:
            return ""

    def create(self, validated_data):
        advice_id = validated_data.pop('advice_id', None)
        if advice_id:
            from .models import Advice  # تأكدي إن Advice مستوردة بشكل صحيح
            advice = Advice.objects.filter(id=advice_id).first()
            if advice:
                validated_data['advice'] = advice
        return super().create(validated_data)

  
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        # التحقق من وجود اسم المستخدم وكلمة المرور
        if not data.get('username') or not data.get('password'):
            raise serializers.ValidationError({'message': 'Username and password are required'})

        return data

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
