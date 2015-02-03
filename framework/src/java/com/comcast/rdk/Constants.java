/*
 * ============================================================================
 * COMCAST C O N F I D E N T I A L AND PROPRIETARY
 * ============================================================================
 * This file (and its contents) are the intellectual property of Comcast.  It may
 * not be used, copied, distributed or otherwise  disclosed in whole or in part
 * without the express written permission of Comcast.
 * ============================================================================
 * Copyright (c) 2014 Comcast. All rights reserved.
 * ============================================================================
 */
package com.comcast.rdk;

/**
 * Class that holds all constants for this applicaiton.
 * 
 * @author ajith, sreejasuma, praveenkp
 * 
 */
public final class Constants
{
    /**
     * Ensure that no instance of this class is created.
     */
    private Constants()
    {

    }

    public static final String ID_DEFAULT           = "1";
    public static final String KEY_ID               = "id";
    public static final String KEY_JSONRPC          = "jsonrpc";
    public static final String KEY_METHOD           = "method";
    public static final String KEY_PARAMS           = "params";
    public static final String KEY_LOCATOR          = "locator";
    public static final String KEY_FREQUENCY        = "frequency";
    public static final String VAL_JSONRPC          = "2.0";
    public static final String DATE_FORMAT          = "yyyy/MM/dd HH:mm:ss";
    public static final String DATE_FORMAT1         = "yyyyMMddHHmmss";
    public static final String SEARCH_DATE_FORMAT   = "yyyy-MM-dd HH:mm:ss";
    public static final String SCHEDULE_DATEFORMAT  = "EEE MMM d HH:mm:ss z yyyy";
    public static final String STRING_QUOTES        = "\"";
    public static final String CLIENTLIST           = "<clientlist>";
    public static final String IP_ADDRESS           = "<ipaddress>";
    public static final String PORT                 = "<port>";
    public static final String LOCALFILE            = "<localfile>";
    public static final String HTML_BR              = "<br/>";
    public static final String VERSIONTRANSFER_FILE = "versiontransfer.py";
    public static final String TEMP_VERSIONFILE_NAME= "Version_File.py";
    public static final String RESULT_TOKEN         = "[SCRIPTSTATUSRESULT]";
    public static final String PYTHON_EXTENSION     = ".py";
    public static final String FILE_STARTS_WITH     = "/script_";
    public static final String FAILURE_STATUS       = "FAILURE";
    public static final String SUCCESS_STATUS       = "SUCCESS";
    public static final String UNDEFINED_STATUS     = "UNDEFINED";
    public static final String INPROGRESS_STATUS    = "IN-PROGRESS";
    public static final String SKIPPED_STATUS    	= "SKIPPED";
    public static final String ABORTED_STATUS    	= "ABORTED";
    public static final String COMPLETED_STATUS    	= "COMPLETED";
    public static final String NOT_APPLICABLE_STATUS="N/A";
    
    
    
