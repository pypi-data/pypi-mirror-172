# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class AntdInputNumber(Component):
    """An AntdInputNumber component.


Keyword arguments:

- id (string; optional)

- addonAfter (a list of or a singular dash component, string or number; optional)

- addonBefore (a list of or a singular dash component, string or number; optional)

- bordered (boolean; optional)

- className (string; optional)

- controls (boolean; optional)

- defaultValue (number | string; optional)

- disabled (boolean; optional)

- key (string; optional)

- keyboard (boolean; optional)

- loading_state (dict; optional)

    `loading_state` is a dict with keys:

    - component_name (string; optional):
        Holds the name of the component that is loading.

    - is_loading (boolean; optional):
        Determines if the component is loading or not.

    - prop_name (string; optional):
        Holds which property is loading.

- max (number | string; optional)

- min (number | string; optional)

- nSubmit (number; default 0)

- persisted_props (list of a value equal to: 'value's; default ['value']):
    Properties whose user interactions will persist after refreshing
    the  component or the page. Since only `value` is allowed this
    prop can  normally be ignored.

- persistence (boolean | string | number; optional):
    Used to allow user interactions in this component to be persisted
    when  the component - or the page - is refreshed. If `persisted`
    is truthy and  hasn't changed from its previous value, a `value`
    that the user has  changed while using the app will keep that
    change, as long as  the new `value` also matches what was given
    originally.  Used in conjunction with `persistence_type`.

- persistence_type (a value equal to: 'local', 'session', 'memory'; default 'local'):
    Where persisted user changes will be stored:  memory: only kept in
    memory, reset on page refresh.  local: window.localStorage, data
    is kept after the browser quit.  session: window.sessionStorage,
    data is cleared once the browser quit.

- placeholder (string; optional)

- precision (number; optional)

- prefix (a list of or a singular dash component, string or number; optional)

- readOnly (boolean; optional)

- size (a value equal to: 'small', 'middle', 'large'; optional)

- status (a value equal to: 'error', 'warning'; optional)

- step (number | string; optional)

- stringMode (boolean; optional)

- style (dict; optional)

- suffix (a list of or a singular dash component, string or number; optional)

- value (number | string; optional)"""
    _children_props = ['addonBefore', 'addonAfter', 'prefix', 'suffix']
    _base_nodes = ['addonBefore', 'addonAfter', 'prefix', 'suffix', 'children']
    _namespace = 'feffery_antd_components'
    _type = 'AntdInputNumber'
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, className=Component.UNDEFINED, style=Component.UNDEFINED, key=Component.UNDEFINED, size=Component.UNDEFINED, addonBefore=Component.UNDEFINED, addonAfter=Component.UNDEFINED, prefix=Component.UNDEFINED, suffix=Component.UNDEFINED, bordered=Component.UNDEFINED, controls=Component.UNDEFINED, defaultValue=Component.UNDEFINED, value=Component.UNDEFINED, disabled=Component.UNDEFINED, keyboard=Component.UNDEFINED, placeholder=Component.UNDEFINED, min=Component.UNDEFINED, max=Component.UNDEFINED, step=Component.UNDEFINED, precision=Component.UNDEFINED, readOnly=Component.UNDEFINED, stringMode=Component.UNDEFINED, nSubmit=Component.UNDEFINED, status=Component.UNDEFINED, loading_state=Component.UNDEFINED, persistence=Component.UNDEFINED, persisted_props=Component.UNDEFINED, persistence_type=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'addonAfter', 'addonBefore', 'bordered', 'className', 'controls', 'defaultValue', 'disabled', 'key', 'keyboard', 'loading_state', 'max', 'min', 'nSubmit', 'persisted_props', 'persistence', 'persistence_type', 'placeholder', 'precision', 'prefix', 'readOnly', 'size', 'status', 'step', 'stringMode', 'style', 'suffix', 'value']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'addonAfter', 'addonBefore', 'bordered', 'className', 'controls', 'defaultValue', 'disabled', 'key', 'keyboard', 'loading_state', 'max', 'min', 'nSubmit', 'persisted_props', 'persistence', 'persistence_type', 'placeholder', 'precision', 'prefix', 'readOnly', 'size', 'status', 'step', 'stringMode', 'style', 'suffix', 'value']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(AntdInputNumber, self).__init__(**args)
