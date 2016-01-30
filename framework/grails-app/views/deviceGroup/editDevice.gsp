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
<%@ page import="com.comcast.rdk.Device" %>

<g:set var="entityName" value="${message(code: 'device.label', default: 'Device')}" />

	<g:if test= "${deviceInstance}">
	<div id="edit-device" class="content scaffold-edit" role="main">
		<h1>Device &nbsp;${deviceInstance?.stbName}</h1>

		<g:form method="post" controller="deviceGroup" >
			<g:hiddenField name="id" value="${deviceInstance?.id}" />
			<g:hiddenField name="version" value="${deviceInstance?.version}" />
			<input type="hidden" name="url" id="url" value="${url}">
			<fieldset class="form">				
				<g:render template="formDevice"/>							
			</fieldset>			
			<div id="streamdiv">			
				<g:render template="streamlistedit"/>
			</div>			
			<br>
			<div style="width : 90%;text-align: center;">
			<g:if test="${flag != 'STATIC'}" >								
					<span class="buttons"><g:actionSubmit class="save" action="updateDevice" value="${message(code: 'default.button.update.label', default: 'Update')}" /></span>
					<span class="buttons"><g:actionSubmit class="delete" action="deviceDelete" value="${message(code: 'default.button.delete.label', default: 'Delete')}" formnovalidate="" onclick="return confirm('${message(code: 'default.button.delete.confirm.message', default: 'Are you sure?')}');" /></span>
					<span class="buttons"><g:actionSubmit class="download" action="downloadDeviceXml" value= "Download"/> </span> 
					
			</g:if>
			
			</div>
		</g:form>
	</div>
	</g:if>
	
