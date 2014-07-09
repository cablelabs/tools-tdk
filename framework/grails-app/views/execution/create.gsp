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
<%--<!DOCTYPE html>--%>
<html>
<head>
<meta name="layout" content="main">
<g:set var="entityName"
	value="${message(code: 'ScriptExecution.label', default: 'ScriptExecution')}" />
<link rel="stylesheet"
	href="${resource(dir:'css',file:'jquery.treeview.css')}" />	

<title>Script Execution</title>
<g:javascript library="jquery.cookie" />
<g:javascript library="jquery.treeview.async" />
<g:javascript library="jquery.treeview" />
<g:javascript library="jquery.contextmenu.r2" />
<g:javascript library="execution_resolver" />
<g:javascript library="jquery.dataTables"/>
<g:javascript library="jquery-ui"/>
<g:javascript library="common"/>	
<g:javascript library="jquery.more"/>
<g:javascript library="select2"/>
<link rel="stylesheet" href="${resource(dir:'css',file:'demo_table.css')}" type="text/css" />
<link rel="stylesheet" href="${resource(dir:'css',file:'jquery-ui.css')}" type="text/css" />
<script type="text/javascript">
//Popup window code
function newPopup(url) {
	popupWindow = window.open(
		url,'popUpWindow','height=700,width=800,left=10,top=10,resizable=yes,scrollbars=yes,toolbar=yes,menubar=no,location=no,directories=no,status=yes')
}

$(function() {

	$.datepicker.setDefaults({		
		changeMonth: true,
		changeYear: true	
		});
	
	 $( "#datepicker" ).datepicker();
	 $( "#todatepicker" ).datepicker();
	 $( "#cleanFromDate" ).datepicker();
	 $( "#cleanToDate" ).datepicker();

});

