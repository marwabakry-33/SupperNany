from rest_framework.authtoken.models import Token as AuthToken
from django.contrib.auth import authenticate, login as mylogin, logout
from .serializers import *
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from rest_framework.views import APIView

from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import MotherSerializer

from rest_framework.authtoken.models import Token  # لازم تستورده
from rest_framework_simplejwt.tokens import RefreshToken


import random
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import User, PasswordResetCode

import logging
logger = logging.getLogger(__name__)


@api_view(['POST'])
def register(request):
    password = request.data.get('password')
    confirm_password = request.data.get('confirm_password')
    email = request.data.get('email')
    
    logger.info(f"Password: {password}")
    logger.info(f"Confirm Password: {confirm_password}")
    logger.info(f"Email: {email}")

    if not password or not isinstance(password, str):
        return Response({"error":"Password must be a non-empty string."}, status=status.HTTP_400_BAD_REQUEST)

    if not confirm_password or not isinstance(confirm_password, str):
        return Response({"error": "Confirm password must be a non-empty string."}, status=status.HTTP_400_BAD_REQUEST)

    if password != confirm_password:
        return Response({"error": "Passwords do not match."}, status=status.HTTP_400_BAD_REQUEST)

    if not email or not isinstance(email, str):
        return Response({"error": "Email must be a non-empty string."}, status=status.HTTP_400_BAD_REQUEST)

    serializer = MotherSerializer(data=request.data)
    if serializer.is_valid():
        mother = serializer.save()
        user = User.objects.get(username=email)

        # ✅ توليد JWT Token
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        mother_data = MotherSerializer(mother).data

        return Response({
            "message": "Registration successful",
            "access": access_token,
            "refresh": str(refresh),
            "mother": mother_data
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
        # جلب الأم المرتبطة بالمستخدم الحالي
        mother = Mother.objects.get(user=request.user)
        
        # استخدام Serializer لعرض بيانات الأم مع الأطفال
        serializer = MotherSerializer(mother)
        return Response(serializer.data)
    

class PreRegisterChildAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PrChildSerializer(data=request.data)
        if serializer.is_valid():
            try:
                # الحصول على الأم المرتبطة بالمستخدم الحالي
                mother = Mother.objects.get(user=request.user)
            except Mother.DoesNotExist:
                return Response({"error": "Mother not found for this user"}, status=status.HTTP_404_NOT_FOUND)

            # إنشاء الطفل مع ربطه بالأم
            child = preChild.objects.create(
                mother=mother,
                gender=serializer.validated_data['gender'],
                birth_date=serializer.validated_data['birth_date']
            )

            # اختياري: تخزين البيانات في session
            request.session['child_gender'] = serializer.validated_data['gender']
            request.session['child_birth_date'] = str(serializer.validated_data['birth_date'])

            return Response({
                'id': child.id,
                'gender': child.gender,
                'birth_date': child.birth_date,
                'message': 'Child has been successfully registered and linked to mother'
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegisterChildAPIView(APIView):
    def post(self, request):

        # ضفناهم للبيانات اللي جاية من الواجهة
        data = request.data.copy()
      
        serializer = ChildSerializer(data=data)
        if serializer.is_valid():
            # تأكدي هنا إن الأم مرتبطة بالمستخدم (لو ده موجود عندك)
            serializer.save(mother=request.user.mother)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def public_data_view(request):
    context = {
        'Advice Babies': AdviceBabySerializer(AdviceBaby.objects.all(), many=True).data,
        'Advice Bads': AdviceBadSerializer(AdviceBad.objects.all(), many=True).data,
        'Advice Mothers': AdviceMotherSerializer(AdviceMother.objects.all(), many=True).data,
        'Advice Bottle': BabyBottleAdviceSerializer(AdviceBottel.objects.all(), many=True).data,
        'Advice Moon': AdviceMoonSerializer(AdviceMoon.objects.all(), many=True).data,
        'How To': HowToSerializer(HowTo.objects.all(), many=True).data,
    }
    return Response(context)
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout(request):
    request.user.auth_token.delete()

    return Response({'message': 'Logout successful'}, status=200)

@api_view(['POST'])
def user_login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'message': 'Login successful',
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user_id': user.id,
                'username': user.username
            }, status=status.HTTP_200_OK)
        return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def RequestPasswordResetAPIView(request):
    serializer = PasswordResetRequestSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        try:
            user = User.objects.get(email=email)
            
            # توليد كود عشوائي
            code = str(random.randint(100000, 999999))  # توليد كود تحقق عشوائي
            
            # حفظ الكود في قاعدة البيانات
            PasswordResetCode.objects.update_or_create(
                user=user,
                defaults={'code': code}
            )
            
            # إرسال الكود عبر البريد الإلكتروني
            send_mail(
                'Password Reset Code',  # الموضوع
                f'Your verification code is: {code}',  # نص الرسالة
                'marwabakry284@gmail.com',  # هنا سيكون البريد الإلكتروني الثابت الذي يرسل منه
                [email],  # هذا هو البريد الإلكتروني للمستلم الذي أدخله المستخدم في الـ body
                fail_silently=False,
            )
            
            return Response({
                "message": "Verification code sent to your email.",
                "user_id": user.id
            }, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"error": "Email not found"}, status=status.HTTP_404_NOT_FOUND)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def ResetPasswordAPIView(request):
    user_id = request.data.get('user_id')
    new_password = request.data.get('new_password')
    code = request.data.get('code')

    try:
        user = User.objects.get(id=user_id)
        
        # تحقق من الكود
        reset_code = PasswordResetCode.objects.get(user=user)
        if reset_code.code != code:
            return Response({"error": "Invalid verification code."}, status=status.HTTP_400_BAD_REQUEST)
        
        # لو الكود صح غيري كلمة السر
        user.set_password(new_password)
        user.save()
        
        # ممكن تحذفي الكود بعد الاستخدام
        reset_code.delete()
        
        return Response({"message": "Password has been reset successfully."}, status=status.HTTP_200_OK)

    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    except PasswordResetCode.DoesNotExist:
        return Response({"error": "Verification code not found."}, status=status.HTTP_404_NOT_FOUND)

from rest_framework import generics

# لقراءة وإنشاء المهامfrom rest_framework.views import APIView

class TaskList(APIView):
    def get(self, request, format=None):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskDetail(APIView):
    def get_object(self,pk):
        try:
            return Task.objects.get(id=pk)
        except Task.DoesNotExist:
            return None
    def get_tasks_for_child(self, child_id):
        try:
            # الحصول على جميع المهام الخاصة بالطفل
            return Task.objects.filter(child__id=child_id)
        except Task.DoesNotExist:
            return None

    def get(self, request, child_id, format=None):
        tasks = self.get_tasks_for_child(child_id)
        if tasks:
            serializer = TaskSerializer(tasks, many=True)
            return Response(serializer.data)
        return Response({"error": "No tasks found for the specified child!"}, status=status.HTTP_404_NOT_FOUND)
    def put(self, request, pk, format=None):
        task = self.get_object(pk)
        if task:
            serializer = TaskSerializer(task, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "not found!"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk, format=None):
        task = self.get_object(pk)
        if task:
            task.delete()
            return Response({"message": "Deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "not found!"}, status=status.HTTP_404_NOT_FOUND)
