/*
 * If not stated otherwise in this file or this component's Licenses.txt file the
 * following copyright and licenses apply:
 *
 * Copyright 2018 RDK Management
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

#include "WIFIHAL.h"
/***************************************************************************
 *Function name : testmodulepre_requisites
 *Description   : testmodulepre_requisites will be used for setting the
 *                pre-requisites that are necessary for this component
 *
 *****************************************************************************/

std::string WIFIHAL::testmodulepre_requisites()
{
    return "SUCCESS";
}

/***************************************************************************
 *Function name : testmodulepost_requisites
 *Description    : testmodulepost_requisites will be used for resetting the
 *                pre-requisites that are set
 *
 *****************************************************************************/
bool WIFIHAL::testmodulepost_requisites()
{
    return true;
}

/**************************************************************************
Function Name   : CreateObject

Arguments       : NULL

Description     : This function is used to create a new object of the class "WIFIHAL".
**************************************************************************/

extern "C" WIFIHAL* CreateObject(TcpSocketServer &ptrtcpServer)
{
        return new WIFIHAL(ptrtcpServer);
}

/***************************************************************************
 *Function name : initialize
 *Description    : Initialize Function will be used for registering the wrapper method
 *                with the agent so that wrapper functions will be used in the
 *                script
 *****************************************************************************/

bool WIFIHAL::initialize(IN const char* szVersion)
{
    return TEST_SUCCESS;
}

/*******************************************************************************************
 *
 * Function Name        : WIFI_HAL_Init
 * Description          : This function invokes WiFi hal api wifi_init()

 * @param [in] req-     : NIL
 * @param [out] response - filled with SUCCESS or FAILURE based on the output status of operation
 *
 ********************************************************************************************/
void WIFIHAL::WIFI_HAL_Init (IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE,"\n WIFI_HAL_Init ----->Entry\n");

    int returnValue;
    char details[200] = {'\0'};

    returnValue = wifi_init();
    if(0 == returnValue)
       {
            sprintf(details, "wifi_init operation success");
            response["result"]="SUCCESS";
            response["details"]=details;
            return;
       }
    else
       {
            sprintf(details, "wifi_init operation failed");
            response["result"]="FAILURE";
            response["details"]=details;
            return;
       }
    DEBUG_PRINT(DEBUG_TRACE,"\n WIFI_HAL_Init --->Exit\n");
}

/*******************************************************************************************
 *
 * Function Name        : WIFI_HAL_Down
 * Description          : This function invokes WiFi hal api wifi_down()

 * @param [in] req-     : NIL
 * @param [out] response - filled with SUCCESS or FAILURE based on the output status of operation
 *
 ********************************************************************************************/
void WIFIHAL::WIFI_HAL_Down (IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE,"\n WIFI_HAL_Down ----->Entry\n");

    int returnValue;
    char details[200] = {'\0'};
    returnValue = wifi_down();
    if(0 == returnValue)
       {
            sprintf(details, "wifi_down operation success");
            response["result"]="SUCCESS";
            response["details"]=details;
       }
    else
       {
            sprintf(details, "wifi_down operation failed");
            response["result"]="FAILURE";
            response["details"]=details;
            return;
       }
    DEBUG_PRINT(DEBUG_TRACE,"\n WIFI_HAL_Down --->Exit\n");
}
/*******************************************************************************************
 *
 * Function Name        : WIFI_HAL_Uninit
 * Description          : This function invokes WiFi hal api wifi_uninit()

 * @param [in] req-     : NIL
 * @param [out] response - filled with SUCCESS or FAILURE based on the output status of operation
 *
 ********************************************************************************************/
