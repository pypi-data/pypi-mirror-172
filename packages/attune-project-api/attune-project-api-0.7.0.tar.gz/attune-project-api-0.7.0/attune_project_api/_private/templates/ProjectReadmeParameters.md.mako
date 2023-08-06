<%page args="params, niceParameterNames"/>
<%text>
## Project Parameters
</%text>

| Name | Type | Script Reference |
| ---- | ---- | ---------------- |
% for parameter in params:
| ${parameter.name} | ${niceParameterNames[parameter.type]} | `${parameter.textName}` |
% endfor
