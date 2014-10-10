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

<g:if test="${script}" >
<g:form name="editScriptForm" action="updateScript" controller="scriptGroup" method="post">
	<input type="hidden" name="id" id="id" value="${script.id}">
	
	<table>
		<tr>
			<th colspan="4" align="center">Edit Script</th>
		</tr>
		<tr>
			<td style="width:15%;">Script Name</td>
			<td>
				<input type="text" name="name" id="name" size="37" maxlength="150" value="${script.name}">			
				&emsp;&emsp;&emsp;&emsp;
				<a href="" onclick="showStreamDetails();return false;">Show Stream Details</a>
			</td>
		</tr>
		<tr>

		<tr>
			<td style="width:15%;">Primitive Test</td>
			<td><select name="ptest" id="ptest" style="width: 250px"><%--
					<option value="default">--Please Select--</option>
					--%><g:each in="${script}" var="primList">
						<option value="${script.primitiveTest.id}">
							${script.primitiveTest.name}
						</option>
					</g:each>
			</select>&emsp;&emsp;&emsp;&emsp;		
			
			<g:if test="${script?.primitiveTest?.module?.testGroup.toString() != "OpenSource"  }"  >
				<a href="JavaScript:newPopup('../htmls/${script?.primitiveTest?.module?.name.trim()}.html#${script.name}');">View&nbsp;${script?.primitiveTest?.module?.name}&nbsp;Testcase</a>
			</g:if>						
			</td>
		</tr>
		
		<tr>
			<td>Box Type</td>
			<td>
				<g:select id="boxTypes" name="boxTypes"  from="${com.comcast.rdk.BoxType.list()}" optionKey="id" required="" value="${script.boxTypes}" class="many-to-one selectCombo" multiple="true"/>
				 &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;Execution TimeOut &emsp;
				<input type="text" id="execTime" name="executionTime" size="5" value="${script.executionTime}" />(min)
			</td>
		</tr>

		<tr>
			<td>RDK Version</td>
			<td>
				<g:select id="rdkVersions" name="rdkVersions"  from="${com.comcast.rdk.RDKVersions.list()}" optionKey="id" required="" value="${script.rdkVersions}" class="many-to-one selectCombo" multiple="true"/>
			</td>
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
		<tr id="buttons">
			<td colspan="2" align="center">
				<g:if test="${SecurityUtils.getSubject().hasRole('ADMIN')}" >
				<g:if test="${flag != 'STATIC'}" >				
					<input type="submit" value="Update" id="save">&emsp;
					<input type="reset" value="Cancel" id="cancel" onclick="makeScriptEditable('${script.id}')">				
				</g:if>
				</g:if>
			</td>
		</tr>
	</table>
</g:form>
<g:if test="${SecurityUtils.getSubject().hasRole('ADMIN')}" >
<g:form name="downloadScriptForm" action="exportScriptContent" controller="scriptGroup" method="post">
		<input type="hidden" name="id" id="id" value="${script.id}">
		<table>
		<tr></tr>
			<tr>
				<td style="width: 15%;"></td>
				<td style="width: 80%;"><input type="submit"
					value="Download Script" id="download"></td>
			</tr>
		</table>
	</g:form>
</g:if>
</g:if>