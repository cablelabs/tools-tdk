
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
<table>
	<tr>
		<td colspan="2">			
			<g:if test="${logFileNames}">
				<h1>Crash Log Files</h1>
			</g:if>
		</td>
	</tr>
	<tr><g:if test="${logFileNames}">
		<th align="left">Log Files</th>
		
		</g:if>
	</tr>
	<g:each in="${logFileNames}" status="i"  var="fileName">				
	<tr><%  j = i + 1 %>
		<td>
		<g:form controller="execution">
		<g:link style="text-decoration:none;" action="showCrashExecutionLog" id="${execId+"_"+execDeviceId+"_"+fileName.key}" 
		 params="[execDeviceId: "${execDeviceId}"]" >
		<span class="customizedLink" >${j} &nbsp;:&nbsp; ${fileName.key} </span>	
		</g:link>
		</g:form>			
		</td>
	</tr>				
	</g:each>
</table>