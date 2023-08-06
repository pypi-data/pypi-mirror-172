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


def lazy_import():
    from smscx_client.model.quiet_hours import QuietHours
    from smscx_client.model.transliteration_app_settings import TransliterationAppSettings
    globals()['QuietHours'] = QuietHours
    globals()['TransliterationAppSettings'] = TransliterationAppSettings


class Sms(ModelNormal):

    allowed_values = {
    }

    validations = {
    }

    additional_properties_type = None

    _nullable = False

    @cached_property
    def api_types():
        """
        Returns
            api_types (dict): The key is attribute name
                and the value is attribute type.
        """
        lazy_import()
        return {
            'enforce_originator': (str, none_type,),  # noqa: E501
            'dlr_callback': (str, none_type,),  # noqa: E501
            'receive_callback': (str, none_type,),  # noqa: E501
            'quiet_hours': (QuietHours,),  # noqa: E501
            'transliteration': (TransliterationAppSettings,),  # noqa: E501
        }

    @cached_property
    def discriminator():
        return None


    attribute_map = {
        'enforce_originator': 'enforceOriginator',  # noqa: E501
        'dlr_callback': 'dlrCallback',  # noqa: E501
        'receive_callback': 'receiveCallback',  # noqa: E501
        'quiet_hours': 'quietHours',  # noqa: E501
        'transliteration': 'transliteration',  # noqa: E501
    }

    read_only_vars = {
    }

    _composed_schemas = {}

    @classmethod
    @convert_js_args_to_python_args
    def _from_api_data(cls, enforce_originator, dlr_callback, receive_callback, quiet_hours, transliteration, *args, **kwargs):  # noqa: E501
        """Sms - a model

        Args:
            enforce_originator (str, none_type):
            dlr_callback (str, none_type):
            receive_callback (str, none_type):
            quiet_hours (QuietHours):
            transliteration (TransliterationAppSettings):

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

        self.enforce_originator = enforce_originator
        self.dlr_callback = dlr_callback
        self.receive_callback = receive_callback
        self.quiet_hours = quiet_hours
        self.transliteration = transliteration
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
    def __init__(self, enforce_originator, dlr_callback, receive_callback, quiet_hours, transliteration, *args, **kwargs):  # noqa: E501
        """Sms - a model

        Args:
            enforce_originator (str, none_type):
            dlr_callback (str, none_type):
            receive_callback (str, none_type):
            quiet_hours (QuietHours):
            transliteration (TransliterationAppSettings):

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

        self.enforce_originator = enforce_originator
        self.dlr_callback = dlr_callback
        self.receive_callback = receive_callback
        self.quiet_hours = quiet_hours
        self.transliteration = transliteration
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
