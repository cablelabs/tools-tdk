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

import org.springframework.dao.DataIntegrityViolationException
/**
 * Controller class for streaming details operations
 * @author sreejasuma
 *
 */
class StreamingDetailsController {

	def utilityService
	
    static allowedMethods = [save: "POST", update: "POST", delete: "POST"]

    def index() {
        redirect(action: "list", params: params)
    }

    /**
     * List stream details
     * @return
     */
    def list() {    
		def streamingDetailsList = StreamingDetails.findAllByGroupsOrGroupsIsNull(utilityService.getGroup())   
		def radioStreamingDetailsList = RadioStreamingDetails.findAllByGroupsOrGroupsIsNull(utilityService.getGroup())
        [streamingDetailsInstanceList: streamingDetailsList,radioStreamingDetails: radioStreamingDetailsList,streamingDetailsInstanceTotal: streamingDetailsList.size(),radioStreamingDetailsInstanceTotal: radioStreamingDetailsList.size()]
    }

    /**
     * Create stream details
     * @return
     */
    def create() {
        [streamingDetailsInstance: new StreamingDetails(params)]
    }
	
	def createRadio() {
		[streamingDetailsInstance: new RadioStreamingDetails(params)]
	}

    /**
     * Save stream details
     * @return
     */
    def save() {
        def streamingDetailsInstance = new StreamingDetails(params)
		streamingDetailsInstance.groups = utilityService.getGroup()
        if (!streamingDetailsInstance.save(flush: true)) {
          // render(view: "create", model: [streamingDetailsInstance: streamingDetailsInstance])
            redirect(action: "list")
            return
        }

        flash.message = message(code: 'default.created.message', args: [message(code: 'streamingDetails.label', default: 'StreamingDetails'), streamingDetailsInstance.streamId])
        redirect(action: "list")
    }
	
	def saveRadio() {
		def streamingDetailsInstance = new RadioStreamingDetails(params)
		if(params?.streamId?.startsWith("R")){
		streamingDetailsInstance.groups = utilityService.getGroup()
		if (!streamingDetailsInstance.save(flush: true)) {
		  // render(view: "create", model: [streamingDetailsInstance: streamingDetailsInstance])
			redirect(action: "list")
			return
		}

		flash.message = message(code: 'default.created.message', args: [message(code: 'streamingDetails.label', default: 'StreamingDetails'), streamingDetailsInstance.streamId])
		}else{
		flash.message = "Stream id should start with R"
		
		}
		redirect(action: "list")
	}

    /**
     * Show stream details
     * @return
     */
    def show(Long id) {
        def streamingDetailsInstance = StreamingDetails.get(id)
        if (!streamingDetailsInstance) {
            flash.message = message(code: 'default.not.found.message', args: [message(code: 'streamingDetails.label', default: 'StreamingDetails'), streamingDetailsInstance.streamId])
            redirect(action: "list")
            return
        }

        [streamingDetailsInstance: streamingDetailsInstance]
    }

    /**
     * Edit stream details
     * @return
     */
    def edit(Long id) {
        def streamingDetailsInstance = StreamingDetails.get(id)
        if (!streamingDetailsInstance) {
            flash.message = message(code: 'default.not.found.message', args: [message(code: 'streamingDetails.label', default: 'StreamingDetails'), streamingDetailsInstance.streamId])
            redirect(action: "list")
            return
        }

        [streamingDetailsInstance: streamingDetailsInstance]
    }
	
	def editRadio(Long id) {
		def streamingDetailsInstance = RadioStreamingDetails.get(id)
		if (!streamingDetailsInstance) {
			flash.message = message(code: 'default.not.found.message', args: [message(code: 'streamingDetails.label', default: 'StreamingDetails'), streamingDetailsInstance.streamId])
			redirect(action: "list")
			return
		}
		[streamingDetailsInstance: streamingDetailsInstance]
	}

