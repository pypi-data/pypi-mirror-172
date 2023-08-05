# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class ParticipationStat(Component):
    """A ParticipationStat component.
This class will be used by DAOInfo and PlatformInfo

Keyword arguments:

- key (string; optional):
    The key used by React for optimization.

- text (string; required):
    The text to show.

- value (string; optional):
    The value to highlight, which will be appended to text."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dao_analyzer_components'
    _type = 'ParticipationStat'
    @_explicitize_args
    def __init__(self, text=Component.REQUIRED, value=Component.UNDEFINED, key=Component.UNDEFINED, **kwargs):
        self._prop_names = ['key', 'text', 'value']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['key', 'text', 'value']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        for k in ['text']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(ParticipationStat, self).__init__(**args)
