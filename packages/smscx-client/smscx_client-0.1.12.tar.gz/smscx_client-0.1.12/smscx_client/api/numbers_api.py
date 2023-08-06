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
from smscx_client.model.cancel_rent_response import CancelRentResponse
from smscx_client.model.data_number_lookup import DataNumberLookup
from smscx_client.model.get_inbound_sms_response import GetInboundSMSResponse
from smscx_client.model.get_rent_status_response import GetRentStatusResponse
from smscx_client.model.model400_invalid_param import Model400InvalidParam
from smscx_client.model.model401_unauthorized import Model401Unauthorized
from smscx_client.model.model403_insufficient_scope import Model403InsufficientScope
from smscx_client.model.model404_not_found import Model404NotFound
from smscx_client.model.model500_server_error import Model500ServerError
from smscx_client.model.number_lookup_response import NumberLookupResponse
from smscx_client.model.number_validate_response import NumberValidateResponse
from smscx_client.model.numbers_bulk_lookup_result import NumbersBulkLookupResult
from smscx_client.model.numbers_lookup_request import NumbersLookupRequest
from smscx_client.model.numbers_lookup_response import NumbersLookupResponse
from smscx_client.model.numbers_validate_request import NumbersValidateRequest
from smscx_client.model.numbers_validate_response import NumbersValidateResponse
from smscx_client.model.renew_rent_request import RenewRentRequest
from smscx_client.model.rent_number_request import RentNumberRequest
from smscx_client.model.rent_number_response import RentNumberResponse
from smscx_client.model.rent_numbers_response import RentNumbersResponse
from smscx_client.model.rented_numbers_response import RentedNumbersResponse


