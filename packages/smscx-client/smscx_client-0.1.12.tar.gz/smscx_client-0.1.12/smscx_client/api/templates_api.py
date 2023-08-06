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
from smscx_client.model.template_details_response import TemplateDetailsResponse
from smscx_client.model.templates_delete_response import TemplatesDeleteResponse
from smscx_client.model.templates_list_response import TemplatesListResponse
from smscx_client.model.templates_new_request import TemplatesNewRequest
from smscx_client.model.templates_new_response import TemplatesNewResponse
from smscx_client.model.templates_update_request import TemplatesUpdateRequest
from smscx_client.model.templates_update_response import TemplatesUpdateResponse


class TemplatesApi(object):
    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client
        self.create_template_endpoint = _Endpoint(
            settings={
                'response_type': (TemplatesNewResponse,),
                'auth': [
                    'ApiKeyAuth',
                    'BearerAuth'
                ],
                'endpoint_path': '/templates',
                'operation_id': 'create_template',
                'http_method': 'POST',
                'servers': None,
            },
            params_map={
                'all': [
                    'templates_new_request',
                ],
                'required': [
                    'templates_new_request',
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
                    'templates_new_request':
                        (TemplatesNewRequest,),
                },
                'attribute_map': {
                },
                'location_map': {
                    'templates_new_request': 'body',
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
        self.delete_template_endpoint = _Endpoint(
            settings={
                'response_type': (TemplatesDeleteResponse,),
                'auth': [
                    'ApiKeyAuth',
                    'BearerAuth'
                ],
                'endpoint_path': '/templates/{templateId}',
                'operation_id': 'delete_template',
                'http_method': 'DELETE',
                'servers': None,
            },
            params_map={
                'all': [
                    'template_id',
                ],
                'required': [
                    'template_id',
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
                    'template_id':
                        (int,),
                },
                'attribute_map': {
                    'template_id': 'templateId',
                },
                'location_map': {
                    'template_id': 'path',
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
        self.get_template_endpoint = _Endpoint(
            settings={
                'response_type': (TemplateDetailsResponse,),
                'auth': [
                    'ApiKeyAuth',
                    'BearerAuth'
                ],
                'endpoint_path': '/templates/{templateId}',
                'operation_id': 'get_template',
                'http_method': 'GET',
                'servers': None,
            },
            params_map={
                'all': [
                    'template_id',
                ],
                'required': [
                    'template_id',
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
                    'template_id':
                        (int,),
                },
                'attribute_map': {
                    'template_id': 'templateId',
                },
                'location_map': {
                    'template_id': 'path',
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
        self.get_templates_list_endpoint = _Endpoint(
            settings={
                'response_type': (TemplatesListResponse,),
                'auth': [
                    'ApiKeyAuth',
                    'BearerAuth'
                ],
                'endpoint_path': '/templates',
                'operation_id': 'get_templates_list',
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
        self.update_template_endpoint = _Endpoint(
            settings={
                'response_type': (TemplatesUpdateResponse,),
                'auth': [
                    'ApiKeyAuth',
                    'BearerAuth'
                ],
                'endpoint_path': '/templates/{templateId}',
                'operation_id': 'update_template',
                'http_method': 'PATCH',
                'servers': None,
            },
            params_map={
                'all': [
                    'template_id',
                    'templates_update_request',
                ],
                'required': [
                    'template_id',
                    'templates_update_request',
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
                    'template_id':
                        (int,),
                    'templates_update_request':
                        (TemplatesUpdateRequest,),
                },
                'attribute_map': {
                    'template_id': 'templateId',
                },
                'location_map': {
                    'template_id': 'path',
                    'templates_update_request': 'body',
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

    def create_template(
        self,
        templates_new_request,
        **kwargs
    ):
        """Create template  # noqa: E501

        Creates a new template.    
### Errors for POST `/templates`  
| HTTP code  | Error code  | Type  | Description  |  
|:------------:|:------------:|:------------:| ------------ |  
|  400 |  1801  |  invalid_param  |  The text message is empty or parameter `text` not set |  

|  400 |  1802  |  invalid_param  |  The parameter `text` is invalid |  

|  400 | 1803  |  invalid_param  |  The name provided is invalid (min 3, max 100 characters) |  

|  400 | 1806  |  invalid_param  |  The parameter `channel` is not valid. Allowed values: |  

|  400 | 1805  |  duplicate_value  |  You already have a template with this name  |    

|  400 | 1811  |  invalid_param  |  Text message too long (max 1000 characters)  |    

|  400 | 1808  |  invalid_param  |  Button caption is too long (min 1, max. 30 characters)  |    

|  400 | 1809  |  invalid_param  |  Invalid target URL |  

|  400 | 1810  |  invalid_param  |  Invalid image URL  |  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.create_template(templates_new_request, async_req=True)
        >>> result = thread.get()

        Args:
            templates_new_request (TemplatesNewRequest): 

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
            TemplatesNewResponse
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
        kwargs['templates_new_request'] = \
            templates_new_request
        return self.create_template_endpoint.call_with_http_info(**kwargs)

    def delete_template(
        self,
        template_id,
        **kwargs
    ):
        """Delete template  # noqa: E501

        Deletes a template if a valid identifier was provided.    
### Errors for DELETE `/templates/{templateId}`  
| HTTP code  | Error code  | Type  | Description  |  
|:------------:|:------------:|:------------:| ------------ |  
|  404 | 1800  |  not_found  |  Template ID not found |  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.delete_template(template_id, async_req=True)
        >>> result = thread.get()

        Args:
            template_id (int): Identifier of the template

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
            TemplatesDeleteResponse
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
        kwargs['template_id'] = \
            template_id
        return self.delete_template_endpoint.call_with_http_info(**kwargs)

    def get_template(
        self,
        template_id,
        **kwargs
    ):
        """Get template  # noqa: E501

        Retrieves the details of a template if a valid identifier was provided.    
### Errors for GET `/templates/{templateId}`  
| HTTP code  | Error code  | Type  | Description  |  
|:------------:|:------------:|:------------:| ------------ |  
|  404 | 1800  |  not_found  |  Template ID not found |  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.get_template(template_id, async_req=True)
        >>> result = thread.get()

        Args:
            template_id (int): Identifier of the template

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
            TemplateDetailsResponse
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
        kwargs['template_id'] = \
            template_id
        return self.get_template_endpoint.call_with_http_info(**kwargs)

    def get_templates_list(
        self,
        **kwargs
    ):
        """Get templates list  # noqa: E501

        Retrieves the list of existing templates. The templates are returned sorted by creation date, with the most recent templates appearing first.    If no templates are available, an empty data object is returned.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.get_templates_list(async_req=True)
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
            TemplatesListResponse
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
        return self.get_templates_list_endpoint.call_with_http_info(**kwargs)

    def update_template(
        self,
        template_id,
        templates_update_request,
        **kwargs
    ):
        """Update template  # noqa: E501

        Updates the specified template by setting the values of the parameters passed. Any parameters not provided will be left unchanged.    Returns HTTP `204 No content` if the parameters provided did not update the template because the data was already the same.    
### Errors for PATCH `/templates/{templateId}`  
| HTTP code  | Error code  | Type  | Description  |  
|:------------:|:------------:|:------------:| ------------ |  
|  404 | 1800  |  not_found  |  Template ID not found |  

|  400 | 1802  |  invalid_param  |  The parameter `text` is invalid |  

|  400 | 1803  |  invalid_param  |  The name provided is invalid (min 3, max 100 characters) |  

|  400 | 1804  |  invalid_param  |  At least one parameter required (name, text) |  

|  400 | 1811  |  invalid_param  |  Text message too long (max 1000 characters) |  
|  403 | 1812  |  access_denied  |  Template is locked for editing |  

|  400 | 1810  |  invalid_param  |  Invalid image URL |  

|  400 | 1808  |  invalid_param  |  Button caption is too long (min 1, max. 30 characters) |  

|  400 | 1809  |  invalid_param  |  Invalid target URL |  

|  400 | 1805  |  duplicate_value  |  You already have a template with this name |  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.update_template(template_id, templates_update_request, async_req=True)
        >>> result = thread.get()

        Args:
            template_id (int): Identifier of the template
            templates_update_request (TemplatesUpdateRequest): 

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
            TemplatesUpdateResponse
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
        kwargs['template_id'] = \
            template_id
        kwargs['templates_update_request'] = \
            templates_update_request
        return self.update_template_endpoint.call_with_http_info(**kwargs)

