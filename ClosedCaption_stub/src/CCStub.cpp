/*
 * This file has the wrapper functiona for all the APIs present in the CC component.
 * Some addtional functions for supporting the CC test cases.
 */


#include "CCAgent.h"

static bool CCInitFlag = true;

/*****************************************************************************************************************
 *
 * This Constructor function for CCAgent class
 *
 *
 ******************************************************************************************************************/

CCAgent::CCAgent()
{
    std::cout<<"CCAgent Initialized"<<std::endl;
}

/**********************************************************************************************************************
 * Function Description  : This is a Common function will get the retvalue as input and it returns corresponding SUCCESS
 * 				       or FAILUER status to the wrapper function
 *
 * @Input parameters      : Integer
 *
 * @return                : returns the description of the error string if its a failure or returns success string
 ***********************************************************************************************************************/
char* getResult_CC(int retval,char *resultDetails)
{
    if(retval==0)
        return (char*)"SUCCESS";
    else
    {
        retval=retval-ERRORVALUE;

        switch(retval)
        {
        case 1:
            strcpy(resultDetails,"ERRORINVALID");
            break;
        case 2:
            strcpy(resultDetails,"ERRORNOMEMORY");
            break;
        case 3:
            strcpy(resultDetails,"ERRORBUSY");
            break;
        case 4:
            strcpy(resultDetails,"ERRORMUTEX");
            break;
        case 5:
            strcpy(resultDetails,"ERRORCOND");
            break;
        case 6:
            strcpy(resultDetails,"ERROREVENT");
            break;
        case 7:
            strcpy(resultDetails,"ERRORTIMEOUT");
            break;
        case 8:
            strcpy(resultDetails,"ERRORNODATA");
            break;
        case 9:
            strcpy(resultDetails,"ERRORTHREADDEATH");
            break;
        default:
            strcpy(resultDetails,"ERRORUNKNOWN");
            break;
        }
        return (char*)"FAILURE";
    }
}
/**************************************************************************************************************************
 * Function Description  : Initialize Function will be used for registering the wrapper method with the agent so that wrapper
 *  	                      function will be used in the script
 *
 * @Param[in]            : None
 *
 * @return               : return success
 **************************************************************************************************************************/

bool CCAgent::initialize(IN const char* szVersion,IN RDKTestAgent *ptrAgentObj)
{
    std::cout<<"CCStub Initialize"<<std::endl;

    /*Register stub function for callback*/
    ptrAgentObj->RegisterMethod(*this,&CCAgent::CCInit, "TestMgr_CC_Init");
    ptrAgentObj->RegisterMethod(*this,&CCAgent::CCSetGetState, "TestMgr_CC_SetGetState");
    ptrAgentObj->RegisterMethod(*this,&CCAgent::CCSetGetAttribute, "TestMgr_CC_SetGetAttribute");
    ptrAgentObj->RegisterMethod(*this,&CCAgent::CCSetGetDigitalChannel, "TestMgr_CC_SetGetDigitalChannel");
    ptrAgentObj->RegisterMethod(*this,&CCAgent::CCSetGetAnalogChannel, "TestMgr_CC_SetGetAnalogChannel");
    ptrAgentObj->RegisterMethod(*this,&CCAgent::CCShow, "TestMgr_CC_Show");
    ptrAgentObj->RegisterMethod(*this,&CCAgent::CCHide, "TestMgr_CC_Hide");
    ptrAgentObj->RegisterMethod(*this,&CCAgent::CCGetSupportedServiceNumberCount, "TestMgr_CC_GetSupportedServiceNumberCount");
    ptrAgentObj->RegisterMethod(*this,&CCAgent::CCGetSupportedServiceNumber, "TestMgr_CC_GetSupportedServiceNumber");
    ptrAgentObj->RegisterMethod(*this,&CCAgent::CCOnEasStart, "TestMgr_CC_OnEasStart");
    ptrAgentObj->RegisterMethod(*this,&CCAgent::CCOnEasStop, "TestMgr_CC_OnEasStop");
    ptrAgentObj->RegisterMethod(*this,&CCAgent::CCSetTrickPlayStatus, "TestMgr_CC_SetTrickPlayStatus");
    ptrAgentObj->RegisterMethod(*this,&CCAgent::CCResetTrickPlayStatus, "TestMgr_CC_ResetTrickPlayStatus");
    return TEST_SUCCESS;
}

/***************************************************************************
 *Function name : testmodulepre_requisites
 *Descrption    : testmodulepre_requisites will  be used for setting the
 *                pre-requisites that are necessary for this component
 *
 *****************************************************************************/

