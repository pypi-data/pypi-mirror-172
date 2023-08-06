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
from smscx_client.model.delete_scheduled_campaign import DeleteScheduledCampaign
from smscx_client.model.delete_scheduled_msg import DeleteScheduledMsg
from smscx_client.model.model400_invalid_param import Model400InvalidParam
from smscx_client.model.model401_unauthorized import Model401Unauthorized
from smscx_client.model.model403_insufficient_scope import Model403InsufficientScope
from smscx_client.model.model403_no_coverage import Model403NoCoverage
from smscx_client.model.model404_not_found import Model404NotFound
from smscx_client.model.model500_server_error import Model500ServerError
from smscx_client.model.send_multichannel_campaign_request import SendMultichannelCampaignRequest
from smscx_client.model.send_multichannel_campaign_request_estimate import SendMultichannelCampaignRequestEstimate
from smscx_client.model.send_multichannel_campaign_response import SendMultichannelCampaignResponse
from smscx_client.model.send_multichannel_message_request import SendMultichannelMessageRequest
from smscx_client.model.send_multichannel_message_request_estimate import SendMultichannelMessageRequestEstimate
from smscx_client.model.send_multichannel_message_response import SendMultichannelMessageResponse


class MultichannelApi(object):
    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client
        self.delete_scheduled_multichannel_campaign_endpoint = _Endpoint(
            settings={
                'response_type': (DeleteScheduledCampaign,),
                'auth': [
                    'ApiKeyAuth',
                    'BearerAuth'
                ],
                'endpoint_path': '/multichannel/scheduled/campaign/{campaignId}',
                'operation_id': 'delete_scheduled_multichannel_campaign',
                'http_method': 'DELETE',
                'servers': None,
            },
            params_map={
                'all': [
                    'campaign_id',
                ],
                'required': [
                    'campaign_id',
                ],
                'nullable': [
                ],
                'enum': [
                ],
                'validation': [
                    'campaign_id',
                ]
            },
            root_map={
                'validations': {
                    ('campaign_id',): {
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
                    'campaign_id':
                        (str,),
                },
                'attribute_map': {
                    'campaign_id': 'campaignId',
                },
                'location_map': {
                    'campaign_id': 'path',
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
        self.delete_scheduled_multichannel_message_endpoint = _Endpoint(
            settings={
                'response_type': (DeleteScheduledMsg,),
                'auth': [
                    'ApiKeyAuth',
                    'BearerAuth'
                ],
                'endpoint_path': '/multichannel/scheduled/{msgId}',
                'operation_id': 'delete_scheduled_multichannel_message',
                'http_method': 'DELETE',
                'servers': None,
            },
            params_map={
                'all': [
                    'msg_id',
                ],
                'required': [
                    'msg_id',
                ],
                'nullable': [
                ],
                'enum': [
                ],
                'validation': [
                    'msg_id',
                ]
            },
            root_map={
                'validations': {
                    ('msg_id',): {
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
                    'msg_id':
                        (str,),
                },
                'attribute_map': {
                    'msg_id': 'msgId',
                },
                'location_map': {
                    'msg_id': 'path',
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
        self.estimate_multichannel_campaign_endpoint = _Endpoint(
            settings={
                'response_type': (SendMultichannelCampaignResponse,),
                'auth': [
                    'ApiKeyAuth',
                    'BearerAuth'
                ],
                'endpoint_path': '/multichannel/campaign/estimate',
                'operation_id': 'estimate_multichannel_campaign',
                'http_method': 'POST',
                'servers': None,
            },
            params_map={
                'all': [
                    'send_multichannel_campaign_request_estimate',
                ],
                'required': [
                    'send_multichannel_campaign_request_estimate',
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
                    'send_multichannel_campaign_request_estimate':
                        (SendMultichannelCampaignRequestEstimate,),
                },
                'attribute_map': {
                },
                'location_map': {
                    'send_multichannel_campaign_request_estimate': 'body',
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
        self.estimate_multichannel_message_endpoint = _Endpoint(
            settings={
                'response_type': (SendMultichannelMessageResponse,),
                'auth': [
                    'ApiKeyAuth',
                    'BearerAuth'
                ],
                'endpoint_path': '/multichannel/estimate',
                'operation_id': 'estimate_multichannel_message',
                'http_method': 'POST',
                'servers': None,
            },
            params_map={
                'all': [
                    'send_multichannel_message_request_estimate',
                ],
                'required': [
                    'send_multichannel_message_request_estimate',
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
                    'send_multichannel_message_request_estimate':
                        (SendMultichannelMessageRequestEstimate,),
                },
                'attribute_map': {
                },
                'location_map': {
                    'send_multichannel_message_request_estimate': 'body',
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
        self.send_multichannel_campaign_endpoint = _Endpoint(
            settings={
                'response_type': (SendMultichannelCampaignResponse,),
                'auth': [
                    'ApiKeyAuth',
                    'BearerAuth'
                ],
                'endpoint_path': '/multichannel/campaign',
                'operation_id': 'send_multichannel_campaign',
                'http_method': 'POST',
                'servers': None,
            },
            params_map={
                'all': [
                    'send_multichannel_campaign_request',
                ],
                'required': [
                    'send_multichannel_campaign_request',
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
                    'send_multichannel_campaign_request':
                        (SendMultichannelCampaignRequest,),
                },
                'attribute_map': {
                },
                'location_map': {
                    'send_multichannel_campaign_request': 'body',
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
        self.send_multichannel_message_endpoint = _Endpoint(
            settings={
                'response_type': (SendMultichannelMessageResponse,),
                'auth': [
                    'ApiKeyAuth',
                    'BearerAuth'
                ],
                'endpoint_path': '/multichannel',
                'operation_id': 'send_multichannel_message',
                'http_method': 'POST',
                'servers': None,
            },
            params_map={
                'all': [
                    'send_multichannel_message_request',
                ],
                'required': [
                    'send_multichannel_message_request',
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
                    'send_multichannel_message_request':
                        (SendMultichannelMessageRequest,),
                },
                'attribute_map': {
                },
                'location_map': {
                    'send_multichannel_message_request': 'body',
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

    def delete_scheduled_multichannel_campaign(
        self,
        campaign_id,
        **kwargs
    ):
        """Delete scheduled Multichannel campaign  # noqa: E501

        Delete a scheduled Multichannel campaign by providing a valid identifier (`campaignId`).    The cost of the deleted scheduled Multichannel campaign will be returned to the balance of the account.    If part of the Multichannel campaign has already started, only scheduled messages will be deleted. Messages already sent cannot be deleted.    
### Errors for DELETE `/multichannel/scheduled/campaign/{campaignId}`  
| HTTP code  | Error code  | Type  | Description  |  
|:------------:|:------------:|:------------:| ------------ |  
|  403 | 1118  |  access_denied  |  Only scheduled campaigns/messages can be deleted |  
|  404 | 1150  |  not_found  |  Campaign ID provided was not found or is not scheduled |  

|  400 | 1155  |  invalid_param  |  Campaign ID provided is not valid |  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.delete_scheduled_multichannel_campaign(campaign_id, async_req=True)
        >>> result = thread.get()

        Args:
            campaign_id (str): Identifier of a scheduled Multichannel campaign

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
            DeleteScheduledCampaign
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
        kwargs['campaign_id'] = \
            campaign_id
        return self.delete_scheduled_multichannel_campaign_endpoint.call_with_http_info(**kwargs)

    def delete_scheduled_multichannel_message(
        self,
        msg_id,
        **kwargs
    ):
        """Delete scheduled Multichannel message  # noqa: E501

        Delete a scheduled Multichannel message by providing a valid identifier (`msgId`).    The cost of the deleted scheduled Multichannel message will be returned to the balance of the account.    
### Errors for DELETE `/multichannel/scheduled/{msgId}`  
| HTTP code  | Error code  | Type  | Description  |  
|:------------:|:------------:|:------------:| ------------ |  
|  403 | 1118  |  access_denied  |  Only scheduled campaigns/messages can be deleted |  
|  404 | 1100  |  not_found  |  Message ID provided was not found or is not scheduled |  

|  400 | 1115  |  invalid_param  |  Message ID provided is not valid |  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.delete_scheduled_multichannel_message(msg_id, async_req=True)
        >>> result = thread.get()

        Args:
            msg_id (str): Identifier of a scheduled Multichannel message

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
            DeleteScheduledMsg
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
        kwargs['msg_id'] = \
            msg_id
        return self.delete_scheduled_multichannel_message_endpoint.call_with_http_info(**kwargs)

    def estimate_multichannel_campaign(
        self,
        send_multichannel_campaign_request_estimate,
        **kwargs
    ):
        """Estimate Multichannel campaign  # noqa: E501

        Estimate the cost of sending a Multichannel message to groups of phone numbers.    This endpoint is identical to `/multichannel/campaign` endpoint, but it will only simulate the Multichannel sending (no billing).    The request body and the response are the same as for `/multichannel/campaign` endpoint.    
### Errors for POST `/multichannel/campaigns/estimate`  
| HTTP code  | Error code  | Type  | Description  |  
|:------------:|:------------:|:------------:| ------------ |  
|  400 | 1101  |  invalid_param  |  The parameter `groups` is empty or not set |  

|  400 | 1140  |  invalid_param  |  Group ID is not a valid group |  

|  400 | 1102  |  invalid_param  |  Group is empty |  

|  400 | 1103  |  invalid_param  |  The phone numbers array is too big (max. allowed: 25000 numbers) |  

|  400 | 1105  |  invalid_param  |  The parameter `from` is empty or not set |  

|  400 | 1106  |  invalid_param  |  The parameter `from` is not valid (min 3, max 11 characters) |  

|  400 | 1107  |  invalid_param  |  The parameter `text` is empty or not set |  

|  400 | 1108  |  invalid_param  |  The parameter `scheduledDate` is not a valid date |  

|  400 | 1109  |  invalid_param  |  The parameter `dlrCallbackUrl` is not a valid URL |  

|  400 | 1112  |  invalid_param  |  The shortlink/attachment ID provided for tracking is invalid or not found |  

|  400 | 1116  |  invalid_param  |  The scheduled date is in the past |  

|  400 | 1103  |  invalid_param  |  The phone numbers array is too big (max. allowed: 25000 numbers) |  
|  403 | 1119  |  no_coverage  |  No coverage or restricted destination |  

|  400 | 1113  |  insufficient_credit  |  Insufficient credit |  

|  400 | 1114  |  insufficient_credit  |  Credit limit reached. To increase the credit limit, please contact your account manager |  

|  400 | 1124  |  invalid_param  |  The parameter `ttl` is not a number |  

|  400 | 1125  |  invalid_param  |  Min value for `ttl` is 300 seconds |  

|  400 | 1134  |  invalid_param  |  Max value for `ttl` is 1209600 seconds (14 days) |  

|  400 | 1120  |  invalid_param  |  The parameter `strategy` is empty or not set |  

|  400 | 1121  |  invalid_param  |  The parameter `strategy` must have at least two channels |  

|  400 | 1122  |  invalid_param  |  The parameter `strategy` must have channel `sms` as last element |  

|  400 | 1129  |  invalid_param  |  The parameter `strategy` contains duplicate channels |  

|  400 | 1123  |  invalid_param  |  The parameter `channel` is not valid. Allowed values: |  
|  403 | 1131  |  access_denied  |  The strategy contains channels that are not active: |  

|  400 | 1126  |  invalid_param  |  The parameter `templateId` is not set |  

|  400 | 1127  |  invalid_param  |  The parameter `templateId` is not valid |  

|  400 | 1128  |  invalid_param  |  The template ID provided is not a valid template |  
|  403 | 1132  |  access_denied  |  The template ID provided is not approved |  
|  403 | 1133  |  access_denied  |  The template ID provided is not locked |  

|  400 | 1130  |  insufficient_credit  |  Insufficient credit for failover sending |  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.estimate_multichannel_campaign(send_multichannel_campaign_request_estimate, async_req=True)
        >>> result = thread.get()

        Args:
            send_multichannel_campaign_request_estimate (SendMultichannelCampaignRequestEstimate): 

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
            SendMultichannelCampaignResponse
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
        kwargs['send_multichannel_campaign_request_estimate'] = \
            send_multichannel_campaign_request_estimate
        return self.estimate_multichannel_campaign_endpoint.call_with_http_info(**kwargs)

    def estimate_multichannel_message(
        self,
        send_multichannel_message_request_estimate,
        **kwargs
    ):
        """Estimate Multichannel message  # noqa: E501

        Estimate the cost of sending a Multichannel message.    This endpoint is identical to `/multichannel` endpoint, but it will only simulate the Multichannel sending (no billing).    The request body and the response are the same as for `/multichannel` endpoint.    
### Errors for POST `/multichannel/estimate`  
| HTTP code  | Error code  | Type  | Description  |  
|:------------:|:------------:|:------------:| ------------ |  
|  400 | 1104  |  invalid_param  | The parameter `to` is empty or not set |  

|  400 | 1105  |  invalid_param  |  The parameter `from` is empty or not set |  

|  400 | 1106  |  invalid_param  |  The parameter `from` is not valid (min 3, max 11 characters) |  

|  400 | 1107  |  invalid_param  |  The parameter `text` is empty or not set |  

|  400 | 1108  |  invalid_param  |  The parameter `scheduledDate` is not a valid date |  

|  400 | 1109  |  invalid_param  |  The parameter `dlrCallbackUrl` is not a valid URL |  

|  400 | 1112  |  invalid_param  |  The shortlink/attachment ID provided for tracking is invalid or not found |  

|  400 | 1116  |  invalid_param  |  The scheduled date is in the past |  

|  400 | 1103  |  invalid_param  |  The phone numbers array is too big (max. allowed: 25000 numbers) |  

|  400 | 1207  |  invalid_param  | The phone number provided is not valid |  

|  400 | 1210  |  invalid_param  |  The phone numbers provided are invalid |  
|  403 | 1119  |  no_coverage  |  No coverage or restricted destination |  

|  400 | 1113  |  insufficient_credit  |  Insufficient credit |  

|  400 | 1114  |  insufficient_credit  |  Credit limit reached. To increase the credit limit, please contact your account manager |  

|  400 | 1130  |  insufficient_credit  |  Insufficient credit for failover sending |  

|  400 | 1124  |  invalid_param  |  The parameter `ttl` is not a number |  

|  400 | 1125  |  invalid_param  |  Min value for `ttl` is 300 seconds |  

|  400 | 1134  |  invalid_param  |  Max value for `ttl` is 1209600 seconds (14 days) |  

|  400 | 1120  |  invalid_param  |  The parameter `strategy` is empty or not set |  

|  400 | 1121  |  invalid_param  |  The parameter `strategy` must have at least two channels |  

|  400 | 1122  |  invalid_param  |  The parameter `strategy` must have channel `sms` as last element |  

|  400 | 1129  |  invalid_param  |  The parameter `strategy` contains duplicate channels |  

|  400 | 1123  |  invalid_param  |  The parameter `channel` is not valid. Allowed values: |  
|  403 | 1131  |  access_denied  |  The strategy contains channels that are not active: |  

|  400 | 1126  |  invalid_param  |  The parameter `templateId` is not set |  

|  400 | 1127  |  invalid_param  |  The parameter `templateId` is not valid |  

|  400 | 1128  |  invalid_param  |  The template ID provided is not a valid template |  
|  403 | 1132  |  access_denied  |  The template ID provided is not approved |  
|  403 | 1133  |  access_denied  |  The template ID provided is not locked |  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.estimate_multichannel_message(send_multichannel_message_request_estimate, async_req=True)
        >>> result = thread.get()

        Args:
            send_multichannel_message_request_estimate (SendMultichannelMessageRequestEstimate): 

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
            SendMultichannelMessageResponse
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
        kwargs['send_multichannel_message_request_estimate'] = \
            send_multichannel_message_request_estimate
        return self.estimate_multichannel_message_endpoint.call_with_http_info(**kwargs)

    def send_multichannel_campaign(
        self,
        send_multichannel_campaign_request,
        **kwargs
    ):
        """Send Multichannel campaign  # noqa: E501

        <a name=\"post-multichannel-campaign\"></a>    Sends Multichannel message to existing group(s) of contacts.    > Note: This endpoint accepts idempotent requests by providing an additional `idempotencyId` parameter in body with a unique value generated by the client of type UUID v1-v5. To confirm that the server understood the request, the response will contain the header `X-Idempotency-Id` with your unique value.  By using idempotency you can retry requests in case of network error or server not responding in time, without accidentally performing the same operation twice and have a guarantee of not being billed twice.     > We recommend to always use Idempotency ID when sending Multichannel campaigns    
### Errors for POST `/multichannel/campaigns`  
| HTTP code  | Error code  | Type  | Description  |  
|:------------:|:------------:|:------------:| ------------ |  
|  400 | 1101  |  invalid_param  |  The parameter `groups` is empty or not set |  

|  400 | 1140  |  invalid_param  |  Group ID is not a valid group |  

|  400 | 1102  |  invalid_param  |  Group is empty |  

|  400 | 1103  |  invalid_param  |  The phone numbers array is too big (max. allowed: 25000 numbers) |  

|  400 | 1105  |  invalid_param  |  The parameter `from` is empty or not set |  

|  400 | 1106  |  invalid_param  |  The parameter `from` is not valid (min 3, max 11 characters) |  

|  400 | 1107  |  invalid_param  |  The parameter `text` is empty or not set |  

|  400 | 1108  |  invalid_param  |  The parameter `scheduledDate` is not a valid date |  

|  400 | 1109  |  invalid_param  |  The parameter `dlrCallbackUrl` is not a valid URL |  

|  400 | 1111  |  invalid_param  |  Idempotency Id provided is not a valid UUID (v1-v5) |  

|  400 | 1112  |  invalid_param  |  The shortlink/attachment ID provided for tracking is invalid or not found |  

|  400 | 1116  |  invalid_param  |  The scheduled date is in the past |  

|  400 | 1103  |  invalid_param  |  The phone numbers array is too big (max. allowed: 25000 numbers) |  
|  403 | 1119  |  no_coverage  |  No coverage or restricted destination |  

|  400 | 1113  |  insufficient_credit  |  Insufficient credit |  

|  400 | 1114  |  insufficient_credit  |  Credit limit reached. To increase the credit limit, please contact your account manager |  

|  400 | 1124  |  invalid_param  |  The parameter `ttl` is not a number |  

|  400 | 1125  |  invalid_param  |  Min value for `ttl` is 300 seconds |  

|  400 | 1134  |  invalid_param  |  Max value for `ttl` is 1209600 seconds (14 days) |  

|  400 | 1120  |  invalid_param  |  The parameter `strategy` is empty or not set |  

|  400 | 1121  |  invalid_param  |  The parameter `strategy` must have at least two channels |  

|  400 | 1122  |  invalid_param  |  The parameter `strategy` must have channel `sms` as last element |  

|  400 | 1129  |  invalid_param  |  The parameter `strategy` contains duplicate channels |  

|  400 | 1123  |  invalid_param  |  The parameter `channel` is not valid. Allowed values: |  
|  403 | 1131  |  access_denied  |  The strategy contains channels that are not active: |  

|  400 | 1126  |  invalid_param  |  The parameter `templateId` is not set |  

|  400 | 1127  |  invalid_param  |  The parameter `templateId` is not valid |  

|  400 | 1128  |  invalid_param  |  The template ID provided is not a valid template |  
|  403 | 1132  |  access_denied  |  The template ID provided is not approved |  
|  403 | 1133  |  access_denied  |  The template ID provided is not locked |  

|  400 | 1130  |  insufficient_credit  |  Insufficient credit for failover sending |  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.send_multichannel_campaign(send_multichannel_campaign_request, async_req=True)
        >>> result = thread.get()

        Args:
            send_multichannel_campaign_request (SendMultichannelCampaignRequest): 

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
            SendMultichannelCampaignResponse
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
        kwargs['send_multichannel_campaign_request'] = \
            send_multichannel_campaign_request
        return self.send_multichannel_campaign_endpoint.call_with_http_info(**kwargs)

    def send_multichannel_message(
        self,
        send_multichannel_message_request,
        **kwargs
    ):
        """Send Multichannel message  # noqa: E501

        <a name=\"post-multichannel\"></a>    Sends Multichannel message to a single phone number or to a list of phone numbers.    This endpoint was designed to handle big data objects (up to 25.000 Multichannel messages in one request).    If you have loops or iterations we recommend building the send object in your application, and make a single request to this endpoint. The time of making the requests will decrease - by doing a single request with multiple send objects vs making requests in a loop -  and you won't have to worry about making concurrent API calls.    > Note: This endpoint accepts idempotent requests by providing an additional `idempotencyId` parameter in body with a unique value generated by the client of type UUID v1-v5. To confirm that the server understood the request, the response will contain the header `X-Idempotency-Id` with your unique value.  By using idempotency you can retry requests in case of network error or server not responding in time, without accidentally performing the same operation twice and have a guarantee of not being billed twice.       
### Errors for POST `/multichannel`  
| HTTP code  | Error code  | Type  | Description  |  
|:------------:|:------------:|:------------:| ------------ |  
|  400 | 1104  |  invalid_param  | The parameter `to` is empty or not set |  

|  400 | 1105  |  invalid_param  |  The parameter `from` is empty or not set |  

|  400 | 1106  |  invalid_param  |  The parameter `from` is not valid (min 3, max 11 characters) |  

|  400 | 1107  |  invalid_param  |  The parameter `text` is empty or not set |  

|  400 | 1108  |  invalid_param  |  The parameter `scheduledDate` is not a valid date |  

|  400 | 1109  |  invalid_param  |  The parameter `dlrCallbackUrl` is not a valid URL |  

|  400 | 1111  |  invalid_param  |  Idempotency Id provided is not a valid UUID (v1-v5) |  

|  400 | 1112  |  invalid_param  |  The shortlink/attachment ID provided for tracking is invalid or not found |  

|  400 | 1116  |  invalid_param  |  The scheduled date is in the past |  

|  400 | 1103  |  invalid_param  |  The phone numbers array is too big (max. allowed: 25000 numbers) |  

|  400 | 1207  |  invalid_param  | The phone number provided is not valid |  

|  400 | 1210  |  invalid_param  |  The phone numbers provided are invalid |  
|  403 | 1119  |  no_coverage  |  No coverage or restricted destination |  

|  400 | 1113  |  insufficient_credit  |  Insufficient credit |  

|  400 | 1114  |  insufficient_credit  |  Credit limit reached. To increase the credit limit, please contact your account manager |  

|  400 | 1130  |  insufficient_credit  |  Insufficient credit for failover sending |  

|  400 | 1124  |  invalid_param  |  The parameter `ttl` is not a number |  

|  400 | 1125  |  invalid_param  |  Min value for `ttl` is 300 seconds |  

|  400 | 1134  |  invalid_param  |  Max value for `ttl` is 1209600 seconds (14 days) |  

|  400 | 1120  |  invalid_param  |  The parameter `strategy` is empty or not set |  

|  400 | 1121  |  invalid_param  |  The parameter `strategy` must have at least two channels |  

|  400 | 1122  |  invalid_param  |  The parameter `strategy` must have channel `sms` as last element |  

|  400 | 1129  |  invalid_param  |  The parameter `strategy` contains duplicate channels |  

|  400 | 1123  |  invalid_param  |  The parameter `channel` is not valid. Allowed values: |  
|  403 | 1131  |  access_denied  |  The strategy contains channels that are not active: |  

|  400 | 1126  |  invalid_param  |  The parameter `templateId` is not set |  

|  400 | 1127  |  invalid_param  |  The parameter `templateId` is not valid |  

|  400 | 1128  |  invalid_param  |  The template ID provided is not a valid template |  
|  403 | 1132  |  access_denied  |  The template ID provided is not approved |  
|  403 | 1133  |  access_denied  |  The template ID provided is not locked |  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.send_multichannel_message(send_multichannel_message_request, async_req=True)
        >>> result = thread.get()

        Args:
            send_multichannel_message_request (SendMultichannelMessageRequest): 

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
            SendMultichannelMessageResponse
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
        kwargs['send_multichannel_message_request'] = \
            send_multichannel_message_request
        return self.send_multichannel_message_endpoint.call_with_http_info(**kwargs)

