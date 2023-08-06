from requests import Response

class ClientError(Exception):
    def __init__(self, response):
        self.response = response
        self.errors = {
            400: InvalidRequestError,
            401: AuthenticationError,
            404: NotFoundError,
            422: UnprocessableRequestError
        }

        try:
            exception_class = self.errors[response.status_code]
            self.error = exception_class(response)
        except KeyError:
            self.error = UnknownError(response)

class AuthenticationError(Exception):
    def __init__(self, response: Response):

        if response.content:
            server_response_message = response.json()["message"]
            self.error_msg = "Server Response: {}\n".format(server_response_message)
        else:
            self.error_msg = "Client authorization is failed. "
            self.error_msg += "Please authenticate the client with correct api key and secret"

        super().__init__(self.error_msg)

    def __str__(self):
        return "Authentication Failed. Error Message: {}".format(self.error_msg)

class UnprocessableRequestError(Exception):
    def __init__(self, response):
        super().__init__(
            "Request could not be processed.\n{}".format(response.content)
        )

class NotFoundError(Exception):
    def __init__(self, response):
        self.response = response
        self.error_msg = response.json()["message"]

    def __str__(self):
        return "Error Message: {}".format(self.error_msg)

class InvalidRequestError(Exception):
    def __init__(self, response):
        self.response = response
        self.error_msg = response.json()["message"]

    def __str__(self):
        return "Invalid Request Parameter or Body. Error Message: {}".format(self.error_msg)

class UnknownError(Exception):
    def __init__(self, response):
        super().__init__("Unknown Response Code: {}".format(response.status_code))