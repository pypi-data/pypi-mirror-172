from requests import Response
import functools

from bitronit.exceptions import AuthenticationError

def authentication_required(func):
    @functools.wraps(func)
    def wrapper_decorator(*args, **kwargs):
        if not args[0]._authenticated:
            raise AuthenticationError(response=Response())
        value = func(*args, **kwargs)
        return value

    return wrapper_decorator