std::string CCAgent::testmodulepre_requisites()
{
        return "SUCCESS";
}
/***************************************************************************
 *Function name : testmodulepost_requisites
 *Descrption    : testmodulepost_requisites will be used for resetting the
 *                pre-requisites that are set
 *
 *****************************************************************************/

bool CCAgent::testmodulepost_requisites()
{
        return TEST_SUCCESS;
}


/**************************************************************************************************************************
 * @Function Description : CCInit Function will be used for intialize the required resources before call the Closed caption APIS
 *
 *
 * @Param[in]            : None
 *
 * @return               :Filled with SUCCESS or FAILURE based on the return value of CC API
 **************************************************************************************************************************/


bool CCAgent::CCInit(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_ERROR,"\nCCAgent_Init --->Entry %d\n",CCInitFlag);

    if(CCInitFlag == true)
    {
        int status = 0, returnvalue;
        char *resultDetails;
        try
        {
            DEBUG_PRINT(DEBUG_ERROR,"\nvlGfxInit(0) --->Entry \n");
            vlGfxInit(0);
        }
        catch(...)
        {
            DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in vlGfxInit(0)\n");
            response["result"] = "FAILURE";
	    response["details"] = "Exception Caught in vlGfxInit";
            return TEST_FAILURE;
        }
        DEBUG_PRINT(DEBUG_ERROR,"\nvlGfxInit(0) --->Entry \n");

        status = vlMpeosCCManagerInit();
        if (0 != status)
        {
            DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in vlMpeosCCManagerInit()\n");
            response["result"] = "FAILURE";
	    response["details"] = "Exception Caught in vlMpeosCCManagerInit";
            return TEST_FAILURE;
        }

        resultDetails=(char *)malloc(sizeof(char)*16);

        CCStatus_t ccStatus = CCStatus_OFF;
        returnvalue = ccSetCCState(ccStatus, 0);
        response["result"]=getResult_CC(returnvalue,resultDetails);
        response["details"]=resultDetails;
        DEBUG_PRINT(DEBUG_ERROR,"\nCCAgent_Init --->result %s\n",response["result"].asCString());
        free(resultDetails);
        DEBUG_PRINT(DEBUG_ERROR,"\nCCAgent_Init --->Exit \n");
        CCInitFlag = false;
        return TEST_SUCCESS;
    }
    else
    {
        DEBUG_PRINT(DEBUG_ERROR,"\nCCAgent_Init already Intialized--->Exit \n");
        response["result"]= "SUCCESS";
        response["details"]="Agent is already intialised";
        return TEST_SUCCESS;
    }
}

/**************************************************************************************************************************
 * @Function Description : CCGetSupportedServiceNumber Function will be used for get the Supported services by the TS
 *
 *
 * @Param[in]            : None
 *
 * @return               :Filled with SUCCESS or FAILURE based on the return value of CC API
 **************************************************************************************************************************/

bool CCAgent::CCGetSupportedServiceNumber(IN const Json::Value& req, OUT Json::Value& response)
{
    unsigned int *stubservicesArray;
    unsigned int *stubservicesArraySize;
    int returnvalue;
    char *resultDetails;
    char *stringDetails = (char*)malloc(sizeof(char)*10);
    char stringDetails1[30] = "ccserviceNumber:";

    resultDetails=(char *)malloc(sizeof(char)*16);
    stubservicesArray = (unsigned int *)malloc(sizeof(unsigned int) * NUM_SERVICES);
    stubservicesArraySize = (unsigned int *)malloc(sizeof(unsigned int) * NUM_SERVICES);

    returnvalue=ccGetSupportedServiceNumbers(stubservicesArray,stubservicesArraySize);
    if(returnvalue ==0)
    {
        sprintf(stringDetails,"%d",*stubservicesArray);
        strcat(stringDetails1,stringDetails);
        DEBUG_PRINT(DEBUG_ERROR,"\nCalling CCServiceNumber %s \n",stringDetails1);
        response["result"]="SUCCESS";
        response["details"]=stringDetails1;

    }
    else
    {
        response["result"]=getResult_CC(returnvalue,resultDetails);
        response["details"]=resultDetails;
    }
    free(stubservicesArray );
    free(stubservicesArraySize );
    free(stringDetails);
    free(resultDetails);
    return TEST_SUCCESS;
}

/**************************************************************************************************************************
 * @Function Description : CCGetSupportedServiceNumberCount Function will be used for get the numberof Supported services
 *  	                      by the TS
 *
 * @Param[in]            : None
 *
 * @return               : Filled with SUCCESS or FAILURE based on the return value of CC API
 **************************************************************************************************************************/
