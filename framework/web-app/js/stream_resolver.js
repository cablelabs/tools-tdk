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
	
	$("#streambrowser").treeview({
		animated:"normal",
		persist: "cookie"
		
	});
	
	$(this).bind("contextmenu", function(e) {
		e.preventDefault();
	});

	$('.folder').contextMenu('root_menu', {
		bindings : {
			'add_property' : function(node) {
				createStreamDetailsForm();
			}
		}
	});
	
	
	$('.file').contextMenu('childs_menu', {
		bindings : {
			'edit_test' : function(node) {
				showStreamDetails(node.id);
			},
			'delete_test' : function(node) {
				if (confirm('Are you want to delete property?')) {
					removeProperty(node.id);
				}
			}
		}
	});
	
	
});

function createStreamDetailsForm() {
	$.get('create', function(data) { $("#responseDiv").html(data); });
}


function showStreamDetails(id) {
	$.get('edit', {id: id}, function(data) { $("#responseDiv").html(data); });
}


function removeProperty(id){
	$.get('deleteStreamDetails', {id: id}, function(data) { document.location.reload(); });
}













