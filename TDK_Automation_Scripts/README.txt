Prerequisite :
---------------
	1) TDK binaries and libraries should be flashed in STB and agent should be up and running in STB/Target.
	2) List of packages need to be installed before running automation scripts.
		1. python-MySQLdb: For Performing read and write operation in database using python script.
	3) Atleast one test should be run from Test Manager UI, prior to running TDK automation scripts.
	4) User should have write permissions to "Test tool folder in webapps folder of apache setup (For collecting test logs)".
	5) Agent should be UP and running in configured "TARGET_IP" STB and loaded with all required stubs and tests.

		
Steps to run TDK automation scripts:
-----------------------------------------

1) TDK Automation scripts organization (Folder structure) :
	Test Automation scripts - @...../twc_automation
	Python libraries 	- @...../python-lib
        Customized tests scripts- @...../tests
        (Component Customized tests scripts are generated from Original tests scripts in the Test Manager web applcation file store)

2) Configure Environment part of "TdkConfig.xml", as per the present Test Environment.

	1) Test Environment Configuration:
	   -------------------------------
		TARGET_IP - STB/Target IP address, where the tests need to be executed
		BUILD_VER - RDK build version in STB (Test results will be updated for this build version in Reports)
		TEST_MANAGER_URL - Host machine Test manager URL
		LOG_PATH - Configure corresponding webapps path of rdk test tool. 
			  (Logs will be transfered to this location with corresponding Execution IDs)
		DEV_NAME  - STB device name

		Example configuration :
		------------------------
			<TestEnvironment>
			<TARGET_IP>10.143.32.85</TARGET_IP>
			<BUILD_VER>Release-1.22.2</BUILD_VER>
			<TEST_MANAGER_URL>http://10.143.32.65:8080/rdk-test-tool_02Sep2014</TEST_MANAGER_URL>
			<LOG_PATH>/home/rdktest/Desktop/apache-tomcat-6.0.37/webapps/rdk-test-tool_02Sep2014/</LOG_PATH>
			<!-- LOG_PATH : Path where logs will be stored -->
			<COMMON_XML_LOGS_PATH enabled="true">./TEMP/TDKLOGS</COMMON_XML_LOGS_PATH>	
			<!-- COMMON_XML_LOGS_PATH : All xml logs will be copied (**duplicated**) to this COMMON_XML_LOGS_PATH -->
			<DEV_NAME>HUMAX_IPSTB0</DEV_NAME>
			<PORT_ID>8087</PORT_ID>
			</TestEnvironment>

	2) Test Suite Configuration:
	   --------------------------
		Enable the tests, which need to be executed using the configuration flags in the component tag of TdkConfig.xml.

		TestExecutionEnabled - true/false to enable/Disable Tests excution for the component repectively
		ReportGenerationEnabled  - true/false to enable/Disable Tests excution for the component repectively

		Other parameters like TestScripts location, ScriptName and  SharedObjectName can be configured based on requirement (if any change in environment).

		<TestSuite name="RDKLogger"  component="RDKLogger" testtype="functional">
			<TestExecutionEnabled>true</TestExecutionEnabled>
			<ReportGenerationEnabled>true</ReportGenerationEnabled>
			<TestCaseReportName>RDKLoggerTestCaseReport</TestCaseReportName>
			<TestScripts location="../tests/RDKLogger/scripts/" runall="false" >
				 <ScriptName>twc_RDKLogger_CheckMPELogEnabled</ScriptName>
				 <ScriptName>twc_RDKLogger_Dbg_Enabled_Status</ScriptName>
			</TestScripts>
			<SharedObjectName>rdklogger</SharedObjectName>
			<Feature name="RDKLogger"/>
		</TestSuite>


3) Run the tests by executing "TdkTestExecuter.py" script.
	sudo python TdkTestExecuter.py;

	On successful execution :
	- Test result XML logs will be updated in COMMON_XML_LOGS_PATH ("./TEMP/TDKLOGS) configured as per Test Environment.
	- Test Report in Excel sheet will be generated.
	- Test manager UI will be updated with test execution details.

Note:
-----
- We had provided option to configure data base details on configuration file.
- We had implemented some additional functionality specific to TWC for reading TDK and RDK version details from STB at run time with the help of new agent method.
- Run the Test automation scripts with enough permissions to folders and files to avoid access issues.
