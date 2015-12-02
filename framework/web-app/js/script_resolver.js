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
				if (confirm('Are you sure you want to delete this script?')) {
					removeScript(node.id);
				}
			}
		}
	});
	
	var decider_id = $("#decider").val();
	
	$("#scriptgrpbrowser").treeview({
		animated:"normal",
		persist: "cookie",
		collapsed: true
	});
	
	$("#scriptgrpbrowser").bind("contextmenu", function(e) {
		e.preventDefault();
	});
	
	$('#addscriptGrpId').contextMenu('scriptgrp_root_menu', {
		bindings : {
			'add_scriptgrp' : function(node) {
				hideAllSearchoptions();
				createScriptGrpForm();
			},	
			'upload_scriptGroup' : function(node) {	
				showUploadOption();
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

function showUploadOption(){
	$("#responseDiv123").hide();
	$("#up_load").show();		
}

function hideUploadOption(){
	$("#responseDiv123").show();
	$("#up_load").hide();		
}

var displayedGroups = [];

// method returns script file list on hovering over test suite
function getScriptsList(val, scriptGroup, scriptInstanceTotal, totalScripts){
	var group = val.id;
	if(displayedGroups.indexOf(group) < 0){
		if(scriptGroup != null && ""!=scriptGroup.trim() && group != null && "" != group.trim()){
			displayedGroups.push(group);
			$.get('getScriptsList', {group: scriptGroup},function(data) {
				var val = JSON.parse(data);
				var displayHtml = "";
				
				var scriptGroupCount = 0;
				
				for(key in val){
					
					var elem = val[key];
					displayHtml= displayHtml+				
						'<li><span  id="' + elem["moduleName"] + '@' + elem["scriptName"] + '"><a href="#" onclick="editScript(' + "'" + elem["moduleName"] + '@' + 
						elem["scriptName"]+ "'); " +
							"highlightTreeElement(" + "'scriptList_', '0', '" + scriptInstanceTotal + "');" +
							"highlightTreeElement('scriptGroupList_', '" + scriptGroupCount + "', '" + totalScripts + "' );"+
							'return false;">'+elem["scriptName"]+'</a></span></li>';
						++scriptGroupCount;
				}
				var displayClass = ".scripts_"+ group;
				$(displayClass).html(displayHtml);
			});
		}
	}
}
function addScripts() {
	var re = document.getElementById("resultElement");
	var selectable = document.getElementById("selectable");
	var sortable = document.getElementById("sortable");
	var scriptElement = document.getElementById("scriptElement");
	var scriptList = scriptElement.innerHTML;

	if (re.value.length > 0) {
		var array = re.value.split(",");
		for (i = 0; i < array.length; i++) {
			var firstChild = document.getElementById("sortable").firstChild;
			scriptList = scriptList + "," + array[i]
			var lie = document.getElementById(array[i]).innerHTML;
			$("#sortable").append(
					'<li id = "sg' + array[i]
							+ 'end" title = '+lie+'class="ui-state-default">' + lie + '</li>');
			$("#" + array[i]).remove()
		}
		refreshElements();
	} else {
		alert("Please select a script to add");
	}

}

function removeScripts(){
	var re = document.getElementById("sgResultElement");
	var selectable = document.getElementById("selectable");
	var sortable = document.getElementById("sortable");
	var scriptElement = document.getElementById("scriptElement");
	var scriptList = scriptElement.innerHTML;
	if(re.value.length > 0){
	var array = re.value.split(",");
	for(i=0 ; i< array.length;i++){
		var idd = array[i];
		var newId = idd.replace("sg","");
			newId = newId.replace("end","");
		var lie = document.getElementById(idd);
		var data = lie.innerHTML;
		var index = data.lastIndexOf("</div>");
		data = data.substring(index + 6, data.length);
			$("#selectable").append('<li id = "'+newId+'" title = '+data+'class="ui-state-default">' + data + '</li>');
			$("#"+array[i]).remove();
	}
	
		refreshElements();
	}else{
		alert("Please select a script to remove");
	}
	
	
}

function moveUp() {
	var re = document.getElementById("sgResultElement");
	
	if(re.value.length > 0){
		
	var array = re.value.split(",");
	for (i = 0; i < array.length; i++) {
		var idd = array[i];
		var lie = document.getElementById(idd);
		var indx = $( "li[id*='sgscript-']" ).index( lie );
		var prevEl = $( "li[id*='sgscript-']" ).get(indx-1).id
		if (indx == 0){
			var prevEl = $( "li[id*='sgscript-']" ).get($( "li[id*='sgscript-']" ).length -1 ).id
			$("li[id*='"+prevEl+"']").after($("li[id*='"+idd+"']"));
		}else{
			$("li[id*='"+prevEl+"']").before($("li[id*='"+idd+"']"));
		}
	}
	}else{
		alert("Please select a script to move up");
	}
}

function moveDown() {
	var re = document.getElementById("sgResultElement");
	if(re.value.length > 0){
	var array = re.value.split(",");
	for (i = array.length -1 ; i >= 0; i --) {
		var idd = array[i];
		var lie = document.getElementById(idd);
		var indx = $( "li[id*='sgscript-']" ).index( lie );
		var nxtEl = "";
		if ($( "li[id*='sgscript-']" ).length > (indx + 1)){
			nxtEl = $( "li[id*='sgscript-']" ).get(indx+1).id;
			$("li[id*='"+nxtEl+"']").after($("li[id*='"+idd+"']"));
		}else{
			nxtEl = $( "li[id*='sgscript-']" ).get(0).id;
			$("li[id*='"+nxtEl+"']").before($("li[id*='"+idd+"']"));
		}
	}
	}else{
		alert("Please select a script to move down");
	}

}


function refreshElements(){
	
	$( "#selectable" ).selectable({
		 stop: function() {
		 var result = $( "#select-result" ).empty();
		 var data = ""
		 var myArray = [];
		 
		 $( ".ui-selected", this ).each(function() {
		 var index = $( "#selectable li" ).index( this );
		 data = data +"," +(index +1)
		 result.append( " #" + ( index + 1 ) );
		 myArray.push(this.id)
		 });
		 document.getElementById("resultElement").value = myArray;
		 }
		 });

	 $( "#sortable" ).selectable({
		 stop: function() {
		 var result = $( "#select-result" ).empty();
		 var data = ""
		 var myArray = [];
		 
		 $( ".ui-selected", this ).each(function() {
		 var index = $( "#sortable li" ).index( this );
		 data = data +"," +(index +1)
		 result.append( " #" + ( index + 1 ) );
		 myArray.push(this.id)
		 });
		 document.getElementById("sgResultElement").value = myArray;
		 }
		 });
	 
	 document.getElementById("resultElement").value = [];
	 document.getElementById("sgResultElement").value = [];
}

//updateScriptGrp

function updateSG() {
	var sortable = document.getElementById("sortable");

	var dataList = ""
	$( "li[id*='sgscript-']" ).each(function(index) {
		
		var elmnt = $(this).attr('id');
		elmnt = elmnt.replace("sgscript-","");
		
		elmnt = elmnt.replace("end","");
		if(!dataList.contains(","+elmnt+",")){
			dataList = dataList +","+ elmnt;
		}
	});

	var name = document.getElementById("scriptName").value;
	var id = document.getElementById("sgId").value;
	var version = document.getElementById("sgVersion").value;
	
	var name = document.getElementById("scriptName").value;
	if(name == null || name.length == 0 ){
		alert("Please enter script group name ");
	}else if(dataList == "" && dataList.length == 0){
		alert("Please add scripts to the script group");
	}else{
		$.post('updateScriptGrp', {id: id, version:version, idList: dataList, name: name},function(data) {   document.location.reload();  $("#responseDiv123").html(data);  });
	}
}
function createSG() {
	var sortable = document.getElementById("sortable");

	var dataList = ""
	
	$( "li[id*='sgscript-']" ).each(function(index) {
		var elmnt = $(this).attr('id');
		elmnt = elmnt.replace("sgscript-","");
		elmnt = elmnt.replace("end","");
		dataList = dataList +","+ elmnt;
	});

	var name = document.getElementById("scriptName").value;
	if(name == null || name.length == 0 ){
		alert("Please enter script group name ");
	}else if(dataList == "" && dataList.length == 0){
		alert("Please add scripts to the script group");
	}else{ 
		$.get('createScriptGrp', {idList: dataList, name: name},function(data) {   document.location.reload();  $("#responseDiv123").html(data); });
	}
}
function createScriptForm() {
	checkAnyEditingScript();
	$.get('createScript', function(data) { $("#responseDiv").html(data); });
}

function editScript(id , flag ) {
	hideUploadOption();	
	hideSearchoptions();
	checkAnyEditingScript();
	$.get('editScript', {id: id , flag : flag}, function(data) { $("#responseDiv").html(data); });

}

function checkAnyEditingScript(){
	var scriptName = $("#scriptName").val();
	if(scriptName && scriptName != "undefined"){
		clearLock(scriptName);
	}
}


function showScript(idVal, flag) {
	checkAnyEditingScript();
	$.get('editScript', {id: idVal , flag : flag}, function(data) { $("#responseDiv").html(data); });
}

function removeScript(id){	
	checkAnyEditingScript();
	$("#currentScriptId").val("");
	$.get('deleteScript', {id: id}, function(data) { document.location.reload();  });
}

function createScriptGrpForm() {	
	checkAnyEditingScript();
	$.get('create', function(data) { $("#responseDiv").html(data); });
}

function editScriptGroup(id) {
	hideUploadOption();
	hideAllSearchoptions();
	checkAnyEditingScript();
	$.get('edit', {name: id}, function(data) { $("#responseDiv").html(data); });
	$.get('getScriptsList', {group: id}, function(data) { $(id).html(data); });
}

function exportScripts() {
	$.get('exportScriptAsXML', function(data) { alert("Script exporting is done.");});
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


function updateScriptListWithScriptName(scriptName){
	$.get('fetchScriptWithScriptName', {scriptName: scriptName}, function(data) {
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

function showSkipRemarks(me){
	if (me.checked) {
		$("#skipRemarks123").show();
		$("#skipReason123").show();
		$("#remarks").show();
	} else {
		$("#remarks").val('');
		$("#remarks").hide();
		$("#skipRemarks123").hide();
		$("#skipReason123").hide();
	}
	$("#skipReason").val("");
}

function enableEdit(me,scriptName,session){
	
	$("#scriptName").val(scriptName);
	
	$.get('addEditLock', {scriptName: scriptName,session:session}, function(data) {
		if(data){
			if(data == "false"){
				alert("Script is already modifying by another user !!!");
				$("#warningMsg").html("Script is already modifying by another user !!!");
			}
		}
	});
	
	$("#save").show();
	$("#cancel").show();
	$("#editButton").hide();
}

function disableEdit(me,scriptName){
	$.get('removeEditLock', {scriptName: scriptName}, function(data) {
	});
	
}

function clearLock(scriptName){
	$.get('removeEditLock', {scriptName: scriptName}, function(data) {
	});
}

function showSkipRemarksLabel(){
	
	$("#skipRemarks123").hide();
	$("#skipReason123").hide();
}

function sleepIt(milliseconds) {
	  var start = new Date().getTime();
	  for (var i = 0; i < 1e7; i++) {
	    if ((new Date().getTime() - start) > milliseconds){
	      break;
	    }
	  }
	}


function refreshListStart(){
	alert(" Please wait, script list refresh will take some time.");
} 
function scriptRefreshSuccess(){
	alert("The script list refreshed sucessfully.");
	window.location.reload(); 
}
function scriptRefreshFailure(){
	alert(" Error while refreshig the script list.");
	window.location.reload(); 
	
}
