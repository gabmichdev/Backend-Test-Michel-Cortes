from django.conf import settings
from django.contrib.sessions.middleware import SessionMiddleware
from django.utils.cache import add_never_cache_headers


class HealthCheckAwareSessionMiddleware(SessionMiddleware):
    def process_request(self, request):
        if request.path_info.startswith("/healthz"):
            request.COOKIES[settings.SESSION_COOKIE_NAME] = "healthcheck"
        super(HealthCheckAwareSessionMiddleware, self).process_request(request)


class HeaderNoCacheMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.method == "GET" and not response.has_header("Cache-Control"):
            add_never_cache_headers(response)

        return response
