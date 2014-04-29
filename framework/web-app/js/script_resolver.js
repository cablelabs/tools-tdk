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
$(document).ready(function() {
	
	$("#scriptbrowser").treeview({
		animated:"normal",
		persist: "cookie"
	});
	
	$("#scriptbrowser").bind("contextmenu", function(e) {
		e.preventDefault();
	});
	
	$("#addScriptId").contextMenu('script_root_menu', {
		bindings : {
			'add_script' : function(node) {
				hideSearchoptions();
				createScriptForm();
			}
		}
	});
	
	
	$('.file').contextMenu('script_childs_menu', {
		bindings : {
			'edit_script' : function(node) {					
				editScript(node.id);
			},
			'delete_script' : function(node) {
				if (confirm('Are you want to delete property?')) {
					removeScript(node.id);
				}
			}
		}
	});
		
	var decider_id = $("#decider").val();
	
	$("#scriptgrpbrowser").treeview({
		animated:"normal",
		persist: "cookie"
	});
	
	$("#scriptgrpbrowser").bind("contextmenu", function(e) {
		e.preventDefault();
	});
	
	$('#addscriptGrpId').contextMenu('scriptgrp_root_menu', {
		bindings : {
			'add_scriptgrp' : function(node) {
				hideSearchoptions();
				createScriptGrpForm();
			}
		}
	});
		
	$('.hasChildren').contextMenu('scriptgrp_childs_menu', {
		bindings : {
			'edit_scriptgrp' : function(node) {
				hideSearchoptions();
				editScriptGroup(node.id);
			},
			'delete_scriptgrp' : function(node) {
				if (confirm('Are you want to delete property?')) {
					removeScriptGroup(node.id);
				}
			}
		}
	});

	$("#scriptid").addClass("changecolor");
	
});


function createScriptForm() {
	$.get('createScript', function(data) { $("#responseDiv").html(data); });
}

function editScript(id , flag ) {
	hideSearchoptions();
	$.get('editScript', {id: id , flag : flag}, function(data) { $("#responseDiv").html(data); });
}

function showScript(id, flag) {
	$.get('editScript', {id: id , flag : flag}, function(data) { $("#responseDiv").html(data); });
}

function removeScript(id){		
	$.get('deleteScript', {id: id}, function(data) { document.location.reload();  });
}

function createScriptGrpForm() {	
	$.get('create', function(data) { $("#responseDiv").html(data); });
}

function editScriptGroup(id) {
	hideAllSearchoptions();
	$.get('edit', {id: id}, function(data) { $("#responseDiv").html(data); });
}

function removeScriptGroup(id){	
	$.get('deleteScriptGrp', {id: id}, function(data) { document.location.reload();  });
}

function clearScriptArea(){
	var scripttextarea = document.getElementById('scriptArea');
	scripttextarea.innerHTML = "";
	document.getElementById("scriptArea").value = scripttextarea.innerHTML.html_entity_decode();	
}

function showStreamDetails(){		
	$.get('showStreamDetails', {}, function(data) { $("#streamDetailsPopup").html(data); });		
	$("#streamDetailsPopup").modal({ opacity : 40, overlayCss : {
		  backgroundColor : "#c4c4c4" }, containerCss: {
	            width: 800,
	            height: 400
	            
	        } }, { onClose : function(dialog) {
		  $.modal.close(); } });

	$("#locktable").dataTable( {
		"sPaginationType": "full_numbers"
	} );		
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
}

function showMinSearch(){	
	$("#advancedSearch").hide();
	$("#minSearch").show();
	$('.veruthe').empty();
}

function showExistingSuite(){
	$("#existingSuiteId").show();
	$("#newSuiteId").hide();
}

function showNewSuite(){
	$("#existingSuiteId").hide();
	$("#newSuiteId").show();
}


/**
 * Function to check whether device is saved or not. If yes show edit page.
 */
function updateScriptList(scriptName){
	$.get('fetchScript', {scriptName: scriptName}, function(data) {
		if(data!=""){
			if($("#isScriptExist").val()==""){
				$("#currentScriptId").val(data);
				setTimeout(function(){location.reload();editScript()},1000);
			}
			$("#isScriptExist").val("");
		}
		$("#scriptMessageDiv").show();
	});
}

/**
 * Function to check whether script with same name exist or not.
 * @param scriptName
 */
function isScriptExist(scriptName){
	$.get('fetchScript', {scriptName: scriptName}, function(data) {
		if(data!=""){
			$("#isScriptExist").val(data);
		}
		$("#scriptMessageDiv").show();
	});
}



