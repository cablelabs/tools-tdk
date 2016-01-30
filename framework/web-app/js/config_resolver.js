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

	$("#browser2").treeview({
		animated:"normal"
	});
	
	$(this).bind("contextmenu", function(e) {
		e.preventDefault();
	});

	$('#addconfId').contextMenu('root_menu_device', {
		bindings : {
			'add_device' : function(node) {
				createDevice();
			},'upload_device':function(node){
				uploadDevice();
			}
		}
	});
	
	$('.file').contextMenu('childs_menu_device', {
		bindings : {
			'edit_device' : function(node) {
				showDevice(node.id);
			},
			'delete_device' : function(node) {
				if (confirm('Are you want to delete this Device?')) {
					deleteDevice(node.id);
				}
			}
		}
	});
	$("#deviceid").addClass("changecolor");
	var decider_id = $("#decider").val();
});

/**
 * Function shows the upload device page option  
 */
function uploadDevice(){
	$("#responseDiv").hide();
	$("#up_load").show();
}
/**
 * function for hide upload device option 
 */
function hideUploadOption(){
	$("#responseDiv").show();
	$("#up_load").hide();
}

function createDevice() {	
	hideUploadOption();
	$.get('createDevice', function(data) { $("#responseDiv").html(data); });
}

function showDevice(id,flag) {
	hideUploadOption();
	$.get('editDevice', {id: id, flag:flag}, function(data) { $("#responseDiv").html(data); });
}


function deleteDevice(id){	
	$.get('deleteDevice', {id: id}, function(data) { document.location.reload(); });
}

function ValidateIPaddress()  
{  
	var inputText = $("#stbIp").val();
	var ipformat = /^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/;  
	if(inputText.match(ipformat))  
	{  	
		return true;  
	}  
	else  
	{  
		alert("You have entered an invalid IP address!");
		$("#stbIp").val("");
		$("#stbIp").focus();
		return false;  
	}  
}  


function ValidateIPaddress1()  
{  
	
	var inputText = $("#systemIP").val();
	var ipformat = /^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/;  
	if(inputText.match(ipformat))  
	{  	
		return true;  
	}  
	else  
	{  
		alert("You have entered an invalid IP address!");
		$("#systemIP").val("");
		$("#systemIP").focus();
		return false;  
	}  
} 