bool CCAgent::CCGetSupportedServiceNumberCount(IN const Json::Value& req, OUT Json::Value& response)
{

    unsigned int *stubservicesArraySize;
    int returnvalue;
    char *resultDetails;
    char *stringDetails = (char*)malloc(sizeof(char)*10);
    char stringDetails1[30] = "ccserviceNumber:";

    resultDetails=(char *)malloc(sizeof(char)*16);
    stubservicesArraySize = (unsigned int *)malloc(sizeof(unsigned int) * NUM_SERVICES);

    returnvalue=ccGetSupportedServiceNumbersCount(stubservicesArraySize);

    if(returnvalue ==0)
    {
        sprintf(stringDetails,"%d",*stubservicesArraySize);
        strcat(stringDetails1,stringDetails);
        DEBUG_PRINT(DEBUG_ERROR,"\nCalling CCServiceNumberCount %s \n",stringDetails1);
        response["result"]="SUCCESS";
        response["details"]=stringDetails1;
    }
    else
    {
        response["result"]=getResult_CC(returnvalue,resultDetails);
        response["details"]=resultDetails;
    }

    free(stubservicesArraySize );
    free(stringDetails);
    free(resultDetails);
    return TEST_SUCCESS;
}

/**************************************************************************************************************************
 * @Function Description : CCResetTrickPlayStatus restore to ccstate before trickplay started
 *
 *
 * @Param[in]            : None
 *
 * @return               : Filled with SUCCESS or FAILURE based on the return value of CC API
 **************************************************************************************************************************/

bool CCAgent::CCResetTrickPlayStatus(IN const Json::Value& req, OUT Json::Value& response)
{

    try
    {
        /*calling CCResetTrickPlayStatus*/
        DEBUG_PRINT(DEBUG_LOG,"\nCalling CCResetTrickPlayStatus\n");
        resetTrickPlayStatus();
    }
    catch(...)
    {
        DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in CCResetTrickPlayStatus()\n");
        response["result"]= "FAILURE";
        response["details"]="Exception Caught in CCResetTrickPlayStatus";
        return TEST_FAILURE;
    }

    response["result"]= "SUCCESS";
    response["details"]="Successfully  executed";
    return TEST_SUCCESS;
}

/**************************************************************************************************************************
 * @Function Description : CCOnEasStart Start the EAS
 *
 *
 * @Param[in]            : None
 *
 * @return               : Filled with SUCCESS or FAILURE based on the return value of CC API
 **************************************************************************************************************************/


bool CCAgent::CCOnEasStart(IN const Json::Value& req, OUT Json::Value& response)
{
    try
    {
        /*calling CCOnEasStop*/
        DEBUG_PRINT(DEBUG_LOG,"\nCalling ccOnEasStart\n");
        ccOnEasStart();
    }
    catch(...)
    {
        DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in ccOnEasStart()\n");
        response["result"]= "FAILURE";
        response["details"]="Exception Caught in ccOnEasStart()";
        return TEST_FAILURE;

    }
    response["result"]= "SUCCESS";
    response["details"]="Successfully  executed";
    return TEST_SUCCESS;
}


/**************************************************************************************************************************
 * @Function Description : CCOnEasStop Stop the EAS
 *
 *
 * @Param[in]            : None
 *
 * @return               : Filled with SUCCESS or FAILURE based on the return value of CC API
 **************************************************************************************************************************/


bool CCAgent::CCOnEasStop(IN const Json::Value& req, OUT Json::Value& response)
{
    try
    {
        /*calling CCOnEasStop*/
        DEBUG_PRINT(DEBUG_LOG,"\nCalling ccOnEasStop\n");
        ccOnEasStop();

    }
    catch(...)
    {
        DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in ccOnEasStop()\n");
        response["result"]= "FAILURE";
        response["details"]="Exception Caught in ccOnEasStop()";
        return TEST_FAILURE;

    }
    response["result"]= "SUCCESS";
    response["details"]="Successfully  executed";
    return TEST_SUCCESS;
}


/**************************************************************************************************************************
 * @Function Description : CCSetTrickPlayStatus set the trickplay status
 *
 *
 * @Param[in]            : Integer ON-1,OFF-0
 *
 * @return               : Filled with SUCCESS or FAILURE based on the return value of CC API
 **************************************************************************************************************************/
