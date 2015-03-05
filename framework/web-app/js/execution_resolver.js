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

var flagMark = false

$(document).ready(function() {
	$.ajaxSetup ({cache: false});
	timedRefresh();	
	deviceStatusRefresh();	
	$("#browser").treeview({
		
		animated:"normal",
		persist: "cookie"
	});
	
	$(this).bind("contextmenu", function(e) {
		e.preventDefault();
	});	
	
	$('.filedevicebusy').contextMenu('childs_menu', {
		bindings : {			
			'reset_device' : function(node) {
				if (confirm('Make sure no scripts is currently executed in the device. Are you want to reset the device?')) {
					resetDevice(node.id);
				}
			}
		}
	});
	
	
	/*$('.filedevicefree').contextMenu('childs_menu', {
		bindings : {			
			'reset_IpRule' : function(node) {
				if (confirm('Make sure no scripts is currently executed in the device. Are you want to reset the device?')) {
					resetIPRule(node.id);
				}
			}
		}
	});*/
		
	var decider_id = $("#decider").val();
	$("#execid").addClass("changecolor");	

	$("#scripts").select2();

	$(":checkbox").each(function() {
		$('.resultCheckbox').prop('checked', false);
		mark(this);
	});
	
	$('.markAll').prop('checked', false);
	
	$('#repeatId').attr('readonly', false);
	
	/*
jQuery 1.9+   $('#inputId').prop('readonly', true);
	 */
	
	
});

function stopExecution(obj){
	if (confirm('Execution will be stopped after finishing the current test case execution.\nDo you want to stop the execution ? ')) {
		$.get('stopExecution', {execid: obj}, function(data) {});
	}
	
}

function isNumberKey(evt)
{
   var charCode = (evt.which) ? evt.which : event.keyCode
   if (charCode > 31 && (charCode < 48 || charCode > 57))
      return false;

   return true;
}

function showSchedule(){
	if($("#scheduletest").prop('checked') == true){		
		$('#scheduleOptionDiv').show();
	}
	else{
		$('#scheduleOptionDiv').hide();
	}
}

function showSuite(){
	$('#testSuite').show();
	$('#singletest').hide();
}

function showSingle(){
	$('#singletest').show();
	$('#testSuite').hide();
}

function showOnetimeSchedule(){
	$('#onetimeScheduleDiv').show();
	$('#reccuranceScheduleDiv').hide();
}

function showReccuranceSchedule(){
	$('#reccuranceScheduleDiv').show();
	$('#onetimeScheduleDiv').hide();
}

function showDaily(){
	$('#reccurDaily').show();
	$('#reccurWeekly').hide();
	$('#reccurMonthly').hide();
}

function showWeekly(){
	$('#reccurDaily').hide();
	$('#reccurWeekly').show();
	$('#reccurMonthly').hide();
}

function showMonthly(){
	$('#reccurDaily').hide();
	$('#reccurWeekly').hide();
	$('#reccurMonthly').show();
}

function showScript(id){
	$.get('showDevices', {id: id}, function(data) { $("#responseDiv").html(data); });
	$.get('updateDeviceStatus', {id: id}, function(data) {refreshDevices(data);});
}

function refreshDevices(data){
	var container = document.getElementById("device_status");
	container.innerHTML= data;
	
	var selectedId = $("#selectedDevice").val();
	var deviceInstanceTotal = $("#deviceInstanceTotal").val();
	highlightTreeElement('deviceExecutionList_', selectedId, deviceInstanceTotal);
}

function resetDevice(id){
	$.get('resetDevice', {id: id}, function(data) { document.location.reload(); });
}


function resetIPRule(id){
	$.get('resetIPRule', {id: id}, function(data) { document.location.reload(); });
}


function changeStyle(){
	$('#resultDiv').css('display','table');
}

function showExecutionLog(id){	
	$.get('showLog', {id: id}, function(data) { $("#executionLogPopup").html(data); });		
	$("#executionLogPopup").modal({ opacity : 40, overlayCss : {
		  backgroundColor : "#c4c4c4" }, containerCss: {
	            width: 800,
	            height: 570
	            
	        } }, { onClose : function(dialog) {
		  $.modal.close(); } });
}	