void WIFIHAL::WIFI_HAL_Uninit (IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE,"\n WIFI_HAL_Uninit ----->Entry\n");

    int returnValue;
    char details[200] = {'\0'};

    returnValue = wifi_uninit();
    if(0 == returnValue)
       {
            sprintf(details, "wifi_uninit operation success");
            response["result"]="SUCCESS";
            response["details"]=details;
            return;
       }
    else
       {
            sprintf(details, "wifi_uninit operation failed");
            response["result"]="FAILURE";
            response["details"]=details;
            return;
       }
    DEBUG_PRINT(DEBUG_TRACE,"\n WIFI_HAL_Uninit --->Exit\n");
}
/*******************************************************************************************
 *
 * Function Name        : WIFI_HAL_GetOrSetParamStringValue
 * Description          : This function invokes WiFi hal's get/set apis, when the value to be
                          get /set is string
 *
 * @param [in] req-    : methodName - identifier for the hal api name
                          radioIndex - radio index value of wifi
                          param     - the string value to be get/set
                          paramType  - To indicate negative test scenario. it is set as NULL for negative sceanario, otherwise empty
 * @param [out] response - filled with SUCCESS or FAILURE based on the output staus of operation
 *
 ********************************************************************************************/
void WIFIHAL::WIFI_HAL_GetOrSetParamStringValue(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE,"\n WIFIHAL_GetOrSetParamStringValue --->Entry\n");
    char methodName[50] = {'\0'};
    int radioIndex;
    char output[1000] = {'\0'};
    int returnValue;
    char details[200] = {'\0'};
    char paramType[10] = {'\0'};
    char param[200] = {'\0'};

    strcpy(methodName, req["methodName"].asCString());
    radioIndex = req["radioIndex"].asInt();
    strcpy(paramType, req["paramType"].asCString());
    strcpy(param, req["param"].asCString());
    if(!strcmp(methodName, "getRadioSupportedFrequencyBands"))
        returnValue = wifi_getRadioSupportedFrequencyBands(radioIndex,output);
    else if(!strcmp(methodName, "getRadioIfName"))
	returnValue = wifi_getRadioIfName(radioIndex,output);
    else if(!strcmp(methodName, "getRadioOperatingFrequencyBand"))
	returnValue = wifi_getRadioOperatingFrequencyBand(radioIndex,output);
    else if(!strcmp(methodName, "getRadioSupportedStandards"))
	returnValue = wifi_getRadioSupportedStandards(radioIndex,output);
    else if(!strcmp(methodName, "getRadioPossibleChannels"))
	returnValue = wifi_getRadioPossibleChannels(radioIndex,output);
    else if(!strcmp(methodName, "getRadioChannelsInUse"))
	returnValue = wifi_getRadioChannelsInUse(radioIndex,output);
    else if(!strcmp(methodName, "getRadioPossibleChannels"))
	returnValue = wifi_getRadioPossibleChannels(radioIndex,output);
    else if(!strcmp(methodName, "getRadioOperatingChannelBandwidth"))
	returnValue = wifi_getRadioOperatingChannelBandwidth(radioIndex,output);
    else if(!strcmp(methodName, "getRegulatoryDomain"))
        returnValue = wifi_getRegulatoryDomain(radioIndex,output);
    else if(!strcmp(methodName, "getSSIDName"))
        returnValue = wifi_getSSIDName(radioIndex,output);
    else if(!strcmp(methodName, "getBaseBSSID"))
        returnValue = wifi_getBaseBSSID(radioIndex,output);
    else if(!strcmp(methodName, "getSSIDMACAddress"))
        returnValue = wifi_getSSIDMACAddress(radioIndex,output);
    else if(!strcmp(methodName, "getRadioStatus"))
        returnValue = wifi_getRadioStatus(radioIndex,output);
    else if(!strcmp(methodName, "getRadioExtChannel"))
        returnValue = wifi_getRadioExtChannel(radioIndex,output);
    else if(!strcmp(methodName, "getHalVersion"))
        returnValue = wifi_getHalVersion(output);
    else if(!strcmp(methodName, "getCliWpsConfigMethodsSupported"))
        returnValue = wifi_getCliWpsConfigMethodsSupported(radioIndex,output);
    else if(!strcmp(methodName, "getCliWpsConfigMethodsEnabled"))
        returnValue = wifi_getCliWpsConfigMethodsEnabled(radioIndex,output);
    else if(!strcmp(methodName, "setCliWpsConfigMethodsEnabled"))
        returnValue = wifi_setCliWpsConfigMethodsEnabled(radioIndex,output);
    else
    {
        returnValue = TEST_FAILURE;
        printf("\n WIFIHAL_GetOrSetParamStringValue: Invalid methodName\n");
    }

    printf("return status of the api call: %d\n",returnValue);

    if(0 == returnValue)
    {
        sprintf(details, "output : %s", output);
        response["result"]="SUCCESS";
        response["details"]=details;
        return;
    }
    else
    {
        sprintf(details, "%s operation failed", methodName);
        response["result"]="FAILURE";
        response["details"]=details;
        return;
    }

    DEBUG_PRINT(DEBUG_TRACE,"\n WIFIHAL_GetOrSetParamStringValue --->Exit\n");
    return;
}


