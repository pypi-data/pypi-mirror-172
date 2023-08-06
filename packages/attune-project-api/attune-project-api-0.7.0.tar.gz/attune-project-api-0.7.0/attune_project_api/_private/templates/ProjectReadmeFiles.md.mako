<%page args="files"/>
<%text>
## Project Files
</%text>

| Name | Type |
| ---- | ---- |
% for file in files:
| ${file.name} | ${file.niceName} |
% endfor
