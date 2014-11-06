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
<%@ page import="com.comcast.rdk.StreamingDetails" %>
<%@ page import="com.comcast.rdk.RadioStreamingDetails" %>
	<g:if  test="${deviceStreams?.size() > 0 }" >
	
	<div>
		<table>		
			<thead>
				<tr>
				<td colspan="5" align="right" style="color: brown;">Duplicate Ocap Id's are not allowed </td>
				</tr>
				<tr>
				
					<th>Stream Id</th>
																					
					<th>Channel Type</th>
				
					<th>Audio Format</th>
					
					<th>Video Format</th>
										
					<th>Ocap Id</th>
				
				</tr>
			</thead>
			<tbody>
			<g:each in="${deviceStreams}" status="i" var="deviceStream">
				<tr class="${(i % 2) == 0 ? 'even' : 'odd'}">
				
					<td align="center">${deviceStream?.stream?.streamId}</td>										
				
					<td align="center">${deviceStream?.stream?.channelType}</td>
				
					<td align="center">${deviceStream?.stream?.audioFormat}</td>
					
					<td align="center">${deviceStream?.stream?.videoFormat}</td>
					
					<td align="center"><g:hiddenField name="streamid" value="${deviceStream?.stream?.streamId}" />
					
					<g:textField name="ocapId"  style="width:55px;" required="" value="${deviceStream?.ocapId}"/></td>
				</tr>
			</g:each>
			<g:if test="${showBlankRadio}">
			<g:each in="${blankList}" status="i" var="streamingDetailsInstance">
			<tr class="${(i % 2) == 0 ? 'even' : 'odd'}">
				
					<td align="center">${fieldValue(bean: streamingDetailsInstance, field: "streamId")}</td>										
				
					<td align="center">Radio</td>
					
					<td align="center">N/A</td>
					
					<td align="center">N/A</td>
				
					<td align="center"><g:hiddenField name="streamid" value="${streamingDetailsInstance.streamId}" />
					
						<g:textField name="ocapId"  style="width:55px;" required="" value=""/></td>
				</tr>
			</g:each>
			</g:if>
			<g:else>
			<g:each in="${radiodeviceStreams}" status="i" var="streamingDetailsInstance">
				<tr class="${(i % 2) == 0 ? 'even' : 'odd'}">
				
					<td align="center">${fieldValue(bean: streamingDetailsInstance, field: "stream.streamId")}</td>										
				
					<td align="center">Radio</td>
					
					<td align="center">N/A</td>
					
					<td align="center">N/A</td>
				
					<td align="center"><g:hiddenField name="streamid" value="${streamingDetailsInstance.stream.streamId}" />
					
						<g:textField name="ocapId"  style="width:55px;" required="" value="${streamingDetailsInstance?.ocapId}"/></td>
				</tr>
			</g:each>
			</g:else>
			</tbody>
		</table>
		
	</div>
	</g:if>