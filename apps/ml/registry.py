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