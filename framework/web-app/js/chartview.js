/*
 * ============================================================================
 * COMCAST CONFIDENTIAL AND PROPRIETARY
 * ============================================================================
 * This file and its contents are the intellectual property of Comcast.  It may
 * not be used, copied, distributed or otherwise  disclosed in whole or in part
 * without the express written permission of Comcast.
 * ============================================================================
 * Copyright (c) 2013 Comcast. All rights reserved.
 * ============================================================================
 */


function showChart(){
	
	$( ".chartdivclass" ).empty();	
	//$('#chartdiv div').html('');
	var id = $("#devices").val();
	
	var scriptGroup = $("#scriptGrp").val();
	
	var resultcount = $("#resultCount").val();

	var ticks = ['1', '2', '3'];
	var labels = ["Success", "Failure", "Not Executed"];
	var labelsBenchMark = ["Execution Time(millisec)"];
	var labelsSd = ["CPU Utilization","Memory Utilization"];
	var labelsCPUSd = ["CPU Average Utilization","CPU Peak Utilization"];
	var labelsMemorySd = ["Memory Available Peak","Memory Used Peak"];
	var labelsMemoryPercSd = ["Memory Used Percentage Peak"];
	var labelsSd1 = ["Paging In","Paging Out"];
	var labelsSwap = ["Swaping"];
	var labelsLoadAvg = ["Load Average"];
	var chartType = null;
	var executionIds = $("#executionId").val();
	var executionIdList = null

	var checked_radio = $('input:radio[name=chartOption]:checked').val();

	if(checked_radio!=undefined)
	{
	    if(checked_radio=="DeviceBased"){
	    	executionIdList = "";
	    	chartType = $("#chartType").val();
		}
	    else{
	    	executionIdList = executionIds.toString();		
	    	chartType = $("#chartType1").val();    
		}
	}

	if(chartType == "ExecutionStatus"){
		
		$.get('getStatusChartData', {deviceId : id, scriptGroup : scriptGroup, resultCnt : resultcount, executionIds : executionIdList}, function(data) { 	
	  		
		    plot2 = $.jqplot('chartdiv', data.listdate, {
		    	seriesColors:['green', 'red', 'grey'],
		        seriesDefaults: {
		            renderer:$.jqplot.BarRenderer,
		            rendererOptions: {
		                barWidth: 10
		             },
		            pointLabels: { show: true }
		        },
		        legend: {
		            show: true,
		            placement: 'outsideGrid',
		            labels: labels,
		            location: 'ne',
		            rowSpacing: '0px'
		        },
		        axes: {
		            xaxis: {
		                renderer: $.jqplot.CategoryAxisRenderer,
		                label:'Execution Name',		                
		                ticks: data.execName,
		                tickOptions:{
		                    angle: -60
		                },
		                tickRenderer:$.jqplot.CanvasAxisTickRenderer
		            },
	
		           yaxis: {
		        	    labelRenderer: $.jqplot.CanvasAxisLabelRenderer,
			            min:0,
			            max: data.yCount, 
			            numberTicks: 11,
			            label:'Script Count'
			        }
		        }
		    });
			 		   	
		});
	}
	else if(chartType == "TimingInfo"){		
		$.get('getStatusBenchMarkData', {deviceId : id, scriptGroup : scriptGroup, resultCnt : resultcount, executionIds : executionIdList}, function(data) {
			
			plot3 = $.jqplot('chartdiv', [data.benchmark], {
		        seriesDefaults: {
		            renderer:$.jqplot.BarRenderer,
		            pointLabels: { show: true },
		            rendererOptions: {
		                barWidth: 25
		             }
		        },
		        legend: {
		            show: true,
		            placement: 'outsideGrid',
		            labels: labelsBenchMark,
		            location: 'ne',
		            rowSpacing: '0px'
		        },		     
		        axes: {
		            xaxis: {
		                renderer: $.jqplot.CategoryAxisRenderer,
		                label:'Execution Name',
		                ticks: data.execName,
		                tickOptions:{
		                    angle: -60
		                },
		                tickRenderer:$.jqplot.CanvasAxisTickRenderer
		            },
		        	yaxis: {
		        	    labelRenderer: $.jqplot.CanvasAxisLabelRenderer,			           
			            label:'Time in milliseconds'
		        	}
		        }
		    });	 
		});	
	}
	else if(chartType == "CPU_Utilization"){			
		$.get('getStatusSystemDiagnosticsCPUData', {deviceId : id, scriptGroup : scriptGroup, resultCnt : resultcount, executionIds : executionIdList}, function(data) { 
			if(data.systemDiag == null || data.systemDiag == ""){
				alert("Performance data is not available with the selected script and device ");
			}
			else{
			plot3 = $.jqplot('chartdiv', data.systemDiag, {
		        seriesDefaults: {
		            renderer:$.jqplot.BarRenderer,
		            rendererOptions: {
		                barWidth: 20
		             },
		            pointLabels: { show: true }
		        },
		        legend: {
		            show: true,
		            placement: 'outsideGrid',
		            labels: labelsCPUSd,
		            location: 'ne',
		            rowSpacing: '0px'
		        },
		        axes: {
		            xaxis: {
		                renderer: $.jqplot.CategoryAxisRenderer,
		                label:'Execution Name',
		                ticks: data.execName,
		                tickOptions:{
		                    angle: -60
		                },
		                tickRenderer:$.jqplot.CanvasAxisTickRenderer
		                
		            },
		            yaxis: {
		        	    labelRenderer: $.jqplot.CanvasAxisLabelRenderer,			           
			            label:'Percentage of Utilization'
		        	}
		        }
		    });	 
			
		   }
			
		});	
	}else if(chartType == "Memory_Utilization"){			
		$.get('getStatusSystemDiagnosticsPeakMemoryData', {deviceId : id, scriptGroup : scriptGroup, resultCnt : resultcount, executionIds : executionIdList}, function(data) { 
			if(data.systemDiag == null || data.systemDiag == ""){
				alert("Performance data is not available with the selected script and device ");
			}
			else{
			plot3 = $.jqplot('chartdiv', data.systemDiag, {
		        seriesDefaults: {
		            renderer:$.jqplot.BarRenderer,
		            rendererOptions: {
		                barWidth: 20
		             },
		            pointLabels: { show: true }
		        },
		        legend: {
		            show: true,
		            placement: 'outsideGrid',
		            labels: labelsMemorySd,
		            location: 'ne',
		            rowSpacing: '0px'
		        },
		        axes: {
		            xaxis: {
		                renderer: $.jqplot.CategoryAxisRenderer,
		                label:'Execution Name',
		                ticks: data.execName,
		                tickOptions:{
		                    angle: -60
		                },
		                tickRenderer:$.jqplot.CanvasAxisTickRenderer
		                
		            },
		            yaxis: {
		        	    labelRenderer: $.jqplot.CanvasAxisLabelRenderer,			           
			            label:'Percentage of Utilization'
		        	}
		        }
		    });	 
			
		   }
			
		});	
	}else if(chartType == "Memory_Used_Percentage"){			
		$.get('getStatusSystemDiagnosticsMemoryPercData', {deviceId : id, scriptGroup : scriptGroup, resultCnt : resultcount, executionIds : executionIdList}, function(data) { 
			if(data.systemDiag == null || data.systemDiag == ""){
				alert("Performance data is not available with the selected script and device ");
			}
			else{
			plot3 = $.jqplot('chartdiv', data.systemDiag, {
		        seriesDefaults: {
		            renderer:$.jqplot.BarRenderer,
		            rendererOptions: {
		                barWidth: 20
		             },
		            pointLabels: { show: true }
		        },
		        legend: {
		            show: true,
		            placement: 'outsideGrid',
		            labels: labelsMemoryPercSd,
		            location: 'ne',
		            rowSpacing: '0px'
		        },
		        axes: {
		            xaxis: {
		                renderer: $.jqplot.CategoryAxisRenderer,
		                label:'Execution Name',
		                ticks: data.execName,
		                tickOptions:{
		                    angle: -60
		                },
		                tickRenderer:$.jqplot.CanvasAxisTickRenderer
		                
		            },
		            yaxis: {
		        	    labelRenderer: $.jqplot.CanvasAxisLabelRenderer,			           
			            label:'Percentage of Utilization'
		        	}
		        }
		    });	 
			
		   }
			
		});	
	}
	else if(chartType == "Paging"){	
		$.get('getPagingData', {deviceId : id, scriptGroup : scriptGroup, resultCnt : resultcount, executionIds : executionIdList}, function(data) { 
			if(data.systemDiag == null || data.systemDiag == ""){
				alert("Performance data is not available with the selected script and device ");
			}
			else{
			plot3 = $.jqplot('chartdiv', data.systemDiag, {
		        seriesDefaults: {
		            renderer:$.jqplot.BarRenderer,
		            rendererOptions: {
		                barWidth: 20
		             },
		            pointLabels: { show: true }
		        },
		        legend: {
		            show: true,
		            placement: 'outsideGrid',
		            labels: labelsSd1,
		            location: 'ne',
		            rowSpacing: '0px'
		        },
		        axes: {
		            xaxis: {
		                renderer: $.jqplot.CategoryAxisRenderer,
		                label:'Execution Name',
		                ticks: data.execName,
		                tickOptions:{
		                    angle: -60
		                },
		                tickRenderer:$.jqplot.CanvasAxisTickRenderer
		                
		            },
		            yaxis: {
		        	    labelRenderer: $.jqplot.CanvasAxisLabelRenderer,			           
			            label:'Values'
		        	}
		        }
		    });	 
			}
		});	
	}    
	else if(chartType == "Swaping"){	
		$.get('getSwapData', {deviceId : id, scriptGroup : scriptGroup, resultCnt : resultcount, executionIds : executionIdList}, function(data) { 
			if(data.systemDiag == null || data.systemDiag == ""){
				alert("Performance data is not available with the selected script and device ");
			}
			else{
			plot3 = $.jqplot('chartdiv', data.systemDiag, {
		        seriesDefaults: {
		            renderer:$.jqplot.BarRenderer,
		            rendererOptions: {
		                barWidth: 20
		             },
		            pointLabels: { show: true }
		        },
		        legend: {
		            show: true,
		            placement: 'outsideGrid',
		            labels: labelsSwap,
		            location: 'ne',
		            rowSpacing: '0px'
		        },
		        axes: {
		            xaxis: {
		                renderer: $.jqplot.CategoryAxisRenderer,
		                label:'Execution Name',
		                ticks: data.execName,
		                tickOptions:{
		                    angle: -60
		                },
		                tickRenderer:$.jqplot.CanvasAxisTickRenderer
		                
		            },
		            yaxis: {
		        	    labelRenderer: $.jqplot.CanvasAxisLabelRenderer,			           
			            label:'Percentage'
		        	}
		        }
		    });	 
		  }
		});	
	}
	else if(chartType == "LoadAverage"){	
	
		$.get('getLoadAverage', {deviceId : id, scriptGroup : scriptGroup, resultCnt : resultcount, executionIds : executionIdList}, function(data) { 
			if(data.systemDiag == null || data.systemDiag == ""){
				alert("Performance data is not available with the selected script and device ");
			}
			else{
			plot3 = $.jqplot('chartdiv', data.systemDiag, {
		        seriesDefaults: {
		            renderer:$.jqplot.BarRenderer,
		            rendererOptions: {
		                barWidth: 20
		             },
		            pointLabels: { show: true }
		        },
		        legend: {
		            show: true,
		            placement: 'outsideGrid',
		            labels: labelsLoadAvg,
		            location: 'ne',
		            rowSpacing: '0px'
		        },
		        axes: {
		            xaxis: {
		                renderer: $.jqplot.CategoryAxisRenderer,
		                label:'Execution Name',
		                ticks: data.execName,
		                tickOptions:{
		                    angle: -60
		                },
		                tickRenderer:$.jqplot.CanvasAxisTickRenderer
		                
		            },
		            yaxis: {
		        	    labelRenderer: $.jqplot.CanvasAxisLabelRenderer,			           
			            label:'Value'
		        	}
		        }
		    });	 
			}
		});	
	}
	$('#chartOptionsDiv').show();
	//showExecutionStatusChart();
}

function showExecutionBased(){
	$(".chartdivclass").empty();	
	$("#executionbased").show();	
	$("#devicebased").hide();
}

function showDeviceBased(){
	$(".chartdivclass").empty();	
	$("#executionbased").hide();	
	$("#devicebased").show();	
}
