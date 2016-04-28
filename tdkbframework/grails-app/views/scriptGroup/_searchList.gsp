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
<%@ page import="com.comcast.rdk.ScriptGroup"%>
<script type="text/javascript">
	$(document).ready(function() {
		$("#scriptlisttable").dataTable({
			"sPaginationType" : "full_numbers"
		});
	});
</script>


<g:form controller="scriptGroup" >
<g:hiddenField name="category" value="${category}"/>
<g:if test="${scriptList}">
	<div id="list-script" class="content scaffold-list" role="main">
		<div id="scriplisttable">
			<g:set var="entityName"
				value="${message(code: 'script.label', default: 'ScriptList')}" />
			<h1>
				<g:message code="default.list.label" args="[entityName]" />
			</h1>
			
				<table id="scriptlisttable" class="display" style="table-layout:fixed;">
					<thead>
						<tr>
							<th width = "2%">Select</th>
							<th width = "45%">Script Name</th>
							<th>PrimitiveTest</th>
							<th width = "10%" >BoxTypes</th>
							<th width = "1%"></th>
						</tr>
					</thead>
					<tbody>
						<g:each in="${scriptList}" status="i" var="scriptListInstance">
							<tr class="${(i % 2) == 0 ? 'even' : 'odd'}">
								<g:if  test="${category == 'RDKB_TCL'}">
									<td><g:checkBox name="${scriptListInstance}"
										value="${false}" /></td>
									<td align="center" style ="width :20% ; word-wrap:break-word; " ><g:link id="tcl@${scriptListInstance}"
											onclick="editTclScript('${scriptListInstance}');return false;">
											${scriptListInstance}
										</g:link></td>
										
									<td align="center" style ="width :20% ; word-wrap:break-word; ">
										${scriptListInstance}
									</td>
									<td></td>
									<td>
										<g:link action="exportScriptContent" id="${scriptListInstance}" params="[category:category]"><img src="../images/script-py.png" title=" Download Script" /></g:link>
									</td>
								</g:if>
								<g:else>
									<td><g:checkBox name="${scriptListInstance?.name}"
										value="${false}" /></td>
									<td align="center" style ="width :20% ; word-wrap:break-word; " ><g:link id="${scriptListInstance?.primitiveTest?.module?.name}@${scriptListInstance?.name}"
											onclick="showScript('${scriptListInstance?.primitiveTest?.module?.name}@${scriptListInstance?.name}','${category }');return false;">
											${scriptListInstance?.name}
										</g:link></td>
									<td align="center" style ="width :20% ; word-wrap:break-word; ">
										${scriptListInstance?.primitiveTest?.name}
									</td>
									<td>
										${scriptListInstance?.boxTypes}
									</td>
									<td>
										<g:link action="exportScriptContent" id="${scriptListInstance?.name}" params="[category:category]"><img src="../images/script-py.png" title=" Download Script" /></g:link>
									</td>
								</g:else>

								<%--<td>
									<g:if  test="${category != 'RDKB_TCL'}">
										${scriptListInstance?.boxTypes}
									</g:if>
								</td>
								--%><%--<td>
									<g:if  test="${category == 'RDKB_TCL'}">
										<g:link action="exportScriptContent" id="${scriptListInstance}" params="[category:category]"><img src="../images/script-py.png" title=" Download Script" /></g:link>
									</g:if>
									<g:else>
										<g:link action="exportScriptContent" id="${scriptListInstance?.name}" params="[category:category]"><img src="../images/script-py.png" title=" Download Script" /></g:link>
									</g:else>
								</td>
							--%></tr>
						</g:each>
					</tbody>
				</table>
		</div>		
	</div>	
	</g:if>	
	<g:else>
		<center>No list to display</center>
	</g:else>
	<br><br><br><br>
	<g:if test="${scriptList}">
	<div>	
		<table style="width:100%;">
		<tr>
			<td nowrap>Add selected scripts to &emsp;
			<input onclick="showExistingSuite();" type="radio" name="suiteRadioGroup" checked="checked" value="Existing" />Existing Suite 
			&emsp;<input onclick="showNewSuite();" type="radio" name="suiteRadioGroup" value="New" />New Suite	
			</td>
		
			<td><g:select name="testsuite" id="existingSuiteId" style="width: 250px;" from="${com.comcast.rdk.ScriptGroup.findAllByCategory(category)}" 
			optionKey="id" required="" value="" 
			class="many-to-one selectCombo" />
			<g:textField style="display:none;width: 239px;" id="newSuiteId" name="newSuiteName" value="" />
			</td>
			<td>
			<span class="buttons"><g:actionSubmit action="addScriptGroupfromSeachList" class="save" name="addScriptGrp" value="ADD" />
			</span>
			</td>
			<td>			
			</td>
		</tr>
		</table>	
	</div>
	</g:if>
</g:form>