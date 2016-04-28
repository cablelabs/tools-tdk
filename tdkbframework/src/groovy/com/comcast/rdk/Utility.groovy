package com.comcast.rdk

import org.springframework.util.StringUtils;
import static com.comcast.rdk.Constants.*;

import com.comcast.rdk.Category

public class Utility{

	public static Category getCategory(def category){
		if(StringUtils.hasText(category)){
			return Category.valueOf(category)
		}
		return null
	}

	public static void writeContentToFile(String content, String fileName){
		BufferedWriter writer = new BufferedWriter(new FileWriter(new File(fileName)))
		writer.write(content)
		writer.close()
	}

	public static String getTclDir(final String realPath) {
		return realPath + FILE_SEPARATOR +  "fileStore" + FILE_SEPARATOR + FileStorePath.RDKTCL.value();
	}

	public static String getFileStorePath(final String realPath, final Category category){
		String path = realPath + FILE_SEPARATOR + 'fileStore' + FILE_SEPARATOR
		switch(category){
			case Category.RDKB: path = path + FileStorePath.RDKB.value()
				break
			case Category.RDKV : path = path + FileStorePath.RDKV.value()
				break
			case Category.RDKB_TCL : path = path + FileStorePath.RDKTCL.value()
				break
			default:break
		}
		return path
	}
	
	/**
	 * Method evaluates whether the text returned from tcl execution represents failure
	 * 
	 * @param htmlData
	 * @return
	 */
	public static boolean isFail(String htmlData){
		return (htmlData.contains('Test Result : FAILED') ||  !htmlData.contains('Test Result :'))
	}
	
	/***
	 * Checks whether tcl file exists in filestore
	 * 
	 * @param realPath
	 * @param fileName
	 * @return
	 */
	public static boolean isTclScriptExists(String realPath, String fileName){
		def isExists = false
		def tcl = getTclFilePath(realPath, fileName)
		if(tcl){
			isExists = true
		}
		return isExists
	}
	
	
	/***
	 * Gets the tcl file absolute path from filestore
	 * 
	 * @author deepesh.mohan
	 *
	 */
	public static String getTclFilePath(String realPath, String fileName){
		def filePath = realPath + FILE_SEPARATOR +  "fileStore" + FILE_SEPARATOR + FileStorePath.RDKTCL.value()
		File[] tcl = new File(filePath).listFiles(new FileFilter(){
					boolean accept(File file) {
						file.name.endsWith(fileName+".tcl")
					};
				})
		if(tcl?.length == 1){
			return tcl[0]?.absolutePath
		}
		return null
	}
	
	
	/**
	 * Returns the tcl scripts path in filestore
	 * 
	 * @param realPath
	 * @return
	 */
	public static String  getTclDirectory(String realPath) {
		return realPath + FILE_SEPARATOR +  "fileStore" + FILE_SEPARATOR + FileStorePath.RDKTCL.value()
	}

	/**
	 * Checks whether the COnfiguration file for tcl execution exists in filestore
	 * 
	 * @author deepesh.mohan
	 *
	 */
	public static boolean isConfigFileExists(def realPath, def deviceName){
		def isExists = false
		def filePath = realPath + FILE_SEPARATOR +  "fileStore" + FILE_SEPARATOR + FileStorePath.RDKTCL.value()
		File[] tcl = new File(filePath).listFiles(new FileFilter(){
					boolean accept(File file) {
						file.name.endsWith(deviceName+".txt")
					};
				})
		if(tcl.length == 1){
			isExists = true
		}
		return isExists
	}
	
	/***
	 * Returns config file path from tcl filestore
	 * @author deepesh.mohan
	 *
	 */
	public static String getConfigFilePath(String realPath, String deviceName){
		def filePath = realPath + FILE_SEPARATOR +  "fileStore" + FILE_SEPARATOR + FileStorePath.RDKTCL.value()
		File[] tcl = new File(filePath).listFiles(new FileFilter(){
					boolean accept(File file) {
						file.name.endsWith(deviceName+".txt")
					};
				})
		if(tcl.length == 1){
			return tcl[0]?.absolutePath
		}
		return null
	}
	
	
	public static String getModuleParentDirectory(TestGroup testgroup){
		def dir = null
		if(testgroup){
			switch(testgroup){
				case TestGroup.E2E : dir = Constants.INTEGRATION
					break
				case TestGroup.Component : dir = Constants.COMPONENT
					break
				/*
				 *  not implemented
				 case TestGroup.OpenSource : dir = Constants.COMPONENT
				 break*/
				default : dir = null
					break
			}
		}
		return dir
	}
}