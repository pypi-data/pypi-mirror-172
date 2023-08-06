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



class Otp(ModelNormal):


    allowed_values = {
        ('pin_type',): {
            'LETTERS': "letters",
            'NUMBERS': "numbers",
            'ALPHANUMERIC': "alphanumeric",
        },
    }

    validations = {
        ('_from',): {
            'max_length': 15,
            'min_length': 3,
        },
        ('pin_length',): {
            'inclusive_maximum': 10,
            'inclusive_minimum': 4,
        },
        ('ttl',): {
            'inclusive_maximum': 1800,
            'inclusive_minimum': 60,
        },
        ('max_attempts',): {
            'inclusive_maximum': 10,
            'inclusive_minimum': 1,
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
            'template': (str,),  # noqa: E501
            '_from': (str,),  # noqa: E501
            'pin_type': (str,),  # noqa: E501
            'pin_length': (int,),  # noqa: E501
            'ttl': (int,),  # noqa: E501
            'max_attempts': (int,),  # noqa: E501
            'otp_callback': (str, none_type,),  # noqa: E501
        }

    @cached_property
    def discriminator():
        return None


    attribute_map = {
        'template': 'template',  # noqa: E501
        '_from': 'from',  # noqa: E501
        'pin_type': 'pinType',  # noqa: E501
        'pin_length': 'pinLength',  # noqa: E501
        'ttl': 'ttl',  # noqa: E501
        'max_attempts': 'maxAttempts',  # noqa: E501
        'otp_callback': 'otpCallback',  # noqa: E501
    }

    read_only_vars = {
    }

    _composed_schemas = {}

    @classmethod
    @convert_js_args_to_python_args
    def _from_api_data(cls, template, _from, pin_type, pin_length, ttl, max_attempts, otp_callback, *args, **kwargs):  # noqa: E501
        """Otp - a model

        Args:
            template (str):
            _from (str):
            pin_type (str):
            pin_length (int):
            ttl (int):
            max_attempts (int):
            otp_callback (str, none_type):


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

        self.template = template
        self._from = _from
        self.pin_type = pin_type
        self.pin_length = pin_length
        self.ttl = ttl
        self.max_attempts = max_attempts
        self.otp_callback = otp_callback
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
    def __init__(self, template, _from, pin_type, pin_length, ttl, max_attempts, otp_callback, *args, **kwargs):  # noqa: E501
        """Otp - a model

        Args:
            template (str):
            _from (str):
            pin_type (str):
            pin_length (int):
            ttl (int):
            max_attempts (int):
            otp_callback (str, none_type):


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

        self.template = template
        self._from = _from
        self.pin_type = pin_type
        self.pin_length = pin_length
        self.ttl = ttl
        self.max_attempts = max_attempts
        self.otp_callback = otp_callback
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