    /**
     * Update stream details
     * @return
     */
    def update(Long id, Long version) {
        def streamingDetailsInstance = StreamingDetails.get(id)
        if (!streamingDetailsInstance) {
            flash.message = message(code: 'default.not.found.message', args: [message(code: 'streamingDetails.label', default: 'StreamingDetails'), streamingDetailsInstance.streamId])
            redirect(action: "list")
            return
        }

        if (version != null) {
            if (streamingDetailsInstance.version > version) {
                streamingDetailsInstance.errors.rejectValue("version", "default.optimistic.locking.failure",
                          [message(code: 'streamingDetails.label', default: 'StreamingDetails')] as Object[],
                          "Another user has updated this StreamingDetails while you were editing")
                //render(view: "edit", model: [streamingDetailsInstance: streamingDetailsInstance])
                redirect(action: "list")
                return
            }
        }

        streamingDetailsInstance.properties = params

        if (!streamingDetailsInstance.save(flush: true)) {
           // render(view: "edit", model: [streamingDetailsInstance: streamingDetailsInstance])
            redirect(action: "list")
            return
        }

        flash.message = message(code: 'default.updated.message', args: [message(code: 'streamingDetails.label', default: 'StreamingDetails'), streamingDetailsInstance.streamId])
        redirect(action: "list")
    }
	/**
	 * update the radio stream details 
	 * @param id
	 * @param version
	 * @return
	 */
	 def updateRadio(Long id,Long version)
	  {
			def radioStreamingDetailsInstance= RadioStreamingDetails.get(id)
			if(!radioStreamingDetailsInstance){
				flash.message = message(code: 'default.not.found.message', args: [message(code: 'radioStreamingDetails.label', default: 'RadioStreamingDetails'), radioStreamingDetailsInstance.streamId])
				redirect(action: "list")
				return
			}
			
			if(version != null )
			{
				if(radioStreamingDetailsInstance.version > version){
					radioStreamingDetailsInstance.errors.rejectValue("version", "default.optimistic.locking.failure",
						[message(code: 'radioStreamingDetails.label', default: 'RadioStreamingDetails')] as Object[],
						"Another user has updated this RadioStreamingDetails while you were editing")
							//render(view: "edit", model: [streamingDetailsInstance: streamingDetailsInstance])
			  redirect(action: "list")
			  return
			}
			radioStreamingDetailsInstance.properties = params
			if (!radioStreamingDetailsInstance.save(flush: true)) {
				// render(view: "edit", model: [streamingDetailsInstance: streamingDetailsInstance])
				 redirect(action: "list")
				 return
			 }
	 
			 flash.message = message(code: 'default.updated.message', args: [message(code: 'radioStreamingDetails.label', default: 'RadioStreamingDetails'),radioStreamingDetailsInstance.streamId])
			 redirect(action: "list")
			}
	
	  }
	 

    /**
     * Delete stream details
     * @return
     */
    def delete(Long id) {
        def streamingDetailsInstance = StreamingDetails.get(id)
        if (!streamingDetailsInstance) {
            flash.message = message(code: 'default.not.found.message', args: [message(code: 'streamingDetails.label', default: 'StreamingDetails'), streamingDetailsInstance.streamId])
            redirect(action: "list")
            return
        }

        try {
            streamingDetailsInstance.delete(flush: true)
            flash.message = message(code: 'default.deleted.message', args: [message(code: 'streamingDetails.label', default: 'StreamingDetails'), streamingDetailsInstance.streamId])
            redirect(action: "list")
        }
        catch (DataIntegrityViolationException e) {
            flash.message = message(code: 'default.not.deleted.message', args: [message(code: 'streamingDetails.label', default: 'StreamingDetails'), streamingDetailsInstance.streamId])
            redirect(action: "list")
        }
    }
    
    /**
     * Delete stream details
     * @return
     */
    def deleteStreamDetails() {
      Long id = params.id as Long
      def streamingDetailsInstance = StreamingDetails.get(id)
        if (!streamingDetailsInstance) {
            flash.message = message(code: 'default.not.found.message', args: [message(code: 'streamingDetails.label', default: 'StreamingDetails'), streamingDetailsInstance.streamId])
            redirect(action: "list")
            return
        }

        try {
            streamingDetailsInstance.delete(flush: true)
            flash.message = message(code: 'default.deleted.message', args: [message(code: 'streamingDetails.label', default: 'StreamingDetails'), streamingDetailsInstance.streamId])
            redirect(action: "list")
        }
        catch (DataIntegrityViolationException e) {
            flash.message = message(code: 'default.not.deleted.message', args: [message(code: 'streamingDetails.label', default: 'StreamingDetails'), streamingDetailsInstance.streamId])
            redirect(action: "list")
        }
    }
	
	def deleteRadioStreamDetails() {
		Long id = params.id as Long
		def radioStreamingDetailsInstance = RadioStreamingDetails.get(id)
		  if (!radioStreamingDetailsInstance) {
			  flash.message = message(code: 'default.not.found.message', args: [message(code: 'radioStreamingDetails.label', default: 'RadioStreamingDetails'), radioStreamingDetailsInstance.streamId])
			  redirect(action: "list")
			  return
		  }
  
		  try {
			  radioStreamingDetailsInstance.delete(flush: true)
			  flash.message = message(code: 'default.deleted.message', args: [message(code: 'radioStreamingDetails.label', default: 'RadioStreamingDetails'), radioStreamingDetailsInstance.streamId])
			  redirect(action: "list")
		  }
		  catch (DataIntegrityViolationException e) {
			  flash.message = message(code: 'default.not.deleted.message', args: [message(code: 'radioStreamingDetails.label', default: 'RadioStreamingDetails'), radioStreamingDetailsInstance.streamId])
			  redirect(action: "list")
		  }
	  }
    
   
}
