/*
 * If not stated otherwise in this file or this component's Licenses.txt file the
 * following copyright and licenses apply:
 *
 * Copyright 2016 RDK Management
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
*/
package com.comcast.rdk;

import java.io.BufferedReader;
import java.io.File;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.PrintWriter;
import java.io.Reader;
import java.io.Writer;
import java.net.Socket;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.Date;

import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.springframework.util.StringUtils;

/**
 * Class meant to execute tcl scripts from command line. Reads the command line
 * parameters, convert them to json request and sends to the testable box
 * 
 * @author deepesh.mohan
 * 
 */
public class TclSocketExecutor {

	private static final String JSON_RPC = "jsonrpc";
	private static final String JSON_RPC_VERSION = "2.0";
	private static final String RESULT_ID = "resultID";
	private static final String METHOD = "method";
	private static final String PARAM_NAME = "paramName";
	private static final String PARAM_VALUE = "paramValue";
	private static final String PARAM_TYPE = "paramType";
	private static final String PARAM = "param1";
	private static final String DELIMITER = ",";
	private static final String ENABLE_SCRIPT_SUITE = "ScriptSuiteEnabled";
	private static final String ID = "id";
	private static final String VERSION = "version";

	private static final int PORT = 8087;

	/**
	 * @param args
	 */

	private static class Builder {
		private JSONObject object = new JSONObject();

		public Builder loadModule() {
			object.put(METHOD, "LoadModule");
			return this;
		}

		public Builder unloadModule() {
			object.put(METHOD, "UnloadModule");
			return this;
		}

		public Builder addParamName(String value) {
			object.put(PARAM_NAME, value);
			return this;
		}

		public Builder addParamValue(String value) {
			object.put(PARAM_VALUE, value);
			return this;
		}

		public Builder addParamType(String value) {
			object.put(PARAM_TYPE, value);
			return this;
		}
		
		public Builder addVersion() {
			object.put(VERSION, "RDKB");
			return this;
		}
		
		public Builder addId() {
			object.put("id", "2");
			return this;
		}

		public Builder addModuleToLoadOrUnload(String value) {
			object.put(PARAM, value);
			return this;
		}

		public Builder addPerformanceParams() {
			object.put("performanceBenchMarkingEnabled", "false");
			object.put("performanceSystemDiagnosisEnabled", "false");
			return this;
		}

		public Builder addResultID() {
			object.put(RESULT_ID, "1");
			return this;
		}

		public Builder addMethod(String value) {
			object.put(METHOD, value);
			return this;
		}

		public Builder addJSONRPCVersion() {
			object.put(JSON_RPC, JSON_RPC_VERSION);
			return this;
		}
		
		public Builder enableScriptSuite(String enable) {
			object.put(ENABLE_SCRIPT_SUITE, enable);
			return this;
		}

		public String build() {
			return this.object.toJSONString();
		}

	}
	
	public static String getModuleName(String param) {
		String moduleName = "";
		if (param.contains("Device.WiFi.") || param.contains("Device.X_CISCO_COM_Security") || param.contains("Device.DHCPv4")) {
			moduleName = "wifiagent";
		}
		return moduleName;
	}
	
	public static String getMethodName(String module , String methodType){
		String method = "";
		if(module.equals("wifiagent")){
			if(methodType.toUpperCase().contains("SET")){
				method = "WIFIAgent_Set";
			}else if(methodType.toUpperCase().contains("GET")){
				method = "WIFIAgent_Get";
			}
		}
		return method;
	}
	
	public static String getDeviceIP(String serailNo){
		String ip = "";

		Connection dbConn = null;

		try {
			dbConn = DriverManager
			.getConnection("jdbc:mysql://127.0.0.1/rdktesttoolproddb?autoReconnect=true","rdktesttooluser", "6dktoolus3r!");
		} catch (SQLException e) {
			e.printStackTrace();
			return "";
		}

		if (dbConn != null) {
			 Statement sqlStmt;
			try {
				sqlStmt = dbConn.createStatement();
				String sql;
				sql = " SELECT stb_ip from device where serial_no=\""+serailNo+"\"";
				ResultSet rs = sqlStmt.executeQuery(sql);
				while(rs.next()){
					ip = rs.getString("stb_ip");
					break;
				}
				
				try{
			         if(sqlStmt!=null)
			            sqlStmt.close();
			      }catch(SQLException se2){
			    	  System.out.println(" err "+se2.getMessage());
			      }
				
			      try{
			         if(dbConn!=null)
			            dbConn.close();
			      }catch(SQLException se){
			    	  System.out.println(" er "+se.getMessage());
			         se.printStackTrace();
			      }
			} catch (SQLException e) {
				e.printStackTrace();
			}
		      
		} else {
			System.out.println("Failed to make connection!");
		}
	
		return ip;
	}

