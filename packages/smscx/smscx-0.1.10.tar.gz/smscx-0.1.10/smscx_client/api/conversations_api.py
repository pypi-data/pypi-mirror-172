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
from smscx_client.model.conversation_details_response import ConversationDetailsResponse
from smscx_client.model.conversation_read_response import ConversationReadResponse
from smscx_client.model.conversation_reply_sms_request import ConversationReplySmsRequest
from smscx_client.model.conversation_reply_sms_response import ConversationReplySmsResponse
from smscx_client.model.conversation_reply_viber_request import ConversationReplyViberRequest
from smscx_client.model.conversation_reply_viber_respone import ConversationReplyViberRespone
from smscx_client.model.conversation_reply_whatsapp_request import ConversationReplyWhatsappRequest
from smscx_client.model.conversation_reply_whatsapp_response import ConversationReplyWhatsappResponse
from smscx_client.model.conversations_list_response import ConversationsListResponse
from smscx_client.model.model400_invalid_param import Model400InvalidParam
from smscx_client.model.model401_unauthorized import Model401Unauthorized
from smscx_client.model.model403_insufficient_scope import Model403InsufficientScope
from smscx_client.model.model404_not_found import Model404NotFound
from smscx_client.model.model500_server_error import Model500ServerError


class ConversationsApi(object):
    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client
        self.get_conversation_endpoint = _Endpoint(
            settings={
                'response_type': (ConversationDetailsResponse,),
                'auth': [
                    'ApiKeyAuth',
                    'BearerAuth'
                ],
                'endpoint_path': '/conversations/{conversationId}',
                'operation_id': 'get_conversation',
                'http_method': 'GET',
                'servers': None,
            },
            params_map={
                'all': [
                    'conversation_id',
                ],
                'required': [
                    'conversation_id',
                ],
                'nullable': [
                ],
                'enum': [
                ],
                'validation': [
                    'conversation_id',
                ]
            },
            root_map={
                'validations': {
                    ('conversation_id',): {
                        'max_length': 36,
                        'min_length': 36,
                        'regex': {
                            'pattern': r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$',  # noqa: E501
                        },
                    },
                },
                'allowed_values': {
                },
                'api_types': {
                    'conversation_id':
                        (str,),
                },
                'attribute_map': {
                    'conversation_id': 'conversationId',
                },
                'location_map': {
                    'conversation_id': 'path',
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
        self.get_converstions_list_endpoint = _Endpoint(
            settings={
                'response_type': (ConversationsListResponse,),
                'auth': [
                    'ApiKeyAuth',
                    'BearerAuth'
                ],
                'endpoint_path': '/conversations',
                'operation_id': 'get_converstions_list',
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
        self.mark_conversation_as_read_endpoint = _Endpoint(
            settings={
                'response_type': (ConversationReadResponse,),
                'auth': [
                    'ApiKeyAuth',
                    'BearerAuth'
                ],
                'endpoint_path': '/conversations/{conversationId}/read',
                'operation_id': 'mark_conversation_as_read',
                'http_method': 'GET',
                'servers': None,
            },
            params_map={
                'all': [
                    'conversation_id',
                ],
                'required': [
                    'conversation_id',
                ],
                'nullable': [
                ],
                'enum': [
                ],
                'validation': [
                    'conversation_id',
                ]
            },
            root_map={
                'validations': {
                    ('conversation_id',): {
                        'max_length': 36,
                        'min_length': 36,
                        'regex': {
                            'pattern': r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$',  # noqa: E501
                        },
                    },
                },
                'allowed_values': {
                },
                'api_types': {
                    'conversation_id':
                        (str,),
                },
                'attribute_map': {
                    'conversation_id': 'conversationId',
                },
                'location_map': {
                    'conversation_id': 'path',
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
        self.send_conversation_reply_sms_endpoint = _Endpoint(
            settings={
                'response_type': (ConversationReplySmsResponse,),
                'auth': [
                    'ApiKeyAuth',
                    'BearerAuth'
                ],
                'endpoint_path': '/conversations/{conversationId}/sms',
                'operation_id': 'send_conversation_reply_sms',
                'http_method': 'POST',
                'servers': None,
            },
            params_map={
                'all': [
                    'conversation_id',
                    'conversation_reply_sms_request',
                ],
                'required': [
                    'conversation_id',
                    'conversation_reply_sms_request',
                ],
                'nullable': [
                ],
                'enum': [
                ],
                'validation': [
                    'conversation_id',
                ]
            },
            root_map={
                'validations': {
                    ('conversation_id',): {
                        'max_length': 36,
                        'min_length': 36,
                        'regex': {
                            'pattern': r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$',  # noqa: E501
                        },
                    },
                },
                'allowed_values': {
                },
                'api_types': {
                    'conversation_id':
                        (str,),
                    'conversation_reply_sms_request':
                        (ConversationReplySmsRequest,),
                },
                'attribute_map': {
                    'conversation_id': 'conversationId',
                },
                'location_map': {
                    'conversation_id': 'path',
                    'conversation_reply_sms_request': 'body',
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
        self.send_conversation_reply_viber_endpoint = _Endpoint(
            settings={
                'response_type': (ConversationReplyViberRespone,),
                'auth': [
                    'ApiKeyAuth',
                    'BearerAuth'
                ],
                'endpoint_path': '/conversations/{conversationId}/viber',
                'operation_id': 'send_conversation_reply_viber',
                'http_method': 'POST',
                'servers': None,
            },
            params_map={
                'all': [
                    'conversation_id',
                    'conversation_reply_viber_request',
                ],
                'required': [
                    'conversation_id',
                    'conversation_reply_viber_request',
                ],
                'nullable': [
                ],
                'enum': [
                ],
                'validation': [
                    'conversation_id',
                ]
            },
            root_map={
                'validations': {
                    ('conversation_id',): {
                        'max_length': 36,
                        'min_length': 36,
                        'regex': {
                            'pattern': r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$',  # noqa: E501
                        },
                    },
                },
                'allowed_values': {
                },
                'api_types': {
                    'conversation_id':
                        (str,),
                    'conversation_reply_viber_request':
                        (ConversationReplyViberRequest,),
                },
                'attribute_map': {
                    'conversation_id': 'conversationId',
                },
                'location_map': {
                    'conversation_id': 'path',
                    'conversation_reply_viber_request': 'body',
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
        self.send_conversation_reply_whatsapp_endpoint = _Endpoint(
            settings={
                'response_type': (ConversationReplyWhatsappResponse,),
                'auth': [
                    'ApiKeyAuth',
                    'BearerAuth'
                ],
                'endpoint_path': '/conversations/{conversationId}/whatsapp',
                'operation_id': 'send_conversation_reply_whatsapp',
                'http_method': 'POST',
                'servers': None,
            },
            params_map={
                'all': [
                    'conversation_id',
                    'conversation_reply_whatsapp_request',
                ],
                'required': [
                    'conversation_id',
                    'conversation_reply_whatsapp_request',
                ],
                'nullable': [
                ],
                'enum': [
                ],
                'validation': [
                    'conversation_id',
                ]
            },
            root_map={
                'validations': {
                    ('conversation_id',): {
                        'max_length': 36,
                        'min_length': 36,
                        'regex': {
                            'pattern': r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$',  # noqa: E501
                        },
                    },
                },
                'allowed_values': {
                },
                'api_types': {
                    'conversation_id':
                        (str,),
                    'conversation_reply_whatsapp_request':
                        (ConversationReplyWhatsappRequest,),
                },
                'attribute_map': {
                    'conversation_id': 'conversationId',
                },
                'location_map': {
                    'conversation_id': 'path',
                    'conversation_reply_whatsapp_request': 'body',
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

    def get_conversation(
        self,
        conversation_id,
        **kwargs
    ):
        """Get conversation  # noqa: E501

        Retrieves the details of a conversation if a valid identifier was provided.    
### Errors for GET `/conversations/{conversationId}`  
| HTTP code  | Error code  | Type  | Description  |  
|:------------:|:------------:|:------------:| ------------ |  
|  404 | 1180  |  not_found  | Conversation ID not found |  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.get_conversation(conversation_id, async_req=True)
        >>> result = thread.get()

        Args:
            conversation_id (str): Identifier of the conversation

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
            ConversationDetailsResponse
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
        kwargs['conversation_id'] = \
            conversation_id
        return self.get_conversation_endpoint.call_with_http_info(**kwargs)

    def get_converstions_list(
        self,
        **kwargs
    ):
        """Get conversations list  # noqa: E501

        Retrieves the list of existing conversations. The list is sorted by last reply date, with the most recent reply appearing first.    If no conversations are available, an empty data object is returned.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.get_converstions_list(async_req=True)
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
            ConversationsListResponse
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
        return self.get_converstions_list_endpoint.call_with_http_info(**kwargs)

    def mark_conversation_as_read(
        self,
        conversation_id,
        **kwargs
    ):
        """Mark conversation as read  # noqa: E501

        Marks a conversation as read    
### Errors for GET `/conversations/{conversationId}/read`  
| HTTP code  | Error code  | Type  | Description  |  
|:------------:|:------------:|:------------:| ------------ |  
|  404 | 1180  |  not_found  | Conversation ID not found |  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.mark_conversation_as_read(conversation_id, async_req=True)
        >>> result = thread.get()

        Args:
            conversation_id (str): Identifier of the conversation

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
            ConversationReadResponse
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
        kwargs['conversation_id'] = \
            conversation_id
        return self.mark_conversation_as_read_endpoint.call_with_http_info(**kwargs)

    def send_conversation_reply_sms(
        self,
        conversation_id,
        conversation_reply_sms_request,
        **kwargs
    ):
        """Send conversation reply via SMS  # noqa: E501

        Sends a reply to a conversation using sms channel.    
### Errors for POST `/conversations/{conversationId}/sms`  
| HTTP code  | Error code  | Type  | Description  |  
|:------------:|:------------:|:------------:| ------------ |  
|  404 | 1180  |  not_found  | Conversation ID not found |  

|  400 | 1801  |  invalid_param  | The text message is empty or parameter `text` not set |  

|  400 | 1802  |  invalid_param  | The parameter `text` is invalid |  

|  400 | 1111  |  invalid_param  |  Idempotency Id provided is not a valid UUID (v1-v5) |  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.send_conversation_reply_sms(conversation_id, conversation_reply_sms_request, async_req=True)
        >>> result = thread.get()

        Args:
            conversation_id (str): Identifier of the conversation
            conversation_reply_sms_request (ConversationReplySmsRequest): 

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
            ConversationReplySmsResponse
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
        kwargs['conversation_id'] = \
            conversation_id
        kwargs['conversation_reply_sms_request'] = \
            conversation_reply_sms_request
        return self.send_conversation_reply_sms_endpoint.call_with_http_info(**kwargs)

    def send_conversation_reply_viber(
        self,
        conversation_id,
        conversation_reply_viber_request,
        **kwargs
    ):
        """Send conversation reply via Viber  # noqa: E501

        Sends a reply to a conversation using viber channel.    
### Errors for POST `/conversations/{conversationId}/viber`  
| HTTP code  | Error code  | Type  | Description  |  
|:------------:|:------------:|:------------:| ------------ |  
|  404 | 1180  |  not_found  | Conversation ID not found |  
|  403 | 1181  |  access_denied  | Cannot reply with channel Viber. More than 24 hours since user reply |  

|  400 | 1801  |  invalid_param  | The text message is empty or parameter `text` not set |  

|  400 | 1802  |  invalid_param  | The parameter `text` is invalid |  

|  400 | 1811  |  invalid_param  | Text message too long (max 1000 characters) |  

|  400 | 1111  |  invalid_param  |  Idempotency Id provided is not a valid UUID (v1-v5) |  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.send_conversation_reply_viber(conversation_id, conversation_reply_viber_request, async_req=True)
        >>> result = thread.get()

        Args:
            conversation_id (str): Identifier of the conversation
            conversation_reply_viber_request (ConversationReplyViberRequest): 

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
            ConversationReplyViberRespone
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
        kwargs['conversation_id'] = \
            conversation_id
        kwargs['conversation_reply_viber_request'] = \
            conversation_reply_viber_request
        return self.send_conversation_reply_viber_endpoint.call_with_http_info(**kwargs)

    def send_conversation_reply_whatsapp(
        self,
        conversation_id,
        conversation_reply_whatsapp_request,
        **kwargs
    ):
        """Send conversation reply via Whatsapp  # noqa: E501

        Sends a reply to a conversation using whatsapp channel.    
### Errors for POST `/conversations/{conversationId}/whatsapp`  
| HTTP code  | Error code  | Type  | Description  |  
|:------------:|:------------:|:------------:| ------------ |  
|  404 | 1180  |  not_found  | Conversation ID not found |  
|  403 | 1182  |  access_denied  | Cannot reply with channel Whatsapp. More than 24 hours since user reply |  

|  400 | 1801  |  invalid_param  | The text message is empty or parameter `text` not set |  

|  400 | 1802  |  invalid_param  | The parameter `text` is invalid |  

|  400 | 1811  |  invalid_param  | Text message too long (max 1000 characters) |  

|  400 | 1111  |  invalid_param  |  Idempotency Id provided is not a valid UUID (v1-v5) |  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.send_conversation_reply_whatsapp(conversation_id, conversation_reply_whatsapp_request, async_req=True)
        >>> result = thread.get()

        Args:
            conversation_id (str): Identifier of the conversation
            conversation_reply_whatsapp_request (ConversationReplyWhatsappRequest): 

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
            ConversationReplyWhatsappResponse
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
        kwargs['conversation_id'] = \
            conversation_id
        kwargs['conversation_reply_whatsapp_request'] = \
            conversation_reply_whatsapp_request
        return self.send_conversation_reply_whatsapp_endpoint.call_with_http_info(**kwargs)

