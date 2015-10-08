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
<%@page import="java.text.DecimalFormat"%>
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

function showHideLink(k,i){
	$('#hidelink'+k+'_'+i).show();
	$('#showlink'+k+'_'+i).hide();
	$('#testSucc'+k+'_'+i).show();
}

function hideLogs(k,i){
	$('#showlink'+k+'_'+i).show();
	$('#testSucc'+k+'_'+i).hide();
	$('#hidelink'+k+'_'+i).hide();
}

/*function showLogs(k){
	$('#hidelink'+k).show();
	$('#testSucc'+k).show();
	$('#showlink'+k).hide();
}*/

function showCrashHideLink(k,i){
	$('#hidecrashlink'+k+'_'+i).show();
	$('#showcrashlink'+k+'_'+i).hide();
	$('#testCrashSucc'+k+'_'+i).show();
}

function hideCrashLogs(k,i){
	$('#showcrashlink'+k+'_'+i).show();
	$('#testCrashSucc'+k+'_'+i).hide();
	$('#hidecrashlink'+k+'_'+i).hide();
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
		<th colspan="2">Execution Status</th>	
	</tr>
	<tr class="trborder even">
		<td colspan="2" align="right">
		<g:link action="exportConsolidatedPerfToExcel" params="[id:"${executionInstance?.id}"]" >Download Consolidated Performance Report(Excel)</g:link>
		</td>		
	</tr>		
	<tr class="trborder even">
		<td class="tdhead">Device Name (IP)</td>
		<td >${executionDeviceInstance?.device}(${executionDeviceInstance?.deviceIp})</td>				
	</tr>
	<tr class="trborder even">
		<td class="tdhead">Date Of Execution</td>
		<td >${executionInstance?.dateOfExecution}</td>				
	</tr>
	<tr class="odd">
		<td class="tdhead">Time taken for script execution(min)</td>
		<%
			String time = executionInstance?.executionTime
			try{
				if(time && time?.length() > 0 && time?.contains(".")){
					int indx = ((time.indexOf(".") + 3) <= time?.length() )?  (time.indexOf(".") + 3) : (time?.length() )
					time = time.substring(0, time.indexOf(".")+3);
				}
			}catch(Exception e){
			}
		 %>
		<td>${time}</td>				
	</tr>
	<tr class="odd">
		<td class="tdhead">Time taken for Complete execution(min)</td>
		<%
			String time1 = executionInstance?.realExecutionTime
			try{
				if(time1 && time1?.length() > 0 && time1?.contains(".")){
					int indx = ((time1.indexOf(".") + 3) <= time1?.length() )?  (time1.indexOf(".") + 3) : (time1?.length() )
					time1 = time1.substring(0, time1.indexOf(".")+3);
				}
			}catch(Exception e){
			}
		 %>
		<td>${time1}</td>				
	</tr>
	
	<tr class="trborder even">
		<td class="tdhead">Image Name </td>		
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
			<b>Unable to fetch Device Details</b>
		</g:else>
		</td>				
	</tr>
	<tr class="odd">
		<th>Test Group 
		</th>
		<th align="left">
		 <g:if test="${executionInstance?.script}">
			${testGroup}		 
		  </g:if>
		  <g:else>
		  	${executionInstance?.scriptGroup}
		  </g:else> &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
		  
		  Result : 
		  <g:if test="${ !(executionInstance.result) }" >FAILURE						
							</g:if>
							<g:else>
							<g:if test="${(executionInstance.executionStatus)}"> 
							
							<g:if test="${fieldValue(bean: executionInstance, field: 'executionStatus').equals('COMPLETED')}"> 
								${fieldValue(bean: executionInstance, field: "result")}
							</g:if>
							<g:else>
								${fieldValue(bean: executionInstance, field: "executionStatus")}
							</g:else>
							</g:if>	
							<g:else>
								${fieldValue(bean: executionInstance, field: "result")}
							</g:else>
							</g:else>	
		</th>			
	</tr>	
	<tr class="even">
		
		<td colspan="8">
			<table style="font: normal;font-size: 12px">
			<g:if test="${tDataMap?.size() > 0}">
			<tr class="even">
						<td class="tdhead" style="white-space:nowrap;text-align: left; min-width: 10%;max-width: 10%;background-color: #b0beb3;">Module Name</td>
						<td class="tdhead" style="white-space:nowrap;text-align: left;min-width: 10%;max-width: 10%;background-color: #b0beb3;">Executed</td>
						<td class="tdhead" style="white-space:nowrap;text-align: left;min-width: 10%;max-width: 10%;background-color: #b0beb3;">SUCCESS</td>
						<td class="tdhead" style="white-space:nowrap;text-align: left;min-width: 10%;max-width: 10%;background-color: #b0beb3;">FAILURE</td>
						<td class="tdhead" style="white-space:nowrap;text-align: left;min-width: 10%;max-width: 10%;background-color: #b0beb3;">SCRIPT TIME OUT</td>
						<td class="tdhead" style="white-space:nowrap;text-align: left;min-width: 10%;max-width: 10%;background-color: #b0beb3;">N/A</td>
						<td class="tdhead" style="white-space:nowrap;text-align: left;min-width: 10%;max-width: 10%;background-color: #b0beb3;">SKIPPED</td>
						<td class="tdhead" style="white-space:nowrap;text-align: left;min-width: 10%;max-width: 10%;background-color: #b0beb3;">PASS %</td>
				</tr>
			<g:each in="${detailDataMap?.keySet()}" status="i"  var="moduleName">						
					<% def mapp =  detailDataMap?.get(moduleName)
					%>
				  <tr class="${i % 2 == 0 ? 'even' : 'odd'}">
						<td class="tdhead" style="white-space:nowrap;text-align: left;">${moduleName}</td>
						<td style="white-space:nowrap;text-align: right;">
						<g:if test="${mapp?.get("Executed") != null}">
							${mapp?.get("Executed")}
						</g:if>
						<g:else>
							0
						</g:else>
						</td>
						<td style="white-space:nowrap;text-align: right;">
						<g:if test="${mapp?.get("SUCCESS") != null}">
							${mapp?.get("SUCCESS")}
						</g:if>
						<g:else>
							0
						</g:else>
						</td>
						<td style="white-space:nowrap;text-align: right;">
						<g:if test="${mapp?.get("FAILURE") != null}">
							${mapp?.get("FAILURE")}
						</g:if>
						<g:else>
							0
						</g:else>
						</td>
						<td style="white-space:nowrap;text-align: right;">
						<g:if test="${mapp?.get("SCRIPT TIME OUT") != null}">
							${mapp?.get("SCRIPT TIME OUT")}
						</g:if>
						<g:else>
							0
						</g:else>
						</td>
						<td style="white-space:nowrap;text-align: right;">
						<g:if test="${mapp?.get("N/A") != null}">
							${mapp?.get("N/A")}
						</g:if>
						<g:else>
							0
						</g:else>
						</td>
						<td style="white-space:nowrap;text-align: right;">
						<g:if test="${mapp?.get("SKIPPED") != null}">
							${mapp?.get("SKIPPED")}
						</g:if>
						<g:else>
							0
						</g:else>
						</td>
						<td style="white-space:nowrap;text-align: right;">
						<g:if test="${mapp?.get("passrate") != null}">
							${mapp?.get("passrate")}
						</g:if>
						<g:else>
							0
						</g:else>
						</td>
				</tr>
			</g:each>
			<tr class="even">
						<td class="tdhead" style="white-space:nowrap;text-align: left;font-weight: bold;background-color: #C4C3C7;">Total</td>
						<td style="white-space:nowrap;text-align: right;font-weight: bold;background-color: #C4C3C7;">
						<g:if test="${tDataMap?.get("Executed") != null}">
							${tDataMap?.get("Executed")}
						</g:if>
						<g:else>
							0
						</g:else>
						</td>
						<td style="white-space:nowrap;text-align: right;font-weight: bold;background-color: #C4C3C7;">
						<g:if test="${tDataMap?.get("SUCCESS") != null}">
							${tDataMap?.get("SUCCESS")}
						</g:if>
						<g:else>
							0
						</g:else>
						</td>
						<td style="white-space:nowrap;text-align: right;font-weight: bold;background-color: #C4C3C7;">
						<g:if test="${tDataMap?.get("FAILURE") != null}">
							${tDataMap?.get("FAILURE")}
						</g:if>
						<g:else>
							0
						</g:else>
						</td>
						<td style="white-space:nowrap;text-align: right;font-weight: bold;background-color: #C4C3C7;">
						<g:if test="${tDataMap?.get("SCRIPT TIME OUT") != null}">
							${tDataMap?.get("SCRIPT TIME OUT")}
						</g:if>
						<g:else>
							0
						</g:else>
						</td>
						<td style="white-space:nowrap;text-align: right;font-weight: bold;background-color: #C4C3C7;">
						<g:if test="${tDataMap?.get("N/A") != null}">
							${tDataMap?.get("N/A")}
						</g:if>
						<g:else>
							0
						</g:else>
						</td>
						<td style="white-space:nowrap;text-align: right;font-weight: bold;background-color: #C4C3C7;">
						<g:if test="${tDataMap?.get("SKIPPED") != null}">
							${tDataMap?.get("SKIPPED")}
						</g:if>
						<g:else>
							0
						</g:else>
						</td>
						<td style="white-space:nowrap;text-align: right;font-weight: bold;background-color: #C4C3C7;">
						<g:if test="${tDataMap?.get("passrate") != null}">
							${tDataMap?.get("passrate")}
						</g:if>
						<g:else>
							0
						</g:else>
						</td>
				</tr>
			</g:if>
			</table>	
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