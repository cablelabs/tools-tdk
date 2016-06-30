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
<%@ page import="org.apache.shiro.SecurityUtils"%>
<%@ page import="com.comcast.rdk.User" %>

<script>
var needToConfirm = false;

window.onbeforeunload = confirmExit;

function confirmExit()
{
  if (needToConfirm){
	checkAnyEditingScripts();
    return "If you navigate away from this page, any unsaved changes will be lost !!!";
  }
}


function checkAnyEditingScripts(){
	var scriptName = $("#scriptName").val();
	if(scriptName && scriptName != "undefined"){
		clearLocks(scriptName);
	}
}

function clearLocks(scriptName){
	$.get('removeEditLock', {scriptName: scriptName}, function(data) {
	});
}

</script>


<g:if test="${script && category != 'RDKB_TCL' }" >
<g:form name="editScriptForm" action="updateScript" controller="scriptGroup" method="post">
	<input type="hidden" name="id" id="id" value="${script?.primitiveTest?.module?.name?.trim()}@${script.name}">
	<input type="hidden" name="scriptVersion" id="scriptVersion" value="${script.version}">
	<input type="hidden" name="prevScriptName" id ="prevScriptName" value="${script.name}">
	<input type="hidden" name="scriptName" id ="scriptName" value="">
	<g:hiddenField name="category" value="${script?.category}"/>
	<table>
		<tr>
			<th colspan="4" align="center">Edit Script</th>
		</tr>
		<tr>
			<td style="width:15%;">Script Name</td>
			<td>
				<input type="text" name="name" id="name" size="37" maxlength="150" value="${script.name}">			
				&emsp;&emsp;&emsp;&emsp;
				<g:if test="${script?.category != 'RDKB'}">
					<a href="" onclick="showStreamDetails();return false;">Show Stream Details</a>
				</g:if>
			</td>
		</tr>
		<tr>

		<tr>
			<td style="width:15%;">Primitive Test</td>
			<td><select name="ptest" id="ptest" style="width: 250px"><%--
					<option value="default">--Please Select--</option>
					--%>
						<option value="${script.primitiveTest.name}">
							${script.primitiveTest.name}
						</option>
				
			</select>&emsp;&emsp;&emsp;&emsp;		
			
			<g:if test="${script?.primitiveTest?.module?.testGroup.toString() != "OpenSource"  }"  >
				<a href="JavaScript:newPopup('../htmls/${script?.primitiveTest?.module?.name.trim()}.html#${script.name}');">View&nbsp;${script?.primitiveTest?.module?.name}&nbsp;Testcase</a>
			</g:if>						
			</td>
		</tr>
		
		<tr>
			<td>Box Type</td>
			<td>
				<g:select id="boxTypes" name="boxTypes"  from="${com.comcast.rdk.BoxType.findAllByCategory(script.category)}" optionKey="id" required="" value="${script.boxTypes}" class="many-to-one selectCombo" multiple="true"/>
				 &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;Execution TimeOut &emsp;
				<input type="text" id="execTime" name="executionTime" size="5" value="${script.executionTime}" />(min)
			</td>
		</tr>

		<tr>
			<td>RDK Version</td>
			<td>
				<g:select id="rdkVersions" name="rdkVersions"  from="${com.comcast.rdk.RDKVersions.findAllByCategory(script.category)}" optionKey="id" required="" value="${script.rdkVersions}" class="many-to-one selectCombo" multiple="true"/>
				 &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;Tags&emsp;&emsp; 
				<g:select id="scriptTags" name="scriptTags"  from="${com.comcast.rdk.ScriptTag.list()}" optionKey="id" value="${script?.scriptTags}" class="many-to-one selectCombo" multiple="true"/>
			
			</td>
		</tr>

		<tr>
			<td></td>
			<td><g:checkBox id="longDuration" name="longDuration" checked="${script.longDuration}" title ="long duration test will be included only in default module/Box type test suites with name ending with LD" />&nbsp;Long duration test</td>
		</tr>
		
		<tr>
			<td></td>
			<td><g:checkBox id="skipStatus" name="skipStatus" checked="${script.skip}"  onclick="showSkipRemarks(this)" />&nbsp;Skip
					Execution</td>
		</tr>
		
		
		<g:if test="${script.skip}" >	
		<tr >
			<td style="width: 15%;">
			
			<span id="skipReason123">Reason For Skipping</span></td>
			<td><span id="skipRemarks123"><g:textArea name="remarks" style="width:465px;height:20px;"
						value="${script.remarks}">
				</g:textArea></span>
				
				</td>
		</tr>
		</g:if>
		<g:else>
			<tr >
			<td style="width: 15%;">
			
			<span id="skipReason123" style="display: none">Reason For Skipping</span></td>
			<td><span id="skipRemarks123" tyle="display: none"><g:textArea name="remarks" style="width:465px;height:20px; display: none"
						value="${script.remarks}">
				</g:textArea></span>
				
				</td>
		</tr>
		</g:else>
		
		
		<tr>
			<td style="width:15%;">Synopsis</td>
			<td>
				<g:textArea  name="synopsis" style="width:465px;height:40px;" value="${script.synopsis}" >
                </g:textArea>               
			</td>
		</tr>
		
		<tr>
			<td style="width:15%;">Script Content</td>
			
			<td style="width:80%;">		
				 <g:textArea id="scriptArea" name="scriptArea" class="scriptArea" style="color:RGB(130,15,15);font-size:12px">${script.scriptContent}</g:textArea>
			</td>		
		</tr>
		<tr>
		<td></td>
		<td>
		<label id="warningMsg" style="color: red;"></label>
		</td>
		</tr>
		<tr id="buttons">
			<td colspan="2" align="center">
				<g:if test="${SecurityUtils.getSubject().hasRole('ADMIN')}" >
				<g:if test="${flag != 'STATIC'}" >	
					<div id = "editDiv">
						<input id ="editButton" class= "editscriptbutton" type="button" onclick="needToConfirm= true;enableEdit(this,'${script.name}','${SecurityUtils.getSubject().getSession(false)}')" value="Edit Script">
					</div>
					<div id ="updateDiv">						
						<input type="submit" class= "updatebutton"   style="display: none"  onclick="needToConfirm= false;" value="Update" id="save"> 
						 <input type="reset"  class="deletebutton" style="display: none" value="Cancel" id="cancel" onclick="makeScriptEditable('${script.name}')">		
					</div>		
				</g:if>
				</g:if>
			</td>
		</tr>
	</table>
