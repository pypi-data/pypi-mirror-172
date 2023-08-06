import re  # noqa: F401
import sys  # noqa: F401

from smscx_client.model_utils import (  # noqa: F401
    ApiTypeError,
    ModelComposed,
    ModelNormal,
    ModelSimple,
    cached_property,
    change_keys_js_to_python,
    convert_js_args_to_python_args,
    date,
    datetime,
    file_type,
    none_type,
    validate_get_composed_info,
    ApiModel
)
from smscx_client.exceptions import ApiAttributeError



class NewOtpRequest(ModelNormal):


    allowed_values = {
        ('pin_type',): {
            'LETTERS': "letters",
            'NUMBERS': "numbers",
            'ALPHANUMERIC': "alphanumeric",
        },
    }

    validations = {
        ('country_iso',): {
            'max_length': 2,
            'min_length': 2,
        },
        ('_from',): {
            'max_length': 15,
            'min_length': 3,
        },
        ('track_id',): {
            'max_length': 36,
            'min_length': 36,
            'regex': {
                'pattern': r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$',  # noqa: E501
            },
        },
        ('ttl',): {
            'inclusive_maximum': 1800,
            'inclusive_minimum': 60,
        },
        ('max_attempts',): {
            'inclusive_maximum': 10,
            'inclusive_minimum': 1,
        },
        ('pin_length',): {
            'inclusive_maximum': 10,
            'inclusive_minimum': 4,
        },
    }

    @cached_property
    def additional_properties_type():
        return (bool, date, datetime, dict, float, int, list, str, none_type,)  # noqa: E501

    _nullable = False

    @cached_property
    def api_types():
        """
        Returns
            api_types (dict): The key is attribute name
                and the value is attribute type.
        """
        return {
            'phone_number': (str,),  # noqa: E501
            'country_iso': (str,),  # noqa: E501
            '_from': (str,),  # noqa: E501
            'template': (str,),  # noqa: E501
            'track_id': (str,),  # noqa: E501
            'ttl': (int,),  # noqa: E501
            'max_attempts': (int,),  # noqa: E501
            'pin_type': (str,),  # noqa: E501
            'pin_length': (int,),  # noqa: E501
            'otp_callback_url': (str,),  # noqa: E501
        }

    @cached_property
    def discriminator():
        return None


    attribute_map = {
        'phone_number': 'phoneNumber',  # noqa: E501
        'country_iso': 'countryIso',  # noqa: E501
        '_from': 'from',  # noqa: E501
        'template': 'template',  # noqa: E501
        'track_id': 'trackId',  # noqa: E501
        'ttl': 'ttl',  # noqa: E501
        'max_attempts': 'maxAttempts',  # noqa: E501
        'pin_type': 'pinType',  # noqa: E501
        'pin_length': 'pinLength',  # noqa: E501
        'otp_callback_url': 'otpCallbackUrl',  # noqa: E501
    }

    read_only_vars = {
    }

    _composed_schemas = {}

    @classmethod
    @convert_js_args_to_python_args
    def _from_api_data(cls, phone_number, *args, **kwargs):  # noqa: E501
        """NewOtpRequest - a model

        Args:
            phone_number (str): Phone number in international E.164 format or national format. If national format is provided, for better validation you must use the parameter `countryIso` to provide the country code of the destination phone number    


            country_iso (str): Country ISO (two-letter) of the destination phone numbers (if provided in national format). Please note that if an international E.164 phone number format is provided in the `to` parameter, the **countryIso** will be ignored. Eg. **FR** for France, **GB** for United Kingdom. Note: It is \"GB\", not \"UK\", as per the ISO-3166 alpha 2. [optional]  # noqa: E501
            _from (str): The originator (sender name) of the text message (min 3, max 11 characters). If the originator used in this value is not approved, it will be overwritten by a default system originator (eg. InfoText). Read more about [sender names](#) Note: This parameter is optional and can be used only if you want to overwrite the OTP settings of your SMS API application. [optional]  # noqa: E501
            template (str): The text message that will be delivered to the mobile number. It must contain the placeholder `{{pin}}`.    Note: This parameter is optional and can be used only if you want to overwrite the OTP settings of your SMS API application. [General placeholders](#) can be used in the text template.. [optional]  # noqa: E501
            track_id (str): Client provided UUID (v1-v5) for tracking purposes. [optional]  # noqa: E501
            ttl (int): The time to live (ttl) defines the time in seconds that a pin is valid. Min 1 minute (60 seconds) and max 30 minutes (1800 seconds)   Note: If this parameter is set, it will overwrite the setting from [Admin Dashboard > HTTP API > Oauth2 > Application settings](#). [optional]  # noqa: E501
            max_attempts (int): Number of attempts to allow the OTP to be verified before marking it as failed  Note: If this parameter is set, it will overwrite the setting from [Admin Dashboard > HTTP API > Oauth2 > Application settings](#). [optional]  # noqa: E501
            pin_type (str): Type of pin that will be generated for each mobile phone and will replace the placeholder {{pin}  Note: If this parameter is set, it will overwrite the setting from [Admin Dashboard > HTTP API > Oauth2 > Application settings](#). [optional]  # noqa: E501
            pin_length (int): Character length of the pin   Note: If this parameter is set, it will overwrite the setting from [Admin Dashboard > HTTP API > Oauth2 > Application settings](#). [optional]  # noqa: E501
            otp_callback_url (str): A valid URL to receive status updates for the OTP verification.   Note: If this parameter is set, it will overwrite the setting from [Admin Dashboard > HTTP API > Oauth2 > Application settings](#). [optional]  # noqa: E501
        """

        _check_type = kwargs.pop('_check_type', True)
        _spec_property_naming = kwargs.pop('_spec_property_naming', True)
        _path_to_item = kwargs.pop('_path_to_item', ())
        _configuration = kwargs.pop('_configuration', None)
        _visited_composed_classes = kwargs.pop('_visited_composed_classes', ())

        self = super(ApiModel, cls).__new__(cls)

        if args:
            for arg in args:
                if isinstance(arg, dict):
                    kwargs.update(arg)
                else:
                    raise ApiTypeError(
                        "Invalid positional arguments=%s passed to %s. Remove those invalid positional arguments." % (
                            args,
                            self.__class__.__name__,
                        ),
                        path_to_item=_path_to_item,
                        valid_classes=(self.__class__,),
                    )

        self._data_store = {}
        self._check_type = _check_type
        self._spec_property_naming = _spec_property_naming
        self._path_to_item = _path_to_item
        self._configuration = _configuration
        self._visited_composed_classes = _visited_composed_classes + (self.__class__,)

        self.phone_number = phone_number
        for var_name, var_value in kwargs.items():
            if var_name not in self.attribute_map and \
                        self._configuration is not None and \
                        self._configuration.discard_unknown_keys and \
                        self.additional_properties_type is None:
                # discard variable.
                continue
            setattr(self, var_name, var_value)
        return self

    required_properties = set([
        '_data_store',
        '_check_type',
        '_spec_property_naming',
        '_path_to_item',
        '_configuration',
        '_visited_composed_classes',
    ])

    @convert_js_args_to_python_args
    def __init__(self, phone_number, *args, **kwargs):  # noqa: E501
        """NewOtpRequest - a model

        Args:
            phone_number (str): Phone number in international E.164 format or national format. If national format is provided, for better validation you must use the parameter `countryIso` to provide the country code of the destination phone number    


            country_iso (str): Country ISO (two-letter) of the destination phone numbers (if provided in national format). Please note that if an international E.164 phone number format is provided in the `to` parameter, the **countryIso** will be ignored. Eg. **FR** for France, **GB** for United Kingdom. Note: It is \"GB\", not \"UK\", as per the ISO-3166 alpha 2. [optional]  # noqa: E501
            _from (str): The originator (sender name) of the text message (min 3, max 11 characters). If the originator used in this value is not approved, it will be overwritten by a default system originator (eg. InfoText). Read more about [sender names](#) Note: This parameter is optional and can be used only if you want to overwrite the OTP settings of your SMS API application. [optional]  # noqa: E501
            template (str): The text message that will be delivered to the mobile number. It must contain the placeholder `{{pin}}`.    Note: This parameter is optional and can be used only if you want to overwrite the OTP settings of your SMS API application. [General placeholders](#) can be used in the text template.. [optional]  # noqa: E501
            track_id (str): Client provided UUID (v1-v5) for tracking purposes. [optional]  # noqa: E501
            ttl (int): The time to live (ttl) defines the time in seconds that a pin is valid. Min 1 minute (60 seconds) and max 30 minutes (1800 seconds)   Note: If this parameter is set, it will overwrite the setting from [Admin Dashboard > HTTP API > Oauth2 > Application settings](#). [optional]  # noqa: E501
            max_attempts (int): Number of attempts to allow the OTP to be verified before marking it as failed  Note: If this parameter is set, it will overwrite the setting from [Admin Dashboard > HTTP API > Oauth2 > Application settings](#). [optional]  # noqa: E501
            pin_type (str): Type of pin that will be generated for each mobile phone and will replace the placeholder {{pin}  Note: If this parameter is set, it will overwrite the setting from [Admin Dashboard > HTTP API > Oauth2 > Application settings](#). [optional]  # noqa: E501
            pin_length (int): Character length of the pin   Note: If this parameter is set, it will overwrite the setting from [Admin Dashboard > HTTP API > Oauth2 > Application settings](#). [optional]  # noqa: E501
            otp_callback_url (str): A valid URL to receive status updates for the OTP verification.   Note: If this parameter is set, it will overwrite the setting from [Admin Dashboard > HTTP API > Oauth2 > Application settings](#). [optional]  # noqa: E501
        """

        _check_type = kwargs.pop('_check_type', True)
        _spec_property_naming = kwargs.pop('_spec_property_naming', False)
        _path_to_item = kwargs.pop('_path_to_item', ())
        _configuration = kwargs.pop('_configuration', None)
        _visited_composed_classes = kwargs.pop('_visited_composed_classes', ())

        if args:
            for arg in args:
                if isinstance(arg, dict):
                    kwargs.update(arg)
                else:
                    raise ApiTypeError(
                        "Invalid positional arguments=%s passed to %s. Remove those invalid positional arguments." % (
                            args,
                            self.__class__.__name__,
                        ),
                        path_to_item=_path_to_item,
                        valid_classes=(self.__class__,),
                    )

        self._data_store = {}
        self._check_type = _check_type
        self._spec_property_naming = _spec_property_naming
        self._path_to_item = _path_to_item
        self._configuration = _configuration
        self._visited_composed_classes = _visited_composed_classes + (self.__class__,)

        self.phone_number = phone_number
        for var_name, var_value in kwargs.items():
            if var_name not in self.attribute_map and \
                        self._configuration is not None and \
                        self._configuration.discard_unknown_keys and \
                        self.additional_properties_type is None:
                # discard variable.
                continue
            setattr(self, var_name, var_value)
            if var_name in self.read_only_vars:
                raise ApiAttributeError(f"`{var_name}` is a read-only attribute. Use `from_api_data` to instantiate "
                                     f"class with read only attributes.")
