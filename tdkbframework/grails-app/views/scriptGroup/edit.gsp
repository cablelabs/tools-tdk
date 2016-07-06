<!-- 
 ============================================================================
  COMCAST CONFIDENTIAL AND PROPRIETARY
 ============================================================================
  This file and its contents are the intellectual property of Comcast.  It may
  not be used, copied, distributed or otherwise  disclosed in whole or in part
  without the express written permission of Comcast.
  ============================================================================
  Copyright (c) 2013 Comcast. All rights reserved.
  ============================================================================
-->
<%@ page import="com.comcast.rdk.ScriptGroup" %>

<head>
<meta charset="utf-8">
<link rel="stylesheet" href="${resource(dir:'css',file:'jquery-ui.css')}" type="text/css" />
<link rel="stylesheet" href="${resource(dir:'css',file:'demo_table.css')}" type="text/css" />
<g:javascript library="jquery-1.10.2.js"/>
<g:javascript library="jquery-ui"/>
<link rel="stylesheet" href="${resource(dir:'css',file:'style.css')}">
<style>
#sortable {
	list-style-type: none;
	margin: 0;
	padding: 0;
	width: 100%;
	border-style : solid;
	border-width:1px;
	border-color:#B6E8F5;
}

#sortable li {
	margin: 0 1px 1px 1px;
	padding: 0.4em;
	padding-left: 1.5em;
	font-size: 2.5;
	height: 7px;
	overflow: hidden;
}

#sortable li span {
	position: absolute;
	margin-left: -1.3em;
}

#feedback {
	font-size: 1.4em;
}

#selectable .ui-selecting {
	background: #FECA40;
}

#selectable .ui-selected {
	background: #F39814;
	color: white;
}

#selectable {
	list-style-type: none;
	margin: 0;
	padding: 0;
	width: 100%;
	border-style : solid;
	border-width:1px;
	border-color:#B6E8F5;
}

#selectable li {
	margin: 0 1px 1px 1px;
	padding: 0.4em;
	padding-left : 8px
	font-size: 2.5;
	height: 10px;
	overflow: hidden;
}

#sortable li .handle {
	background: #CC6633;
	position: absolute;
	left: 0;
	top: 0;
	bottom: 0;
	padding: 0.4em;
	width: 8px
}

#sortable .ui-selecting {
	background: #FECA40;
}

#sortable .ui-selecting .handle {
	background: #FFFF99;
}

#sortable .ui-selected {
	background: #F39814;
}

#sortable .ui-selected .handle {
	background: #FFFF99;
}

#sortable ul {
	width: 300px;
	list-style: none;
	margin: 0;
	padding: 0;
}

#sortable li {
	background: white;
	position: relative;
	margin: 0 1px 1px 1px;
	list-style: none;
	font-size: 2.5;
	height: 10px;
	overflow: hidden;
}


</style>
<script>
	$(function() {
		 $( "#selectable" ).selectable({
			 stop: function() {
			 var result = $( "#select-result" ).empty();
			 var data = ""
			 var myArray = [];
			 
			 $( ".ui-selected", this ).each(function() {
			 var index = $( "#selectable li" ).index( this );
			 data = data +"," +(index +1)
			 result.append( " #" + ( index + 1 ) );
			 myArray.push(this.id)
			 });
			 document.getElementById("resultElement").value = myArray;
			 }
			 });

		

		 $( "#sortable" ).selectable({
			 stop: function() {
			 var result = $( "#select-result" ).empty();
			 var data = ""
			 var myArray = [];
			 
			 $( ".ui-selected", this ).each(function() {
			 var index = $( "#sortable li" ).index( this );
			 data = data +"," +(index +1)
			 result.append( " #" + ( index + 1 ) );
			 myArray.push(this.id)
			 });
			 document.getElementById("sgResultElement").value = myArray;
			 },
			 selecting: function(e, ui) { // on select
			        var curr = $(ui.selecting.tagName, e.target).index(ui.selecting); // get selecting item index
			        if(e.shiftKey && prev > -1) { // if shift key was pressed and there is previous - select them all
			            $(ui.selecting.tagName, e.target).slice(Math.min(prev, curr), 1 + Math.max(prev, curr)).addClass('ui-selected');
			            prev = -1; // and reset prev
			        } else {
			            prev = curr; // othervise just save prev
			        }
			    }
			 });
		
			
	});