bool CCAgent::CCSetTrickPlayStatus(IN const Json::Value& request, OUT Json::Value& response)
{
    int status=request["trickPlayStatus"].asInt();
    try
    {
        /*calling CCSetTrickPlayStatus*/
        DEBUG_PRINT(DEBUG_LOG,"\nCalling CCSetTrickPlayStatus\n");
        ccSetTrickPlayStatus(status);

    }
    catch(...)
    {
        DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in ccSetTrickPlayStatus()\n");
        response["result"]= "FAILURE";
        response["details"]="Exception Caught in ccSetTrickPlayStatus()";
        return TEST_FAILURE;
    }

    response["result"]= "SUCCESS";
    response["details"]="Successfully  executed";
    return TEST_SUCCESS;
}
/**************************************************************************************************************************
 * @Function Description : CCShow will show the Closed Caption display
 *
 *
 * @Param[in]            : None
 *
 * @return               : Filled with SUCCESS or FAILURE based on the return value of CC API
 **************************************************************************************************************************/
bool CCAgent::CCShow(IN const Json::Value& req, OUT Json::Value& response)
{
    int retval;
    char *resultDetails;
    resultDetails=(char *)malloc(sizeof(char)*16);
    retval=ccShow();
    response["result"]=getResult_CC(retval,resultDetails);
    response["details"]=resultDetails;
    return TEST_SUCCESS;
}
/**************************************************************************************************************************
 * @Function Description : CCHide will hide the closed caption display
 *
 *
 * @Param[in]            : None
 *
 * @return               : Filled with SUCCESS or FAILURE based on the return value of CC API
 **************************************************************************************************************************/
bool CCAgent::CCHide(IN const Json::Value& req, OUT Json::Value& response)
{
    int retval;
    char *resultDetails;
    resultDetails=(char *)malloc(sizeof(char)*16);
    retval=ccHide();
    response["result"]=getResult_CC(retval,resultDetails);
    response["details"]=resultDetails;
    free(resultDetails);
    return TEST_SUCCESS;
}

/**************************************************************************************************************************
 * @Function Description : CCSetGetState-is used to set the state ON or OFF
 *
 *
 * @Param[in]            : Integer CCStateON-1,CCSateOFF-0
 *
 * @return               : Filled with SUCCESS or FAILURE based on the return value of CC API
 **************************************************************************************************************************/

bool CCAgent::CCSetGetState(IN const Json::Value& request, OUT Json::Value& response)
{

    int retval;
    char *resultDetails;
    CCStatus_t ccStatus,ccGetStatus;
    char *stringDetails = (char*)malloc(sizeof(char)*10);
    char stringDetails1[30] = "ccstate:";

    resultDetails=(char *)malloc(sizeof(char)*16);
    DEBUG_PRINT(DEBUG_ERROR,"\nCalling CCSetGetState \n");

    ccStatus=(CCStatus_t)request["status"].asInt();
    retval=ccSetCCState(ccStatus, 0);
    DEBUG_PRINT(DEBUG_ERROR,"\nCalling CCSetGetState retval ccStatus %d \n",ccStatus);
    if(retval==0)
    {
        retval=ccGetCCState(&ccGetStatus);
        if(retval==0)
        {
            sprintf(stringDetails,"%d",ccGetStatus);
            strcat(stringDetails1,stringDetails);
            DEBUG_PRINT(DEBUG_ERROR,"\nCalling CCSetGetState retval ccStatus %s \n",stringDetails1);
            response["result"]=(char *)"SUCCESS";
            response["details"]= stringDetails1;

            free(stringDetails);
            free(resultDetails);
            return TEST_SUCCESS;
        }

    }
    DEBUG_PRINT(DEBUG_LOG,"\nset and get\n");
    response["result"]=getResult_CC(retval,resultDetails);
    response["details"]=resultDetails;
    DEBUG_PRINT(DEBUG_ERROR,"\nCalling CCGetState %s \n",response["result"].asCString());
    free(stringDetails);
    free(resultDetails);
    return TEST_SUCCESS;
}


/**************************************************************************************************************************
 * @Function Description : CCSetGetDigitalChannel-is used to set and get the  Digital channels
 *  	                   supported  by the streams
 *
 * @Param[in]            : Integer range from 0-to-63
 *
 * @return               : Filled with SUCCESS or FAILURE based on the return value of CC API
 **************************************************************************************************************************/
