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
<%@ page import="com.comcast.rdk.PrimitiveTest"%>
<%@ page import="com.comcast.rdk.Module"%>
<%@ page import="com.comcast.rdk.ParameterType"%>

<g:form action="update" controller="primitiveTest" method="post">
	<g:set var="ids" value="${paramTypes?.id?.toString()}"/>
	<%--<g:set var="ids" value="${primitiveTest.parameters?.parameterType?.id?.toString()}"/>--%>
	<input type="hidden" name="parameterTypeIds" id="parameterTypeIds" value="${ids?.substring(1, ids?.lastIndexOf(']'))}">
	<input type="hidden" name="id" id="id" value="${primitiveTest?.name}">
	<input type="hidden" name="ptVersion" id="ptVersion" value="${primitiveTest?.version}">
	<input type="hidden" name="functionValue" id="functionValue" value="${primitiveTest?.function?.id}">
	
	<table>
		<tr>
			<th colspan="2" align="center">Edit Primitive Test</th>
		</tr>
		<tr>
			<td>Test Name</td>
			<td>
				<input type="text" name="testName" id="testName" size="37" maxlength="150" value="${primitiveTest.name}" disabled="true">
			</td>
		</tr>
		<tr>
			<td>Select Module</td>
			<td>
				<input type="text" name="module" id="module" size="37" maxlength="150" value="${primitiveTest.module?.name}" disabled="true">
				<%--<g:select from="${Module.list([order: 'asc', sort: 'name'])}" id="module"
					name="module" style="width: 250px" optionKey="id" value="${primitiveTest.module?.id}"/>
			--%>
			</td>
		</tr>
		<tr>
			<td>Select Function</td>
			<td id="functionTd">
				<input type="text" name="functionValue" id="functionValue" size="37" maxlength="150" 
						value="${primitiveTest?.function?.name}" disabled="true">
				<%--<select name="functionValue" id="functionValue" style="width: 250px" onchange="getAssociatedParameters()">
					<g:each in="${functions}" var="function">
						<g:if test="${function.id == primitiveTest.function.id}">
							<option value="${function.id}" selected="selected">${function.name}</option>
						</g:if>
						<g:else>
							<option value="${function.id}">${function.name}</option>
						</g:else>
					</g:each>
				</select>--%>
			</td>
		</tr>
		<tr>
			<td colspan="2" align="center">
				<table id="parameterTable">
					<tr>
						<th>Parameter Name</th>
						<th>Type</th>
						<th>Range</th>
						<th>Value</th>
					</tr>
					<g:each in="${primitiveTest.parameters}" var="parameter">
						<tr>
							<td align="left">&emsp;&emsp;${parameter.parameterType.name}</td>
							<td>${parameter.parameterType.parameterTypeEnum}</td>
							<td>${parameter.parameterType.rangeVal}</td>
							<td align="center">
								<input type="text" name="value_${parameter.parameterType.id}" value="${parameter.value}">
							</td>
						</tr>
					</g:each>
					<g:each in="${newParams}" var="newparam">
						<tr>
							<td align="left">&emsp;&emsp;${newparam.name}</td>
							<td>${newparam.parameterTypeEnum}</td>
							<td>${newparam.rangeVal}</td>
							<td align="center">
								<input type="text" name="value_${newparam.id}" value="">
							</td>
						</tr>
					</g:each>
				</table>
			</td>
		</tr>
		<tr id="buttons">
			<td colspan="2" align="center">
				<input type="submit" value="Update" id="save">&emsp;
				<input type="reset" value="Cancel" id="cancel" onclick="makeTestEditable('${primitiveTest?.name}')">
			</td>
		</tr>
	</table>
</g:form>

