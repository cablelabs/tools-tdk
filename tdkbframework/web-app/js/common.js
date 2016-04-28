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

/**
 * Function to highlight selected tree node.
 * @param componentId
 * @param currentId
 * @param treeElementCount
 */
function highlightTreeElement(componentId, currentId, treeElementCount){
	
	for ( var i = 1; i <= treeElementCount; i++) {
		
		$('#'+componentId+i).css('background-color','')
	}
    $('#'+componentId+currentId).css('background-color','#FAE2D2')
    
    if(componentId == "deviceExecutionList_"){
			updateSelectedDeviceId(currentId);
	}
}

/**
 * Function to cache previously selected device id.
 * This is needed for tree element highlight during device refresh.
 * @param selectedId
 */
function updateSelectedDeviceId(selectedId){
	
	$("#selectedDevice").val(selectedId);
}