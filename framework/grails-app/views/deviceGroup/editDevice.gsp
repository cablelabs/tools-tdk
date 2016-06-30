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
					<g:if test="${deviceInstance?.category?.toString()?.equals('RDKV')}">
						<span class="buttons"><g:actionSubmit class="download" action="downloadDeviceXml" value= "Download"/> </span> 
					</g:if>
			</g:if>			
			</div>
		</g:form>
		<!--  New feature for upload configuration file -->	
		<div id="uploadTclConfig">
				<g:if test="${category?.toString()?.equals('RDKB')}">
					<div style="padding-left: 17%; padding-top: 2%;" id="uploadForm">

						<g:form enctype="multipart/form-data" name="tclForm">
			Update Configuration file (<span style="color: #C00;">TCL Execution *</span>) <input
								type="file" name="tclConfigFile" id="file" />
							<input type="button" value="UPLOAD" onclick="upload()" />
						</g:form>
					</div>
				</g:if>
			</div>
			<div style="padding-left:17%;padding-top:2%;" id="uploadStatus"></div>	
	</div>
	
	
	</g:if>
	
