import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')  # غيّري 'project' لاسم مجلد الإعدادات عندك

application = get_wsgi_application()
