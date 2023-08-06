import re  # noqa: F401
import sys  # noqa: F401

from smscx_client.api_client import ApiClient, Endpoint as _Endpoint
from smscx_client.model_utils import (  # noqa: F401
    check_allowed_values,
    check_validations,
    date,
    datetime,
    file_type,
    none_type,
    validate_and_convert_types
)
from smscx_client.model.model400_invalid_param import Model400InvalidParam
from smscx_client.model.model401_unauthorized import Model401Unauthorized
from smscx_client.model.model403_insufficient_scope import Model403InsufficientScope
from smscx_client.model.model404_not_found import Model404NotFound
from smscx_client.model.model500_server_error import Model500ServerError
from smscx_client.model.originator_new_request import OriginatorNewRequest
from smscx_client.model.originator_new_response import OriginatorNewResponse
from smscx_client.model.originators_list_response import OriginatorsListResponse


class OriginatorsApi(object):
    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client
        self.create_originator_endpoint = _Endpoint(
            settings={
                'response_type': (OriginatorNewResponse,),
                'auth': [
                    'ApiKeyAuth',
                    'BearerAuth'
                ],
                'endpoint_path': '/originators',
                'operation_id': 'create_originator',
                'http_method': 'POST',
                'servers': None,
            },
            params_map={
                'all': [
                    'originator_new_request',
                ],
                'required': [
                    'originator_new_request',
                ],
                'nullable': [
                ],
                'enum': [
                ],
                'validation': [
                ]
            },
            root_map={
                'validations': {
                },
                'allowed_values': {
                },
                'api_types': {
                    'originator_new_request':
                        (OriginatorNewRequest,),
                },
                'attribute_map': {
                },
                'location_map': {
                    'originator_new_request': 'body',
                },
                'collection_format_map': {
                }
            },
            headers_map={
                'accept': [
                    'application/json'
                ],
                'content_type': [
                    'application/json'
                ]
            },
            api_client=api_client
        )
        self.delete_originator_endpoint = _Endpoint(
            settings={
                'response_type': (OriginatorNewResponse,),
                'auth': [
                    'ApiKeyAuth',
                    'BearerAuth'
                ],
                'endpoint_path': '/originators/{originatorId}',
                'operation_id': 'delete_originator',
                'http_method': 'DELETE',
                'servers': None,
            },
            params_map={
                'all': [
                    'originator_id',
                ],
                'required': [
                    'originator_id',
                ],
                'nullable': [
                ],
                'enum': [
                ],
                'validation': [
                ]
            },
            root_map={
                'validations': {
                },
                'allowed_values': {
                },
                'api_types': {
                    'originator_id':
                        (int,),
                },
                'attribute_map': {
                    'originator_id': 'originatorId',
                },
                'location_map': {
                    'originator_id': 'path',
                },
                'collection_format_map': {
                }
            },
            headers_map={
                'accept': [
                    'application/json'
                ],
                'content_type': [],
            },
            api_client=api_client
        )
        self.get_originators_list_endpoint = _Endpoint(
            settings={
                'response_type': (OriginatorsListResponse,),
                'auth': [
                    'ApiKeyAuth',
                    'BearerAuth'
                ],
                'endpoint_path': '/originators',
                'operation_id': 'get_originators_list',
                'http_method': 'GET',
                'servers': None,
            },
            params_map={
                'all': [
                ],
                'required': [],
                'nullable': [
                ],
                'enum': [
                ],
                'validation': [
                ]
            },
            root_map={
                'validations': {
                },
                'allowed_values': {
                },
                'api_types': {
                },
                'attribute_map': {
                },
                'location_map': {
                },
                'collection_format_map': {
                }
            },
            headers_map={
                'accept': [
                    'application/json'
                ],
                'content_type': [],
            },
            api_client=api_client
        )

    def create_originator(
        self,
        originator_new_request,
        **kwargs
    ):
        """Create new originator  # noqa: E501

        Creates and submits an originator for approval.    
### Errors for POST `/originators`  
| HTTP code  | Error code  | Type  | Description  |  
|:------------:|:------------:|:------------:| ------------ |  
|  400 | 1301  |  invalid_param  |  The originator is empty or parameter `originator` not set |  

|  400 | 1303  |  invalid_param  |  The parameter `originator` can contain only letters and numbers |  

|  400 | 1304  |  invalid_param  |  The alphanumeric originator provided is invalid (min 3, max 11 characters) |  

|  400 | 1305  |  invalid_param  |  The numeric originator provided is invalid (min 3, max 15 characters) |  

|  400 | 1306  |  duplicate_value  |  Originator already exists |  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.create_originator(originator_new_request, async_req=True)
        >>> result = thread.get()

        Args:
            originator_new_request (OriginatorNewRequest): 

        Keyword Args:
            _return_http_data_only (bool): response data without head status
                code and headers. Default is True.
            _preload_content (bool): if False, the urllib3.HTTPResponse object
                will be returned without reading/decoding response data.
                Default is True.
            _request_timeout (int/float/tuple): timeout setting for this request. If
                one number provided, it will be total request timeout. It can also
                be a pair (tuple) of (connection, read) timeouts.
                Default is None.
            _check_input_type (bool): specifies if type checking
                should be done one the data sent to the server.
                Default is True.
            _check_return_type (bool): specifies if type checking
                should be done one the data received from the server.
                Default is True.
            _spec_property_naming (bool): True if the variable names in the input data
                are serialized names.
                False if the variable names in the input data
                are pythonic names, e.g. snake case (default)
            _content_type (str/None): force body content-type.
                Default is None and content-type will be predicted by allowed
                content-types and body.
            _host_index (int/None): specifies the index of the server
                that we want to use.
                Default is read from the configuration.
            _request_auths (list): set to override the auth_settings for an a single
                request; this effectively ignores the authentication
                in the spec for a single request.
                Default is None
            async_req (bool): execute request asynchronously

        Returns:
            OriginatorNewResponse
                If the method is called asynchronously, returns the request
                thread.
        """
        kwargs['async_req'] = kwargs.get(
            'async_req', False
        )
        kwargs['_return_http_data_only'] = kwargs.get(
            '_return_http_data_only', True
        )
        kwargs['_preload_content'] = kwargs.get(
            '_preload_content', True
        )
        kwargs['_request_timeout'] = kwargs.get(
            '_request_timeout', None
        )
        kwargs['_check_input_type'] = kwargs.get(
            '_check_input_type', True
        )
        kwargs['_check_return_type'] = kwargs.get(
            '_check_return_type', True
        )
        kwargs['_spec_property_naming'] = kwargs.get(
            '_spec_property_naming', False
        )
        kwargs['_content_type'] = kwargs.get(
            '_content_type')
        kwargs['_host_index'] = kwargs.get('_host_index')
        kwargs['_request_auths'] = kwargs.get('_request_auths', None)
        kwargs['originator_new_request'] = \
            originator_new_request
        return self.create_originator_endpoint.call_with_http_info(**kwargs)

    def delete_originator(
        self,
        originator_id,
        **kwargs
    ):
        """Delete originator  # noqa: E501

        Deletes an originator if a valid identifier was provided.    
### Errors for DELETE `/originators/{originatorId}`  
| HTTP code  | Error code  | Type  | Description  |  
|:------------:|:------------:|:------------:| ------------ |  
|  404 | 1300  |  not_found  |  Originator ID not found  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.delete_originator(originator_id, async_req=True)
        >>> result = thread.get()

        Args:
            originator_id (int): Identifier of the originator

        Keyword Args:
            _return_http_data_only (bool): response data without head status
                code and headers. Default is True.
            _preload_content (bool): if False, the urllib3.HTTPResponse object
                will be returned without reading/decoding response data.
                Default is True.
            _request_timeout (int/float/tuple): timeout setting for this request. If
                one number provided, it will be total request timeout. It can also
                be a pair (tuple) of (connection, read) timeouts.
                Default is None.
            _check_input_type (bool): specifies if type checking
                should be done one the data sent to the server.
                Default is True.
            _check_return_type (bool): specifies if type checking
                should be done one the data received from the server.
                Default is True.
            _spec_property_naming (bool): True if the variable names in the input data
                are serialized names.
                False if the variable names in the input data
                are pythonic names, e.g. snake case (default)
            _content_type (str/None): force body content-type.
                Default is None and content-type will be predicted by allowed
                content-types and body.
            _host_index (int/None): specifies the index of the server
                that we want to use.
                Default is read from the configuration.
            _request_auths (list): set to override the auth_settings for an a single
                request; this effectively ignores the authentication
                in the spec for a single request.
                Default is None
            async_req (bool): execute request asynchronously

        Returns:
            OriginatorNewResponse
                If the method is called asynchronously, returns the request
                thread.
        """
        kwargs['async_req'] = kwargs.get(
            'async_req', False
        )
        kwargs['_return_http_data_only'] = kwargs.get(
            '_return_http_data_only', True
        )
        kwargs['_preload_content'] = kwargs.get(
            '_preload_content', True
        )
        kwargs['_request_timeout'] = kwargs.get(
            '_request_timeout', None
        )
        kwargs['_check_input_type'] = kwargs.get(
            '_check_input_type', True
        )
        kwargs['_check_return_type'] = kwargs.get(
            '_check_return_type', True
        )
        kwargs['_spec_property_naming'] = kwargs.get(
            '_spec_property_naming', False
        )
        kwargs['_content_type'] = kwargs.get(
            '_content_type')
        kwargs['_host_index'] = kwargs.get('_host_index')
        kwargs['_request_auths'] = kwargs.get('_request_auths', None)
        kwargs['originator_id'] = \
            originator_id
        return self.delete_originator_endpoint.call_with_http_info(**kwargs)

    def get_originators_list(
        self,
        **kwargs
    ):
        """Get originators list  # noqa: E501

        Retrieves the list of existing originators (sender ids). The originators are returned sorted by creation date, with the most recent group appearing first.    If no originators are available, an empty data object is returned  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.get_originators_list(async_req=True)
        >>> result = thread.get()


        Keyword Args:
            _return_http_data_only (bool): response data without head status
                code and headers. Default is True.
            _preload_content (bool): if False, the urllib3.HTTPResponse object
                will be returned without reading/decoding response data.
                Default is True.
            _request_timeout (int/float/tuple): timeout setting for this request. If
                one number provided, it will be total request timeout. It can also
                be a pair (tuple) of (connection, read) timeouts.
                Default is None.
            _check_input_type (bool): specifies if type checking
                should be done one the data sent to the server.
                Default is True.
            _check_return_type (bool): specifies if type checking
                should be done one the data received from the server.
                Default is True.
            _spec_property_naming (bool): True if the variable names in the input data
                are serialized names.
                False if the variable names in the input data
                are pythonic names, e.g. snake case (default)
            _content_type (str/None): force body content-type.
                Default is None and content-type will be predicted by allowed
                content-types and body.
            _host_index (int/None): specifies the index of the server
                that we want to use.
                Default is read from the configuration.
            _request_auths (list): set to override the auth_settings for an a single
                request; this effectively ignores the authentication
                in the spec for a single request.
                Default is None
            async_req (bool): execute request asynchronously

        Returns:
            OriginatorsListResponse
                If the method is called asynchronously, returns the request
                thread.
        """
        kwargs['async_req'] = kwargs.get(
            'async_req', False
        )
        kwargs['_return_http_data_only'] = kwargs.get(
            '_return_http_data_only', True
        )
        kwargs['_preload_content'] = kwargs.get(
            '_preload_content', True
        )
        kwargs['_request_timeout'] = kwargs.get(
            '_request_timeout', None
        )
        kwargs['_check_input_type'] = kwargs.get(
            '_check_input_type', True
        )
        kwargs['_check_return_type'] = kwargs.get(
            '_check_return_type', True
        )
        kwargs['_spec_property_naming'] = kwargs.get(
            '_spec_property_naming', False
        )
        kwargs['_content_type'] = kwargs.get(
            '_content_type')
        kwargs['_host_index'] = kwargs.get('_host_index')
        kwargs['_request_auths'] = kwargs.get('_request_auths', None)
        return self.get_originators_list_endpoint.call_with_http_info(**kwargs)

