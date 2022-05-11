"""
WSGI config for credit_challenge project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'credit_challenge.settings')

from apps.ml.registry import MLRegistry
from apps.ml.classifier.xgb_model import MLModel
import inspect
registry = MLRegistry()
xgb = MLModel()
try:
    registry.add_algorithm(endpoint_name='classifier', alg_obj=xgb, alg_status='production', 
    alg_name='xgb', alg_ver='1.0.0', alg_description='first', alg_owner='pk', 
    alg_code = inspect.getsource(MLModel))
except Exception as e:
    print('exception', str(e))

application = get_wsgi_application()
