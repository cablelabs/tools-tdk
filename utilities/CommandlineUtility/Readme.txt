TWC Automation is the command line utility which is used for the automated execution of input test scripts.While make use of this utility we can avoiid the usage of Test Manager .The utility requires the following contents,

	1. TestExecuter.sh 

	2. xml_check.sh 

	3. TDK python libraries:
	   tdklib.py
	   As per the latest release.	 
	   ( The files devicestatus.py, streamlib.py, dvrlib.py, recorderlib.py, getDevices.py, setRoute.py and resetAgent.py
		are required)

	4. Report generation scripts:	   
	   PerformanceReportGenerator.py
	   ReportGenerator.py
	   generatereport_sample.sh
	 
	5. GstreamerBasePluginTest.py (Modified for automation)
	   It is the sample script for the TWC Automation.
     	   
	 
	6. SuiteExecuter.sh (Modified for automation)
           opensrc_comp_test.properties ( Modified for automation)

	7. Test report Templates:
	   GStreamerPerformanceTestReport.xls
	   GStreamerTestCaseReport.xls
	  
	  	   
How to execute the tests:

1) Install the below packages
	1. python-MySQLdb
	2. python-xlwt
	3. python-xlrd
	4. python-xlutils

2) Modify the configuration section in  "TestExecuter.sh" as below:
		a) TARGET_IP - STB IP address ie; DUT IP Address.
		   Example : 
			TARGET_IP=192.168.160.170  #XG1_BOX
		b) LOG_PATH - Same path as the web application/Test Manager is keeping the logs.
		   Example : 
			LOG_PATH=<Path to Apache web server home folder>/opt/apache-tomcat-6.0.41/webapps/rdk-test-tool/logs/
		c) BUILD_VER - for which RDK build, reports need to generated . Any version number will do.
		   Example :
			BUILD_VER=Release-2.0  
		d) TEST_MANAGER_URL - Test Manager URL
		   Example : 
			TEST_MANAGER_URL="http://192.168.161.32:8080/rdk-test-tool"
		e) DEV_NAME - Name of the Device, for displaying the "Execution name" in the Test manager
		   Example :
			DEV_NAME=XG1_BOX		
		f) TESTS_TO_RUN - Test need to be run (GSTREAMER, WEBKIT and RDKWEBKIT)
            	   Example :
			TESTS_TO_RUN="GSTREAMER"
		
		Suppose we are working with the command line aruments we need to give all the inputs as arguments,
		But here we need to just edit our inputs in TestExecuter.sh as our need. 
		
3) Create/Add/Insert blank columns for new build results , in the excel sheet template. (A new blank column is already created in the excel sheets.)
   Example : For Release 1.4.0, append (after last available Test Result column) a column in "TWC_Tests" sheet of Functional tests.

		|  Test Result   |
		|  Release-1.4.0 |
   		|		 |
             Similarly for "RDK_Tests" sheet. And for Performance sheet four additional column needed as mentioned below.

		| Release-1.4.0	 |	    | 		      |          |
		|  Reading	 |  Result  |	Execution Id  |	Comments |
          

4) Compile the given dummy tests for the target platform (STB/DUT).Load the STB with TDK binaries & libraries (agent, stubs, test binaries and dependent libs). 
   - Dummy tests implementations are given for the sample Gstreamer script.

5) Replace the "SuiteExecuter.sh" and "opensrc_comp_test.properties" files in STB with the new given files.

6) Once agent is in running state in STB, run the "TestExecuter.sh" file from host machine. 
   After successful execution, Results will be populated in report.You can look into the file named "GstreamerBasePluginTest.log" for the detailed information.

  
  