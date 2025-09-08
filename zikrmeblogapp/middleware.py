from typing import Callable


class ProxyHeaderMiddleware:
    """Normalize host and scheme from reverse proxy headers.

    Ensures Django builds absolute URLs using the external tunnel domain
    and protocol (https) instead of localhost/http.
    """

    def __init__(self, get_response: Callable):
        self.get_response = get_response

    def __call__(self, request):
        forwarded_host = request.META.get("HTTP_X_FORWARDED_HOST") or request.META.get("HTTP_X_ORIGINAL_HOST")
        if forwarded_host:
            request.META["HTTP_HOST"] = forwarded_host

        forwarded_proto = request.META.get("HTTP_X_FORWARDED_PROTO")
        if forwarded_proto:
            scheme = forwarded_proto.split(",")[0].strip()
            request.META["wsgi.url_scheme"] = scheme
            if scheme == "https":
                request.is_secure = lambda: True  # type: ignore[assignment]

        return self.get_response(request)


