# smscx_client

The SMS Connexion API Python library provides convenient access to the SMS API of SMS.CX from applications written in Python language.

Using this library you can send single or bulk SMS, create groups of contacts, import contacts, validate phone numbers, lookup phone numbers, send OTP SMS (2 factor authentication), create short links, and more.
  
For more information, please visit [https://sms.cx](https://sms.cx)

## Installation

### Requirements

Python >=3.6

### pip install

Install the python package using:

```sh
pip install smscx_client
```
(you may need to run `pip` with root permission: `sudo pip install smscx_client`)

Then import the package:
```python
import smscx_client
```

### Setuptools

Install via [Setuptools](http://pypi.python.org/pypi/setuptools).

```sh
python setup.py install --user
```
(or `sudo python setup.py install` to install the package for all users)

Then import the package:
```python
import smscx_client
```

## Authentication

To use the library you must authenticate. SMS.CX PHP Library supports the authentication methods supported by the SMS Connexion API:
 - [API Key](#1-api-key)
 - [Oauth2 Access Token](#2-oauth2-access-token)

### 1. API Key

To create a new API Key go to [SMS.CX Account > HTTP API > API Keys](https://account.sms.cx/) and click on **New API Key**.

![Create new API KEY from SMS.CX Dashboard](https://sms.cx/assets/img/docs/dashboard-apikeys.png) 

Copy the API Key and use it in this client library.


### 2. Oauth2 Access Token

Access tokens are used by applications to make API requests.

To create a new application go to [SMS.CX Account > HTTP API > Applications](https://account.sms.cx/) and click on **New Application**.  

When you have the Application ID and Application Secret, you can use them to request an access token that you can use to make API calls.


![Create new application from SMS.CX Dashboard](https://sms.cx/assets/img/docs/dashboard-tokens.png)  

Copy the `APPLICATION_ID` and `APPLICATION_SECRET` and use them to request an access token:

```python
import time
import smscx_client
from smscx_client.api import oauth_api
from smscx_client.model.oauth_token_response import OauthTokenResponse
from pprint import pprint

configuration = smscx_client.Configuration(
    username = "YOUR_APPLICATION_ID",
    password = "YOUR_APPLICATION_SECRET"
)

# Create an instance of the API class
api_instance = oauth_api.OauthApi(
    smscx_client.ApiClient(configuration)
)

# A list of space-delimited, case-sensitive strings
# If left empty or ommited, the issued access token will be granted with all scopes (full privileges) (optional)
scope = "sms groups templates numbers shortlinks attachments"

try:
    # Get access token
    api_response = api_instance.get_access_token(scope=scope)
    pprint(api_response)
    access_token = api_response.access_token
    expires_in = api_response.expires_in
except smscx_client.InvalidRequestException as e:
    # Code for invalid request # noqa: E501
except smscx_client.InvalidCredentialsException as e:
    # Code for invalid credentials # noqa: E501
except smscx_client.InvalidScopeException as e:
    # Code for invalid scope # noqa: E501
except smscx_client.ApiException as e:
    print("Exception when calling OauthApi->get_access_token: %s\n" % e)
    error_response = json.loads(e.body)
    error_type = error_response['error']['type']
    error_code = error_response['error']['code']
    error_msg = error_response['error']['message']          
    http_code = e.status     
```

Access tokens provide three main security benefits over using an API Key:

- **Revocable access**. Access tokens can be revoked, removing access for only that token without having to change your API Key everywhere.
- **Limited access**. Access tokens have access scopes which allow for more granular access to API resources. For instance, you can grant access only to send SMS but not to get groups of contacts.
- **Short lifetime**. Access tokens have an expire time (1 day, 1 week) which reduces the risk of the token being compromised.


## Usage

The library needs to be configured with your account's Application ID & secret or API Key which are available in your SMS.CX Dashboard. 

The following example will send SMS to a single phone number:

```python
import time
import smscx_client
from smscx_client.api import sms_api
from smscx_client.model.send_sms_message_request import SendSmsMessageRequest
from smscx_client.model.send_sms_message_response import SendSmsMessageResponse
from pprint import pprint

configuration = smscx_client.Configuration(
    # Use authentication via API Key
    api_key = "YOUR_API_KEY",

    # Uncomment to use authentication via Access Token
    # access_token = "YOUR_ACCESS_TOKEN",
)

# Create an instance of the API class
api_instance = sms_api.SmsApi(
    smscx_client.ApiClient(configuration)
)
send_sms_message_request = SendSmsMessageRequest(
    to=["+31612469xxx"],
    _from = "InfoText",
    text = "Your confirmation code is 15997",
)

try:
    # Send single SMS
    api_response = api_instance.send_sms(send_sms_message_request)
    pprint(api_response)
    # api_response.info.total_cost
    for item in api_response.data:
        # item.msg_id
except smscx_client.NoCoverageException as e:
    # Code for No coverage
except smscx_client.InvalidRequestException as e:
    # Code for invalid request
except smscx_client.InvalidPhoneNumberException as e:
    # Code for invalid phone number
except smscx_client.InsufficientBalanceException as e:
    # Code for insufficient balance                                              
except smscx_client.ApiException as e:
    print("Exception when calling SmsApi->send_sms: %s\n" % e)
    error_response = json.loads(e.body)
    error_response = json.loads(e.body)
    error_type = error_response['error']['type']
    error_code = error_response['error']['code']
    error_msg = error_response['error']['message']          
    http_code = e.status
```

### Example of bulk SMS sending (up to 25.000 destination phone numbers)

```python
import time
import smscx_client
from smscx_client.api import sms_api
from smscx_client.model.send_sms_message_request import SendSmsMessageRequest
from smscx_client.model.send_sms_message_response import SendSmsMessageResponse
from pprint import pprint

configuration = smscx_client.Configuration(
    # Use authentication via API Key
    api_key = "YOUR_API_KEY",

    # Uncomment to use authentication via Access Token
    # access_token = "YOUR_ACCESS_TOKEN",
)

# Create an instance of the API class
api_instance = sms_api.SmsApi(
    smscx_client.ApiClient(configuration)
)

send_sms_message_request = SendSmsMessageRequest(
    to=[
        "+31612469xxx", 
        "+4474005085xx", 
        "+49151238353xx", 
        "+417811126xx", 
        "+3519123350xx", 
        "+4206016090xx",
        "+359483059xx",
        "+336127904xx",
        "+436645595xx",
        "+3519121385xx",
        "+3069125917xx",
    ],
    _from="InfoText",
    text="Redeem this voucher and you will get 30% discount off all Summer Fashion ",
    idempotency_id="bf325375-e030-fccb-a009-17317c574773",
    transliteration=Transliteration(
        alphabet="NONE",
        remove_emojis=False,
    ),        
)

try:
    # Send SMS
    api_response = api_instance.send_sms(send_sms_message_request)
    pprint(api_response)
    # api_response.info.total_cost
    for item in api_response.data:
        # item.msg_id
except smscx_client.NoCoverageException as e:
    # Code for No coverage
except smscx_client.InvalidRequestException as e:
    # Code for invalid request
except smscx_client.InvalidPhoneNumberException as e:
    # Code for invalid phone number
except smscx_client.InsufficientBalanceException as e:
    # Code for insufficient balance                                              
except smscx_client.ApiException as e:
    print("Exception when calling SmsApi->send_sms: %s\n" % e)
    error_response = json.loads(e.body)
    error_type = error_response['error']['type']
    error_code = error_response['error']['code']
    error_msg = error_response['error']['message']          
    http_code = e.status
```

## Handling errors

With this client library, you don’t need to check for non-200 HTTP responses. The library translates them as exceptions.  

In some specific rare cases you may need to analyze the [Error object](#) for `type` and `code` properties.  

To handle errors, use these two techniques:

- Catch Exceptions (recommended)
- Analyze and handle the [Error object](#) provided in the response body

### 1. Catch Exceptions

The SMS.CX Python library raises an exception for every error type. It is recommended to catch and handle exceptions.

To catch an exception, use Python’s `try`/`except` syntax. SMS Connexion provides many exception classes you can catch. Each one represents a different kind of error. When you catch an exception, you can use its class to choose a response.

#### General exceptions:
- `DuplicateIdException` - A resource with the same ID already exist
- `DuplicateValueException` - You are trying to create/update a resource that must be unique (eg. originators, group name, shortlinks, template name)
- `InsufficientScopeException` - Your application does not have the privilege to access a resource
- `InvalidCredentialsException` - Unable to authenticate you based on the information provided. 
- `InvalidRequestException` - The parameters provided were invalid
- `InvalidScopeException` - The scope requested does not exist
- `RateLimitExcedeedException` - You made too many API calls in short period of time.
- `ResourceNotFoundException` - The ID of the requested resource was not found (eg. group, campaign, otp, shortlink, template, etc.)
- `ApiMethodNotAllowedException` - The target resource doesn’t support this HTTP method
- `AccessDeniedException` - You don’t have permission to perform an action (eg. editing a template that was locked, replying to an Whatsapp after more than 24 hours passed from client reply, etc.)
- `ServerErrorException` - Something went wrong on SMS Connexion’s side.
- `ApiException` - Something went wrong on SMS Connexion’s side

#### Exceptions for methods that validate numbers or incur costs (to send SMS, add phone numbers to groups, validate number, etc.):
- `InsufficientBalanceException` - Your request incurs charges in excess of your existing balance. 
- `InvalidPhoneNumberException` - The phone number provided is not valid

#### Exceptions for methods that require network coverage (send SMS, Viber, Whatsapp):
- `NoCoverageException` - There is no coverage for the destination requested (these are rare)

#### Exceptions for Otp:
- `InvalidPinException` - The PIN provided does not verify with our records
- `OtpAlreadyVerifiedException` - The OTP was already verified
- `OtpCancelledException` - You cannot verify an OTP that was cancelled
- `OtpActionNotAllowedException` - You cannot cancel an OTP that has non-pending status (eg. was already verified, canceled, or expired)
- `OtpExpiredException` - You cannot verify an OTP that was expired
- `OtpFailedException` - The OTP verification has failed because the numbers of max attempts was reached

#### Exceptions for Viber/Whatsapp:
- `ChannelNotActiveException` - Channel is not active. You need to register Viber and Whatsapp by contacting us
- `TemplateNotApprovedException` - Template for sending Viber or Whatsapp is not approved

### 2. Analyze Error object

The error object ( [**Error**](docs/model/Error.md) ), which is present in all Exceptions, store information about failures. 

If you don’t want to rely on our existing Exceptions, you might need to analyze the details of the Error object.  

You can retrieve the error object and examine it to learn more about the failure. Choose an appropriate response according on the error type. Check the examples provided to learn how to get the HTTP code and the error object.

A range of different error types are returned by the API, correlated with their HTTP codes:
- HTTP 400 Bad Request for error type `invalid_param`, `insufficient_credit`
- HTTP 401 Unauthorized for `invalid_api_key`, `invalid_client`
- HTTP 404 Not Found for `not_found`
- HTTP 429 Too Many Requests for `rate_limit`

Read the complete list of [error types and codes](https://sms.cx/sms-api-documentation/#section/Errors) from the API specification.

### Example of error handling

```python
try:
    # Method
except smscx_client.InvalidRequestException as e:
    # Code for invalid request
except smscx_client.RateLimitExcedeedException as e:
    # Wait some time and retry the request
    retry_after = e.headers['X-Rate-Limit-Reset']; # Unix timestamp eg. 1664103086
except smscx_client.ServerErrorException as e:
    # Code for this situation                                        
except smscx_client.ApiException as e:
    # If you want to analyze the Error object
    error_response = json.loads(e.body)
    error_type = error_response['error']['type']
    error_code = error_response['error']['code']
    error_msg = error_response['error']['message']          
    http_code = e.status
```

In special cases, when using methods to validate phone numbers in bulk or when adding phone numbers to an existing group, the `Error` object will contain a [**list with invalid**](docs/model/Model400InvalidPhoneNumbers.md) phone numbers (if the parameter `allowInvalid` was not set to true or if not a single valid number was detected).

```python
x = json.loads(e.body)
invalid_phone_numbers = x['error']['invalid'];
"""
Returns list of invalid numbers:
[
  "+336123",
  "+336123",
  "+441589945xx",
  "+396778143xx",
  "+3362599873xx",
]
"""
```

## Rate limit

To detect an API rate limit error, you can catch the Exception `RateLimitExcedeedException` or check the Error object for error type `rate_limit` or check if the HTTP code is `429`:

```python
try:
    # Method
except smscx_client.RateLimitExcedeedException as e:
    # Rate limited
    retry_after = e.headers['X-Rate-Limit-Reset']; # Unix timestamp eg. 1664103086
```

## Documentation 
Full documentation of the API is available [here](https://sms.cx/sms-api-documentation/).  
The [docs folder](/docs) provides detailed guides for using this library (methods, models, examples).
The [examples folder](/examples) provides an example for each method.



## Available methods

Read the documentation for each method to get more examples, complete parameter list, expected responses and list of error codes.



### Class AccountApi

Method | Description
| ------------- | -------------
| [**get_account_balance()**](docs/api/AccountApi.md#get_account_balance) | Get account balance
| [**get_channel_pricing()**](docs/api/AccountApi.md#get_channel_pricing) | Get channels pricing
| [**get_channel_pricing_by_country_iso()**](docs/api/AccountApi.md#get_channel_pricing_by_country_iso) | Get pricing for channel by country iso
| [**get_channels_status()**](docs/api/AccountApi.md#get_channels_status) | Get status of all channels



### Class ApplicationsApi

Method | Description
| ------------- | -------------
| [**get_application_settings()**](docs/api/ApplicationsApi.md#get_application_settings) | Get application settings
| [**get_applications_list()**](docs/api/ApplicationsApi.md#get_applications_list) | Get applications list
| [**get_scopes()**](docs/api/ApplicationsApi.md#get_scopes) | Get scopes



### Class AttachmentsApi

Method | Description
| ------------- | -------------
| [**delete_attachment()**](docs/api/AttachmentsApi.md#delete_attachment) | Delete attachment
| [**export_attachment_hits_to_csv()**](docs/api/AttachmentsApi.md#export_attachment_hits_to_csv) | Export attachment hits to CSV
| [**export_attachment_hits_to_xlsx()**](docs/api/AttachmentsApi.md#export_attachment_hits_to_xlsx) | Export attachment hits to XLSX
| [**get_attachment_hits()**](docs/api/AttachmentsApi.md#get_attachment_hits) | Get attachment hits
| [**get_attachments_list()**](docs/api/AttachmentsApi.md#get_attachments_list) | Get attachments list



### Class ConversationsApi

Method | Description
| ------------- | -------------
| [**get_conversation()**](docs/api/ConversationsApi.md#get_conversation) | Get conversation
| [**get_converstions_list()**](docs/api/ConversationsApi.md#get_converstions_list) | Get conversations list
| [**mark_conversation_as_read()**](docs/api/ConversationsApi.md#mark_conversation_as_read) | Mark conversation as read
| [**send_conversation_reply_sms()**](docs/api/ConversationsApi.md#send_conversation_reply_sms) 💰 | Send conversation reply via SMS
| [**send_conversation_reply_viber()**](docs/api/ConversationsApi.md#send_conversation_reply_viber) 💰 | Send conversation reply via Viber
| [**send_conversation_reply_whatsapp()**](docs/api/ConversationsApi.md#send_conversation_reply_whatsapp) 💰 | Send conversation reply via Whatsapp



### Class GroupsApi

Method | Description
| ------------- | -------------
| [**add_contacts_to_group()**](docs/api/GroupsApi.md#add_contacts_to_group) | Add contacts to group
| [**create_group()**](docs/api/GroupsApi.md#create_group) | Create new group
| [**delete_contact_from_group()**](docs/api/GroupsApi.md#delete_contact_from_group) | Delete contact from group
| [**delete_group()**](docs/api/GroupsApi.md#delete_group) | Delete group
| [**empty_group()**](docs/api/GroupsApi.md#empty_group) | Empty group
| [**export_group_to_csv()**](docs/api/GroupsApi.md#export_group_to_csv) | Export group to CSV
| [**export_group_to_xlsx()**](docs/api/GroupsApi.md#export_group_to_xlsx) | Export group to XLSX
| [**get_group_details()**](docs/api/GroupsApi.md#get_group_details) | Get group details
| [**get_groups_list()**](docs/api/GroupsApi.md#get_groups_list) | Get list of groups
| [**update_contact_from_group()**](docs/api/GroupsApi.md#update_contact_from_group) | Update contact from group



### Class MultichannelApi

Method | Description
| ------------- | -------------
| [**delete_scheduled_multichannel_campaign()**](docs/api/MultichannelApi.md#delete_scheduled_multichannel_campaign) | Delete scheduled Multichannel campaign
| [**delete_scheduled_multichannel_message()**](docs/api/MultichannelApi.md#delete_scheduled_multichannel_message) | Delete scheduled Multichannel message
| [**estimate_multichannel_campaign()**](docs/api/MultichannelApi.md#estimate_multichannel_campaign) | Estimate Multichannel campaign
| [**estimate_multichannel_message()**](docs/api/MultichannelApi.md#estimate_multichannel_message)  | Estimate Multichannel message
| [**send_multichannel_campaign()**](docs/api/MultichannelApi.md#send_multichannel_campaign) 💰 | Send Multichannel campaign
| [**send_multichannel_message()**](docs/api/MultichannelApi.md#send_multichannel_message) 💰 | Send Multichannel message



### Class NumbersApi

Method | Description
| ------------- | -------------
| [**get_bulk_lookup_status()**](docs/api/NumbersApi.md#get_bulk_lookup_status) | Get Bulk Lookup result
| [**get_single_lookup_status()**](docs/api/NumbersApi.md#get_single_lookup_status) | Get Single Lookup result
| [**lookup_number()**](docs/api/NumbersApi.md#lookup_number) 💰 | Lookup number
| [**lookup_numbers()**](docs/api/NumbersApi.md#lookup_numbers) 💰 | Lookup numbers in bulk
| [**validate_number()**](docs/api/NumbersApi.md#validate_number) | Validate number
| [**validate_numbers()**](docs/api/NumbersApi.md#validate_numbers) | Validate numbers in bulk
| [**get_available_numbers()**](docs/api/NumbersApi.md#get_available_numbers) | Get available numbers for rent
| [**rent_number()**](docs/api/NumbersApi.md#rent_number) 💰 | Rent phone number
| [**cancel_rent()**](docs/api/NumbersApi.md#cancel_rent) | Cancel rent for phone number
| [**renew_rent()**](docs/api/NumbersApi.md#renew_rent) 💰 | Renew rent for phone number
| [**get_rent_status()**](docs/api/NumbersApi.md#get_rent_status) | Get status of rent
| [**get_rented_numbers()**](docs/api/NumbersApi.md#get_rented_numbers) | Get list of your rented numbers
| [**get_inbound_sms()**](docs/api/NumbersApi.md#get_inbound_sms) | Get inbound SMS from rented number



### Class OauthApi

Method | Description
| ------------- | -------------
| [**get_access_token()**](docs/api/OauthApi.md#get_access_token) | Get access token



### Class OptoutsApi

Method | Description
| ------------- | -------------
| [**add_contact_to_optouts_list()**](docs/api/OptoutsApi.md#add_contact_to_optouts_list) | Add contact to optouts list
| [**delete_contact_from_optouts_list()**](docs/api/OptoutsApi.md#delete_contact_from_optouts_list) | Delete contact from optouts list
| [**export_optouts_to_csv()**](docs/api/OptoutsApi.md#export_optouts_to_csv) | Export optouts to CSV
| [**export_optouts_to_xlsx()**](docs/api/OptoutsApi.md#export_optouts_to_xlsx) | Export optouts to XLSX
| [**get_optouts_list()**](docs/api/OptoutsApi.md#get_optouts_list) | Get optouts list



### Class OriginatorsApi

Method | Description
| ------------- | -------------
| [**create_originator()**](docs/api/OriginatorsApi.md#create_originator) | Create new originator
| [**delete_originator()**](docs/api/OriginatorsApi.md#delete_originator) | Delete originator
| [**get_originators_list()**](docs/api/OriginatorsApi.md#get_originators_list) | Get originators list



### Class OtpApi

Method | Description
| ------------- | -------------
| [**cancel_otp()**](docs/api/OtpApi.md#cancel_otp) | Cancel OTP
| [**get_otp_status()**](docs/api/OtpApi.md#get_otp_status) | Get OTP status
| [**new_otp()**](docs/api/OtpApi.md#new_otp) 💰 | New OTP
| [**verify_otp()**](docs/api/OtpApi.md#verify_otp) | Verify OTP



### Class ReportsApi

Method | Description
| ------------- | -------------
| [**export_advanced_report_to_csv()**](docs/api/ReportsApi.md#export_advanced_report_to_csv) | Export advanced report to CSV
| [**export_advanced_report_to_xlsx()**](docs/api/ReportsApi.md#export_advanced_report_to_xlsx) | Export advanced report to XLSX
| [**export_campaign_report_to_csv()**](docs/api/ReportsApi.md#export_campaign_report_to_csv) | Export campaign report to CSV
| [**export_campaign_report_to_xlsx()**](docs/api/ReportsApi.md#export_campaign_report_to_xlsx) | Export campaign report to XLSX
| [**get_advanced_report()**](docs/api/ReportsApi.md#get_advanced_report) | Get advanced report
| [**get_campaign_report()**](docs/api/ReportsApi.md#get_campaign_report) | Get campaign report
| [**get_campaigns_list()**](docs/api/ReportsApi.md#get_campaigns_list) | Get list of sent campaigns
| [**get_single_report()**](docs/api/ReportsApi.md#get_single_report) | Get report for single SMS or Viber or Whatsapp or Multichannel
| [**get_summary_reports()**](docs/api/ReportsApi.md#get_summary_reports) | Get summary reports for a dimension



### Class ShortlinksApi

Method | Description
| ------------- | -------------
| [**create_shortlink()**](docs/api/ShortlinksApi.md#create_shortlink) | Create shortlink
| [**delete_shortlink()**](docs/api/ShortlinksApi.md#delete_shortlink) | Delete shortlink
| [**export_shortlink_hits_to_csv()**](docs/api/ShortlinksApi.md#export_shortlink_hits_to_csv) | Export shortlink hits to CSV
| [**export_shortlink_hits_to_xlsx()**](docs/api/ShortlinksApi.md#export_shortlink_hits_to_xlsx) | Export shortlink hits to XLSX
| [**get_shortlink_hits()**](docs/api/ShortlinksApi.md#get_shortlink_hits) | Get shortlink hits
| [**get_shortlinks_list()**](docs/api/ShortlinksApi.md#get_shortlinks_list) | Get shortlinks list
| [**update_shortlink()**](docs/api/ShortlinksApi.md#update_shortlink) | Update shortlink



### Class SmsApi

Method | Description
| ------------- | -------------
| [**delete_scheduled_sms()**](docs/api/SmsApi.md#delete_scheduled_sms) | Delete scheduled SMS
| [**delete_scheduled_sms_campaign()**](docs/api/SmsApi.md#delete_scheduled_sms_campaign) | Delete scheduled SMS campaign
| [**estimate_sms()**](docs/api/SmsApi.md#estimate_sms) | Estimate new SMS
| [**estimate_sms_campaign()**](docs/api/SmsApi.md#estimate_sms_campaign) | Estimate SMS campaign
| [**send_sms()**](docs/api/SmsApi.md#send_sms) 💰 | Send SMS
| [**send_sms_campaign()**](docs/api/SmsApi.md#send_sms_campaign) 💰 | Send SMS campaign



### Class TemplatesApi

Method | Description
| ------------- | -------------
| [**create_template()**](docs/api/TemplatesApi.md#create_template) | Create template
| [**delete_template()**](docs/api/TemplatesApi.md#delete_template) | Delete template
| [**get_template()**](docs/api/TemplatesApi.md#get_template) | Get template
| [**get_templates_list()**](docs/api/TemplatesApi.md#get_templates_list) | Get templates list
| [**update_template()**](docs/api/TemplatesApi.md#update_template) | Update template



### Class ViberApi

Method | Description
| ------------- | -------------
| [**delete_scheduled_viber_campaign()**](docs/api/ViberApi.md#delete_scheduled_viber_campaign) | Delete scheduled Viber campaign
| [**delete_scheduled_viber_message()**](docs/api/ViberApi.md#delete_scheduled_viber_message) | Delete scheduled Viber message
| [**estimate_viber_campaign()**](docs/api/ViberApi.md#estimate_viber_campaign) | Estimate Viber campaign
| [**estimate_viber_message()**](docs/api/ViberApi.md#estimate_viber_message) | Estimate Viber message
| [**send_viber_campaign()**](docs/api/ViberApi.md#send_viber_campaign) 💰 | Send Viber campaign
| [**send_viber_message()**](docs/api/ViberApi.md#send_viber_message) 💰 | Send Viber message



### Class WhatsappApi

Method | Description
| ------------- | -------------
| [**delete_scheduled_whatsapp_message()**](docs/api/WhatsappApi.md#delete_scheduled_whatsapp_message) | Delete scheduled Whatsapp message
| [**estimate_whatsapp_message()**](docs/api/WhatsappApi.md#estimate_whatsapp_message) | Estimate Whatsapp message
| [**send_whatsapp_message()**](docs/api/WhatsappApi.md#send_whatsapp_message) 💰 | Send Whatsapp message




## Documentation For Authorization


## ApiKeyAuth

- **Type**: API key
- **API key parameter name**: X-API-KEY
- **Location**: HTTP header


## BasicAuth

- **Type**: HTTP basic authentication


## BearerAuth

- **Type**: Bearer authentication



## Author

dev@sms.cx

## About this package

- Client library version: `0.1.0`
- API version: `1.0.2`

## License

[Apache 2.0](LICENSE) © 2022 SMS Connexion