function showScheduler(id){	
	
	var scriptGroup = $("#scriptGrp").val();
	var scripts = $("#scripts").val();
    var deviceList = $("#devices").val();
	var repeatid = $("#repeatId").val();

	 if ($('input[name=myGroup]:checked').val()=='TestSuite'){     	
	    	scripts = "";
	 }
	 else{     	
	    	scriptGroup ="";
	 }

	var reRun = "";
	var benchmark = "false";
	var systemDiag = "false"
    if ($("#rerunId").prop('checked')==true){     	
    	reRun = "true";
    }
	if ($("#benchmarkId").prop('checked')==true){     	
		benchmark = "true";
	}
	if ($("#systemDiagId").prop('checked')==true){     	
		systemDiag = "true";
	}
	
	if( (deviceList =="" || deviceList == null ) ){
		alert("Please select Device");
		return false;
	}
	
	if(deviceList.length > 1){	
		alert("Scheduling is not currently allowed for multiple devices");
		return false;
	}
	else{
		id = deviceList.toString();		
	}

	if((scripts=="" || scripts == null )&& scriptGroup == "" ){
		alert("Please select Script/ScriptGroup");
		return false;
	}
	if(scripts){
		var scriptVals = scripts.toString()
	}

	$.get('showSchedular', {deviceId : id, devices : deviceList.toString(), scriptGroup : scriptGroup, scripts:scriptVals, repeatId:repeatid, rerun:reRun, systemDiagnostics : systemDiag , benchMarking : benchmark}, function(data) { $("#scheduleJobPopup").html(data); });		
	$("#scheduleJobPopup").modal({ opacity : 40, overlayCss : {
		  backgroundColor : "#c4c4c4" }, containerCss: {
	            width: 800,
	            height: 570	            
	        } }, { onClose : function(dialog) {
		  $.modal.close(); } });
	$("#scheduletable").dataTable( {
		"sPaginationType": "full_numbers",
		 "bRetrieve": "true" 
	} );	
}

function showCleanUpPopUp(){
	$("#cleanupPopup").modal({ opacity : 40, overlayCss : {
		  backgroundColor : "#c4c4c4" }, containerCss: {
	            width: 600,
	            height: 250	            
	        } }, { onClose : function(dialog) {
		  $.modal.close(); } });
}

function showDateTime(){
	$('#defexecName').val(" ");
	checkDeviceList();
	var stbName
	var deviceList = $("#devices").val();
	 if(deviceList == null){
		 stbName = ""
	 }else if(deviceList.length > 1){	
		 stbName = "multiple"
	 }else{
		 stbName = $('#stbname').val();
	 }
	
	$.get('showDateTime', {}, function(data) { 	
		$('#defexecName').val(stbName+"-"+data[0]);
		$('#newexecName').val(stbName+"-"+data[0]);
	});		
}

function checkDeviceList(){
	 var deviceList = $("#devices").val();
	 if(deviceList != null && deviceList.length > 1){		
		 $("#repeatId").val(1);
		// document.getElementById("repeatId").disabled = true;
		 $('#repeatId').attr('readonly', true);
			
	 }
	 else{
		 $('#repeatId').attr('readonly', false);			
		// document.getElementById("repeatId").disabled = false;
	 }
}

function showEditableExecName(){
	$("#givenExcName").show();
	$("#defExcName").hide();
}

function showDefaultExecName(){
	$("#defExcName").show();
	$("#givenExcName").hide();	
	$('#newexecName').val($('#defexecName').val());
}

function displayWaitSpinner(){		
	$("#spinnr").show();
}

function hideWaitSpinner(){	
	$("#spinnr").hide();
}

function showSpinner(){		
	$("#spinner1").show();
}

function hideSpinner(){	
	$("#spinner1").hide();
}

var repeatTask;

