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
from smscx_client.model.add_contacts_to_group400_response import AddContactsToGroup400Response
from smscx_client.model.add_contacts_to_group_request import AddContactsToGroupRequest
from smscx_client.model.add_contacts_to_group_with_fields_request import AddContactsToGroupWithFieldsRequest
from smscx_client.model.add_contacts_to_group_response import AddContactsToGroupResponse
from smscx_client.model.delete_contact import DeleteContact
from smscx_client.model.delete_group import DeleteGroup
from smscx_client.model.group_details_response import GroupDetailsResponse
from smscx_client.model.group_response import GroupResponse
from smscx_client.model.groups_list import GroupsList
from smscx_client.model.model400_invalid_param import Model400InvalidParam
from smscx_client.model.model401_unauthorized import Model401Unauthorized
from smscx_client.model.model403_insufficient_scope import Model403InsufficientScope
from smscx_client.model.model403_no_coverage import Model403NoCoverage
from smscx_client.model.model404_not_found import Model404NotFound
from smscx_client.model.model500_server_error import Model500ServerError
from smscx_client.model.new_group_request import NewGroupRequest
from smscx_client.model.new_group_response import NewGroupResponse
from smscx_client.model.update_number_request import UpdateNumberRequest
from smscx_client.model.update_number_response import UpdateNumberResponse


