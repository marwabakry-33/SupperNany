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

@api_view(['POST'])
def register(request):
    password = request.data.get('password')
    confirm_password = request.data.get('confirm_password')
    email = request.data.get('email')

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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
        # جلب الأم المرتبطة بالمستخدم الحالي
        mother = Mother.objects.get(user=request.user)
        
        # استخدام Serializer لعرض بيانات الأم مع الأطفال
        serializer = MotherSerializer(mother)
        return Response(serializer.data)
    
    
@api_view(['POST'])
def user_login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    print(f"🔍 Trying to authenticate: {username} - {password}")  # ✅ طباعة البيانات للتحقق

    user = authenticate(username=username, password=password)
    if user is not None:
        mylogin(request, user)
        token, created = Token.objects.get_or_create(user=user)
        print("✅ Login successful!")  # ✅ تأكيد نجاح تسجيل الدخول
        return Response({
            'message': 'Login successful',
            'token': token.key,
            'user_id': user.id,
            'username': user.username 
        }, status=200)
    else:
        print("❌ Invalid credentials!")  # ❌ طباعة عند فشل تسجيل الدخول
        return Response({'message': 'Invalid credentials'}, status=400)

# views.py

class PreRegisterChildAPIView(APIView):
    def post(self, request):
        serializer = PrChildSerializer(data=request.data)
        if serializer.is_valid(): # تخزين في session
            request.session['child_type'] = serializer.validated_data['type']
            request.session['child_birth_date'] = str(serializer.validated_data['birth_date'])
            return Response({'message': 'تم حفظ بيانات الطفل مؤقتاً'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegisterChildAPIView(APIView):
    def post(self, request):
        # جبنا البيانات من الجلسة
        child_type = request.session.get('child_type')
        birth_date = request.session.get('child_birth_date')

        # ضفناهم للبيانات اللي جاية من الواجهة
        data = request.data.copy()
        if child_type and birth_date:
            data['type'] = child_type
            data['birth_date'] = birth_date

        serializer = ChildSerializer(data=data)
        if serializer.is_valid():
            # تأكدي هنا إن الأم مرتبطة بالمستخدم (لو ده موجود عندك)
            serializer.save(mother=request.user.mother)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout(request):
    request.user.auth_token.delete()

    return Response({'message': 'Logout successful'}, status=200)