$(document).ready(function() {

	$(":checkbox").each(function() {
		$('.resultCheckbox').prop('checked', false);
		mark(this);
	});
	
	$('.markAll').prop('checked', false);
	
});

	
</script>
<link rel="stylesheet" href="${resource(dir:'css',file:'select2.css')}" type="text/css" />
</head>
<body>	
	<div>
		<g:if test="${flash.message}">
			<div class="message" role="status">${flash.message}</div>
		</g:if>
		<g:if test="${error}">
			<ul class="errors" role="alert">
				<li>${error}</li>
			</ul>
		</g:if>
		<br>
		<g:hiddenField id="url" name="url" value="${url}"/>
		<table class="noClass" style="border: 1; border-color: black;">
			<tr>
				<td>
						<div id="deleteMessageDiv"></div>
				</td>
			</tr>
			<tr>
				<td style="width: 16%;" class="treeborder">
				   
					<div class="" style="width: 180px; height: 400px; overflow: auto;">
						<ul id="browser" class="filetree">
							<li class="" id="root"><span class="folder" id="addconfId">Device</span>
								<ul> <% int deviceStatusCount = 0; %>
								<span id="device_status">								
									<g:each in="${deviceList}" var="device">
									<% deviceStatusCount++; %>
										<li id="deviceExecutionList_${deviceStatusCount}" ><g:if test="${device.deviceStatus.toString()=="NOT_FOUND" }">
										<span class="filedevicenotfound" id="${device.id}"><a href="#" onclick="showScript('${device.id}'); highlightTreeElement('deviceExecutionList_', '${deviceStatusCount}', '${deviceInstanceTotal}'); return false;">${device.stbName}</a></span>
										</g:if>
										<g:if test="${device.deviceStatus.toString()=="FREE" }">
										<span class="filedevicefree" id="${device.id}"><a href="#" onclick="showScript('${device.id}'); highlightTreeElement('deviceExecutionList_', '${deviceStatusCount}', '${deviceInstanceTotal}'); return false;">${device.stbName}</a></span>
										</g:if>
										<g:if test="${device.deviceStatus.toString()=="BUSY" }">
										<span class="filedevicebusy" id="${device.id}"><a href="#" onclick="showScript('${device.id}'); highlightTreeElement('deviceExecutionList_', '${deviceStatusCount}', '${deviceInstanceTotal}'); return false;">${device.stbName}</a></span>
										</g:if>
										<g:if test="${device.deviceStatus.toString()=="HANG" }">
										<span class="filedevicehang" id="${device.id}"><a href="#" onclick="showScript('${device.id}'); highlightTreeElement('deviceExecutionList_', '${deviceStatusCount}', '${deviceInstanceTotal}'); return false;">${device.stbName}</a></span>
										</g:if>
										<g:if test="${device.deviceStatus.toString()=="ALLOCATED" }">
											<span class="filedevicebusy" id="${device.id}"><a href="#"
												onclick="showScript('${device.id}'); highlightTreeElement('deviceExecutionList_', '${deviceStatusCount}', '${deviceInstanceTotal}'); return false;">
													${device.stbName}
											</a></span>
										</g:if>
										</li>
									</g:each>
									</span>	
								</ul>
							</li>
						</ul>
					</div>
				</td> 
				<td style="width: 84%;">	
					<div style="width: 100%; overflow: auto;">
					 <div id="minSearch" style="width: 96%;overflow: auto;text-align: right;vertical-align: top;">					
						    	<g:form controller="execution" >
						    	 <g:textField name="searchName" id="searchId" value=""/>
						    	 <span class="buttons"><g:submitToRemote after="hideExectionHistory();" before="showSpinner();" onSuccess="hideSpinner();" class="find" action="searchExecutionList" update="searchResultDiv" value="Search" /></span>
						    	 <img src="../images/more.png" title="Advanced Search" onclick="displayAdvancedSearch();"></img>
						    	 <span id="spinner1" style="display: none;">											
									<img id="sss" src="${resource(dir:'images',file:'spinner.gif')}" />
								 </span>						    	
						    	</g:form>						
							</div>
							<div id="advancedSearch" style="display:none;width: 100%; overflow: auto;">
								<g:form controller="execution" >
								<table>															
									<tr>
										<th colspan="6">Search</th>
									</tr>
									<tr>
										<td valign="middle">From</td>
										<td valign="middle"><input type="text" id="datepicker" name="fromDate" />
										</td>
										<td valign="middle">To</td>
										<td valign="middle"><input type="text" id="todatepicker" name="toDate"/>										
										</td>
										<td></td>
										<td valign="middle">
										
										</td>
									</tr>
									<tr>
										<td valign="middle">DeviceName</td>
										<td valign="middle"><g:textField name="deviceName"/></td>
										<td valign="middle">Status</td>
										<td valign="middle">
											<select name="resultStatus" id="resultStatus" style="width: 150px">
												<option value="">--Please Select--</option>
												<option value="UNDEFINED">UNDEFINED</option>
												<option value="SUCCESS">SUCCESS</option>
												<option value="FAILURE">FAILURE</option>
								 			</select>
										</td>	
										<td valign="middle"></td>
										<td valign="middle"></td>
									</tr>
									<tr>
										<td valign="middle">ScriptType</td>
										<td valign="middle">											
								 			<select name="scriptType" id="scriptType" onchange="showScriptTypes();" style="width: 150px">
												<option value="">--Please Select--</option>
												<option value="Script">SINGLE SCRIPT</option>
												<option value="TestSuite">SCRIPTGROUP</option>												
											</select>
										</td>
										<td valign="middle"><span id="scriptLabel" style="display:none;">Script/ScriptGroup</span></td>
										<td valign="middle"><span id="scriptVal" style="display:none;"><g:textField id="scriptValue" name="scriptVal"/></span>									
										</td>
										<td></td>
										<td valign="middle" width="20%">
											<span class="buttons">
												<g:submitToRemote before="displayWaitSpinner();" class="find" action="multisearch" update="searchResultDiv" value="Search" onSuccess="hideWaitSpinner();" />
											</span>
											<img src="../images/less.png" title="Simple Search" onclick="showMinSearch();"></img>
											<span id="spinnr" style="display: none;">											
										              <img id="ss" src="${resource(dir:'images',file:'spinner.gif')}" />
										    </span>													
										</td>
									</tr>
									<tr>
										<td colspan="6"><hr></td>
									</tr>																		
								</table>
								</g:form>
						</div>
						<div id="searchResultDiv" style="width: 100%;overflow: auto;" class="veruthe"></div>
					
						<div id="listscript" style="width: 97%; overflow: auto; ">
							<g:render template="listExecution"/>
						</div>	
					</div>		
					<div id="responseDiv" style="width: 100%; height: 600px; overflow: auto;" class="responseclass"></div>
				</td>
			</tr>
		</table>			 
	</div>
	<div class="contextMenu" id="childs_menu">
		<ul>
			<li id="reset_device">
         		<img src="../images/delete.png" />
         		Reset Device</li>
              	
			<li id="reset_IpRule">
         		<img src="../images/delete.png" />
         		Reset Ip Rule</li>
       	</ul>
	</div>
	<div id="executionLogPopup" style="display: none; overflow: auto; width : 98%; height : 98%;">			
	</div>

	<div id="cleanupPopup" style="display: none; overflow: auto;">			
		<g:form controller="execution" ><br>
		<table>																	
			<tr>
				<td valign="middle">From</td>
				<td valign="middle"><input type="text" id="cleanFromDate" name="cleanFromDate" />
				</td>
				<td valign="middle">To</td>
				<td valign="middle"><input type="text" id="cleanToDate" name="cleanToDate"/>										
				</td>
				<td></td>
				<td valign="middle">
				<span class="buttons">
					<g:submitToRemote before="showSpinner();" class="delete" action="deleteExecutions" update="searchDelResultDiv" value="Delete" onSuccess="hideSpinner();" />
					
					<span id="delspinnr" style="display: none;">											
						<img id="ss" src="${resource(dir:'images',file:'spinner.gif')}" />
					</span>	
					
				</span>										
				</td>
			</tr>
		</table>
		<span id="searchDelResultDiv"></span>
		</g:form>
	</div>

	<g:hiddenField name = "selectedDevice" id = "selectedDevice" value = ""/>
	<g:hiddenField name = "deviceInstance" id = "deviceInstance" value = "${deviceInstanceTotal}"/>

</body>
</html> 
