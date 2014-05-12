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
	<g:if test="${executionInstanceList}">
		<div id="list-executor" class="content scaffold-list" role="main">		
			<div id="historytable" style="width:99%; overflow: auto;">		
			<table>
				<thead>
					<tr>
						<th colspan="7" align="center" style="width:50%;" ><h1>Executed Script Details</h1></th>
					</tr>
					<tr>
						<g:sortableColumn style="width:2%;" property="markAll" title="${message(code: 'execution.result.label', default: '        ')}" />
						
						<g:sortableColumn style="width:25%;" property="name" title="${message(code: 'execution.name.label', default: 'Execution Name')}" />
						
						<th width="35%">Script/ScriptGroup</th>
						
						<g:sortableColumn style="width:14%;" property="device" title="${message(code: 'execution.device.label', default: 'Device')}" />
					
						<g:sortableColumn style="width:15%;" property="dateOfExecution" title="${message(code: 'execution.dateOfExecution.label', default: 'Date Of Execution')}" />
					
						<g:sortableColumn style="width:10%;" property="result" title="${message(code: 'execution.result.label', default: 'Result')}" />
						<th width="10%"></th>
						<g:sortableColumn style="width:10%;" property="export" title="${message(code: 'execution.result.label', default: '        ')}" />
					    
					</tr>
				</thead>
				<tbody>
				<g:each in="${executionInstanceList}" status="i" var="executionInstance">
				
					<tr class="${(i % 2) == 0 ? 'even' : 'odd'}">
					
						<td align="left" width="2%">
						<g:if test="${executionInstance.isMarked == 1 }">
							 <g:checkBox name="deleteExecutionCheckbox" id="${executionInstance?.id}" class="resultCheckbox" onClick="mark(this);" checked="true"/>
						</g:if>
						<g:else>
							<g:checkBox name="deleteExecutionCheckbox" id="${executionInstance?.id}" class="resultCheckbox" onClick="mark(this);" />
						</g:else>
						 </td>
						<td align="center" width="20%">${fieldValue(bean: executionInstance, field: "name")}</td>
						<td align="center" width="30%">
							<g:if test="${executionInstance?.script}">
								${fieldValue(bean: executionInstance, field: "script")}
							</g:if>
							<g:else>
								${fieldValue(bean: executionInstance, field: "scriptGroup")}
							</g:else>	
							
							<g:if test=	"${executionInstance?.isBenchMarkEnabled || executionInstance?.isSystemDiagnosticsEnabled }">
								(p)
							</g:if>													
						</td>
						<td align="center" width="15%">${fieldValue(bean: executionInstance, field: "device")}</td>
						<td align="center" nowrap width="15%">${fieldValue(bean: executionInstance, field: "dateOfExecution")}</td>
						<td align="center" width="15%"><g:link onclick="showExecutionLog(${executionInstance.id}); return false;" id="${executionInstance.id}">
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
						</g:link>
						</td>
						<td>
							<g:if test="${(executionInstance.executionStatus)}"> 
							
							<g:if test="${fieldValue(bean: executionInstance, field: 'executionStatus').equals('IN-PROGRESS') || fieldValue(bean: executionInstance, field: 'executionStatus').equals('PAUSED')}"> 
								<g:if test="${executionInstance?.scriptGroup}">
									<img src="../images/execution_stop.png" onclick="stopExecution(${executionInstance.id})" id="${executionInstance.id}" />
								</g:if>
							</g:if>
							</g:if>
						</td>
						<td width="5%">
						 
						<g:link action="exportToExcel" id="${executionInstance.id}" ><img src="../images/excel.png" /></g:link>
						
						</td>
					</tr>
				</g:each>
				</tbody>
			</table>
			</div>
			
			<div class="pagination" style="width: 98%;">
					<input type="checkbox" name="markAll" id="markAll2" class="markAll" onclick="clickCheckbox(this)">
					<label> <b>Mark All </b></label>	
					<img src="../images/trash.png" onclick="deleteResults();return false;" style="cursor: pointer;" alt="Delete"/>
					<g:paginate total="${executorInstanceTotal}" />
			</div>
			
			</div>
			<g:hiddenField name="pageOffset" id="pageOffset" value="${params.offset}"/>
		
	</g:if>