/*******************************************************************************************
 *
 * Function Name        : WIFI_HAL_GetOrSetParamULongValue
 * Description          : This function invokes WiFi hal's get/set apis, when the value to be
                          get /set is Unsigned long
 *
 * @param [in] req-    : methodName - identifier for the hal api name
                         radioIndex - radio index value of wifi
                         param     - the ulong value to be get/set
                         paramType  - To indicate negative test scenario. it is set as NULL for negative scenario, otherwise empty
 * @param [out] response - filled with SUCCESS or FAILURE based on the output staus of operation
 *
 ********************************************************************************************/
void WIFIHAL::WIFI_HAL_GetOrSetParamULongValue(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE,"\n WIFI_HAL_GetOrSetParamULongValue------>Entry\n");
    char methodName[50] = {'\0'};
    int radioIndex = 1;
    unsigned long uLongVar = 1;
    int returnValue;
    char details[200] = {'\0'};
    char paramType[10] = {'\0'};

    strcpy(methodName, req["methodName"].asCString());
    radioIndex = req["radioIndex"].asInt();
    uLongVar = (unsigned long)req["param"].asLargestUInt();
    strcpy(paramType, req["paramType"].asCString());

    if(!strcmp(methodName, "getRadioChannel"))
        returnValue = wifi_getRadioChannel(radioIndex,&uLongVar);
    else if(!strcmp(methodName, "getRadioNumberOfEntries"))
        returnValue = wifi_getRadioNumberOfEntries(&uLongVar);
    else if(!strcmp(methodName, "getSSIDNumberOfEntries"))
        returnValue = wifi_getSSIDNumberOfEntries(&uLongVar);
    else
    {
        returnValue = TEST_FAILURE;
        printf("\n WIFI_HAL_GetOrSetParamULongValue: Invalid methodName\n");
	return;
    }
    printf("return status of the api call: %d",returnValue);

    if(0 == returnValue)
    {
        DEBUG_PRINT(DEBUG_TRACE,"\n output: %lu\n",uLongVar);
        sprintf(details, "Value returned is :%lu", uLongVar);
        response["result"]="SUCCESS";
        response["details"]=details;
        return;
    }
    else
    {
        sprintf(details, "%s operation failed", methodName);
        response["result"]="FAILURE";
        response["details"]=details;
        return;
    }

    DEBUG_PRINT(DEBUG_TRACE,"\n WIFI_HAL_GetOrSetParamULongValue --->Exit\n");
    return;
}

/*******************************************************************************************
 *
 * Function Name        : WIFI_HAL_GetOrSetParamBoolValue
 * Description          : This function invokes WiFi hal's get/set apis, when the value to be
                          get /set is BOOL
 *
 * @param [in] req-    : methodName - identifier for the hal api name
                          radioIndex - radio index value of wifi
                          enable     - the bool value to be get/set
                          paramType  - To indicate negative test scenario. it is set as NULL for negative scenario, otherwise empty
 * @param [out] response - filled with SUCCESS or FAILURE based on the output staus of operation
 *
 ********************************************************************************************/
