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

import java.io.OutputStream;
import java.util.List;
import java.util.Map;

import de.andreasschmitt.export.builder.ExcelBuilder
import de.andreasschmitt.export.exporter.Exporter
import de.andreasschmitt.export.exporter.ExportingException

/**
 * Service to export the excel report.
 *
 */
class ExcelExportService {

	def serviceMethod() {
	}
	
	public void export(String type, OutputStream outputStream, Map dataMap, List fields, Map labels, Map formatters, Map parameters) throws ExportingException {
		ExcelExporter exporter = new ExcelExporter()
//		if(fields){
//			exporter.setExportFields(fields)
//		}
//
		if(labels){
			exporter.setLabels(labels)
		}
//
//		if(formatters){
//			exporter.setFormatters(formatters)
//		}
//
		if(parameters){
			exporter.setParameters(parameters)
		}

		exporter.exportData(outputStream, dataMap)
	}
}
