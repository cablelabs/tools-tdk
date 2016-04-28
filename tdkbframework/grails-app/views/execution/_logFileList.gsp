
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
--><%@ page import="com.comcast.rdk.Execution" %>
<g:if test="${logFileNames}">
<table>	
	<tr>
		<th>Download the log file </th>
		<%--<th>Test Details</th>		
	--%></tr>
	<g:each in="${logFileNames}" status="i"  var="fileName">				
	<tr><%  j = i + 1 %>
		<td>
		<g:form controller="execution">
		<g:link style="text-decoration:none;" action="showExecutionLog" id="${execId+"_"+fileName.key}" 
		 params="[execId: "${execId}", execDeviceId: "${execDeviceId}", execResultId: "${execResId}" ]" >
		<%--<span class="customizedLink" >${j} &nbsp;:&nbsp; ${fileName.key} </span>	--%>
		<span class="customizedLink" >${fileName.key}</span>	
		</g:link>
		</g:form>			
		</td>
		<%--<td>${fileName.value}</td>
	--%>
	</tr>				
	</g:each>
</table>
</g:if>