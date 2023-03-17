from rest_framework.response import Response
from rest_framework import status
from functools import wraps

def required_params(request_attr='query_params', params=None):
    """
    When we use @required_params(params=['same_param']),
    this required_params func should return a decorator func,
    its parameters are the view_func wrapped by @required_params 
    """
    if params is None:
        params = []

    def decorator(view_func):
        """
        decorator func use wraps to pass in view_func' params
        pass to _wrapped_view
        here, instance param is actually the self in view_func
        """
        @wraps(view_func)
        def __wrapped_view(instance, request, *args, **kwargs):
            data = getattr(request, request_attr)
            missing_params = [
                param
                for param in params
                if param not in data
            ]
            if missing_params:
                param_str = '.'.join(missing_params)
                return Response({
                    'message': u'missing {} in request'.format(param_str),
                    'success': False,
                }, status=status.HTTP_400_BAD_REQUEST)
            # after checking, we then call the view_func wrapped by @required_params 
            return view_func(instance, request, *args, **kwargs)
        return __wrapped_view
    return decorator
