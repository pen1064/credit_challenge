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
