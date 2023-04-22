from django.core import serializers
from utils.json_encoder import JSONEncoder

class DjangoModelSerializer:

    @classmethod
    def serialize(cls, instance):
        # Django serializers default needs a queryset or list to do serializer
        # so we need to add a [] to instance, make it a list
        return serializers.serialize('json', [instance], cls=JSONEncoder)
    
    @classmethod
    def deserialize(cls, serialized_data):
        # needs to add .object to get the original model type
        # or you didn't get an ORM object, but instead, you get a deserializedobject type
        return list(serializers.deserialize('json', serialized_data))[0].object
