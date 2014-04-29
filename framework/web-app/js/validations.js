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
	
	$(".checkbox").each(function() {
		this.checked = false;
	});

});

var count = 0;
function checkBoxClicked(that) {
	if(that.checked){
		count ++;
		document.getElementById("delete").disabled=false;
	}
	else {
		count --;
	}
	if(count <=0){
		document.getElementById("delete").disabled=true;
	}
}

function populateBoxManufacturerField(that){
	$.get('getBoxManufacturer', {id:that.id}, function(data) {		
		document.getElementById("boxManufacturerId").value = that.id;
		document.getElementById("name").value = data[0];
		$("#updateBtn").show(); 
		$("#resetBtn").show(); 
		$("#createBtn").hide(); 
	});
}

function populateSoCVendorField(that){
	$.get('getSoCVendor', {id:that.id}, function(data) {		
		document.getElementById("soCVendorId").value = that.id;
		document.getElementById("name").value = data[0];
		$("#updateBtn").show(); 
		$("#resetBtn").show(); 
		$("#createBtn").hide(); 
	});
}

function populateGroupField(that){

	$.get('getGroup', {id:that.id}, function(data) {		
		alert(data[0]);
		document.getElementById("groupId").value = that.id;
		document.getElementById("name").value = data[0];
		$("#updateBtn").show(); 
		$("#resetBtn").show(); 
		$("#createBtn").hide(); 
	});
}

function onResetClick(){
	$("#updateBtn").hide(); 
	$("#resetBtn").show(); 
	$("#createBtn").show(); 
}

function populateFieldVals(id){
	$.get('populateFields', {id: id}, function(data) {
		$("#userId").val(data[0]); 
		document.getElementById("passwordId").value = "";
		document.getElementById("nameOfUser").value = data[1];
		document.getElementById("email").value = data[2];
		document.getElementById("userName1").value = data[3];
		/*document.getElementById("groupName").value = data[4];*/
		$('#groupName option[value="'+data[4]+'"]"').attr("selected", "selected");		
		if(data[5] == "null"){
		}
		else{
			document.getElementById("passwordId").value = data[5];
		}		
		$('#roleid option[value="'+data[6]+'"]"').attr("selected", "selected");	
		$("#updateBtn").show(); 
		$("#resetBtn").show(); 
		$("#createBtn").hide(); 
	});		
}
	