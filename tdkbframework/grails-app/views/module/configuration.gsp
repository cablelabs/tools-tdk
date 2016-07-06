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
<%@ page
	import="org.apache.shiro.SecurityUtils;com.comcast.rdk.Category"%>
<!DOCTYPE html>
<html>
<head>
<meta name="layout" content="main" />
<title>RDK Test Suite</title>
<style type="text/css" media="screen"></style>
<%--<g:javascript library="jquery-1.6.1.min" />
<g:javascript library="jquery.simplemodal" />
<g:javascript library="config_resolver" />
--%><script type="text/javascript">
window.onload = function(){
	$("#rdkB").hide();
	$("#rdkV").hide();
	var ele = document.getElementsByName("chooseCat");
	for(var i=0;i<ele.length;i++)
		ele[i].checked = false;
}

function display(val) {
	if (val.trim() === 'RDKV') {
		$("#rdkB").hide();
		$("#rdkV").show();
	} else if (val.trim() === 'RDKB') {
		$("#rdkV").hide();
		$("#rdkB").show();
	} else {}
}

</script>

</head>
<body>
	<div style="padding: 20px;margin-left:20%;">
		<b style="color: #A24C15;">Choose the configuration Category</b>&nbsp;&nbsp;&nbsp;
		<input type="radio" onclick="display('RDKV')" name="chooseCat">RDK-V</input> &nbsp;&nbsp;
		<input type="radio" onclick="display('RDKB')" name="chooseCat">RDK-B</input>
	</div>
	<br>
	<div id="rdkV">
		<div style="float: left; padding-left: 10%; padding-top: 5%;">
			<h2 style="color: #A24C15;">
				<center>RDK-V</center>
			</h2>
		</div>
		<div style="width: 40%; margin: 0 auto; align: center;">
			<!-- RDK_V -->
			<table>
				<tr>
					<td><g:link controller="module" action="list"
							params="[category: com.comcast.rdk.Category.RDKV]">
							<span>Modules</span>
						</g:link></td>
					<td>Configure Information about Component Interface Modules</td>
				</tr>
				<tr>
					<td><g:link controller="module" action="crashlog"
							params="[category:com.comcast.rdk.Category.RDKV ]">
							<span>Link Crash Files</span>
						</g:link></td>
					<td>Link Crash Files to Modules</td>
				</tr>

				<tr>
					<td><g:link controller="module" action="logFileNames"
							params="[category:com.comcast.rdk.Category.RDKV ]">
							<span>Link logs files</span>
						</g:link></td>
					<td>Link Configure STB logs to Module</td>
				</tr>
				<tr>
					<td><g:link controller="streamingDetails" action="list"
							params="[category:com.comcast.rdk.Category.RDKV]">
							<span>Streaming Details</span>
						</g:link></td>
					<td>Option to add streaming details</td>
				</tr>
				<tr>
					<td><g:link controller="boxManufacturer" action="index"
							params="[category:com.comcast.rdk.Category.RDKV]">
							<span>Box Manufacturers</span>
						</g:link></td>
					<td>Option to add Box Manufacturers</td>
				</tr>
				<tr>
					<td><g:link controller="boxType" action="index"
							params="[category:com.comcast.rdk.Category.RDKV]">
							<span>Box Type</span>
						</g:link></td>
					<td>Option to add Box Type</td>
				</tr>
				<tr>
					<td><g:link controller="RDKVersions" action="index"
							params="[category:com.comcast.rdk.Category.RDKV]">
							<span>RDK Versions</span>
						</g:link></td>
					<td>Option to add RDK Versions</td>
				</tr>
				<tr>
					<td><g:link controller="soCVendor" action="index"
							params="[category:com.comcast.rdk.Category.RDKV ]">
							<span>SoC Vendors</span>
						</g:link></td>
					<td>Option to add SoC Vendors</td>
				</tr>
				<%--<g:if test="${SecurityUtils.subject.principal.equals("admin")}">
					<tr>
						<td><g:link controller="groups" action="index"
								params="[category:com.comcast.rdk.Category.RDKV]">
								<span>Groups</span>
							</g:link></td>
						<td>Option to add Groups</td>
					</tr>
					<tr>
						<td><g:link controller="user" action="index"
								params="[category:com.comcast.rdk.Category.RDKV ]">
								<span>User Management</span>
							</g:link></td>
						<td>Option to manage users</td>
					</tr>
				</g:if>
			--%></table>
		</div>
		</div>

		<div id="rdkB">
			<div style="float: left; padding-left: 10%; padding-top: 5%;">
				<h2 style="color: #A24C15;">
					<center>RDK-B</center>
				</h2>
			</div>
			<div style="width: 40%; margin: 0 auto; align: center;">
				<table>
					<tr>
						<td><g:link controller="module" action="list"
								params="[category:com.comcast.rdk.Category.RDKB]">
								<span>Modules</span>
							</g:link></td>
						<td>Configure Information about Component Interface Modules</td>
					</tr>
					<tr>
						<td><g:link controller="module" action="crashlog"
								params="[category:com.comcast.rdk.Category.RDKB]">
								<span>Link Crash Files</span>
							</g:link></td>
						<td>Link Crash Files to Modules</td>
					</tr>

					<tr>
						<td><g:link controller="module" action="logFileNames"
								params="[category:com.comcast.rdk.Category.RDKB]">
								<span>Link logs files</span>
							</g:link></td>
						<td>Link Configure Broadband logs to Module</td>
					</tr>
					<tr>
						<td><g:link controller="boxManufacturer" action="index"
								params="[category:com.comcast.rdk.Category.RDKB]">
								<span>Box Manufacturers</span>
							</g:link></td>
						<td>Option to add Box Manufacturers</td>
					</tr>
					<tr>
						<td><g:link controller="boxType" action="index"
								params="[category:com.comcast.rdk.Category.RDKB]">
								<span>Box Type</span>
							</g:link></td>
						<td>Option to add Box Type</td>
					</tr>
					<tr>
						<td><g:link controller="RDKVersions" action="index"
								params="[category:com.comcast.rdk.Category.RDKB ]">
								<span>RDK Versions</span>
							</g:link></td>
						<td>Option to add RDK Versions</td>
					</tr>
					<tr>
						<td><g:link controller="soCVendor" action="index"
								params="[category:com.comcast.rdk.Category.RDKB ]">
								<span>SoC Vendors</span>
							</g:link></td>
						<td>Option to add SoC Vendors</td>
					</tr>
					<%--<g:if test="${SecurityUtils.subject.principal.equals("admin")}">
						<tr>
							<td><g:link controller="groups" action="index"
									params="[category:com.comcast.rdk.Category.RDKB]">
									<span>Groups</span>
								</g:link></td>
							<td>Option to add Groups</td>
						</tr>
						<tr>
							<td><g:link controller="user" action="index"
									params="[category:com.comcast.rdk.Category.RDKB]">
									<span>User Management</span>
								</g:link></td>
							<td>Option to manage users</td>
						</tr>
					</g:if>
				--%></table>
			</div>
		</div>

	<div style="padding-top:40px;">
	
		<g:if test="${SecurityUtils.subject.principal.equals("admin")}">
		
		<div style="float: left; padding-left: 10%; ">
				<h2 style="color: #A24C15;">
					<center>Common Configuration</center>
				</h2>
			</div>
			<div style="width: 40%; margin: 0 auto; align: center;">
			<table style="max-width: 60%;">
				<tr>
					<td><g:link controller="groups" action="index">
							<span>Groups</span>
						</g:link></td>
					<td>Option to add Groups</td>
				</tr>
				<tr>
					<td><g:link controller="user" action="index">
							<span>User Management</span>
						</g:link></td>
					<td>Option to manage users</td>
				</tr>
			</table>
			</div>
		</g:if>
	</div>
</body>
</html>