class GroupsApi(object):
    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client
        self.add_contacts_to_group_endpoint = _Endpoint(
            settings={
                'response_type': (AddContactsToGroupResponse,),
                'auth': [
                    'ApiKeyAuth',
                    'BearerAuth'
                ],
                'endpoint_path': '/groups/{groupId}',
                'operation_id': 'add_contacts_to_group',
                'http_method': 'POST',
                'servers': None,
            },
            params_map={
                'all': [
                    'group_id',
                    'add_contacts_to_group_request',
                ],
                'required': [
                    'group_id',
                    'add_contacts_to_group_request',
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
                    'group_id':
                        (int,),
                    'add_contacts_to_group_request':
                        (AddContactsToGroupRequest,),
                },
                'attribute_map': {
                    'group_id': 'groupId',
                },
                'location_map': {
                    'group_id': 'path',
                    'add_contacts_to_group_request': 'body',
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
        self.add_contacts_to_group_with_fields_endpoint = _Endpoint(
            settings={
                'response_type': (AddContactsToGroupResponse,),
                'auth': [
                    'ApiKeyAuth',
                    'BearerAuth'
                ],
                'endpoint_path': '/groups/{groupId}',
                'operation_id': 'add_contacts_to_group',
                'http_method': 'POST',
                'servers': None,
            },
            params_map={
                'all': [
                    'group_id',
                    'add_contacts_to_group_with_fields_request',
                ],
                'required': [
                    'group_id',
                    'add_contacts_to_group_with_fields_request',
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
                    'group_id':
                        (int,),
                    'add_contacts_to_group_with_fields_request':
                        (AddContactsToGroupWithFieldsRequest,),
                },
                'attribute_map': {
                    'group_id': 'groupId',
                },
                'location_map': {
                    'group_id': 'path',
                    'add_contacts_to_group_with_fields_request': 'body',
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
        self.create_group_endpoint = _Endpoint(
            settings={
                'response_type': (NewGroupResponse,),
                'auth': [
                    'ApiKeyAuth',
                    'BearerAuth'
                ],
                'endpoint_path': '/groups',
                'operation_id': 'create_group',
                'http_method': 'POST',
                'servers': None,
            },
            params_map={
                'all': [
                    'new_group_request',
                ],
                'required': [
                    'new_group_request',
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
                    'new_group_request':
                        (NewGroupRequest,),
                },
                'attribute_map': {
                },
                'location_map': {
                    'new_group_request': 'body',
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
        self.delete_contact_from_group_endpoint = _Endpoint(
            settings={
                'response_type': (DeleteContact,),
                'auth': [
                    'ApiKeyAuth',
                    'BearerAuth'
                ],
                'endpoint_path': '/groups/{groupId}/{phoneNumberId}',
                'operation_id': 'delete_contact_from_group',
                'http_method': 'DELETE',
                'servers': None,
            },
            params_map={
                'all': [
                    'group_id',
                    'phone_number_id',
                ],
                'required': [
                    'group_id',
                    'phone_number_id',
                ],
                'nullable': [
                ],
                'enum': [
                ],
                'validation': [
                    'phone_number_id',
                ]
            },
            root_map={
                'validations': {
                    ('phone_number_id',): {
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
                    'group_id':
                        (int,),
                    'phone_number_id':
                        (str,),
                },
                'attribute_map': {
                    'group_id': 'groupId',
                    'phone_number_id': 'phoneNumberId',
                },
                'location_map': {
                    'group_id': 'path',
                    'phone_number_id': 'path',
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
        self.delete_group_endpoint = _Endpoint(
            settings={
                'response_type': (DeleteGroup,),
                'auth': [
                    'ApiKeyAuth',
                    'BearerAuth'
                ],
                'endpoint_path': '/groups/{groupId}',
                'operation_id': 'delete_group',
                'http_method': 'DELETE',
                'servers': None,
            },
            params_map={
                'all': [
                    'group_id',
                ],
                'required': [
                    'group_id',
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
                    'group_id':
                        (int,),
                },
                'attribute_map': {
                    'group_id': 'groupId',
                },
                'location_map': {
                    'group_id': 'path',
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
        self.empty_group_endpoint = _Endpoint(
            settings={
                'response_type': (GroupResponse,),
                'auth': [
                    'ApiKeyAuth',
                    'BearerAuth'
                ],
                'endpoint_path': '/groups/{groupId}/empty',
                'operation_id': 'empty_group',
                'http_method': 'GET',
                'servers': None,
            },
            params_map={
                'all': [
                    'group_id',
                ],
                'required': [
                    'group_id',
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
                    'group_id':
                        (int,),
                },
                'attribute_map': {
                    'group_id': 'groupId',
                },
                'location_map': {
                    'group_id': 'path',
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
        self.export_group_to_csv_endpoint = _Endpoint(
            settings={
                'response_type': (str,),
                'auth': [
                    'ApiKeyAuth',
                    'BearerAuth'
                ],
                'endpoint_path': '/groups/{groupId}/csv',
                'operation_id': 'export_group_to_csv',
                'http_method': 'GET',
                'servers': None,
            },
            params_map={
                'all': [
                    'group_id',
                ],
                'required': [
                    'group_id',
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
                    'group_id':
                        (int,),
                },
                'attribute_map': {
                    'group_id': 'groupId',
                },
                'location_map': {
                    'group_id': 'path',
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
        self.export_group_to_xlsx_endpoint = _Endpoint(
            settings={
                'response_type': (file_type,),
                'auth': [
                    'ApiKeyAuth',
                    'BearerAuth'
                ],
                'endpoint_path': '/groups/{groupId}/xlsx',
                'operation_id': 'export_group_to_xlsx',
                'http_method': 'GET',
                'servers': None,
            },
            params_map={
                'all': [
                    'group_id',
                ],
                'required': [
                    'group_id',
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
                    'group_id':
                        (int,),
                },
                'attribute_map': {
                    'group_id': 'groupId',
                },
                'location_map': {
                    'group_id': 'path',
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
        self.get_group_details_endpoint = _Endpoint(
            settings={
                'response_type': (GroupDetailsResponse,),
                'auth': [
                    'ApiKeyAuth',
                    'BearerAuth'
                ],
                'endpoint_path': '/groups/{groupId}',
                'operation_id': 'get_group_details',
                'http_method': 'GET',
                'servers': None,
            },
            params_map={
                'all': [
                    'group_id',
                    'short_response',
                    'limit',
                    'next',
                    'previous',
                ],
                'required': [
                    'group_id',
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
                    'group_id':
                        (int,),
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
                    'group_id': 'groupId',
                    'short_response': 'short_response',
                    'limit': 'limit',
                    'next': 'next',
                    'previous': 'previous',
                },
                'location_map': {
                    'group_id': 'path',
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
        self.get_groups_list_endpoint = _Endpoint(
            settings={
                'response_type': (GroupsList,),
                'auth': [
                    'ApiKeyAuth',
                    'BearerAuth'
                ],
                'endpoint_path': '/groups',
                'operation_id': 'get_groups_list',
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
        self.update_contact_from_group_endpoint = _Endpoint(
            settings={
                'response_type': (UpdateNumberResponse,),
                'auth': [
                    'ApiKeyAuth',
                    'BearerAuth'
                ],
                'endpoint_path': '/groups/{groupId}/{phoneNumberId}',
                'operation_id': 'update_contact_from_group',
                'http_method': 'PATCH',
                'servers': None,
            },
            params_map={
                'all': [
                    'group_id',
                    'phone_number_id',
                    'update_number_request',
                ],
                'required': [
                    'group_id',
                    'phone_number_id',
                    'update_number_request',
                ],
                'nullable': [
                ],
                'enum': [
                ],
                'validation': [
                    'phone_number_id',
                ]
            },
            root_map={
                'validations': {
                    ('phone_number_id',): {
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
                    'group_id':
                        (int,),
                    'phone_number_id':
                        (str,),
                    'update_number_request':
                        (UpdateNumberRequest,),
                },
                'attribute_map': {
                    'group_id': 'groupId',
                    'phone_number_id': 'phoneNumberId',
                },
                'location_map': {
                    'group_id': 'path',
                    'phone_number_id': 'path',
                    'update_number_request': 'body',
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

    def add_contacts_to_group(
        self,
        group_id,
        add_contacts_to_group_request,
        **kwargs
    ):
        """Add contacts to group  # noqa: E501

        Add contacts to a group if a valid identifier was provided.    
### Errors for POST `/groups/{groupId}`  
| HTTP code  | Error code  | Type  | Description  |  
|:------------:|:------------:|:------------:| ------------ |  
|  400 | 1203  |  invalid_param  | The parameter `phoneNumbers` is empty or not set |  

|  400 | 1208  |  invalid_param  |  The parameter `phoneNumbers` must be an array of phone numbers  |    

|  400 | 1207  |  invalid_param  | The phone number provided is not valid |  

|  400 | 1210  |  invalid_param  | The phone numbers provided are invalid |  
|  404 | 1200  |  not_found  | Group ID not found |  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.add_contacts_to_group(group_id, add_contacts_to_group_request, async_req=True)
        >>> result = thread.get()

        Args:
            group_id (int): Identifier of a group of contacts
            add_contacts_to_group_request (AddContactsToGroupRequest): 

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
            AddContactsToGroupResponse
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
        kwargs['group_id'] = \
            group_id
        kwargs['add_contacts_to_group_request'] = \
            add_contacts_to_group_request
        return self.add_contacts_to_group_endpoint.call_with_http_info(**kwargs)

    def add_contacts_to_group_with_fields(
        self,
        group_id,
        add_contacts_to_group_with_fields_request,
        **kwargs
    ):
        """Add contacts to group  # noqa: E501

        Add contacts to a group if a valid identifier was provided.    
### Errors for POST `/groups/{groupId}`  
| HTTP code  | Error code  | Type  | Description  |  
|:------------:|:------------:|:------------:| ------------ |  
|  400 | 1203  |  invalid_param  | The parameter `phoneNumbers` is empty or not set |  

|  400 | 1208  |  invalid_param  |  The parameter `phoneNumbers` must be an array of phone numbers  |    

|  400 | 1207  |  invalid_param  | The phone number provided is not valid |  

|  400 | 1210  |  invalid_param  | The phone numbers provided are invalid |  
|  404 | 1200  |  not_found  | Group ID not found |  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.add_contacts_to_group(group_id, add_contacts_to_group_request, async_req=True)
        >>> result = thread.get()

        Args:
            group_id (int): Identifier of a group of contacts
            add_contacts_to_group_request (AddContactsToGroupRequest): 

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
            AddContactsToGroupResponse
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
        kwargs['group_id'] = \
            group_id
        kwargs['add_contacts_to_group_with_fields_request'] = \
            add_contacts_to_group_with_fields_request
        return self.add_contacts_to_group_with_fields_endpoint.call_with_http_info(**kwargs)

    def create_group(
        self,
        new_group_request,
        **kwargs
    ):
        """Create new group  # noqa: E501

        Creates a new group.      
### Errors for POST `/groups`  
| HTTP code  | Error code  | Type  | Description  |  
|:------------:|:------------:|:------------:| ------------ |  
|  400 | 1204  |  invalid_param  | The name is empty or parameter `name` not set |  

|  400 | 1206  |  invalid_param  | The name provided is invalid (min 3, max 60 characters) |  

|  400 | 1211  |  duplicate_value  | You already have a group with this name |  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.create_group(new_group_request, async_req=True)
        >>> result = thread.get()

        Args:
            new_group_request (NewGroupRequest): 

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
            NewGroupResponse
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
        kwargs['new_group_request'] = \
            new_group_request
        return self.create_group_endpoint.call_with_http_info(**kwargs)

    def delete_contact_from_group(
        self,
        group_id,
        phone_number_id,
        **kwargs
    ):
        """Delete contact from group  # noqa: E501

        Deletes a contact from a group if a valid group identifier was provided.    
### Errors for DELETE `/groups/{groupId}/{phoneNumberId}`  
| HTTP code  | Error code  | Type  | Description  |  
|:------------:|:------------:|:------------:| ------------ |  
|  404 | 1200  |  not_found  | Group ID not found |  
|  404 | 1202  |  not_found  | Phone number ID not found |  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.delete_contact_from_group(group_id, phone_number_id, async_req=True)
        >>> result = thread.get()

        Args:
            group_id (int): Identifier of a group of contacts
            phone_number_id (str): Identifier of the phone number

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
            DeleteContact
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
        kwargs['group_id'] = \
            group_id
        kwargs['phone_number_id'] = \
            phone_number_id
        return self.delete_contact_from_group_endpoint.call_with_http_info(**kwargs)

    def delete_group(
        self,
        group_id,
        **kwargs
    ):
        """Delete group  # noqa: E501

        Deletes a group and all the contacts in the group    
### Errors for DELETE `/groups/{groupId}`  
| HTTP code  | Error code  | Type  | Description  |  
|:------------:|:------------:|:------------:| ------------ |  
|  404 | 1200  |  not_found  | Group ID not found |  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.delete_group(group_id, async_req=True)
        >>> result = thread.get()

        Args:
            group_id (int): Identifier of a group of contacts

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
            DeleteGroup
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
        kwargs['group_id'] = \
            group_id
        return self.delete_group_endpoint.call_with_http_info(**kwargs)

    def empty_group(
        self,
        group_id,
        **kwargs
    ):
        """Empty group  # noqa: E501

        Deletes all the contacts in a group.        Returns HTTP `204 No content` if group is already empty.    
### Errors for GET `/groups/{groupId}/empty`  
| HTTP code  | Error code  | Type  | Description  |  
|:------------:|:------------:|:------------:| ------------ |  
|  404 | 1200  |  not_found  | Group ID not found |  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.empty_group(group_id, async_req=True)
        >>> result = thread.get()

        Args:
            group_id (int): Identifier of a group of contacts

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
            GroupResponse
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
        kwargs['group_id'] = \
            group_id
        return self.empty_group_endpoint.call_with_http_info(**kwargs)

    def export_group_to_csv(
        self,
        group_id,
        **kwargs
    ):
        """Export group to CSV  # noqa: E501

        Exports the contacts from a group to a CSV file.    If the group is empty, an empty CSV file is returned (with first line headers).    
### Errors for GET `/groups/{groupId}/csv`  
| HTTP code  | Error code  | Type  | Description  |  
|:------------:|:------------:|:------------:| ------------ |  
|  404 | 1200  |  not_found  | Group ID not found |  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.export_group_to_csv(group_id, async_req=True)
        >>> result = thread.get()

        Args:
            group_id (int): Identifier of a group of contacts

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
        kwargs['group_id'] = \
            group_id
        return self.export_group_to_csv_endpoint.call_with_http_info(**kwargs)

    def export_group_to_xlsx(
        self,
        group_id,
        **kwargs
    ):
        """Export group to XLSX  # noqa: E501

        Exports the contacts from a group to a XLSX file (Excel).    If the group is empty, an empty XLSX file is returned (with first line headers).    
### Errors for GET `/groups/{groupId}/xlsx`  
| HTTP code  | Error code  | Type  | Description  |  
|:------------:|:------------:|:------------:| ------------ |  
|  404 | 1200  |  not_found  | Group ID not found |  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.export_group_to_xlsx(group_id, async_req=True)
        >>> result = thread.get()

        Args:
            group_id (int): Identifier of a group of contacts

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
        kwargs['group_id'] = \
            group_id
        return self.export_group_to_xlsx_endpoint.call_with_http_info(**kwargs)

    def get_group_details(
        self,
        group_id,
        **kwargs
    ):
        """Get group details  # noqa: E501

        Retrieves the details of a group if a valid identifier was provided.      
### Errors for GET `/groups/{groupId}`  
| HTTP code  | Error code  | Type  | Description  |  
|:------------:|:------------:|:------------:| ------------ |  
|  404 | 1200  |  not_found  | Group ID not found |  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.get_group_details(group_id, async_req=True)
        >>> result = thread.get()

        Args:
            group_id (int): Identifier of a group of contacts

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
            GroupDetailsResponse
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
        kwargs['group_id'] = \
            group_id
        return self.get_group_details_endpoint.call_with_http_info(**kwargs)

    def get_groups_list(
        self,
        **kwargs
    ):
        """Get list of groups  # noqa: E501

        Retrieves the list of existing groups of contacts. The groups are returned sorted by creation date, with the most recent group appearing first.    If no groups are available, an empty data object is returned.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.get_groups_list(async_req=True)
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
            GroupsList
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
        return self.get_groups_list_endpoint.call_with_http_info(**kwargs)

    def update_contact_from_group(
        self,
        group_id,
        phone_number_id,
        update_number_request,
        **kwargs
    ):
        """Update contact from group  # noqa: E501

        Updates the specified contact by setting the values of the parameters passed. Any parameters not provided will be left unchanged.    Returns HTTP `204 No content` if the parameters provided did not update the contact because the data was already the same.    
### Errors for PATCH `/groups/{groupId}/{phoneNumberId}`  
| HTTP code  | Error code  | Type  | Description  |  
|:------------:|:------------:|:------------:| ------------ |  
|  404 | 1202  |  not_found  | Phone number ID not found |  

|  400 | 1213  |  invalid_param  | At least one parameter required (phoneNumber, firstName, lastName, email, field1, field2, field3, field4, field5, customFields) |  

|  400 | 1215  |  duplicate_value  | The phone number already exists |  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.update_contact_from_group(group_id, phone_number_id, update_number_request, async_req=True)
        >>> result = thread.get()

        Args:
            group_id (int): Identifier of a group of contacts
            phone_number_id (str): Identifier of the phone number
            update_number_request (UpdateNumberRequest): 

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
            UpdateNumberResponse
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
        kwargs['group_id'] = \
            group_id
        kwargs['phone_number_id'] = \
            phone_number_id
        kwargs['update_number_request'] = \
            update_number_request
        return self.update_contact_from_group_endpoint.call_with_http_info(**kwargs)

