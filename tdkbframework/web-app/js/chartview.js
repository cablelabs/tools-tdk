/*
 * If not stated otherwise in this file or this component's Licenses.txt file the
 * following copyright and licenses apply:
 *
 * Copyright 2016 RDK Management
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
*/
var listTest =[];
var startIndex = 0 ;
var endIndex = 8  ; 
var maxSize = -1;
var previousCount = 0;
var nextCount = 0 ;
/**
 * Compare the result by execution name 
 */
function showChart(){	
	var checked_radio1 = $('input:radio[name=ChartType]:checked').val();
	if(checked_radio1 != undefined  ){
		if(checked_radio1 == "BarChart" ){
			$("#previous").hide();
			$("#next").hide();	
			showBarChart();	

		}else if(checked_radio1 == "LineChart" ){
			showLineChart();	 
		}
	}
}
/**
 * Compare result by device details 
 */
function showChart1(){	
	var checked_radio1 = $('input:radio[name=ChartType1]:checked').val();
	if(checked_radio1 != undefined  ){
		if(checked_radio1 == "BarChart" ){
			$("#previous").hide();
			$("#next").hide();	
			$("#previous1").hide();
			$("#next1").hide();	
			showBarChart();	
		}else if(checked_radio1 == "LineChart" ){
			showLineChart();	 
		}
	}
}
/**
 * Function for hide buttons (home,next, previous buttons)  
 */
function hideOptions(){
	$("#previous").hide();
	$("#next").hide();	
	$("#previous1").hide();
	$("#next1").hide();	
	$("#home").hide();
	$("#home1").hide();	
}








/**
 * Plotting the bar chart  on the bases of the script group.
 */

