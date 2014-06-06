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
	
	$("#primitveTestbrowser").treeview({
		animated:"normal",
		persist: "cookie"
		
	});
	
	$(this).bind("contextmenu", function(e) {
		e.preventDefault();
	});

	$('.folder').contextMenu('root_menu', {
		bindings : {
			'add_property' : function(node) {
				createTestForm();
			}
		}
	});
	
	
	$('.file').contextMenu('childs_menu', {
		bindings : {
			'edit_test' : function(node) {
				makeTestEditable(node.id);
			},
			'delete_test' : function(node) {
				if (confirm('Are you want to delete property?')) {
					removeProperty(node.id);
				}
			}
		}
	});
	
	$("#module").live('change', function(){
		var module_id = $(this).val();
		if(module_id != '') {
			getAssociatedFunctions(module_id);
		}
		else {
			$("#functionTd").html('<select style="width: 250px"><option value="">Please Select</option></select>');
		}
		$("#parameterTable").html('');
		$("#buttons").hide();
	});
	$("#primid").addClass("changecolor");
	var decider_id = $("#decider").val();
});

function createTestForm() {
	$.get('template', function(data) { $("#responseDiv").html(data); });
}

function createConfigForm() {
	$.get('confTemplate', function(data) { 
		$("#responseDiv").html(data); });
}

function getAssociatedFunctions(module_id) {
	if(module_id != '') {
		$.get('getFunctions', {moduleId: module_id}, function(data) {
			var select = '<select style="width: 250px" id="functionValue" name="functionValue" onchange="getAssociatedParameters()"><option value="">Please Select</option>';
			
			for(var index = 0; index < data.length; index ++ ) {
				select += '<option value="' + data[index].id + '">' + data[index].name + '</option>';
			}
			
			select += '</select>';
			
			$("#functionTd").html(''); 
			$("#functionTd").html(select); 
		});
	}
	else {
		$("#functionTd").html('');
		$("#buttons").hide();
		$("#tableheader").hide();
	}
}

function getAssociatedParameters() {
	var function_id = $("#functionValue").val();
	if(function_id != '') {
		$.get('getParameters', {functionId: function_id}, function(data) {
			var parameter = '';
			var ids = '';
			for(var index = 0; index < data.length; index ++ ) {
				if(index == 0) {
					parameter += '<tr><th>Parameter Name</th><th>Type</th><th>Range</th><th>Value</th></tr>';
				}
				parameter += '<tr><td align="left">&emsp;&emsp;' + data[index].name + '</td><td>' + data[index].type + 
				'</td><td>' + data[index].range + '</td><td align="center"><input type="text" name="value_' + data[index].id + '"></td></tr>';
				ids += data[index].id + ', ';
			}			
			$("#parameterTable").html(''); 
			$("#parameterTable").html(parameter);
			$("#parameterTypeIds").val(ids);
			$("#buttons").show();
			$("#tableheader").show();
		});
	}
	else {
		$("#parameterTable").html('');
		$("#buttons").hide();
		$("#tableheader").hide();
	}
}

function makeTestEditable(id) {
	$.get('getEditableTest', {id: id}, function(data) { $("#responseDiv").html(data); });
}

function makeConfEditable(id) {	
	$.get('getEditableTest', {id: id}, function(data) { 
		alert("callin ..... makeConfEditable");
		$("#responseDiv").html(data); });
}

function removeProperty(id){
	$.get('deleteTest', {id: id}, function(data) { document.location.reload(); });
}



/**
 * Function to check whether primitive test is saved or not.
 */
function updateTestList(testName){
	
	$.get('fetchPrimitiveTest', {testName: testName}, function(data) {
		if(data!=""){
			if($("#isTestExist").val()==""){
				$("#currentPrimitiveTestId").val(data);
				//setTimeout(function(){location.reload();makeTestEditable(data);},1000);
				location.reload();
			}
			$("#isTestExist").val("");
		}
		$("#testMessageDiv").show();
	});
}

/**
 * Function to check whether primitive test with same name exist or not.
 * @param testName
 */
function isTestExist(testName){
	
	$.get('fetchPrimitiveTest', {testName: testName}, function(data) {
		if(data!=""){
			$("#isTestExist").val(data);
		}
		$("#testMessageDiv").show();
	});
}


function clearValues(){
	$("#parameterTable").html('');
	$("#buttons").hide();
	$("#tableheader").hide();
}








