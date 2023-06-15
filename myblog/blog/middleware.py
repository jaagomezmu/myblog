import os

import redis


class RedisVisitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        redis_host = os.environ.get('REDIS_HOST', 'localhost')
        redis_port = int(os.environ.get('REDIS_PORT', 6379))
        self.redis = redis.Redis(host=redis_host, port=redis_port, db=0)

    def __call__(self, request):
        response = self.get_response(request)
        if request.method == 'GET' and request.resolver_match:
            pk = request.resolver_match.kwargs.get('pk')
            key = f'post:{pk}:visits'
            self.redis.incr(key)
        return response
