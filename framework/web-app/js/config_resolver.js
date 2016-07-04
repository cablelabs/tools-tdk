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
				createDevice("RDKV");
			},
			'add_deviceB' : function(node) {
				createDevice("RDKB");
			},
			'upload_device':function(node){
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

function upload(){
	var gateway = document.getElementById('stbName').value;
	var ip = document.getElementById('stbIp').value;
	if((gateway != null) && (ip != null)){
		gateway = gateway.trim();
		ip = ip.trim();
		if((gateway !== '') && (ip !== '')){
			var elem = new FormData(document.forms.namedItem('tclForm'));
			elem.append('gatewayName', gateway);
			elem.append('ip', ip);
			 var url="uploadTclConfiguration";
		     $.ajax({
		         url:url,
		         type:'POST',
		         data:elem,
		         processData: false,  // tell jQuery not to process the data
		         contentType: false ,
		         success:function (response) {
		        	 if(response !== 'Upload failed'){
		        		 $('#uploadForm').hide();
		        		 $('#uploadStatus').text(response).css({'color':'green'});
		        	 }
		        	 else{
		        		 $('#uploadStatus').text(response).css({'color':'red'});
		        	 }
		            }
		         });
		}
		else{
			alert('Gateway Name and ip are mandatory');
		}
	}
	else{
		alert('Gateway Name and ip are mandatory');
	}
	
}


/**
 * function for hide upload device option 
 */
function hideUploadOption(){
	$("#responseDiv").show();
	$("#up_load").hide();
}

function createDevice(category) {
	hideUploadOption();
	$.get('createDevice',{category:category}, function(data) { $("#responseDiv").html(data); });
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




