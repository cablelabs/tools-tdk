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
package com.comcast.rdk;

import static com.comcast.rdk.Constants.PYTHON_COMMAND
import java.util.concurrent.ExecutorService
import java.util.concurrent.Executors
import java.util.concurrent.Future

import javax.servlet.http.HttpServletRequest;

import org.codehaus.groovy.grails.validation.routines.InetAddressValidator

public class DeviceStatusUpdater {

	static final int THREAD_COUNT = 20;

	/**
	 * Executer service for handling the device status update process.
	 * Currently 10 threads are assigned for this.
	 */
	static ExecutorService executorService = Executors.newFixedThreadPool(THREAD_COUNT)

	/**
	 * Method to trigger the device status update.
	 * @param grailsApplication
	 * @param deviceStatusService
	 */
	public static void updateDeviceStatus(def grailsApplication,def deviceStatusService,def executescriptService){
		File layoutFolder = grailsApplication.parentContext.getResource("//fileStore//calldevicestatus_cmndline.py").file
		def absolutePath = layoutFolder.absolutePath
		def deviceStatus
		def deviceId
		String filePath = absolutePath//"${RequestContextHolder.currentRequestAttributes().currentRequest.getRealPath("/")}//fileStore//calldevicestatus_cmndline.py"
		def deviceList = Device.list()
		//def deviceList1 = Device.list()
		//	def deviceInstance
		def ipAddress
		NetworkInterface nface
		Enumeration ne = NetworkInterface.getNetworkInterfaces();
		while (ne.hasMoreElements()) {
			NetworkInterface netFace = (NetworkInterface) ne.nextElement();
			Enumeration ae = netFace.getInetAddresses();
			while (ae.hasMoreElements()) {
				InetAddress address = (InetAddress) ae.nextElement();
				if(InetAddressValidator.getInstance().isValidInet4Address(address.getHostAddress())){
					if(!address.isLoopbackAddress()){
						ipAddress = address.getHostAddress()
					}
				}
			}
		}
		List childDeviceList = []
		deviceList?.each{ device ->
			int port = Integer.parseInt(device?.statusPort)
			String[] cmd = [
				PYTHON_COMMAND,
				filePath,
				device?.stbIp,
				port,
				ipAddress,
				device?.stbName
			]
			Runnable statusUpdator = new StatusUpdaterTask(cmd, device, deviceStatusService,executescriptService,grailsApplication);
			executorService.execute(statusUpdator);
		}
	}

	public static String fetchDeviceStatus(def grailsApplication,Device device){

		File layoutFolder = grailsApplication.parentContext.getResource("//fileStore//calldevicestatus_cmndline.py").file

		def absolutePath = layoutFolder.absolutePath

		def deviceStatus

		def deviceId

		String filePath = absolutePath//"${RequestContextHolder.currentRequestAttributes().currentRequest.getRealPath("/")}//fileStore//calldevicestatus_cmndline.py"

		def ipAddress

		NetworkInterface nface

		Enumeration ne = NetworkInterface.getNetworkInterfaces();

		while (ne.hasMoreElements()) {

			NetworkInterface netFace = (NetworkInterface) ne.nextElement();

			Enumeration ae = netFace.getInetAddresses();

			while (ae.hasMoreElements()) {

				InetAddress address = (InetAddress) ae.nextElement();

				if(InetAddressValidator.getInstance().isValidInet4Address(address.getHostAddress())){

					if(!address.isLoopbackAddress()){

						ipAddress = address.getHostAddress()

					}

				}

			}

		}

		int port = Integer.parseInt(device?.statusPort)

		String[] cmd = [
			"python",
			filePath,
			device?.stbIp,
			port,
			ipAddress,
			device?.stbName
		]

		String outData = ""
		
		try {
			outData =  new ScriptExecutor().executeScript(cmd,1)

			if(outData != null){

				outData = outData.trim()

			}
		} catch (Exception e) {
			e.printStackTrace()
		}

		return outData;

	}
}

