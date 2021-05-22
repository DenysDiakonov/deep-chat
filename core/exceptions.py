class APIException(Exception):
    status_code = 500
    default_detail = "A server error occurred."

    def __init__(self, detail=None, code=None):
        if detail is None:
            self.detail = self.default_detail
        else:
            self.detail = detail
        if code is None:
            self.code = self.status_code
        else:
            self.code = code

    def __str__(self):
        return str(self.detail)


class ValidationError(APIException):
    status_code = 400
    default_detail = "Invalid input."

    def __init__(self, detail=None, code=None):
        if detail is None:
            self.detail = self.default_detail
        else:
            self.detail = detail
        if code is None:
            self.code = self.status_code
        else:
            self.code = code
