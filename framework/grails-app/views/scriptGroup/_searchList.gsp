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
--><%@ page import="com.comcast.rdk.Script"%>
<%@ page import="com.comcast.rdk.ScriptGroup"%>
<script type="text/javascript">
	$(document).ready(function() {
		$("#scriptlisttable").dataTable({
			"sPaginationType" : "full_numbers"
		});
	});
</script>
<g:form controller="scriptGroup" >
<g:if test="${scriptList}">
	<div id="list-script" class="content scaffold-list" role="main">
		<div id="scriplisttable">
			<g:set var="entityName"
				value="${message(code: 'script.label', default: 'ScriptList')}" />
			<h1>
				<g:message code="default.list.label" args="[entityName]" />
			</h1>
			
				<table id="scriptlisttable" class="display">
					<thead>
						<tr>
							<th>Select</th>
							<th>Script Name</th>
							<th>PrimitiveTest</th>
							<th>BoxTypes</th>
						</tr>
					</thead>
					<tbody>
						<g:each in="${scriptList}" status="i" var="scriptListInstance">
							<tr class="${(i % 2) == 0 ? 'even' : 'odd'}">
								<td><g:checkBox name="${scriptListInstance?.id}"
										value="${false}" /></td>
								<td><g:link id="${scriptListInstance?.id}"
										onclick="showScript('${scriptListInstance?.id}','STATIC');return false;">
										${fieldValue(bean: scriptListInstance, field: "name")}
									</g:link></td>

								<td>
									${fieldValue(bean: scriptListInstance, field: "primitiveTest")}
								</td>

								<td>
									${fieldValue(bean: scriptListInstance, field: "boxTypes")}
								</td>
							</tr>
						</g:each>
					</tbody>
				</table>
		</div>		
	</div>	
	</g:if>	
	<br><br><br><br>
	<g:if test="${scriptList}">
	<div>	
		<table style="width:100%;">
		<tr>
			<td nowrap>Add selected scripts to &emsp;
			<input onclick="showExistingSuite();" type="radio" name="suiteRadioGroup" checked="checked" value="Existing" />Existing Suite 
			&emsp;<input onclick="showNewSuite();" type="radio" name="suiteRadioGroup" value="New" />New Suite	
			</td>
		
			<td><g:select name="testsuite" id="existingSuiteId" style="width: 250px;" from="${com.comcast.rdk.ScriptGroup.list()}" 
			optionKey="id" required="" value="" 
			class="many-to-one selectCombo" />
			<g:textField style="display:none;width: 239px;" id="newSuiteId" name="newSuiteName" value="" />
			</td>
			<td>
			<span class="buttons"><g:actionSubmit action="addScriptGroup" class="save" name="addScriptGrp" value="ADD" />
			</span>
			</td>
			<td>			
			</td>
		</tr>
		</table>	
	</div>
	</g:if>
</g:form>