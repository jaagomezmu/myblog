import redis

class RedisVisitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.redis = redis.Redis(host='localhost', port=6379, db=0)

    def __call__(self, request):
        response = self.get_response(request)
        if request.method == 'GET' and request.resolver_match:
            pk = request.resolver_match.kwargs.get('pk')
            key = f'post:{pk}:visits'
            self.redis.incr(key)
        return response
