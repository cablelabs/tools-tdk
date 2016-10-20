<!--
 If not stated otherwise in this file or this component's Licenses.txt file the
 following copyright and licenses apply:

 Copyright 2016 RDK Management

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

 http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
-->
<%@page import="com.comcast.rdk.Utility"%>
<%@ page import="com.comcast.rdk.Device"%>
<%@ page import="com.comcast.rdk.ScriptGroup"%>
<div id="chart1"></div>
<div>
	<h1>Result Analysis</h1>
	<g:if test="${flash.message}">
		<div class="message" role="status">
			${flash.message}
		</div>
	</g:if>
	<g:if test="${error}">
		<ul class="errors" role="alert">
			<li>
				${error}
			</li>
		</ul>
	</g:if>
	<br>
	<div>
		<g:hiddenField name="startIndex" value="${startIndex}" />
		<g:hiddenField name="endIndex" value="${endIndex}" />
		<input onclick="showExecutionBased();" type="radio" name="chartOption"
			value="ExecutionBased" checked="checked" id="exec" />Compare Results
		by Execution Name &emsp;<input onclick="showDeviceBased();"
			type="radio" name="chartOption" value="DeviceBased" id="device" />Compare
		Results by Device Details &emsp;&emsp;
		<%--<g:select name="category" from="['RDKV','RDKB']"
			onchange="updateValueOnCategoryChange(this.value)"
			value="${category}" />
	--%>
	<g:form controller="trends" action="chart">
		<g:select name="category" from="['RDKV','RDKB']"
			onchange="submit()"
			value="${category}" />
	</g:form>
	</div>
	<br />

	<div id="executionbased">
		<table class="noClass" style="border: 1; border-color: black;">
			<tr>
				<td style="vertical-align: top;">Select Execution Names</td>
				<td><g:select id="executionId" multiple="true"
						style="height:200px;width:400px" name="execution"
						from="${executionList}" optionKey="id" value=""
						class="many-to-one selectCombo" /></td>

				<td style="vertical-align: top;">Select Field To Compare</td>
				<td><g:select id="chartType1" name="chartType"
						from="${['ExecutionStatus', 'TimingInfo', 'CPU_Utilization','Memory_Utilization','Memory_Used_Percentage']}"
						value="${count}" required="" /></td>
				<td>
					<form>
						<input onclick="showBarChartBased()" type="radio" name="ChartType"
							id="bar" value="BarChart" checked="checked" />Script Group Wise
						<br> <input onclick="showLineChartBased()" type="radio"
							name="ChartType" id="line " value="LineChart" />Script Wise
					</form>
				</td>

				<td>
					<%--
	          			<input type="button" value="Compare" onclick="showChart();" /><br>           			
	          		--%> <g:submitToRemote class=" buttons" value="Compare"
						before="homePage();" onclick="showChart();" />
				</td>
			</tr>
		</table>
		<table>
			<tr>
				<td align="left" width="60%"><input id="previous" type="button"
					value="Previous " onclick="previousPlot()" class="buttons"
					style="width: 9%" /></td>
				<td align="center" width="40%"><input id="next" type="button"
					value="Next" onclick="nextPlot()" class="buttons"
					style="width: 15%" /></td>
				<!-- my new add  -->
				<td align="right" width="99%" id="home"><img
					src="../images/skin/house.png" onclick="homePage()" height="28"
					width="28" title="First Page " /></td>
			</tr>
		</table>
	</div>

	<div id="devicebased" style="display: none;">
		<table class="noClass" style="border: 1; border-color: black;">
			<tr>
				<td style="vertical-align: middle;">Device</td>
				<td><g:select id="devices" name="devices"
						noSelection="['' : 'Please Select']"
						from="${Device?.findAllByCategory(Utility.getCategory(category))}"
						required="" value="" optionKey="id"
						class="many-to-one selectCombo" /></td>
				<td style="vertical-align: middle;">ScriptGroup</td>
				<td><g:select id="scriptGrp" name="scriptGrp"
						noSelection="['' : 'Please Select']"
						from="${ScriptGroup?.findAllByCategory(Utility.getCategory(category))}"
						required="" optionKey="id" class="many-to-one selectCombo" /></td>
				<td style="vertical-align: middle;">Select Field To Compare</td>
				<td><g:select id="chartType" name="chartType"
						from="${['ExecutionStatus', 'TimingInfo', 'CPU_Utilization','Memory_Utilization','Memory_Used_Percentage']}"
						value="${count}" required="" /></td>
				<td style="vertical-align: middle;">Result No's</td>
				<td><g:select id="resultCount" name="result.count"
						from="${2..10}" value="${count}" style="width:45px;" required="" /></td>
				<td><input type="button" value="Compare" onclick="showChart();" /><br>
					<td style="vertical-align: top;">Select chart</td>
					<td>
						<form>
							<input type="radio" name="ChartType1" id="bar" value="BarChart"
								checked="checked" />Script Group Wise <br> <input
								type="radio" name="ChartType1" id="line" value="LineChart" />Script
							Wise
						</form>
					</td>
					<td>
						<g:submitToRemote  class =" buttons"   value="Compare"
						onclick="showChart1();"  before ="homePage()"/>							
						<br></td>
				</tr>
			</table>
			<table>
				<tr>
					<td align="left" width ="60%">
					<input id="previous1" type="button"
						value="Previous " onclick="previousPlot()" class="buttons"
						style="width: 9%;display:none" /></td>
					<td align="center" width= "50%">
					<input id="next1" type="button"
						value="Next" onclick="nextPlot()" class="buttons"
						style="width: 15%;display:none" /></td>
					<%--<td align="right" width= "99%" id= "home1" ><img src="../images/skin/house.png"  onclick="homePage()" height="28" width="28"  title="First Page"/></td>
						<script type="text/javascript">
						var elem = document.getElementById("home1");
						elem.style.display = "none";
					</script>
				--%></tr>
			</table>
		</div>
	</div>
	<div class="chartdivclass" id="chartdiv"
		style="width: 100%; height: 600px;"></div>
</div>
