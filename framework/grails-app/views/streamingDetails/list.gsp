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
<%@ page import="com.comcast.rdk.StreamingDetails" %>
<!DOCTYPE html>
<html>
	<head>
		<meta name="layout" content="main">
		<g:set var="entityName" value="${message(code: 'streamingDetails.label', default: 'StreamingDetails')}" />
		<title><g:message code="default.list.label" args="[entityName]" /></title>
		<link rel="stylesheet" href="${resource(dir:'css',file:'jquery.treeview.css')}" />
		<g:javascript library="jquery.cookie"/>
	  	<g:javascript library="jquery.treeview.async"/>
	  	<g:javascript library="jquery.treeview"/>
	  	<g:javascript library="jquery.contextmenu.r2" />
	  	<g:javascript library="stream_resolver" />
	</head>
	<body>		
		<div id="list-streamingDetails" class="content scaffold-list" role="main">
			<h1><g:message code="default.list.label" args="[entityName]" /></h1>
			<g:if test="${flash.message}">
			<div class="message" role="status">${flash.message}</div>
			</g:if>
			
			<table class="noClass" style="border: 1; border-color: black;">
				<tr>
					<td>
						<div class="" style="width: 200px; height: 400px; overflow: auto;">
							<ul id="streambrowser" class="filetree">
								<li class="" id="root"><span class="folder">Streaming Details</span>
									<ul>
										<g:each in="${streamingDetailsInstanceList}" var="stream">
											<li><span class="file" id="${stream.id}"><a href="#" onclick="showStreamDetails('${stream.id}'); return false;">${stream.streamId}</a></span></li>
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
	          		<li id="add_property"><img src="../images/add_new.png" height="15px" width="15px"/>Add New Stream Details</li>
	        	</ul>
	        </div>
			<div class="contextMenu" id="childs_menu">
				<ul>
					<li id="edit_test"><img src="../images/edit.png" />Edit</li>
	          		<li id="delete_test">	          		
	          		<img src="../images/delete.png" />Delete</li>
	        	</ul>
	        </div>			
		</div>
	</body>
</html>