</script>
</head>
<g:set var="entityName" value="${message(code: 'scriptGroup.label', default: 'TestSuite')}" />

<a href="#edit-scriptGroup" class="skip" tabindex="-1"><g:message code="default.link.skip.label" default="Skip to content&hellip;"/></a>
<div id="edit-scriptGroup" class="content scaffold-edit" role="main">
	<h1><g:message code="default.edit.label" args="[entityName]" /></h1>
<g:if test="${flash.message}">
<div class="message" role="status">${flash.message}</div>
</g:if>
<g:hasErrors bean="${scriptGroupInstance}">
<ul class="errors" role="alert">
	<g:eachError bean="${scriptGroupInstance}" var="error">
	<li <g:if test="${error in org.springframework.validation.FieldError}">data-field-id="${error.field}"</g:if>><g:message error="${error}"/></li>
	</g:eachError>
</ul>
</g:hasErrors>
<g:form method="post" >
	<g:hiddenField id ="sgId" name="id" value="${scriptGroupInstance?.id}" />
	<g:hiddenField id="sgVersion" name="version" value="${scriptGroupInstance?.version}" />
	
<br>
<input type="hidden" id = "scriptElement" name="scriptElement">
			<input type="hidden" id = "resultElement" name="resultElement">
			<input type="hidden" id = "sgResultElement" name="sgResultElement">
			<label for="name">
		<g:message code="scriptGroup.name.label" default="Name" />
		<span class="required-indicator">*</span>
	</label>
	
	<g:textField id= "scriptName" name="name" required="" value="${scriptGroupInstance?.name}" style="width: 240px"/>
			<br><br>
			<table name="scripttable">
			<tr>
				<td name="selectabletd" style="width: 45%">
					<div class="selectablediv" name ="selectablediv"> 
					<label>All Scripts</label> <br>
					<ul class= "selectable" id="selectable" name ="selectable"  title="selectable" style="max-height : 454px; max-width : 380px; overflow: auto; ">
						<g:each in='${scripts}' var="script">
						<% 
							String idScript = script?.id;
 					     %>
							<li id = "script-${idScript}" title="${script.scriptName}" class="ui-state-default">
								${script.scriptName}
							</li>
						</g:each>
					</ul>
					</div>
					</td>
				<td style="width: 8%">
				<br><br><br><br>
				<input type="image" src= "../images/arrow_right.png" onclick="addScripts();return false;"  ><br><br>
				<input type="image" src= "../images/arrow_left.png" onclick="removeScripts();return false;">
				</td>
				<td  style="width: 45%">
				 <br>
				 ${scriptGroupInstance} &emsp;&emsp;&emsp; &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;  Scripts Count : ${scriptGroupInstance.scriptList.size()} 
					<ul id="sortable" style="min-height : 454px; min-width : 250px; max-height : 350px; max-width : 380px; overflow: auto;">
						<g:if test="${scriptGroupInstance}">
						<g:each in='${scriptGroupInstance.scriptList}' var="script">
						<% 
							String idSgScript = script?.id;
 					     %>
							<li id = "sgscript-${idSgScript}end"  title="${script.scriptName}" class="ui-state-default">
								${script.scriptName}
							</li>
						</g:each>
						</g:if>
						<g:else> <li class="ui-state-default">
								No scripts in list
							</li></g:else>
					</ul>
				</td>
				<td style="width: 8%">
					<br>
					<input type="image" src= "../images/reorder_up.png" value="Move Up" onclick="moveUp();return false;"  title  = " Move Up "> <br><br>
					<input type="image" src="../images/reorder_down.png" value="Move Down" onclick="moveDown();return false;"  title  = " Move Down ">
				</td>
			</tr>
		</table>
		
	<%--<fieldset class="buttons">--%>
	<div style="width : 90%; text-align: center;">
	<span class="buttons"><input type="button" class="save" value="${message(code: 'default.button.update.label', default: 'Update')}" onclick="updateSG()"></span>
		<span class="buttons"><g:actionSubmit class="delete" action="deleteScriptGrp" value="${message(code: 'default.button.delete.label', default: 'Delete')}" formnovalidate="" onclick="return confirm('${message(code: 'default.button.delete.confirm.message', default: 'Are you sure?')}');" /></span>
		<span class="buttons" ><g:actionSubmit class="save" action ="downloadXml" value="Download XML"  /></span>
	</div>
	<%--</fieldset>--%>
	</g:form>
</div>
