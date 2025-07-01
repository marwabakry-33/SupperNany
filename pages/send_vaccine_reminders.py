# send_vaccine_reminders.py

import os
import django
from datetime import date, timedelta
from django.core.mail import send_mail

# إعداد Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SupperNany.settings")  # ← غيريها
django.setup()

# استيراد موديلاتك
from pages.models import preChild2

def check_vaccines():
    today = date.today()

    for child in preChild2.objects.select_related('mother__user'):
        if not child.birth_date:
            continue

        mother = child.mother
        user = mother.user

        # جدول التطعيمات (بعد كم يوم من الميلاد)
        schedule = [
            (30, "تطعيم الشهر الأول"),
            (180, "تطعيم الست شهور"),
            (365, "تطعيم السنة الأولى"),
        ]

        for days, title in schedule:
            vaccine_date = child.birth_date + timedelta(days=days)

            # هل النهاردة ميعاد التطعيم؟
            if vaccine_date == today:
                send_mail(
                    subject='📌 تذكير بتطعيم ابنك',
                    message=f"عزيزتي {mother.first_name}، اليوم هو {title} لطفلك {child.baby}.",
                    from_email='marwabakry284@gmail.com',  # ← حطي إيميلك
                    recipient_list=[user.email],
                    fail_silently=False,
                )

if __name__ == "__main__":
    check_vaccines()
