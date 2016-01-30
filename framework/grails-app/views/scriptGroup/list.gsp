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
<%@ page import="org.apache.shiro.SecurityUtils"%>
<%@ page import="com.comcast.rdk.User" %>
<!DOCTYPE html>
<html>
<head>
	<meta name="layout" content="main">
	<g:set var="entityName" value="${message(code: 'scriptGroup.label', default: 'Scripts & TestSuites')}" />
	<title><g:message code="default.list.label" args="[entityName]" /></title>	
	<link rel="stylesheet"
		href="${resource(dir:'css',file:'jquery.treeview.css')}" />
	<g:javascript library="jquery.cookie" />
	<g:javascript library="jquery.treeview.async" />
	<g:javascript library="jquery.treeview" />
	<g:javascript library="jquery.contextmenu.r2" />
	<g:javascript library="script_resolver" />
	<g:javascript library="jquery.dataTables"/> 
	<g:javascript library="common" />
	
	<link rel="stylesheet" href="${resource(dir:'css',file:'demo_table.css')}" type="text/css" />
	
	<script type="text/javascript">

	$(document).ready(function() {
		$("#list-scriptDetails").show();
		//$("#responseDiv123").hide();
			$("#scriptTable").dataTable( {
			"sPaginationType": "full_numbers"
		});
		var scriptId = $("#currentScriptId").val();
		if(scriptId!=null && scriptId!=""){
			editScript(scriptId);
		}

		var scriptGroupId = $("#currentScriptGroupId").val();
		if(scriptGroupId){
			editScriptGroup(scriptGroupId);			
		}
		
	});
	
	//Popup window code
	function newPopup(url) {
		popupWindow = window.open(
			url,'popUpWindow','height=700,width=800,left=10,top=10,resizable=yes,scrollbars=yes,toolbar=yes,menubar=no,location=no,directories=no,status=yes')
	}

	
	</script>
</head>

