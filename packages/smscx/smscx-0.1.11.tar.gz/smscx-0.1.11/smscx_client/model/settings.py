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
    from smscx_client.model.attachments import Attachments
    from smscx_client.model.lookup import Lookup
    from smscx_client.model.multichannel import Multichannel
    from smscx_client.model.optouts import Optouts
    from smscx_client.model.otp import Otp
    from smscx_client.model.shortlinks import Shortlinks
    from smscx_client.model.sms import Sms
    from smscx_client.model.viber import Viber
    from smscx_client.model.whatsapp import Whatsapp
    globals()['Attachments'] = Attachments
    globals()['Lookup'] = Lookup
    globals()['Multichannel'] = Multichannel
    globals()['Optouts'] = Optouts
    globals()['Otp'] = Otp
    globals()['Shortlinks'] = Shortlinks
    globals()['Sms'] = Sms
    globals()['Viber'] = Viber
    globals()['Whatsapp'] = Whatsapp


class Settings(ModelNormal):


    allowed_values = {
    }

    validations = {
    }

    @cached_property
    def additional_properties_type():
        lazy_import()
        return (bool, date, datetime, dict, float, int, list, str, none_type,)  # noqa: E501

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
            'sms': (Sms,),  # noqa: E501
            'viber': (Viber,),  # noqa: E501
            'whatsapp': (Whatsapp,),  # noqa: E501
            'multichannel': (Multichannel,),  # noqa: E501
            'shortlinks': (Shortlinks,),  # noqa: E501
            'attachments': (Attachments,),  # noqa: E501
            'optouts': (Optouts,),  # noqa: E501
            'lookup': (Lookup,),  # noqa: E501
            'otp': (Otp,),  # noqa: E501
        }

    @cached_property
    def discriminator():
        return None


    attribute_map = {
        'sms': 'sms',  # noqa: E501
        'viber': 'viber',  # noqa: E501
        'whatsapp': 'whatsapp',  # noqa: E501
        'multichannel': 'multichannel',  # noqa: E501
        'shortlinks': 'shortlinks',  # noqa: E501
        'attachments': 'attachments',  # noqa: E501
        'optouts': 'optouts',  # noqa: E501
        'lookup': 'lookup',  # noqa: E501
        'otp': 'otp',  # noqa: E501
    }

    read_only_vars = {
    }

    _composed_schemas = {}

    @classmethod
    @convert_js_args_to_python_args
    def _from_api_data(cls, sms, viber, whatsapp, multichannel, shortlinks, attachments, optouts, lookup, otp, *args, **kwargs):  # noqa: E501
        """Settings - a model

        Args:
            sms (Sms):
            viber (Viber):
            whatsapp (Whatsapp):
            multichannel (Multichannel):
            shortlinks (Shortlinks):
            attachments (Attachments):
            optouts (Optouts):
            lookup (Lookup):
            otp (Otp):


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

        self.sms = sms
        self.viber = viber
        self.whatsapp = whatsapp
        self.multichannel = multichannel
        self.shortlinks = shortlinks
        self.attachments = attachments
        self.optouts = optouts
        self.lookup = lookup
        self.otp = otp
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
    def __init__(self, sms, viber, whatsapp, multichannel, shortlinks, attachments, optouts, lookup, otp, *args, **kwargs):  # noqa: E501
        """Settings - a model

        Args:
            sms (Sms):
            viber (Viber):
            whatsapp (Whatsapp):
            multichannel (Multichannel):
            shortlinks (Shortlinks):
            attachments (Attachments):
            optouts (Optouts):
            lookup (Lookup):
            otp (Otp):


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

        self.sms = sms
        self.viber = viber
        self.whatsapp = whatsapp
        self.multichannel = multichannel
        self.shortlinks = shortlinks
        self.attachments = attachments
        self.optouts = optouts
        self.lookup = lookup
        self.otp = otp
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
