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
<%@ page import="org.apache.shiro.SecurityUtils"%>
<!DOCTYPE html>
<html>
	<head>
		<meta name="layout" content="main"/>
		<title>RDK Test Suite</title>
		<style type="text/css" media="screen"></style>
	</head>
	<body>	
	<br>
		<div style="width:40%;margin: 0 auto;align:center;">
			<table>
				<tr>					
					<td><g:link controller="module" action="list"><span>Modules</span></g:link></td>
					<td>Configure Information about Component Interface Modules</td>
				</tr>
				<tr>					
					<td><g:link controller="module" action="crashlog"><span>Link Crash Files</span></g:link></td>
					<td>Link Crash Files to Modules</td>
				</tr>
					
				<tr>
					<td><g:link controller="module" action="logFileNames"><span>Link logs files</span></g:link></td>
					<td>Link Configure STB logs to Module</td>
				</tr>
				<tr>					
					<td><g:link controller="streamingDetails" action="list"><span>Streaming Details</span></g:link></td>
					<td>Option to add streaming details</td>
				</tr>	
				<tr>					
					<td><g:link controller="boxManufacturer" action="index"><span>Box Manufacturers</span></g:link></td>
					<td>Option to add Box Manufacturers</td>
				</tr>
				<tr>					
					<td><g:link controller="boxType" action="index"><span>Box Type</span></g:link></td>
					<td>Option to add Box Type</td>
				</tr>
				<tr>					
					<td><g:link controller="RDKVersions" action="index"><span>RDK Versions</span></g:link></td>
					<td>Option to add RDK Versions</td>
				</tr>		
				<tr>					
					<td><g:link controller="soCVendor" action="index"><span>SoC Vendors</span></g:link></td>
					<td>Option to add SoC Vendors</td>
				</tr>	
				<g:if test="${SecurityUtils.subject.principal.equals("admin")}">	
				<tr>					
					<td><g:link controller="groups" action="index"><span>Groups</span></g:link></td>
					<td>Option to add Groups</td>
				</tr>				
				<tr>					
					<td><g:link controller="user" action="index"><span>User Management</span></g:link></td>
					<td>Option to manage users</td>
				</tr>
				</g:if>
				<%--				
				<tr>					
					<td><g:link controller="userGroup" action="index"><span>User Groups</span></g:link></td>
					<td>Option to manage user groups</td>
				</tr>						
			--%></table>
		</div>
	</body>
</html>
