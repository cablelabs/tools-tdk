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
<%@ page import="com.comcast.rdk.Script"%>
<%@ page import="org.apache.shiro.SecurityUtils"%>
<%@ page import="com.comcast.rdk.User" %>

<script type="text/javascript">
	var scripttextarea = document.getElementById('scriptArea');
	var scrname = document.getElementById('name');
	var ptestdropdown = document.getElementById('ptest');

	ptestdropdown.onchange = function() {
		var primitiveTestName = (this.options[this.selectedIndex].innerHTML).trim();
		$.get('getModuleName', {primId: this.value}, function(data) {
			if (this.selectedIndex != 0) {
				scripttextarea.innerHTML = 
					"# use tdklib library,which provides a wrapper for tdk testcase script \r\nimport tdklib; \r\n\r\n#Test component to be tested\r\nobj = tdklib.TDKScriptingLibrary(\""
					+ data[0].toLowerCase() + "\",\"" + data[1]
					+ "\");\r\n\r\n#IP and Port of box, No need to change,\r\n#This will be replaced with correspoing Box Ip and port while executing script\r\nip = <ipaddress>\r\nport = <port>\r\nobj.configureTestCase(ip,port,\'"					
					+ scrname.value
					+ "');\r\n\r\n#Get the result of connection with test component and STB\r\nresult =obj.getLoadModuleResult();\r\nprint \"[LIB LOAD STATUS]  :  %s\" %result;\r\n"	
					+ "\r\n#Prmitive test case which associated to this Script\r\ntdkTestObj = obj.createTestStep('"
					+ primitiveTestName
					+ "');\r\n\r\n#Execute the test case in STB\r\ntdkTestObj.executeTestCase("+ "\"\""+");\r\n\r\n#Get the result of execution\r\nresult = tdkTestObj.getResult();\r\nprint \"[TEST EXECUTION RESULT] : %s\" %result;\r\n"
					+ "\r\n#Set the result status of execution\r\ntdkTestObj.setResultStatus(\"none\");\r\n"

					+ "\r\nobj.unloadModule(\""+data[0].toLowerCase() +"\");";					
				if(data[2] != "OpenSource"){
					link = "<a href=\"JavaScript:newPopup('../htmls/"+data[0]+".html');\">View&nbsp;"+data[0]+"&nbsp;Testcase</a>";
					$("#linkId").html(link); 
				}
				else{
					$("#linkId").html(''); 
				}
				document.getElementById("execTime").value=data[3]
				document.getElementById("scriptArea").value = scripttextarea.innerHTML.html_entity_decode();
			}
		});				
	}

</script>


<div id="scriptMessageDiv" class="message" style="display: none;"></div>
<div id="scriptTclMessageDiv" class="message" style="display: none;"></div>

