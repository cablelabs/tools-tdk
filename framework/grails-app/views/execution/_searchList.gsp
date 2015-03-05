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
<%@ page import="com.comcast.rdk.Execution" %>
<script type="text/javascript">
	$(document).ready(function() {
		oTable = $("#searchtable").dataTable({
			"sPaginationType" : "full_numbers"
		});
		oTable.fnSort( [ [3,'desc'] ] );
	});
</script>
<br/>	
<g:if test="${executionInstanceList}">
<div id="list-execution" class="content scaffold-list" role="main">					
	<table id="searchtable" style="table-layout:fixed;">
		<thead>					
			<tr>
				<th>Execution Name</th>						
				<th>Script/ScriptGroup</th>						
				<th>Device</th>						
				<th>DateOfExecution</th>
				<th>Result</th>	
				<th width = "2%"> </th>					
			</tr>
		</thead>
		<tbody>
		  <g:each in="${executionInstanceList}" status="i" var="executionInstance">			
			<tr class="${(i % 2) == 0 ? 'even' : 'odd'}">				
				<td align="center" style ="width :20% ;  overflow:hidden ; word-wrap:break-word;" >${fieldValue(bean: executionInstance, field: "name")}</td>				
					<g:if test="${executionInstance?.script}">
								 <g:set var="titlevar" value="${fieldValue(bean: executionInstance, field: "script")}"/>
							</g:if>
							<g:else>
								 <g:set var="titlevar" value="${fieldValue(bean: executionInstance, field: "scriptGroup")}"/>
							</g:else>	
						
						<td align="center" style ="width :20% ; word-wrap:break-word;" title="${ titlevar}">
							<g:if test="${executionInstance?.script}">
							 <%
						 String scriptName = executionInstance?.script;
						 if(scriptName.length() > 35){
							 scriptName = scriptName?.substring(0, 32) + "...";
						 }
						  %>
								${scriptName}
							</g:if>
							<g:else>
								${fieldValue(bean: executionInstance, field: "scriptGroup")}
							</g:else>	
							<g:if test=	"${executionInstance?.isBenchMarkEnabled || executionInstance?.isSystemDiagnosticsEnabled }">
								(p)
							</g:if>														
				</td>					
				<td align="center" style ="width :20% ; word-wrap:break-word;">${fieldValue(bean: executionInstance, field: "device")}</td>				
				<td align="center" nowrap>${fieldValue(bean: executionInstance, field: "dateOfExecution")}</td>											
				<td align="center"><g:link onclick="showExecutionLog(${executionInstance.id}); return false;" id="${executionInstance.id}">
					
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
										
				</g:link></td>
						<td >
							<g:if test="${(executionInstance.executionStatus)}"> 							
								<g:if test="${fieldValue(bean: executionInstance, field: 'executionStatus').equals('IN-PROGRESS') || fieldValue(bean: executionInstance, field: 'executionStatus').equals('PAUSED')}"> 
									<g:if test="${executionInstance?.scriptGroup}">
										<img src="../images/execution_stop.png" onclick="stopExecution(${executionInstance.id})" id="${executionInstance.id}" />
									</g:if>
								</g:if>
							</g:if>
							<g:link action="exportConsolidatedToExcel" id="${executionInstance.id}" ><img src="../images/excel.png" /></g:link>
						</td>
			</tr>
		  </g:each>
		</tbody>
	</table>
</div>			
</g:if>