<body>
	<a href="#list-scriptGroup" class="skip" tabindex="-1"><g:message code="default.link.skip.label" default="Skip to content&hellip;"/></a>
		
		<%--<div class="nav" role = "navigation" style ="background: #f7f7f7">
		<table  height = "5">
			<tr>
				<td>
				 		<span class=" buttons"> <g:submitToRemote class="refresh"   before="refreshListStart()"  action="scriptListRefresh;"  value="Script List Refresh"  onFailure="scriptRefreshFailure()" onSuccess="scriptRefreshSuccess()" /></span> 
				</td>
			</tr>
		<tr></tr>
		</table>
		</div>--%>
		<div id="" class="">
			<g:if test="${flash.message}">
				<div class="message" role="status">${flash.message}</div>
			</g:if>
			<g:if test="${error}">
				<ul class="errors" role="alert">
					<li>${error}</li>
				</ul>
			</g:if>
			<g:hasErrors bean="${scriptGroupInstance}">
			<ul class="errors" role="alert">
				<g:eachError bean="${scriptGroupInstance}" var="error">
				<li <g:if test="${error in org.springframework.validation.FieldError}">data-field-id="${error.field}"</g:if>><g:message error="${error}"/></li>
				</g:eachError>
			</ul>
			</g:hasErrors>
			<br>

			<input type="hidden" name="decider" id="decider" value="${params.id}">
			<table class="noClass" style="border: 1; border-color: black;">
				<tr>
					<td style="width: 20%; vertical-align: top;" class="treeborder">
						<div class="" style="vertical-align: top; width: 290px; max-height: 260px;">
							<ul id="scriptbrowser" class="filetree">
								<li class="" id="root"><span class="folder" id="addScriptId" style="overflow: auto;">Scripts</span>
								<% int scriptCount = 0;
									   int totalScripts = scriptInstanceTotal * scriptGroupInstanceTotal;
									 %>
									<ul>
									<div class="" style="max-height: 224px;overflow: auto;vertical-align: top;">
									<g:each in="${scriptGroupMap}" var="mapEntry">
										<li class="closed"><span class="folder" id="addScriptId">${mapEntry.key}</span>
											<ul id ="module_">
												<g:each in="${mapEntry.value}" var="script">
												<% scriptCount++; %>
    												<li id="scriptList_${scriptCount}"><span class="file" id="${mapEntry.key}@${script}"><a href="#"  onclick="editScript('${mapEntry.key}@${script}'); highlightTreeElement('scriptList_', '${scriptCount}', '${scriptInstanceTotal}'); highlightTreeElement('scriptGroupList_', '0', '${totalScripts}'); return false;">${script}</a></span></li>
												</g:each>
											</ul>
										</li>
									</g:each>
									</div>
									</ul> 
								</li>
							</ul>
						</div>
						<div class="" style="width: 290px; max-height: 350px;vertical-align: top;">
							<ul id="scriptgrpbrowser" class="filetree">
								<li class=""><span class="folder" id="addscriptGrpId">TestSuite</span>
									<ul>
									<div class="" style="max-height: 340px;overflow: auto;vertical-align: top;">
									<% int scriptGroupCount = 0; %>
									
										<g:each in="${scriptGroupInstanceList}" var="scriptGrp">
										<% def id = scriptGrp
											if(id.contains(".")){
												id = id.replace(".", "_")
											}
										 %>
										<div id="${id}" class="${scriptGrp}" onmouseover="getScriptsList(this, '${scriptGrp}', ${scriptInstanceTotal}, ${totalScripts} )">
											<li class="closed"><span class="folder" id="${scriptGrp}"><a href="#" onclick="editScriptGroup('${scriptGrp}'); return false;">${scriptGrp}</a></span>
												<ul>
												<div class="scripts_${id}">
												</div>
												</ul>											
											</li>
										</div>
										</g:each>
										</div>
									</ul>
								</li>
							</ul>
						</div>
					</td>
										
					<td rowspan="2" style="width: 80%;">	
						<div id="responseDiv123" style="width: 100%; height: 610px; overflow: auto;">						    
						    <div id="minSearch" style="width: 100%;overflow: auto;text-align: right;vertical-align: top;">
						    	<g:form controller="scriptGroup" >
						    	 <g:textField name="searchName" id="searchId" value=""/>
						    	 <span class="buttons"><g:submitToRemote class="find" action="searchScript" update="searchResultDiv" value="Search" /></span>
						    	 <img src="../images/more.png" title="Advanced Search" onclick="displayAdvancedSearch();" style="display:none;"></img>						    	
						    	</g:form>						
							</div>
							
								<!-- The script details table UI changes -->
							
					<div style="width: 95%; max-height: 600px; display: none ;"
						id="list-scriptDetails" class="content scaffold-list"
						id="scriptDetails">
						<table id="scriptTable" class="display">
							<thead>
								<tr>
									<th colspan="4" align="center" style="width: 50%;"><h1>Script
											Details Summary</h1></th>
								</tr>
								<tr align="left">
									<th width="15%">Sl No</th>
									<th width ="28%">Module Name</th>
									<th width ="23%"> Test Group </th>
									<th width ="13%">Script Count</th>							
								</tr>
							</thead>
							<br>
							<br>
							<tbody align="left">
								<%int moduleCount =0  %>
								<g:each in="${scriptGroupMap}" var=" name">					
									<tr class="odd">									
										<% 	moduleCount++ %>
										<td>
											${moduleCount}
										</td>
										<td>
											${name.key}
										</td>
										<td>
											<g:each in="${testGroup}" var ="groupName">
												 <g:if test="${groupName.key?.toString() == name?.key?.toString()}" >
												${groupName?.value }
												</g:if>
											</g:each>
										</td>
										<td>
											${name.value.size()}
										</td>												
									</tr>
									</g:each>								
							</tbody>
						</table>
					</div>
						
							<div id="advancedSearch" style="display:none;width: 100%; overflow: auto;">
								<g:form controller="scriptGroup" >
								<table>
									<tr>
										<th colspan="5">Search</th>
									</tr>
									<tr>
										<td valign="middle">ScriptName</td>
										<td valign="middle"><g:textField name="searchName" id="searchId" value="" style="width: 190px" /></td>
										<td valign="middle">PrimitiveTest</td>
										<td valign="middle">
											<select name="primtest" id="primtest" style="width: 210px">
												<option value="">--Please Select--</option>
												<g:each in="${com.comcast.rdk.PrimitiveTest.list()}" var="primList">
													<option value="${primList.id}">
														${primList.name}
													</option>
												</g:each>
								 			</select>
										</td>
										<td valign="middle"><img src="../images/less.png" title="Simple Search" onclick="showMinSearch();"></img></td>
									</tr>
									<tr>
										<td valign="middle">BoxType</td>
										<td valign="middle">
											<g:select id="selboxTypes" name="selboxTypes"  from="${com.comcast.rdk.BoxType.list()}" 
											optionKey="id" required="" value="${deviceInstance?.boxType}" multiple="true"
											class="many-to-one selectCombo" />
										</td>
										<td valign="middle"></td>
										<td valign="middle"><span class="buttons">
											<g:submitToRemote class="find" action="advsearchScript" update="searchResultDiv" value="Search" /></span>
										</td>
										<td valign="middle"></td>
									</tr>
									<tr>
										<td colspan="5"><hr></td>
									</tr>									
								</table>
								</g:form>
						    </div>
							<div id="searchResultDiv" style="width: 100%;overflow: auto;" class="veruthe"></div>							
							<div id="responseDiv" style="width: 100%;overflow: auto;" class="responseclass">							    
							</div>
						</div>
						
						
					
					<div class="contextMenu" id="up_load" align="center"
						style="width: 950px; height: 900px;">
						<br> <br> <br> <br>
						<g:form method="POST" controller="scriptGroup" action="upload"
							enctype="multipart/form-data">
							<label> <b><g:message code="scriptGroup.name.label"
										default="Select the testSuite XML file" /></b>
							</label>
							&emsp;
							<input class="uploadFile" type="file" name="file" />
							&emsp;&emsp;
							<g:actionSubmit class="buttons" style="width : 100px; "
								action="upload" value="Upload" />

						</g:form>
					</div>
					</td>					
				</tr>
			</table>
		<div class="contextMenu" id="script_root_menu">
			<ul>
				<li id="add_script"><img src="../images/add_new.png"
					height="15px" width="15px" />Add New Script</li>

				<li id="refresh"><img src="../images/refresh.gif" height="15px"
					width="15px" /> <g:submitToRemote class="test"
						before="refreshListStart()" action="scriptListRefresh;"
						value="ScriptList Refresh" onFailure="scriptRefreshFailure()"
						onSuccess="scriptRefreshSuccess()" /></li>
			<li id="download_script"> <img src="../images/script_download.png" height="15px" width="15px"/>Download Script Details </li> 
			</ul>
		</div>
	      	
			<div class="contextMenu" id="script_childs_menu">
				<g:if test="${SecurityUtils.getSubject().hasRole('ADMIN')}" >
				<ul>
					<li id="edit_script"><img src="../images/edit.png" />Edit</li>
	          		<li id="delete_script"><img src="../images/delete.png" />Delete</li>
	        	</ul>
	        	</g:if>
	      	</div>

	       <div class="contextMenu" id="scriptgrp_root_menu">
				<ul>
	          		<li id="add_scriptgrp"><img src="../images/add_new.png" height="15px" width="15px"/>Add New Test Suite</li>
	          		<li id="upload_scriptGroup"><img src="../images/reorder_up.png"
					height="15px" width="15px" /> Upload script group XML</li>
	        	</ul>
	        </div>
			<div class="contextMenu" id="scriptgrp_childs_menu">
				<ul>
					<li id="edit_scriptgrp"><img src="../images/edit.png" />Edit</li>
	          		<li id="delete_scriptgrp"><img src="../images/delete.png" />Delete</li>
	        	</ul>
	      	</div>	      
		</div>
		<div id="streamDetailsPopup" style="display: none; overflow: auto; width : 98%; height : 98%;">			
	</div>
	
	<g:hiddenField name="currentScriptId" id="currentScriptId" value="${scriptId}"/>
	<g:hiddenField name="currentScriptGroupId" id="currentScriptGroupId" value="${scriptGroupId}"/>
	<g:hiddenField name="isDeviceExist" id="isScriptExist" value=""/>
	
	
</body>
</html>


