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
<%@ page import="java.io.*"%>
<!DOCTYPE html>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
<title>RDK Test Suite</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<link rel="shortcut icon" href="${resource(dir: 'images', file: 'favicon.ico')}" type="image/x-icon">
<link rel="apple-touch-icon"
	href="${resource(dir: 'images', file: 'apple-touch-icon.png')}">
<link rel="apple-touch-icon" sizes="114x114"
	href="${resource(dir: 'images', file: 'apple-touch-icon-retina.png')}">
<link rel="stylesheet" href="${resource(dir: 'css', file: 'main.css')}"
	type="text/css">
<link rel="stylesheet"
	href="${resource(dir: 'css', file: 'mobile.css')}" type="text/css">
<link rel="stylesheet" href="${resource(dir:'css',file:'basic.css')}"
	type="text/css" />

<g:javascript library="jquery-1.6.1.min" />
<g:javascript library="jquery-ui"/>
<g:javascript library="common"/>

<script type="text/javascript">
function viewOnClick(me,k,i)
{ 
  if(document.getElementById('allmessages'+k+'_'+i).style.display == 'none') {
    document.getElementById('allmessages'+k+'_'+i).style.display = '';
    $('#expander'+k+'_'+i).text('Hide');  
  }
  else {
    document.getElementById('allmessages'+k+'_'+i).style.display = 'none';
    $('#expander'+k+'_'+i).text('Details');    
  }
  return false;
}

$(function() {
	$('#longtext').more({length: 100});
});

function showHideLink(k){
	alert(k);
	$('#hidelink'+k).show();
}

function hideLogs(k){
	$('#showlink'+k).show();
	$('#testSucc'+k).hide();
	$('#hidelink'+k).hide();
}

function showLogs(k){
	$('#hidelink'+k).show();
	$('#testSucc'+k).show();
	$('#showlink'+k).hide();
}

</script>
</head>
<body>
	<div id="grailsLogo" role="banner">
		<img src="${resource(dir: 'images', file: 'rdk_logo.png')}"
			alt="Grails" />
	</div>
	<div
		style="width: 100%; min-width: 100%; text-align: right; border-bottom: 3px solid #CCCCCC; border-bottom-color: #C11B17">		
	</div>
	<hr>
	<table id="maintable">
		<tr>
			<td nowrap="nowrap"
				style="position: absolute; min-width: 500px; height: 20px; width: 947px; background-color: #C8BBBE; border-bottom-color: #C11B17">
				<div id="header" align="left">
					<ul>
						<li></li>
						<li></li>
						<li></li>
						<li></li>
						<li></li>						
					</ul>
				</div>
			</td>
		</tr>
	</table>
	<br>
	<g:if test="${scriptStatus}"><br><br>&emsp;
	<div style="text-align: center;"><h1>${scriptStatus}</h1></div>
	</g:if>

