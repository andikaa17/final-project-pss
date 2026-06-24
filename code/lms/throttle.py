from ninja.throttling import BaseThrottle
from django.core.cache import cache
import time

class RedisRateThrottle(BaseThrottle):
    def __init__(self, rate="60/minute"):
        self.rate = rate
        self.num_requests, self.duration = self.parse_rate(rate)

    def parse_rate(self, rate):
        num, period = rate.split('/')
        num_requests = int(num)
        duration = {'second': 1, 'minute': 60, 'hour': 3600, 'day': 86400}[period]
        return num_requests, duration

    def allow_request(self, request):
        identifier = f"user_{request.auth.id}" if request.auth else f"ip_{request.META.get('REMOTE_ADDR', 'unknown')}"
        current_time = int(time.time())
        window_key = f"ratelimit:{identifier}:{current_time // self.duration}"
        
        request_count = cache.get(window_key, 0)
        
        if request_count >= self.num_requests:
            return False
        
        cache.set(window_key, request_count + 1, self.duration)
        return True