void WIFIHAL::WIFI_HAL_GetOrSetParamBoolValue(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE,"\n WIFI_HAL_GetOrSetParamBoolValue --->Entry\n");
    char methodName[50] = {'\0'};
    int radioIndex;
    unsigned char enable;
    int returnValue;
    char details[200] = {'\0'};
    char paramType[10] = {'\0'};

    strcpy(methodName, req["methodName"].asCString());
    radioIndex = req["radioIndex"].asInt();
    enable = req["param"].asInt();
    strcpy(paramType, req["paramType"].asCString());

    if(!strcmp(methodName, "getRadioEnable"))
        returnValue = wifi_getRadioEnable(radioIndex,&enable);
    else
    {
        returnValue = TEST_FAILURE;
        printf("\n WIFI_HAL_GetOrSetParamULongValue: Invalid methodName\n");
        return;
    }
    printf("return status of the api call: %d",returnValue);

    if(0 == returnValue)
    {
        DEBUG_PRINT(DEBUG_TRACE,"\n enable: %u\n",enable);
        sprintf(details, "Value returned is :%u", enable);
        response["result"]="SUCCESS";
        response["details"]=details;
        return;
    }
    else
    {
        sprintf(details, "%s operation failed", methodName);
        response["result"]="FAILURE";
        response["details"]=details;
        return;
    }

    DEBUG_PRINT(DEBUG_TRACE,"\n WIFI_HAL_GetOrSetParamBoolValue --->Exit\n");
    return;
}

/*******************************************************************************************
 *
 * Function Name        : WIFI_HAL_GetOrSetRadioStandard
 * Description          : This function invokes WiFi hal's get/set apis, when the value to be
                          get /set is a string
 *
 * @param [in] req-    : methodName - identifier for the hal api name
                          radioIndex - radio index value of wifi
                          param     - the string value to be get
                          paramType  - To indicate negative test scenario. it is set as NULL for negative scenario, otherwise empty
                          gOnly, nOnly, acOnly - the bool values to be set/get
 * @param [out] response - filled with SUCCESS or FAILURE based on the output staus of operation
 *
 ********************************************************************************************/
void WIFIHAL::WIFI_HAL_GetOrSetRadioStandard(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE,"\n WIFI_HAL_GetOrSetParamRadioStandard ----->Entry\n");
    char methodName[50] = {'\0'};
    int radioIndex = 1;
    char output[1000] = {'\0'};
    int returnValue;
    char details[200] = {'\0'};
    char paramType[10] = {'\0'};
    char param[200] = {'\0'};
    unsigned char gOnly, nOnly, acOnly;

    strcpy(methodName, req["methodName"].asCString());
    radioIndex = req["radioIndex"].asInt();
    strcpy(paramType, req["paramType"].asCString());
    strcpy(param, req["param"].asCString());

    if(!strcmp(methodName, "getRadioStandard"))
        returnValue = wifi_getRadioStandard(radioIndex, output, &gOnly, &nOnly, &acOnly);
    else
    {
        returnValue = TEST_FAILURE;
        printf("\n WIFI_HAL_GetOrSetRadioStandard: Invalid methodName\n");
        return;
    }
    printf("returnValue: %d",returnValue);
//add apply settings steps here

    if(0 == returnValue)
    {
        DEBUG_PRINT(DEBUG_TRACE,"\n output: %s\n",output);
        sprintf(details, "Value returned is :output=%s,gOnly=%d,nOnly=%d,acOnly=%d", output,gOnly,nOnly,acOnly);
        response["result"]="SUCCESS";
        response["details"]=details;
        return;
    }
    else
    {
        sprintf(details, "%s operation failed", methodName);
        response["result"]="FAILURE";
        response["details"]=details;
        DEBUG_PRINT(DEBUG_TRACE,"\n WiFiCallMethodForRadioStandard --->Error in execution\n");
        return;
    }
}
/*******************************************************************************************
 *
 * Function Name        : WIFIHAL_GetRadiotrafficStats
 * Description          : This function invokes WiFi hal get api which are
                          related to wifi_getRadiotrafficStats()

 * @param [in] req-     : NIL
 * @param [out] response - filled with SUCCESS or FAILURE based on the output status of operation
 *
 ********************************************************************************************/