	public static void main(String[] args) {
		try {
			File myFile = new File("log-"+System.currentTimeMillis()+".txt");
			myFile.createNewFile();
			PrintWriter pwr = new PrintWriter(myFile);
			pwr.write("Here start " + new Date());
			pwr.write("args " + args);
			pwr.flush();
			pwr.close();
		} catch (Exception e) {
			System.out.println(" errorrr "+e.getMessage());
		}
		String arr[] = new String[10];
		int count = 0;
		try {
			for (String s : args) {
				arr[count] = s;
				++count;
			}
			String oui = args[0];
			String sNo = args[1];
			String deviceType = args[2];
			String methodType = args[3];
			String paramName = args[4];
			String paramValue = null;
			String paramType = null;
			String module = getModuleName(paramName);
			String deviceIp = getDeviceIP(sNo);
			String method = getMethodName(module, methodType);
			BufferedReader buf = null;
			PrintWriter pw = null;
			
			if (StringUtils.hasText(methodType)
					&& methodType.toUpperCase().contains("SET")) {
				paramValue = args[5];
				paramType = args[6];
				if (!StringUtils.hasText(paramValue)
						|| !StringUtils.hasText(paramType)) {
					System.out
							.println("Insufficient parameters for Set method call !!! ");
//					exitExecution();
				}
			}
			Socket socket = null;
			OutputStream out = null;
			try {
				System.out.flush();
			} catch (Exception e) {
			}
			
			try{
				Thread.sleep(5000);
			}
			catch(Exception e){
				
			}
			try{
			socket = new Socket(deviceIp, PORT);
			out = socket.getOutputStream();
			buf = new BufferedReader(new InputStreamReader(
					socket.getInputStream()));
			
			pw = new PrintWriter(out, true);

			loadModule(module, buf, pw);
			try{
				Thread.sleep(3000);
			}
			catch(Exception e){
				
			}

			try {
				if (methodType.toUpperCase().startsWith("SETMULTIPLE")) {
					executeMultipleSet(method, paramName, paramValue,
							paramType, pw, buf);
				} else if (methodType.toUpperCase().startsWith("GET")) {
					executeGet(method, paramName, pw, buf);
				} else if (methodType.toUpperCase().startsWith("SET")) {
					executeSet(method, paramName, paramValue, paramType, pw,
							buf);
				}

			} catch (Exception e) {
				System.out.println(" Error "+e.getMessage());
				e.printStackTrace();
			}
			unloadModule(module, pw, buf);
			try{
				Thread.sleep(10000);
			}
			catch(Exception e){
				
			}
			}finally{
				
				terminateConnection(buf, pw, out);
				if (socket != null && !socket.isClosed()) {
					try {
						socket.shutdownInput();
						socket.shutdownOutput();
					} catch (Exception e) {
						System.out.println(" Error here during shutdown");
					}
					socket.close();
					socket = null;
				}
			}
			

		} catch (Exception e) {
			System.out.println("Error occured "+e.getMessage());
			e.printStackTrace();
		}
	}

	private static void loadModule(String module, BufferedReader buf,
			PrintWriter pw) throws Exception {
		try {
			String val;
			Builder builder = new Builder();
			builder.addJSONRPCVersion().loadModule()
					.addModuleToLoadOrUnload(module).addPerformanceParams()
					.addResultID().build();

			System.out.println("Load module request : " + builder.build());
			pw.println(builder.build());
			pw.flush();
			String result = buf.readLine();
			System.out.println("Load module response : " + result);
			if (result == null) {
				throwError();
			}
			val = getResultStatus(result);
			if (!StringUtils.hasText(val) || (!val.equalsIgnoreCase("SUCCESS"))) {
				System.out.println("Load Module failed");
				System.out.println(val);
				exitExecution();
			}
		} catch (Exception e) {
			e.printStackTrace();
//			exitExecution();
			throwError();
		}
	}

