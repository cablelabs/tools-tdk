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
<div class="fieldcontain ${hasErrors(bean: streamingDetailsInstance, field: 'streamId', 'error')} required">
	<label for="streamId">
		<g:message code="streamingDetails.streamId.label" default="Stream Id" />
		<span class="required-indicator">*</span>
	</label>
	<g:textField name="streamId" required="" value="${streamingDetailsInstance?.streamId}" class="textwidth"/>
</div>

<div class="fieldcontain ${hasErrors(bean: streamingDetailsInstance, field: 'channelType', 'error')} required">
	<label for="channelType">
		<g:message code="streamingDetails.channelType.label" default="Channel Type" />
		<span class="required-indicator">*</span>
	</label>
	<g:select name="channelType" from="${com.comcast.rdk.ChannelType?.values()}" keys="${com.comcast.rdk.ChannelType.values()*.name()}" required="" value="${streamingDetailsInstance?.channelType?.name()}" class="selectCombo" />
</div>

<div class="fieldcontain ${hasErrors(bean: streamingDetailsInstance, field: 'audioFormat', 'error')} required">
	<label for="audioFormat">
		<g:message code="streamingDetails.audioFormat.label" default="Audio Format" />
		<span class="required-indicator">*</span>
	</label>
	<g:select name="audioFormat" from="${com.comcast.rdk.AudioFormat?.values()}" keys="${com.comcast.rdk.AudioFormat.values()*.name()}" required="" value="${streamingDetailsInstance?.audioFormat?.name()}" class="selectCombo" />
</div>

<div class="fieldcontain ${hasErrors(bean: streamingDetailsInstance, field: 'videoFormat', 'error')} required">
	<label for="videoFormat">
		<g:message code="streamingDetails.videoFormat.label" default="Video Format" />
		<span class="required-indicator">*</span>
	</label>
	<g:select name="videoFormat" from="${com.comcast.rdk.VideoFormat?.values()}" keys="${com.comcast.rdk.VideoFormat.values()*.name()}" required="" value="${streamingDetailsInstance?.videoFormat?.name()}" class="selectCombo" />
</div>
