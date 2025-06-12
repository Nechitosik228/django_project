import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
print(os.environ.get("DJANGO_SETTINGS_MODULE"))