void WIFIHAL::WIFI_HAL_GetRadioTrafficStats (IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE,"\n WIFI_HAL_GetRadiotrafficStats ----->Entry\n");
    wifi_radioTrafficStats_t trafficStats;
    int radioIndex = 1;
    int returnValue;
    char details[1000] = {'\0'};
    radioIndex = req["radioIndex"].asInt();
    returnValue = wifi_getRadioTrafficStats(radioIndex, &trafficStats);
    if(0 == returnValue)
    {
        sprintf(details, "Value returned is :radio_BytesSent=%lu,radio_BytesReceived=%lu,radio_PacketsSent=%lu,radio_PacketsReceived=%lu,radio_ErrorsSent=%lu,radio_ErrorsReceived=%lu,radio_DiscardPacketsSent=%lu,radio_DiscardPacketsReceived=%lu,radio_PLCPErrorCount=%lu,radio_FCSErrorCount=%lu,radio_InvalidMACCount=%lu,radio_PacketsOtherReceived=%lu,radio_NoiseFloor=%d,radio_ChannelUtilization=%lu,radio_ActivityFactor=%d,radio_CarrierSenseThreshold_Exceeded=%d,radio_RetransmissionMetirc=%d,radio_MaximumNoiseFloorOnChannel=%d,radio_MinimumNoiseFloorOnChannel=%d,radio_MedianNoiseFloorOnChannel=%d,radio_StatisticsStartTime=%lu",trafficStats.radio_BytesSent,trafficStats.radio_BytesReceived,trafficStats.radio_PacketsSent,trafficStats.radio_PacketsReceived,trafficStats.radio_ErrorsSent,trafficStats.radio_ErrorsReceived,trafficStats.radio_DiscardPacketsSent,trafficStats.radio_DiscardPacketsReceived,trafficStats.radio_PLCPErrorCount,trafficStats.radio_FCSErrorCount,trafficStats.radio_InvalidMACCount,trafficStats.radio_PacketsOtherReceived,trafficStats.radio_NoiseFloor,trafficStats.radio_ChannelUtilization,trafficStats.radio_ActivityFactor,trafficStats.radio_CarrierSenseThreshold_Exceeded,trafficStats.radio_RetransmissionMetirc,trafficStats.radio_MaximumNoiseFloorOnChannel,trafficStats.radio_MinimumNoiseFloorOnChannel,trafficStats.radio_MedianNoiseFloorOnChannel,trafficStats.radio_StatisticsStartTime);
        response["result"]="SUCCESS";
        response["details"]=details;
        return;
    }
    else
    {
        sprintf(details, "wifi_getRadioTrafficStats operation failed");
        response["result"]="FAILURE";
        response["details"]=details;
        DEBUG_PRINT(DEBUG_TRACE,"\n WiFiCallMethodForGetRadioTrafficStats  --->Error in execution\n");
        return;
    }
}
/*******************************************************************************************
 *
 * Function Name        : WIFI_HAL_GetSSIDTrafficStats
 * Description          : This function invokes WiFi hal api wifi_getSSIDTrafficStats

 * @param [in] req-     : radioIndex - radio index of the wifi
 * @param [out] response - filled with SUCCESS or FAILURE based on the output status of operation
 *
 ********************************************************************************************/
