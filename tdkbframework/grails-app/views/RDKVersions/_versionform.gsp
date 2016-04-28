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

<%@ page import="com.comcast.rdk.RDKVersions" %>

<div class="fieldcontain ${hasErrors(bean: rdkVersionsInstance, field: 'buildVersion', 'error')} required">
	<label for="buildVersion">
		<g:message code="rdkVersions.buildVersion.label" default="Build Version" />
		<span class="required-indicator">*</span>
	</label>
	<g:textField  id="buildVersion" name="buildVersion" required="" value="${rdkVersionsInstance?.buildVersion}"/>
	<%--<g:textField name="type" required="" value="${rdkVersionsInstance?.type}"/>--%>
</div>