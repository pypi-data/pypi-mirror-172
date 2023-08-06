class ApiExceptionBase(Exception):
    """The base exception class for all ApiExceptionBases"""


class ApiTypeError(ApiExceptionBase, TypeError):
    def __init__(self, msg, path_to_item=None, valid_classes=None,
                 key_type=None):
        """ Raises an exception for TypeErrors

        Args:
            msg (str): the exception message

        Keyword Args:
            path_to_item (list): a list of keys an indices to get to the
                                 current_item
                                 None if unset
            valid_classes (tuple): the primitive classes that current item
                                   should be an instance of
                                   None if unset
            key_type (bool): False if our value is a value in a dict
                             True if it is a key in a dict
                             False if our item is an item in a list
                             None if unset
        """
        self.path_to_item = path_to_item
        self.valid_classes = valid_classes
        self.key_type = key_type
        full_msg = msg
        if path_to_item:
            full_msg = "{0} at {1}".format(msg, render_path(path_to_item))
        super(ApiTypeError, self).__init__(full_msg)


class ApiValueError(ApiExceptionBase, ValueError):
    def __init__(self, msg, path_to_item=None):
        """
        Args:
            msg (str): the exception message

        Keyword Args:
            path_to_item (list) the path to the exception in the
                received_data dict. None if unset
        """

        self.path_to_item = path_to_item
        full_msg = msg
        if path_to_item:
            full_msg = "{0} at {1}".format(msg, render_path(path_to_item))
        super(ApiValueError, self).__init__(full_msg)


class ApiAttributeError(ApiExceptionBase, AttributeError):
    def __init__(self, msg, path_to_item=None):
        """
        Raised when an attribute reference or assignment fails.

        Args:
            msg (str): the exception message

        Keyword Args:
            path_to_item (None/list) the path to the exception in the
                received_data dict
        """
        self.path_to_item = path_to_item
        full_msg = msg
        if path_to_item:
            full_msg = "{0} at {1}".format(msg, render_path(path_to_item))
        super(ApiAttributeError, self).__init__(full_msg)


class ApiKeyError(ApiExceptionBase, KeyError):
    def __init__(self, msg, path_to_item=None):
        """
        Args:
            msg (str): the exception message

        Keyword Args:
            path_to_item (None/list) the path to the exception in the
                received_data dict
        """
        self.path_to_item = path_to_item
        full_msg = msg
        if path_to_item:
            full_msg = "{0} at {1}".format(msg, render_path(path_to_item))
        super(ApiKeyError, self).__init__(full_msg)


class ApiException(ApiExceptionBase):

    def __init__(self, status=None, reason=None, http_resp=None):
        if http_resp:
            self.status = http_resp.status
            self.reason = http_resp.reason
            self.body = http_resp.data
            self.headers = http_resp.getheaders()
        else:
            self.status = status
            self.reason = reason
            self.body = None
            self.headers = None

    def __str__(self):
        """Custom error messages for exception"""
        error_message = "Status Code: {0}\n"\
                        "Reason: {1}\n".format(self.status, self.reason)
        if self.headers:
            error_message += "HTTP response headers: {0}\n".format(
                self.headers)

        if self.body:
            error_message += "HTTP response body: {0}\n".format(self.body)

        return error_message


class ResourceNotFoundException(ApiException):

    def __init__(self, status=None, reason=None, http_resp=None):
        super(ResourceNotFoundException, self).__init__(status, reason, http_resp)


class InvalidCredentialsException(ApiException):

    def __init__(self, status=None, reason=None, http_resp=None):
        super(InvalidCredentialsException, self).__init__(status, reason, http_resp)


class AccessDeniedException(ApiException):

    def __init__(self, status=None, reason=None, http_resp=None):
        super(AccessDeniedException, self).__init__(status, reason, http_resp)


class ServerErrorException(ApiException):

    def __init__(self, status=None, reason=None, http_resp=None):
        super(ServerErrorException, self).__init__(status, reason, http_resp)


