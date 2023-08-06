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
from smscx_client.model.cancel_otp_response import CancelOtpResponse
from smscx_client.model.data_otp import DataOtp
from smscx_client.model.model400_invalid_param import Model400InvalidParam
from smscx_client.model.model401_unauthorized import Model401Unauthorized
from smscx_client.model.model403_insufficient_scope import Model403InsufficientScope
from smscx_client.model.model404_not_found import Model404NotFound
from smscx_client.model.model500_server_error import Model500ServerError
from smscx_client.model.new_otp_request import NewOtpRequest
from smscx_client.model.new_otp_response import NewOtpResponse
from smscx_client.model.verify_pin_request import VerifyPinRequest
from smscx_client.model.verify_pin_response import VerifyPinResponse


class OtpApi(object):
    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client
        self.cancel_otp_endpoint = _Endpoint(
            settings={
                'response_type': (CancelOtpResponse,),
                'auth': [
                    'ApiKeyAuth',
                    'BearerAuth'
                ],
                'endpoint_path': '/otp/{otpId}',
                'operation_id': 'cancel_otp',
                'http_method': 'DELETE',
                'servers': None,
            },
            params_map={
                'all': [
                    'otp_id',
                ],
                'required': [
                    'otp_id',
                ],
                'nullable': [
                ],
                'enum': [
                ],
                'validation': [
                    'otp_id',
                ]
            },
            root_map={
                'validations': {
                    ('otp_id',): {
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
                    'otp_id':
                        (str,),
                },
                'attribute_map': {
                    'otp_id': 'otpId',
                },
                'location_map': {
                    'otp_id': 'path',
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
        self.get_otp_status_endpoint = _Endpoint(
            settings={
                'response_type': (DataOtp,),
                'auth': [
                    'ApiKeyAuth',
                    'BearerAuth'
                ],
                'endpoint_path': '/otp/{otpId}',
                'operation_id': 'get_otp_status',
                'http_method': 'GET',
                'servers': None,
            },
            params_map={
                'all': [
                    'otp_id',
                ],
                'required': [
                    'otp_id',
                ],
                'nullable': [
                ],
                'enum': [
                ],
                'validation': [
                    'otp_id',
                ]
            },
            root_map={
                'validations': {
                    ('otp_id',): {
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
                    'otp_id':
                        (str,),
                },
                'attribute_map': {
                    'otp_id': 'otpId',
                },
                'location_map': {
                    'otp_id': 'path',
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
        self.new_otp_endpoint = _Endpoint(
            settings={
                'response_type': (NewOtpResponse,),
                'auth': [
                    'ApiKeyAuth',
                    'BearerAuth'
                ],
                'endpoint_path': '/otp',
                'operation_id': 'new_otp',
                'http_method': 'POST',
                'servers': None,
            },
            params_map={
                'all': [
                    'new_otp_request',
                ],
                'required': [
                    'new_otp_request',
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
                    'new_otp_request':
                        (NewOtpRequest,),
                },
                'attribute_map': {
                },
                'location_map': {
                    'new_otp_request': 'body',
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
        self.verify_otp_endpoint = _Endpoint(
            settings={
                'response_type': (VerifyPinResponse,),
                'auth': [
                    'ApiKeyAuth',
                    'BearerAuth'
                ],
                'endpoint_path': '/otp/{otpId}',
                'operation_id': 'verify_otp',
                'http_method': 'POST',
                'servers': None,
            },
            params_map={
                'all': [
                    'otp_id',
                    'verify_pin_request',
                ],
                'required': [
                    'otp_id',
                    'verify_pin_request',
                ],
                'nullable': [
                ],
                'enum': [
                ],
                'validation': [
                    'otp_id',
                ]
            },
            root_map={
                'validations': {
                    ('otp_id',): {
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
                    'otp_id':
                        (str,),
                    'verify_pin_request':
                        (VerifyPinRequest,),
                },
                'attribute_map': {
                    'otp_id': 'otpId',
                },
                'location_map': {
                    'otp_id': 'path',
                    'verify_pin_request': 'body',
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

    def cancel_otp(
        self,
        otp_id,
        **kwargs
    ):
        """Cancel OTP  # noqa: E501

        Cancel OTP request if a valid identifier was provided.    
### Errors for DELETE `/otp/{otpId}`  
| HTTP code  | Error code  | Type  | Description  |  
|:------------:|:------------:|:------------:| ------------ |  
| 404 | 2021 | not_found | Otp ID not found |  
| 403 | 2030 | access_denied | Otp already cancelled |  
| 403 | 2031 | access_denied | You cannot cancel a non-pending Otp |  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.cancel_otp(otp_id, async_req=True)
        >>> result = thread.get()

        Args:
            otp_id (str): Identifier of the OTP request

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
            CancelOtpResponse
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
        kwargs['otp_id'] = \
            otp_id
        return self.cancel_otp_endpoint.call_with_http_info(**kwargs)

    def get_otp_status(
        self,
        otp_id,
        **kwargs
    ):
        """Get OTP status  # noqa: E501

        Retrieves the details of OTP status if a valid identifier was provided.    ### Status for OTP requests  | Status | Description |  
|:------------:|:------------|  | PENDING | The OTP is pending validation by user |  | VERIFIED | The OTP was validated by user |  | EXPIRED | The validity of OTP has expired |  | CANCELLED | The OTP was cancelled by the user |  | FAILED | The OTP failed because too many unsuccessful attempts |    
### Errors for GET `/otp/{otpId}`  
| HTTP code  | Error code  | Type  | Description  |  
|:------------:|:------------:|:------------:| ------------ |  
| 404 | 2021 | not_found | Otp ID not found |  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.get_otp_status(otp_id, async_req=True)
        >>> result = thread.get()

        Args:
            otp_id (str): Identifier of the OTP request

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
            DataOtp
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
        kwargs['otp_id'] = \
            otp_id
        return self.get_otp_status_endpoint.call_with_http_info(**kwargs)

    def new_otp(
        self,
        new_otp_request,
        **kwargs
    ):
        """New OTP  # noqa: E501

        Create a OTP request to verify a phone number.    <a name=\"otp-status\"></a>  ### Status for OTP requests  | Status | Description |  
|:------------:|:------------|  | PENDING | The OTP is pending validation by user |  | VERIFIED | The OTP was validated by user |  | EXPIRED | The validity of OTP has expired |  | CANCELLED | The OTP was cancelled by the user |  | FAILED | The OTP failed because too many unsuccessful attempts |    
### Errors for POST `/otp`  
| HTTP code  | Error code  | Type  | Description  |  
|:------------:|:------------:|:------------:| ------------ |  
| 400 | 2001 | invalid_param | The parameter 'phoneNumber' is empty or not set |  
| 400 | 2002 | invalid_param | The parameter 'countryIso' is empty or not set |  
| 400 | 2003 | invalid_param | Country ISO provided is invalid |  
| 400 | 2004 | invalid_param | The parameter 'from' is empty or not set |  
| 400 | 2005 | invalid_param | The parameter 'from' is not valid (min 3, max 15 characters) |  
| 400 | 2006 | invalid_param | The parameter 'template' is empty or not set |  
| 400 | 2006 | invalid_param | The parameter 'template' does not contain placeholder {{pin}} |  
| 400 | 2007 | invalid_param | The parameter 'ttl' is not a number |  
| 400 | 2008 | invalid_param | Min value for 'ttl' is 60 seconds |  
| 400 | 2009 | invalid_param | Max value for 'ttl' is 1800 seconds (30 mins) |  
| 400 | 2010 | invalid_param | The parameter 'maxAttempts' is not a number |  
| 400 | 2011 | invalid_param | Min value for 'maxAttempts' is 1 |  
| 400 | 2012 | invalid_param | Max value for 'maxAttempts' is 10 |  
| 400 | 2013 | invalid_param | The parameter 'pinType' is empty or not set |  
| 400 | 2014 | invalid_param | Invalid parameter 'pinType'. Must be one of: letters, numbers, alphanumeric |  
| 400 | 2015 | invalid_param | The parameter 'pinLength' is not a number |  
| 400 | 2016 | invalid_param | Min value for 'pinLength' is 4 |  
| 400 | 2017 | invalid_param | Max value for 'pinLength' is 10 |  
| 400 | 2018 | invalid_param | Track ID provided (parameter 'trackId') is not a valid UUID (v1-v5) |  
| 400 | 2019 | invalid_param | The parameter 'otpCallbackUrl' is not a valid URL |  
| 400 | 2020 | invalid_param | The phone number provided is invalid |    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.new_otp(new_otp_request, async_req=True)
        >>> result = thread.get()

        Args:
            new_otp_request (NewOtpRequest): 

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
            NewOtpResponse
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
        kwargs['new_otp_request'] = \
            new_otp_request
        return self.new_otp_endpoint.call_with_http_info(**kwargs)

    def verify_otp(
        self,
        otp_id,
        pin,
        **kwargs
    ):
        """Verify OTP  # noqa: E501

        Verify the OTP received on the phone number.    
### Errors for POST `/otp/{otpId}`  
| HTTP code  | Error code  | Type  | Description  |  
|:------------:|:------------:|:------------:| ------------ |  
| 404 | 2021 | not_found | Otp ID not found |  
| 400 | 2022 | invalid_param | The parameter pin is empty or not set |  
| 400 | 2023 | otp_verified | The OTP was already verified |  
| 400 | 2024 | otp_cancelled | The OTP was canceled |  
| 400 | 2025 | otp_expired | The OTP has expired |  
| 400 | 2026 | otp_failed | The OTP has failed, maximum attempts reached |  
| 400 | 2027 | otp_failed | Max attempts reached |  
| 400 | 2028 | otp_expired | The PIN has expired |  
| 400 | 2029 | invalid_pin | The PIN provided does not verify |  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.verify_otp(otp_id, verify_pin_request, async_req=True)
        >>> result = thread.get()

        Args:
            otp_id (str): Identifier of the OTP request
            pin (str, int): 

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
            VerifyPinResponse
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
        kwargs['otp_id'] = \
            otp_id
        kwargs['verify_pin_request'] = VerifyPinRequest(pin)
        return self.verify_otp_endpoint.call_with_http_info(**kwargs)

