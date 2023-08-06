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



class DataDlrUpdate(ModelNormal):


    allowed_values = {
        ('status',): {
            'ACCEPTED': "ACCEPTED",
            'SENT': "SENT",
            'DELIVERED': "DELIVERED",
            'FAILED': "FAILED",
            'SCHEDULED': "SCHEDULED",
            'REJECTED': "REJECTED",
            'NO_COVERAGE': "NO COVERAGE",
        },
    }

    validations = {
        ('campaign_id',): {
            'max_length': 36,
            'min_length': 36,
            'regex': {
                'pattern': r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$',  # noqa: E501
            },
        },
        ('msg_id',): {
            'max_length': 36,
            'min_length': 36,
            'regex': {
                'pattern': r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$',  # noqa: E501
            },
        },
        ('track_data',): {
            'max_length': 36,
            'min_length': 36,
            'regex': {
                'pattern': r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$',  # noqa: E501
            },
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
            'campaign_id': (str,),  # noqa: E501
            'msg_id': (str,),  # noqa: E501
            'status_code': (int,),  # noqa: E501
            'status': (str,),  # noqa: E501
            'error_code': (int, none_type,),  # noqa: E501
            'datetime': (str,),  # noqa: E501
            'track_data': (str, none_type,),  # noqa: E501
        }

    @cached_property
    def discriminator():
        return None


    attribute_map = {
        'campaign_id': 'campaignId',  # noqa: E501
        'msg_id': 'msgId',  # noqa: E501
        'status_code': 'statusCode',  # noqa: E501
        'status': 'status',  # noqa: E501
        'error_code': 'errorCode',  # noqa: E501
        'datetime': 'datetime',  # noqa: E501
        'track_data': 'trackData',  # noqa: E501
    }

    read_only_vars = {
    }

    _composed_schemas = {}

    @classmethod
    @convert_js_args_to_python_args
    def _from_api_data(cls, campaign_id, msg_id, status_code, status, error_code, datetime, *args, **kwargs):  # noqa: E501
        """DataDlrUpdate - a model

        Args:
            campaign_id (str): Identifier of the sent campaign
            msg_id (str): Identifier of the sent message
            status_code (int): Numeric value of the delivery report
            status (str): Delivery report of the sent SMS
            error_code (int, none_type): A code that give detailed information about a failed delivery. See the [list of error codes](#error-codes) for more details. A non-null value indicates that the message could not be delivered.
            datetime (str):


            track_data (str, none_type): Identifier of the message ID provided by client for tracking purposes. [optional]  # noqa: E501
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

        self.campaign_id = campaign_id
        self.msg_id = msg_id
        self.status_code = status_code
        self.status = status
        self.error_code = error_code
        self.datetime = datetime
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
    def __init__(self, campaign_id, msg_id, status_code, status, error_code, datetime, *args, **kwargs):  # noqa: E501
        """DataDlrUpdate - a model

        Args:
            campaign_id (str): Identifier of the sent campaign
            msg_id (str): Identifier of the sent message
            status_code (int): Numeric value of the delivery report
            status (str): Delivery report of the sent SMS
            error_code (int, none_type): A code that give detailed information about a failed delivery. See the [list of error codes](#error-codes) for more details. A non-null value indicates that the message could not be delivered.
            datetime (str):


            track_data (str, none_type): Identifier of the message ID provided by client for tracking purposes. [optional]  # noqa: E501
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

        self.campaign_id = campaign_id
        self.msg_id = msg_id
        self.status_code = status_code
        self.status = status
        self.error_code = error_code
        self.datetime = datetime
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
