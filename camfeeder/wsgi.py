"""
WSGI config for camfeeder project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""
import site
import sys
import os

prev_sys_path = list(sys.path)
root = os.path.normpath(os.path.join(os.path.dirname("/vagrant/camfeeder/camfeeder/"), "../"))
settings_path = os.path.normpath(os.path.join(root, "camfeeder/"))
sys.path.append(root)
site.addsitedir(os.path.join(root, ".env/lib/python2.6/site-packages"))

new_sys_path = []
for item in list(sys.path):
    if item not in prev_sys_path:
        new_sys_path.append(item)
        sys.path.remove(item)
sys.path[:0] = new_sys_path

os.environ["DJANGO_SETTINGS_MODULE"] = "camfeeder.settings"

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
