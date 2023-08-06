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
    from smscx_client.model.group import Group
    from smscx_client.model.status import Status
    globals()['Group'] = Group
    globals()['Status'] = Status


class DataReportsCampaigns(ModelNormal):


    allowed_values = {
        ('source',): {
            'API': "api",
            'WEBAPP': "webapp",
            'SMPP': "smpp",
            'PLUGIN': "plugin",
            'ALERTS': "alerts",
            'EXCEL': "excel",
        },
        ('channel',): {
            'SMS': "sms",
            'VIBER': "viber",
            'WHATSAPP': "whatsapp",
        },
    }

    validations = {
        ('id',): {
            'max_length': 36,
            'min_length': 36,
            'regex': {
                'pattern': r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$',  # noqa: E501
            },
        },
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
            'id': (str,),  # noqa: E501
            'name': (str,),  # noqa: E501
            '_from': (str,),  # noqa: E501
            'groups': ([Group],),  # noqa: E501
            'total_phone_numers': (int,),  # noqa: E501
            'parts': (int,),  # noqa: E501
            'cost': (float,),  # noqa: E501
            'text': (str,),  # noqa: E501
            'source': (str,),  # noqa: E501
            'channel': (str,),  # noqa: E501
            'datetime_added': (datetime,),  # noqa: E501
            'datetime_scheduled': (datetime, none_type,),  # noqa: E501
            'status': (Status,),  # noqa: E501
        }

    @cached_property
    def discriminator():
        return None


    attribute_map = {
        'id': 'id',  # noqa: E501
        'name': 'name',  # noqa: E501
        '_from': 'from',  # noqa: E501
        'groups': 'groups',  # noqa: E501
        'total_phone_numers': 'totalPhoneNumers',  # noqa: E501
        'parts': 'parts',  # noqa: E501
        'cost': 'cost',  # noqa: E501
        'text': 'text',  # noqa: E501
        'source': 'source',  # noqa: E501
        'channel': 'channel',  # noqa: E501
        'datetime_added': 'datetimeAdded',  # noqa: E501
        'datetime_scheduled': 'datetimeScheduled',  # noqa: E501
        'status': 'status',  # noqa: E501
    }

    read_only_vars = {
    }

    _composed_schemas = {}

    @classmethod
    @convert_js_args_to_python_args
    def _from_api_data(cls, id, name, _from, groups, total_phone_numers, parts, cost, text, source, channel, datetime_added, datetime_scheduled, *args, **kwargs):  # noqa: E501
        """DataReportsCampaigns - a model

        Args:
            id (str): Unique identifier of the campaign
            name (str): Name of the sent campaign
            _from (str): Originator (sender name) of the message 
            groups ([Group]): 
            total_phone_numers (int): Total recipients of the sent campaign
            parts (int): Total parts of the sent campaign
            cost (float): Total cost of the sent campaign 
            text (str): Content of the message
            source (str): Source of the message sending
            channel (str): Channel that sent the message
            datetime_added (datetime):
            datetime_scheduled (datetime, none_type):


            status (Status): [optional]  # noqa: E501
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

        self.id = id
        self.name = name
        self._from = _from
        self.groups = groups
        self.total_phone_numers = total_phone_numers
        self.parts = parts
        self.cost = cost
        self.text = text
        self.source = source
        self.channel = channel
        self.datetime_added = datetime_added
        self.datetime_scheduled = datetime_scheduled
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
    def __init__(self, id, name, _from, groups, total_phone_numers, parts, cost, text, source, channel, datetime_added, datetime_scheduled, *args, **kwargs):  # noqa: E501
        """DataReportsCampaigns - a model

        Args:
            id (str): Unique identifier of the campaign
            name (str): Name of the sent campaign
            _from (str): Originator (sender name) of the message 
            groups ([Group]): 
            total_phone_numers (int): Total recipients of the sent campaign
            parts (int): Total parts of the sent campaign
            cost (float): Total cost of the sent campaign 
            text (str): Content of the message
            source (str): Source of the message sending
            channel (str): Channel that sent the message
            datetime_added (datetime):
            datetime_scheduled (datetime, none_type):


            status (Status): [optional]  # noqa: E501
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

        self.id = id
        self.name = name
        self._from = _from
        self.groups = groups
        self.total_phone_numers = total_phone_numers
        self.parts = parts
        self.cost = cost
        self.text = text
        self.source = source
        self.channel = channel
        self.datetime_added = datetime_added
        self.datetime_scheduled = datetime_scheduled
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