void WIFIHAL::WIFI_HAL_GetSSIDTrafficStats(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE,"\n WIFI_HAL_GetSSIDTrafficStats ----->Entry\n");

    wifi_ssidTrafficStats_t ssidTrafficStats;
    int radioIndex = 1;
    int returnValue;
    char details[1000] = {'\0'};

    radioIndex = req["radioIndex"].asInt();

    returnValue = wifi_getSSIDTrafficStats(radioIndex, &ssidTrafficStats);
    if(0 == returnValue)
    {
        sprintf(details, "Value returned is :ssid_BytesSent=%lu,ssid_BytesReceived=%lu,ssid_PacketsSent=%lu,ssid_PacketsReceived=%lu,ssid_RetransCount=%lu,ssid_FailedRetransCount=%lu,ssid_RetryCount=%lu,ssid_MultipleRetryCount=%lu,ssid_ACKFailureCount=%lu,ssid_AggregatedPacketCount=%lu,ssid_ErrorsSent=%lu,ssid_ErrorsReceived=%lu,ssid_UnicastPacketsSent=%lu,ssid_UnicastPacketsReceived=%lu,ssid_DiscardedPacketsSent=%lu,ssid_DiscardedPacketsReceived=%lu,ssid_MulticastPacketsSent=%lu,ssid_MulticastPacketsReceived=%lu,ssid_BroadcastPacketsSent=%lu,ssid_BroadcastPacketsRecevied=%lu,ssid_UnknownPacketsReceived=%lu\n",ssidTrafficStats.ssid_BytesSent,ssidTrafficStats.ssid_BytesReceived,ssidTrafficStats.ssid_PacketsSent,ssidTrafficStats.ssid_PacketsReceived,ssidTrafficStats.ssid_RetransCount,ssidTrafficStats.ssid_FailedRetransCount,ssidTrafficStats.ssid_RetryCount,ssidTrafficStats.ssid_MultipleRetryCount,ssidTrafficStats.ssid_ACKFailureCount,ssidTrafficStats.ssid_AggregatedPacketCount,ssidTrafficStats.ssid_ErrorsSent,ssidTrafficStats.ssid_ErrorsReceived,ssidTrafficStats.ssid_UnicastPacketsSent,ssidTrafficStats.ssid_UnicastPacketsReceived,ssidTrafficStats.ssid_DiscardedPacketsSent,ssidTrafficStats.ssid_DiscardedPacketsReceived,ssidTrafficStats.ssid_MulticastPacketsSent,ssidTrafficStats.ssid_MulticastPacketsReceived,ssidTrafficStats.ssid_BroadcastPacketsSent,ssidTrafficStats.ssid_BroadcastPacketsRecevied,ssidTrafficStats.ssid_UnknownPacketsReceived);
        response["result"]="SUCCESS";
        response["details"]=details;
        return;
    }
    else
    {
        sprintf(details, "wifi_getSSIDTrafficStats operation failed");
        response["result"]="FAILURE";
        response["details"]=details;
        DEBUG_PRINT(DEBUG_TRACE,"\n WIFI_HAL_GetSSIDTrafficStats ---->Error in execution\n");
        return;
    }
}
/*******************************************************************************************
 *
 * Function Name        : WIFI_HAL_GetNeighboringWiFiDiagnosticResult
 * Description          : This function invokes WiFi hal api wifi_getNeighboringWiFiDiagnosticResult

 * @param [in] req-     : radioIndex - radio index of the wifi
 * @param [out] response - filled with SUCCESS or FAILURE based on the output status of operation
 *
 ********************************************************************************************/
