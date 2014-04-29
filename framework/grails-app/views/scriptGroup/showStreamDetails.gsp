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
 <script type="text/javascript">
	        $(document).ready(function(){	
	        	$("#locktable").dataTable( {
					"sPaginationType": "full_numbers"
				} );		        	
			});	   
</script>
<div id="list-streamingDetails" class="content scaffold-list" role="main">
	<g:set var="entityName" value="${message(code: 'streamingDetails.label', default: 'StreamingDetails')}" />

	<h1><g:message code="default.list.label" args="[entityName]" /></h1>
	
	<table  id="locktable" class="display">
		<thead>			
           <tr>
                   <th>StreamId</th>                             
                   <th>ChannelType</th>
                   <th>AudioFormat</th>
                   <th>VideoFormat</th>
           </tr>              
		</thead>
		<tbody>
		<g:each in="${streamingDetailsInstanceList}" status="i" var="streamingDetailsInstance">
			<tr class="${(i % 2) == 0 ? 'even' : 'odd'}">
			
				<td class="center">${fieldValue(bean: streamingDetailsInstance, field: "streamId")}</td>							
			
				<td class="center">${fieldValue(bean: streamingDetailsInstance, field: "channelType")}</td>
			
				<td class="center">${fieldValue(bean: streamingDetailsInstance, field: "audioFormat")}</td>
				
				<td class="center">${fieldValue(bean: streamingDetailsInstance, field: "videoFormat")}</td>
			
			</tr>
		</g:each>
		</tbody>
	</table>
	
</div>