function showBarChart(){	
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
	// plotting the  graph for Execution Status  
	if(chartType == "ExecutionStatus"){
		hideOptions();
		$.get('getStatusChartData', {deviceId : id, scriptGroup : scriptGroup, resultCnt : resultcount, executionIds : executionIdList}, function(data) {
			if(data.execName.length  == 1  ){
				alert(" Please select  more than one execution name");
			}else{

				plot2 = $.jqplot('chartdiv', data.listdate, {
					seriesColors:['green', 'red', 'grey'],
					animate: true,
					animateReplot: true,
					seriesDefaults: {
						renderer:$.jqplot.BarRenderer,
						rendererOptions: {
							barWidth: 10,
							animation: {
								speed: 2500
							},	
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
			}

		});
	}// Plotting  the  bar chart  for timing info 
	else if(chartType == "TimingInfo"){		
		$.get('getStatusBenchMarkData', {deviceId : id, scriptGroup : scriptGroup, resultCnt : resultcount, executionIds : executionIdList}, function(data) {
			if(data.execName.length  == 1  ){
				alert(" Please select  more than one execution name");
			}else{
				plot3 = $.jqplot('chartdiv', [data.benchmark], {
					animate: true,
					animateReplot: true,
					seriesDefaults: {
						renderer:$.jqplot.BarRenderer,
						pointLabels: { show: true },
						rendererOptions: {
							barWidth: 25,
							animation: {
								speed: 2500
							},	
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
			}
		});	
	} //plotting the bar chart for " CPU-Utilization 
	else if(chartType == "CPU_Utilization"){			
		$.get('getStatusSystemDiagnosticsCPUData', {deviceId : id, scriptGroup : scriptGroup, resultCnt : resultcount, executionIds : executionIdList}, function(data) {
			if(data.execName.length  == 1  ){
				alert(" Please select  more than one execution name");
			}else{
				if(data.systemDiag == null || data.systemDiag == ""){
					alert("Performance data is not available with the selected script and device ");
				}
				else{
					plot3 = $.jqplot('chartdiv', data.systemDiag, {
						animate: true,
						animateReplot: true,
						seriesDefaults: {
							renderer:$.jqplot.BarRenderer,
							rendererOptions: {
								barWidth: 20,
								animation: {
									speed: 2500
								},	
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
			}

		});	//Plotting the graph for Memory_Utilization 
	}else if(chartType == "Memory_Utilization"){			
		$.get('getStatusSystemDiagnosticsPeakMemoryData', {deviceId : id, scriptGroup : scriptGroup, resultCnt : resultcount, executionIds : executionIdList}, function(data) {
			if(data.execName.length  == 1  ){
				alert(" Please select  more than one execution name");
			}else{
				if(data.systemDiag == null || data.systemDiag == ""){
					alert("Performance data is not available with the selected script and device ");
				}
				else{
					plot3 = $.jqplot('chartdiv', data.systemDiag, {
						animate: true,
						animateReplot: true,
						seriesDefaults: {
							renderer:$.jqplot.BarRenderer,
							rendererOptions: {
								barWidth: 20,
								animation: {
									speed: 2500
								},	
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
								label:'Used Memory(KB)'
							}
						}
					});	 

				}
			}

		});	//Plotting the graph for Memory_Used_Percentage 
	}else if(chartType == "Memory_Used_Percentage"){			
		$.get('getStatusSystemDiagnosticsMemoryPercData', {deviceId : id, scriptGroup : scriptGroup, resultCnt : resultcount, executionIds : executionIdList}, function(data) {
			if(data.execName.length  == 1  ){
				alert(" Please select  more than one execution name");
			}else{
				if(data.systemDiag == null || data.systemDiag == ""){
					alert("Performance data is not available with the selected script and device ");
				}
				else{
					plot3 = $.jqplot('chartdiv', data.systemDiag, {
						animate: true,
						animateReplot: true,
						seriesDefaults: {
							renderer:$.jqplot.BarRenderer,
							rendererOptions: {
								barWidth: 20,
								animation: {
								speed: 2500,
								},	
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
			}
		});	

	}
}
/**
 * Plotting the line chart. 
 */
function showLineChart(){
	$( ".chartdivclass" ).empty();	
	var id = $("#devices").val();
	var scriptGroup = $("#scriptGrp").val();
	var resultcount = $("#resultCount").val();
	var labels = ["Success", "Failure", "Not Executed"];	
	var chartType = null;
	var executionIds = $("#executionId").val();
	var executionIdList = null
	var type = null 
	var checked_radio = $('input:radio[name=chartOption]:checked').val();
	if(checked_radio!=undefined){
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
		hideOptions();		
		$.get('getStatusChartData1', {deviceId : id, scriptGroup : scriptGroup, resultCnt : resultcount, executionIds : executionIdList,startIndex:startIndex,endIndex:endIndex}, function(data) {	
			if(data.execName.length  == 1  ){
				alert(" Please select  more than one execution name");
			}else{						
				var plot2 = $.jqplot('chartdiv', [data.success , data.failure ,data.notFound] , {
					seriesColors:['green', 'red', 'gray '],
					animate: true,
					animateReplot: true,
					series:[
					        {
					        	showHighlight: false,
					        	yaxis: 'yaxis',
					        	rendererOptions: {
					        		animation: {
					        			speed: 2500
					        		},			                   
					           	}
					        }, 
					        {
					        	rendererOptions:{
					        		animation: {
					        			speed: 2000
					        		}
					        	}
					        }
					        ],
					        seriesDefaults: {
					        	rendererOptions: {
					        		lineWidth: 2,
					        		smooth: true,
					        	},
					      	pointLabels: { show: true, 
					      		
					      		}
					        },
					        legend: {
					        	show: true,
					        	placement: 'outsideGrid',
					        	labels: labels ,
					        	location: 'ne',
					        	rowSpacing: '0px'
					        },
					        axes: {
					        	xaxis: {
					        		renderer: $.jqplot.CategoryAxisRenderer,
					        		label:'Execution Name',	
					        		min:0,
					        		ticks: data.execName,
					        		tickOptions:{
					        			angle: -40
					        		},
					        		tickRenderer:$.jqplot.CanvasAxisTickRenderer
					        	},

					        	yaxis: {
					        		labelRenderer: $.jqplot.CanvasAxisLabelRenderer,
					        		min:0,
					        		max: data.yCount +5, 
					        		numberTicks: 11,
					        		label:'Script Count'
					        	}
					        },
					       /* highlighter: {
					        	show: true,
					        	sizeAdjust: 15,
					            tooltipAxes: 'y',
					        },
					        cursor: {
								show: true,
								 tooltipLocation:'sw', 
							}	*/				       
				});	

			}
		});
	}
	else if(chartType == "TimingInfo"){				
		$.get('getStatusBenchMarkData1', {deviceId : id, scriptGroup : scriptGroup,resultCnt : resultcount, executionIds : executionIdList, startIndex:startIndex,endIndex:endIndex}, function(data) {
			if( data.scripts.length == 0 ){			
				alert("Chart comparison not possible, matching script name not found ");	
			}else{
				if(data.execName.length  == 1  ){
					alert(" Please select  more than one execution name");
				}else{
					maxSize = data.maxSize;
					nextPreviousButtonDisplay();
					timingInfo(data);		
				}
			}
		});	
	}
	else if(chartType == "CPU_Utilization"){		
		$.get('getStatusSystemDiagnosticsCPUData1', {deviceId : id, scriptGroup : scriptGroup, resultCnt : resultcount, executionIds : executionIdList, startIndex:startIndex,endIndex:endIndex}, function(data) {
			if( data.scripts.length == 0 ){			
				alert("Chart comparison not possible, script name list is empty");	
			}else{
				if(data.execName.length  == 1  ){
					alert(" Please select  more than one execution name");
				}else{

					if(data.systemDiag == null || data.systemDiag == ""){
						alert("Performance data is not available with the selected script and device ");
					}else if ( data.scripts ==   null || data.scripts == " " ){
						alert(" Performance data is not available becoz scripts are not same ");
					}		
					else{
						maxSize = data.maxSize;	
						nextPreviousButtonDisplay();
						cpuUtilization(data);						
					}
				}
			}
		});	
	}else if(chartType == "Memory_Utilization"){			
		$.get('getStatusSystemDiagnosticsPeakMemoryData1', {deviceId : id, scriptGroup : scriptGroup, resultCnt : resultcount, executionIds : executionIdList,startIndex:startIndex,endIndex:endIndex}, function(data) {
			if( data.scripts.length == 0 ){			
				alert("Chart comparison not possible, script name list is empty");	
			}else{
				if(data.execName.length  == 1  ){
					alert(" Please select  more than one execution name");
				}else{
					if(data.systemDiag == null || data.systemDiag == ""){
						alert("Performance data is not available with the selected script and device ");
					}
					else{				
						maxSize = data.maxSize;
						nextPreviousButtonDisplay();
						memeryUtilization(data);
					}
				}
			}
		});	
	}else if(chartType == "Memory_Used_Percentage"){	
		$.get('getStatusSystemDiagnosticsMemoryPercData1', {deviceId : id, scriptGroup : scriptGroup, resultCnt : resultcount, executionIds : executionIdList,startIndex:startIndex,endIndex:endIndex}, function(data) {
			if( data.scripts.length == 0 ){			
				alert("Chart comparison not possible, script name list is empty");	
			}else{
				if(data.execName.length  == 1  ){
					alert(" Please select  more than one execution name");
				}else{
					if(data.systemDiag == null || data.systemDiag == ""){
						alert("Performance data is not available with the selected script and device ");
					}
					else{
						maxSize = data.maxSize;
						nextPreviousButtonDisplay();
						newFunMemPers(data);	
					}	
				}
			}
		});
	}	
	$('#chartOptionsDiv').show();
}

/**
 * function used to hide/show the next , previous button based on the datas 
 */
function nextPreviousButtonDisplay(){
	if(startIndex == 0 && endIndex == 8 &&  maxSize < endIndex ){
		$("#previous").hide();
		$("#next").hide();	
		$("#previous1").hide();
		$("#next1").hide();
		$("#home").hide();
		$("#home1").hide();
	}else if( startIndex == 0 &&  maxSize > endIndex){
		$("#previous").hide();
		$("#next").show();	
		$("#previous1").hide();
		$("#next1").show();	
		$("#home").hide();
		$("#home1").hide();
	}				
	else if(maxSize <= endIndex  ){		
		$("#previous").show();
		$("#next").hide();	
		$("#previous1").show();
		$("#next1").hide();	
		$("#home").show();
		$("#home1").show();
	}	
	else {
		$("#previous").show();
		$("#next").show();
		$("#previous1").show();
		$("#next1").show();
		$("#home").show();		
		$("#home1").show();		
	}
}
/**
 * Function display the execution name  based chart 
 */

function showExecutionBased(){
	$(".chartdivclass").empty();	
	$("#executionbased").show();	
	$("#devicebased").hide();
}
/**
 * Function display the device based chart 
 */

function showDeviceBased(){
	$(".chartdivclass").empty();	
	$("#executionbased").hide();	
	$("#devicebased").show();		
}

function updateValueOnCategoryChange(val){
	$.get('getCategorySpecificList',{category:val}, function(data) { 
		$("#categoricalDisplay").html(data);
	});
}


/**
 * This function plot the line graph for Memory_Utilization 
 */
function memeryUtilization(data){
	plot3 = $.jqplot('chartdiv', data.memoryValuesTest,{
		animate: true,
		animateReplot: true,
		series:[
		        {   
		        	showHighlight: false,
		        	yaxis: 'yaxis',
		        	rendererOptions: {
		        		animation: {
		        			speed: 2500
		        		},			                   
		        	}
		        }, 
		        {
		        	rendererOptions:{
		        		animation: {
		        			speed: 2000
		        		}
		        	}
		        }
		        ],
		        seriesDefaults: {
		        	rendererOptions: {
		        		lineWidth: 2,
		        		smooth: true,
		        	},
		        	pointLabels: { show: true ,
		        		}
		        },
		        legend: {
		        	show: true,
		        	placement: 'outsideGrid',
		        	labels: data.execName,
		        	location: 'ne',
		        	rowSpacing: '0px'
		        },
		        axes: {
		        	xaxis: {
		        		labelRenderer: $.jqplot.CanvasAxisLabelRenderer,
		        		renderer: $.jqplot.CategoryAxisRenderer,		               
		        		label:'Script Name',	
		        		min:0,
		        		ticks: data.scripts,	             
		        		tickOptions:{
		        			angle: 10,		   
		        			fontFamily: 'Courier New',
		        			fontSize: '9pt',

		        		},
		        		tickRenderer:$.jqplot.CanvasAxisTickRenderer
		        	},

		        	yaxis: {
		        		min:0,
		        		numberTicks: 11,
		        		labelRenderer: $.jqplot.CanvasAxisLabelRenderer,			           
		        		label:'Used Memory (KB)'
		        	}
		        },
		        /*highlighter: {
		        	show: true,
		        	sizeAdjust: 15,
		            tooltipAxes: 'y',
		        },
		        cursor: {
					show: true,
					 tooltipLocation:'sw', 
				} */		          
	});
}
/**
 * Function for  plotting the line chart for  CPU Utilization
 */
function cpuUtilization(data){
	plot3 = $.jqplot('chartdiv', data.cpuValuesTest,{ 
		animate: true,
		animateReplot: true,
		series:[
		        {  	showHighlight: false,
		        	yaxis: 'yaxis',
		        	rendererOptions: {
		        		animation: {
		        			speed: 2500,
		        		},			                   
		        	}
		        }, 
		        {	            	
		        	rendererOptions:{
		        		animation: {
		        			speed: 2000,
		        		}
		        	}
		        }
		        ],
		        seriesDefaults: {
		        	rendererOptions: {
		        		lineWidth: 2,
		        		smooth: true,
		        	},
		        	pointLabels: { show: true,
		        		},
		        },
		        legend: {
		        	show: true,
		        	placement: 'outsideGrid',		          
		        	labels : data.execName,		            
		        	location: 'ne',
		        	rowSpacing: '10px'
		        },
		        axes: {
		        	xaxis: {
		        		labelRenderer: $.jqplot.CanvasAxisLabelRenderer,
		        		renderer: $.jqplot.CategoryAxisRenderer,		               
		        		label:'Script  Name',	
		        		min:0,
		        		ticks: data.scripts,	             
		        		tickOptions:{
		        			angle: 10,		   
		        			fontFamily: 'Courier New',
		        			fontSize: '9pt',

		        		},
		        		tickRenderer:$.jqplot.CanvasAxisTickRenderer

		        	},	
		        	yaxis: {
		        		min:0,
		        		numberTicks: 11,		        	   
		        		labelRenderer: $.jqplot.CanvasAxisLabelRenderer,			           
		        		label:'Percentage of Utilization (Peak)'
		        	}
		        },
		       /* highlighter: {
		        	show: true,
		        	sizeAdjust: 15,
		            tooltipAxes: 'y',
		        },
		        cursor: {
					show: true,
					 tooltipLocation:'sw', 
				}*/
	});		

}
//Function for  plotting the line chart for  Memory Used Persentage 
function newFunMemPers(data){
	plot3 = $.jqplot('chartdiv', data.memoryValuesTest, {
		animate: true,
		animateReplot: true,
		series:[
		        {
		        	showHighlight: false,
		        	yaxis: 'yaxis',
		        	rendererOptions: {
		        		animation: {
		        			speed: 2500
		        		},			                   
		           	}
		        }, 
		        {
		        	rendererOptions:{
		        		animation: {
		        			speed: 2000
		        		}
		        	}
		        }
		        ],
		        seriesDefaults: {		           
		        	rendererOptions: {
		        		lineWidth: 2,
		        		smooth: true,
		        	},
		        	pointLabels: { show:true,
		        		}
		        },
		        legend: {
		        	show: true,
		        	placement: 'outsideGrid',
		        	labels: data.execName,
		        	location: 'ne',
		        	rowSpacing: '0px'
		        },
		        axes: {
		        	xaxis: {
		        		labelRenderer: $.jqplot.CanvasAxisLabelRenderer,
		        		renderer: $.jqplot.CategoryAxisRenderer,		               
		        		label:'Script Name',	
		        		min:0,
		        		ticks: data.scripts,	             
		        		tickOptions:{
		        			angle: 10,		   
		        			fontFamily: 'Courier New',
		        			fontSize: '9pt',

		        		},
		        		tickRenderer:$.jqplot.CanvasAxisTickRenderer
		        	},

		        	yaxis: {
		        		min:0,
		        		numberTicks: 11,
		        		labelRenderer: $.jqplot.CanvasAxisLabelRenderer,			           
		        		label:'Percentage of Utilization(Peak)'
		        	}
		        },
		        /*highlighter: {
		        	show: true,
		        	sizeAdjust: 15,
		            tooltipAxes: 'y',
		        },
		        cursor: {
					show: true,
					 tooltipLocation:'sw', 
				}*/
	});
}

//Function for  plotting the line chart for Timing info 

function  timingInfo(data ){
	plot3 = $.jqplot('chartdiv', data.benchmark , {
		animate: true,
		animateReplot: true,
		series:[
		        {
		        	showHighlight: false,
		        	yaxis: 'yaxis',
		        	rendererOptions: {
		        		animation: {
		        			speed: 2500
		        		},			                   
		        	}
		        }, 
		        {
		        	rendererOptions:{
		        		animation: {
		        			speed: 2000
		        		}
		        	}
		        }
		        ],
		        seriesDefaults: {
		        	rendererOptions: {
		        		lineWidth: 2,
		        		smooth: true,
		        	},
		        	pointLabels: { show: true,
		        		}
		        },
		        legend: {
		        	show: true,
		        	placement: 'outsideGrid',
		        	labels: data.execName,
		        	location: 'ne',
		        	rowSpacing: '0px',
		        	showSwatches: true,
		        },
		        axes: {
		        	xaxis: {
		        		labelRenderer: $.jqplot.CanvasAxisLabelRenderer,
		        		renderer: $.jqplot.CategoryAxisRenderer,		               
		        		label:'Script Name',	
		        		min:0,
		        		ticks: data.scripts,
		        		tickOptions:{
		        			angle: 10,		   
		        			fontFamily: 'Courier New',
		        			fontSize: '9pt',
		        		},
		        		tickRenderer:$.jqplot.CanvasAxisTickRenderer
		        	},

		        	yaxis: {
		        		min:0,
		        		numberTicks: 11,
		        		labelRenderer: $.jqplot.CanvasAxisLabelRenderer,			           
		        		label:'Execution Time(millisec) ',
		        	}
		        },
		        /*highlighter: {
		        	show: true,
		        	sizeAdjust: 15,
		            tooltipAxes: 'y',
		        },
		        cursor: {
					show: true,
					 tooltipLocation:'sw', 
				},*/
	});

}
/*
 * Plotting the 8 script for next points. 
 */
function nextPlot(){
	if((maxSize != -1 && endIndex <= maxSize) || maxSize == -1){
		startIndex = endIndex ;
		endIndex = startIndex + 8 ;
	}else{
		alert("No more next available");
	}
	nextCount++;
	showLineChart();
}
/*
 * Plotting the 8 script for previous points.
 */
function previousPlot(){
	if(startIndex == 0){
		alert("No more previous available");
	}else{
		endIndex = endIndex - 8 ;
		startIndex = endIndex - 8;
		if(startIndex < 0){
			startIndex = 0;
		}
	}
	previousCount++ ;
	showLineChart();
}


/**
 * Function for shows the home page
 */

function homePage(){	
	startIndex = 0 ;
	endIndex = 8  ; 

	var checked_radio1 = $('input:radio[name=ChartType]:checked').val();
	if(checked_radio1 != undefined ){
		if(checked_radio1 == "BarChart" ){
			showChart1();	
		}else{
			showChart();	
		}
	}

}


