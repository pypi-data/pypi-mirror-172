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
from smscx_client.model.shortlink_delete_response import ShortlinkDeleteResponse
from smscx_client.model.shortlink_details_response import ShortlinkDetailsResponse
from smscx_client.model.shortlink_new_request import ShortlinkNewRequest
from smscx_client.model.shortlink_new_response import ShortlinkNewResponse
from smscx_client.model.shortlink_update_request import ShortlinkUpdateRequest
from smscx_client.model.shortlink_update_response import ShortlinkUpdateResponse
from smscx_client.model.shortlinks_list_response import ShortlinksListResponse


class ShortlinksApi(object):
    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client
        self.create_shortlink_endpoint = _Endpoint(
            settings={
                'response_type': (ShortlinkNewResponse,),
                'auth': [
                    'ApiKeyAuth',
                    'BearerAuth'
                ],
                'endpoint_path': '/shortlinks',
                'operation_id': 'create_shortlink',
                'http_method': 'POST',
                'servers': None,
            },
            params_map={
                'all': [
                    'shortlink_new_request',
                ],
                'required': [
                    'shortlink_new_request',
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
                    'shortlink_new_request':
                        (ShortlinkNewRequest,),
                },
                'attribute_map': {
                },
                'location_map': {
                    'shortlink_new_request': 'body',
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
        self.delete_shortlink_endpoint = _Endpoint(
            settings={
                'response_type': (ShortlinkDeleteResponse,),
                'auth': [
                    'ApiKeyAuth',
                    'BearerAuth'
                ],
                'endpoint_path': '/shortlinks/{shortId}',
                'operation_id': 'delete_shortlink',
                'http_method': 'DELETE',
                'servers': None,
            },
            params_map={
                'all': [
                    'short_id',
                ],
                'required': [
                    'short_id',
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
                    'short_id':
                        (str,),
                },
                'attribute_map': {
                    'short_id': 'shortId',
                },
                'location_map': {
                    'short_id': 'path',
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
        self.export_shortlink_hits_to_csv_endpoint = _Endpoint(
            settings={
                'response_type': (str,),
                'auth': [
                    'ApiKeyAuth',
                    'BearerAuth'
                ],
                'endpoint_path': '/shortlinks/{shortId}/csv',
                'operation_id': 'export_shortlink_hits_to_csv',
                'http_method': 'GET',
                'servers': None,
            },
            params_map={
                'all': [
                    'short_id',
                ],
                'required': [
                    'short_id',
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
                    'short_id':
                        (str,),
                },
                'attribute_map': {
                    'short_id': 'shortId',
                },
                'location_map': {
                    'short_id': 'path',
                },
                'collection_format_map': {
                }
            },
            headers_map={
                'accept': [
                    'application/csv',
                    'application/json'
                ],
                'content_type': [],
            },
            api_client=api_client
        )
        self.export_shortlink_hits_to_xlsx_endpoint = _Endpoint(
            settings={
                'response_type': (file_type,),
                'auth': [
                    'ApiKeyAuth',
                    'BearerAuth'
                ],
                'endpoint_path': '/shortlinks/{shortId}/xlsx',
                'operation_id': 'export_shortlink_hits_to_xlsx',
                'http_method': 'GET',
                'servers': None,
            },
            params_map={
                'all': [
                    'short_id',
                ],
                'required': [
                    'short_id',
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
                    'short_id':
                        (str,),
                },
                'attribute_map': {
                    'short_id': 'shortId',
                },
                'location_map': {
                    'short_id': 'path',
                },
                'collection_format_map': {
                }
            },
            headers_map={
                'accept': [
                    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                    'application/json'
                ],
                'content_type': [],
            },
            api_client=api_client
        )
        self.get_shortlink_hits_endpoint = _Endpoint(
            settings={
                'response_type': (ShortlinkDetailsResponse,),
                'auth': [
                    'ApiKeyAuth',
                    'BearerAuth'
                ],
                'endpoint_path': '/shortlinks/{shortId}',
                'operation_id': 'get_shortlink_hits',
                'http_method': 'GET',
                'servers': None,
            },
            params_map={
                'all': [
                    'short_id',
                    'short_response',
                    'limit',
                    'next',
                    'previous',
                ],
                'required': [
                    'short_id',
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
                    'short_id':
                        (str,),
                    'short_response':
                        (bool,),
                    'limit':
                        (int,),
                    'next':
                        (str,),
                    'previous':
                        (str,),
                },
                'attribute_map': {
                    'short_id': 'shortId',
                    'short_response': 'short_response',
                    'limit': 'limit',
                    'next': 'next',
                    'previous': 'previous',
                },
                'location_map': {
                    'short_id': 'path',
                    'short_response': 'query',
                    'limit': 'query',
                    'next': 'query',
                    'previous': 'query',
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
        self.get_shortlinks_list_endpoint = _Endpoint(
            settings={
                'response_type': (ShortlinksListResponse,),
                'auth': [
                    'ApiKeyAuth',
                    'BearerAuth'
                ],
                'endpoint_path': '/shortlinks',
                'operation_id': 'get_shortlinks_list',
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
        self.update_shortlink_endpoint = _Endpoint(
            settings={
                'response_type': (ShortlinkUpdateResponse,),
                'auth': [
                    'ApiKeyAuth',
                    'BearerAuth'
                ],
                'endpoint_path': '/shortlinks/{shortId}',
                'operation_id': 'update_shortlink',
                'http_method': 'PATCH',
                'servers': None,
            },
            params_map={
                'all': [
                    'short_id',
                    'shortlink_update_request',
                ],
                'required': [
                    'short_id',
                    'shortlink_update_request',
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
                    'short_id':
                        (str,),
                    'shortlink_update_request':
                        (ShortlinkUpdateRequest,),
                },
                'attribute_map': {
                    'short_id': 'shortId',
                },
                'location_map': {
                    'short_id': 'path',
                    'shortlink_update_request': 'body',
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

    def create_shortlink(
        self,
        shortlink_new_request,
        **kwargs
    ):
        """Create shortlink  # noqa: E501

        Creates a new shortlink.    
### Errors for POST `/shortlinks`  
| HTTP code  | Error code  | Type  | Description  |  
|:------------:|:------------:|:------------:| ------------ |  
|  400 | 1401  |  invalid_param  |  The URL is empty or parameter `url` not set |  

|  400 | 1402  |  invalid_param  |  The URL provided is invalid |  

|  400 | 1404  |  invalid_param  |  The parameter `name` is invalid (min 3, max 25 characters) |  

|  400 | 1405  |  duplicate_id  |  Short ID already exists |  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.create_shortlink(shortlink_new_request, async_req=True)
        >>> result = thread.get()

        Args:
            shortlink_new_request (ShortlinkNewRequest): 

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
            ShortlinkNewResponse
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
        kwargs['shortlink_new_request'] = \
            shortlink_new_request
        return self.create_shortlink_endpoint.call_with_http_info(**kwargs)

    def delete_shortlink(
        self,
        short_id,
        **kwargs
    ):
        """Delete shortlink  # noqa: E501

        Deletes a shortlink and all the hits data associated, if a valid identifier was provided.    
### Errors for DELETE `/shortlinks/{shortId}`  
| HTTP code  | Error code  | Type  | Description  |  
|:------------:|:------------:|:------------:| ------------ |  
|  404 | 1400  |  not_found  |  Shortlink ID not found |  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.delete_shortlink(short_id, async_req=True)
        >>> result = thread.get()

        Args:
            short_id (str): Identifier of the shortlink

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
            ShortlinkDeleteResponse
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
        kwargs['short_id'] = \
            short_id
        return self.delete_shortlink_endpoint.call_with_http_info(**kwargs)

    def export_shortlink_hits_to_csv(
        self,
        short_id,
        **kwargs
    ):
        """Export shortlink hits to CSV  # noqa: E501

        Exports the hits details of a shortlink (phone number, device, model, operating system, browser, city, country, etc.) to a CSV file.    If there are no hits for the shortlink, an empty CSV file is returned (with first line headers).    
### Errors for GET `/shortlinks/{shortId}/csv`  
| HTTP code  | Error code  | Type  | Description  |  
|:------------:|:------------:|:------------:| ------------ |  
|  404 | 1400  |  not_found  |  Shortlink ID not found |  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.export_shortlink_hits_to_csv(short_id, async_req=True)
        >>> result = thread.get()

        Args:
            short_id (str): Identifier of the shortlink

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
            str
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
        kwargs['short_id'] = \
            short_id
        return self.export_shortlink_hits_to_csv_endpoint.call_with_http_info(**kwargs)

    def export_shortlink_hits_to_xlsx(
        self,
        short_id,
        **kwargs
    ):
        """Export shortlink hits to XLSX  # noqa: E501

        Exports the hits details of a shortlink (phone number, device, model, operating system, browser, city, country, etc.) to a XLSX file (Excel).    If there are no hits for the shortlink, an empty XLSX file is returned (with first line headers).    
### Errors for GET `/shortlinks/{shortId}/xlsx`  
| HTTP code  | Error code  | Type  | Description  |  
|:------------:|:------------:|:------------:| ------------ |  
|  404 | 1400  |  not_found  |  Shortlink ID not found |  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.export_shortlink_hits_to_xlsx(short_id, async_req=True)
        >>> result = thread.get()

        Args:
            short_id (str): Identifier of the shortlink

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
            file_type
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
        kwargs['short_id'] = \
            short_id
        return self.export_shortlink_hits_to_xlsx_endpoint.call_with_http_info(**kwargs)

    def get_shortlink_hits(
        self,
        short_id,
        **kwargs
    ):
        """Get shortlink hits  # noqa: E501

        Retrieves the hits details (phone number, device, model, operating system, browser, city, country, etc.) of a shortlink if a valid identifier was provided.    
### Errors for GET `/shortlinks/{shortId}`  
| HTTP code  | Error code  | Type  | Description  |  
|:------------:|:------------:|:------------:| ------------ |  
|  404 | 1400  |  not_found  |  Shortlink ID not found |  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.get_shortlink_hits(short_id, async_req=True)
        >>> result = thread.get()

        Args:
            short_id (str): Identifier of the shortlink

        Keyword Args:
            short_response (bool): If set to true, it will return the full `info` object and an empty `data` object. [optional] if omitted the server will use the default value of False
            limit (int): A limit on the number of objects to be returned. [optional] if omitted the server will use the default value of 500
            next (str): The next token used to retrieve additional data. [optional]
            previous (str): The previous token used to retrieve additional data. [optional]
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
            ShortlinkDetailsResponse
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
        kwargs['short_id'] = \
            short_id
        return self.get_shortlink_hits_endpoint.call_with_http_info(**kwargs)

    def get_shortlinks_list(
        self,
        **kwargs
    ):
        """Get shortlinks list  # noqa: E501

        Retrieves the list of existing shortlinks. The shortlinks are returned sorted by creation date, with the most recent shortlink appearing first.    If no shortlinks are available, an empty data object is returned.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.get_shortlinks_list(async_req=True)
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
            ShortlinksListResponse
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
        return self.get_shortlinks_list_endpoint.call_with_http_info(**kwargs)

    def update_shortlink(
        self,
        short_id,
        shortlink_update_request,
        **kwargs
    ):
        """Update shortlink  # noqa: E501

        Updates the specified shortlink by setting the values of the parameters passed. Any parameters not provided will be left unchanged.    Returns HTTP `204 No content` if the parameters provided did not update the contact because the data was already the same.    
### Errors for PATCH `/shortlinks/{shortId} `  
| HTTP code  | Error code  | Type  | Description  |  
|:------------:|:------------:|:------------:| ------------ |  
|  404 | 1400  |  not_found  |  Shortlink ID not found |  

|  400 | 1401  |  invalid_param  |  The URL is empty or parameter `url` not set |  

|  400 | 1402  |  invalid_param  |  The URL provided is invalid |  

|  400 | 1404  |  invalid_param  |  The parameter `name` is invalid (min 3, max 25 characters) |  

|  400 | 1406  |  invalid_param  |  At least one parameter required (name, url) |  

|  400 | 1407  |  duplicate_value  |  You already have a shortlink with this name |  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.update_shortlink(short_id, shortlink_update_request, async_req=True)
        >>> result = thread.get()

        Args:
            short_id (str): Identifier of the shortlink
            shortlink_update_request (ShortlinkUpdateRequest): 

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
            ShortlinkUpdateResponse
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
        kwargs['short_id'] = \
            short_id
        kwargs['shortlink_update_request'] = \
            shortlink_update_request
        return self.update_shortlink_endpoint.call_with_http_info(**kwargs)

