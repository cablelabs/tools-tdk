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
		$("#searchtable").dataTable({
			"sPaginationType" : "full_numbers"
		});
	});
</script>
<br/>	
<g:if test="${executionInstanceList}">
<div id="list-execution" class="content scaffold-list" role="main">					
	<table id="searchtable">
		<thead>					
			<tr>
				<th>Execution Name</th>						
				<th>Script/ScriptGroup</th>						
				<th>Device</th>						
				<th>DateOfExecution</th>
				<th>Result</th>					
			</tr>
		</thead>
		<tbody>
		  <g:each in="${executionInstanceList}" status="i" var="executionInstance">			
			<tr class="${(i % 2) == 0 ? 'even' : 'odd'}">				
				<td align="center" nowrap>${fieldValue(bean: executionInstance, field: "name")}</td>				
				<td align="center">
					<g:if test="${executionInstance?.script}">
						${fieldValue(bean: executionInstance, field: "script")}
					</g:if>
					<g:else>
						${fieldValue(bean: executionInstance, field: "scriptGroup")}
					</g:else>													
				</td>					
				<td align="center" nowrap>${fieldValue(bean: executionInstance, field: "device")}</td>				
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
			</tr>
		  </g:each>
		</tbody>
	</table>
</div>			
</g:if>