function showWaitSpinner(){	
	$("#popup").show();
	$("#executeBtn").hide();
	
	var execId = $('#exId').val();
	var deviceList= $('#devices').val();
	if(deviceList  && deviceList.length > 1 )
	{
		$('#resultDiv'+execId).show();	
		$('#resultDiv'+execId).html('Multiple Device Execution ');
		//$('#dynamicResultDiv').show();
	}
	else
	{	
	$('#resultDiv'+execId).hide();
	$('#dynamicResultDiv').show();
	$('#dynamicResultDiv').html('Starting the script execution...');
	repeatTask = setInterval("updateLog()",5000);
	}
}

function showSpinner(){
	$("#delspinnr").show();
}

function hideSpinnerForDelete(){
	$("#delspinnr").hide();
	 $( "#cleanFromDate" ).datepicker();
	 $( "#cleanToDate" ).datepicker();
}

function updateLog(){
	var execName = "";
	if(  $("#defexecName").is(":visible") == true )
	{  
		execName = $('#defexecName').val();
	}
	
	if (  $("#newexecName").is(":visible") == true )
	{  
		execName = $('#newexecName').val();       
	}
	$.get('readOutputFileData', {executionName: execName}, function(data) {
		$("#dynamicResultDiv").html(data); 
	});
}

function completed(id) {
	if (repeatTask) {
		clearInterval(repeatTask);
	}
	showDateTime();
	var execId = $('#exId').val();
	if (id == execId) {
		$('#resultDiv' + execId).show();
		$('#dynamicResultDiv').hide();
	}

}
function changeStyles(){
	showDateTime();
	$("#popup").hide();
	$("#executeBtn").show();
}

function baseScheduleTableRemove(){		
	$("#baseScheduleTable").hide();
	$('.hello').remove();
	alert("script/ScriptGroup unScheduled");
}
function baseScheduleTableSave()
{
	alert(" Script/ScriptGroup Scheduled");
	$("#baseScheduleTable").hide();
	$('.hello').remove();
	
}
function baseScheduleTableDelete()
{
	
	$("#baseScheduleTable").hide();
	$('.hello').remove();
	
}

/**
 * Dynamic page refresh call. First time called from the document ready of list
 * page
 */
function timedRefresh() {
	if(flagMark == true){
		$('.markAll').prop('checked', true);
	}
	setTimeout("loadXMLDoc();", 5 * 1000);	
}

/**
 * Ajax call to refresh only the list table when dynamic refresh is enabled
 */
function loadXMLDoc() {
	var xmlhttp;	
	var url = $("#url").val();
	var paginateOffset = $("#pageOffset").val();
	if (window.XMLHttpRequest) {// code for IE7+, Firefox, Chrome, Opera, Safari
		xmlhttp = new XMLHttpRequest();
	} else {// code for IE6, IE5
		xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
	}
	xmlhttp.onreadystatechange = function() {
		if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
			document.getElementById("list-executor").innerHTML = xmlhttp.responseText;
			timedRefresh();			
		}
	} 
	if(paginateOffset != undefined){
		if(flagMark == true){
			$('.markAll').prop('checked', true);
		}
		xmlhttp.open("GET", url+"/execution/create?t=" + Math.random()+"&max=10&offset="+paginateOffset+"&devicetable=true&flagMark="+flagMark, true);
		if(flagMark == true){
			$('.markAll').prop('checked', true);
		}
	}
	xmlhttp.send();
}


/**
 * Dynamic page refresh call. First time called from the document ready of list
 * page
 */
function deviceStatusRefresh() {
	setTimeout("loadXMLDoc1();", 5 * 1000);	
	var selectedId = $("#selectedDevice").val();
	var deviceInstanceTotal = $("#deviceInstanceTotal").val();
	highlightTreeElement('deviceExecutionList_', selectedId, deviceInstanceTotal);
}

/**
 * Ajax call to refresh only the list table when dynamic refresh is enabled
 */
function loadXMLDoc1() {
	
	var xmlhttp;	
	var url = $("#url").val();
	if (window.XMLHttpRequest) {// code for IE7+, Firefox, Chrome, Opera, Safari
		xmlhttp = new XMLHttpRequest();
	} else {// code for IE6, IE5
		xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
	}
	xmlhttp.onreadystatechange = function() {
		if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
			document.getElementById("device_status").innerHTML = "";
			document.getElementById("device_status").innerHTML = xmlhttp.responseText;			
			deviceStatusRefresh();			
		}
	}
	xmlhttp.open("GET", url+"/execution/create?t=" + Math.random()+"&max=10&offset=0&devicestatustable=true", true);
	xmlhttp.send();
	
}

