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
<%@ page import="com.comcast.rdk.DeviceGroup" %>
<!DOCTYPE html>
<html>
<head>
<meta name="layout" content="main">
<g:set var="entityName"
	value="${message(code: 'Configuration.label', default: 'Configuration')}" />
<link rel="stylesheet"
	href="${resource(dir:'css',file:'jquery.treeview.css')}" />
<title>Device Group</title>
<g:javascript library="jquery.cookie" />
<g:javascript library="jquery.treeview.async" />
<g:javascript library="jquery.treeview" />
<g:javascript library="jquery.contextmenu.r2" />
<g:javascript library="devicegrp_resolver" />
<g:javascript library="config_resolver" />
<g:javascript library="common" />

	<script type="text/javascript">

	$(document).ready(function() {

		var deviceId = $("#currentDeviceId").val();
		if(deviceId!=null || deviceId!=""){
			showDevice(deviceId);
		}

		var deviceGroupId = $("#currentDeviceGroupId").val();
		if(deviceGroupId){
			showDeviceGroup(deviceGroupId);
			
		}

	});

	</script>
</head>
<body>
 
	<a href="#create-primitiveTest" class="skip" tabindex="-1"><g:message code="default.link.skip.label" default="Skip to content&hellip;"/></a>	
		<div id="" class="">
			<h1>Device Groups</h1>
			
			<g:if test="${flash.message}">
				<div id="messageDiv" class="message" role="status">${flash.message}</div>
			</g:if>
			<g:if test="${error}">
				<ul class="errors" role="alert">
					<li>${error}</li>
				</ul>
			</g:if>
			
			<g:hasErrors bean="${deviceGroupsInstance}">
			<ul class="errors" role="alert">
				<g:eachError bean="${deviceGroupsInstance}" var="error">
				<li <g:if test="${error in org.springframework.validation.FieldError}">data-field-id="${error.field}"</g:if>><g:message error="${error}"/></li>
				</g:eachError>
			</ul>
			</g:hasErrors>
			<br>
			<g:hiddenField id="url" name="url" value="${url}"/>
			<input type="hidden" name="decider" id="decider" value="${params.id}">
			
			<span>
			<table class="noClass" style="border: 1; border-color: black;">
				<tr>
					<td style="width: 20%; vertical-align: top;" class="treeborder" >
						<div id="deviceTreeDefault"class="" style="overflow: auto;vertical-align: top; height: 300px;">
									<% int deviceCount = 0;
									   int totalDevices = deviceInstanceTotal * deviceGroupsInstanceTotal;
									   int deviceGroupCount = 0;
									 %>
							<ul id="browser2" class="filetree">
								<li id="root"><span class="folder" id="addconfId">Devices</span>
									<ul>
											<g:each in="${deviceInstanceList}" var="parentDevice">
											<g:if test="${parentDevice.isChild == 0}">
												<li class="closed"><span class="file" id="${parentDevice.id}"><a href="#" onclick="showDevice('${parentDevice.id}');  highlightTreeElement('deviceList_', '${deviceCount}', '${deviceInstanceTotal}'); highlightTreeElement('deviceGroupList_', '0', '${totalDevices}'); return false;">${parentDevice.stbName}</a></span>
													<ul>
														<g:each in="${ parentDevice.childDevices}" var="childDevice">
															<% deviceCount++; %>
															<li id="deviceList_${deviceCount}">
																<span class="file" id="${childDevice.id}">
																	<a href="#" onclick="showDevice('${childDevice.id}');  highlightTreeElement('deviceList_', '${deviceCount}', '${deviceInstanceTotal}'); highlightTreeElement('deviceGroupList_', '0', '${totalDevices}'); return false;">${childDevice.stbName}</a>
																</span>
															</li>
													     </g:each>
													</ul>											
												</li>
												 </g:if>
											</g:each>
									</ul>
								</li>
							</ul>
						</div>
					</td>
					
					<td rowspan="2" style="width: 80%;">
						<div id="responseDiv" style="width: 97%; overflow: auto;"></div>
					</td>					
				</tr>
				<tr>
					<td style="width: 20%; vertical-align: top;" class="treeborder" >
						<div class="" style="width: 200px; height: 400px;overflow: auto;vertical-align: top;">
							<ul id="browser1" class="filetree">
								<li class="" id="root1"><span class="folder" id="addDeviceGrpId">DeviceGroup</span>
									<ul>
										<g:each in="${deviceGroupsInstanceList}" var="deviceGrp">
											<li class="closed"><span class="hasChildren" id="${deviceGrp.id}"><a href="#" onclick="showDeviceGroup('${deviceGrp.id}'); return false;">${deviceGrp.name}</a></span>
												<ul>
													<g:each in="${deviceGrp.devices}" var="device">
														<% deviceGroupCount++; %>
													<li id="deviceGroupList_${deviceGroupCount}">
														<span id="${device.id}"><a href="#" onclick="showDevice('${device.id}' , 'STATIC');  highlightTreeElement('deviceList_', '0', '${deviceInstanceTotal}'); highlightTreeElement('deviceGroupList_', '${deviceGroupCount}', '${totalDevices}'); return false;">${device.stbName}</a></span>
													</li>
													</g:each>
												</ul>											
											</li>
										</g:each>
									</ul>
								</li>
							</ul>
						</div>
					</td>									
				</tr>
			</table>
			</span>
			<div class="contextMenu" id="root_menu">
				<ul>
	          		<li id="add_devicegrp"><img src="../images/add_new.png" height="15px" width="15px"/>Add New DeviceGroup</li>
	        	</ul>
	        </div>
			<div class="contextMenu" id="childs_menu">
				<ul>
					<li id="edit_devicegrp"><img src="../images/edit.png" />Edit</li>
	          		<li id="delete_devicegrp"><img src="../images/delete.png" />Delete</li>
	          	
	        	</ul>
	      </div>	      
	     
	       <div class="contextMenu" id="root_menu_device">
				<ul>
	          		<li id="add_device"><img src="../images/add_new.png" height="15px" width="15px"/>Add New Device</li>
	        	</ul>
	        </div>
			<div class="contextMenu" id="childs_menu_device">
				<ul>
					<li id="edit_device"><img src="../images/edit.png" />Edit</li>
	          		<li id="delete_device"><img src="../images/delete.png" />Delete</li>
	          		
	        	</ul>
	      </div>
	      
		</div>
		
		<g:hiddenField name="currentDeviceId" id="currentDeviceId" value="${deviceId}"/>
		<g:hiddenField name="currentDeviceGroupId" id="currentDeviceGroupId" value="${deviceGroupId}"/>
		
		<g:hiddenField name="deviceGroupCount" id="deviceGroupCount" value="${deviceInstanceTotal}"/>
		<g:hiddenField name="isDeviceExist" id="isDeviceExist" value=""/>
		

</body>
</html>