</g:form>
<g:if test="${SecurityUtils.getSubject().hasRole('ADMIN')}" >
<g:form name="downloadScriptForm" action="exportScriptContent" controller="scriptGroup" method="post">
		<g:hiddenField name="category" value="${script?.category}"/>
		<input type="hidden" name="id" id="id" value="${script?.name}">
		<table>
		<tr></tr>
			<tr>
				<td style="width: 15%;"></td>
				<td style="width: 80%;">
				<span class="buttons"> <input class= "download" type="submit"
					value="Download Script" id="download"> </span></td>
			</tr>
		</table>
	</g:form>
</g:if>
</g:if>
<!-- Only display for tcl scripts, is not editable -->
<g:if test="${script && category == 'RDKB_TCL' }">
	<!--<g:if test="${category == 'RDKB_TCL' }"> -->
		<%--<table>
			<tr>
				<th colspan="4" align="center">Edit Script</th>
			</tr>
			<tr>
				<td>Script Name</td>
				<td>
					${scriptName }
				</td>
			</tr>
			<tr>
				<td>Content</td>
				<td>
				<g:textArea id="tclText" name="tcl" value="${script}" style="height:250px;width:700px;" disabled="true"></g:textArea></td>
			</tr>
			<tr>
				<td colspan="2" align="center" style="padding: 20px;"><g:if
						test="${SecurityUtils.getSubject().hasRole('ADMIN')}">
						<div id = "editDivTcl">
							<input id ="editButtonTcl" class= "editscriptbutton" type="button" onclick="needToConfirm= true;enableEditTcl('${scriptName}')" value="Edit Script">
						</div>
						<div id ="updateDivTcl">			
							<input type="button" id="saveTcl" class= "updatebutton"   style="display: none"  onclick="updateTclContents('${scriptName}')" value="Update" > 
							 <input type="reset" id="cancelTcl" class="deletebutton" style="display: none" value="Cancel"  onclick="cancelTclEdit('${scriptName}')">		
						</div>
						<div style="padding-top:30px;">	
						<g:form action="exportTCL" controller="scriptGroup">
							<g:hiddenField name="scriptName" value="${ scriptName}" />
							<span class="buttons"> <input class="download"
								type="submit" value="Download Script" id="">
							</span>
						</g:form>
						</div>
					</g:if></td>
			</tr>
		</table>
--%><!-- </g:if>  -->	


<g:form action="saveTcl" method="post">
<g:hiddenField name="scriptName" value="${scriptName}"/> 
<table> 
			<tr>
				<th colspan="4" align="center">Edit Script</th>
			</tr>
			<tr>
				<td>Script Name</td>
				<td>
					${scriptName }
				</td>
			</tr>
			<tr>
				<td>Content</td>
				<td>
				<g:textArea id="tclText" name="tclText" value="${script}" style="height:250px;width:700px;" disabled="true"></g:textArea></td>
			</tr>
			<tr>
				<td colspan="2" align="center" style="padding: 20px;"><g:if
						test="${SecurityUtils.getSubject().hasRole('ADMIN')}">
						<div id = "editDivTcl">
							<input id ="editButtonTcl" class= "editscriptbutton" type="button" onclick="needToConfirm= true;enableEditTcl('${scriptName}')" value="Edit Script">
						</div>
						<div id ="updateDivTcl">			
							<input type="submit" id="saveTcl" class= "updatebutton"   style="display: none"  value="Update"  onclick="needToConfirm= true;confirmExit();"> 
							 <input type="reset" id="cancelTcl" class="deletebutton" style="display: none" value="Cancel"  onclick="cancelTclEdit('${scriptName}')">		
						</div>
					</g:if></td>
			</tr>
		</table>


</g:form>

<div style="padding-top:20px;padding-left: 15%;">	

<g:form action="exportTCL" controller="scriptGroup">
							<g:hiddenField name="scriptName" value="${ scriptName}" />
							<span class="buttons"> <input class="download"
								type="submit" value="Download Script" id="">
							</span>
						</g:form>
						
</div>

</g:if>
