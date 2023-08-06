<%page args="makoGlobal, project, params, niceParameterNames, files, blueprints"/>
# ${project.name}
<%doc>
TODO: Make Attune have an editable comment stored in the metadata.json  and
      print that here
${project.comment}
</%doc>

<%include file="ProjectReadmeBlueprints.md.mako" args="blueprints=blueprints"/>

<%include file="ProjectReadmeParameters.md.mako" args="params=params, niceParameterNames=niceParameterNames"/>

<%include file="ProjectReadmeFiles.md.mako" args="files=files"/>

<%include file="ProjectReadmeServerTribe.md.mako"
args=""/>

Thank you.