function hideSearchoptions(){
	$("#advancedSearch").hide();
	$("#minSearch").show();
	$('.veruthe').empty();
}

function hideAllSearchoptions(){
	$("#advancedSearch").hide();
	$("#minSearch").hide();
	$('.veruthe').empty();
}

function displayAdvancedSearch(){		
	$("#advancedSearch").show();
	$("#minSearch").hide();
	$('.veruthe').empty();
	$('.responseclass').empty();
	$("#listscript").hide();
	$("#scriptValue").val('');
	
}

function showMinSearch(){	
	$("#advancedSearch").hide();
	$("#minSearch").show();
	$('.veruthe').empty();
	$("#listscript").show();
}

function hideExectionHistory(){
	$("#listscript").hide();
}

function showOther(){
	$("#otherBased").show();
	$("#dateBased").hide()
	$('.veruthe').empty();
	
}

function showDateBased(){
	$("#dateBased").show();
	$("#otherBased").hide();
	$('.veruthe').empty();
}

function showScriptTypes(){
	var choice = $( "#scriptType" ).val()
	if((choice == "")){
		$("#scriptLabel").hide();
		$("#scriptVal").hide();
		$("#scriptValue").val('');
	}
	else{
		$("#scriptLabel").show();
		$("#scriptVal").show();
		$("#scriptValue").val('');
	}
}

function showFulltextDeviceDetails(k){
	$("#fulltext"+k).show();
	$("#firstfourlines"+k).hide();
	$("#showlessdd"+k).show();	
}

function showMintextDeviceDetails(k){
	$("#fulltext"+k).hide();
	$("#firstfourlines"+k).show();
	$("#showlessdd"+k).hide();	
}


/**
 * Function to perform deletion of marked execution results. This will invoke an
 * ajax method and perform deletion of corresponding execution instance.
 */
function deleteResults() {

	var notChecked = [];
	var checkedRows;
	$(":checkbox").each(function() {
		if (this.checked) {
			checkedRows = checkedRows + "," + this.id;
		} else {
			notChecked.push(this.id);
		}
	});
	if (checkedRows != null && checkedRows != "") {
		
		var result = confirm("Are you sure you want to delete?");
		if (result==true) {
			$.get('deleteExecutioResults', {
				checkedRows : checkedRows
			}, function(data) {
	
				$(":checkbox").each(function() {
					$('.resultCheckbox').prop('checked', false);
	
				});
				$('.markAll').prop('checked', false);
				location.reload();
			});
		}
	}
	else 
	{
		alert("Please select the execution entries")
	}	
}


/**
 * Function to perform mark all operation in execution page.
 * 
 * @param me
 */
function clickCheckbox(me) {
	

	var $this = $(this);
	if (me.checked) {
		$(":checkbox").each(function() {
			$('.resultCheckbox').prop('checked', true);
			if(this.id != "benchmarkId" && this.id != "rerunId" && this.id != "systemDiagId"){
				mark(this);
			}
		});
		flagMark = true
	} else {
		$(":checkbox").each(function() {
			$('.resultCheckbox').prop('checked', false);
			if(this.id != "benchmarkId" && this.id != "rerunId" && this.id != "systemDiagId"){
			mark(this);
			}
		});
		flagMark = false
	}
}



/**
 * Function to mark individual execution results in execution page.
 * 
 * @param me
 */
function mark(me) {

	if (me.id != 'undefined' && me.id != 'markAll1' && me.id != 'markAll2'
			&& me.id != "" && me.id != null) {
		if (me.checked) {
			$.get('updateMarkStatus', {
				markStatus : 1,
				id : me.id
			}, function(data) {
			});
		} else {
			$.get('updateMarkStatus', {
				markStatus : 0,
				id : me.id
			}, function(data) {
			});
		}
	}

}
