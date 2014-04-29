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
import java.io.IOException
import com.comcast.rdk.User
import com.comcast.rdk.Role
import com.comcast.rdk.Module
import com.comcast.rdk.BoxType
import com.comcast.rdk.BoxManufacturer
import com.comcast.rdk.socketCommuniation.SocketPortConnector

import org.apache.shiro.crypto.hash.Sha256Hash

class BootStrap {
	
	def grailsApplication

    def primitivetestService
     
    def init = { servletContext ->
				
		File layoutFolder = grailsApplication.parentContext.getResource("//fileStore//filetransfer.py").file
		def absolutePath = layoutFolder.absolutePath

		layoutFolder = grailsApplication.parentContext.getResource("//logs//crashlogs//execId_logdata.txt").file
		def absolutePath1 = layoutFolder.absolutePath

		def user = new User(username: "admin", passwordHash: new Sha256Hash("password").toHex(),
			name : "ADMINISTRATOR", email : "sreejasuma@tataelxsi.co.in")
        user.addToPermissions("*:*")
        user.save(flush:true)
		createRolesAndAssignForAdmin()
		
		def boxManufacturer
		
        def modules = Module.list()
        if(!modules) {
            primitivetestService.parseAndSaveStubXml()
        }

        def boxTypes = BoxType.list()
        if(!boxTypes){
            primitivetestService.parseAndSaveBoxTypes()
        }
        
       int port = Integer.parseInt("8089")
        try
        {
           Thread t = new SocketPortConnector(port,absolutePath.toString(),absolutePath1.toString())
           t.start()
        }catch(IOException e)
        {
           e.printStackTrace()
        }   
    }
    
    def destroy = {        
		SocketPortConnector.closeServerSocket()
    }
	
	def createRolesAndAssignForAdmin()
	{
		def permDeviceGroup = "DeviceGroup:*:*"
		def permScriptGroup = "ScriptGroup:*:*"
		def permExecution = "Execution:*:*"
		def permRecorder = "Recorder:*:*"
		def permPrimitiveTest = "PrimitiveTest:*:*"
		def permModule = "Module:*:*"
		def permStreamingDetails = "StreamingDetails:*:*"
		
		def adminRole = Role.findByName("ADMIN")
		if(!adminRole)
		{
			def adminUser  = User.findByUsername("admin")
			adminRole = new Role(name: "ADMIN")
			adminRole.addToPermissions("*:*")
			adminRole.save(flush:true)
		   
			if(adminUser){
				adminUser.addToRoles(adminRole)
			}
		}
		Role testerRole = Role.findByName("TESTER")
		if(!testerRole)
		{
			testerRole = new Role(name: "TESTER")
			testerRole.addToPermissions(permDeviceGroup)
			testerRole.addToPermissions(permScriptGroup)
			testerRole.addToPermissions(permExecution)
			testerRole.addToPermissions(permRecorder)
			testerRole.addToPermissions(permPrimitiveTest)
			testerRole.addToPermissions(permModule)
			testerRole.addToPermissions(permStreamingDetails)
			
			testerRole.save(flush:true)
		}else{
			if(testerRole.permissions){
				
				if(!testerRole.permissions.contains(permDeviceGroup)){
					testerRole.addToPermissions(permDeviceGroup)
				}
				
				if(!testerRole.permissions.contains(permScriptGroup)){
					testerRole.addToPermissions(permScriptGroup)
				}
				
				if(!testerRole.permissions.contains(permExecution)){
					testerRole.addToPermissions(permExecution)
				}
				
				if(!testerRole.permissions.contains(permRecorder)){
					testerRole.addToPermissions(permRecorder)
				}
	
				if(!testerRole.permissions.contains(permPrimitiveTest)){
					testerRole.addToPermissions(permPrimitiveTest)
				}
				
				if(!testerRole.permissions.contains(permModule)){
					testerRole.addToPermissions(permModule)
				}
				
				if(!testerRole.permissions.contains(permStreamingDetails)){
					testerRole.addToPermissions(permStreamingDetails)
				}
				
			
				testerRole.save(flush:true)
			}
		}		
	}

}

              