class NumbersApi(object):
    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client
        self.cancel_rent_endpoint = _Endpoint(
            settings={
                'response_type': (CancelRentResponse,),
                'auth': [
                    'ApiKeyAuth',
                    'BearerAuth'
                ],
                'endpoint_path': '/numbers/rent/{rentId}',
                'operation_id': 'cancel_rent',
                'http_method': 'DELETE',
                'servers': None,
            },
            params_map={
                'all': [
                    'rent_id',
                ],
                'required': [
                    'rent_id',
                ],
                'nullable': [
                ],
                'enum': [
                ],
                'validation': [
                    'rent_id',
                ]
            },
            root_map={
                'validations': {
                    ('rent_id',): {
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
                    'rent_id':
                        (str,),
                },
                'attribute_map': {
                    'rent_id': 'rentId',
                },
                'location_map': {
                    'rent_id': 'path',
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
        self.get_available_numbers_endpoint = _Endpoint(
            settings={
                'response_type': (RentNumbersResponse,),
                'auth': [
                    'ApiKeyAuth',
                    'BearerAuth'
                ],
                'endpoint_path': '/numbers/rent/available/{countryIso}',
                'operation_id': 'get_available_numbers',
                'http_method': 'GET',
                'servers': None,
            },
            params_map={
                'all': [
                    'country_iso',
                ],
                'required': [
                    'country_iso',
                ],
                'nullable': [
                ],
                'enum': [
                ],
                'validation': [
                    'country_iso',
                ]
            },
            root_map={
                'validations': {
                    ('country_iso',): {
                        'max_length': 2,
                        'min_length': 2,
                    },
                },
                'allowed_values': {
                },
                'api_types': {
                    'country_iso':
                        (str,),
                },
                'attribute_map': {
                    'country_iso': 'countryIso',
                },
                'location_map': {
                    'country_iso': 'path',
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
        self.get_bulk_lookup_status_endpoint = _Endpoint(
            settings={
                'response_type': (NumbersBulkLookupResult,),
                'auth': [
                    'ApiKeyAuth',
                    'BearerAuth'
                ],
                'endpoint_path': '/numbers/lookup/lookupBulkId/{lookupBulkId}',
                'operation_id': 'get_bulk_lookup_status',
                'http_method': 'GET',
                'servers': None,
            },
            params_map={
                'all': [
                    'lookup_bulk_id',
                ],
                'required': [
                    'lookup_bulk_id',
                ],
                'nullable': [
                ],
                'enum': [
                ],
                'validation': [
                    'lookup_bulk_id',
                ]
            },
            root_map={
                'validations': {
                    ('lookup_bulk_id',): {
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
                    'lookup_bulk_id':
                        (str,),
                },
                'attribute_map': {
                    'lookup_bulk_id': 'lookupBulkId',
                },
                'location_map': {
                    'lookup_bulk_id': 'path',
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
        self.get_inbound_sms_endpoint = _Endpoint(
            settings={
                'response_type': (GetInboundSMSResponse,),
                'auth': [
                    'ApiKeyAuth',
                    'BearerAuth'
                ],
                'endpoint_path': '/numbers/rent/{rentId}/inbound',
                'operation_id': 'get_inbound_sms',
                'http_method': 'GET',
                'servers': None,
            },
            params_map={
                'all': [
                    'rent_id',
                ],
                'required': [
                    'rent_id',
                ],
                'nullable': [
                ],
                'enum': [
                ],
                'validation': [
                    'rent_id',
                ]
            },
            root_map={
                'validations': {
                    ('rent_id',): {
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
                    'rent_id':
                        (str,),
                },
                'attribute_map': {
                    'rent_id': 'rentId',
                },
                'location_map': {
                    'rent_id': 'path',
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
        self.get_rent_status_endpoint = _Endpoint(
            settings={
                'response_type': (GetRentStatusResponse,),
                'auth': [
                    'ApiKeyAuth',
                    'BearerAuth'
                ],
                'endpoint_path': '/numbers/rent/{rentId}',
                'operation_id': 'get_rent_status',
                'http_method': 'GET',
                'servers': None,
            },
            params_map={
                'all': [
                    'rent_id',
                ],
                'required': [
                    'rent_id',
                ],
                'nullable': [
                ],
                'enum': [
                ],
                'validation': [
                    'rent_id',
                ]
            },
            root_map={
                'validations': {
                    ('rent_id',): {
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
                    'rent_id':
                        (str,),
                },
                'attribute_map': {
                    'rent_id': 'rentId',
                },
                'location_map': {
                    'rent_id': 'path',
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
        self.get_rented_numbers_endpoint = _Endpoint(
            settings={
                'response_type': (RentedNumbersResponse,),
                'auth': [
                    'ApiKeyAuth',
                    'BearerAuth'
                ],
                'endpoint_path': '/numbers/rent',
                'operation_id': 'get_rented_numbers',
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
        self.get_single_lookup_status_endpoint = _Endpoint(
            settings={
                'response_type': (DataNumberLookup,),
                'auth': [
                    'ApiKeyAuth',
                    'BearerAuth'
                ],
                'endpoint_path': '/numbers/lookup/lookupId/{lookupId}',
                'operation_id': 'get_single_lookup_status',
                'http_method': 'GET',
                'servers': None,
            },
            params_map={
                'all': [
                    'lookup_id',
                ],
                'required': [
                    'lookup_id',
                ],
                'nullable': [
                ],
                'enum': [
                ],
                'validation': [
                    'lookup_id',
                ]
            },
            root_map={
                'validations': {
                    ('lookup_id',): {
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
                    'lookup_id':
                        (str,),
                },
                'attribute_map': {
                    'lookup_id': 'lookupId',
                },
                'location_map': {
                    'lookup_id': 'path',
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
        self.lookup_number_endpoint = _Endpoint(
            settings={
                'response_type': (NumberLookupResponse,),
                'auth': [
                    'ApiKeyAuth',
                    'BearerAuth'
                ],
                'endpoint_path': '/numbers/lookup/{phoneNumber}',
                'operation_id': 'lookup_number',
                'http_method': 'GET',
                'servers': None,
            },
            params_map={
                'all': [
                    'phone_number',
                ],
                'required': [
                    'phone_number',
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
                    'phone_number':
                        (str,),
                },
                'attribute_map': {
                    'phone_number': 'phoneNumber',
                },
                'location_map': {
                    'phone_number': 'path',
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
        self.lookup_numbers_endpoint = _Endpoint(
            settings={
                'response_type': (NumbersLookupResponse,),
                'auth': [
                    'ApiKeyAuth',
                    'BearerAuth'
                ],
                'endpoint_path': '/numbers/lookup',
                'operation_id': 'lookup_numbers',
                'http_method': 'POST',
                'servers': None,
            },
            params_map={
                'all': [
                    'numbers_lookup_request',
                ],
                'required': [
                    'numbers_lookup_request',
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
                    'numbers_lookup_request':
                        (NumbersLookupRequest,),
                },
                'attribute_map': {
                },
                'location_map': {
                    'numbers_lookup_request': 'body',
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
        self.renew_rent_endpoint = _Endpoint(
            settings={
                'response_type': (RentNumberResponse,),
                'auth': [
                    'ApiKeyAuth',
                    'BearerAuth'
                ],
                'endpoint_path': '/numbers/rent/{rentId}',
                'operation_id': 'renew_rent',
                'http_method': 'PATCH',
                'servers': None,
            },
            params_map={
                'all': [
                    'rent_id',
                    'renew_rent_request',
                ],
                'required': [
                    'rent_id',
                    'renew_rent_request',
                ],
                'nullable': [
                ],
                'enum': [
                ],
                'validation': [
                    'rent_id',
                ]
            },
            root_map={
                'validations': {
                    ('rent_id',): {
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
                    'rent_id':
                        (str,),
                    'renew_rent_request':
                        (RenewRentRequest,),
                },
                'attribute_map': {
                    'rent_id': 'rentId',
                },
                'location_map': {
                    'rent_id': 'path',
                    'renew_rent_request': 'body',
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
        self.rent_number_endpoint = _Endpoint(
            settings={
                'response_type': (RentNumberResponse,),
                'auth': [
                    'ApiKeyAuth',
                    'BearerAuth'
                ],
                'endpoint_path': '/numbers/rent',
                'operation_id': 'rent_number',
                'http_method': 'POST',
                'servers': None,
            },
            params_map={
                'all': [
                    'rent_number_request',
                ],
                'required': [
                    'rent_number_request',
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
                    'rent_number_request':
                        (RentNumberRequest,),
                },
                'attribute_map': {
                },
                'location_map': {
                    'rent_number_request': 'body',
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
        self.validate_number_endpoint = _Endpoint(
            settings={
                'response_type': (NumberValidateResponse,),
                'auth': [
                    'ApiKeyAuth',
                    'BearerAuth'
                ],
                'endpoint_path': '/numbers/validate/{phoneNumber}',
                'operation_id': 'validate_number',
                'http_method': 'GET',
                'servers': None,
            },
            params_map={
                'all': [
                    'phone_number',
                ],
                'required': [
                    'phone_number',
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
                    'phone_number':
                        (str,),
                },
                'attribute_map': {
                    'phone_number': 'phoneNumber',
                },
                'location_map': {
                    'phone_number': 'path',
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
        self.validate_numbers_endpoint = _Endpoint(
            settings={
                'response_type': (NumbersValidateResponse,),
                'auth': [
                    'ApiKeyAuth',
                    'BearerAuth'
                ],
                'endpoint_path': '/numbers/validate',
                'operation_id': 'validate_numbers',
                'http_method': 'POST',
                'servers': None,
            },
            params_map={
                'all': [
                    'numbers_validate_request',
                ],
                'required': [
                    'numbers_validate_request',
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
                    'numbers_validate_request':
                        (NumbersValidateRequest,),
                },
                'attribute_map': {
                },
                'location_map': {
                    'numbers_validate_request': 'body',
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

    def cancel_rent(
        self,
        rent_id,
        **kwargs
    ):
        """Cancel rent for phone number  # noqa: E501

        Cancel rent for a phone number. Phone numbers rentals can be canceled within the first 30 minutes of renting period. Your account will be credited for the phone number rental cost.      
### Errors for DELETE `/numbers/rent/{rentId}`  
| HTTP code  | Error code  | Type  | Description  |  
|:------------:|:------------:|:------------:| ------------ |  
|  400 | 1221  |  invalid_param  |  Invalid parameter `rentId` |  
|  403 | 1227  |  access_denied  |  Cannot cancel this rent. More than 30 minutes passed from start of renting period |  
|  404 | 1223  |  not_found  |  Rent ID not found |    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.cancel_rent(rent_id, async_req=True)
        >>> result = thread.get()

        Args:
            rent_id (str): Identifier of the rental operation

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
            CancelRentResponse
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
        kwargs['rent_id'] = \
            rent_id
        return self.cancel_rent_endpoint.call_with_http_info(**kwargs)

    def get_available_numbers(
        self,
        country_iso,
        **kwargs
    ):
        """Get available numbers for rent  # noqa: E501

        Get the list of available phone numbers for rent       
### Errors for GET `/numbers/rent/available/{countryIso}`  
| HTTP code  | Error code  | Type  | Description  |  
|:------------:|:------------:|:------------:| ------------ |  
|  400 | 2003  |  invalid_param  |  Country ISO provided is invalid |    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.get_available_numbers(country_iso, async_req=True)
        >>> result = thread.get()

        Args:
            country_iso (str):

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
            RentNumbersResponse
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
        kwargs['country_iso'] = \
            country_iso
        return self.get_available_numbers_endpoint.call_with_http_info(**kwargs)

    def get_bulk_lookup_status(
        self,
        lookup_bulk_id,
        **kwargs
    ):
        """Get Bulk Lookup result  # noqa: E501

        Get details of a bulk phone number lookup.        
### Errors for GET `/numbers/lookup/lookupBulkId/{lookupBulkId}`  
| HTTP code  | Error code  | Type  | Description  |  
|:------------:|:------------:|:------------:| ------------ |  
| 400 | 1218 | not_found | The lookupBulkId provided is invalid |  
| 404 | 1220 | invalid_param | Lookup Bulk ID not found |  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.get_bulk_lookup_status(lookup_bulk_id, async_req=True)
        >>> result = thread.get()

        Args:
            lookup_bulk_id (str): Identifier of the bulk number lookup campaign

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
            NumbersBulkLookupResult
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
        kwargs['lookup_bulk_id'] = \
            lookup_bulk_id
        return self.get_bulk_lookup_status_endpoint.call_with_http_info(**kwargs)

    def get_inbound_sms(
        self,
        rent_id,
        **kwargs
    ):
        """Get inbound SMS from rented number  # noqa: E501

        Get a list of SMS received on the rented phone number.      
### Errors for GET `/numbers/rent/{rentId}/inbound`  
| HTTP code  | Error code  | Type  | Description  |  
|:------------:|:------------:|:------------:| ------------ |  
|  400 | 1221  |  invalid_param  |  Invalid parameter `rentId` |  
|  404 | 1223  |  not_found  |  Rent ID not found |    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.get_inbound_sms(rent_id, async_req=True)
        >>> result = thread.get()

        Args:
            rent_id (str): Identifier of the rental operation

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
            GetInboundSMSResponse
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
        kwargs['rent_id'] = \
            rent_id
        return self.get_inbound_sms_endpoint.call_with_http_info(**kwargs)

    def get_rent_status(
        self,
        rent_id,
        **kwargs
    ):
        """Get status of rent  # noqa: E501

        Get details of an existing rental.      
### Errors for GET `/numbers/rent/{rentId}`  
| HTTP code  | Error code  | Type  | Description  |  
|:------------:|:------------:|:------------:| ------------ |  
|  400 | 1221  |  invalid_param  |  Invalid parameter `rentId` |  
|  404 | 1223  |  not_found  |  Rent ID not found |    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.get_rent_status(rent_id, async_req=True)
        >>> result = thread.get()

        Args:
            rent_id (str): Identifier of the rental operation

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
            GetRentStatusResponse
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
        kwargs['rent_id'] = \
            rent_id
        return self.get_rent_status_endpoint.call_with_http_info(**kwargs)

    def get_rented_numbers(
        self,
        **kwargs
    ):
        """Get list of your rented numbers  # noqa: E501

        Get the list of your rented phone numbers  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.get_rented_numbers(async_req=True)
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
            RentedNumbersResponse
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
        return self.get_rented_numbers_endpoint.call_with_http_info(**kwargs)

    def get_single_lookup_status(
        self,
        lookup_id,
        **kwargs
    ):
        """Get Single Lookup result  # noqa: E501

        Get details of a single number lookup.      
### Errors for GET `/numbers/lookup/lookupId/{lookupId}`  
| HTTP code  | Error code  | Type  | Description  |  
|:------------:|:------------:|:------------:| ------------ |  
| 400 | 1217 | invalid_param | The lookupId provided is invalid |  
| 404 | 1219 | not_found | Lookup  ID not found |  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.get_single_lookup_status(lookup_id, async_req=True)
        >>> result = thread.get()

        Args:
            lookup_id (str): Identifier of the number lookup

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
            DataNumberLookup
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
        kwargs['lookup_id'] = \
            lookup_id
        return self.get_single_lookup_status_endpoint.call_with_http_info(**kwargs)

    def lookup_number(
        self,
        phone_number,
        **kwargs
    ):
        """Lookup number  # noqa: E501

        Lookup a single phone number, provided in international E.164 format. Returns info about status of the number (ACTIVE, ABSENT), if the phone number is ported, roaming, original and current network operator.    The endpoint returns error if phone number is invalid.    ### Statuses of phone number lookup  | Status | Description |  
|:------------:|:------------|  | ACTIVE | Phone number is reachable |  | ABSENT | Phone number is not reachable |  | BARRED | Phone number has a block from their operator |  | UNKNOWN | Unknown subscriber. Phone number is not reachable |  | FAILED | Lookup for this phone number failed |    
### Errors for GET `/numbers/lookup/{phoneNumber}`  
| HTTP code  | Error code  | Type  | Description  |  
|:------------:|:------------:|:------------:| ------------ |  
| 400 | 1207 | invalid_param | The phone number is invalid |  
| 403 | 1214 | no_coverage | No coverage or restricted destination |  
| 400 | 1113 | insufficient_credit | Insufficient credit |  
| 400 | 1114 | insufficient_credit | Credit limit reached. To increase the credit limit, please contact your account manager |  
| 400 | 1212 | invalid_param | Invalid request parameters |  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.lookup_number(phone_number, async_req=True)
        >>> result = thread.get()

        Args:
            phone_number (str): Phone number in international E.164 format (eg. **+33612424105**). The leading plus sign of the international format can be set as is, ommited or url encoded. The API will automatically format and set the plus sign.   The following values are considered valid:   - +33612424105 - 33612424105 - %2B33612424105

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
            NumberLookupResponse
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
        kwargs['phone_number'] = \
            phone_number
        return self.lookup_number_endpoint.call_with_http_info(**kwargs)

    def lookup_numbers(
        self,
        numbers_lookup_request,
        **kwargs
    ):
        """Lookup numbers in bulk  # noqa: E501

        Lookup a list of phone numbers. The result of the bulk phone lookup: status of the number (ACTIVE, ABSENT), if the phone numbers are ported, roaming, original and current network operator. You can lookup in bulk up to **40.000 phone numbers**.    The endpoint does not return error if phone numbers are invalid.    <a name=\"lookup-statuses\"></a>  ### Statuses of phone number lookup  | Status | Description |  
|:------------:|:------------|  | ACTIVE | Phone number is reachable |  | ABSENT | Phone number is not reachable |  | BARRED | Phone number has a block from their operator |  | UNKNOWN | Unknown subscriber. Phone number is not reachable |  | FAILED | Lookup for this phone number failed |    
### Errors for POST `/numbers/lookup`  
| HTTP code  | Error code  | Type  | Description  |  
|:------------:|:------------:|:------------:| ------------ |  
| 400 | 1203 | invalid_param | The parameter 'phoneNumbers' is empty or not set |  
| 400 | 1208 | invalid_param | The parameter 'phoneNumbers' must be an array of phone numbers |  
| 400 | 1205 | invalid_param | The phone numbers array is too big (max. allowed: 40000 numbers) |  
| 400 | 1209 | invalid_param | The parameter 'lookupCallbackUrl' is not a valid URL |  
| 403 | 1214 | no_coverage | No coverage or restricted destination |  
| 400 | 1216 | invalid_param | No valid numbers provided or no coverage |  
| 400 | 1113 | insufficient_credit | Insufficient credit |  
| 400 | 1114 | insufficient_credit | Credit limit reached. To increase the credit limit, please contact your account manager |  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.lookup_numbers(numbers_lookup_request, async_req=True)
        >>> result = thread.get()

        Args:
            numbers_lookup_request (NumbersLookupRequest): 

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
            NumbersLookupResponse
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
        kwargs['numbers_lookup_request'] = \
            numbers_lookup_request
        return self.lookup_numbers_endpoint.call_with_http_info(**kwargs)

    def renew_rent(
        self,
        rent_id,
        renew_rent_request,
        **kwargs
    ):
        """Renew rent for phone number  # noqa: E501

        Renew the rental of a phone number.      
### Errors for PATCH `/numbers/rent/{rentId}`  
| HTTP code  | Error code  | Type  | Description  |  
|:------------:|:------------:|:------------:| ------------ |  
|  400 | 1221  |  invalid_param  |  Invalid parameter `rentId` |  

|  400 | 1224  |  invalid_param  |  Rent period is invalid (1, 7 or 30 days) |  

|  400 | 1225  |  invalid_param  |  Parameter `autorenew` must be of type boolean |  

|  400 | 1226  |  invalid_param  |  The parameter `callbackUrl` is not a valid url |  

|  400 | 1229  |  invalid_param  |  Rent period is not between min and max period allowed for this number |  
|  403 | 1228  |  access_denied  |  The rent cannot be renewed (rent already expired or phone number will not be available in the future) |  
|  404 | 1223  |  not_found  |  Rent ID not found |    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.renew_rent(rent_id, renew_rent_request, async_req=True)
        >>> result = thread.get()

        Args:
            rent_id (str): Identifier of the rental operation
            renew_rent_request (RenewRentRequest): 

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
            RentNumberResponse
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
        kwargs['rent_id'] = \
            rent_id
        kwargs['renew_rent_request'] = \
            renew_rent_request
        return self.renew_rent_endpoint.call_with_http_info(**kwargs)

    def rent_number(
        self,
        rent_number_request,
        **kwargs
    ):
        """Rent phone number  # noqa: E501

        Rent a phone number for a period of time (1, 7 or 30 days).       
### Errors for POST `/numbers/rent`  
| HTTP code  | Error code  | Type  | Description  |  
|:------------:|:------------:|:------------:| ------------ |  
|  400 | 1222  |  invalid_param  |  Invalid parameter `numberId` |  

|  400 | 1224  |  invalid_param  |  Rent period is invalid (1, 7 or 30 days) |  

|  400 | 1225  |  invalid_param  |  Parameter `autorenew` must be of type boolean |  

|  400 | 1226  |  invalid_param  |  The parameter `callbackUrl` is not a valid url |  

|  400 | 1229  |  invalid_param  |  Rent period is not between min and max period allowed for this number |  

|  400 | 1113  |  insufficient_credit  |  Insufficient credit |  
|  403 | 1231  |  access_denied  |  Cannot rent this phone number (already rented by someone else) |  
|  404 | 1230  |  not_found  |  Number ID not found or number is not available for rent anymore|    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.rent_number(rent_number_request, async_req=True)
        >>> result = thread.get()

        Args:
            rent_number_request (RentNumberRequest): 

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
            RentNumberResponse
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
        kwargs['rent_number_request'] = \
            rent_number_request
        return self.rent_number_endpoint.call_with_http_info(**kwargs)

    def validate_number(
        self,
        phone_number,
        **kwargs
    ):
        """Validate number  # noqa: E501

        Validates a single phone number, provided in international E.164 format.    The endpoint returns error if phone number is invalid.    
### Errors for GET `/numbers/validate/{phoneNumber}`  
| HTTP code  | Error code  | Type  | Description  |  
|:------------:|:------------:|:------------:| ------------ |  
|  400 | 1207  |  invalid_param  |  The phone number is invalid  |  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.validate_number(phone_number, async_req=True)
        >>> result = thread.get()

        Args:
            phone_number (str): Phone number in international E.164 format (eg. **+33612424105**). The leading plus sign of the international format can be set as is, ommited or url encoded. The API will automatically format and set the plus sign.   The following values are considered valid:   - +33612424105 - 33612424105 - %2B33612424105

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
            NumberValidateResponse
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
        kwargs['phone_number'] = \
            phone_number
        return self.validate_number_endpoint.call_with_http_info(**kwargs)

    def validate_numbers(
        self,
        numbers_validate_request,
        **kwargs
    ):
        """Validate numbers in bulk  # noqa: E501

        Validate a list of phone numbers. You can validate in bulk up to **40.000 phone numbers**.    The endpoint does not return error if phone numbers are invalid.    This method will validate the list of phone numbers and return an array of objects, **preserving the order of the list provided** and not excluding the invalid phone numbers.     An invalid phone number will have the parameter `invalid` with value `true` in the response object.      
### Errors for POST `/numbers/validate`  
| HTTP code  | Error code  | Type  | Description  |  
|:------------:|:------------:|:------------:| ------------ |  
|  400 | 1203  |  invalid_param  |  The parameter `phoneNumbers` is empty or not set |  

|  400 | 1208  |  invalid_param  |  The parameter `phoneNumbers` must be an array of phone numbers |  
| 400 | 1205 | invalid_param | The phone numbers array is too big (max. allowed: 40000 numbers) |    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.validate_numbers(numbers_validate_request, async_req=True)
        >>> result = thread.get()

        Args:
            numbers_validate_request (NumbersValidateRequest): 

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
            NumbersValidateResponse
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
        kwargs['numbers_validate_request'] = \
            numbers_validate_request
        return self.validate_numbers_endpoint.call_with_http_info(**kwargs)

