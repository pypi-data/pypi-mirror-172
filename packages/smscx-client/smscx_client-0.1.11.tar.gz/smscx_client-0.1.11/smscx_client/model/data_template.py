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
    from smscx_client.model.rich_media import RichMedia
    globals()['RichMedia'] = RichMedia


class DataTemplate(ModelNormal):


    allowed_values = {
        ('channel',): {
            'SMS': "sms",
            'VIBER': "viber",
            'WHATSAPP': "whatsapp",
        },
    }

    validations = {
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
            'id': (int,),  # noqa: E501
            'name': (str,),  # noqa: E501
            'text': (str,),  # noqa: E501
            'channel': (str,),  # noqa: E501
            'type': (str, none_type,),  # noqa: E501
            'rich_media': (RichMedia,),  # noqa: E501
            'created_at': (str,),  # noqa: E501
            'approved': (bool,),  # noqa: E501
            'locked': (bool,),  # noqa: E501
        }

    @cached_property
    def discriminator():
        return None


    attribute_map = {
        'id': 'id',  # noqa: E501
        'name': 'name',  # noqa: E501
        'text': 'text',  # noqa: E501
        'channel': 'channel',  # noqa: E501
        'type': 'type',  # noqa: E501
        'rich_media': 'richMedia',  # noqa: E501
        'created_at': 'createdAt',  # noqa: E501
        'approved': 'approved',  # noqa: E501
        'locked': 'locked',  # noqa: E501
    }

    read_only_vars = {
    }

    _composed_schemas = {}

    @classmethod
    @convert_js_args_to_python_args
    def _from_api_data(cls, id, name, text, channel, type, rich_media, created_at, approved, locked, *args, **kwargs):  # noqa: E501
        """DataTemplate - a model

        Args:
            id (int): Identifier of the template
            name (str): Name of the template
            text (str): Text of the template
            channel (str): Channel for wich the template can be used
            type (str, none_type):
            rich_media (RichMedia):
            created_at (str):
            approved (bool): Approval status of the template (for channel `sms` this variable is always `true`)
            locked (bool): If a Viber or Whatsapp template is approved it cannot be edited, so this parameter will be **true**


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
        self.text = text
        self.channel = channel
        self.type = type
        self.rich_media = rich_media
        self.created_at = created_at
        self.approved = approved
        self.locked = locked
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
    def __init__(self, id, name, text, channel, type, rich_media, created_at, approved, locked, *args, **kwargs):  # noqa: E501
        """DataTemplate - a model

        Args:
            id (int): Identifier of the template
            name (str): Name of the template
            text (str): Text of the template
            channel (str): Channel for wich the template can be used
            type (str, none_type):
            rich_media (RichMedia):
            created_at (str):
            approved (bool): Approval status of the template (for channel `sms` this variable is always `true`)
            locked (bool): If a Viber or Whatsapp template is approved it cannot be edited, so this parameter will be **true**


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
        self.text = text
        self.channel = channel
        self.type = type
        self.rich_media = rich_media
        self.created_at = created_at
        self.approved = approved
        self.locked = locked
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