<g:if test="${ category == 'RDKV' || category == 'RDKB'   }">
<g:form action="saveScript" method="post">
	<g:hiddenField name="category" value="${category}"/>
	<table>

		<tr>
			<th colspan="4" align="center">Create New Script</th>
		</tr>

		<tr>
			<td>Script Name</td>		 
			<td><input type="text" name="name" id="name" size="37"
				maxlength="150"> &emsp;&emsp;&emsp;&emsp;  <g:if test="${category == "RDKV"}">
				<a href=""
				onclick="showStreamDetails();return false;">Show Stream Details</a>
				</g:if></td>
		</tr>

		<tr>
			<td>Primitive Test</td>
			<td><select name="ptest" id="ptest" style="width: 250px" >
					<option value="default">--Please Select--</option>
					<g:each in="${primitiveTestList}" var="primList">
						<option value="${primList}">
							${primList}
						</option>
					</g:each>
			</select>&emsp;&emsp;&emsp;&emsp; <span id="linkId"></span></td>
		</tr>
				
		<tr>
			<td>Box Type</td>
			<td>
			<g:select id="boxTypes" name="boxTypes"  from="${com.comcast.rdk.BoxType.findAllByCategory(category)}" optionKey="id" required="" value="${deviceInstance?.boxType?.id}" class="many-to-one selectCombo" multiple="true"/>
			&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;Execution TimeOut &emsp;
			<input type="text" id="execTime" name="executionTime" size="5"/>(min)
			</td>
		</tr>
		
		<tr>
			<td>RDK Version</td>
			<td>
				<g:select id="rdkVersions" name="rdkVersions"  from="${com.comcast.rdk.RDKVersions.findAllByCategory(category)}" optionKey="id" required="" value="" class="many-to-one selectCombo" multiple="true"/>
			 &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;Tags&emsp;&emsp; 
				<g:select id="scriptTags" name="scriptTags"  from="${com.comcast.rdk.ScriptTag.findAllByCategory(category)}" optionKey="id" value="" class="many-to-one selectCombo" multiple="true"/>
			
			</td>
		</tr>
		<tr>
			<td></td>
			<td><g:checkBox id="longDuration" name="longDuration" checked="false" title ="long duration test will be included only in default module/Box type test suites with name ending with LD" />&nbsp;Long duration test</td>
		</tr>
		<tr>
			<td></td>
			<td><g:checkBox name="skipStatus" checked="false" onclick="showSkipRemarks(this)" />&nbsp;Skip
				Execution</td>
		</tr>
		<tr>
			<td style="width: 15%;"><span id="skipReason" style="display:none;">Reason For Skipping</span></td>
			<td><span id="skipRemarks" style="display:none;" style="display:none;"><g:textArea name="remarks" style="width:465px;height:20px;"
					value="">
				</g:textArea></span></td>
		</tr>

		<tr>
			<td>Synopsis</td>
			<td><g:textArea name="synopsis" style="width:465px;height:40px;">
				</g:textArea></td>
		</tr>

		<tr>
			<td>Script Content</td>
			<td><g:textArea id="scriptArea" name="scriptArea" 
					class="scriptArea" style="color:RGB(130,15,15);font-size:12px">
				</g:textArea></td>
		</tr>

		<tr id="buttons">
			<g:if test="${SecurityUtils.getSubject().hasRole('ADMIN')}" >
			<td colspan="2" align="center">
					<span id="saveScript" >
						<g:submitToRemote action="saveScript" controller="scriptGroup" update="scriptMessageDiv" 
							value="Save"  before= "isScriptExist(document.getElementById('name').value);" 
							onSuccess = "updateScriptListWithScriptName(document.getElementById('name').value);" >
						</g:submitToRemote>	
					</span>
				 <input type="reset" value="Reset" id="cancel" onclick="clearScriptArea();"/>&emsp;
			</td>
			</g:if>
		</tr>

	</table>
</g:form>
</g:if>
<g:if test="${ category == 'RDKB_TCL' }">
	<g:form action="saveTclScript" method="post">
		<g:hiddenField name="category" value="${category}" />
		<table>
			<tr>
				<th colspan="4" align="center">Add New TCL Script</th>
			</tr>
			<tr>
				<td>Script Name</td>
				<td><input type="text" name="name" id="name" size="37"
					maxlength="150"></td>
			</tr>
			<tr>
				<td>Content</td>
				<td><g:textArea id="scriptArea" name="scriptArea"
						class="scriptArea" style="color:RGB(130,15,15);font-size:12px">
					</g:textArea></td>
			</tr>
			<tr>
			<tr id="buttons">
				<g:if test="${SecurityUtils.getSubject().hasRole('ADMIN')}">
					<td colspan="2" align="center">
					<div id="saveTclScript">	
						<input type="submit" id="saveTclScript" class= "updatebutton"   style="display: true"  value="save" onclick="needToConfirm= false;" > 
					<%--	<span id="saveTclScript"><g:submitToRemote  controller="scriptGroup"
								action="saveTclScript" controller="scriptGroup"
								update="scriptTclMessageDiv" value="Save">
							</g:submitToRemote>
					
					<g:submitToRemote  controller="scriptGroup"
								 controller="scriptGroup"
								update="scriptMessageDiv" value="Save"	before=	"isTclScriptExist(document.getElementById('name').value);" 						
								onSuccess="updateTclScriptListWithScriptName(document.getElementById('name').value);">
							</g:submitToRemote>
								</span> --%>					
					<input type="reset" value="Reset" id="cancel" class="deletebutton" 
						onclick="clearScriptArea();" />&emsp;</td>
						</div>
				</g:if>
			</tr>
		</table>
	</g:form>
</g:if>

