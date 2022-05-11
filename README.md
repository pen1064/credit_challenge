# Deploying Single Model with Django (credit_challenge)
Lighter version of deploying ML model with Django and Docker, not so overkill :p\
In here, only one model is allowed, u either create a new one or replace the old one (no saving the old models)!

1. Create venv and install Django
```
virtualenv env
env\Scripts\activate.bat
pip3 install django
```
2. Start project 
```
cd backend
django-admin startproject mysite
cd mysite folder
pip3 install djangrestframework
pip3 install markdown
pip3 install django-filter
```
3. Start endpoints in the project 
```
python3 manage.py startapp endpoints
```
4. Create apps, put appname in it 
5. Change apps.py such that it knows we have moved the endpoints directory into apps
```
class EndpointsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.endpoints'
```
6. Edit settings to install apps (rest_frame, apps.endpoints, apps.ml) 
apps.ml is where you put your model for different endpoints
```
  INSTALLED_APPS = [
      'django.contrib.admin',
      'django.contrib.auth',
      'django.contrib.contenttypes',
      'django.contrib.sessions',
      'django.contrib.messages',
      'django.contrib.staticfiles',
      'rest_framework',
      'apps.endpoints',
      'apps.ml'] 
  SECRET_KEY = 'django-insecure-' # delete just for security reason
```
7. Edit apps/endpoints/apps.py, such that it knows the endpoints folder has moved into the apps folder
```
class EndpointsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.endpoints'
```
9. Edit apps/endpoints/models.py
Only one ml model is allowed to upload here
```
from django.db import models

# Create your models here.
class Endpoints(models.Model):
    name = models.CharField(max_length = 128)
    owner = models.CharField(max_length=128)
    created_date = models.DateTimeField(auto_now_add=True, blank=True)

class MLAlgorithm(models.Model):
    name = models.CharField(max_length = 128)
    status = models.CharField(max_length = 128)
    code = models.CharField(max_length = 10000000)
    created_date = models.DateTimeField(auto_now_add=True, blank=True)
    description = models.CharField(max_length = 1000)
    parent_endpoint = models.ForeignKey(Endpoints, on_delete=models.CASCADE)
    version = models.CharField(max_length = 128)

class MLRequest(models.Model):
    input_data = models.CharField(max_length = 100000000)
    response = models.CharField(max_length = 1000000000)
    full_response = models.CharField(max_length =1000000000)
    parent_algorithm = models.ForeignKey(MLAlgorithm, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True, blank=True)
```

8. Good time to migrate the fields into the db. 
```
python3 manage.py makemigrations
python3 manage.py migrate
```
9. Add [apps/endpoints/serializers.py](https://github.com/pen1064/credit_challenge/blob/main/apps/endpoints/serializers.py)
```
from apps.endpoints.models import Endpoints, MLAlgorithm, MLRequest
from rest_framework import serializers

class EndpointsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endpoints
        read_only_fields = ('id', 'name', 'owner', 'created_date')
        fields = read_only_fields

class MLAlgorithmSerializer(serializers.ModelSerializer):
    class Meta:
        model = MLAlgorithm
        read_only_fields = ('id', 'status', 'code', 'created_date', 'description', 'parent_endpoint', 'version')
        fields = read_only_fields

class MLRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = MLRequest
        read_only_fields = ('id', 'input_data', 'response', 'full_response', 'created_date', 'parent_algorithm')
        fields = read_only_fields
```
10. Edit [apps/endpoints/views.py](https://github.com/pen1064/credit_challenge/blob/main/apps/endpoints/views.py)
There are three basic views in total (each one for each model):\
   10.1 EndpointsViewSet\
   10.2 MLAlgorithmViewSet\
   10.3 MLRequestViewSet (store the requests made)\
The last one will be PredictView (for user to innput prediction, only POST) 

11. Create [apps/endpoints/urls.py](https://github.com/pen1064/credit_challenge/blob/main/apps/endpoints/urls.py) Add the links to urls (server side)
```
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EndpointsViewSet, MLAlgorithmViewSet, MLRequestViewSet, PredictView

router = DefaultRouter(trailing_slash=False)
router.register(r"endpoints", EndpointsViewSet, basename="endpoints")
router.register(r"mlalgorithms", MLAlgorithmViewSet, basename="mlalgorithms")
router.register(r"mlrequests", MLRequestViewSet, basename="mlrequests")

urlpatterns = [
    path(r"api/v1/", include(router.urls)),
    path(r"api/v1/classifier/predict", PredictView.as_view(), name='predict')]
```
12. Make a class for the ML moodel, and ofc test it!

13. Make registry to add connect the ML to server side -> [apps/ml/registry.py](https://github.com/pen1064/credit_challenge/blob/main/apps/ml/registry.py)
```
from apps.endpoints.models import Endpoints, MLAlgorithm 
class MLRegistry:
    def __init__(self):
        self.endpoints={}
        
    def add_algorithm(self, endpoint_name, alg_obj, alg_status, alg_name, alg_ver, alg_description, alg_code, alg_owner):
        endpoint, _ = Endpoints.objects.get_or_create(name=endpoint_name, owner=alg_owner)
        
        if MLAlgorithm.objects.filter(parent_endpoint = endpoint).exists():
            MLAlgorithm.objects.filter(parent_endpoint = endpoint).update(code=alg_code, description=alg_description, version=alg_ver, status=alg_status, name=alg_name)
        else:
            MLAlgorithm.objects.get_or_create(parent_endpoint = endpoint, code=alg_code, description=alg_description, version=alg_ver, status=alg_status, name=alg_name)

        self.endpoints = alg_obj
 ```
14. Definitely put some test case to test your registry 
12. Double Check asgi.py 
```
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'credit_challenge.settings')
```
13. Edit urls.py
```
  from apps.endpoints.urls import urlpatterns as endpoints_urlpatterns
  urlpatterns += endpoints_urlpatterns
```
15. Use [wsgi.py](https://github.com/pen1064/credit_challenge/blob/main/credit_challenge/wsgi.py) to add MLAlgorithm 
```
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
```
16. Corss your finger hopes everything will workout!
<img width="611" alt="image" src="https://user-images.githubusercontent.com/45325095/167357185-1c6feab1-7a48-450f-b919-dde7fa0f5fed.png">
<img width="586" alt="image" src="https://user-images.githubusercontent.com/45325095/167356799-70317e81-59d1-4350-9716-27b9fd94a3a9.png">
<img width="600" alt="image" src="https://user-images.githubusercontent.com/45325095/167356842-1b21982b-94c0-4bd3-865e-97245883907e.png">
<img width="630" alt="image" src="https://user-images.githubusercontent.com/45325095/167356940-d9fd4387-c9e7-4644-82ae-d5788591140e.png">

17. Test it out with query, copy and past the query from [here](https://github.com/pen1064/credit_challenge/blob/main/apps/ml/classifier/query.json)

19. Start creating Dockerfile and docker-compose yaml 
```
docker-compose build # build docker
docker-compose up -d #to run

```
<p align="center">
<img src="https://user-images.githubusercontent.com/45325095/167355679-81f64d66-2022-4844-b5f0-b99be572d04d.png" width="250" height="180" />
 </p>


