import os
import sys

# تفعيل البيئة الافتراضية
activate_this = '/home/marwabakry23/SupperNany/.venv/bin/activate_this.py'
exec(open(activate_this).read(), {'__file__': activate_this})

# إضافة المسار إلى sys.path
path = '/home/marwabakry23/SupperNany'
if path not in sys.path:
    sys.path.append(path)

# تعيين إعدادات Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

# استيراد تطبيق WSGI
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