void WIFIHAL::WIFI_HAL_GetNeighboringWiFiDiagnosticResult(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE,"\n WIFI_HAL_GetNeighboringWiFiDiagnosticResult ----->Entry\n");

    wifi_neighbor_ap_t *neighbor_ap;
    unsigned int output_array_size;
    int radioIndex = 1;
    int returnValue;
    char details[1000] = {'\0'};

    radioIndex = req["radioIndex"].asInt();

    returnValue = wifi_getNeighboringWiFiDiagnosticResult(radioIndex, &neighbor_ap, &output_array_size);
    if(0 == returnValue)
    {
        sprintf(details, "Value returned is :ap_SSID=%s,ap_BSSID=%s,ap_Mode=%s,ap_Channel=%d,ap_SignalStrength=%d,ap_SecurityModeEnabled=%s,ap_EncryptionMode=%s,ap_OperatingFrequencyBand=%s,ap_SupportedStandards=%s,ap_OperatingStandards=%s,ap_OperatingChannelBandwidth=%s,ap_BeaconPeriod=%d,ap_Noise=%d,ap_BasicDataTransferRates=%s,ap_SupportedDataTransferRates=%s,ap_DTIMPeriod=%d,ap_ChannelUtilization=%d,output_array_size=%u",neighbor_ap->ap_SSID,neighbor_ap->ap_BSSID,neighbor_ap->ap_Mode,neighbor_ap->ap_Channel,neighbor_ap->ap_SignalStrength,neighbor_ap->ap_SecurityModeEnabled,neighbor_ap->ap_EncryptionMode,neighbor_ap->ap_OperatingFrequencyBand,neighbor_ap->ap_SupportedStandards,neighbor_ap->ap_OperatingStandards,neighbor_ap->ap_OperatingChannelBandwidth,neighbor_ap->ap_BeaconPeriod,neighbor_ap->ap_Noise,neighbor_ap->ap_BasicDataTransferRates,neighbor_ap->ap_SupportedDataTransferRates,neighbor_ap->ap_DTIMPeriod,neighbor_ap->ap_ChannelUtilization,output_array_size);
        response["result"]="SUCCESS";
        response["details"]=details;
        return;
    }
    else
    {
        sprintf(details, "wifi_getNeighboringWiFiDiagnosticResult operation failed");
        response["result"]="FAILURE";
        response["details"]=details;
        DEBUG_PRINT(DEBUG_TRACE,"\n WIFI_HAL_GetNeighboringWiFiDiagnosticResult ---->Error in execution\n");
        return;
    }
}

/*******************************************************************************************
 *
 * Function Name        : WIFI_HAL_ConnectEndpoint
 * Description          : This function invokes WiFi hal api wifi_connectEndpoint()
 *
 * @param [in] req-    : methodName - identifier for the hal api name
                          radioIndex - radio index value of wifi
                          param     - the string value to be get
                          paramType  - To indicate negative test scenario. it is set as NULL for negative sceanario, otherwise empty
                          gOnly, nOnly, acOnly - the bool values to be set/get
 * @param [out] response - filled with SUCCESS or FAILURE based on the output staus of operation
 *
 ********************************************************************************************/
void WIFIHAL::WIFI_HAL_ConnectEndpoint(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE,"\n WIFI_HAL_ConnectEndpoint ----->Entry\n");
    int radioIndex = 1;
    int returnValue;
    char details[200] = {'\0'};

    radioIndex = req["radioIndex"].asInt();

    char ap_ssid[10] = "1";
    wifiSecurityMode_t AP_security_mode = WIFI_SECURITY_WPA_PSK_AES;
    char AP_security_WEPKey[30] = "1";
    char AP_security_PreSharedKey[30] = "factor8490fifty";
    char AP_security_KeyPassphrase[30] = "factor8490fifty";
    int saveSSID = 1;
    char eapIdentity[20];
    char carootcert[20];
    char clientcert[20];
    char privatekey[20];
    returnValue = wifi_connectEndpoint(radioIndex, ap_ssid,AP_security_mode,AP_security_WEPKey,AP_security_PreSharedKey,AP_security_KeyPassphrase,saveSSID,eapIdentity,carootcert,clientcert,privatekey);
    printf("return status from api call: %d",returnValue);

    if(0 == returnValue)
    {
        sprintf(details, "wifi_connectEndpoint operation success");
        response["result"]="SUCCESS";
        response["details"]=details;
        return;
    }
    else
    {
        sprintf(details, "wifi_connectEndpoint operation failed");
        response["result"]="FAILURE";
        response["details"]=details;
        DEBUG_PRINT(DEBUG_TRACE,"\n WIFI_HAL_ConnectEndpoint --->Error in execution\n");
        return;
    }
}
/*******************************************************************************************
 *
 * Function Name        : WIFI_HAL_LastConnected_Endpoint
 * Description          : This function invokes WiFi hal api wifi_lastConnected_Endpoint()
 *
 * @param [in] req-    : methodName - identifier for the hal api name
                          radioIndex - radio index value of wifi
                          param     - the string value to be get
                          paramType  - To indicate negative test scenario. it is set as NULL for negative sceanario, otherwise empty
 * @param [out] response - filled with SUCCESS or FAILURE based on the output staus of operation
 *
 ********************************************************************************************/
