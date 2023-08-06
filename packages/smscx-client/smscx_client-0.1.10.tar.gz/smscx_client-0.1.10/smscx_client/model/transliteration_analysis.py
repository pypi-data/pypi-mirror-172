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
    from smscx_client.model.text import Text
    globals()['Text'] = Text


class TransliterationAnalysis(ModelNormal):


    allowed_values = {
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
            'total_original_cost': (float,),  # noqa: E501
            'total_original_parts': (int,),  # noqa: E501
            'total_replaced_cost': (float,),  # noqa: E501
            'total_replaced_parts': (int,),  # noqa: E501
            'total_cost_saved': (int,),  # noqa: E501
            'total_parts_saved': (int,),  # noqa: E501
            'text': (Text,),  # noqa: E501
        }

    @cached_property
    def discriminator():
        return None


    attribute_map = {
        'total_original_cost': 'totalOriginalCost',  # noqa: E501
        'total_original_parts': 'totalOriginalParts',  # noqa: E501
        'total_replaced_cost': 'totalReplacedCost',  # noqa: E501
        'total_replaced_parts': 'totalReplacedParts',  # noqa: E501
        'total_cost_saved': 'totalCostSaved',  # noqa: E501
        'total_parts_saved': 'totalPartsSaved',  # noqa: E501
        'text': 'text',  # noqa: E501
    }

    read_only_vars = {
    }

    _composed_schemas = {}

    @classmethod
    @convert_js_args_to_python_args
    def _from_api_data(cls, total_original_cost, total_original_parts, total_replaced_cost, total_replaced_parts, total_cost_saved, total_parts_saved, text, *args, **kwargs):  # noqa: E501
        """TransliterationAnalysis - a model

        Args:
            total_original_cost (float): Total cost of sending the text before the conversion of Unicode characters to GSM alphabet
            total_original_parts (int): Total parts before the conversion of Unicode characters to GSM alphabet
            total_replaced_cost (float): Total cost of sending the text with the converted (replaced) text
            total_replaced_parts (int): Total parts of the sending with the converted (replaced) text
            total_cost_saved (int): Total cost saved by sending with the text converted to GSM-7 alphabet
            total_parts_saved (int): Total parts saved by sending with the text converted to GSM-7 alphabet
            text (Text):


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

        self.total_original_cost = total_original_cost
        self.total_original_parts = total_original_parts
        self.total_replaced_cost = total_replaced_cost
        self.total_replaced_parts = total_replaced_parts
        self.total_cost_saved = total_cost_saved
        self.total_parts_saved = total_parts_saved
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
    def __init__(self, total_original_cost, total_original_parts, total_replaced_cost, total_replaced_parts, total_cost_saved, total_parts_saved, text, *args, **kwargs):  # noqa: E501
        """TransliterationAnalysis - a model

        Args:
            total_original_cost (float): Total cost of sending the text before the conversion of Unicode characters to GSM alphabet
            total_original_parts (int): Total parts before the conversion of Unicode characters to GSM alphabet
            total_replaced_cost (float): Total cost of sending the text with the converted (replaced) text
            total_replaced_parts (int): Total parts of the sending with the converted (replaced) text
            total_cost_saved (int): Total cost saved by sending with the text converted to GSM-7 alphabet
            total_parts_saved (int): Total parts saved by sending with the text converted to GSM-7 alphabet
            text (Text):


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

        self.total_original_cost = total_original_cost
        self.total_original_parts = total_original_parts
        self.total_replaced_cost = total_replaced_cost
        self.total_replaced_parts = total_replaced_parts
        self.total_cost_saved = total_cost_saved
        self.total_parts_saved = total_parts_saved
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
