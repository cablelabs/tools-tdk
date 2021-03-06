<!--
 If not stated otherwise in this file or this component's Licenses.txt file the
 following copyright and licenses apply:

 Copyright 2016 RDK Management

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

 http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
-->
<%@ page import="com.comcast.rdk.ScriptGroup" %>

<div class="fieldcontain ${hasErrors(bean: scriptGroupInstance, field: 'name', 'error')} required">
	<label for="name">
		<g:message code="scriptGroup.name.label" default="Name" />
		<span class="required-indicator">*</span>
	</label>
	<g:textField name="name" required="" value="${scriptGroupInstance?.name}" style="width: 240px"/>
</div>

<div class="fieldcontain ${hasErrors(bean: scriptGroupInstance, field: 'scriptList', 'error')} ">
	<label for="scripts">
		<g:message code="scriptGroup.scripts.label" default="Scripts" />		
	</label>
	<g:select name="scripts" from="${com.comcast.rdk.Script.list()}" multiple="multiple" optionKey="id" style="width: 250px;height:350px;" size="5" value="${scriptGroupInstance?.scriptList*.id}" class="many-to-many"/>
</div>

