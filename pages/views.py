from rest_framework.authtoken.models import Token as AuthToken
from django.contrib.auth import authenticate, login as mylogin, logout
from .serializers import *
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
import random
from django.core.mail import send_mail
from .models import User, PasswordResetCode
from django.utils.translation import gettext as _
from rest_framework import generics
import logging
import os
from django.conf import settings


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
        return Response({"error": _("Password must be a non-empty string.")}, status=status.HTTP_400_BAD_REQUEST)

    if not confirm_password or not isinstance(confirm_password, str):
        return Response({"error": _("Confirm password must be a non-empty string.")}, status=status.HTTP_400_BAD_REQUEST)

    if password != confirm_password:
        return Response({"error": _("Passwords do not match.")}, status=status.HTTP_400_BAD_REQUEST)

    if not email or not isinstance(email, str):
        return Response({"error": _("Email must be a non-empty string.")}, status=status.HTTP_400_BAD_REQUEST)

    serializer = MotherSerializer(data=request.data)
    if serializer.is_valid():
        mother = serializer.save()
        user = User.objects.get(username=email)
        
        send_mail(
            subject="تأكيد التسجيل",
            message=f"مرحبًا {mother.first_name}، تم إنشاء حسابك بنجاح على التطبيق.",
            from_email=None,  # سيستخدم EMAIL_HOST_USER تلقائيًا
            recipient_list=[email],
            fail_silently=False,
        )


        # ✅ توليد JWT Token
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        mother_data = MotherSerializer(mother).data

        return Response({
            "message": _("Registration successful"),
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



@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_mother_profile(request):
    try:
        mother = Mother.objects.get(user=request.user)
    except Mother.DoesNotExist:
        return Response({"error": "الأم غير موجودة."}, status=status.HTTP_404_NOT_FOUND)

    serializer = MotherUpdateSerializer(mother, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        
        # تحديث الإيميل في User نفسه لو اتغير
        if 'email' in request.data:
            request.user.username = request.data['email']
            request.user.email = request.data['email']
            request.user.save()
        
        return Response({
            "message": "updated successfully.",
            "mother": serializer.data
        }, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PreRegisterChildAPIView2(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PrChildSerializer2(data=request.data)
        if serializer.is_valid():
            try:
                mother = Mother.objects.get(user=request.user)
            except Mother.DoesNotExist:
                return Response({"error": _("Mother not found for this user")}, status=status.HTTP_404_NOT_FOUND)

            # إنشاء الطفل
            child = preChild2.objects.create(
                mother=mother,
                baby=serializer.validated_data['baby'],
                gender=serializer.validated_data['gender'],
                birth_date=serializer.validated_data['birth_date']
            )

            # 🔔 إرسال نصيحة عشوائية على الإيميل
            try:
                advice_list = AdviceBaby.objects.all()
                if advice_list.exists() and request.user.email:
                    advice = random.choice(advice_list)
                    advice_text = advice.advice_baby  # أو استخدمي advice.advice_baby_ar لو عايزة بالعربي
                    send_mail(
                        subject='👶 نصيحة للطفل الجديد من Supper Nany',
                        message=advice_text,
                        from_email='marwabakry284@gmail.com', 
                        recipient_list=[request.user.email],
                        fail_silently=True,
                    )
            except Exception as e:
                print(f"❗ فشل إرسال الإيميل: {e}")

            # 🎟️ توليد التوكن
            refresh = RefreshToken.for_user(request.user)

            return Response({
                'child': {
                    'id': child.id,
                    'baby': child.baby,
                    'gender': child.gender,
                    'birth_date': child.birth_date,
                    'message': _('Child has been successfully registered and linked to mother')
                },
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetChildByIdAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, child_id):
        try:
            # التأكد إن الطفل ينتمي للأم الخاصة بالمستخدم الحالي
            mother = Mother.objects.get(user=request.user)
            child = preChild2.objects.get(id=child_id, mother=mother)

            serializer = PrChildSerializer2(child)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Mother.DoesNotExist:
            return Response({'error': _('Mother not found')}, status=status.HTTP_404_NOT_FOUND)
        except preChild2.DoesNotExist:
            return Response({'error': _('Child not found or does not belong to this mother')}, status=status.HTTP_404_NOT_FOUND)


LAST_USER_FILE = os.path.join(settings.BASE_DIR, 'last_user.txt')



LAST_CHILD_FILE = 'last_child_id.txt'  # تأكدي من المسار الصحيح للملف المؤقت



@api_view(['POST'])
def user_login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            try:
                mother = Mother.objects.get(user=user)
                child = preChild2.objects.filter(mother=mother).first()
            except Mother.DoesNotExist:
                child = None

            # حذف صورة الطفل السابق
            last_child_id = None
            if os.path.exists(LAST_CHILD_FILE):
                with open(LAST_CHILD_FILE, 'r') as f:
                    last_child_id = f.read().strip()

            if child and last_child_id and str(child.id) != last_child_id:
                try:
                    photo = ChildPhoto.objects.get(pre_id=last_child_id)
                    if photo.photo and os.path.isfile(photo.photo.path):
                        os.remove(photo.photo.path)
                    photo.delete()
                except ChildPhoto.DoesNotExist:
                    pass

            # تحديث ملف الطفل الحالي
            if child:
                with open(LAST_CHILD_FILE, 'w') as f:
                    f.write(str(child.id))

            # إرسال نصيحة
            advice_list = AdviceMother.objects.all()
            if advice_list.exists():
                random_advice = random.choice(advice_list)
                advice_text = random_advice.advice_mather

                email_message = f"""
مرحبًا {user.first_name if hasattr(user, 'first_name') else ''} 👋

تم تسجيل الدخول بنجاح ✅

💡 نصيحة اليوم للأمهات:
{advice_text}
"""
                send_mail(
                    subject="نصيحة اليوم بعد تسجيل الدخول 🌸",
                    message=email_message,
                    from_email="marwabakry284@gmail.com",
                    recipient_list=[user.email],
                    fail_silently=True
                )

            # إرسال تذكير بالتطعيم
            if child:
                today = date.today()
                birth_date = child.birth_date
                vaccination_dates = [birth_date + timedelta(days=90 * i) for i in range(1, 5)]
                for v_date in vaccination_dates:
                    if v_date == today + timedelta(days=1):
                        send_mail(
                            subject="📅 تذكير: تطعيم الطفل غدًا",
                            message=f"مرحبًا {user.first_name or ''}،\n\nتذكير: معاد تطعيم طفلك غدًا {v_date}.\nيرجى الاستعداد 🌸",
                            from_email="marwabakry284@gmail.com",
                            recipient_list=[user.email],
                            fail_silently=True
                        )
                        break
                    elif v_date == today:
                        send_mail(
                            subject="💉 اليوم معاد تطعيم الطفل!",
                            message=f"صباح الخير {user.first_name or ''}،\n\nاليوم {v_date} هو ميعاد تطعيم طفلك.\nيرجى التوجه لأقرب وحدة صحية ✅",
                            from_email="marwabakry284@gmail.com",
                            recipient_list=[user.email],
                            fail_silently=True
                        )
                        break

            # إنشاء JWT
            refresh = RefreshToken.for_user(user)
            child_data = {
                'id': child.id,
                'baby': child.baby,
                'gender': child.gender,
                'birth_date': child.birth_date
            } if child else None

            return Response({
                'message': 'Login successful',
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user_id': user.id,
                'username': user.username,
                'child': child_data
            }, status=status.HTTP_200_OK)

        return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegisterChildAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if not hasattr(user, 'mother'):
            return Response({"error": "لا يوجد ملف أم مرتبط بهذا المستخدم."}, status=404)

        # جلب الأطفال المرتبطين بالأم
        children = Child.objects.filter(mother=user.mother)

        serializer = ChildSerializer(children, many=True)
        return Response(serializer.data)

    def post(self, request):
        user = request.user

        pre_id = request.data.get('pre_id')
        if not pre_id:
            return Response({"error": "يرجى إرسال pre_id المرتبط بالطفل."}, status=400)

        try:
            pre = preChild2.objects.get(id=pre_id, mother__user=user)
        except preChild2.DoesNotExist:
            return Response({"error": "preChild2 غير موجود أو ليس بمالِك الأم."}, status=404)

        serializer = ChildSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(mother=user.mother, pre=pre)
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)

# داله ل edit for child
class UpdateChildAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        user = request.user
        try:
            mother = user.mother
        except Mother.DoesNotExist:
            return Response({"detail": "هذا المستخدم غير مرتبط بأي أم."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            child = Child.objects.get(pk=pk, mother=mother)
        except Child.DoesNotExist:
            return Response({"detail": "هذا الطفل غير موجود أو لا يتبع هذه الأم."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ChildSerializer(child, data=request.data, partial=True)  # partial=True يسمح بتعديل جزئي

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

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


# لقراءة وإنشاء المهامfrom rest_framework.views import APIView

class TaskList(APIView):
    def get(self, request, format=None):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True, context={'request': request})  # ✅ أضفنا context
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = TaskSerializer(data=request.data, context={'request': request})  # ✅ أضفنا context
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
            serializer = TaskSerializer(tasks, many=True, context={'request': request})  # ✅ أضفنا context
            return Response(serializer.data)
        return Response({"error": _("No tasks found for the specified child!")}, status=status.HTTP_404_NOT_FOUND)
    def put(self, request, pk, format=None):
        task = self.get_object(pk)
        if task:
            serializer = TaskSerializer(task, data=request.data, context={'request': request})  # ✅ أضفنا context
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": _("Task not found!")}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk, format=None):
        task = self.get_object(pk)
        if task:
            task.delete()
            return Response({"message": _("Deleted successfully!")}, status=status.HTTP_204_NO_CONTENT)
        return Response({"error": _("Task not found!")}, status=status.HTTP_404_NOT_FOUND)


class RandomAdviceView(APIView):
    def get(self, request, category):
        model_map = {
            'baby': (AdviceBaby, AdviceBabySerializer),
            'mother': (AdviceMother, AdviceMotherSerializer),
            'bad': (AdviceBad, AdviceBadSerializer),
            'bottle': (AdviceBottel, BabyBottleAdviceSerializer),
            'moon': (AdviceMoon, AdviceMoonSerializer),
        }

        if category not in model_map:
            return Response({'error': _("Invalid category")}, status=status.HTTP_400_BAD_REQUEST)

        model_class, serializer_class = model_map[category]
        advice_list = model_class.objects.all()

        if not advice_list.exists():
            return Response({'message': _(f'No {category} advice found.')}, status=status.HTTP_404_NOT_FOUND)

        random_advice = random.choice(advice_list)
        serializer = serializer_class(random_advice)
        return Response(serializer.data)
class FavoriteTasksForChild(APIView):
    def get(self, request, child_id, format=None):
        tasks = Task.objects.filter(child__id=child_id, is_favorite=True)
        if tasks.exists():
            serializer = TaskSerializer(tasks, many=True, context={'request': request})
            return Response(serializer.data)
        return Response({"error": _("No favorite tasks found!")}, status=status.HTTP_404_NOT_FOUND)



class HowToByCategoryView(generics.ListCreateAPIView):  # بدل ListAPIView
    serializer_class = HowToSerializer

    def get_queryset(self):
        category = self.kwargs.get('category')
        return HowTo.objects.filter(category=category)

    def perform_create(self, serializer):
        category = self.kwargs.get('category')
        serializer.save(category=category)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_child_photo(request, child_id):
    try:
        child = Child.objects.get(id=child_id, mother__user=request.user)
        pre = child.pre  
    except (Child.DoesNotExist, preChild2.DoesNotExist):
        return Response({"error": "Child or related preChild2 not found."}, status=404)

    photo = request.FILES.get('photo')
    if not photo:
        return Response({"error": "No photo provided."}, status=400)

    ChildPhoto.objects.create(pre=pre, photo=photo)
    return Response({"message": "Photo uploaded successfully."})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_child_photo(request, child_id):
    try:
        child = Child.objects.get(id=child_id, mother__user=request.user)
        pre = child.pre
        photo = ChildPhoto.objects.get(pre=pre)
    except Child.DoesNotExist:
        return Response({"error": "الطفل غير موجود"}, status=404)
    except preChild2.DoesNotExist:
        return Response({"error": "لا يوجد سجل pre للطفل"}, status=404)
    except ChildPhoto.DoesNotExist:
        return Response({"error": "لا توجد صورة لهذا الطفل"}, status=404)

    serializer = ChildPhotoSerializer(photo)
    return Response(serializer.data, status=200)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_child_photo(request, child_id):
    try:
        child = Child.objects.get(id=child_id, mother__user=request.user)
        pre = child.pre
    except (Child.DoesNotExist, preChild2.DoesNotExist):
        return Response({"error": "الطفل غير موجود أو pre غير متوفر"}, status=404)

    photo_file = request.FILES.get('photo')
    if not photo_file:
        return Response({"error": "يجب توفير صورة"}, status=400)

    try:
        photo_obj = ChildPhoto.objects.get(pre=pre)
        photo_obj.photo = photo_file
        photo_obj.save()
    except ChildPhoto.DoesNotExist:
        ChildPhoto.objects.create(pre=pre, photo=photo_file)

    return Response({"message": "تم التحديث بنجاح"}, status=200)

from .models import preChild2  # أو import as Child

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_growth_record(request, child_id):
    try:
        child = preChild2.objects.get(id=child_id, mother__user=request.user)
    except preChild2.DoesNotExist:
        return Response({'error': 'الطفل غير موجود أو غير مرتبط بهذه الأم.'}, status=404)

    serializer = GrowthRecordSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(child=child)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_growth_records(request, child_id):
    try:
        child = preChild2.objects.get(id=child_id, mother__user=request.user)
    except preChild2.DoesNotExist:
        return Response({'error': 'الطفل غير موجود أو غير مرتبط بهذه الأم.'}, status=404)

    records = GrowthRecord.objects.filter(child=child).order_by('date')
    serializer = GrowthRecordSerializer(records, many=True)
    return Response(serializer.data)

@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_growth_record(request, child_id, record_id):
    try:
        # التأكد من ملكية الطفل
        child = preChild2.objects.get(id=child_id, mother__user=request.user)
    except preChild2.DoesNotExist:
        return Response({'error': 'الطفل غير موجود أو غير مرتبط بهذه الأم.'}, status=404)

    try:
        # التأكد من أن سجل النمو يتبع نفس الطفل
        record = GrowthRecord.objects.get(id=record_id, child=child)
    except GrowthRecord.DoesNotExist:
        return Response({'error': 'سجل النمو غير موجود لهذا الطفل.'}, status=404)

    serializer = GrowthRecordSerializer(record, data=request.data, partial=True)  # partial=True يسمح بالتحديث الجزئي
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=200)
    return Response(serializer.errors, status=400)


from datetime import date, timedelta
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Child  # أو عدلي حسب مكان موديل الطفل
from django.contrib.auth.models import User  # أو موديل المستخدم عندك

from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from .models import preChild2  # حسب مكان الموديل





@api_view(['GET'])
@permission_classes([IsAuthenticated])
def test_vaccine_reminder(request):
    user = request.user
    try:
        mother = Mother.objects.get(user=user)
        child = preChild2.objects.get(mother=mother)
    except (Mother.DoesNotExist, preChild2.DoesNotExist):
        return Response({"error": "لا توجد بيانات أم أو طفل"}, status=404)

    today = date.today()
    birth_date = child.birth_date
    if isinstance(birth_date, datetime):
        birth_date = birth_date.date()

    vaccination_dates = [birth_date + timedelta(days=90 * i) for i in range(1, 5)]

    for v_date in vaccination_dates:
        if v_date == today + timedelta(days=1):
            send_mail(
                subject="📅 تذكير: تطعيم الطفل غدًا",
                message=f"مرحبًا {user.first_name or ''}،\n\nتذكير: معاد تطعيم طفلك غدًا {v_date}.\nيرجى الاستعداد 🌸",
                from_email="marwabakry284@gmail.com",
                recipient_list=[user.email],
                fail_silently=False
            )
            return Response({"message": f"📧 تم إرسال تذكير بتطعيم الطفل غدًا ({v_date})."})
        elif v_date == today:
            send_mail(
                subject="💉 اليوم معاد تطعيم الطفل!",
                message=f"صباح الخير {user.first_name or ''}،\n\nاليوم {v_date} هو ميعاد تطعيم طفلك.\nيرجى التوجه لأقرب وحدة صحية ✅",
                from_email="marwabakry284@gmail.com",
                recipient_list=[user.email],
                fail_silently=False
            )
            return Response({"message": f"📧 تم إرسال تذكير بتطعيم الطفل اليوم ({v_date})."})

    return Response({"message": "لا يوجد تطعيم اليوم أو غدًا."})