bool CCAgent::CCSetGetDigitalChannel(IN const Json::Value& request, OUT Json::Value& response)
{
    unsigned int channel=0;
    int userSelection;
    int returnvalue;
    char *resultDetails;
    char *stringDetails ;
    char stringDetails1[50] = "ccDigitalChannel:";
    DEBUG_PRINT(DEBUG_ERROR,"\n Input Parameter value CCSetGetDigitalChannel %d\n",request["channel_num"].asInt());


    if(request["channel_num"].asInt()== 0)
    {
        DEBUG_PRINT(DEBUG_ERROR,"\n Input Parameter is null CCSetDigitalChannel\n");
        response["result"]= "FAILURE";
        return TEST_FAILURE;

    }

    userSelection = request["channel_num"].asInt();
    resultDetails=(char *)malloc(sizeof(char)*16);

    if(userSelection <= NUM_DIGITALCHANNEL_RANGE)
    {
        returnvalue=ccSetDigitalChannel( userSelection );
        if(returnvalue!=0)
        {
            DEBUG_PRINT(DEBUG_ERROR,"\n Execution Failed on ccSetDigitalChannel()\n");
            response["result"]=getResult_CC(returnvalue,resultDetails);
            response["details"]=resultDetails;
            free(resultDetails);
            return TEST_FAILURE;
        }
    }
    else
    {
        response["result"]="FAILURE";
        response["details"]="Invalid Digital Channel";
        free(resultDetails);

        return TEST_FAILURE;
    }
    stringDetails = (char*)malloc(sizeof(char)*10);

    returnvalue=ccGetDigitalChannel(&channel);
    sprintf(stringDetails,"%d",channel);
    strcat(stringDetails1,stringDetails);
    DEBUG_PRINT(DEBUG_ERROR,"\nCalling CCDigitalchannel value %s \n",stringDetails1);

    if(returnvalue ==0)
    {
        response["result"]="SUCCESS";
        response["details"]=stringDetails1;
    }
    else
    {
        response["result"]=getResult_CC(returnvalue,resultDetails);
        response["details"]=resultDetails;
    }
    free(stringDetails);
    free(resultDetails);

    return TEST_SUCCESS;
}


/**************************************************************************************************************************
 * @Function Description : CCSetGetAnalogChannel-is used to set and get the  Analog channels
 *  	                   Supoprted by the streams
 *
 * @Param[in]            : Integer range from 0-to-8
 *
 * @return               : Filled with SUCCESS or FAILURE based on the return value of CC API
 **************************************************************************************************************************/
bool CCAgent::CCSetGetAnalogChannel(IN const Json::Value& request, OUT Json::Value& response)
{



    unsigned int channel=0;
    int analogChannel = 0;
    int returnvalue;
    char *resultDetails;
    char *stringDetails ;
    char stringDetails1[30] = "ccAnalogChannel:";

    DEBUG_PRINT(DEBUG_ERROR,"\n Input Parameter value CCSetGetAnalogChannel %d\n",request["analog_channel_num"].asInt());
    if(request["analog_channel_num"].asInt()== 0)
    {
        DEBUG_PRINT(DEBUG_ERROR,"\n Input Parameter is null CCSetGetAnalogChannel\n");
        response["result"]= "FAILURE";
        response["details"]="Input Parameter is null CCSetGetAnalogChannel";
        return TEST_FAILURE;

    }

    resultDetails=(char *)malloc(sizeof(char)*16);

    //CCStatus_t ccStatus = CCStatus_OFF;
   /* returnvalue=ccSetCCState(ccStatus, 0);
    if (returnvalue!=0)
    { 
    response["result"]=getResult_CC(returnvalue,resultDetails);
    response["details"]="ccSEtCCstate functon failed to return";
    free(resultDetails);
    return TEST_FAILURE;
    }*/

    int userSelection = request["analog_channel_num"].asInt();

    if(userSelection <= NUM_ANALOGCHANNEL_RANGE )
    {
        analogChannel = GSW_CC_ANALOG_SERVICE_CC1 + (userSelection - 1);
        returnvalue=ccSetAnalogChannel( analogChannel );
        if(returnvalue!=0)
        {
            DEBUG_PRINT(DEBUG_ERROR,"\n Execution Failed on ccSetAnalogChannel()\n");
            response["result"]=getResult_CC(returnvalue,resultDetails);
            response["details"]=resultDetails;
            free(resultDetails);
            return TEST_FAILURE;
        }


    }
    else
    {

        response["result"]="FAILURE";
        response["details"]="Invalid AnalogChannel range 10";
        free(resultDetails);
        return TEST_FAILURE;

    }
    stringDetails = (char*)malloc(sizeof(char)*30);
    returnvalue=ccGetAnalogChannel(&channel);
    sprintf(stringDetails,"%d",channel);
    strcat(stringDetails1,stringDetails);

    DEBUG_PRINT(DEBUG_ERROR,"\nCalling CCAnalogchannel value %s \n",stringDetails1);
    if(returnvalue ==0)
    {
        response["result"]="SUCCESS";
        response["details"]=stringDetails1;
    }
    else
    {
        response["result"]=getResult_CC(returnvalue,resultDetails);
        response["details"]=resultDetails;
    }
    free(stringDetails);
    free(resultDetails);
    return TEST_SUCCESS;

}

