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

import static com.comcast.rdk.Constants.KEY_GROUP

/**
 * A service class for ScriptGroups
 * @author sreejasuma
 *
 */

class ScriptgroupService {

    
    /**
     * Method to save the script to a script group, according to the library chosen for the script
     * Creates two types of script groups.
     * 1: Based on Test group of selected library.
     * 2: Based on the boxType of script.     
     * @param scriptInstance
     * @param boxTypeList
     * @return
     */
    def saveToDefaultGroup(final Script scriptInstance, final List boxTypeList){
       
        String groupName = scriptInstance.primitiveTest.module.testGroup.toString() + KEY_GROUP
		createOrUpdateScriptGroup(scriptInstance, groupName)
		
		boxTypeList.each { boxType ->
			
			BoxType box = BoxType.findById(boxType);
			groupName = box.name + KEY_GROUP
			createOrUpdateScriptGroup(scriptInstance, groupName)
		}
    }
	
	
	/**
	 * Method to create or update script group
	 * If the script group exists then add the script to that group.
	 * Else create a script group and add the script to the group.
	 * @param scriptInstance
	 * @param groupName
	 * @return
	 */
	def createOrUpdateScriptGroup(final Script scriptInstance, final String groupName){

		def scriptGrpInstance = ScriptGroup.findByName(groupName)
		if(!scriptGrpInstance){
			scriptGrpInstance = new ScriptGroup()
			scriptGrpInstance.name = groupName
		}
		scriptGrpInstance.addToScripts(scriptInstance)
		scriptGrpInstance.save(flush:true)
	}
	
	
	/**
	 * Method to remove a particular script from all available box suites.
	 * This method is called during update operation of scripts.
	 * @param scriptInstance
	 * @return
	 */
	def removeScriptsFromBoxSuites(final Script scriptInstance){

		String groupName
		int flag = 0
		def boxTypeList = BoxType.list()
		boxTypeList.each { boxType ->

			groupName = boxType.name + KEY_GROUP
			def scriptGrpInstance = ScriptGroup.findByName(groupName , [lock : true])
			if(scriptGrpInstance){
				scriptGrpInstance.scripts.each { script ->
					if(script.name == scriptInstance.name){
						flag = 1
					}
				}

				if(flag){

					scriptGrpInstance.removeFromScripts(scriptInstance)
				}
			}
		}
	}
	
	
	/**
	 * Method to convert boxType params to list of boxTypes.
	 * @param boxTypes
	 * @return
	 */
	def createBoxTypeList(def boxTypes){

		def boxTypesList = []
		if(boxTypes instanceof String){
			boxTypesList.add(boxTypes)
		}
		else{
			boxTypes.each { boxType ->
				boxTypesList.add(boxType)
			}
		}
		return boxTypesList
	}
    
	
    /**
     * Delete script after checking whether the script is executing on a device
     * or the script is present in a script group which is selected to execute
     */
   
    public boolean checkScriptStatus(final Script script){
        
        boolean scriptInUse = false
        boolean isAllocatedScriptGrp = false
        if(script.status.equals( Status.ALLOCATED.toString() )){
            scriptInUse = true
        }
        else{           
            /**
             * Selecting scriptGroups based on whether selected script exists 
             * in the script group's and status of the ScriptGroup is Allocated. 
             * In this case the script cannot be deleted. 
             */
            def scriptAllocated = ScriptGroup.where {
                scripts { id == script.id } && status == Status.ALLOCATED.toString()
            }          
            scriptAllocated.each{
                isAllocatedScriptGrp = true
                return true                
            }          
            if(isAllocatedScriptGrp){
                scriptInUse = true               
            }
            else{
                /**
                 * Selecting ScriptGroups where the given script is present
                 */
                def scriptGroups = ScriptGroup.where {
                    scripts { id == script.id }
                }
                def scriptInstance
                scriptGroups?.each{ scriptGrp ->
                    scriptInstance = scriptGrp.scripts.find { it.id == script.id }
                    if(scriptInstance){
                        scriptGrp.removeFromScripts(scriptInstance)
                    }
                }
            }                       
        }
        return scriptInUse
    }
 
    /**
     * Get the list of scripts based on the scriptName, primitiveTest and selected box types.
     * @param searchName
     * @param primtest
     * @param selboxTypes
     * @return
     */
    public List getAdvancedSearchResult(final String searchName, final String primtest, final String selboxTypes){
        def scriptList
        def boxTypeObjList = []
        PrimitiveTest ptest
        if((!searchName)){
            if((primtest) && (!selboxTypes)){
                scriptList = Script.findAll("from Script as b where b.primitiveTest='${primtest}'")
            }
            else if((!primtest) && (selboxTypes)){
                boxTypeObjList = getBoxTypes(selboxTypes)
                scriptList = Script.createCriteria().list {
                    boxTypes{
                        'in'('id',boxTypeObjList)
                    }
                }
            }
            else{
                boxTypeObjList = getBoxTypes(selboxTypes)
                ptest = PrimitiveTest.findById(primtest)
                scriptList = Script.createCriteria().list {
                    boxTypes{
                        'in'('id',boxTypeObjList)
                    }
                    eq('primitiveTest', ptest)
                }
            }
        }
        else if((!primtest)){
            if((searchName) && (!selboxTypes)){
                scriptList = Script.findAll("from Script as b where b.name like '%${searchName}%'")
            }
            else if((!searchName) && (selboxTypes)){
                boxTypeObjList = getBoxTypes(selboxTypes)
                scriptList = Script.createCriteria().list {
                    boxTypes{
                        'in'('id',boxTypeObjList)
                    }
                }
            }
            else{
                boxTypeObjList = getBoxTypes(selboxTypes)
                scriptList = Script.createCriteria().list {
                    boxTypes{
                        'in'('id',boxTypeObjList)
                    }
                    ilike("name", "%${searchName}%")
                }
            }
        }
        else if((!selboxTypes)){
            if((searchName) && (!primtest)){
                scriptList = Script.findAll("from Script as b where b.name like '%${searchName}%'")
            }
            else if((!searchName) && (primtest)){
                scriptList = Script.findAll("from Script as b where b.primitiveTest='${primtest}'")
            }
            else{
                scriptList = Script.findAll("from Script as b where b.name like '%${searchName}%' and primitiveTest='${primtest}'")
            }
        }
        else{
            boxTypeObjList = getBoxTypes(selboxTypes)
            ptest = PrimitiveTest.findById(primtest)
            scriptList = Script.createCriteria().list {
                boxTypes{
                    'in'('id',boxTypeObjList)
                }
                eq('primitiveTest', ptest)
                ilike("name", "%${searchName}%")
            }
        }
        scriptList.unique()
        return scriptList
    }  
    
    /**
     * Method to get the id of boxtypes in a list
     * @param selboxTypes
     * @return
     */
    def getBoxTypes(final def selboxTypes){
        def boxTypesList = []
        BoxType bt
        boxTypesList = createBoxTypeList(selboxTypes)
        def boxTypeObjList = []
        boxTypesList.each{
            bt = BoxType.findById(it)
            boxTypeObjList.add( bt?.id )
        }
        return boxTypeObjList
    }
}
