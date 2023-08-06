from python_framework import StaticConverter

try:
    import SubscriptionConstant
except:
    from queue_manager_api.api.src.constant import SubscriptionConstant


class SubscriptionRequestDto:
    def __init__(self,
        key = None,
        url = None,
        onErrorUrl = None,
        maxTries = None,
        backOff = None,
        queue = None
    ):
        self.key = key
        self.url = url
        self.onErrorUrl = onErrorUrl
        self.maxTries = StaticConverter.getValueOrDefault(maxTries, SubscriptionConstant.DEFAULT_MAX_TRIES)
        self.backOff = StaticConverter.getValueOrDefault(backOff, SubscriptionConstant.DEFAULT_BACKOFF)
        self.queue = queue


class SubscriptionResponseDto:
    def __init__(self,
        key = None,
        url = None,
        onErrorUrl = None,
        maxTries = None,
        backOff = None,
        headers = None,
        queue = None
    ):
        self.key = key
        self.url = url
        self.onErrorUrl = onErrorUrl
        self.maxTries = StaticConverter.getValueOrDefault(maxTries, SubscriptionConstant.DEFAULT_MAX_TRIES)
        self.backOff = StaticConverter.getValueOrDefault(backOff, SubscriptionConstant.DEFAULT_BACKOFF)
        self.queue = queue
