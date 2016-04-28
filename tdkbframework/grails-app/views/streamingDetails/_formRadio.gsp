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
<%@ page import="com.comcast.rdk.RadioStreamingDetails" %>
<div class="fieldcontain ${hasErrors(bean: streamingDetailsInstance, field: 'streamId', 'error')} required">
	<label for="streamId">
		<g:message code="streamingDetails.streamId.label" default="Stream Id" />
		<span class="required-indicator">*</span>
	</label>
	<g:textField name="streamId" required="" value="${streamingDetailsInstance?.streamId}" class="textwidth"/>
</div>
