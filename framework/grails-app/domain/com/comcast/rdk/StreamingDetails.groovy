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
package com.comcast.rdk

/**
 * Domain class which holds the streaming details
 * @author sreejasuma
 *
 */

class StreamingDetails {

    /**
     * Stream Id
     */
    String streamId
	
    /**
     * Channel Type : The channel is either HD or SD
     */
    ChannelType channelType

    /**
     * Audio Format : Either ac3/mp3/wav/aac
     */
    AudioFormat audioFormat

    /**
     * Video Format : Either mpeg2/mpeg4/h.264
     */
    VideoFormat videoFormat

	/**
	 * Indicates the group name which the device belongs
	 */
	Groups groups
	
    static constraints = {
        streamId(nullable:false, blank:false, maxSize:64, unique:true)   
        channelType(nullable:false, blank:false)
        audioFormat(nullable:false, blank:false)
        videoFormat(nullable:false, blank:false)
		groups(nullable:true, blank:true)
    }
    
    
    @Override
    String toString() {
        return streamId ?: 'NULL'
    }

	static mapping = {
		datasource 'ALL'
	}
}
