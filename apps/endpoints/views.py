from django.shortcuts import render
from rest_framework import views, mixins, viewsets
from rest_framework.response import Response
from apps.endpoints.models import Endpoints, MLAlgorithm, MLRequest
from apps.endpoints.serializers import EndpointsSerializer,  MLAlgorithmSerializer, MLRequestSerializer
from credit_challenge.wsgi import registry
import json

# Create your views here.
class EndpointsViewSet( mixins.RetrieveModelMixin, 
                        mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = EndpointsSerializer
    queryset = Endpoints.objects.all()
    
class MLAlgorithmViewSet(mixins.RetrieveModelMixin, 
                        mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = MLAlgorithmSerializer
    queryset =  MLAlgorithm.objects.all()

class MLRequestViewSet(mixins.RetrieveModelMixin, 
                        mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = MLRequestSerializer
    queryset = MLRequest.objects.all()


class PredictView(views.APIView):
    def post(self, request, endpoint_name='classifier', format=None):
        alg = MLAlgorithm.objects.filter(parent_endpoint__name = endpoint_name)
        print(alg)
        if alg is None:
            return Response({'status':'error'})
        else:
            alg_obj = registry.endpoints
            prediction = alg_obj.prediction(self.request.data)
            label = prediction['label'] if 'label' in prediction else 'error'
            mlrequest = MLRequest(input_data= json.dumps(request.data), full_response=prediction, response=label, parent_algorithm=alg[0])
            mlrequest.save()

            prediction['request_id'] = mlrequest.id

            return Response(prediction)