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
<%@ page import="com.comcast.rdk.Module" %>
<!DOCTYPE html>
<html>
	<head>
		<meta name="layout" content="main">
		<g:set var="entityName" value="${category} ${message(code: 'module.label', default: 'Add Crash LogFile Path')}" />
		<title><g:message code="default.create.label" args="[entityName]" /></title>
		<g:javascript library="jquery.table.addrow" />
		<script type="text/javascript">
			(function($){
				$(document).ready(function(){
					$(".addRow").btnAddRow();
					$(".delRow").btnDelRow();
			});
			})(jQuery);
		</script>
	</head>
	<body>
	<g:form controller="module" action="saveLogsFiles" >
		<g:hiddenField name="category" value="${category}"/>
		<a href="#show-module" class="skip" tabindex="-1"><g:message code="default.link.skip.label" default="Skip to content&hellip;"/></a>
		<div class="nav" role="navigation">
			<ul>
				<li><a class="home" href="<g:createLink params="[category:category]" action="configuration" controller="module"/>"><g:message code="default.home.label"/></a></li>
			</ul>
		</div>
		<div id="show-module" class="content scaffold-show" role="main">
		
			<h1>${category}  Add LogFile Path</h1>
			<g:if test="${flash.message}">
			<div class="message" role="status">${flash.message}</div>
			</g:if>

			<div class="fieldcontain ${hasErrors(bean: moduleInstance, field: 'stbLogFilesNames', 'error')} ">
		<table style="width:50%;">
		<tr>
			<td>Select Module</td>
			<td>&nbsp;&nbsp;
			<g:select id="module" name="module.id" from="${moduleInstanceList}" noSelection="['' : 'Please Select']" 
				optionKey="id" required="" value="" class="many-to-one"
				onchange="${remoteFunction(action:"getLogList",update:"propData1", params: " \'moduleid=\' + this.value")}" />
			</td>
		</tr>
		
		<tr>
			<td>
				<g:message code="module.stbLogFiles.label" default="LogFile Names" />
			</td>
			<td><div id="propData1">
			</div>	
				<table  style="width:15%;">
						<tr>	
							<td>
								<g:textField name="stbLogFiles" value="" type="text" />
							</td>
							<td>
								<img class="addRow"
							        src="${resource(dir:'images/',file:'addRow.png')}"
							        alt="Add" border="0"
							        title="Add" /></td>
						        
							<td>
								<img class="delRow"
							        src="${resource(dir:'images/',file:'removeRow.png')}"
							        alt="Remove" border="0"
							        title="Remove" />
							</td>
						</tr>						
				</table>
			</td>
		</tr>		
	</table>
</div>

		</div>
		
		<div class="fieldcontain ${hasErrors(bean: functionInstance, field: 'module', 'error')} required">
	<label for="module">		
	</label>
	<span class="buttons">
	<g:submitButton name="create" class="save"   value="${message(code: 'default.button.create.label', default: 'Create')}" />
	</span>
</div>
</g:form>
	</body>
</html>


