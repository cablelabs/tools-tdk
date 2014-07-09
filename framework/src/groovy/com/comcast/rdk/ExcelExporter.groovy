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
import de.andreasschmitt.export.exporter.AbstractExporter
import de.andreasschmitt.export.exporter.Exporter;
import de.andreasschmitt.export.exporter.ExportingException;

/**
 * Exporter for excel exporting of consolidated report.
 *
 */
class ExcelExporter extends AbstractExporter {

	@Override
	protected void exportData(OutputStream outputStream, List data, List fields)
	throws ExportingException {
		// TODO Auto-generated method stub

	}

	def exportData(OutputStream outputStream, Map dataMap){
		try {
			def builder = new ExcelBuilder()

			// Enable/Disable header output
			boolean isHeaderEnabled = true
			if(getParameters().containsKey("header.enabled")){
				isHeaderEnabled = getParameters().get("header.enabled")
			}


			def sheetsList = dataMap.keySet()
			
			builder {
				workbook(outputStream: outputStream){
					sheetsList.each { sheetName ->
						if(sheetName.equals("CoverPage")){
							Map coverPageMap = dataMap.get(sheetName)
							List columnWidthList = [0.05,0.05,0.05,0.05,0.08,0.4,0.15,0.2,0.2,0.2,0.2]
							sheet(name: "Summary" ?: "Export", widths: columnWidthList){
								int rowIndex = 0
								//Default format
								format(name: "header"){
									font(name: "arial", bold: true)
								}

								format(name: "titlecell"){
									font(name: "arial", bold: true)
								}
								
								format(name: "cell"){
									font(name: "arial", bold: false)
								}

								
								Set keySet = coverPageMap.keySet()
								if(keySet.size() > 0){
									def key = keySet.first()
									Map resultMap = coverPageMap.get("Details")
									Set kSet = resultMap.keySet()
									kSet.eachWithIndex { field, index ->
										String label = getLabel(field)
										cell(row: rowIndex, column: 5, value: label, format: "header")
										String value = resultMap.get(field)
										cell(row: rowIndex, column: 5 +1, value: value, format: "cell")
										rowIndex ++
									}
								}
								
								for(int i = 0 ; i < 4 ; i ++ ){
									cell(row: rowIndex, column: 5 +1, value: "", format: "cell")
									rowIndex ++
								}
								
								if(keySet.size() > 0){
									Map resultMap = coverPageMap.get("Total")
									Set kSet = resultMap?.keySet()
									kSet?.eachWithIndex { field, index ->
										String value = getLabel(field)
										cell(row: rowIndex, column: 4+index, value: value, format: "header")
									}
								}
								

								keySet.eachWithIndex {  object, k ->
									if(!object.equals("Details")){
									Map resultMap = coverPageMap.get(object)
									Set kSet = resultMap.keySet()
									kSet.eachWithIndex {field, i ->
										Object value = resultMap.get(field)//getValue(object, field)
										String formatString = "cell"
										if(i == 1){
											formatString = "titlecell"
										}
										cell(row: k + rowIndex, column: 4+i, value: value , format :formatString)
									}

									}
								}

							}
						}else{
						int rowIndex = 0
							Map tabMap = dataMap.get(sheetName)
							if(tabMap != null){
								List data = tabMap?.get("dataList")
								List fields = tabMap?.get("fieldsList")
								if(data != null && fields != null){
									sheet(name: sheetName ?: "Export", widths: getParameters().get("column.widths")){
										//Default format
										format(name: "header"){
											font(name: "arial", bold: true)
										}

										format(name: "cell"){
											font(name: "arial", bold: false)
										}


										//Create header
										if(isHeaderEnabled){
											fields.eachWithIndex { field, index ->
												String value = getLabel(field)
												cell(row: rowIndex, column: index, value: value, format: "header")
											}

											rowIndex ++ 
										}

										//Rows
										data.eachWithIndex { object, k ->
											fields.eachWithIndex { field, i ->
												Object value = getValue(object, field)
												cell(row: k + rowIndex, column: i, value: value , format :"cell")
											}
										}
									}
								}
							}
						}
					}
				}
			}

			builder.write()
		}
		catch(Exception e){
			throw new ExportingException("Error during export", e)
		}
	}

}
