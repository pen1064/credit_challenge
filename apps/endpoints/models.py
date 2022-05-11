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