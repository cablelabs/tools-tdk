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
<%@ page import="com.comcast.rdk.ParameterType" %>
<%@ page import="com.comcast.rdk.Module" %>
<%@ page import="com.comcast.rdk.User" %>
<%@ page import="com.comcast.rdk.Groups" %>
<%@ page import="org.apache.shiro.SecurityUtils" %>

<script type="text/javascript">	
	function onModuleChange() {
	 	var module_id = $("#moduleId").val();
		if(module_id != '') {
			$.get('getFunctions', {moduleId: module_id}, function(data) {
				var select = '<select style="width: 200px" id="function" name="function.id" ><option value="">Please Select</option>';						
				for(var index = 0; index < data.length; index ++ ) {
					select += '<option value="' + data[index].id + '">' + data[index].name + '</option>';
				}						
				select += '</select>';						
				$("#respDiv").html(''); 
				$("#respDiv").html(select); 
			});
		}				
	}		 	
</script>

<div class="fieldcontain ${hasErrors(bean: parameterTypeInstance, field: 'name', 'error')} required">
	<label for="name">
		<g:message code="parameterType.name.label" default="Parameter Name" />
		<span class="required-indicator">*</span>
	</label>
	<g:textField name="name" required="" value="${parameterTypeInstance?.name}"/>
</div>

<div class="fieldcontain ${hasErrors(bean: parameterTypeInstance, field: 'parameterTypeEnum', 'error')} required">
	<label for="parameterTypeEnum">
		<g:message code="parameterType.parameterTypeEnum.label" default="Parameter Type Enum" />
		<span class="required-indicator">*</span>
	</label>
	<g:select name="parameterTypeEnum" from="${com.comcast.rdk.ParameterTypeEnum?.values()}" keys="${com.comcast.rdk.ParameterTypeEnum.values()*.name()}" required="" value="${parameterTypeInstance?.parameterTypeEnum?.name()}"/>
</div>

<div class="fieldcontain ${hasErrors(bean: parameterTypeInstance, field: 'rangeVal', 'error')} required">
	<label for="rangeVal">
		<g:message code="parameterType.rangeVal.label" default="Range Val" />
		<span class="required-indicator">*</span>
	</label>
	<g:textField name="rangeVal" required="" value="${parameterTypeInstance?.rangeVal}"/>
</div>
<%
	def user = User.findByUsername(SecurityUtils.subject.principal)
	def group = Groups.findById(user.groupName?.id)
%>
<div class="fieldcontain ${hasErrors(bean: parameterTypeInstance, field: 'rangeVal', 'error')} required">
	<label for="function">
		<g:message code="parameterType.module.label" default="Module" />
		<span class="required-indicator">*</span>
	</label>
	<g:select noSelection="['' : 'Please Select']"  onChange="onModuleChange();" id="moduleId" name="module" from="${Module.findAllByGroupsOrGroupsIsNull(group, [order: 'asc', sort: 'name'])}" optionKey="id" required="" value="${module?.id}" class="many-to-one"/>
</div>

<div class="fieldcontain ${hasErrors(bean: parameterTypeInstance, field: 'function', 'error')} required">
	<label for="function">
		<g:message code="parameterType.function.label" default="Function" />
		<span class="required-indicator">*</span>
	</label>
	<span id="respDiv">
	<g:select id="function" name="function.id"  optionKey="id" from="" style="width: 200px"
	noSelection="['' : 'Please Select']" required="" class="many-to-one"/>
	</span>
</div>

<div class="fieldcontain ${hasErrors(bean: parameterTypeInstance, field: 'function', 'error')} required">
	<label for="function">	
	</label>
	<span class="buttons">
		<g:submitButton name="create" class="save" value="${message(code: 'default.button.create.label', default: 'Create')}" />
	</span>
</div>

