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
<%@ page import="com.comcast.rdk.ExecutionResult"%>
<%@ page import="com.comcast.rdk.Performance"%>
<%@ page import="com.comcast.rdk.DeviceDetails"%>
<%@ page import="com.comcast.rdk.Device"%>
<head>
<script type='text/javascript'>
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

function viewOnClickperf(me,k,i)
{ 
  if(document.getElementById('allmessagesperf'+k+'_'+i).style.display == 'none') {
    document.getElementById('allmessagesperf'+k+'_'+i).style.display = '';
    $('#expanderperf'+k+'_'+i).text('Hide');  
  }
  else {
    document.getElementById('allmessagesperf'+k+'_'+i).style.display = 'none';
    $('#expanderperf'+k+'_'+i).text('Show');    
  }
  return false;
}

$(function() {
	$('#longtext').more({length: 100});
});

function showHideLink(k){
	$('#hidelink'+k).show();
	$('#showlink'+k).hide();
	$('#testSucc'+k).show();
}

function hideLogs(k){
	$('#showlink'+k).show();
	$('#testSucc'+k).hide();
	$('#hidelink'+k).hide();
}

/*function showLogs(k){
	$('#hidelink'+k).show();
	$('#testSucc'+k).show();
	$('#showlink'+k).hide();
}*/

function showCrashHideLink(k){
	$('#hidecrashlink'+k).show();
	$('#showcrashlink'+k).hide();
	$('#testCrashSucc'+k).show();
}

function hideCrashLogs(k){
	$('#showcrashlink'+k).show();
	$('#testCrashSucc'+k).hide();
	$('#hidecrashlink'+k).hide();
}

/*function showCrashLogs(k){
	$('#hidecrashlink'+k).show();
	$('#testCrashSucc'+k).show();
	$('#showcrashlink'+k).hide();
}*/

function showConsoleHideLink(k,i){
	$('#hideconsolelink'+k+'_'+i).show();
	$('#consoleLog'+k+'_'+i).show();
	$('#showconsolelink'+k+'_'+i).hide();
}

function hideConsoleLogs(k,i){
	$('#showconsolelink'+k+'_'+i).show();
	$('#consoleLog'+k+'_'+i).hide();
	$('#hideconsolelink'+k+'_'+i).hide();
}

/*function showConsoleLogs(k,i){
	$('#hideconsolelink'+k+'_'+i).show();
	$('#consoleLog'+k+'_'+i).show();
	$('#showconsolelink'+k+'_'+i).hide();
}*/

function showParameters(k){
	$('#divDD'+k).show();
	$('#hideDevParam'+k).show();
	$('#showDevParam'+k).hide();
}

function hideParameters(k){
	$('#divDD'+k).hide();
	$('#hideDevParam'+k).hide();
	$('#showDevParam'+k).show();
}

</script>


<g:if test="${executionDeviceInstanceList?.size() > 0}">