    public static final String ERROR_STATUS         = "error";
    public static final String KEY_GROUP            = "Suite";
    public static final String URL_SEPERATOR        = "/";
    public static final String DOUBLE_FWD_SLASH     = "//";
    public static final String TEST_SUITE           = "TestSuite";
    public static final String SINGLE_SCRIPT        = "SingleScript";
    public static final String METHOD_TOKEN         = "configureTestCase";
    public static final String REPLACE_TOKEN        = "configureTestCase(ip,port,";
    public static final String REPLACE_BY_TOKEN     = ",ip,port,";
    public static final String LEFT_PARANTHESIS     = "(";
    public static final String RIGHT_PARANTHESIS    = ")";
    public static final String CURLY_BRACKET_OPEN   = "{";
    public static final String CURLY_BRACKET_CLOSE  = "}";
    public static final String SQUARE_BRACKET_OPEN  = "[";
    public static final String SQUARE_BRACKET_CLOSE = "]";
    public static final String KEY_GATEWAYIP        = "gatewayip";
    public static final String KEY_CHANNELTYPE      = "channeltype";
    public static final String KEY_OCAPID           = "ocapid";
    public static final String KEY_RECORDERID       = "recorderid";
    public static final String COMMA_SEPERATOR      = ",";
	public static final String SINGLE_QUOTES        = "'";
	public static final String UNDERSCORE           = "_";
	public static final String KEY_AUDIOFORMAT      = "audioformat";
	public static final String KEY_VIDEOFORMAT      = "videoformat";
	public static final String BOXTYPE_CLIENT       = "client";
	public static final String BOXTYPE_GATEWAY      = "gateway";
	public static final int EXEC_EXITCODE_SUCCESS   = 0;
	public static final String NEW_LINE             = "\n";
	public static final String LINE_STRING          = "======";
	public static final int INDEX_ZERO              = 0;
	public static final int INDEX_ONE               = 1;
	public static final int INDEX_TWO               = 2;
	public static final int INDEX_THREE             = 3;
	public static final String KEY_ON               = "on";
	public static final String KEY_FNID             = "fnid";
	public static final String KEY_FNCHKBOX         = "fnchkbox";
	public static final String KEY_CHKBOX           = "chkbox";
	public static final String STATUS_NONE          = "none";	
	public static final String SEMI_COLON           = ";";
	public static final String COLON          		= ":";
    public static final String KEY_DAILY            = "Daily";
    public static final String KEY_WEEKLY           = "Weekly";
    public static final String KEY_MONTHLY          = "Monthly";
    public static final String KEY_DAILYDAYS        = "dailyDays";
    public static final String KEY_DAILYWEEKDAY     = "dailyWeekday";
    public static final String KEY_MONTHLYDAYS      = "monthlyDays";
    public static final String KEY_MONTHLYCOMPLEX   = "monthlyComplex";
    public static final String KEY_JOB              = "Job";
    public static final String KEY_TIGGER           = "Trigger";
    public static final String KEY_RECCURENCE       = "ReccurenceSchedule";
    public static final String KEY_ONETIME          = "OnetimeSchedule";
    public static final String MULTIPLESCRIPT       = "Multiple Scripts";
    public static final String KEY_EXISTING         = "Existing";
    public static final String KEY_EXPECT           = "expect";
    public static final String KEY_BINARYTRANSFER   = "Binaries Transferred";
    public static final String KEY_LASTDAY          = "L";
    public static final String KEY_ENTERNEW_LINE          = "\r\n";
    public static final String GREATERTHAN                = ">";
    public static final String LESSTHAN                   = "<";
    public static final String HTML_GREATERTHAN           = "&gt;";
    public static final String HTML_LESSTHAN              = "&lt;";
    public static final String HTML_REPLACEBR             = "</?br\\b[^>]*>";
    public static final String HTML_PATTERN             = "<span(.*?)</span>";
    public static final String HTML_PATTERN_AFTERSPAN   = "</?span\\b[^>]*>";
    
    public static final String PYTHON_COMMAND     = "python";
    public static final String HYPHEN             = "-";
    public static final String XI3_BOX            = "IPClient-3"; //"Xi3";
    public static final String FOUND_MACID        = "DEVICES=";
    
	public static final String NO_DEVICES_MSG 	   = "NO_DEVICES";
	public static final String AGENT_NOT_FOUND_MSG = "AGENT_NOT_FOUND";
	public static final String FAILURE_MSG 		   = "FAILURE";
	public static final String BLANK_SPACE         = "";
	public static final String SPACE               = " ";
	public static final String GATEWAY_BOX         = "gateway";
	public static final String DEFAULT_BOX_MANUFACTURER =  "Pace";
	public static final String DEFAULT_SOCVENDOR   = "Px001bn";
    
    
    public static final int customStbPort = 10000;
    public static final	int customStatusPort = 20000;
    public static final	int customLogTransferPort = 30000;
    public static final	int customAgentMonitorPort = 40000;
    public static final String CI_EXECUTION = "CI_";
    
    public static final String RERUN = "_RERUN";
    public static final String MULTIPLE = "Multiple";
    
    public static final String SCRIPT_OUTPUT_FILE_PATH = "//fileStore//opFolder//";
    public static final String SCRIPT_OUTPUT_FILE_EXTN = ".txt";
    
    public static final String TDK_ERROR = "#TDK_@error-";
    
    public static final String TRUE = "true";
    public static final String FALSE = "false";
    public static final String KEY_BENCHMARK = "BENCHMARK";
    public static final String KEY_SYSTEMDIAGNOSTICS = "SYSTEMDIAGNOSTICS";
    public static final String KEY_SCRIPTEND = "SCRIPTEND#!@~";
    public static final String PENDING = "PENDING";
    public static final String PAUSED = "PAUSED";
    public static final String SKIPPED = "SKIPPED";
    public static final String KEY_PERFORMANCE_BM = "PerformanceBenchMarking";
    public static final String KEY_PERFORMANCE_SD ="PerformanceSystemDiagnostics";
    
    public static final String COMPONENT ="component";
    public static final String INTEGRATION ="integration";
    public static final String NO_OS_SUITE = "_NO_OS";
    
    
}
