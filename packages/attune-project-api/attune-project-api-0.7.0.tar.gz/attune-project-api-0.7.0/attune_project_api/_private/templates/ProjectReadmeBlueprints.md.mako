<%page args="blueprints"/>
<%text>
## Project Blueprints
</%text>
% for blueprint in blueprints:

<%text>###</%text> ${blueprint.name}

% if blueprint.comment:
```markdown
% for line in blueprint.comment.splitlines():
${line}
% endfor
```
% endif
% endfor