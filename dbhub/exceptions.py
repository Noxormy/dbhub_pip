import requests


class ServiceException(Exception):
    def __init__(self, msg):
        self.msg = msg


class CredentialsException(ServiceException):
    pass


class WrongDataException(ServiceException):
    pass


class NotFoundException(ServiceException):
    pass


class UnknownException(ServiceException):
    pass


def is_res_ok(response):
    return response.status_code == requests.codes.ok


def get_error(response):
    msg = response.text

    return {
        400: WrongDataException(msg),
        401: CredentialsException(msg),
        404: NotFoundException(msg)

    }.get(response.status_code, UnknownException(msg))