/**************************************************************************************************************************
 * @Function Description : CCSetGetAttribute-is used to set and get the  color, Opacity ,size ,style, type ect
 *
 *
 * @Param[in]            :Interger - ccType - 0- Analog, 1-Digital
 *                        Interger - AttributeType ,
 *                        String   -Categories - color, Opacity ,size ,style, type ect String
 *                        Attribute values
 * @return               : Filled with SUCCESS or FAILURE based on the return value of CC API
 *					Attribute values
 **************************************************************************************************************************/


bool CCAgent::CCSetGetAttribute(IN const Json::Value& request, OUT Json::Value& response)
{
    gsw_CcAttributes CCAttribute,CCGetAttribute;
    char *resultDetails;
    int retval,flagValue=0;
    std::string Categories = request["Categories"].asString();
    char *stringDetails ;
    char stringDetails1[30] = "ccAttributeValue :";

    DEBUG_PRINT(DEBUG_ERROR,"\n Categories : color Invalid AttributeType :%d %d %s\n", request["ccType"].asInt(), request["ccAttribute"].asInt(),request["Categories"].asCString());

    gsw_CcType ccType=(gsw_CcType)request["ccType"].asInt();
    gsw_CcAttribType AttributeType=(gsw_CcAttribType)request["ccAttribute"].asInt();


    resultDetails=(char *)malloc(sizeof(char)*16);
    DEBUG_PRINT(DEBUG_ERROR,"\nAttributeType= %d,Categories =%s\n",AttributeType,request["Categories"].asCString());

    if(Categories.compare("color")==0)
    {
        // static unsigned long ccColor=request["value"].asInt();
        int setvalue=request["value"].asInt();
        static unsigned long ccColor=CCSupportedColors[setvalue];
        switch(AttributeType)
        {
        case GSW_CC_ATTRIB_FONT_COLOR:
            CCAttribute.charFgColor.rgb = ccColor;
            flagValue =1;
            break;
        case GSW_CC_ATTRIB_BACKGROUND_COLOR:
            CCAttribute.charBgColor.rgb = ccColor;
            flagValue =2;
            break;
        case GSW_CC_ATTRIB_BORDER_COLOR:
            CCAttribute.borderColor.rgb = ccColor;
            flagValue =3;
            break;
        case GSW_CC_ATTRIB_WIN_COLOR:
            CCAttribute.winColor.rgb = ccColor;
            flagValue =4;
            break;
        case GSW_CC_ATTRIB_EDGE_COLOR:
            CCAttribute.edgeColor.rgb =ccColor;
            flagValue =5;
            break;
        default:
            DEBUG_PRINT(DEBUG_ERROR,"\n Categories : color Invalid AttributeType :%d\n",AttributeType);
            break;

        }
    }
    else if(Categories.compare("Opacity")==0)
    {
        gsw_CcOpacity ccOpacity = (gsw_CcOpacity)request["value"].asInt();
        switch(AttributeType)
        {
        case GSW_CC_ATTRIB_WIN_OPACITY:
            CCAttribute.winOpacity =ccOpacity;
            flagValue =6;
            break;
        case GSW_CC_ATTRIB_BACKGROUND_OPACITY:
            CCAttribute.charBgOpacity =ccOpacity;
            flagValue =7;
            break;
        case GSW_CC_ATTRIB_FONT_OPACITY:
            CCAttribute.charFgOpacity =ccOpacity;
            flagValue=8;
            break;
        default:
            DEBUG_PRINT(DEBUG_ERROR,"\n Categories : Opacity Invalid AttributeType :%d\n",AttributeType);
            break;

        }
    }
    else if(Categories.compare("size")==0)
    {
        gsw_CcFontSize ccSize =(gsw_CcFontSize)request["value"].asInt();
        if (AttributeType == GSW_CC_ATTRIB_FONT_SIZE)
        {
            CCAttribute.fontSize = ccSize;
            flagValue=9;
        }
    }
    else if(Categories.compare("style")==0)
    {
        char *ccStyle = (char *)request["value"].asCString();
        if (AttributeType == GSW_CC_ATTRIB_FONT_STYLE)
        {
            strcpy(CCAttribute.fontStyle,ccStyle);
            flagValue=10;
        }
    }
    else if(Categories.compare("type")==0)
    {
        DEBUG_PRINT(DEBUG_ERROR,"\n Categories :AttributeType :%d \n",AttributeType);
        gsw_CcBorderType ccType =(gsw_CcBorderType)request["value"].asInt();
        gsw_CcEdgeType ccEdgeType=(gsw_CcEdgeType)request["value"].asInt();
        switch(AttributeType)
        {
        case GSW_CC_ATTRIB_BORDER_TYPE:
            CCAttribute.borderType = ccType;
            flagValue =11;
            break;
        case GSW_CC_ATTRIB_EDGE_TYPE:
            CCAttribute.edgeType = ccEdgeType ;
            flagValue=12;

            break;
        default:
            DEBUG_PRINT(DEBUG_ERROR,"\n Categories : type Invalid AttributeType :%d\n",AttributeType);
            break;
        }
    }
    else if(Categories.compare("fontItalic")==0)
    {
        gsw_CcTextStyle ccFontItalic =(gsw_CcTextStyle)request["value"].asInt();
        if (AttributeType == GSW_CC_ATTRIB_FONT_ITALIC)
        {
            CCAttribute.fontItalic = ccFontItalic;
            flagValue=13;
        }
    }
    else if(Categories.compare("fontUnderline")==0)
    {
        gsw_CcTextStyle ccFontUnderline =(gsw_CcTextStyle)request["value"].asInt();
        if (AttributeType == GSW_CC_ATTRIB_FONT_UNDERLINE)
        {
            CCAttribute.fontUnderline = ccFontUnderline;
            flagValue=14;
        }
    }
    else
    {
        DEBUG_PRINT(DEBUG_ERROR,"\n Not a valid Categories  CCSetGetAttributes\n");
        response["result"]= "FAILURE";
        response["details"]="Not a valid Categories for CCSetGetAttributes";
        return TEST_FAILURE;
    }

    try
    {
        ccSetAttributes(&CCAttribute, AttributeType, ccType);
        
    }
    catch(...)
    {
        DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in ccSetAttributes\n");
        response["result"]= "FAILURE";
        response["details"]="Exception Caught in ccSetAttributes()";
        return TEST_FAILURE;

    }
    retval=ccGetAttributes(&CCGetAttribute, ccType);

    DEBUG_PRINT(DEBUG_LOG,"\nCCGetAttribute.charBgColor.rgb : %x\n",CCGetAttribute.charBgColor.rgb);
    DEBUG_PRINT(DEBUG_LOG,"\nCGetAttribute.charFgColor.rgb:%x \n",CCGetAttribute.charFgColor.rgb);
    DEBUG_PRINT(DEBUG_LOG,"\nCCGetAttribute.winColor.rgb : %x\n",CCGetAttribute.winColor.rgb);
    DEBUG_PRINT(DEBUG_LOG,"\nCCGetAttribute.edgeColor : %d\n",CCGetAttribute.edgeColor.rgb);
    DEBUG_PRINT(DEBUG_LOG,"\nCCGetAttribute.charBgOpacity : %d\n",CCGetAttribute.charBgOpacity);
    DEBUG_PRINT(DEBUG_LOG,"\nCGetAttribute.charFgOpacity : %d\n",CCGetAttribute.charFgOpacity);
    DEBUG_PRINT(DEBUG_LOG,"\nCCGetAttribute.winOpacity :%d\n",CCGetAttribute.winOpacity);
    DEBUG_PRINT(DEBUG_LOG,"\nCCCGetAttribute.fontSize :%d\n",CCGetAttribute.fontSize);
    DEBUG_PRINT(DEBUG_LOG,"\nCCGetAttribute.fontStyle :%s\n",CCGetAttribute.fontStyle);
    DEBUG_PRINT(DEBUG_LOG,"\nCCGetAttribute.fontItalic :%d\n",CCGetAttribute.fontItalic);
    DEBUG_PRINT(DEBUG_LOG,"\nCCGetAttribute.fontUnderline :%d\n",CCGetAttribute.fontUnderline);
    DEBUG_PRINT(DEBUG_LOG,"\nCCGetAttribute.borderType :%d\n",CCGetAttribute.borderType);
    DEBUG_PRINT(DEBUG_LOG,"\nCCGetAttribute.edgeType :%d\n",CCGetAttribute.edgeType);

    stringDetails = (char*)malloc(sizeof(char)*30);
    DEBUG_PRINT(DEBUG_ERROR,"\nflagvalue  : %d\n",flagValue);

    switch(flagValue)
    {
    case 1:
        sprintf(stringDetails,"%x",CCGetAttribute.charFgColor.rgb);
        strcat(stringDetails1,stringDetails);
        response["details"]=stringDetails1;
        break;
    case 2:
        sprintf(stringDetails,"%x",CCGetAttribute.charBgColor.rgb);
        strcat(stringDetails1,stringDetails);
        response["details"]=stringDetails;
        //std::cout<<"response[""details""] at switchcase"<<stringDetails<<std::endl;
        //std::cout<<"charBgColor.rgb at switchcase " <<CCGetAttribute.charBgColor.rgb<<std::endl;
        break;
    case 3:
        sprintf(stringDetails,"%x", CCGetAttribute.borderColor.rgb);
        strcat(stringDetails1,stringDetails);
        response["details"]=stringDetails1;
        break;
    case 4:
        sprintf(stringDetails,"%x",CCGetAttribute.winColor.rgb);
        strcat(stringDetails1,stringDetails);
        response["details"]=stringDetails1;
        break;
    case 5:
        sprintf(stringDetails,"%x",CCGetAttribute.edgeColor.rgb);
        strcat(stringDetails1,stringDetails);
        response["details"]=stringDetails1;
        break;
    case 6:
        sprintf(stringDetails,"%d",CCGetAttribute.winOpacity);
        strcat(stringDetails1,stringDetails);
        response["details"]=stringDetails1;
        break;
    case 7:
        sprintf(stringDetails,"%d",CCGetAttribute.charBgOpacity);
        strcat(stringDetails1,stringDetails);
        response["details"]=stringDetails1;
        break;
    case 8:
        sprintf(stringDetails,"%d",CCGetAttribute.charFgOpacity);
        strcat(stringDetails1,stringDetails);
        response["details"]=stringDetails1;
        break;
    case 9:
        sprintf(stringDetails,"%d",CCGetAttribute.fontSize);
        strcat(stringDetails1,stringDetails);
        response["details"]=stringDetails1;
        break;
    case 10:
        strcpy(resultDetails,CCGetAttribute.fontStyle);
        response["details"]=resultDetails;
        break;
    case 11:
        sprintf(stringDetails,"%d",CCGetAttribute.borderType);
        strcat(stringDetails1,stringDetails);
        response["details"]=stringDetails1;
        break;
    case 12:
        sprintf(stringDetails,"%d",CCGetAttribute.edgeType);
        strcat(stringDetails1,stringDetails);
        response["details"]=stringDetails1;
        break;
    case 13:
        sprintf(stringDetails,"%d",CCGetAttribute.fontItalic);
        strcat(stringDetails1,stringDetails);
        response["details"]=stringDetails1;
        break;
    case 14:
        sprintf(stringDetails,"%d",CCGetAttribute.fontUnderline);
        strcat(stringDetails1,stringDetails);
        response["details"]=stringDetails1;
        break;

    }

    DEBUG_PRINT(DEBUG_ERROR,"\nStringDetails  : %s\n",stringDetails1);
    response["result"]=getResult_CC(retval,resultDetails);
    //response["details"]=resultDetails;
        
    free(stringDetails);
    free(resultDetails);
    return TEST_SUCCESS;
}