	private static void unloadModule(String module, PrintWriter pw,
			BufferedReader buf) throws Exception {
		try {
			Builder builder;
			builder = new Builder();
			builder.addJSONRPCVersion().unloadModule().enableScriptSuite("false").addId().addVersion()
					.addModuleToLoadOrUnload(module);
			System.out.println("Unload module request : " + builder.build());
			pw.println(builder.build());
			pw.flush();
			System.out.println("Unload module response : " + buf.readLine());
		} catch (Exception e) {
			System.out.println(" Error in unloadModule "+e.getMessage());
			e.printStackTrace();
//			exitExecution();
			throwError();
		}
	}

	private static void executeMultipleSet(String method, String paramName,
			String paramValue, String paramType, PrintWriter pw,
			BufferedReader buf) throws Exception {
		String[] paramNames = paramName.split(DELIMITER);
		String[] paramValues = paramValue.split(DELIMITER);
		String[] paramTypes = paramType.split(DELIMITER);
		boolean valid = checkForValidMultipleSetParams(paramNames.length,
				paramValues.length, paramTypes.length);
		if (valid) {
			for (int i = 0; i < paramNames.length; i++) {
				executeSet(method, paramNames[i], paramValues[i],
						paramTypes[i], pw, buf);
			}
		} else {
			System.out
					.println("Parameter Names/Values/Types list doesn't match. ");
			throwError();
		}
	}

	private static boolean checkForValidMultipleSetParams(int paramNameSize,
			int paramValueSize, int paramTypeSize) {
		return ((paramNameSize == paramValueSize) && (paramNameSize == paramTypeSize));
	}

	private static void executeSet(String method, String paramName,
			String paramValue, String paramType, PrintWriter pw,
			BufferedReader buf) throws Exception {
		String val = null;
		Builder builder = new Builder();
		builder.addJSONRPCVersion().addMethod(method).addParamValue(paramValue)
				.addParamName(paramName).addParamType(paramType);
		pw.println(builder.build());
		pw.flush();
		System.out.println("Request " + method + " : " + builder.build());

		String respo = buf.readLine();
		System.out.println("Response " + method + " : " + respo);
		if (!StringUtils.hasText(respo)) {
			System.out.println(" Going to throw Error ");
			throwError();
		}
		val = getResultStatus(respo);
		if (!StringUtils.hasText(val) || (!val.equalsIgnoreCase("SUCCESS"))) {
			//terminateConnection(buf, pw);
			System.out.println(" Going to throw Error as fail");
			throwError();
		}
	}

	private static void executeGet(String method, String paramName,
			PrintWriter pw, BufferedReader buf) throws Exception {
		String val = null;
		Builder builder = new Builder();
		builder.addJSONRPCVersion().addMethod(method).addParamName(paramName);
		System.out.println("Request " + method + " : " + builder.build());
		pw.println(builder.build());
		pw.flush();
		String respo = buf.readLine();
		System.out.println("Response " + method + " : " + respo);
		if (!StringUtils.hasText(respo)) {
			throwError();
		}
		val = getResultStatus(respo);
		if (!val.equalsIgnoreCase("SUCCESS")) {
			//terminateConnection(buf, pw);
			throwError();
		}
	}

	private static String getResultStatus(String response) {
		String status = null;
		try {
			JSONParser parser = new JSONParser();
			JSONObject obj = (JSONObject) parser.parse(response);
			if (obj.containsKey("result")) {
				status = (String) obj.get("result");
			}
		} catch (Exception e) {
			e.printStackTrace();
		}
		return status;
	}

	private static void throwError() throws Exception {
		throw new Exception("Error occured");
	}

	private static void exitExecution() {
		System.out.println("Error occured");
		System.exit(0);
	}

	private static void terminateConnection(Reader reader, Writer writer, OutputStream out) {
		if (reader != null) {
			try {
				reader.close();
				reader = null;
			} catch (Exception e) {
				e.printStackTrace();
			}
		}
		if (writer != null) {
			try {
				writer.close();
				writer = null;
			} catch (Exception e) {
				e.printStackTrace();
			}
		}
		
		if(out != null){
			try {
				out.close();
				out = null;
			} catch (Exception e) {
				e.printStackTrace();
			}
		}

	}

}
