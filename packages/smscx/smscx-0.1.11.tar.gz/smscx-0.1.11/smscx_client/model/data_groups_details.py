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
    from smscx_client.model.custom_fields_obj import CustomFieldsObj
    globals()['CustomFieldsObj'] = CustomFieldsObj


class DataGroupsDetails(ModelNormal):


    allowed_values = {
    }

    validations = {
        ('id',): {
            'max_length': 36,
            'min_length': 36,
            'regex': {
                'pattern': r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$',  # noqa: E501
            },
        },
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
            'id': (str,),  # noqa: E501
            'phone_number': (str,),  # noqa: E501
            'country_iso': (str,),  # noqa: E501
            'first_name': (str, none_type,),  # noqa: E501
            'last_name': (str, none_type,),  # noqa: E501
            'email': (str, none_type,),  # noqa: E501
            'field1': (str, none_type,),  # noqa: E501
            'field2': (str, none_type,),  # noqa: E501
            'field3': (str, none_type,),  # noqa: E501
            'field4': (str, none_type,),  # noqa: E501
            'field5': (str, none_type,),  # noqa: E501
            'group_id': (int,),  # noqa: E501
            'optout': (bool,),  # noqa: E501
            'date_added': (str,),  # noqa: E501
            'custom_fields': (CustomFieldsObj,),  # noqa: E501
        }

    @cached_property
    def discriminator():
        return None


    attribute_map = {
        'id': 'id',  # noqa: E501
        'phone_number': 'phoneNumber',  # noqa: E501
        'country_iso': 'countryIso',  # noqa: E501
        'first_name': 'firstName',  # noqa: E501
        'last_name': 'lastName',  # noqa: E501
        'email': 'email',  # noqa: E501
        'field1': 'field1',  # noqa: E501
        'field2': 'field2',  # noqa: E501
        'field3': 'field3',  # noqa: E501
        'field4': 'field4',  # noqa: E501
        'field5': 'field5',  # noqa: E501
        'group_id': 'groupId',  # noqa: E501
        'optout': 'optout',  # noqa: E501
        'date_added': 'dateAdded',  # noqa: E501
        'custom_fields': 'customFields',  # noqa: E501
    }

    read_only_vars = {
    }

    _composed_schemas = {}

    @classmethod
    @convert_js_args_to_python_args
    def _from_api_data(cls, id, phone_number, country_iso, first_name, last_name, email, field1, field2, field3, field4, field5, group_id, optout, date_added, *args, **kwargs):  # noqa: E501
        """DataGroupsDetails - a model

        Args:
            id (str):
            phone_number (str):
            country_iso (str):
            first_name (str, none_type):
            last_name (str, none_type):
            email (str, none_type):
            field1 (str, none_type):
            field2 (str, none_type):
            field3 (str, none_type):
            field4 (str, none_type):
            field5 (str, none_type):
            group_id (int):
            optout (bool):
            date_added (str):


            custom_fields (CustomFieldsObj): [optional]  # noqa: E501
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

        self.id = id
        self.phone_number = phone_number
        self.country_iso = country_iso
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.field1 = field1
        self.field2 = field2
        self.field3 = field3
        self.field4 = field4
        self.field5 = field5
        self.group_id = group_id
        self.optout = optout
        self.date_added = date_added
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
    def __init__(self, id, phone_number, country_iso, first_name, last_name, email, field1, field2, field3, field4, field5, group_id, optout, date_added, *args, **kwargs):  # noqa: E501
        """DataGroupsDetails - a model

        Args:
            id (str):
            phone_number (str):
            country_iso (str):
            first_name (str, none_type):
            last_name (str, none_type):
            email (str, none_type):
            field1 (str, none_type):
            field2 (str, none_type):
            field3 (str, none_type):
            field4 (str, none_type):
            field5 (str, none_type):
            group_id (int):
            optout (bool):
            date_added (str):


            custom_fields (CustomFieldsObj): [optional]  # noqa: E501
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

        self.id = id
        self.phone_number = phone_number
        self.country_iso = country_iso
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.field1 = field1
        self.field2 = field2
        self.field3 = field3
        self.field4 = field4
        self.field5 = field5
        self.group_id = group_id
        self.optout = optout
        self.date_added = date_added
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
