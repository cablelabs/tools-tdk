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
<g:form action="saveScript" method="post">
	<table>

		<tr>
			<th colspan="4" align="center">Create New Script</th>
		</tr>

		<tr>
			<td>Script Name</td>
			<td><input type="text" name="name" id="name" size="37"
				maxlength="150"> &emsp;&emsp;&emsp;&emsp; <a href=""
				onclick="showStreamDetails();return false;">Show Stream Details</a></td>
		</tr>

		<tr>
			<td>Primitive Test</td>
			<td><select name="ptest" id="ptest" style="width: 250px">
					<option value="default">--Please Select--</option>
					<g:each in="${primitiveTestList}" var="primList">
						<option value="${primList.id}">
							${primList.name}
						</option>
					</g:each>
			</select>&emsp;&emsp;&emsp;&emsp; <span id="linkId"></span></td>
		</tr>
				
		<tr>
			<td>Box Type</td>
			<td>
			<g:select id="boxTypes" name="boxTypes"  from="${com.comcast.rdk.BoxType.list()}" optionKey="id" required="" value="${deviceInstance?.boxType?.id}" class="many-to-one selectCombo" multiple="true"/>
			&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;Execution TimeOut &emsp;
			<input type="text" id="execTime" name="executionTime" size="5"/>(min)
			</td>
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
			<td colspan="2" align="center">
					<span id="saveScript" >
						<g:submitToRemote action="saveScript" controller="scriptGroup" update="scriptMessageDiv" 
							value="Save"  before= "isScriptExist(document.getElementById('name').value);" 
							onSuccess = "updateScriptList(document.getElementById('name').value);" >
						</g:submitToRemote>	
					</span>
				 <input type="reset" value="Reset" id="cancel" onclick="clearScriptArea();"/>&emsp;
			</td>
		</tr>

	</table>

</g:form>

