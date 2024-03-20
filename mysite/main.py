
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

from user.models import CustomUser
from user.serializers import CustomUserRequestSchema



ins = CustomUser()
a = CustomUserRequestSchema(instance=ins)
print(a.data)