<g:each in="${executionDeviceInstanceList}" status="k"  var="executionDeviceInstance">
<table id="logtable" >
	<tr>
		<th colspan="2">Execution Details</th>		
	</tr>
	<tr class="trborder even">
		<td class="tdhead">Device Name</td>
		<td >${executionDeviceInstance?.device}</td>				
	</tr>
	<tr class="odd">
		<td class="tdhead">IP</td>
		<td>${executionDeviceInstance?.deviceIp}</td>				
	</tr>
	<tr class="odd">
		<td class="tdhead">Time taken for execution(min)</td>
		<td>${executionDeviceInstance?.executionTime}</td>				
	</tr>
	<tr class="trborder even">
		<td class="tdhead">Device Details</td>
		<td>
		<%
			int c = 0
			def fileContents = ""
			def firstfourLine = ""
			try{
			    def filePath = "${request.getRealPath('/')}//logs//version//${executionInstance.id}//${executionDeviceInstance?.id.toString()}//${executionDeviceInstance.id}_version.txt"	
				BufferedReader inn = new BufferedReader(new FileReader(filePath));
				String line;
				while((line = inn.readLine()) != null)
				{				
					if(!(line.isEmpty())){
						if(!(line.startsWith( "=====" ))){
							if(c < 3 )  {
								firstfourLine =  firstfourLine + line + "<br>"
								c++
							}
							fileContents = fileContents + line + "<br>"
						}
					}
				}
		 	}catch(Exception fnf){
           		
       	 	}
		 %>	
		<span id="firstfourlines${k}">${firstfourLine} &emsp; <g:link  onclick="showFulltextDeviceDetails(${k}); return false;"><b><i>Show More</i></b></g:link></span>
		<span id="fulltext${k}" style="display:none;">${fileContents}&emsp; <g:link onclick="showMintextDeviceDetails(${k}); return false;"><b><i>Show Less</i></b></g:link></span>		
		</td>				
	</tr>
	<tr class="odd">
		<th>Test Group</th>
		<th>Result : ${executionInstance?.result}</th>			
	</tr>	
	
	<tr class="even">	
		<td class="tdhead" style="vertical-align: middle; text-align: center;">
		  <g:if test="${executionInstance?.script}">
			${testGroup}		 
		  </g:if>
		  <g:else>
		  	${executionInstance?.scriptGroup}
		  </g:else>
		</td>
		<td>
		<g:each in="${executionDeviceInstance.executionresults}" status="i"  var="executionResultInstance">
		<section class="round-border">
			<table>
				<tr class="scripthead">
					<td class="tdhead">Test Script </td>
					<td>${executionResultInstance?.script}</td>
					<td class="tdhead">Status</td>
					<td>${executionResultInstance?.status}</td>
					<td>
					<a href="#" id="expander${k}_${i}" onclick="this.innerHTML='Hide';viewOnClick(this,${k},${i}); return false;">Details</a>
				</tr>
				<tbody id="allmessages${k}_${i}"  style="display: none;">
				<g:each in="${executionResultInstance.executemethodresults}"  var="executionResultMthdsInstance">
				<tr class="fnhead">
					<td>Function Name</td>
					<td colspan="3">${executionResultMthdsInstance?.functionName}</td>				
				</tr>
				<tr>
					<td>ExpectedResult</td>
					<td colspan="3">${executionResultMthdsInstance?.expectedResult}</td>				
				</tr>
				<tr>
					<td>ActualResult</td>
					<td colspan="3">${executionResultMthdsInstance?.actualResult}</td>				
				</tr>
				<tr>
					<td>Status</td>
					<td colspan="3">${executionResultMthdsInstance?.status}</td>				
				</tr>
				</g:each>
				<tr>
					<td>Log Data </td>
					<td colspan="3"><div style="overflow : auto; height : 180px;">${executionResultInstance?.executionOutput}</div></td>				
				</tr>
				</tbody>
			</table>
			</section>
		</g:each>	
		</td>
	</tr>
	<tr>
		<td colspan="2">
			<g:remoteLink action="showLogFiles" id="1" update="testSucc${k}" onSuccess="showHideLink(${k});" params="[execDeviceId:"${executionDeviceInstance?.id}", execId:"${executionInstance?.id}"]">Show Log Files</g:remoteLink>						
			&emsp;<span id="hidelink${k}" style="display:none;"><a style="color:#7E2217;" href="#" onclick="hideLogs(${k})">Hide</a></span>
			<span id="showlink${k}" style="display:none;"><a style="color:#7E2217;" href="#" onclick="showLogs(${k})">Show</a></span>
			<div id="testSucc${k}"></div>
		</td>	
	</tr>
</table>	
</g:each>

</body>
</html>

<%--<!DOCTYPE html>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
<title>RDK Test Suite</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<link rel="shortcut icon" href="${resource(dir: 'images', file: 'favicon.ico')}" type="image/x-icon">
<link rel="apple-touch-icon"
	href="${resource(dir: 'images', file: 'apple-touch-icon.png')}">
<link rel="apple-touch-icon" sizes="114x114"
	href="${resource(dir: 'images', file: 'apple-touch-icon-retina.png')}">
<link rel="stylesheet" href="${resource(dir: 'css', file: 'main.css')}"
	type="text/css">
<link rel="stylesheet"
	href="${resource(dir: 'css', file: 'mobile.css')}" type="text/css">
<link rel="stylesheet" href="${resource(dir:'css',file:'basic.css')}"
	type="text/css" />

<g:javascript library="jquery-1.6.1.min" />
<g:javascript library="jquery-ui"/>
<g:javascript library="common"/>

<script type="text/javascript">


function viewOnClick(me,i)
{
  if(document.getElementById('allmessages'+i).style.display == 'none') {
    document.getElementById('allmessages'+i).style.display = '';
    $('#expander'+i).text('Hide');  
  }
  else {
    document.getElementById('allmessages'+i).style.display = 'none';
    $('#expander'+i).text('Details');    
  }
  return false;
}



</script>