/*****************************************************************************************************************
 *
 * This CreateObject function for CCAgent class
 *
 *
 ******************************************************************************************************************/

extern "C" CCAgent* CreateObject()
{
    return new CCAgent();
}

/*****************************************************************************************************************
 *
 * This Cleanup function for CCAgent class
 *
 *
 ******************************************************************************************************************/
bool CCAgent::cleanup(IN const char* szVersion,IN RDKTestAgent *ptrAgentObj)
{
    DEBUG_PRINT(DEBUG_LOG,"\n CCAgent shutting down ");
    ptrAgentObj->UnregisterMethod("TestMgr_CC_Init");
    ptrAgentObj->UnregisterMethod("TestMgr_CC_SetGetState");
    ptrAgentObj->UnregisterMethod("TestMgr_CC_SetGetAttribute");
    ptrAgentObj->UnregisterMethod("TestMgr_CC_SetGetDigitalChannel");
    ptrAgentObj->UnregisterMethod("TestMgr_CC_SetGetAnalogChannel");
    ptrAgentObj->UnregisterMethod("TestMgr_CC_Show");
    ptrAgentObj->UnregisterMethod("TestMgr_CC_Hide");
    ptrAgentObj->UnregisterMethod("TestMgr_CC_GetSupportedServiceNumberCount");
    ptrAgentObj->UnregisterMethod("TestMgr_CC_GetSupportedServiceNumber");
    ptrAgentObj->UnregisterMethod("TestMgr_CC_OnEasStart");
    ptrAgentObj->UnregisterMethod("TestMgr_CC_OnEasStop");
    ptrAgentObj->UnregisterMethod("TestMgr_CC_SetTrickPlayStatus");
    ptrAgentObj->UnregisterMethod("TestMgr_CC_ResetTrickPlayStatus");
    return TEST_SUCCESS;
}

/**************************************************************************
Function name : CCAgent::DestroyObject()

Arguments     : Input argument is CCAgent Stub Object

Description   : Delete CC stub object
***************************************************************************/
extern "C" void DestroyObject(CCAgent *stubobj)
{
    DEBUG_PRINT(DEBUG_TRACE, "Destroying Object\n");
    delete stubobj;
}
