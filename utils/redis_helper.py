from django.conf import settings
from utils.redis_serializers import DjangoModelSerializer
from utils.redis_client import RedisClient

class RedisHelper:
    
    @classmethod
    def _load_objects_to_cache(cls, key, objects):
        conn = RedisClient.get_connection()

        serialized_list = []
        # add redis_list_limit constrain
        for obj in objects[:settings.REDIS_LIST_LENGTH_LIMIT]:
            serialized_data = DjangoModelSerializer.serialize(obj)
            serialized_list.append(serialized_data)
        
        if serialized_list:
            conn.rpush(key, *serialized_list)
            conn.expire(key, settings.REDIS_KEY_EXPIRE_TIME)

    @classmethod
    def load_objects(cls, key, queryset):
        conn = RedisClient.get_connection()

        # if in cache, return directly
        if conn.exists(key):
            serialized_list = conn.lrange(key, 0, -1) # [0, -1] get all
            objects = []
            for serialized_data in serialized_list:
                deserialized_obj = DjangoModelSerializer.deserialize(serialized_data)
                objects.append(deserialized_obj)
            return objects
        
        # cache miss
        cls._load_objects_to_cache(key, queryset)

        # convert to list to make sure the return type is consistent
        return list(queryset)
        

    @classmethod
    def push_object(cls, key, obj, queryset):
        conn = RedisClient.get_connection()
        if not conn.exists(key):
            # if key doesn't exist, load from db
            cls._load_objects_to_cache(key, queryset)
            return
        serialized_data = DjangoModelSerializer.serialize(obj)
        conn.lpush(key, serialized_data)
        conn.ltrim(key, 0, settings.REDIS_LIST_LENGTH_LIMIT - 1)
