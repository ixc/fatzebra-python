class GatewayError(Exception):
    def __init__(self, errors=[]):
        self.errors = errors

class AuthenticationError(Exception):
    pass

class GatewayUnknownResponseError(Exception):
    def __init__(self, code, response):
        self.code = code
        self.response = response