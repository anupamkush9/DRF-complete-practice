import traceback
from django.http import JsonResponse
from django.conf import settings

class CheckURLMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            if settings.DEBUG and request.method in ['POST', 'PATCH', 'PUT', 'DELETE'] and not request.path.endswith('/'):
                error_dict = {
                    "detail": "Please add a trailing slash to the url"
                }
                return JsonResponse(error_dict, status=400)
            # Code to be executed for each request before the view are called.
            resp = self.get_response(request)
            # Code to be executed for each request/response after the view is called.
            return resp
        except Exception as e:
            traceback.print_exc()
            print("Exception in CheckURLMiddleware", str(e))
        return self.get_response(request)

# Ref : https://docs.djangoproject.com/en/5.1/topics/http/middleware/#:~:text=Middleware%20is%20a%20framework%20of,for%20doing%20some%20specific%20function.    