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
from smscx_client.model.get_summary_reports200_response import GetSummaryReports200Response
from smscx_client.model.model400_invalid_param import Model400InvalidParam
from smscx_client.model.model401_unauthorized import Model401Unauthorized
from smscx_client.model.model403_insufficient_scope import Model403InsufficientScope
from smscx_client.model.model404_not_found import Model404NotFound
from smscx_client.model.model500_server_error import Model500ServerError
from smscx_client.model.report_single_response import ReportSingleResponse
from smscx_client.model.reports_advanced_response import ReportsAdvancedResponse
from smscx_client.model.reports_campaign_response import ReportsCampaignResponse
from smscx_client.model.reports_campaigns_respone import ReportsCampaignsRespone


class ReportsApi(object):
    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client
        self.export_advanced_report_to_csv_endpoint = _Endpoint(
            settings={
                'response_type': (str,),
                'auth': [
                    'ApiKeyAuth',
                    'BearerAuth'
                ],
                'endpoint_path': '/reports/csv',
                'operation_id': 'export_advanced_report_to_csv',
                'http_method': 'GET',
                'servers': None,
            },
            params_map={
                'all': [
                    'period',
                    'start_date',
                    'end_date',
                    'channel',
                    'source',
                    'delivery_report',
                    'country_iso',
                    'limit',
                ],
                'required': [
                    'period',
                    'start_date',
                    'end_date',
                ],
                'nullable': [
                ],
                'enum': [
                    'channel',
                    'source',
                    'delivery_report',
                ],
                'validation': [
                ]
            },
            root_map={
                'validations': {
                },
                'allowed_values': {
                    ('channel',): {

                        "SMS": "sms",
                        "VIBER": "viber",
                        "WHATSAPP": "whatsapp",
                        "MULTICHANNEL": "multichannel"
                    },
                    ('source',): {

                        "API": "api",
                        "EXCEL": "excel",
                        "WEBAPP": "webapp",
                        "SMPP": "smpp",
                        "PLUGIN": "plugin",
                        "ALERTS": "alerts"
                    },
                    ('delivery_report',): {

                        "DELIVERED": "delivered",
                        "FAILED": "failed",
                        "SENT": "sent",
                        "ACCEPTED": "accepted",
                        "REJECTED": "rejected",
                        "SCHEDULED": "scheduled"
                    },
                },
                'api_types': {
                    'period':
                        (str,),
                    'start_date':
                        (str,),
                    'end_date':
                        (str,),
                    'channel':
                        (str,),
                    'source':
                        (str,),
                    'delivery_report':
                        (str,),
                    'country_iso':
                        (str,),
                    'limit':
                        (int,),
                },
                'attribute_map': {
                    'period': 'period',
                    'start_date': 'start_date',
                    'end_date': 'end_date',
                    'channel': 'channel',
                    'source': 'source',
                    'delivery_report': 'delivery_report',
                    'country_iso': 'country_iso',
                    'limit': 'limit',
                },
                'location_map': {
                    'period': 'query',
                    'start_date': 'query',
                    'end_date': 'query',
                    'channel': 'query',
                    'source': 'query',
                    'delivery_report': 'query',
                    'country_iso': 'query',
                    'limit': 'query',
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
        self.export_advanced_report_to_xlsx_endpoint = _Endpoint(
            settings={
                'response_type': (file_type,),
                'auth': [
                    'ApiKeyAuth',
                    'BearerAuth'
                ],
                'endpoint_path': '/reports/xlsx',
                'operation_id': 'export_advanced_report_to_xlsx',
                'http_method': 'GET',
                'servers': None,
            },
            params_map={
                'all': [
                    'period',
                    'start_date',
                    'end_date',
                    'channel',
                    'source',
                    'delivery_report',
                    'country_iso',
                    'limit',
                ],
                'required': [
                    'period',
                    'start_date',
                    'end_date',
                ],
                'nullable': [
                ],
                'enum': [
                    'channel',
                    'source',
                    'delivery_report',
                ],
                'validation': [
                ]
            },
            root_map={
                'validations': {
                },
                'allowed_values': {
                    ('channel',): {

                        "SMS": "sms",
                        "VIBER": "viber",
                        "WHATSAPP": "whatsapp",
                        "MULTICHANNEL": "multichannel"
                    },
                    ('source',): {

                        "API": "api",
                        "EXCEL": "excel",
                        "WEBAPP": "webapp",
                        "SMPP": "smpp",
                        "PLUGIN": "plugin",
                        "ALERTS": "alerts"
                    },
                    ('delivery_report',): {

                        "DELIVERED": "delivered",
                        "FAILED": "failed",
                        "SENT": "sent",
                        "ACCEPTED": "accepted",
                        "REJECTED": "rejected",
                        "SCHEDULED": "scheduled"
                    },
                },
                'api_types': {
                    'period':
                        (str,),
                    'start_date':
                        (str,),
                    'end_date':
                        (str,),
                    'channel':
                        (str,),
                    'source':
                        (str,),
                    'delivery_report':
                        (str,),
                    'country_iso':
                        (str,),
                    'limit':
                        (int,),
                },
                'attribute_map': {
                    'period': 'period',
                    'start_date': 'start_date',
                    'end_date': 'end_date',
                    'channel': 'channel',
                    'source': 'source',
                    'delivery_report': 'delivery_report',
                    'country_iso': 'country_iso',
                    'limit': 'limit',
                },
                'location_map': {
                    'period': 'query',
                    'start_date': 'query',
                    'end_date': 'query',
                    'channel': 'query',
                    'source': 'query',
                    'delivery_report': 'query',
                    'country_iso': 'query',
                    'limit': 'query',
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
        self.export_campaign_report_to_csv_endpoint = _Endpoint(
            settings={
                'response_type': (str,),
                'auth': [
                    'ApiKeyAuth',
                    'BearerAuth'
                ],
                'endpoint_path': '/reports/campaigns/{campaignId}/csv',
                'operation_id': 'export_campaign_report_to_csv',
                'http_method': 'GET',
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
                    'application/csv',
                    'application/json'
                ],
                'content_type': [],
            },
            api_client=api_client
        )
        self.export_campaign_report_to_xlsx_endpoint = _Endpoint(
            settings={
                'response_type': (file_type,),
                'auth': [
                    'ApiKeyAuth',
                    'BearerAuth'
                ],
                'endpoint_path': '/reports/campaigns/{campaignId}/xlsx',
                'operation_id': 'export_campaign_report_to_xlsx',
                'http_method': 'GET',
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
                    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                    'application/json'
                ],
                'content_type': [],
            },
            api_client=api_client
        )
        self.get_advanced_report_endpoint = _Endpoint(
            settings={
                'response_type': (ReportsAdvancedResponse,),
                'auth': [
                    'ApiKeyAuth',
                    'BearerAuth'
                ],
                'endpoint_path': '/reports',
                'operation_id': 'get_advanced_report',
                'http_method': 'GET',
                'servers': None,
            },
            params_map={
                'all': [
                    'period',
                    'start_date',
                    'end_date',
                    'channel',
                    'source',
                    'delivery_report',
                    'country_iso',
                    'short_response',
                    'limit',
                    'next',
                    'previous',
                ],
                'required': [
                    'period',
                    'start_date',
                    'end_date',
                ],
                'nullable': [
                ],
                'enum': [
                    'channel',
                    'source',
                    'delivery_report',
                ],
                'validation': [
                ]
            },
            root_map={
                'validations': {
                },
                'allowed_values': {
                    ('channel',): {

                        "SMS": "sms",
                        "VIBER": "viber",
                        "WHATSAPP": "whatsapp",
                        "MULTICHANNEL": "multichannel"
                    },
                    ('source',): {

                        "API": "api",
                        "EXCEL": "excel",
                        "WEBAPP": "webapp",
                        "SMPP": "smpp",
                        "PLUGIN": "plugin",
                        "ALERTS": "alerts"
                    },
                    ('delivery_report',): {

                        "DELIVERED": "delivered",
                        "FAILED": "failed",
                        "SENT": "sent",
                        "ACCEPTED": "accepted",
                        "REJECTED": "rejected",
                        "SCHEDULED": "scheduled"
                    },
                },
                'api_types': {
                    'period':
                        (str,),
                    'start_date':
                        (str,),
                    'end_date':
                        (str,),
                    'channel':
                        (str,),
                    'source':
                        (str,),
                    'delivery_report':
                        (str,),
                    'country_iso':
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
                    'period': 'period',
                    'start_date': 'start_date',
                    'end_date': 'end_date',
                    'channel': 'channel',
                    'source': 'source',
                    'delivery_report': 'delivery_report',
                    'country_iso': 'country_iso',
                    'short_response': 'short_response',
                    'limit': 'limit',
                    'next': 'next',
                    'previous': 'previous',
                },
                'location_map': {
                    'period': 'query',
                    'start_date': 'query',
                    'end_date': 'query',
                    'channel': 'query',
                    'source': 'query',
                    'delivery_report': 'query',
                    'country_iso': 'query',
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
        self.get_campaign_report_endpoint = _Endpoint(
            settings={
                'response_type': (ReportsCampaignResponse,),
                'auth': [
                    'ApiKeyAuth',
                    'BearerAuth'
                ],
                'endpoint_path': '/reports/campaigns/{campaignId}',
                'operation_id': 'get_campaign_report',
                'http_method': 'GET',
                'servers': None,
            },
            params_map={
                'all': [
                    'campaign_id',
                    'short_response',
                    'limit',
                    'next',
                    'previous',
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
                    'campaign_id': 'campaignId',
                    'short_response': 'short_response',
                    'limit': 'limit',
                    'next': 'next',
                    'previous': 'previous',
                },
                'location_map': {
                    'campaign_id': 'path',
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
        self.get_campaigns_list_endpoint = _Endpoint(
            settings={
                'response_type': (ReportsCampaignsRespone,),
                'auth': [
                    'ApiKeyAuth',
                    'BearerAuth'
                ],
                'endpoint_path': '/reports/campaigns',
                'operation_id': 'get_campaigns_list',
                'http_method': 'GET',
                'servers': None,
            },
            params_map={
                'all': [
                    'delivery_reports',
                    'source',
                    'limit',
                    'next',
                    'previous',
                ],
                'required': [],
                'nullable': [
                ],
                'enum': [
                    'source',
                ],
                'validation': [
                ]
            },
            root_map={
                'validations': {
                },
                'allowed_values': {
                    ('source',): {

                        "API": "api",
                        "EXCEL": "excel",
                        "WEBAPP": "webapp",
                        "SMPP": "smpp",
                        "PLUGIN": "plugin",
                        "ALERTS": "alerts"
                    },
                },
                'api_types': {
                    'delivery_reports':
                        (bool,),
                    'source':
                        (str,),
                    'limit':
                        (int,),
                    'next':
                        (str,),
                    'previous':
                        (str,),
                },
                'attribute_map': {
                    'delivery_reports': 'delivery_reports',
                    'source': 'source',
                    'limit': 'limit',
                    'next': 'next',
                    'previous': 'previous',
                },
                'location_map': {
                    'delivery_reports': 'query',
                    'source': 'query',
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
        self.get_single_report_endpoint = _Endpoint(
            settings={
                'response_type': (ReportSingleResponse,),
                'auth': [
                    'ApiKeyAuth',
                    'BearerAuth'
                ],
                'endpoint_path': '/reports/single/{msgId}',
                'operation_id': 'get_single_report',
                'http_method': 'GET',
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
        self.get_summary_reports_endpoint = _Endpoint(
            settings={
                'response_type': (GetSummaryReports200Response,),
                'auth': [
                    'ApiKeyAuth',
                    'BearerAuth'
                ],
                'endpoint_path': '/reports/summary/{dimension}',
                'operation_id': 'get_summary_reports',
                'http_method': 'GET',
                'servers': None,
            },
            params_map={
                'all': [
                    'dimension',
                    'period',
                    'start_date',
                    'end_date',
                    'limit',
                ],
                'required': [
                    'dimension',
                    'period',
                    'start_date',
                    'end_date',
                ],
                'nullable': [
                ],
                'enum': [
                    'dimension',
                ],
                'validation': [
                ]
            },
            root_map={
                'validations': {
                },
                'allowed_values': {
                    ('dimension',): {

                        "SOURCE": "source",
                        "CHANNEL": "channel",
                        "COUNTRY": "country",
                        "TRAFFIC": "traffic",
                        "DELIVERY": "delivery"
                    },
                },
                'api_types': {
                    'dimension':
                        (str,),
                    'period':
                        (str,),
                    'start_date':
                        (str,),
                    'end_date':
                        (str,),
                    'limit':
                        (int,),
                },
                'attribute_map': {
                    'dimension': 'dimension',
                    'period': 'period',
                    'start_date': 'start_date',
                    'end_date': 'end_date',
                    'limit': 'limit',
                },
                'location_map': {
                    'dimension': 'path',
                    'period': 'query',
                    'start_date': 'query',
                    'end_date': 'query',
                    'limit': 'query',
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

    def export_advanced_report_to_csv(
        self,
        period,
        start_date,
        end_date,
        **kwargs
    ):
        """Export advanced report to CSV  # noqa: E501

        Exports the report for for the specified filters to a CSV file.  The only required parameters are the dates filters: `period` parameter or `start_date` and `end_date`.    If no data is available for the report, an empty CSV file is returned (with first line headers).    
### Errors for GET `/reports/csv`  
| HTTP code  | Error code  | Type  | Description  |  
|:------------:|:------------:|:------------:| ------------ |  
|  400 | 1820  |  invalid_param  |  The parameter `period` is not a valid date (format Y-m or Y) |  

|  400 | 1821  |  invalid_param  |  The parameter `start_date` is not a valid date |  

|  400 | 1822  |  invalid_param  |  The parameter `end_date` is not a valid date |  

|  400 | 1823  |  invalid_param  |  The end date is before the start date |  

|  400 | 1824  |  invalid_param  |  No `period` parameter or interval (`start_date`, `end_date`) |  

|  400 | 1825  |  invalid_param  |  The parameter `source` is not valid |  

|  400 | 1826  |  invalid_param  |  The parameter `delivery_report` is not valid (delivered, failed or sent) |  

|  400 | 1827  |  invalid_param  |  The parameter `country_iso` is not for a valid country  |  

|  400 | 1828  |  invalid_param  |  The parameter `channel` is not valid (sms, viber, whatsapp, multichannel) |  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.export_advanced_report_to_csv(period, start_date, end_date, async_req=True)
        >>> result = thread.get()

        Args:
            period (str): Period for the requested report in format **Y-M** or **Y**
            start_date (str): The start date of the report in format Y-M-D
            end_date (str): The end date of the report in format Y-M-D

        Keyword Args:
            channel (str): Channel of the sent messages. [optional]
            source (str): Source of the sent messages. [optional]
            delivery_report (str): . [optional]
            country_iso (str): Two-letter country code defined in ISO-3166 alpha 2 standard (case insensitive). [optional]
            limit (int): A limit on the number of objects to be returned. [optional] if omitted the server will use the default value of 500
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
        kwargs['period'] = \
            period
        kwargs['start_date'] = \
            start_date
        kwargs['end_date'] = \
            end_date
        return self.export_advanced_report_to_csv_endpoint.call_with_http_info(**kwargs)

    def export_advanced_report_to_xlsx(
        self,
        period,
        start_date,
        end_date,
        **kwargs
    ):
        """Export advanced report to XLSX  # noqa: E501

        Exports the report for for the specified filters to a XLSX file (Excel).  The only required parameters are the dates filters: `period` parameter or `start_date` and `end_date`.    If no data is available for the report, an empty XLSX file is returned (with first line headers).    
### Errors for GET `/reports/xlsx`  
| HTTP code  | Error code  | Type  | Description  |  
|:------------:|:------------:|:------------:| ------------ |  
|  400 | 1820  |  invalid_param  |  The parameter `period` is not a valid date (format Y-m or Y) |  

|  400 | 1821  |  invalid_param  |  The parameter `start_date` is not a valid date |  

|  400 | 1822  |  invalid_param  |  The parameter `end_date` is not a valid date |  

|  400 | 1823  |  invalid_param  |  The end date is before the start date |  

|  400 | 1824  |  invalid_param  |  No `period` parameter or interval (`start_date`, `end_date`) |  

|  400 | 1825  |  invalid_param  |  The parameter `source` is not valid |  

|  400 | 1826  |  invalid_param  |  The parameter `delivery_report` is not valid (delivered, failed or sent) |  

|  400 | 1827  |  invalid_param  |  The parameter `country_iso` is not for a valid country  |  

|  400 | 1828  |  invalid_param  |  The parameter `channel` is not valid (sms, viber, whatsapp, multichannel) |  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.export_advanced_report_to_xlsx(period, start_date, end_date, async_req=True)
        >>> result = thread.get()

        Args:
            period (str): Period for the requested report in format **Y-M** or **Y**
            start_date (str): The start date of the report in format Y-M-D
            end_date (str): The end date of the report in format Y-M-D

        Keyword Args:
            channel (str): Channel of the sent messages. [optional]
            source (str): Source of the sent messages. [optional]
            delivery_report (str): . [optional]
            country_iso (str): Two-letter country code defined in ISO-3166 alpha 2 standard (case insensitive). [optional]
            limit (int): A limit on the number of objects to be returned. [optional] if omitted the server will use the default value of 500
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
        kwargs['period'] = \
            period
        kwargs['start_date'] = \
            start_date
        kwargs['end_date'] = \
            end_date
        return self.export_advanced_report_to_xlsx_endpoint.call_with_http_info(**kwargs)

    def export_campaign_report_to_csv(
        self,
        campaign_id,
        **kwargs
    ):
        """Export campaign report to CSV  # noqa: E501

        Exports the details of a sent campaign to a CSV file.    
### Errors for GET `/reports/campaigns/{campaignId}/csv`  
| HTTP code  | Error code  | Type  | Description  |  
|:------------:|:------------:|:------------:| ------------ |  
|  404 | 1160  |  not_found  |  Campaign ID or msg ID provided was not found  |    

|  400 | 1165  |  invalid_param  |  Campaign ID or msg ID provided is not valid  |  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.export_campaign_report_to_csv(campaign_id, async_req=True)
        >>> result = thread.get()

        Args:
            campaign_id (str): Identifier of a sent campaign

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
        kwargs['campaign_id'] = \
            campaign_id
        return self.export_campaign_report_to_csv_endpoint.call_with_http_info(**kwargs)

    def export_campaign_report_to_xlsx(
        self,
        campaign_id,
        **kwargs
    ):
        """Export campaign report to XLSX  # noqa: E501

        Exports the details of a sent campaign to a XLSX file (Excel).    
### Errors for GET `/reports/campaigns/{campaignId}/xlsx`  
| HTTP code  | Error code  | Type  | Description  |  
|:------------:|:------------:|:------------:| ------------ |  
|  404 | 1160  |  not_found  |  Campaign ID or msg ID provided was not found  |    

|  400 | 1165  |  invalid_param  |  Campaign ID or msg ID provided is not valid  |  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.export_campaign_report_to_xlsx(campaign_id, async_req=True)
        >>> result = thread.get()

        Args:
            campaign_id (str): Identifier of a sent campaign

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
        kwargs['campaign_id'] = \
            campaign_id
        return self.export_campaign_report_to_xlsx_endpoint.call_with_http_info(**kwargs)

    def get_advanced_report(
        self,
        period,
        start_date,
        end_date,
        **kwargs
    ):
        """Get advanced report  # noqa: E501

        Retrieves the report for the specified filters.  The only required parameters are the dates filters: `period` parameter or `start_date` and `end_date`.    If no data is available for the report, an empty data object is returned.    
### Errors for GET `/reports`  
| HTTP code  | Error code  | Type  | Description  |  
|:------------:|:------------:|:------------:| ------------ |  
|  400 | 1820  |  invalid_param  |  The parameter `period` is not a valid date (format Y-m or Y) |  

|  400 | 1821  |  invalid_param  |  The parameter `start_date` is not a valid date |  

|  400 | 1822  |  invalid_param  |  The parameter `end_date` is not a valid date |  

|  400 | 1823  |  invalid_param  |  The end date is before the start date |  

|  400 | 1824  |  invalid_param  |  No `period` parameter or interval (`start_date`, `end_date`) |  

|  400 | 1825  |  invalid_param  |  The parameter `source` is not valid |  

|  400 | 1826  |  invalid_param  |  The parameter `delivery_report` is not valid (delivered, failed or sent) |  

|  400 | 1827  |  invalid_param  |  The parameter `country_iso` is not for a valid country  |  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.get_advanced_report(period, start_date, end_date, async_req=True)
        >>> result = thread.get()

        Args:
            period (str): Period for the requested report in format **Y-M** or **Y**
            start_date (str): The start date of the report in format Y-M-D
            end_date (str): The end date of the report in format Y-M-D

        Keyword Args:
            channel (str): Channel of the sent messages. [optional]
            source (str): Source of the sent messages. [optional]
            delivery_report (str): . [optional]
            country_iso (str): Two-letter country code defined in ISO-3166 alpha 2 standard (case insensitive). [optional]
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
            ReportsAdvancedResponse
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
        kwargs['period'] = \
            period
        kwargs['start_date'] = \
            start_date
        kwargs['end_date'] = \
            end_date
        return self.get_advanced_report_endpoint.call_with_http_info(**kwargs)

    def get_campaign_report(
        self,
        campaign_id,
        **kwargs
    ):
        """Get campaign report  # noqa: E501

        Returns the details of a sent campaign if a valid identifier was provided.    
### Errors for GET `/reports/campaigns/{campaignId}`  
| HTTP code  | Error code  | Type  | Description  |  
|:------------:|:------------:|:------------:| ------------ |  
|  404 | 1150  |  not_found  |  Campaign ID provided was not found |  

|  400 | 1155  |  invalid_param  |  Campaign ID provided is not valid |  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.get_campaign_report(campaign_id, async_req=True)
        >>> result = thread.get()

        Args:
            campaign_id (str): Identifier of a sent campaign

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
            ReportsCampaignResponse
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
        return self.get_campaign_report_endpoint.call_with_http_info(**kwargs)

    def get_campaigns_list(
        self,
        **kwargs
    ):
        """Get list of sent campaigns  # noqa: E501

        Returns a list of sent Campaigns, with the most recent appearing first.    If no data is available, an empty data object is returned.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.get_campaigns_list(async_req=True)
        >>> result = thread.get()


        Keyword Args:
            delivery_reports (bool): The response will contain an object **data.status** with delivery report summary for each campaign. [optional] if omitted the server will use the default value of False
            source (str): Source of the sent messages. [optional]
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
            ReportsCampaignsRespone
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
        return self.get_campaigns_list_endpoint.call_with_http_info(**kwargs)

    def get_single_report(
        self,
        msg_id,
        **kwargs
    ):
        """Get report for single SMS or Viber or Whatsapp or Multichannel  # noqa: E501

        Returns the details of a single message if a valid identifier was provided.    
### Errors for GET `/reports/single/{msgId} `  
| HTTP code  | Error code  | Type  | Description  |  
|:------------:|:------------:|:------------:| ------------ |  
|  404 | 1160  |  not_found  |  Campaign ID or msg ID provided was not found  |    

|  400 | 1165  |  invalid_param  |  Campaign ID or msg ID provided is not valid  |  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.get_single_report(msg_id, async_req=True)
        >>> result = thread.get()

        Args:
            msg_id (str): Identifier of a sent message

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
            ReportSingleResponse
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
        return self.get_single_report_endpoint.call_with_http_info(**kwargs)

    def get_summary_reports(
        self,
        dimension,
        period,
        start_date,
        end_date,
        **kwargs
    ):
        """Get summary reports for a dimension  # noqa: E501

        Retrieves a summary report for the specified dimensions.    The only required parameters are the dates for the report. The date filters can be: with `period` parameter or with `start_date` and `end_date`    For some dimensions (**traffic** and **delivery**) the summary report will aggregate on dates.   If the summary report was requested with **period** parameter, the dates will be months or days.  If it was requested with interval **start_date** - **end_date**, the dates will be the days between the interval.    Eg. period=2011, the property will be all months in the year  period=2011-06, the property will be all days in month   start_date=2021-06-15, end_date=2021-06-30, the properties will be all days between the interval      If no data is available for the summary report an empty data object is returned.      
### Errors for GET `/reports/summary/{dimension}`  
| HTTP code  | Error code  | Type  | Description  |  
|:------------:|:------------:|:------------:| ------------ |  
|  400 | 1829  |  invalid_param  |  Invalid dimension. Accepted dimensions: source, channel, country, traffic, delivery |    

|  400 | 1820  |  invalid_param  |  The parameter `period` is not a valid date (format Y-m or Y) |  

|  400 | 1821  |  invalid_param  |  The parameter `start_date` is not a valid date |  

|  400 | 1822  |  invalid_param  |  The parameter `end_date` is not a valid date |  

|  400 | 1823  |  invalid_param  |  The end date is before the start date |  

|  400 | 1824  |  invalid_param  |  No `period` parameter or interval (`start_date`, `end_date`) |  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.get_summary_reports(dimension, period, start_date, end_date, async_req=True)
        >>> result = thread.get()

        Args:
            dimension (str): Dimension for wich the summary report is requested
            period (str): Period for the requested report in format **Y-M** or **Y**
            start_date (str): The start date of the report in format Y-M-D
            end_date (str): The end date of the report in format Y-M-D

        Keyword Args:
            limit (int): A limit on the number of objects to be returned. [optional] if omitted the server will use the default value of 500
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
            GetSummaryReports200Response
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
        kwargs['dimension'] = \
            dimension
        kwargs['period'] = \
            period
        kwargs['start_date'] = \
            start_date
        kwargs['end_date'] = \
            end_date
        return self.get_summary_reports_endpoint.call_with_http_info(**kwargs)

