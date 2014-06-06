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
	<div >
		<table>	
			
			<thead>
				<tr>
				<td colspan="5" align="right" style="color: brown;">Duplicate Ocap Id's are not allowed</td>
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
			<g:each in="${streamingDetailsInstanceList}" status="i" var="streamingDetailsInstance">
				<tr class="${(i % 2) == 0 ? 'even' : 'odd'}">
				
					<td align="center">${fieldValue(bean: streamingDetailsInstance, field: "streamId")}</td>										
				
					<td align="center">${fieldValue(bean: streamingDetailsInstance, field: "channelType")}</td>
				
					<td align="center">${fieldValue(bean: streamingDetailsInstance, field: "audioFormat")}</td>
					
					<td align="center">${fieldValue(bean: streamingDetailsInstance, field: "videoFormat")}</td>
					
					<td align="center"><g:hiddenField name="streamid" value="${streamingDetailsInstance.streamId}" />
					
						<g:textField name="ocapId"  style="width:55px;" required="" value=""/></td>
				</tr>
			</g:each>
			</tbody>
		</table>		
	</div>
	