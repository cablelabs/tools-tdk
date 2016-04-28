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
<%--<!DOCTYPE html>--%>
<%@ page import="com.comcast.rdk.Device"%>
<%@ page import="com.comcast.rdk.ScriptGroup"%>
<%@ page import="com.comcast.rdk.Execution"%>

<html>
<head>
<meta name="layout" content="main">
<g:set var="entityName"
	value="${message(code: 'ScriptExecution.label', default: 'ScriptExecution')}" />
<link rel="stylesheet"
	href="${resource(dir:'css',file:'jquery.jqplot.min.css')}" />
<link rel="stylesheet"
	href="${resource(dir:'css',file:'shCoreDefault.min.css')}" />
<link rel="stylesheet"
	href="${resource(dir:'css',file:'shThemejqPlot.min.css')}" />
<title>Trends</title>
<g:javascript library="chart/jquery.jqplot.min" />
<g:javascript library="chart/shCore.min" />
<g:javascript library="chart/shBrushJScript.min" />
<g:javascript library="chart/shBrushXml.min" />
<g:javascript library="chart/jqplot.barRenderer.min" />
<g:javascript library="chart/jqplot.categoryAxisRenderer.min" />
<g:javascript library="chart/jqplot.pointLabels.min" />
<g:javascript library="chart/jqplot.canvasTextRenderer.min" />
<g:javascript library="chart/jqplot.canvasAxisLabelRenderer.min" />
<g:javascript library="chart/jqplot.canvasAxisTickRenderer.min" />
<g:javascript library="jquery.more" />
<g:javascript library="select2" />
<g:javascript library="chartview" />
<link rel="stylesheet"
	href="${resource(dir:'css',file:'jquery-ui.css')}" type="text/css" />
<link rel="stylesheet" href="${resource(dir:'css',file:'select2.css')}"
	type="text/css" />

<script type="text/javascript">

	$(document).ready(function() {		
		$("#trendid").addClass("changecolor");	
		$("#executionId").select2();	
		var defaultValue = "ExecutionBased";
		$('input[name=chartOption][value=ExecutionBased]').prop('checked', true);	
		$("#previous").hide();
		$("#next").hide();
		$("#home").hide();
	});
	
</script>
</head>
<body>
	<div id="categoricalDisplay" style="margin-left: 10px;">
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
			<div style="width:40%;overflow: auto;margin-bottom: 20px;">
				<div style="float: left;">Choose the category of device :</div>
				<div style="float: left;margin-left: 20px;">
					<g:form controller="trends" action="chart">
						<g:select name="category" from="['RDKV','RDKB']"
							onchange="submit()" value="${category}" />
					</g:form>
				</div>
			</div>
			<div>
				<g:hiddenField name="startIndex" value="${startIndex}" />
				<g:hiddenField name="endIndex" value="${endIndex}" />
				<input onclick="showExecutionBased();" type="radio"
					name="chartOption" value="ExecutionBased" checked="checked" />Compare
				Results by Execution Name &emsp;<input onclick="showDeviceBased();"
					type="radio" name="chartOption" value="DeviceBased" />Compare
				Results by Device Details &nbsp;&nbsp;

			</div>
			<br />

			<div id="executionbased">
				<table class="noClass" style="border: 1; border-color: black;">
					<tr>
						<td style="vertical-align: top;">Select Execution Names</td>
						<td id="executionNameList"><g:select id="executionId"
								multiple="true" style="height:200px;width:400px"
								name="execution" from="${executionList}" optionKey="id" value=""
								class="many-to-one selectCombo" /></td>

						<td style="vertical-align: top;">Select Field To Compare</td>
						<td><g:select id="chartType1" name="chartType"
								from="${['ExecutionStatus', 'TimingInfo', 'CPU_Utilization','Memory_Utilization','Memory_Used_Percentage']}"
								value="${count}" required="" /></td>
						<td style="vertical-align: top;">Select chart Type</td>
						
						<td>
								<input type="radio"
									name="ChartType" id="bar" value="BarChart" checked="checked" />Script
								Group Wise <br> <input 
									type="radio" name="ChartType" id="line " value="LineChart" />Script
								Wise
						</td>
						
						
						
						<td>
							<g:submitToRemote class=" buttons" value="Compare"
								before="homePage()" onclick="showChart()" /> <br>
						</td>
					</tr>
				</table>
				<table>
					<tr>
						<td align="left" width="60%"><input id="previous"
							type="button" value="Previous " onclick="previousPlot()"
							class="buttons" style="width: 9%" /></td>
						<td align="center" width="40%"><input id="next" type="button"
							value="Next" onclick="nextPlot()" class="buttons"
							style="width: 15%" /></td>
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
								from="${Device?.findAllByCategory(category)}" required=""
								value="" optionKey="id" class="many-to-one selectCombo" style="max-width:200px;"/></td>
						<td style="vertical-align: middle;">ScriptGroup</td>
						<td><g:select id="scriptGrp" name="scriptGrp"
								noSelection="['' : 'Please Select']"
								from="${ScriptGroup?.findAllByCategory(category)}" required=""
								optionKey="id" class="many-to-one selectCombo" /></td>
						<td style="vertical-align: middle;">Select Field To Compare</td>
						<td><g:select id="chartType" name="chartType"
								from="${['ExecutionStatus', 'TimingInfo', 'CPU_Utilization','Memory_Utilization','Memory_Used_Percentage']}"
								value="${count}" required="" /></td>
						<td style="vertical-align: middle;">Result No's</td>
						<td><g:select id="resultCount" name="result.count"
								from="${2..10}" value="${count}" style="width:45px;" required="" /></td>
						<td><input type="button" value="Compare"/></td>
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
						<td><g:submitToRemote class=" buttons" value="Compare"
								onclick="showChart1();" before="homePage()" /> <br></td>
					</tr>
				</table>
				<table>
					<tr>
						<td align="left" width="60%"><input id="previous1"
							type="button" value="Previous " onclick="previousPlot()"
							class="buttons" style="width: 9%; display: none" /></td>
						<td align="center" width="50%"><input id="next1"
							type="button" value="Next" onclick="nextPlot()" class="buttons"
							style="width: 15%; display: none" /></td>
						<td align="right" width="99%" id="home1"><img
							src="../images/skin/house.png" onclick="homePage()" height="28"
							width="28" title="First Page" /></td>
						<script type="text/javascript">
						var elem = document.getElementById("home1");
						elem.style.display = "none";
					</script>
					</tr>
				</table>
			</div>
			<div class="chartdivclass" id="chartdiv"
				style="width: 100%; height: 600px;"></div>
		</div>






	</div>
</body>
</html>