void WIFIHAL::WIFI_HAL_LastConnected_Endpoint(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE,"\n WIFI_HAL_LastConnected_Endpoint ------>Entry\n");
    int returnValue;
    char details[500] = {'\0'};

    wifi_pairedSSIDInfo_t *pairedSSIDInfo;

    returnValue=wifi_lastConnected_Endpoint(pairedSSIDInfo);

    printf("return status from api call: %d",returnValue);

    if(0 == returnValue)
    {
        sprintf(details, "Value returned is :ap_ssid=%s,ap_bssid=%s,ap_security=%s,ap_passphrase=%s",pairedSSIDInfo->ap_ssid,pairedSSIDInfo->ap_bssid,pairedSSIDInfo->ap_security,pairedSSIDInfo->ap_passphrase);
        response["result"]="SUCCESS";
        response["details"]=details;
        return;
    }
    else
    {
        sprintf(details, "wifi_lastConnected_Endpoint operation failed");
        response["result"]="FAILURE";
        response["details"]=details;
        DEBUG_PRINT(DEBUG_TRACE,"\n WIFI_HAL_LastConnected_Endpoint --->Error in execution\n");
        return;
    }
}

/*******************************************************************************************
 *
 * Function Name        : WIFI_HAL_DisconnectEndpoint
 * Description          : This function invokes WiFi hal api wifi_disconnectEndpoint()
 *
 * @param [in] req-    : methodName - identifier for the hal api name
                          radioIndex - radio index value of wifi
                          param     - the string value to be get
                          paramType  - To indicate negative test scenario. it is set as NULL for negative sceanario, otherwise empty
 * @param [out] response - filled with SUCCESS or FAILURE based on the output staus of operation
 *
 ********************************************************************************************/
void WIFIHAL::WIFI_HAL_DisconnectEndpoint(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE,"\n WIFI_HAL_DisconnectEndpoint ------>Entry\n");
    int radioIndex = 1;
    int returnValue;
    char details[500] = {'\0'};
    char ap_ssid[10] = "1";

    radioIndex = req["radioIndex"].asInt();

    returnValue=wifi_disconnectEndpoint(radioIndex,ap_ssid);

    printf("return status from api call: %d",returnValue);

    if(0 == returnValue)
    {
        sprintf(details, "wifi_disconnectEndpoint operation success");
        response["result"]="SUCCESS";
        response["details"]=details;
        return;
    }
    else
    {
        sprintf(details, "wifi_disconnectEndpoint operation failed");
        response["result"]="FAILURE";
        response["details"]=details;
        DEBUG_PRINT(DEBUG_TRACE,"\n WIFI_HAL_DisconnectEndpoint --->Error in execution\n");
        return;
    }
}

/**************************************************************************
Function Name   : cleanup

Arguments       : NULL

Description     : This function will be used to the close things cleanly.
 **************************************************************************/
bool WIFIHAL::cleanup(IN const char* szVersion)
{
    DEBUG_PRINT(DEBUG_LOG,"WIFIHAL shutting down\n");
    return TEST_SUCCESS;
}

/**************************************************************************
Function Name : DestroyObject

Arguments     : Input argument is WIFIHAL Object

Description   : This function will be used to destory the WIFIHAL object.
**************************************************************************/
extern "C" void DestroyObject(WIFIHAL *stubobj)
{
        DEBUG_PRINT(DEBUG_LOG, "Destroying WIFIHAL Agent object\n");
        delete stubobj;
}
