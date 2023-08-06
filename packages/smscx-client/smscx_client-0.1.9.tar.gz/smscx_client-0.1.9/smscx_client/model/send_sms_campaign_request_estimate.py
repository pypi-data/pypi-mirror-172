import re  # noqa: F401
import sys  # noqa: F401

from smscx_client.model_utils import (  # noqa: F401
    ApiTypeError,
    ModelComposed,
    ModelNormal,
    ModelSimple,
    cached_property,
    change_keys_js_to_python,
    convert_js_args_to_python_args,
    date,
    datetime,
    file_type,
    none_type,
    validate_get_composed_info,
    ApiModel
)
from smscx_client.exceptions import ApiAttributeError


def lazy_import():
    from smscx_client.model.transliteration import Transliteration
    globals()['Transliteration'] = Transliteration


class SendSmsCampaignRequestEstimate(ModelNormal):


    allowed_values = {
    }

    validations = {
        ('_from',): {
            'max_length': 15,
            'min_length': 3,
        },
    }

    @cached_property
    def additional_properties_type():
        lazy_import()
        return (bool, date, datetime, dict, float, int, list, str, none_type,)  # noqa: E501

    _nullable = False

    @cached_property
    def api_types():
        """
        Returns
            api_types (dict): The key is attribute name
                and the value is attribute type.
        """
        lazy_import()
        return {
            'groups': ([int],),  # noqa: E501
            '_from': (str,),  # noqa: E501
            'text': (str,),  # noqa: E501
            'scheduled_date': (datetime,),  # noqa: E501
            'is_utc': (bool,),  # noqa: E501
            'dlr_callback_url': (str,),  # noqa: E501
            'short_response': (bool,),  # noqa: E501
            'no_text_details': (bool,),  # noqa: E501
            'show_timezone': (bool,),  # noqa: E501
            'transliteration': (Transliteration,),  # noqa: E501
        }

    @cached_property
    def discriminator():
        return None


    attribute_map = {
        'groups': 'groups',  # noqa: E501
        '_from': 'from',  # noqa: E501
        'text': 'text',  # noqa: E501
        'scheduled_date': 'scheduledDate',  # noqa: E501
        'is_utc': 'isUtc',  # noqa: E501
        'dlr_callback_url': 'dlrCallbackUrl',  # noqa: E501
        'short_response': 'shortResponse',  # noqa: E501
        'no_text_details': 'noTextDetails',  # noqa: E501
        'show_timezone': 'showTimezone',  # noqa: E501
        'transliteration': 'transliteration',  # noqa: E501
    }

    read_only_vars = {
    }

    _composed_schemas = {}

    @classmethod
    @convert_js_args_to_python_args
    def _from_api_data(cls, groups, _from, text, *args, **kwargs):  # noqa: E501
        """SendSmsCampaignRequestEstimate - a model

        Args:
            groups ([int]): An array of identifiers for groups of contacts
            _from (str): The originator (sender name) of the text message (min 3, max 15 characters). If the originator used in this value is not approved, it will be overwritten by a default system originator (eg. InfoText). Read more about [sender names](#)
            text (str): A standard GSM message is limited to 160 characters. If a text message contains even one (or more) Unicode characters (for example ç, ö, ü) the character limit then becomes 70 characters per message part. Long text messages are concatenated into a multipart SMS. A text message can have up to 1530 characters (10 message parts).   <br><br>   You can use custom fields in the text, by using the name of the field between two curly braces. The placeholders will be replaced with the availale data. If no data is found the placeholder will be replaced by a blank string. Available fields are:   - `{{firstName}}` - will be replaced with data saved when the contact was added to group  - `{{lastName}}` - will be replaced with data saved when the contact was added to group  - `{{email}}` - will be replaced with data saved when the contact was added to group  - `{{field1}}` - `{{field5}}` - will be replaced with data saved when the contact was added to group<br>   - `{{<CUSTOM-FIELD>}}` - Eg. **{{height}}** cand be used as placeholder if this custom field was added when [validating the contact to a group](#add-contacts-to-a-group)   - `{{optoutLink}}`  - `{{shortlink:<ID>}}`  - `{{attachement:<ID>}}`  <br> <br>   The placeholder `{{shortlink:<ID>}}` is used when you want to track a shortlink. The API will generate a unique string for every contact, and doing so you will know what phone number clicked on the link. Eg. `{{shortlink:bVc}}` will be replaced by **ht<span>tps://</span>en.ax/bVc/r2N**  <br><br>  General placeholders can be used in the text, which will be replaced with data. Available general placeholders are:   - `{{numbers}}` - will be replaced with a random number. Default length of the number is 4 characters. Eg. **9765**  - `{{numbers:8}}` - will be replaced with a random number with length of 8 characters. The minimum number length can be 1 and maximum length can be 20  - `{{letters}}` - will be replaced with a random string of letters. Default length of the string is 4 characters. Eg. **AJKV**  - `{{letters:10}}` - will be replaced with a random string with length of 10 characters. The minimum string length can be 1 and maximum length can be 20  - `{{alphanumeric}}` - will be replaced with a random string of letters and numbers. Default length of the string is 4 characters. Eg. **BH4V**  - `{{alphanumeric:6}}` - will be replaced with a random string of letters and numbers with length of 6 characters. The minimum alphanumeric string length can be 1 and maximum length can be 20  - `{{today}}` - will be replaced with today date in following example format: **7 Aug 2022**


            scheduled_date (datetime): If you want to schedule the SMS at a later date. The date provided must be in format **YYYY-MM-DD HH:MM:SS** (Eg. 2021-06-23 14:26:10). By default, the date and time in this parameter is treated as `UTC`. So if you want to schedule a SMS to a french phone number at 16:00 (France is UTC+2), then you should set the parameter at 2021-06-23 14:00 (UTC). If you don't want to make the calculations, you can set this parameter as the date time of the destination (eg. 2021-06-23 16:00) and set the parameter `isUtc` to `false`. In this way, the API will automatically make the conversion from the destination timezone to UTC and set the scheduledDate accordingly. [optional]  # noqa: E501
            is_utc (bool): If set to `false` it will indicate that the `scheduledDate` parameter is not a date in UTC time, but the date relative to the timezone of the destination phone number. The API will calculate the offset and convert the date to UTC.  . [optional] if omitted the server will use the default value of True  # noqa: E501
            dlr_callback_url (str): A valid URL to receive the delivery report update for the sent SMS. If this parameter is set, it will overwrite the setting from [Admin Dashboard > HTTP API > Oauth2 > Application settings](#). [optional]  # noqa: E501
            short_response (bool): If set to `true`, it will return the full `info` object and empty `data` object. For situations when you don't need the information in the `data` object and want to save bandwith. [optional] if omitted the server will use the default value of False  # noqa: E501
            no_text_details (bool): The response will not have the parameters `data.text` and `data.textAnalysis`. For situations when you send to large lists of phone numbers and don't need all response parameters (save bandwith). [optional] if omitted the server will use the default value of False  # noqa: E501
            show_timezone (bool): Shows the parameter `timezone` in the response, for each phone number. [optional] if omitted the server will use the default value of False  # noqa: E501
            transliteration (Transliteration): [optional]  # noqa: E501
        """

        _check_type = kwargs.pop('_check_type', True)
        _spec_property_naming = kwargs.pop('_spec_property_naming', True)
        _path_to_item = kwargs.pop('_path_to_item', ())
        _configuration = kwargs.pop('_configuration', None)
        _visited_composed_classes = kwargs.pop('_visited_composed_classes', ())

        self = super(ApiModel, cls).__new__(cls)

        if args:
            for arg in args:
                if isinstance(arg, dict):
                    kwargs.update(arg)
                else:
                    raise ApiTypeError(
                        "Invalid positional arguments=%s passed to %s. Remove those invalid positional arguments." % (
                            args,
                            self.__class__.__name__,
                        ),
                        path_to_item=_path_to_item,
                        valid_classes=(self.__class__,),
                    )

        self._data_store = {}
        self._check_type = _check_type
        self._spec_property_naming = _spec_property_naming
        self._path_to_item = _path_to_item
        self._configuration = _configuration
        self._visited_composed_classes = _visited_composed_classes + (self.__class__,)

        self.groups = groups
        self._from = _from
        self.text = text
        for var_name, var_value in kwargs.items():
            if var_name not in self.attribute_map and \
                        self._configuration is not None and \
                        self._configuration.discard_unknown_keys and \
                        self.additional_properties_type is None:
                # discard variable.
                continue
            setattr(self, var_name, var_value)
        return self

    required_properties = set([
        '_data_store',
        '_check_type',
        '_spec_property_naming',
        '_path_to_item',
        '_configuration',
        '_visited_composed_classes',
    ])

    @convert_js_args_to_python_args
    def __init__(self, groups, _from, text, *args, **kwargs):  # noqa: E501
        """SendSmsCampaignRequestEstimate - a model

        Args:
            groups ([int]): An array of identifiers for groups of contacts
            _from (str): The originator (sender name) of the text message (min 3, max 15 characters). If the originator used in this value is not approved, it will be overwritten by a default system originator (eg. InfoText). Read more about [sender names](#)
            text (str): A standard GSM message is limited to 160 characters. If a text message contains even one (or more) Unicode characters (for example ç, ö, ü) the character limit then becomes 70 characters per message part. Long text messages are concatenated into a multipart SMS. A text message can have up to 1530 characters (10 message parts).   <br><br>   You can use custom fields in the text, by using the name of the field between two curly braces. The placeholders will be replaced with the availale data. If no data is found the placeholder will be replaced by a blank string. Available fields are:   - `{{firstName}}` - will be replaced with data saved when the contact was added to group  - `{{lastName}}` - will be replaced with data saved when the contact was added to group  - `{{email}}` - will be replaced with data saved when the contact was added to group  - `{{field1}}` - `{{field5}}` - will be replaced with data saved when the contact was added to group<br>   - `{{<CUSTOM-FIELD>}}` - Eg. **{{height}}** cand be used as placeholder if this custom field was added when [validating the contact to a group](#add-contacts-to-a-group)   - `{{optoutLink}}`  - `{{shortlink:<ID>}}`  - `{{attachement:<ID>}}`  <br> <br>   The placeholder `{{shortlink:<ID>}}` is used when you want to track a shortlink. The API will generate a unique string for every contact, and doing so you will know what phone number clicked on the link. Eg. `{{shortlink:bVc}}` will be replaced by **ht<span>tps://</span>en.ax/bVc/r2N**  <br><br>  General placeholders can be used in the text, which will be replaced with data. Available general placeholders are:   - `{{numbers}}` - will be replaced with a random number. Default length of the number is 4 characters. Eg. **9765**  - `{{numbers:8}}` - will be replaced with a random number with length of 8 characters. The minimum number length can be 1 and maximum length can be 20  - `{{letters}}` - will be replaced with a random string of letters. Default length of the string is 4 characters. Eg. **AJKV**  - `{{letters:10}}` - will be replaced with a random string with length of 10 characters. The minimum string length can be 1 and maximum length can be 20  - `{{alphanumeric}}` - will be replaced with a random string of letters and numbers. Default length of the string is 4 characters. Eg. **BH4V**  - `{{alphanumeric:6}}` - will be replaced with a random string of letters and numbers with length of 6 characters. The minimum alphanumeric string length can be 1 and maximum length can be 20  - `{{today}}` - will be replaced with today date in following example format: **7 Aug 2022**


            scheduled_date (datetime): If you want to schedule the SMS at a later date. The date provided must be in format **YYYY-MM-DD HH:MM:SS** (Eg. 2021-06-23 14:26:10). By default, the date and time in this parameter is treated as `UTC`. So if you want to schedule a SMS to a french phone number at 16:00 (France is UTC+2), then you should set the parameter at 2021-06-23 14:00 (UTC). If you don't want to make the calculations, you can set this parameter as the date time of the destination (eg. 2021-06-23 16:00) and set the parameter `isUtc` to `false`. In this way, the API will automatically make the conversion from the destination timezone to UTC and set the scheduledDate accordingly. [optional]  # noqa: E501
            is_utc (bool): If set to `false` it will indicate that the `scheduledDate` parameter is not a date in UTC time, but the date relative to the timezone of the destination phone number. The API will calculate the offset and convert the date to UTC.  . [optional] if omitted the server will use the default value of True  # noqa: E501
            dlr_callback_url (str): A valid URL to receive the delivery report update for the sent SMS. If this parameter is set, it will overwrite the setting from [Admin Dashboard > HTTP API > Oauth2 > Application settings](#). [optional]  # noqa: E501
            short_response (bool): If set to `true`, it will return the full `info` object and empty `data` object. For situations when you don't need the information in the `data` object and want to save bandwith. [optional] if omitted the server will use the default value of False  # noqa: E501
            no_text_details (bool): The response will not have the parameters `data.text` and `data.textAnalysis`. For situations when you send to large lists of phone numbers and don't need all response parameters (save bandwith). [optional] if omitted the server will use the default value of False  # noqa: E501
            show_timezone (bool): Shows the parameter `timezone` in the response, for each phone number. [optional] if omitted the server will use the default value of False  # noqa: E501
            transliteration (Transliteration): [optional]  # noqa: E501
        """

        _check_type = kwargs.pop('_check_type', True)
        _spec_property_naming = kwargs.pop('_spec_property_naming', False)
        _path_to_item = kwargs.pop('_path_to_item', ())
        _configuration = kwargs.pop('_configuration', None)
        _visited_composed_classes = kwargs.pop('_visited_composed_classes', ())

        if args:
            for arg in args:
                if isinstance(arg, dict):
                    kwargs.update(arg)
                else:
                    raise ApiTypeError(
                        "Invalid positional arguments=%s passed to %s. Remove those invalid positional arguments." % (
                            args,
                            self.__class__.__name__,
                        ),
                        path_to_item=_path_to_item,
                        valid_classes=(self.__class__,),
                    )

        self._data_store = {}
        self._check_type = _check_type
        self._spec_property_naming = _spec_property_naming
        self._path_to_item = _path_to_item
        self._configuration = _configuration
        self._visited_composed_classes = _visited_composed_classes + (self.__class__,)

        self.groups = groups
        self._from = _from
        self.text = text
        for var_name, var_value in kwargs.items():
            if var_name not in self.attribute_map and \
                        self._configuration is not None and \
                        self._configuration.discard_unknown_keys and \
                        self.additional_properties_type is None:
                # discard variable.
                continue
            setattr(self, var_name, var_value)
            if var_name in self.read_only_vars:
                raise ApiAttributeError(f"`{var_name}` is a read-only attribute. Use `from_api_data` to instantiate "
                                     f"class with read only attributes.")
