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
<%@ page import="com.comcast.rdk.PrimitiveTest" %>
<%--<!DOCTYPE html>--%>
<html>
	<head>
		<meta name="layout" content="main">
		<g:set var="entityName" value="${message(code: 'primitiveTest.label', default: 'PrimitiveTest')}" />
		<link rel="stylesheet" href="${resource(dir:'css',file:'jquery.treeview.css')}" />
		<title>Primitive Tests Control Panel</title>
	  	<g:javascript library="jquery.cookie"/>
	  	<g:javascript library="jquery.treeview.async"/>
	  	<g:javascript library="jquery.treeview"/>
	  	<g:javascript library="jquery.contextmenu.r2" />
	  	<g:javascript library="test_resolver" />
	  	<g:javascript library="common" />
	  	
	  	<script type="text/javascript">

		$(document).ready(function() {
	
			var primitiveTestId = $("#currentPrimitiveTestId").val();
			if(primitiveTestId){
				makeTestEditable(primitiveTestId);
				$("#currentPrimitiveTestId").val("");
			}
		});

	</script>		
	</head>
	<body>
		<a href="#create-primitiveTest" class="skip" tabindex="-1"><g:message code="default.link.skip.label" default="Skip to content&hellip;"/></a>
		<div id="" class="">
			<h1>Primitive Tests Control Panel</h1>
			<g:if test="${flash.message}">
				<div class="message" role="status">${flash.message}</div>
			</g:if>
			<g:if test="${error}">
				<ul class="errors" role="alert">
					<li>${error}</li>
				</ul>
			</g:if>
			<br>
			<div id="testMessageDiv" class="message" style="display: none;"></div>
			
			<input type="hidden" name="decider" id="decider" value="${params.id}">
			<table class="noClass" style="border: 1; border-color: black;">
				<tr>
					<td>
						<div class="treeborder" style="width: 230px; height: 400px; overflow: auto;">
							<ul id="primitveTestbrowser" class="filetree">
								<li  class="" id="root"><span class="folder">Primitive Tests</span>
									<ul>
										<% int primitiveTestIndex = 0; %>
										<g:each in="${primitiveTestList}" var="test">
											<%  primitiveTestIndex++; %>
											
											<li id="primitiveTestList_${primitiveTestIndex}">
												<span class="file" id="${test.id}">
													<a href="#" onclick="makeTestEditable('${test.id}'); highlightTreeElement('primitiveTestList_', '${primitiveTestIndex}', '${primitiveTestCount}'); return false;">${test.name}</a>
												</span>
											</li>
										</g:each>
									</ul>
								</li>
							</ul>
						</div>
					</td>
					<td>
						<div id="responseDiv" style="width: 500px; height: 400px; overflow: auto;"></div>
					</td>
				</tr>
			</table>
			<div class="contextMenu" id="root_menu">
				<ul>
	          		<li id="add_property"><img src="../images/add_new.png" height="15px" width="15px"/>Add New Primitive Test</li>
	        	</ul>
	      </div>
			<div class="contextMenu" id="childs_menu">
				<ul>
					<li id="edit_test"><img src="../images/edit.png" />Edit</li>
	          		<li id="delete_test">
	          		
	          		<img src="../images/delete.png" />
	          			
	          		Delete</li>
	        	</ul>
	      </div>
		</div>
		<g:hiddenField name="currentPrimitiveTestId" id="currentPrimitiveTestId" value="${primitiveTestId}"/>
		<g:hiddenField name="isTestExist" id="isTestExist" value=""/>
	</body>
</html>
