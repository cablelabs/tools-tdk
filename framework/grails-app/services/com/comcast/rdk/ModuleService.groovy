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
 * Service class for Module related operations
 * 
 *
 */
class ModuleService {


    /**
     * Deletes functions of the given module
     * @param moduleInstance      
     *      
     **/
    def deleteFunctionandParameters(final Module moduleInstance, def applnPath){
        def functionInstance = Function.findAllByModule(moduleInstance)
        functionInstance.each{ fnInstance ->
            deleteParameters(fnInstance)
            fnInstance.delete(flush: true)
        }

        //TODO In appln we need to move to dynamic file separator
        def fileSeparator=System.getProperty("file.separator")

        //Deletes the component folder and its contents
        def path=applnPath+fileSeparator+"fileStore"+fileSeparator+"testscripts"+fileSeparator+"component"+fileSeparator+moduleInstance.name
        deleteModuleFiles(path, moduleInstance.name)

        //Delete integration folder and its contents
        path=applnPath+fileSeparator+"fileStore"+fileSeparator+"testscripts"+fileSeparator+"integration"+fileSeparator+moduleInstance.name
        deleteModuleFiles(path, moduleInstance.name)

    }

    /**
     * Deletes parameters of the given function
     * @param function
     * @return
     */
    def deleteParameters(final Function function){
        def parameterList = ParameterType.findAllByFunction(function)
        parameterList?.each { parameters ->
            try{
                def parameterInstanceList = Parameter.findByParameterType(parameters)
                parameterInstanceList?.each { parameterType ->
                    parameterType.delete()
                }
                parameters.delete()
            }
            catch(Exception ex){
//                log.error(parameters.errors)
            }
        }
    }


    /**
     * Deletes the script files and entries for primitive test 
     * @param scriptPath Absolute path to script directory
     * @param module Module name
     * 
     */
    def deleteModuleFiles(def scriptPath, def moduleName){

        def  scriptDir=  new File( scriptPath)
        if (scriptDir && scriptDir.exists()){
            for (File script : scriptDir.listFiles()){
                script.delete()
            }
            scriptDir.delete()

            def primitiveTests=  PrimitiveService.primitiveMap.get(moduleName)
            primitiveTests.each{ pTest->
                //Removes primitive test for the module
                PrimitiveService.primitiveList.remove( pTest )
                //Removes primitive test & module entry
                PrimitiveService.primitiveModuleMap.remove( pTest )
            }
            //Removes module and primitive tests entry
            PrimitiveService.primitiveMap.remove( moduleName )
        }
    }
}
