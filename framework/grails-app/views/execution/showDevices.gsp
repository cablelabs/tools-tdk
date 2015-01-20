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
<%@ page import="com.comcast.rdk.Device"%>
<%@ page import="com.comcast.rdk.DeviceGroup"%>

<script type="text/javascript">
$(document).ready(function() {
	$("#scripts").select2();	
	$("#devices").select2();	
});

</script>


<g:form  method="post">
	<input type="hidden" name="id" id="id" value="${device?.id}">
	<g:hiddenField name="stbname" id="stbname" value="${device?.stbName}" />
	<g:hiddenField name="exId" id="exId" value="${device?.id}" />	
	<table>
		<tr>
			<th colspan="2" align="center">Execute script on ${device?.stbName}</th>
		</tr>
		<tr>
			<td>Execution Name</td>
			<td style="vertical-align: middle;">
				<span id="defExcName">
					<g:textField readonly="true" id="defexecName" name="name" required="" value="${device?.stbName}-${datetime}" class="textwidth"/>
					<a href="#"><img style="vertical-align: middle;" src="../images/edit.png" onclick="showEditableExecName();" /></a>
				</span>
				<span id="givenExcName" style="display:none;">
					<g:textField id="newexecName" name="execName" required="" value="${device?.stbName}-${datetime}" class="textwidth"/>
					<a href="#"><img style="vertical-align: middle;" src="../images/undo.png" onclick="showDefaultExecName();"/></a>					
				</span>		
				<a href="#"><img style="vertical-align: middle;" src="../images/refresh.gif" onclick="showDateTime();"/></a>				
			</td>		
		</tr>
		<tr>
			<td style="vertical-align: middle;">Device</td>
			<td style="vertical-align: middle;">
				<select id="devices" name="devices" multiple="true" id="functionValue" onchange="showDateTime();" style="height:200px;width:400px" class="many-to-one selectCombo">
					<g:each in="${Device?.list()}" var="deviceInstance">
						<g:if test="${deviceInstance.id == device.id}">
							<option value="${deviceInstance.id}" selected="selected">${deviceInstance.stbName}</option>
						</g:if>
						<g:else>
							<option value="${deviceInstance.id}">${deviceInstance.stbName}</option>
						</g:else>
					</g:each>
				</select>
			</td>		
		</tr>
		<tr>
			<td>Select Type</td>
			<td>
				<input onclick="showSuite();" id="testSuiteRadio" type="radio" name="myGroup" value="TestSuite" />TestSuite 
				&emsp;<input onclick="showSingle();" id="singleTestRadio" type="radio" name="myGroup" checked="checked" value="SingleScript" />SingleScript	
			</td>		
		</tr>	
		<tr>
			<td>Select Script</td>
			<td>				
				<div id="testSuite" style="display: none;">
				<g:select id="scriptGrp" onchange="showDateTime();" name="scriptGrp" noSelection="['' : 'Please Select']" from="${scriptGrpList}" optionKey="id" required="" value="" class="many-to-one selectCombo"/>
				</div>
				<div id="singletest" >
				<g:select id="scripts" multiple="true" style="height:200px;width:400px" onchange="showDateTime();" name="scripts"  from="${scriptList}" value="" class="many-to-one selectCombo"/>
				</div>							
			</td>						
		</tr>	
		<tr>
			<td>Repeat Test</td>
			<td>				
				<%--<g:textField size="5" onkeypress="return digitonly(event);" id="repeatId" name="repeatNo" required="" value="1" />&nbsp; times (Not Applicable for scheduling)
				--%>
				<input size="5" id="repeatId" onkeypress="return isNumberKey(event)" type="text" name="repeatNo" required="" value="1">&nbsp; times		
				&emsp;&emsp;<g:checkBox id="rerunId" name="rerun" checked="false" />&nbsp;Re-Run on Failure										
			</td>						
		</tr>
		<tr>
			<td>Execution Options</td>
			<td><g:checkBox id="benchmarkId" name="benchMarking" checked="false" />&nbsp;Timing Info 
			&emsp;&emsp;<g:checkBox id="systemDiagId" name="systemDiagnostics" checked="false"  />&nbsp;Performance Data
			</td>
		</tr>	
		<tr>
			<td colspan="2" align="center">				
				<g:hiddenField name="pageFlag" value="execute"/>
				<span id="executeBtn" class="buttons"><g:submitToRemote class="save" before="showWaitSpinner();" 
				action="executeScriptMethod" controller="execution" update="resultDiv${device?.id}" value="Execute" 
				onComplete="completed(${device?.id})" onFailure="changeStyles()"  onSuccess="changeStyles()" >
				</g:submitToRemote>&emsp;	
				</span>
				<span id="scheduleBtn" class="buttons">
					<input type=button class="save"  onclick="showScheduler(${device?.id});return false;"
					value="Schedule" />	
				</span>
				<div id="popup" style="display: none;">
			              Please wait.....<img id="s" src="${resource(dir:'images',file:'spinner.gif')}" />
			    </div>				
			</td>
		</tr>		
		<tr>		
			<td>Execution Result</td>					
			<td style="width:80%;">
				<div id="resultDiv${device?.id}" style="border-color: #FFAAAA;border-style: solid;
					border-width: 1px;width: 550px;height:215px;overflow:auto;" >
					
				</div>
				<div id="dynamicResultDiv" style="display: none;border-color: #FFAAAA;border-style: solid;
					border-width: 1px;width: 550px;height:215px;overflow:auto;" >
					
				</div>
		 	</td>
		</tr>						
	</table>
</g:form>
<div id="scheduleJobPopup" style="display: none; overflow: auto; width : 98%; height : 98%;">	
</div>