class InsufficientBalanceException(ApiException):

    def __init__(self, status=None, reason=None, http_resp=None):
        super(InsufficientBalanceException, self).__init__(status, reason, http_resp)


class DuplicateIdException(ApiException):

    def __init__(self, status=None, reason=None, http_resp=None):
        super(DuplicateIdException, self).__init__(status, reason, http_resp)


class DuplicateValueException(ApiException):

    def __init__(self, status=None, reason=None, http_resp=None):
        super(DuplicateValueException, self).__init__(status, reason, http_resp)


class OtpAlreadyVerifiedException(ApiException):

    def __init__(self, status=None, reason=None, http_resp=None):
        super(OtpAlreadyVerifiedException, self).__init__(status, reason, http_resp)


class OtpCancelledException(ApiException):

    def __init__(self, status=None, reason=None, http_resp=None):
        super(OtpCancelledException, self).__init__(status, reason, http_resp)


class OtpExpiredException(ApiException):

    def __init__(self, status=None, reason=None, http_resp=None):
        super(OtpExpiredException, self).__init__(status, reason, http_resp)


class OtpFailedException(ApiException):

    def __init__(self, status=None, reason=None, http_resp=None):
        super(OtpFailedException, self).__init__(status, reason, http_resp)


class InvalidPinException(ApiException):

    def __init__(self, status=None, reason=None, http_resp=None):
        super(InvalidPinException, self).__init__(status, reason, http_resp)


class InvalidPhoneNumberException(ApiException):

    def __init__(self, status=None, reason=None, http_resp=None):
        super(InvalidPhoneNumberException, self).__init__(status, reason, http_resp)


class InvalidScopeException(ApiException):

    def __init__(self, status=None, reason=None, http_resp=None):
        super(InvalidScopeException, self).__init__(status, reason, http_resp)


class InvalidPhoneNumberException(ApiException):

    def __init__(self, status=None, reason=None, http_resp=None):
        super(InvalidPhoneNumberException, self).__init__(status, reason, http_resp)


class InvalidRequestException(ApiException):

    def __init__(self, status=None, reason=None, http_resp=None):
        super(InvalidRequestException, self).__init__(status, reason, http_resp)


class InsufficientScopeException(ApiException):

    def __init__(self, status=None, reason=None, http_resp=None):
        super(InsufficientScopeException, self).__init__(status, reason, http_resp)


class NoCoverageException(ApiException):

    def __init__(self, status=None, reason=None, http_resp=None):
        super(NoCoverageException, self).__init__(status, reason, http_resp)


class TemplateNotApprovedException(ApiException):

    def __init__(self, status=None, reason=None, http_resp=None):
        super(TemplateNotApprovedException, self).__init__(status, reason, http_resp)


class ChannelNotActiveException(ApiException):

    def __init__(self, status=None, reason=None, http_resp=None):
        super(ChannelNotActiveException, self).__init__(status, reason, http_resp)


class OtpCancelledException(ApiException):

    def __init__(self, status=None, reason=None, http_resp=None):
        super(OtpCancelledException, self).__init__(status, reason, http_resp)


class OtpActionNotAllowedException(ApiException):

    def __init__(self, status=None, reason=None, http_resp=None):
        super(OtpActionNotAllowedException, self).__init__(status, reason, http_resp)


class ApiMethodNotAllowedException(ApiException):

    def __init__(self, status=None, reason=None, http_resp=None):
        super(ApiMethodNotAllowedException, self).__init__(status, reason, http_resp)


class RateLimitExcedeedException(ApiException):

    def __init__(self, status=None, reason=None, http_resp=None):
        super(RateLimitExcedeedException, self).__init__(status, reason, http_resp)

def render_path(path_to_item):
    """Returns a string representation of a path"""
    result = ""
    for pth in path_to_item:
        if isinstance(pth, int):
            result += "[{0}]".format(pth)
        else:
            result += "['{0}']".format(pth)
    return result
