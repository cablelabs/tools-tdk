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

<g:form action="save" controller="primitiveTest" method="post">
	<input type="hidden" name="parameterTypeIds" id="parameterTypeIds">
	<table>
		<tr>
			<th colspan="2" align="center">Create New Primitive Test</th>
		</tr>
		<tr>
			<td>Test Name</td>
			<td>
				<input type="text" name="testName" id="testName" size="37" maxlength="150">
			</td>
		</tr>
		<tr>
			<td>Select Module</td>
			<td>
				<g:select from="${moduleInstanceList}" var="module" noSelection="['' : 'Please Select']" id="module"
					name="module" style="width: 250px" optionKey="id"/>
			</td>
		</tr>
		<tr>
			<td>Select Function</td>
			<td id="functionTd">
				<select style="width: 250px">
					<option value="">Please Select</option>
				</select>
			</td>
		</tr> 
		<tr id="tableheader" style="display: none;">
			<td colspan="2" align="center">
				<table id="parameterTable">
					<tr>
						<th>Parameter Name</th>
						<th>Type</th>
						<th>Range</th>
						<th>Value</th>
					</tr>
				</table>
			</td>
		</tr>
		<tr id="buttons" style="display: none;">
			<td colspan="2" align="center">
			<span id="save">
					<g:submitToRemote action="save" controller="primitiveTest" update="testMessageDiv" 
						value="Save" before= "isTestExist(document.getElementById('testName').value);" 
						onSuccess = "updateTestList(document.getElementById('testName').value);" >
					</g:submitToRemote>	
			</span>&emsp;
			<input type="reset" value="Reset" id="cancel">				
			</td>
		</tr>
	</table>
</g:form>