</head>
<body>
	<div id="grailsLogo" role="banner">
		<img src="${resource(dir: 'images', file: 'rdk_logo.png')}"
			alt="Grails" />
	</div>
	<div
		style="width: 100%; min-width: 100%; text-align: right; border-bottom: 3px solid #CCCCCC; border-bottom-color: #C11B17">		
	</div>
	<hr>
	<table id="maintable">
		<tr>
			<td nowrap="nowrap"
				style="position: absolute; min-width: 500px; height: 20px; width: 947px; background-color: #C8BBBE; border-bottom-color: #C11B17">
				<div id="header" align="left">
					<ul>
						<li></li>
						<li></li>
						<li></li>
						<li></li>
						<li></li>						
					</ul>
				</div>
			</td>
		</tr>
	</table>
	<br>
	<g:if test="${scriptStatus}"><br><br>&emsp;
	<div style="text-align: center;"><h1>${scriptStatus}</h1></div>
	</g:if>

<table id="logtable" >
	<tr>
		<th colspan="2">Execution Details</th>		
	</tr>	
	<tr class="trborder even">
		<td class="tdhead">Device Name</td>
		<td >${executionInstance?.device}</td>				
	</tr>
	<tr class="odd">
		<td class="tdhead">IP</td>
		<td>${stbIp}</td>				
	</tr>
	<tr class="trborder even">
		<td class="tdhead">Time taken for execution(min)</td>
		<td>${executionInstance?.executionTime}</td>				
	</tr>
	
	<tr class="odd">
		<th>Test Group</th>
		<th>Result : ${executionInstance?.result}</th>			
	</tr>	
	
	<tr class="even">	
		<td class="tdhead" style="vertical-align: middle; text-align: center;">
		  <g:if test="${executionInstance?.script}">
			${testGroup}		 
		  </g:if>
		  <g:else>
		  	${executionInstance?.scriptGroup}
		  </g:else>
		</td>
		<td>
		<g:each in="${executionResultInstanceList}" status="i"  var="executionResultInstance">
		<section class="round-border">
			<table>
				<tr class="scripthead">
					<td class="tdhead">Test Script</td>
					<td>${executionResultInstance?.script}</td>
					<td class="tdhead">Status</td>
					<td>${executionResultInstance?.status}</td>
					<td>
					<a href="#" id="expander${i}" onclick="this.innerHTML='Hide';viewOnClick(this,${i}); return false;">Details</a>
				</tr>
				<tbody id="allmessages${i}"  style="display: none;">
				<g:each in="${executionResultInstance.executemethodresults}"  var="executionResultMthdsInstance">
				<tr class="fnhead">
					<td>Function Name</td>
					<td colspan="3">${executionResultMthdsInstance?.functionName}</td>				
				</tr>
				<tr>
					<td>ExpectedResult</td>
					<td colspan="3">${executionResultMthdsInstance?.expectedResult}</td>				
				</tr>
				<tr>
					<td>ActualResult</td>
					<td colspan="3">${executionResultMthdsInstance?.actualResult}</td>				
				</tr>
				<tr>
					<td>Status</td>
					<td colspan="3">${executionResultMthdsInstance?.status}</td>				
				</tr>
				</g:each>
				<tr>
					<td>Log Data </td>
					<td colspan="3"><div style="overflow : auto; height : 180px;">${executionResultInstance?.executionOutput}</div></td>				
				</tr>
				
				</tbody>
			</table>
			</section>
		</g:each>	
		</td>
	</tr>	
	<tr>		
		<td>			
			<g:if test="${logFileNames}">
				Log Files
			</g:if>
		</td>
		<td>
			<table>
				<tr><g:if test="${logFileNames}">
					<th>FunctionName</th>
					<th>Test Details</th>
					</g:if>
				</tr>
				<g:each in="${logFileNames}" status="i"  var="fileName">				
				<tr><%  j = i + 1 %>
					<td>
					<g:form controller="execution">
					<g:link style="text-decoration:none;" action="showExecutionLog" id="${executionInstance?.id+"_"+fileName.key}" >
					<span class="customizedLink" >${j} &nbsp;:&nbsp; ${fileName.key} </span>	
					</g:link>
					</g:form>			
					</td>
					<td>${fileName.value}</td>
				</tr>				
				</g:each>
			</table>
		</td>		
	</tr>
</table>	


	<br>
	<div class="footer" role="contentinfo"></div>
	<div id="spinner" class="spinner" style="display: none;">
		<g:message code="spinner.alt" default="Loading&hellip;" />
	</div>
			<g:javascript library="application"/>
			<r:layoutResources />
	
</body>
</html>




--%>