<g:each in="${executionDeviceInstanceList}" status="k"  var="executionDeviceInstance">
<table id="logtable" >
	<tr>
		<th colspan="2">Execution Details</th>	
	</tr>
	<tr class="trborder even">
		<td colspan="2" align="right">
		<g:link action="writexmldata" params="[execName:"${executionInstance?.name}"]" >Download Result(xml)</g:link>	
		</td>		
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
		<td class="tdhead">Device Parameters</td>
		<td>		
			<%
			   def device = Device.findByStbName(executionDeviceInstance?.device) 
			   def deviceDetailsList = DeviceDetails.findAllByDevice(device)	
			%>			
			<g:if test="${deviceDetailsList}">
						
			<span id="showDevParam${k}" ><g:link  onclick="showParameters(${k}); return false;"><b><i>Show</i></b></g:link></span>
		    <span id="hideDevParam${k}" style="display:none;"><g:link onclick="hideParameters(${k}); return false;"><b><i>Hide</i></b></g:link></span>		
						
			<div id="divDD${k}" style="display:none;width: 600px;overflow: auto;">			
				<table style="width:70%;">
					<g:each in="${deviceDetailsList}" var="deviceDetailsInstance">
						<tr>
							<td>${deviceDetailsInstance.deviceParameter}</td>
							<td>${deviceDetailsInstance.deviceValue}</td>
						</tr>
					</g:each>
				</table>			
			</div>	
			</g:if>
			<g:else>
				Not Available
			</g:else>	
		</td>				
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
		<g:if test="${!(fileContents.isEmpty())}">
			<span id="showlessdd${k}" style="display:none;"><g:link onclick="showMintextDeviceDetails(${k}); return false;"><b><i>Show Less</i></b></g:link></span><br>
			<span id="firstfourlines${k}">${firstfourLine} &emsp; <g:link  onclick="showFulltextDeviceDetails(${k}); return false;"><b><i>Show More</i></b></g:link></span>
			<span id="fulltext${k}" style="display:none;">${fileContents}&emsp; </span>
		</g:if>		
		<g:else>
			<b>Unable to fetch Device Details due to Network Traffic error</b>
		</g:else>
		</td>				
	</tr>
	<tr class="odd">
		<th>Test Group</th>
		<th>Result : ${executionDeviceInstance?.status}</th>			
	</tr>	
	<tr class="even">
		<td></td>
		<td>
			<table >
			<g:if test="${(statusResults?.get(executionDeviceInstance))?.size() > 0}">
			<tr class="scripthead" >
					<td colspan="2" class="tdhead">Summary</td>
			</tr>
			</g:if>
			<g:each in="${statusResults.get(executionDeviceInstance)}" status="i"  var="executionStatusInstance">						
				<g:each in="${executionStatusInstance}"  var="statusItem">		
					
				  <tr class="even">
						<td class="tdhead" style="white-space:nowrap;text-align: right;">${statusItem.key }</td>
						<td>${statusItem.value }</td>
					</tr>
				</g:each>		   
			</g:each>
			</table>	
		</td>
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

		<g:each in="${executionresults.get(executionDeviceInstance)}" status="i"  var="executionResultInstance">
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
					<td colspan="4">${executionResultMthdsInstance?.functionName}</td>				
				</tr>
				<tr>
					<td>ExpectedResult</td>
					<td colspan="4">${executionResultMthdsInstance?.expectedResult}</td>				
				</tr>
				<tr>
					<td>ActualResult</td>
					<td colspan="4">${executionResultMthdsInstance?.actualResult}</td>				
				</tr>
				<tr>
					<td>Status</td>
					<td colspan="4">${executionResultMthdsInstance?.status}</td>				
				</tr>
				</g:each>
				<tr>
					<td>Log Data </td>
					<td colspan="4"><div style="overflow : auto; height : 180px;">${executionResultInstance?.executionOutput}</div></td>				
				</tr>
				
				<tr>
					<td>Agent Console Log		
					
					</td>	
					<td colspan="4">
						&emsp;<span id="showconsolelink${k}_${i}" >
						<g:remoteLink action="showAgentLogFiles" update="consoleLog${k}_${i}" onSuccess="showConsoleHideLink(${k},${i});" params="[execResId : "${executionResultInstance?.id}", execDeviceId:"${executionDeviceInstance?.id}", execId:"${executionInstance?.id}"]">Show</g:remoteLink>						
						</span>

						<span id="hideconsolelink${k}_${i}" style="display:none;"><a style="color:#7E2217;" href="#" onclick="hideConsoleLogs(${k},${i})">Hide</a></span>
					</td>					
				</tr>
				<tr>
					<td></td>
					<td colspan="4">
						<div id="consoleLog${k}_${i}"></div>	
						
					</td>	
				</tr>

				</tbody>
			</table>
			</section>			
			<g:if test="${executionResultInstance.performance}">
			<table>
						<tr class="scripthead">
							<td colspan="4" class="tdhead">Performance</td>					
							<td>
							<a href="#" id="expanderperf${k}_${i}" onclick="this.innerHTML='Hide';viewOnClickperf(this,${k},${i}); return false;">Show</a>
						</tr>
						</table>
						<span id="allmessagesperf${k}_${i}"  style="display: none;">
						<section class="round-border">
						
						<%
							def performance = Performance.findAllByExecutionResultAndPerformanceType(executionResultInstance,"BenchMark")							
						%>
						<table>
						<g:if test="${performance}">					
						<tbody >
							<tr class="fnhead">
								<td class="tdhead">Performance Type</td>
								<td>BenchMarking</td>
							</tr>
							<tr class="fnhead1">												
								<td class="tdhead">API Name</td>
								<td class="tdhead">Execution Time(millisec)</td>							
							</tr>
							<g:each in="${performance}"  var="performanceInstance">
								<tr>																					
									<td>${performanceInstance?.processName}</td>												
									<td >${performanceInstance?.processValue}</td>				
								</tr>					
							</g:each>						
						</tbody>
						</g:if>						
					</table>
					
						<%
							def performance1 = Performance.findAllByExecutionResultAndPerformanceType(executionResultInstance,"SYSTEMDIAGNOSTICS")													
						%>
						<table>	
						<tr class="fnhead">
								<td class="tdhead">Performance Type</td>
								<td>System Diagnostics</td>
								<td></td>
						</tr>				
						<tbody>
							<g:if test="${performance1}">
							<tr class="fnhead1">					
								<td class="tdhead">Diagnostic Type</td>
								<td class="tdhead">Value</td>									
							</tr>
							<g:each in="${performance1}"  var="performanceInstance1">
								<tr>																									
									<td>${performanceInstance1?.processName}</td>
									<td>${performanceInstance1?.processValue}</td>							
								</tr>					
							</g:each>
							</g:if>					
						</tbody>
						</table>
				</section>		
				</span>		
			</g:if>
		</g:each>	
		</td>
	</tr>
	<tr>
		<td colspan="2">
			<b>Log Files</b>						
			&emsp;<span id="hidelink${k}" style="display:none;"><a style="color:#7E2217;" href="#" onclick="hideLogs(${k})">Hide</a></span>
			<span id="showlink${k}">
			&emsp;<g:remoteLink style="color:#7E2217;" action="showLogFiles" id="1" update="testSucc${k}" onSuccess="showHideLink(${k});" params="[execDeviceId:"${executionDeviceInstance?.id}", execId:"${executionInstance?.id}"]">Show</g:remoteLink>								
			</span>
			<div id="testSucc${k}"></div>
		</td>	
	</tr>
	<tr>
		<td colspan="2">
			<b>Crash Log Files</b>					
			&emsp;<span id="hidecrashlink${k}" style="display:none;"><a style="color:#7E2217;" href="#" onclick="hideCrashLogs(${k})">Hide</a></span>
			&emsp;<span id="showcrashlink${k}">			
			<g:remoteLink style="color:#7E2217;" action="showCrashLogFiles" id="1" update="testCrashSucc${k}" onSuccess="showCrashHideLink(${k});" params="[execDeviceId:"${executionDeviceInstance?.id}", execId:"${executionInstance?.id}"]">Show</g:remoteLink>
			</span>
			<div id="testCrashSucc${k}"></div>
		</td>	
	</tr>
</table>	
</g:each>

</g:if>
<g:else>
<div>
${executionInstance?.outputData}
</div>
</g:else>