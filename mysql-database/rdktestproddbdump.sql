-- MySQL dump 10.13  Distrib 5.5.38, for debian-linux-gnu (i686)
--
-- Host: localhost    Database: rdktesttoolproddb
-- ------------------------------------------------------
-- Server version	5.5.38-0ubuntu0.12.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `box_manufacturer`
--

DROP TABLE IF EXISTS `box_manufacturer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `box_manufacturer` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `version` bigint(20) NOT NULL,
  `name` varchar(255) NOT NULL,
  `groups_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `FK3D2E11C5984B586A` (`groups_id`),
  CONSTRAINT `FK3D2E11C5984B586A` FOREIGN KEY (`groups_id`) REFERENCES `groups` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `box_manufacturer`
--

LOCK TABLES `box_manufacturer` WRITE;
/*!40000 ALTER TABLE `box_manufacturer` DISABLE KEYS */;
INSERT INTO `box_manufacturer` VALUES (2,0,'Broadcom',NULL),(3,0,'Cisco',NULL),(4,0,'Entropic',NULL),(5,0,'Humax',NULL),(6,0,'Intel',NULL),(7,0,'Motorola',NULL),(8,0,'Pace',NULL),(9,0,'Samsung',NULL),(10,0,'Technicolor',NULL);
/*!40000 ALTER TABLE `box_manufacturer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `box_model`
--

DROP TABLE IF EXISTS `box_model`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `box_model` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `version` bigint(20) NOT NULL,
  `name` varchar(255) NOT NULL,
  `groups_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `FK411117B5984B586A` (`groups_id`),
  CONSTRAINT `FK411117B5984B586A` FOREIGN KEY (`groups_id`) REFERENCES `groups` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;



--
-- Table structure for table `box_type`
--

DROP TABLE IF EXISTS `box_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `box_type` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `version` bigint(20) NOT NULL,
  `name` varchar(255) NOT NULL,
  `type` varchar(255) NOT NULL,
  `groups_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `FK863DB12E984B586A` (`groups_id`),
  CONSTRAINT `FK863DB12E984B586A` FOREIGN KEY (`groups_id`) REFERENCES `groups` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `box_type`
--

LOCK TABLES `box_type` WRITE;
/*!40000 ALTER TABLE `box_type` DISABLE KEYS */;
INSERT INTO `box_type` VALUES (1,0,'IPClient-3','Client',NULL),(2,0,'Hybrid-1','Gateway',NULL),(3,0,'Hybrid-5','Gateway',NULL);
/*!40000 ALTER TABLE `box_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `device`
--

DROP TABLE IF EXISTS `device`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `device` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `version` bigint(20) NOT NULL,
  `box_manufacturer_id` bigint(20) NOT NULL,
  `box_type_id` bigint(20) NOT NULL,
  `device_status` varchar(255) NOT NULL,
  `socvendor_id` bigint(20) NOT NULL,
  `stb_ip` varchar(255) NOT NULL,
  `stb_name` varchar(255) NOT NULL,
  `stb_port` varchar(255) NOT NULL,
  `gateway_ip` varchar(255) DEFAULT NULL,
  `recorder_id` varchar(255) DEFAULT NULL,
  `upload_binary_status` varchar(255) NOT NULL,
  `log_transfer_port` varchar(255) NOT NULL,
  `status_port` varchar(255) NOT NULL,
  `mac_id` varchar(255) DEFAULT NULL,
  `child_devices` varchar(255) DEFAULT NULL,
  `is_child` int(11) NOT NULL,
  `groups_id` bigint(20) DEFAULT NULL,
  `agent_monitor_port` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `stb_name` (`stb_name`),
  KEY `FKB06B1E56D70E4BBC` (`box_manufacturer_id`),
  KEY `FKB06B1E5641CE91C` (`box_type_id`),
  KEY `FKB06B1E565DC65445` (`socvendor_id`),
  KEY `FKB06B1E56984B586A` (`groups_id`),
  CONSTRAINT `FKB06B1E5641CE91C` FOREIGN KEY (`box_type_id`) REFERENCES `box_type` (`id`),
  CONSTRAINT `FKB06B1E565DC65445` FOREIGN KEY (`socvendor_id`) REFERENCES `socvendor` (`id`),
  CONSTRAINT `FKB06B1E56984B586A` FOREIGN KEY (`groups_id`) REFERENCES `groups` (`id`),
  CONSTRAINT `FKB06B1E56D70E4BBC` FOREIGN KEY (`box_manufacturer_id`) REFERENCES `box_manufacturer` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6463 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;



--
-- Table structure for table `device_details`
--

DROP TABLE IF EXISTS `device_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `device_details` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `version` bigint(20) NOT NULL,
  `device_id` bigint(20) NOT NULL,
  `device_parameter` varchar(255) NOT NULL,
  `device_value` longtext,
  PRIMARY KEY (`id`),
  KEY `FKD2D30159EC4FF12A` (`device_id`),
  CONSTRAINT `FKD2D30159EC4FF12A` FOREIGN KEY (`device_id`) REFERENCES `device` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23185 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;



--
-- Table structure for table `device_device`
--

DROP TABLE IF EXISTS `device_device`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `device_device` (
  `device_child_devices_id` bigint(20) DEFAULT NULL,
  `device_id` bigint(20) DEFAULT NULL,
  `child_devices_idx` int(11) DEFAULT NULL,
  KEY `FKABF7505FBC11ECEF` (`device_id`),
  CONSTRAINT `FKABF7505FBC11ECEF` FOREIGN KEY (`device_id`) REFERENCES `device` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;



--
-- Table structure for table `device_group`
--

DROP TABLE IF EXISTS `device_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `device_group` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `version` bigint(20) NOT NULL,
  `name` varchar(255) NOT NULL,
  `status` varchar(255) DEFAULT NULL,
  `groups_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `FKDC71DF56984B586A` (`groups_id`),
  CONSTRAINT `FKDC71DF56984B586A` FOREIGN KEY (`groups_id`) REFERENCES `groups` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;



--
-- Table structure for table `device_group_device`
--

DROP TABLE IF EXISTS `device_group_device`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `device_group_device` (
  `device_group_devices_id` bigint(20) DEFAULT NULL,
  `device_id` bigint(20) DEFAULT NULL,
  KEY `FKD0056F5FBC11ECEF` (`device_id`),
  KEY `FKD0056F5FE4F3C3A` (`device_group_devices_id`),
  CONSTRAINT `FKD0056F5FBC11ECEF` FOREIGN KEY (`device_id`) REFERENCES `device` (`id`),
  CONSTRAINT `FKD0056F5FE4F3C3A` FOREIGN KEY (`device_group_devices_id`) REFERENCES `device_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;



--
-- Table structure for table `device_radio_stream`
--

DROP TABLE IF EXISTS `device_radio_stream`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `device_radio_stream` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `version` bigint(20) NOT NULL,
  `device_id` bigint(20) NOT NULL,
  `ocap_id` varchar(255) NOT NULL,
  `stream_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `FK81A39F8D3DFB26A5` (`stream_id`),
  KEY `FK81A39F8DEC4FF12A` (`device_id`),
  CONSTRAINT `FK81A39F8DEC4FF12A` FOREIGN KEY (`device_id`) REFERENCES `device` (`id`),
  CONSTRAINT `FK81A39F8D3DFB26A5` FOREIGN KEY (`stream_id`) REFERENCES `radio_streaming_details` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;



--
-- Table structure for table `device_stream`
--

DROP TABLE IF EXISTS `device_stream`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `device_stream` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `version` bigint(20) NOT NULL,
  `device_id` bigint(20) NOT NULL,
  `ocap_id` varchar(255) NOT NULL,
  `stream_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `FKC66181895BBC466F` (`stream_id`),
  KEY `FKC6618189BC11ECEF` (`device_id`),
  CONSTRAINT `FKC66181895BBC466F` FOREIGN KEY (`stream_id`) REFERENCES `streaming_details` (`id`),
  CONSTRAINT `FKC6618189BC11ECEF` FOREIGN KEY (`device_id`) REFERENCES `device` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1009 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;



--
-- Table structure for table `execute_method_result`
--

DROP TABLE IF EXISTS `execute_method_result`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `execute_method_result` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `version` bigint(20) NOT NULL,
  `actual_result` varchar(255) DEFAULT NULL,
  `execution_result_id` bigint(20) NOT NULL,
  `expected_result` varchar(255) DEFAULT NULL,
  `function_name` varchar(255) DEFAULT NULL,
  `status` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `FKA1287DF19FCEDC3B` (`execution_result_id`),
  CONSTRAINT `FKA1287DF19FCEDC3B` FOREIGN KEY (`execution_result_id`) REFERENCES `execution_result` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=192979 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;



--
-- Table structure for table `execution`
--

DROP TABLE IF EXISTS `execution`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `execution` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `version` bigint(20) NOT NULL,
  `date_of_execution` datetime DEFAULT NULL,
  `device` varchar(255) DEFAULT NULL,
  `device_group` varchar(255) DEFAULT NULL,
  `execution_time` varchar(255) DEFAULT NULL,
  `is_marked` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `output_data` longtext,
  `result` varchar(255) DEFAULT NULL,
  `script` varchar(255) DEFAULT NULL,
  `script_group` varchar(255) DEFAULT NULL,
  `groups_id` bigint(20) DEFAULT NULL,
  `is_performance_done` bit(1) NOT NULL,
  `execution_status` varchar(255) DEFAULT NULL,
  `is_aborted` bit(1) NOT NULL,
  `application_url` varchar(255) DEFAULT NULL,
  `is_bench_mark_enabled` bit(1) NOT NULL,
  `is_rerun_required` bit(1) NOT NULL,
  `is_system_diagnostics_enabled` bit(1) NOT NULL,
  `third_party_execution_details_id` bigint(20) DEFAULT NULL,
  `script_count` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `FKBEF90B18984B586A` (`groups_id`),
  KEY `FKBEF90B18D2187869` (`third_party_execution_details_id`),
  CONSTRAINT `FKBEF90B18984B586A` FOREIGN KEY (`groups_id`) REFERENCES `groups` (`id`),
  CONSTRAINT `FKBEF90B18D2187869` FOREIGN KEY (`third_party_execution_details_id`) REFERENCES `third_party_execution_details` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4843 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;



--
-- Table structure for table `execution_device`
--

DROP TABLE IF EXISTS `execution_device`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `execution_device` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `version` bigint(20) NOT NULL,
  `date_of_execution` datetime DEFAULT NULL,
  `device` varchar(255) NOT NULL,
  `device_ip` varchar(255) NOT NULL,
  `execution_id` bigint(20) NOT NULL,
  `execution_time` varchar(255) DEFAULT NULL,
  `status` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `FKE2CBE55D8358C58A` (`execution_id`),
  CONSTRAINT `FKE2CBE55D8358C58A` FOREIGN KEY (`execution_id`) REFERENCES `execution` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4793 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;



--
-- Table structure for table `execution_result`
--

DROP TABLE IF EXISTS `execution_result`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `execution_result` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `version` bigint(20) NOT NULL,
  `device` varchar(255) NOT NULL,
  `execution_id` bigint(20) NOT NULL,
  `execution_device_id` bigint(20) NOT NULL,
  `execution_output` longtext,
  `script` varchar(255) NOT NULL,
  `status` varchar(255) DEFAULT NULL,
  `exec_device_id` bigint(20) DEFAULT NULL,
  `device_id_string` varchar(255) DEFAULT NULL,
  `date_of_execution` datetime DEFAULT NULL,
  `execution_time` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `FKFAAE8F24F5E1059B` (`execution_device_id`),
  KEY `FKFAAE8F248358C58A` (`execution_id`),
  KEY `FKFAAE8F241B03E2FC` (`exec_device_id`),
  CONSTRAINT `FKFAAE8F241B03E2FC` FOREIGN KEY (`exec_device_id`) REFERENCES `device` (`id`),
  CONSTRAINT `FKFAAE8F248358C58A` FOREIGN KEY (`execution_id`) REFERENCES `execution` (`id`),
  CONSTRAINT `FKFAAE8F24F5E1059B` FOREIGN KEY (`execution_device_id`) REFERENCES `execution_device` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=28512 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;



--
-- Table structure for table `function`
--

DROP TABLE IF EXISTS `function`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `function` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `version` bigint(20) NOT NULL,
  `module_id` bigint(20) NOT NULL,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `FK524F73D86DEEED2F` (`module_id`),
  CONSTRAINT `FK524F73D86DEEED2F` FOREIGN KEY (`module_id`) REFERENCES `module` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=508 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `function`
--

LOCK TABLES `function` WRITE;
/*!40000 ALTER TABLE `function` DISABLE KEYS */;
INSERT INTO `function` VALUES (18,0,8,'TestMgr_IARMBUS_Init'),(19,0,8,'TestMgr_IARMBUS_Connect'),(20,0,8,'TestMgr_IARMBUS_Disconnect'),(21,0,8,'TestMgr_IARMBUS_Term'),(22,0,8,'TestMgr_IARMBUS_BusCall'),(24,0,8,'TestMgr_IARMBUS_RegisterCall'),(25,0,8,'TestMgr_IARMBUS_RequestResource'),(26,0,8,'TestMgr_IARMBUS_ReleaseResource'),(29,0,8,'TestMgr_IARMBUS_BroadcastEvent'),(30,0,8,'TestMgr_IARMBUS_InvokeSecondApplication'),(31,0,8,'TestMgr_IARMBUS_RegisterEventHandler'),(32,0,8,'TestMgr_IARMBUS_UnRegisterEventHandler'),(37,0,8,'TestMgr_IARMBUS_IsConnected'),(38,0,8,'TestMgr_IARMBUS_RegisterEvent'),(40,0,8,'TestMgr_IARMBUS_GetContext'),(41,0,8,'TestMgr_IARMBUS_GetLastReceivedEventDetails'),(74,0,24,'TestMgr_Opensource_Test_Execute'),(75,0,25,'TestMgr_DS_FP_setColor'),(76,0,25,'TestMgr_DS_managerInitialize'),(77,0,25,'TestMgr_DS_managerDeinitialize'),(78,0,25,'TestMgr_DS_FP_setBrightness'),(79,0,25,'TestMgr_DS_FP_setBlink'),(80,0,25,'TestMgr_DS_FP_setScroll'),(81,0,25,'TestMgr_DS_AOP_setLevel'),(82,0,25,'TestMgr_DS_AOP_setDB'),(83,0,25,'TestMgr_DS_VD_setDFC'),(84,0,25,'TestMgr_DS_AOP_setEncoding'),(85,0,25,'TestMgr_DS_AOP_setCompression'),(86,0,25,'TestMgr_DS_AOP_setStereoMode'),(87,0,25,'TestMgr_DS_HOST_setPowerMode'),(88,0,25,'TestMgr_DS_VOP_setResolution'),(89,0,25,'TestMgr_DS_FP_getIndicators'),(90,0,25,'TestMgr_DS_FP_FP_getSupportedColors'),(91,0,25,'TestMgr_DS_FP_getTextDisplays'),(92,0,25,'TestMgr_DS_FP_setText'),(93,0,25,'TestMgr_DS_FP_setTimeForamt'),(94,0,25,'TestMgr_DS_FP_setTime'),(95,0,25,'TestMgr_DS_AOP_loopThru'),(96,0,25,'TestMgr_DS_AOP_mutedStatus'),(97,0,25,'TestMgr_DS_AOP_getSupportedEncodings'),(98,0,25,'TestMgr_DS_AOP_getSupportedCompressions'),(99,0,25,'TestMgr_DS_AOP_getSupportedStereoModes'),(100,0,25,'TestMgr_DS_HOST_addPowerModeListener'),(101,0,25,'TestMgr_DS_HOST_removePowerModeListener'),(102,0,25,'TestMgr_DS_HOST_Resolutions'),(103,0,25,'TestMgr_DS_VOPTYPE_HDCPSupport'),(104,0,25,'TestMgr_DS_VOPTYPE_DTCPSupport'),(105,0,25,'TestMgr_DS_VOP_getAspectRatio'),(106,0,25,'TestMgr_DS_VOP_getDisplayDetails'),(107,0,25,'TestMgr_DS_VOPTYPE_isDynamicResolutionSupported'),(108,0,22,'TestMgr_MediaStreamer_LiveTune_Request'),(110,0,22,'TestMgr_MediaStreamer_Recorded_Urls'),(111,0,22,'TestMgr_MediaStreamer_Recorded_Metadata'),(112,0,22,'TestMgr_MediaStreamer_Live_Playback'),(113,0,22,'TestMgr_MediaStreamer_Recording_Playback'),(115,0,22,'TestMgr_MediaStreamer_DVR_Trickplay'),(117,0,25,'TestMgr_DS_VOP_isContentProtected'),(118,0,25,'TestMgr_DS_VOP_isDisplayConnected'),(122,0,25,'TestMgr_DS_HOST_addDisplayConnectionListener'),(123,0,25,'TestMgr_DS_HOST_removeDisplayConnectionListener'),(124,0,27,'TestMgr_SM_RegisterService'),(125,0,27,'TestMgr_SM_UnRegisterService'),(126,0,27,'TestMgr_SM_DoesServiceExist'),(128,0,22,'TestMgr_MediaStreamer_Recording_Request'),(129,0,27,'TestMgr_SM_GetRegisteredServices'),(142,0,39,'TestMgr_rmfapp_Test_Execute'),(149,0,27,'TestMgr_SM_GetGlobalService'),(150,0,27,'TestMgr_SM_HN_EnableMDVR'),(151,0,27,'TestMgr_SM_HN_EnableVPOP'),(152,0,27,'TestMgr_SM_HN_SetDeviceName'),(153,0,27,'TestMgr_SM_SetAPIVersion'),(154,0,27,'TestMgr_SM_RegisterForEvents'),(156,0,27,'TestMgr_SM_DisplaySetting_SetZoomSettings'),(157,0,27,'TestMgr_SM_DisplaySetting_SetCurrentResolution'),(158,0,35,'TestMgr_CC_Init'),(164,0,35,'TestMgr_CC_SetGetDigitalChannel'),(166,0,35,'TestMgr_CC_SetGetAnalogChannel'),(167,0,35,'TestMgr_CC_Show'),(168,0,35,'TestMgr_CC_Hide'),(173,0,35,'TestMgr_CC_SetGetAttribute'),(174,0,35,'TestMgr_CC_GetSupportedServiceNumberCount'),(175,0,35,'TestMgr_CC_GetSupportedServiceNumber'),(177,0,35,'TestMgr_CC_SetGetState'),(179,0,35,'TestMgr_CC_OnEasStart'),(180,0,35,'TestMgr_CC_OnEasStop'),(181,0,35,'TestMgr_CC_ResetTrickPlayStatus'),(182,0,35,'TestMgr_CC_SetTrickPlayStatus'),(192,0,42,'TestMgr_newrmf_Appplay'),(201,0,44,'TestMgr_MPSink_SetGetMute'),(202,0,44,'TestMgr_MPSink_SetGetVolume'),(207,0,44,'TestMgr_HNSrc_GetBufferedRanges'),(208,0,44,'TestMgr_HNSrc_GetState'),(211,0,44,'TestMgr_HNSrcMPSink_Video_Pause'),(212,0,44,'TestMgr_MPSink_InitTerm'),(216,0,44,'TestMgr_HNSrcMPSink_Video_Speed'),(223,0,44,'TestMgr_HNSrcMPSink_Video_Play'),(224,0,44,'TestMgr_HNSrcMPSink_Video_State'),(227,0,44,'TestMgr_HNSrcMPSink_Video_Skip_Backward'),(230,0,44,'TestMgr_HNSrcMPSink_Video_Volume'),(231,0,44,'TestMgr_HNSrcMPSink_Video_Play_Position'),(232,0,44,'TestMgr_HNSrcMPSink_Video_MuteUnmute'),(270,0,44,'TestMgr_DVRSink_init_term'),(277,0,51,'TestMgr_RDKLogger_Dbg_Enabled_Status'),(278,0,51,'TestMgr_RDKLogger_EnvGet'),(279,0,51,'TestMgr_RDKLogger_EnvGetNum'),(280,0,51,'TestMgr_RDKLogger_EnvGetValueFromNum'),(281,0,51,'TestMgr_RDKLogger_EnvGetModFromNum'),(282,0,51,'TestMgr_RDKLogger_Init'),(283,0,51,'TestMgr_RDKLogger_Log'),(285,0,44,'TestMgr_QAMSource_Play'),(292,0,44,'TestMgr_QAMSource_InitTerm'),(293,0,44,'TestMgr_QAMSource_OpenClose'),(294,0,44,'TestMgr_QAMSource_Pause'),(295,0,44,' TestMgr_QAMSource_GetTsId'),(296,0,44,'TestMgr_QAMSource_GetLtsId'),(297,0,44,'TestMgr_QAMSource_GetQAMSourceInstance'),(298,0,44,'TestMgr_QAMSource_Init_Uninit_Platform'),(299,0,44,'TestMgr_QAMSource_GetUseFactoryMethods'),(300,0,44,'TestMgr_QAMSource_Get_Free_LowLevelElement'),(301,0,44,'TestMgr_QAMSource_ChangeURI'),(302,0,44,'TestMgr_DVRManager_GetSpace'),(303,0,44,'TestMgr_DVRManager_GetRecordingCount'),(304,0,44,'TestMgr_DVRManager_GetRecordingInfoByIndex'),(305,0,44,'TestMgr_DVRManager_GetRecordingInfoById'),(306,0,44,'TestMgr_DVRManager_GetIsRecordingInProgress'),(307,0,44,'TestMgr_DVRManager_GetRecordingSize'),(308,0,44,'TestMgr_DVRManager_GetRecordingDuration'),(309,0,44,'TestMgr_DVRManager_GetRecordingStartTime'),(310,0,44,'TestMgr_DVRManager_GetDefaultTSBMaxDuration'),(311,0,44,'TestMgr_DVRManager_CreateTSB'),(312,0,44,'TestMgr_DVRManager_CreateRecording'),(313,0,44,'TestMgr_DVRManager_UpdateRecording'),(314,0,44,'TestMgr_DVRManager_DeleteRecording'),(315,0,44,'TestMgr_DVRManager_GetSegmentsCount'),(316,0,44,'TestMgr_DVRManager_ConvertTSBToRecording'),(317,0,44,'TestMgr_DVRManager_GetRecordingSegmentInfoByIndex'),(350,0,22,'TestMgr_RMFStreamer_InterfaceTesting'),(351,0,22,'TestMgr_RMFStreamer_Player'),(353,0,44,'TestMgr_DVR_Rec_List'),(354,0,44,'TestMgr_RmfElementCreateInstance'),(355,0,44,'TestMgr_RmfElementInit'),(356,0,44,'TestMgr_RmfElementTerm'),(357,0,44,'TestMgr_RmfElementOpen'),(358,0,44,'TestMgr_RmfElementClose'),(359,0,44,'TestMgr_RmfElementRemoveInstance'),(360,0,44,'TestMgr_RmfElementPlay'),(361,0,44,'TestMgr_RmfElement_Sink_SetSource'),(362,0,44,'TestMgr_RmfElement_MpSink_SetVideoRectangle'),(363,0,44,'TestMgr_RmfElementSetSpeed'),(364,0,44,'TestMgr_RmfElementGetSpeed'),(365,0,44,'TestMgr_RmfElementGetMediaTime'),(366,0,44,'TestMgr_RmfElementGetState'),(367,0,44,'TestMgr_RmfElementPause'),(368,0,44,'TestMgr_RmfElementSetMediaTime'),(369,0,44,'TestMgr_RmfElementGetMediaInfo'),(370,0,57,'Xi4Init'),(371,0,58,'TestMgr_Recorder_ScheduleRecording'),(372,0,58,'TestMgr_Recorder_checkRecording_status'),(373,0,44,'TestMgr_DVRManager_CheckRecordingInfoById'),(374,0,44,'TestMgr_DVRManager_CheckRecordingInfoByIndex'),(375,0,59,'TestMgr_HybridE2E_T2pTuning'),(376,0,59,'TestMgr_HybridE2E_T2pTrickMode'),(378,0,59,'TestMgr_E2EStub_PlayURL'),(379,0,59,'TestMgr_E2EStub_GetRecURLS'),(380,0,59,'TestMgr_E2ELinearTV_GetURL'),(381,0,59,'TestMgr_E2ELinearTV_PlayURL'),(382,0,59,'TestMgr_Dvr_Play_Pause'),(383,0,59,'TestMgr_Dvr_Play_TrickPlay_FF_FR'),(384,0,59,'TestMgr_LinearTv_Dvr_Play'),(385,0,59,'TestMgr_Dvr_Play_TrickPlay_RewindFromEndPoint'),(386,0,59,'TestMgr_Dvr_Pause_Play'),(387,0,59,'TestMgr_Dvr_Play_Pause_Play'),(388,0,59,'TestMgr_Dvr_Play_Pause_Play_Repeat'),(389,0,59,'TestMgr_Dvr_Skip_Forward_Play'),(390,0,59,'TestMgr_Dvr_Skip_Forward_From_Middle'),(391,0,59,'TestMgr_Dvr_Skip_Forward_From_End'),(392,0,59,'TestMgr_Dvr_Skip_Backward_From_End'),(393,0,59,'TestMgr_Dvr_Skip_Backward_From_Middle'),(394,0,59,'TestMgr_Dvr_Skip_Backward_From_Starting'),(395,0,59,'TestMgr_Dvr_Play_Rewind_Forward'),(396,0,59,'TestMgr_Dvr_Play_Forward_Rewind'),(397,0,59,'TestMgr_Dvr_Play_FF_FR_Pause_Play'),(398,0,59,'TestMgr_Dvr_Play_Pause_FF_FR'),(399,0,59,'TestMgr_Dvr_Play_Pause_Play_SF_SB'),(400,0,59,'TestMgr_Dvr_Play_FF_FR_SF_SB'),(401,0,59,'TestMgr_Dvr_Play_Pause_Pause'),(402,0,59,'TestMgr_Dvr_Play_Play'),(403,0,59,'TestMgr_LiveTune_GETURL'),(404,0,59,'TestMgr_RF_Video_ChannelChange'),(405,0,44,'TestMgr_RmfElement_DVRManagerCreateRecording'),(407,0,44,'TestMgr_RmfElement_QAMSrc_RmfPlatform_Init'),(408,0,44,'TestMgr_RmfElement_QAMSrc_RmfPlatform_Uninit'),(409,0,44,'TestMgr_RmfElement_QAMSrc_InitPlatform'),(410,0,44,'TestMgr_RmfElement_QAMSrc_UninitPlatform'),(412,0,44,'TestMgr_RmfElement_QAMSrc_GetTSID'),(413,0,44,'TestMgr_RmfElement_QAMSrc_GetLTSID'),(414,0,44,'TestMgr_RmfElement_QAMSrc_GetLowLevelElement'),(415,0,44,'TestMgr_RmfElement_QAMSrc_FreeLowLevelElement'),(416,0,44,'TestMgr_RmfElement_QAMSrc_ChangeURI'),(417,0,44,'TestMgr_RmfElement_QAMSrc_UseFactoryMethods'),(418,0,44,'TestMgr_RmfElement_HNSink_InitPlatform'),(419,0,44,'TestMgr_RmfElement_HNSink_UninitPlatform'),(420,0,44,'TestMgr_RmfElement_HNSink_SetProperties'),(421,0,44,'TestMgr_RmfElement_HNSink_SetSourceType'),(422,0,59,'TestMgr_TSB_Play'),(424,0,39,'TestMgr_CreateRecord'),(425,0,59,'TestMgr_MDVR_Record_Play'),(426,0,59,'TestMgr_MDVR_GetResult'),(427,0,60,'TestMgr_GetParameterValue'),(429,0,51,'TestMgr_RDKLogger_Log_All'),(431,0,51,'TestMgr_RDKLogger_Log_InverseTrace'),(432,0,51,'TestMgr_RDKLogger_Log_Msg'),(433,0,51,'TestMgr_RDKLogger_Log_None'),(434,0,51,'TestMgr_RDKLogger_Log_Trace'),(437,0,51,'TestMgr_RDKLogger_CheckMPELogEnabled'),(438,0,60,'TestMgr_VerifyParameterValue'),(440,0,51,'TestMgr_RDKLogger_SetLogLevel'),(441,0,51,'TestMgr_RDKLogger_GetLogLevel'),(442,0,44,'TestMgr_HNSrc_GetBufferedRanges'),(443,0,61,'TestMgr_Aesdecrypt_DecryptEnable_Prop'),(445,0,62,'TestMgr_TRM_GetAllTunerStates'),(446,0,62,'TestMgr_TRM_GetAllTunerIds'),(447,0,62,'TestMgr_TRM_GetAllReservations'),(448,0,62,'TestMgr_TRM_GetVersion'),(449,0,61,'TestMgr_Aesdecrypt_DecryptEnable_Get_Prop'),(450,0,61,'TestMgr_Aesencrypt_EncryptEnable_Set_Prop'),(453,0,61,'TestMgr_Aesencrypt_EncryptEnable_Get_Prop'),(454,0,61,'TestMgr_Dvrsrc_RecordId_Set_Prop'),(455,0,61,'TestMgr_Dvrsrc_RecordId_Get_Prop'),(456,0,61,'TestMgr_Dvrsrc_SegmentName_Set_Prop'),(457,0,61,'TestMgr_Dvrsrc_SegmentName_Get_Prop'),(458,0,61,'TestMgr_Dvrsrc_Ccivalue_Get_Prop'),(459,0,61,'TestMgr_Dvrsrc_Rate_Set_Prop'),(460,0,62,'TestMgr_TRM_TunerReserveForRecord'),(461,0,62,'TestMgr_TRM_TunerReserveForLive'),(462,0,61,'TestMgr_Dvrsrc_Rate_Get_Prop'),(463,0,61,'TestMgr_Dvrsrc_StartTime_Get_Prop'),(464,0,61,'TestMgr_Dvrsrc_Duration_Get_Prop'),(465,0,61,'TestMgr_Dvrsrc_PlayStartPosition_Set_Prop'),(466,0,61,'TestMgr_Dvrsrc_PlayStartPosition_Get_Prop'),(467,0,61,'TestMgr_Dvrsink_RecordId_Set_Prop'),(468,0,61,'TestMgr_Dvrsink_RecordId_Get_Prop'),(469,0,61,'TestMgr_Dvrsink_Ccivalue_Get_Prop'),(470,0,61,'TestMgr_Dvrsrc_RecordId_Get_Prop'),(471,0,61,'TestMgr_Dvrsrc_SegmentName_Set_Prop'),(472,0,61,'TestMgr_Dvrsrc_SegmentName_Set_Prop'),(474,0,62,'TestMgr_TRM_ReleaseTunerReservation'),(475,0,62,'TestMgr_TRM_ValidateTunerReservation'),(476,0,62,'TestMgr_TRM_CancelRecording'),(477,0,62,'TestMgr_TRM_CancelLive'),(481,0,27,'TestMgr_SM_DeviceSetting_GetDeviceInfo'),(482,0,27,'TestMgr_SM_ScreenCapture_Upload'),(483,0,27,'TestMgr_SM_WebSocket_GetUrl'),(484,0,27,'TestMgr_SM_WebSocket_GetReadyState'),(485,0,27,'TestMgr_SM_WebSocket_GetBufferedAmount'),(486,0,27,'TestMgr_SM_WebSocket_GetProtocol'),(487,0,27,'TestMgr_SM_GetSetting'),(488,0,27,'TestMgr_SM_CreateService'),(489,0,27,'TestMgr_Services_GetName'),(490,0,44,'TestMgr_RmfElement_CheckForSPTSRead_QAMSrc_Error'),(491,0,25,'TestMgr_DS_FP_setState'),(492,0,25,'TestMgr_DS_VOP_setEnable'),(495,0,44,'TestMgr_CheckAudioVideoStatus'),(497,0,64,'TestMgr_DTCPAgent_Init'),(498,0,65,'TestMgr_XUPNPAgent_checkjson'),(499,0,65,'TestMgr_XUPNPAgent_checkSTRurl'),(500,0,65,'TestMgr_XUPNPAgent_checkSerialNo'),(501,0,65,'TestMgr_XUPNPAgent_checkPBurl'),(502,0,65,'TestMgr_XUPNPAgent_recordId'),(503,0,65,'TestMgr_XUPNPAgent_ModBasicDevice'),(504,0,65,'TestMgr_XUPNPAgent_removeXmls'),(505,0,65,'TestMgr_XUPNPAgent_evtCheck'),(506,0,44,'TestMgr_CheckRmfStreamerCrash'),(507,0,44,'TestMgr_ClearLogFile');
/*!40000 ALTER TABLE `function` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `groups`
--

DROP TABLE IF EXISTS `groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `groups` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `version` bigint(20) NOT NULL,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `groups`
--

LOCK TABLES `groups` WRITE;
/*!40000 ALTER TABLE `groups` DISABLE KEYS */;
INSERT INTO `groups` VALUES (1,0,'RDK LLC'),(2,0,'Time Warner'),(3,0,'Comcast'),(4,0,'Tata Elxsi');
/*!40000 ALTER TABLE `groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `job_details`
--

DROP TABLE IF EXISTS `job_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `job_details` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `version` bigint(20) NOT NULL,
  `app_url` varchar(255) NOT NULL,
  `device` varchar(255) DEFAULT NULL,
  `device_group` varchar(255) DEFAULT NULL,
  `file_path` varchar(255) NOT NULL,
  `job_name` varchar(255) NOT NULL,
  `real_path` varchar(255) NOT NULL,
  `schedule_type` varchar(255) DEFAULT NULL,
  `script_group` varchar(255) DEFAULT NULL,
  `trigger_name` varchar(255) NOT NULL,
  `end_date` datetime DEFAULT NULL,
  `one_time_schedule_date` datetime DEFAULT NULL,
  `query_string` varchar(255) DEFAULT NULL,
  `start_date` datetime DEFAULT NULL,
  `groups_id` bigint(20) DEFAULT NULL,
  `is_bench_mark` varchar(255) DEFAULT NULL,
  `is_system_diagnostics` varchar(255) DEFAULT NULL,
  `repeat_count` int(11) NOT NULL,
  `rerun` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `FK3E2527C0984B586A` (`groups_id`),
  CONSTRAINT `FK3E2527C0984B586A` FOREIGN KEY (`groups_id`) REFERENCES `groups` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;



--
-- Table structure for table `job_details_script`
--

DROP TABLE IF EXISTS `job_details_script`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `job_details_script` (
  `job_details_id` bigint(20) DEFAULT NULL,
  `script_string` varchar(255) DEFAULT NULL,
  `script_idx` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;



--
-- Table structure for table `module`
--

DROP TABLE IF EXISTS `module`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `module` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `version` bigint(20) NOT NULL,
  `name` varchar(255) NOT NULL,
  `rdk_version` varchar(255) NOT NULL,
  `test_group` varchar(255) NOT NULL,
  `groups_id` bigint(20) DEFAULT NULL,
  `execution_time` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `FKC04BA66C984B586A` (`groups_id`),
  CONSTRAINT `FKC04BA66C984B586A` FOREIGN KEY (`groups_id`) REFERENCES `groups` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=66 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `module`
--

LOCK TABLES `module` WRITE;
/*!40000 ALTER TABLE `module` DISABLE KEYS */;
INSERT INTO `module` VALUES (8,6,'iarmbus','1.2','Component',NULL,3),(22,2,'mediastreamer','1.2','Component',NULL,3),(24,1,'openSource_components','1.2','OpenSource',NULL,60),(25,3,'devicesettings','1.2','Component',NULL,3),(27,1,'servicemanager','1.3','Component',NULL,2),(35,1,'closedcaption','1.2','Component',NULL,1),(39,1,'rmfapp','2.0','E2E',NULL,5),(42,1,'newrmf','RDK2.0','Component',NULL,5),(44,2,'mediaframework','2.0','Component',NULL,3),(51,1,'rdk_logger','2.0','Component',NULL,5),(57,0,'Xi4Module1','2.1','Component',NULL,2),(58,0,'recorder','2.0','Component',NULL,10),(59,1,'tdk_integration','1.3','E2E',NULL,5),(60,0,'tr69','1','Component',NULL,5),(61,0,'gst-plugins-rdk','1','Component',NULL,5),(62,0,'trm','1','Component',NULL,10),(64,0,'dtcp','1','Component',NULL,5),(65,0,'xupnp','1','Component',NULL,7);
/*!40000 ALTER TABLE `module` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `module_log_file_names`
--

DROP TABLE IF EXISTS `module_log_file_names`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `module_log_file_names` (
  `module_id` bigint(20) DEFAULT NULL,
  `log_file_names_string` varchar(255) DEFAULT NULL,
  KEY `FKE56384D39E2CF16A` (`module_id`),
  CONSTRAINT `FKE56384D39E2CF16A` FOREIGN KEY (`module_id`) REFERENCES `module` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `module_log_file_names`
--

LOCK TABLES `module_log_file_names` WRITE;
/*!40000 ALTER TABLE `module_log_file_names` DISABLE KEYS */;
INSERT INTO `module_log_file_names` VALUES (8,'/opt/logs/uimgr_log.txt'),(22,'/opt/logs/ocapri_log.txt'),(59,'/opt/logs/ocapri_log.txt');
/*!40000 ALTER TABLE `module_log_file_names` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `parameter`
--

DROP TABLE IF EXISTS `parameter`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `parameter` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `version` bigint(20) NOT NULL,
  `parameter_type_id` bigint(20) NOT NULL,
  `primitive_test_id` bigint(20) DEFAULT NULL,
  `value` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `FK747EB3A9C5F1CB98` (`parameter_type_id`),
  KEY `FK747EB3A967097214` (`primitive_test_id`),
  CONSTRAINT `FK747EB3A967097214` FOREIGN KEY (`primitive_test_id`) REFERENCES `primitive_test` (`id`),
  CONSTRAINT `FK747EB3A9C5F1CB98` FOREIGN KEY (`parameter_type_id`) REFERENCES `parameter_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2122 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;



--
-- Table structure for table `parameter_type`
--

DROP TABLE IF EXISTS `parameter_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `parameter_type` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `version` bigint(20) NOT NULL,
  `function_id` bigint(20) NOT NULL,
  `name` varchar(255) NOT NULL,
  `parameter_type_enum` varchar(255) NOT NULL,
  `range_val` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `FK438D7610F773FC6F` (`function_id`),
  CONSTRAINT `FK438D7610F773FC6F` FOREIGN KEY (`function_id`) REFERENCES `function` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=771 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `parameter_type`
--

LOCK TABLES `parameter_type` WRITE;
/*!40000 ALTER TABLE `parameter_type` DISABLE KEYS */;
INSERT INTO `parameter_type` VALUES (20,0,18,'Process_name','STRING','A-Z'),(21,0,22,'owner_name','STRING','A-Z'),(22,0,22,'method_name','STRING','A-Z'),(24,0,22,'set_timeout','INTEGER','1-65535'),(25,0,22,'newState','INTEGER','0-2'),(26,0,22,'resource_type','INTEGER','0-7'),(27,0,24,'owner_name','STRING','A-Z'),(29,0,25,'resource_type','INTEGER','0-7'),(30,0,26,'resource_type','INTEGER','0-7'),(34,0,29,'event_id','INTEGER','0-2'),(35,0,29,'owner_name','STRING','A-Z'),(37,0,29,'keyType','INTEGER','1-65535'),(38,0,29,'keyCode','INTEGER','1-65535'),(39,0,29,'newState','INTEGER','0-2'),(40,0,29,'resource_type','INTEGER','0-7'),(43,0,31,'event_id','INTEGER','0-2'),(44,0,31,'owner_name','STRING','A-Z'),(45,0,32,'event_id','INTEGER','0-2'),(46,0,32,'owner_name','STRING','A-Z'),(49,0,37,'member_name','STRING','A-Z'),(51,0,38,'max_event','INTEGER','0-2'),(68,0,22,'mfr_param_type','INTEGER','0-9'),(81,0,74,'Opensource_component_type','STRING','qt_non_gfx (or) qt_gfx (or) webkit (or) gstreamer (or) gst_plugin_base (or) gst_plugin_good'),(82,0,74,'Display_option','STRING','directfb (or) eglnullws (or) intelce'),(85,0,78,'indicator_name','STRING','A-Z'),(86,0,78,'brightness','INTEGER','1-100'),(87,0,79,'indicator_name','STRING','A-Z'),(88,0,79,'blink_interval','INTEGER','1-10'),(89,0,79,'blink_iteration','STRING','1-10'),(90,0,80,'viteration','INTEGER','1-10'),(91,0,80,'hiteration','INTEGER','1-10'),(92,0,80,'hold_duration','INTEGER','1-10'),(93,0,80,'text','STRING','A-Z'),(94,0,81,'port_name','STRING','A-Z'),(97,0,82,'port_name','STRING','A-Z'),(98,0,83,'zoom_setting','STRING','A-Z'),(99,0,84,'port_name','STRING','A-Z'),(100,0,84,'encoding_format','STRING','A-Z'),(101,0,85,'port_name','STRING','A-Z'),(102,0,85,'compression_format','STRING','A-Z'),(103,0,86,'port_name','STRING','A-Z'),(104,0,86,'stereo_mode','STRING','A-Z'),(105,0,87,'new_power_state','INTEGER','0-1'),(106,0,88,'port_name','STRING','A-Z'),(107,0,88,'resolution','STRING','A-Z & 0-9'),(108,0,90,'indicator_name','STRING','A-Z'),(109,0,92,'text_display','STRING','A-Z'),(110,0,92,'text','STRING','A-Z'),(111,0,93,'time_format','INTEGER','0-2'),(112,0,93,'text','STRING','A-Z'),(113,0,94,'time_hrs','INTEGER','1-24'),(114,0,94,'time_mins','INTEGER','1-60'),(115,0,94,'text','STRING','A-Z'),(116,0,95,'loop_thru','INTEGER','0-1'),(117,0,95,'port_name','STRING','A-Z'),(118,0,96,'mute_status','INTEGER','0-1'),(119,0,96,'port_name','STRING','A-Z'),(120,0,97,'port_name','STRING','A-Z'),(121,0,98,'port_name','STRING','A-Z'),(122,0,99,'port_name','STRING','A-Z'),(123,0,102,'port_name','STRING','A-Z'),(124,0,103,'port_id','INTEGER','0'),(125,0,104,'port_id','INTEGER','0'),(126,0,105,'port_name','STRING','A-Z'),(127,0,106,'port_name','STRING','A-Z'),(128,0,107,'port_name','STRING','A-Z'),(129,0,108,'ocapId','STRING','A-Z'),(130,0,112,'ocapId','STRING','A-Z'),(134,0,115,'timePosition','STRING','A-Z'),(135,0,115,'PlaySpeed','STRING','A-Z'),(137,0,117,'port_name','STRING','A-Z'),(138,0,118,'port_name','STRING','A-Z'),(139,0,124,'service_name','STRING','A-Z'),(140,0,125,'service_name','STRING','A-Z'),(141,0,126,'service_name','STRING','A-Z'),(142,0,81,'audio_level','FLOAT','1-10'),(143,0,82,'db_level','FLOAT','1-100'),(145,0,128,'recordingId','STRING','A-Z'),(152,0,142,'rmfapp_command','STRING','any alphanumeric sequence'),(154,0,149,'service_name','STRING','A-Z'),(155,0,150,'enable','INTEGER','0,1'),(156,0,151,'enable','INTEGER','0,1'),(158,0,153,'apiVersion','INTEGER','1-1000'),(159,0,154,'service_name','STRING','A-Z'),(160,0,154,'event_name','STRING','A-Z'),(161,0,152,'device_name','STRING','A-Z & 1-1000'),(162,0,153,'service_name','STRING','A-Z'),(163,0,156,'videoDisplay','STRING','A-Z'),(164,0,157,'videoDisplay','STRING','A-Z'),(165,0,156,'zoomLevel','STRING','A-Z'),(166,0,157,'resolution','STRING','A-Z'),(189,0,177,'status','INTEGER','0-1'),(193,0,182,'trickPlayStatus','INTEGER','0-1'),(195,0,173,'Categories','STRING','A-Z'),(196,0,173,'ccAttribute','INTEGER','1 - 14'),(197,0,173,'value','INTEGER','1-8'),(198,0,173,'ccType','INTEGER','0-1'),(199,0,173,'stylevalue','STRING','A-Z'),(201,0,164,'channel_num','INTEGER','1-63'),(202,0,166,'analog_channel_num','INTEGER','1-8'),(209,0,192,'ocapid','STRING','A-Z'),(212,0,30,'appname','STRING','A-Z'),(214,0,22,'testapp_API1_data','INTEGER','1-1000'),(215,0,22,'testapp_API0_data','INTEGER','1-1000'),(254,0,211,'pauseuri','STRING','A-Z'),(259,0,216,'playuri','STRING','A-Z'),(264,0,224,'playuri','STRING','A-Z'),(266,0,224,'Y','INTEGER','0-1'),(267,0,224,'X','INTEGER','0-1'),(268,0,224,'H','INTEGER','0-10000'),(269,0,224,'W','INTEGER','0-10000'),(277,0,224,'apply','INTEGER','0,1'),(283,0,223,'playuri','STRING','A-Z'),(284,0,202,'Volume','FLOAT','0-100'),(286,0,227,'playuri','STRING','A-Z'),(301,0,230,'Volume','FLOAT','0-100'),(302,0,230,'X','INTEGER','0-1'),(303,0,230,'Y','INTEGER','0-1'),(304,0,230,'H','INTEGER','0-10000'),(305,0,230,'W','INTEGER','0-1000'),(306,0,230,'apply','INTEGER','0,1'),(307,0,230,'playuri','STRING','A-Z'),(313,0,231,'playuri','STRING','A-Z'),(314,0,232,'X','INTEGER','0-1'),(315,0,232,'Y','INTEGER','0-1'),(316,0,232,'H','INTEGER','0-10000'),(317,0,232,'W','INTEGER','0-1000'),(318,0,232,'playuri','STRING','A-Z'),(319,0,232,'apply','INTEGER','0,1'),(374,0,270,'recordingId','INTEGER','usually 5 digit nos '),(375,0,270,'playUrl','STRING','play url'),(385,0,277,'module','STRING','A-Z'),(386,0,277,'level','STRING','A-Z'),(387,0,278,'module','STRING','A-Z'),(390,0,279,'module','STRING','A-Z'),(393,0,283,'module','STRING','A-Z'),(394,0,283,'level','STRING','A-Z'),(395,0,280,'number','INTEGER','0-100'),(396,0,281,'number','INTEGER','0-100'),(397,0,285,'ocaplocator','STRING','A-Z'),(398,0,293,'ocaplocator','STRING','A-Z'),(399,0,294,'ocaplocator','STRING','A-Z'),(400,0,295,'ocaplocator','STRING','A-Z'),(401,0,296,'ocaplocator','STRING','A-Z'),(402,0,297,'ocaplocator','STRING','A-Z'),(403,0,300,'ocaplocator','STRING','A-Z'),(404,0,301,'ocaplocator','STRING','A-Z'),(405,0,301,'newocaplocator','STRING','A-Z'),(406,0,304,'index','INTEGER','0-100'),(407,0,305,'recordingId','STRING','A-Z'),(408,0,306,'recordingId','STRING','A-Z'),(409,0,307,'recordingId','STRING','A-Z'),(410,0,308,'recordingId','STRING','A-Z'),(411,0,309,'recordingId','STRING','A-Z'),(412,0,311,'duration','INTEGER','long long (+positive no)'),(413,0,312,'recordingTitle','STRING','A-Z'),(414,0,312,'recordingId','STRING','A-Z'),(415,0,312,'recordDuration','DOUBLE','+ postive no'),(416,0,312,'qamLocator','STRING','qam locator string'),(417,0,313,'recordingId','STRING','A-Z'),(418,0,314,'recordingId','STRING','A-Z'),(419,0,316,'tsbId','STRING','negative long long'),(420,0,316,'recordingId','STRING','A-Z'),(421,0,317,'index','INTEGER','0-100'),(488,0,350,'URL','STRING','A-Z'),(489,0,351,'VideostreamURL','STRING','A-Z'),(490,0,351,'play_time','INTEGER','0-50'),(492,0,353,'recordingTitle','STRING','A-Z'),(493,0,353,'recordingId','STRING','A-Z'),(494,0,353,'recordDuration','DOUBLE','1-1000'),(495,0,353,'qamLocator','STRING','A-Z'),(496,0,351,'SkipTime','INTEGER','0-100'),(497,0,354,'rmfElement','STRING','A-Z'),(498,0,355,'rmfElement','STRING','A-Z'),(499,0,356,'rmfElement','STRING','A-Z'),(500,0,357,'url','STRING','A-Z'),(501,0,357,'rmfElement','STRING','A-Z'),(502,0,358,'rmfElement','STRING','A-Z'),(503,0,359,'rmfElement','STRING','A-Z'),(504,0,360,'rmfElement','STRING','A-Z'),(505,0,360,'playSpeed','FLOAT','1-100'),(506,0,360,'playTime','DOUBLE','0-100'),(507,0,360,'defaultPlay','INTEGER','0-1'),(508,0,361,'rmfSourceElement','STRING','A-Z'),(509,0,361,'rmfSinkElement','STRING','A-Z'),(510,0,362,'apply','INTEGER','0-1'),(511,0,362,'X','INTEGER','0-100'),(512,0,362,'Y','INTEGER','0-100'),(513,0,362,'height','INTEGER','1-10000'),(514,0,362,'width','INTEGER','1-10000'),(515,0,363,'playSpeed','FLOAT','1-100'),(516,0,364,'rmfElement','STRING','A-Z'),(517,0,363,'rmfElement','STRING','A-Z'),(518,0,365,'rmfElement','STRING','A-Z'),(519,0,366,'rmfElement','STRING','A-Z'),(520,0,367,'rmfElement','STRING','A-Z'),(521,0,368,'rmfElement','STRING','A-Z'),(522,0,368,'mediaTime','DOUBLE','0-10000'),(523,0,369,'rmfElement','STRING','A-Z'),(524,0,370,'Input1','INTEGER','1-100'),(529,0,372,'Recording_Id','STRING','0-100000'),(530,0,314,'playUrl','STRING','A-Z'),(531,0,305,'playUrl','STRING','A-Z'),(532,0,306,'playUrl','STRING','A-Z'),(533,0,307,'playUrl','STRING','A-Z'),(534,0,308,'playUrl','STRING','A-Z'),(535,0,309,'playUrl','STRING','A-Z'),(536,0,316,'playUrl','STRING','A-Z'),(537,0,313,'playUrl','STRING','A-Z'),(539,0,304,'playUrl','STRING','A-Z'),(540,0,373,'recordingId','STRING','A-Z'),(541,0,374,'index','INTEGER','0-100'),(544,0,380,'Validurl','STRING','A-Z'),(545,0,381,'videoStreamURL','STRING','A-Z'),(546,0,379,'RecordURL','STRING','A-Z'),(547,0,378,'videoStreamURL','STRING','A-Z'),(548,0,382,'playUrl','STRING','A-Z'),(549,0,383,'playUrl','STRING','A-Z'),(550,0,383,'speed','FLOAT','1-100'),(551,0,384,'playUrl','STRING','A-Z'),(552,0,385,'playUrl','STRING','A-Z'),(553,0,354,'dvrSinkRecordId','STRING','A-Z'),(554,0,385,'rewindSpeed','FLOAT','1-100'),(555,0,386,'playUrl','STRING','A-Z'),(556,0,387,'playUrl','STRING','A-Z'),(557,0,388,'playUrl','STRING','A-Z'),(558,0,388,'rCount','INTEGER','1-100'),(559,0,389,'playUrl','STRING','A-Z'),(560,0,389,'seconds','DOUBLE','1-100'),(561,0,389,'rCount','INTEGER','1-100'),(562,0,390,'playUrl','STRING','A-Z'),(564,0,390,'rCount','INTEGER','1-100'),(565,0,390,'seconds','DOUBLE','1-100'),(566,0,391,'playUrl','STRING','A-Z'),(567,0,391,'seconds','DOUBLE','1-100'),(568,0,392,'playUrl','STRING','A-Z'),(569,0,392,'seconds','DOUBLE','1-100'),(570,0,392,'rCount','INTEGER','1-100'),(571,0,393,'playUrl','STRING','A-Z'),(572,0,393,'seconds','DOUBLE','1-100'),(573,0,394,'playUrl','STRING','A-Z'),(574,0,394,'seconds','DOUBLE','1-100'),(575,0,395,'playUrl','STRING','A-Z'),(576,0,395,'rewindSpeed','FLOAT','1-100'),(577,0,395,'forwardSpeed','FLOAT','1-100'),(578,0,396,'playUrl','STRING','A-Z'),(579,0,396,'rewindSpeed','FLOAT','1-100'),(580,0,396,'forwardSpeed','FLOAT','1-100'),(581,0,397,'playUrl','STRING','A-Z'),(582,0,397,'trickPlayRate','FLOAT','1-100'),(583,0,398,'playUrl','STRING','A-Z'),(584,0,398,'trickPlayRate','FLOAT','1-100'),(585,0,399,'playUrl','STRING','A-Z'),(586,0,399,'sfSeconds','DOUBLE','1-100'),(587,0,399,'sbSeconds','DOUBLE','1-100'),(588,0,399,'rCount','INTEGER','1-100'),(589,0,400,'playUrl','STRING','A-Z'),(590,0,400,'rewindSpeed','FLOAT','1-100'),(591,0,400,'forwardSpeed','FLOAT','1-100'),(592,0,400,'sfSeconds','DOUBLE','1-100'),(593,0,400,'sbSeconds','DOUBLE','1-100'),(594,0,400,'rCount','INTEGER','1-100'),(595,0,401,'playUrl','STRING','A-Z'),(596,0,402,'playUrl','STRING','1-100'),(597,0,403,'Validurl','STRING','A-Z'),(599,0,405,'recordingId','STRING','A-Z'),(600,0,405,'url','STRING','A-Z'),(601,0,405,'recDuration','DOUBLE','1-100'),(602,0,371,'Duration','STRING','Inmillsec'),(603,0,371,'Start_time','STRING','In-MilliSec'),(604,0,371,'Recording_Id','STRING','0-10000'),(605,0,371,'Source_id','STRING','A-Z'),(606,0,371,'UTCTime','STRING','mmddHHMMyyyy'),(607,0,404,'playUrl','STRING','A-Z'),(608,0,416,'url','STRING','A-Z'),(609,0,354,'factoryEnable','STRING','A-Z'),(610,0,354,'qamSrcUrl','STRING','A-Z'),(611,0,359,'factoryEnable','STRING','A-Z'),(612,0,420,'url','STRING','A-Z'),(614,0,420,'socketId','INTEGER','0-100'),(615,0,420,'streamIp','STRING','A-Z'),(616,0,420,'typeFlag','INTEGER','0-1'),(617,0,421,'rmfElement','STRING','A-Z'),(618,0,420,'dctpEnable','STRING','A-Z'),(619,0,376,'VideostreamURL','STRING','A-Z'),(620,0,376,'trickPlayRate','FLOAT','0-100'),(621,0,375,'ValidocapId','STRING','A-Z'),(622,0,420,'useChunkTransfer','STRING','A-Z'),(624,0,422,'VideostreamURL','STRING','A-Z'),(625,0,422,'SpeedRate','FLOAT','0-100'),(631,0,425,'playUrl','STRING','A-Z'),(632,0,424,'recordId','STRING','any alphanumeric sequence'),(633,0,424,'recordDuration','STRING','any alphanumeric sequence'),(634,0,424,'recordTitle','STRING','any alphanumeric sequence'),(635,0,424,'ocapId','STRING','any alphanumeric sequence'),(636,0,426,'resultList','STRING','A-Z'),(637,0,427,'path','STRING','A-Z'),(641,0,29,'state','INTEGER','0-100'),(642,0,29,'error','INTEGER','0-100'),(643,0,29,'payload','STRING','A-Z'),(644,0,429,'module','STRING','A-Z'),(645,0,434,'module','STRING','A-Z'),(646,0,431,'module','STRING','A-Z'),(647,0,433,'module','STRING','A-Z'),(648,0,432,'module','STRING','A-Z'),(649,0,432,'level','STRING','A-Z'),(650,0,432,'msg','STRING','A-Z'),(651,0,438,'path','STRING','A-Z'),(652,0,438,'paramValue','STRING','A-Z'),(654,0,30,'argv1','STRING','ON,OFF,PAIR'),(655,0,441,'module','STRING','A-Z'),(656,0,440,'module','STRING','A-Z'),(657,0,440,'level','STRING','A-Z'),(658,0,207,'X','INTEGER','0-1'),(659,0,207,'H','INTEGER','0-10000'),(660,0,207,'playuri','STRING','A-Z'),(661,0,207,'Y','INTEGER','0-1'),(662,0,207,'apply','INTEGER','0-10000'),(663,0,207,'W','INTEGER','0-10000'),(665,0,450,'propValue','INTEGER','0-1000'),(666,0,454,'propValue','STRING','AZ'),(669,0,459,'propValue','STRING','AZ'),(670,0,460,'recordingId','STRING','A-Z'),(671,0,460,'duration','DOUBLE','0-1000000'),(672,0,460,'locator','STRING','A-Z'),(673,0,465,'propValue','STRING','AZ'),(674,0,467,'propValue','STRING','AZ'),(675,0,461,'duration','DOUBLE','0-1000000'),(676,0,461,'locator','STRING','A-Z'),(679,0,456,'propValue','INTEGER','0-100'),(680,0,443,'propValue','INTEGER','0-100'),(684,0,474,'duration','DOUBLE','0-1000000'),(685,0,474,'locator','STRING','A-Z'),(686,0,475,'duration','DOUBLE','0-1000000'),(687,0,475,'locator','STRING','A-Z'),(688,0,476,'recordingId','STRING','A-Z'),(689,0,476,'duration','DOUBLE','0-1000000'),(690,0,476,'locator','STRING','A-Z'),(691,0,477,'duration','DOUBLE','0-1000000'),(692,0,477,'locator','STRING','A-Z'),(698,0,317,'playUrl','STRING','A-Z'),(701,0,482,'url','STRING','A-Z'),(710,0,354,'newQamSrc','STRING','A-Z'),(711,0,354,'newQamSrcUrl','STRING','A-Z'),(712,0,359,'newQamSrc','STRING','A-Z'),(713,0,361,'newQamSrc','STRING','A-Z'),(714,0,360,'newQamSrc','STRING','A-Z'),(715,0,367,'newQamSrc','STRING','A-Z'),(716,0,487,'service_name','STRING','A-Z'),(717,0,488,'service_name','STRING','A-Z'),(718,0,489,'service_name','STRING','A-Z'),(719,0,490,'logPath','STRING','A-Z'),(720,0,78,'get_only','INTEGER','0-1'),(723,0,78,'text','STRING','A-Z'),(725,0,487,'service_name','STRING','A-Z'),(726,0,488,'service_name','STRING','A-Z'),(727,0,489,'service_name','STRING','A-Z'),(728,0,354,'numOfTimeChannelChange','INTEGER','0-100'),(729,0,416,'numOfTimeChannelChange','INTEGER','0-100'),(730,0,361,'numOfTimeChannelChange','INTEGER','0-100'),(731,0,360,'numOfTimeChannelChange','INTEGER','0-100'),(732,0,367,'numOfTimeChannelChange','INTEGER','0-100'),(734,0,359,'numOfTimeChannelChange','INTEGER','0-100'),(735,0,88,'get_only','INTEGER','0-1'),(736,0,491,'state','INTEGER','0-1'),(737,0,492,'enable','INTEGER','0-1'),(738,0,491,'indicator_name','STRING','A-Z'),(739,0,492,'port_name','STRING','A-Z'),(740,0,75,'color','INTEGER','0-4'),(741,0,75,'indicator_name','STRING','A-Z'),(750,0,460,'startTime','DOUBLE','0-1000000'),(751,0,461,'startTime','DOUBLE','0-1000000'),(752,0,460,'deviceNo','INTEGER','0-5'),(753,0,461,'deviceNo','INTEGER','0-5'),(754,0,460,'hot','INTEGER','0-1'),(755,0,495,'audioVideoStatus','STRING','A-Z'),(756,0,474,'deviceNo','INTEGER','0-5'),(757,0,475,'deviceNo','INTEGER','0-5'),(758,0,497,'funcName','STRING','A-Z'),(759,0,497,'param1','STRING','A-Z'),(762,0,497,'param4','INTEGER','0-100'),(763,0,497,'param2','INTEGER','0-100'),(764,0,497,'param3','INTEGER','0-100'),(765,0,505,'evtName','STRING','A-Z'),(766,0,505,'evtValue','STRING','A-Z'),(767,0,506,'logFile','STRING','A-Z'),(768,0,506,'FileNameToCpTdkPath','STRING','A-Z'),(769,0,506,'patternToSearch','STRING','A-Z'),(770,0,507,'logFileToClear','STRING','A-Z');
/*!40000 ALTER TABLE `parameter_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `performance`
--

DROP TABLE IF EXISTS `performance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `performance` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `version` bigint(20) NOT NULL,
  `execution_result_id` bigint(20) DEFAULT NULL,
  `performance_type` varchar(255) DEFAULT NULL,
  `process_name` varchar(255) DEFAULT NULL,
  `process_value` varchar(255) DEFAULT NULL,
  `process_value1` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `FKA7C310309FCEDC3B` (`execution_result_id`),
  CONSTRAINT `FKA7C310309FCEDC3B` FOREIGN KEY (`execution_result_id`) REFERENCES `execution_result` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;



--
-- Table structure for table `primitive_test`
--

DROP TABLE IF EXISTS `primitive_test`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `primitive_test` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `version` bigint(20) NOT NULL,
  `function_id` bigint(20) NOT NULL,
  `module_id` bigint(20) NOT NULL,
  `name` varchar(255) NOT NULL,
  `groups_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `FKA504E8EA6DEEED2F` (`module_id`),
  KEY `FKA504E8EAF773FC6F` (`function_id`),
  KEY `FKA504E8EA984B586A` (`groups_id`),
  CONSTRAINT `FKA504E8EA6DEEED2F` FOREIGN KEY (`module_id`) REFERENCES `module` (`id`),
  CONSTRAINT `FKA504E8EA984B586A` FOREIGN KEY (`groups_id`) REFERENCES `groups` (`id`),
  CONSTRAINT `FKA504E8EAF773FC6F` FOREIGN KEY (`function_id`) REFERENCES `function` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=673 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `radio_streaming_details`
--

DROP TABLE IF EXISTS `radio_streaming_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `radio_streaming_details` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `version` bigint(20) NOT NULL,
  `groups_id` bigint(20) DEFAULT NULL,
  `stream_id` varchar(64) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `stream_id` (`stream_id`),
  KEY `FKE2194421984B586A` (`groups_id`),
  CONSTRAINT `FKE2194421984B586A` FOREIGN KEY (`groups_id`) REFERENCES `groups` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `radio_streaming_details`
--

LOCK TABLES `radio_streaming_details` WRITE;
/*!40000 ALTER TABLE `radio_streaming_details` DISABLE KEYS */;
INSERT INTO `radio_streaming_details` VALUES (1,0,NULL,'R01'),(2,0,NULL,'R02');
/*!40000 ALTER TABLE `radio_streaming_details` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rdkversions`
--

DROP TABLE IF EXISTS `rdkversions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rdkversions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `version` bigint(20) NOT NULL,
  `build_version` varchar(255) NOT NULL,
  `groups_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `build_version` (`build_version`),
  KEY `FK3CD0AE14984B586A` (`groups_id`),
  CONSTRAINT `FK3CD0AE14984B586A` FOREIGN KEY (`groups_id`) REFERENCES `groups` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rdkversions`
--

LOCK TABLES `rdkversions` WRITE;
/*!40000 ALTER TABLE `rdkversions` DISABLE KEYS */;
INSERT INTO `rdkversions` VALUES (1,0,'RDK1.2',NULL),(2,0,'RDK1.3',NULL),(3,0,'RDK2.0',NULL);
/*!40000 ALTER TABLE `rdkversions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `repeat_pending_execution`
--

DROP TABLE IF EXISTS `repeat_pending_execution`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `repeat_pending_execution` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `version` bigint(20) NOT NULL,
  `complete_execution_pending` int(11) NOT NULL,
  `current_execution_count` int(11) NOT NULL,
  `device_name` varchar(255) NOT NULL,
  `execution_name` varchar(255) NOT NULL,
  `status` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;



--
-- Table structure for table `role`
--

DROP TABLE IF EXISTS `role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `role` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `version` bigint(20) NOT NULL,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `role`
--

LOCK TABLES `role` WRITE;
/*!40000 ALTER TABLE `role` DISABLE KEYS */;
INSERT INTO `role` VALUES (1,5,'ADMIN'),(2,3,'TESTER');
/*!40000 ALTER TABLE `role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `role_permissions`
--

DROP TABLE IF EXISTS `role_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `role_permissions` (
  `role_id` bigint(20) DEFAULT NULL,
  `permissions_string` varchar(255) DEFAULT NULL,
  KEY `FKEAD9D23BA4EB492A` (`role_id`),
  CONSTRAINT `FKEAD9D23BA4EB492A` FOREIGN KEY (`role_id`) REFERENCES `role` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `role_permissions`
--

LOCK TABLES `role_permissions` WRITE;
/*!40000 ALTER TABLE `role_permissions` DISABLE KEYS */;
INSERT INTO `role_permissions` VALUES (1,'*:*'),(2,'Execution:*:*'),(2,'Module:*:*'),(2,'StreamingDetails:*:*'),(2,'ScriptGroup:*:*'),(2,'DeviceGroup:*:*'),(2,'Recorder:*:*'),(2,'PrimitiveTest:*:*'),(2,'Trends:*:*');
/*!40000 ALTER TABLE `role_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `script`
--

DROP TABLE IF EXISTS `script`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `script` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `version` bigint(20) NOT NULL,
  `name` varchar(255) NOT NULL,
  `primitive_test_id` bigint(20) NOT NULL,
  `script_content` longtext NOT NULL,
  `status` varchar(255) DEFAULT NULL,
  `synopsis` varchar(255) DEFAULT NULL,
  `groups_id` bigint(20) DEFAULT NULL,
  `execution_time` int(11) NOT NULL,
  `remarks` varchar(255) NOT NULL,
  `skip` bit(1) NOT NULL,
  `long_duration` bit(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `FKC9E5D0CB67097214` (`primitive_test_id`),
  KEY `FKC9E5D0CB984B586A` (`groups_id`),
  CONSTRAINT `FKC9E5D0CB67097214` FOREIGN KEY (`primitive_test_id`) REFERENCES `primitive_test` (`id`),
  CONSTRAINT `FKC9E5D0CB984B586A` FOREIGN KEY (`groups_id`) REFERENCES `groups` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1738 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `script_box_type`
--

DROP TABLE IF EXISTS `script_box_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `script_box_type` (
  `script_box_types_id` bigint(20) DEFAULT NULL,
  `box_type_id` bigint(20) DEFAULT NULL,
  KEY `FK7583C622B8519149` (`script_box_types_id`),
  KEY `FK7583C62241CE91C` (`box_type_id`),
  CONSTRAINT `FK7583C62241CE91C` FOREIGN KEY (`box_type_id`) REFERENCES `box_type` (`id`),
  CONSTRAINT `FK7583C622B8519149` FOREIGN KEY (`script_box_types_id`) REFERENCES `script` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;



--
-- Table structure for table `script_file`
--

DROP TABLE IF EXISTS `script_file`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `script_file` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `version` bigint(20) NOT NULL,
  `module_name` longtext,
  `script_name` longtext NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1017 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `script_file`
--

LOCK TABLES `script_file` WRITE;
/*!40000 ALTER TABLE `script_file` DISABLE KEYS */;
INSERT INTO `script_file` VALUES (1,0,'closedcaption','CC_SetGet_Attribute_BgColor_BoundHigh_56'),(2,0,'closedcaption','CC_SetGet_Attribute_EdgeType_invalid_53'),(3,0,'closedcaption','CC_Get_SupportedServiceNumberCount_ServiceNumber_23'),(4,0,'closedcaption','CC_SetGet_Attribute_FontSize_08'),(5,0,'closedcaption','CC_Get_Attribute_FontUnderline_default_32'),(6,0,'closedcaption','CC_SetGet_Attribute_BorderType_BoundHigh_63'),(7,0,'closedcaption','CC_SetGet_AnalogChannel_19'),(8,0,'closedcaption','CC_SetGet_Attribute_FontStyle_invalid_45'),(9,0,'closedcaption','CC_SetGet_Attribute_FontOpacity_invalid_43'),(10,0,'closedcaption','CC_Get_Attribute_BorderColor_default_34'),(11,0,'closedcaption','CC_SetGet_Attribute_EdgeColor_16'),(12,0,'closedcaption','CC_SetGet_Attribute_FontItalic_invalid_47'),(13,0,'closedcaption','CC_SetGet_Attribute_BorderColor_12'),(14,0,'closedcaption','CC_SetGet_Attribute_FontColor_BoundLow_69'),(15,0,'closedcaption','CC_SetGet_Attribute_BGOpacity_invalid_44'),(16,0,'closedcaption','CC_SetGet_InvalidDigitalChannel_18'),(17,0,'closedcaption','CC_SetGet_Attribute_BgColor_BoundLow_70'),(18,0,'closedcaption','CC_Get_Attribute_FontSize_default_30'),(19,0,'closedcaption','CC_Get_Attribute_FontItalic_default_31'),(20,0,'closedcaption','CC_SetGet_Attribute_WinOpacity_invalid_52'),(21,0,'closedcaption','CC_SetGet_Attribute_FontColor_BoundHigh_55'),(22,0,'closedcaption','CC_SetGet_Attribute_EdgeType_BoundHigh_67'),(23,0,'closedcaption','CC_SetGet_Attribute_WinBorderColor_13'),(24,0,'closedcaption','CC_ResetTrickPlayStatus_24'),(25,0,'closedcaption','CC_SetGet_Attribute_BorderColor_BoundHigh_64'),(26,0,'closedcaption','CC_Get_Attribute_WinOpacity_default_36'),(27,0,'closedcaption','CC_SetGet_Attribute_WinBorderColor_invalid_51'),(28,0,'closedcaption','CC_Get_Attribute_FontColor_default_26'),(29,0,'closedcaption','CC_Get_Attribute_WinBorderColor_default_35'),(30,0,'closedcaption','CC_Hide_22'),(31,0,'closedcaption','CC_SetGet_Attribute_FontColor_invalid_41'),(32,0,'closedcaption','CC_SetGet_Attribute_FontUnderline_invalid_48'),(33,0,'closedcaption','CC_Get_Attribute_EdgeColor_default_38'),(34,0,'closedcaption','CC_SetGet_Attribute_BGOpacity_BoundHigh_58'),(35,0,'closedcaption','CC_Get_Attribute_BorderType_default_33'),(36,0,'closedcaption','CC_Get_Attribute_FontStyle_default_29'),(37,0,'closedcaption','CC_SetGet_Attribute_FontItalic_BoundLow_75'),(38,0,'closedcaption','CC_Show_21'),(39,0,'closedcaption','CC_SetGet_DigitalChannel_17'),(40,0,'closedcaption','CC_SetGet_Attribute_FontItalic_BoundHigh_61'),(41,0,'closedcaption','CC_SetGet_Attribute_WinOpacity_14'),(42,0,'closedcaption','CC_Get_Attribute_FontOpacity_default_27'),(43,0,'closedcaption','CC_SetGet_Attribute_FontSize_BoundHigh_60'),(44,0,'closedcaption','CC_SetGet_Attribute_WindowOpacity_BoundHigh_66'),(45,0,'closedcaption','CC_SetGet_Attribute_EdgeColor_invalid_54'),(46,0,'closedcaption','CC_SetGet_Attribute_BGOpacity_BoundLow_72'),(47,0,'closedcaption','CC_Initialization_01'),(48,0,'closedcaption','CC_SetGet_Attribute_WinBorderColor_BoundHigh_65'),(49,0,'closedcaption','CC_SetGet_Invalid_AnalogChannel_20'),(50,0,'closedcaption','CC_SetGet_Attribute_EdgeType_15'),(51,0,'closedcaption','CC_SetGet_Attribute_FontOpacity_BoundHigh_57'),(52,0,'closedcaption','CC_SetGet_Attribute_FontSize_invalid_46'),(53,0,'closedcaption','CC_SetGet_Attribute_BorderColor_invalid_50'),(54,0,'closedcaption','CC_Get_Attribute_EdgeType_default_37'),(55,0,'closedcaption','CC_SetGet_Attribute_FontStyle_07'),(56,0,'closedcaption','CC_SetGet_Attribute_FontOpacity_05'),(57,0,'closedcaption','CC_SetGet_Attribute_FontUnderline_10'),(58,0,'closedcaption','CC_SetGet_Attribute_BGOpacity_06'),(59,0,'closedcaption','CC_SetGet_Attribute_FontItalic_09'),(60,0,'closedcaption','CC_SetGet_Attribute_BgColor_invalid_42'),(61,0,'closedcaption','CC_SetGet_Attribute_FontColor_03'),(62,0,'closedcaption','CC_SetGet_Attribute_BgColor_04'),(63,0,'closedcaption','CC_SetGet_Attribute_FontStyle_BoundHigh_59'),(64,0,'closedcaption','CC_SetTrickPlayStatus_25'),(65,0,'closedcaption','CC_SetGet_Attribute_BorderType_invalid_49'),(66,0,'closedcaption','CC_Get_Attribute_BGOpacity_default_28'),(67,0,'closedcaption','CC_SetGet_Attribute_BorderType_11'),(68,0,'closedcaption','CC_SetGet_Attribute_FontUnderline_BoundLow_76'),(69,0,'closedcaption','CC_SetGet_Attribute_FontUnderline_BoundHigh_62'),(70,0,'closedcaption','CC_SetGet_State_02'),(71,0,'closedcaption','CC_SetGet_Attribute_EdgeColor_BoundHigh_68'),(72,0,'closedcaption','CC_SetGet_Attribute_FontColor_190'),(73,0,'closedcaption','CC_SetGet_Attribute_FontColor_191'),(74,0,'closedcaption','CC_SetGet_Attribute_FontColor_192'),(75,0,'closedcaption','CC_SetGet_Attribute_FontColor_193'),(76,0,'closedcaption','CC_SetGet_Attribute_FontColor_194'),(77,0,'closedcaption','CC_SetGet_Attribute_FontColor_195'),(78,0,'closedcaption','CC_SetGet_Attribute_FontColor_196'),(79,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_DAC_InitTimeStamp_103'),(80,0,'rdk_logger','RDKLogger_Log_InverseTrace'),(81,0,'iarmbus','IARMBUS BusCall MFR-Hardware version test'),(82,0,'tr69','TR069_Get_DeviceIPInterfaceNumOfEntries_32'),(83,0,'iarmbus','IARMBUS BusCall MFR-First Use Date test'),(84,0,'devicesettings','DS_Resolution_1080p60_test_92'),(85,0,'tr69','TR069_Get_DeviceModelName_03'),(86,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_DSG_CATunnel_97'),(87,0,'tr69','TR069_Get_DeviceProcessStatusCommandDefaultProcess_20'),(88,0,'iarmbus','IARMBUS_BusCall_MFR-MOCA_MAC_59'),(89,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_Docsis_95'),(90,0,'tr69','TR069_Get_DeviceProcessStatusPriorityDefaultProcess_22'),(91,0,'iarmbus','IARMBUS_BusCall_MFR-DeletePDRI_image_61'),(92,0,'tr69','TR069_Get_DeviceManufacturer_01'),(93,0,'tr69','TR069_Get_DeviceEthernetInterfaceDefaultEnable_44'),(94,0,'tr69','TR069_Get_DeviceFirstUseDate_12'),(95,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_ECMIP_92'),(96,0,'tr69','TR069_Get_DeviceXCOMSTBIP_14'),(97,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_Download_101'),(98,0,'mediaframework','RMF_HNSrcMPSink_InvalidRewindSpeed_10'),(99,0,'devicesettings','DS_Resolution_576p50_test_86'),(100,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_EstbIP_91'),(101,0,'iarmbus','IARMBUS_BusCall_MFR-Validateandwriteimage_into_flash_63'),(102,0,'tr69','TR069_Get_DeviceHardwareVersion_07'),(103,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_GetSetHDCPProfile_67'),(104,0,'tr69','TR069_Get_DeviceProcessorArchitecture_25'),(105,0,'rdk_logger','RDKLogger_Log_Trace6'),(106,0,'tr69','TR069_Get_DeviceIPDefaultInterfaceMaxMTUSize_39'),(107,0,'iarmbus','IARMBUS_BusCall_MFR-HDMIHDCP_60'),(108,0,'mediaframework','RMF_DVRManager_DeleteRecording'),(109,0,'rdk_logger','RDKLogger_Log_InvalidLevel'),(110,0,'iarmbus','IARM_BUS_SysMgr_Event_XUPNP_Data_Update_72'),(111,0,'devicesettings','DS_Resolution_Invalid_value_test_94'),(112,0,'rdk_logger','RDKLogger_SetLogLevel'),(113,0,'devicesettings','DS_Resolution_480i_test_82'),(114,0,'rdk_logger','RDKLogger_Log_Trace7'),(115,0,'tr69','TR069_Get_DeviceEthernetInterfaceDefaultDuplexMode_50'),(116,0,'devicesettings','DS_SetblueColor_REMOTE_LED_30'),(117,0,'tr69','TR069_Get_DeviceIPv4Capable_29'),(118,0,'mediastreamer','RMF_MS_ContinousCH_Change_test'),(119,0,'devicesettings','DS_SetStereoMode_STEREO_FORMAT_70'),(120,0,'devicesettings','DS_Resolution_STRESS_test_112'),(121,0,'tr69','TR069_Get_DeviceProcessStatusStateDefaultProcess_24'),(122,0,'iarmbus','IARM_BUS_SysMgr_Event_Card_FwDNLD_73'),(123,0,'iarmbus','IARMBUS Broadcast IR event'),(124,0,'tr69','TR069_Get_DeviceEthernetInterfaceDefaultUpstream_47'),(125,0,'devicesettings','DS_Resolution_1080p30_test_91'),(126,0,'iarmbus','IARMBUS BusCall MFR-Software version test'),(127,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_ECMMac_105'),(128,0,'rdk_logger','RDKLogger_Log_UnknownModule'),(129,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_PlantId_107'),(130,0,'tr69','TR069_Get_DeviceIPv4Enable_30'),(131,0,'iarmbus','IARMBUS BusCall MFR-Board description test'),(132,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_VideoPresenting_83'),(133,0,'devicesettings','DS_Resolution_720p_test_83'),(134,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_CMAC_79'),(135,0,'iarmbus','IARMBUS_DiskMgr_Event_HwDisk_18'),(136,0,'tr69','TR069_Get_DeviceManufacturerOUI_02'),(137,0,'devicesettings','DS_SetStereoMode_STRESS_test_110'),(138,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_HDMIOut_84'),(139,0,'rdk_logger','RDKLogger_GetLogLevel'),(140,0,'rdk_logger','RDKLogger_Log_All_None'),(141,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_VOD_AD_102'),(142,0,'tr69','TR069_Get_DeviceIPActivePortNumOfEntries_33'),(143,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_CableCard_98'),(144,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_CVRSubsystem_100'),(145,0,'rdk_logger','RDKLogger_Log_Trace4'),(146,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_Moca_94'),(147,0,'tr69','TR069_Get_DeviceAdditionalSoftwareVersion_09'),(148,0,'devicesettings','DS_SetStereoMode_SURROUND_FORMAT_71'),(149,0,'tr69','TR069_Get_DeviceMemoryStatusFree_27'),(150,0,'devicesettings','DS_SetStereoMode_UNKNOWN_72'),(151,0,'mediaframework','RMF_HNSrc_MPSink_DVR_Play_26'),(152,0,'rdk_logger','RDKLogger_Log_Error'),(153,0,'rdk_logger','RDKLogger_GetDefaultLevel'),(154,0,'devicesettings','DS_SetDB_Invalid_Value_test_58'),(155,0,'tr69','TR069_Get_DeviceEthernetInterfaceDefaultName_46'),(156,0,'rdk_logger','RDKLogger_Log_InverseLevel'),(157,0,'tr69','TR069_Get_DeviceProcessStatusCPUTimeDefaultProcess_23'),(158,0,'tr69','TR069_Get_DeviceXCOMPowerStatus_16'),(159,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_DACId_106'),(160,0,'mediaframework','RMF_HNSrc_MPSink_SetGetmediaTime_03'),(161,0,'rdk_logger','RDKLogger_Log_Trace3'),(162,0,'tr69','TR069_Get_DeviceEthernetInterfaceNumOfEntries_43'),(163,0,'tr69','TR069_Get_DeviceEthernetInterfaceDefaultStatus_45'),(164,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_MotoHRVRX_81'),(165,0,'iarmbus','IARM_BUS_SysMgr_Event_HDCPProfile_update_74'),(166,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_LANIP_93'),(167,0,'devicesettings','DS_SetStereoModes test_12'),(168,0,'iarmbus','IARMBUS BusCall MFR- Provision Code test'),(169,0,'iarmbus','IARMBUS_Reset_WareHouse_state_64'),(170,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_StbSerialNo_65'),(171,0,'iarmbus','IARMBUS_BusCall_MFR-Device_MAC_58'),(172,0,'iarmbus','IARM_BUS_DiskMgr_Event_ExtHDD_Pair_20'),(173,0,'mediaframework','RMF_HNSrc_MPSink_BufferClearing_17'),(174,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_70'),(175,0,'devicesettings','DS_Resolution_Invalid_port_test_93'),(176,0,'tr69','TR069_Get_DeviceSerialNumber_06'),(177,0,'tr69','TR069_Get_DeviceIPDefaultInterfaceType_40'),(178,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_CableCard_SerialNo_104'),(179,0,'devicesettings','DS_Resolution_1080i50_test_90'),(180,0,'devicesettings','DS_Resolution_1080p24_test_88'),(181,0,'tr69','TR069_Get_DeviceIPDefaultInterfaceName_37'),(182,0,'tr69','TR069_Get_DeviceXCOMSTBMAC_13'),(183,0,'mediastreamer','RMF_MS_ContionusDVR_Playback'),(184,0,'tr69','TR069_Get_DeviceEthernetInterfaceDefaultMaxBitRate_49'),(185,0,'mediaframework','RMF_HNSrc_MPSink_InvalidMediaTime_13'),(186,0,'rdk_logger','RDKLogger_Log_DefaultLevel'),(187,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_CardCisco_Status_82'),(188,0,'mediaframework','RMF_HNSrc_MPSink_Pause&Rewind_38'),(189,0,'iarmbus','IARMBUS BusCall MFR-Model Name test'),(190,0,'tr69','TR069_Get_DeviceUpTime_11'),(191,0,'devicesettings','DS_Resolution_1080i_test_84'),(192,0,'iarmbus','IARM_BUS_DiskMgr_Event_ExtHDD_19'),(193,0,'rdk_logger','RDKLogger_Log_Trace9'),(194,0,'devicesettings','DS_SetStereoMode_MONO_FORMAT_69'),(195,0,'mediaframework','RMF_HNSrcMPSink_Video_Play_01'),(196,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_ExitOk_78'),(197,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_CableCardDWLD_99'),(198,0,'iarmbus','IARMBUS Set Power state'),(199,0,'iarmbus','IARMBUS BusCall MFR-Board Product Class test'),(200,0,'iarmbus','IARMBUS BusCall MFR-STB Manufature Name test'),(201,0,'tr69','TR069_Get_DeviceIPDefaultInterfaceStatus_36'),(202,0,'rdk_logger','RDKLogger_GetEnv_UnknownModule'),(203,0,'rdk_logger','RDKLogger_Log_None_All'),(204,0,'iarmbus','IARM_BUS_DiskMgr_Event_ExtHDD_Off_22'),(205,0,'devicesettings','DS_Resolution_720p50_test_87'),(206,0,'rdk_logger','RDKLogger_Log_Notice'),(207,0,'tr69','TR069_Get_DeviceIPDefaultInterfaceReset_38'),(208,0,'tr69','TR069_Get_DeviceDeviceInfoNegative_51'),(209,0,'mediaframework','RMF_HNSrc_MPSink_LivetsbReset_19'),(210,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_FirmwareDWLD_87'),(211,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_CASystem_90'),(212,0,'rdk_logger','RDKLogger_Log_Trace8'),(213,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_TimeSource_88'),(214,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_BootUp_66'),(215,0,'tr69','TR069_Get_DeviceProcessStatusSizeDefaultProcess_21'),(216,0,'rdk_logger','RDKLogger_Dbg_Enabled_Status'),(217,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_TimeZone_89'),(218,0,'tr69','TR069_Get_DeviceIPDefaultInterfaceEnable_34'),(219,0,'tr69','TR069_Get_DeviceSoftwareVersion_08'),(220,0,'mediaframework','RMF_HNSrcMPSink_InvalidSpeed_09'),(221,0,'rdk_logger','RDKLogger_Log_Debug'),(222,0,'tr69','TR069_Get_DeviceIPv4Status_31'),(223,0,'tr69','TR069_Get_DeviceProcessStatusCPUUsage_18'),(224,0,'rdk_logger','RDKLogger_Log_Info'),(225,0,'rdk_logger','RDKLogger_Log_All'),(226,0,'devicesettings','DS_Resolution_480p_test_85'),(227,0,'rdk_logger','RDKLogger_Log_None'),(228,0,'tr69','TR069_Get_DeviceXCOMFirmwareFileName_15'),(229,0,'rdk_logger','RDKLogger_Log_Trace2'),(230,0,'tr69','TR069_Get_DeviceProvisioningCode_10'),(231,0,'iarmbus','IARMBUS BusCall MFR-SerialNumber test'),(232,0,'rdk_logger','RDKLogger_Log_MPEOSDisabled'),(233,0,'tr69','TR069_Get_DeviceEthernetInterfaceDefaultMACAddress_48'),(234,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_HDCPEnabled_85'),(235,0,'rdk_logger','RDKLogger_Log_Warning'),(236,0,'iarmbus','IARM_BUS_SysMgr_Event_XUPNP_Data_Request_71'),(237,0,'rdk_logger','RDKLogger_Log_Trace5'),(238,0,'rdk_logger','RDKLogger_Log_Trace1'),(239,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_MotoEntitlement_80'),(240,0,'tr69','TR069_Get_DeviceMemoryStatusTotal_26'),(241,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_HDCPProfileEvent_68'),(242,0,'iarmbus','IARMBUS_BusCall_MFR-Scruballbanks_62'),(243,0,'rdk_logger','RDKLogger_Log_Fatal'),(244,0,'rdk_logger','RDKLogger_MaxLogLine'),(245,0,'iarmbus','IARM_BUS_DiskMgr_Event_ExtHDD_On_21'),(246,0,'tr69','TR069_Get_DeviceProcessorNumOfEntries_17'),(247,0,'tr69','TR069_Get_DeviceIPDefaultInterfaceLoopback_41'),(248,0,'rdk_logger','RDKLogger_Log_Trace'),(249,0,'iarmbus','IARMBUS BusCall MFR-OUI test'),(250,0,'mediaframework','RMF_HNSrc_MPSink_InvalidMediaTime_14'),(251,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_DsgBroadCastChannel_96'),(252,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_HDMI_EDID_Ready_86'),(253,0,'tr69','TR069_Get_DeviceProcessStatusPIDDefaultProcess_19'),(254,0,'devicesettings','DS_Resolution_1080p_test_89'),(255,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_TuneReady_77'),(256,0,'rdk_logger','RDKLogger_CheckMPELogEnabled'),(257,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_ChannelMap_75'),(258,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_DisconnectMGR_76'),(259,0,'tr69','TR069_Get_DeviceIPDefaultInterfaceIPv4Enable_35'),(260,0,'mediaframework','RMF_HNSrc_GetBufferedRanges_04'),(261,0,'iarmbus','IARMBUS_DummyEvt_Persistent_test'),(262,0,'iarmbus','IARMBUS_DummyCall_Persistent_test'),(263,0,'mediaframework','RMF_HNSrc_MPSink_Pause&FF_39'),(264,0,'mediaframework','RMF_HNSrc_MPSink_SetSpeed_64x_12'),(265,0,'mediastreamer','RMF_MS_LivePlayback_test'),(266,0,'mediastreamer','RMF_MS_LongTime_LivePlayback'),(267,0,'mediastreamer','RMF_MS_RecordingPlayback'),(268,0,'mediastreamer','RMF_MS_Without_StreamInit'),(269,0,'iarmbus','IARMBUS Connect & Disconnect test'),(270,0,'iarmbus','IARMBUS_Term_Without_Init_42'),(271,0,'iarmbus','IARMBUS IsConnected test'),(272,0,'iarmbus','IARMBUS Init Negative test'),(273,0,'gst-plugins-rdk','GstPluginRdk_Aesdecrypt_DecryptEnable_True'),(274,0,'gst-plugins-rdk','GstPluginRdk_Aesdecrypt_DecryptEnable_False'),(275,0,'gst-plugins-rdk','GstPluginRdk_Aesdecrypt_DecryptEnable_Invalid'),(276,0,'iarmbus','IARMBUS Broadcast ResolutionChange Event test'),(277,0,'iarmbus','IARMBUS BusCall test'),(278,0,'iarmbus','IARMBUS Query Key Repeat Interval test'),(279,0,'iarmbus','IARMBUS Query Power state'),(280,0,'iarmbus','IARMBUS Register for Resource Available event test'),(281,0,'iarmbus','IARMBUS RegisterCall test'),(282,0,'iarmbus','IARMBUS RegisterEventMax'),(283,0,'iarmbus','IARMBUS Release Resource test'),(284,0,'iarmbus','IARMBUS Request decoder-0 test'),(285,0,'iarmbus','IARMBUS Request decoder-1 test'),(286,0,'iarmbus','IARMBUS Request display_resolution_change  test'),(287,0,'iarmbus','IARMBUS Request graphics plane-0 test'),(288,0,'iarmbus','IARMBUS Request graphics plane-1 test'),(289,0,'iarmbus','IARMBUS Request power  test'),(290,0,'iarmbus','IARMBUS Request same resource from same application test'),(291,0,'iarmbus','IARMBUS Request same resource in different application test'),(292,0,'iarmbus','IARMBUS Set Key Repeat Interval test'),(293,0,'iarmbus','IARMBUS Unregister with out Register Event Handler test'),(294,0,'iarmbus','IARMBUS unregisterEvt Handler test'),(295,0,'iarmbus','IARMBUS_Disconnect_without_connect_55'),(296,0,'iarmbus','IARMBUS_Init_with_Invalidparameter_test_43'),(297,0,'iarmbus','IARMBUS_Init_with_Invalid_App_test_44'),(298,0,'iarmbus','IARMBUS_IsConnected_Invalid_Membername_54'),(299,0,'iarmbus','IARMBUS_IsConnect_STRESS_57'),(300,0,'iarmbus','IARMBUS_IsConnect_Without_Connect_53'),(301,0,'iarmbus','IARMBUS_RegisterEvtHandler_With_NegId_48'),(302,0,'iarmbus','IARMBUS_RegisterEvtHandler_With_PosId_47'),(303,0,'iarmbus','IARMBUS_RegUnReg_STRESS_51'),(304,0,'iarmbus','IARMBUS_Release_Invalid_Resource_52'),(305,0,'iarmbus','IARMBUS_Request_FOCUS_Resource_50'),(306,0,'iarmbus','IARMBUS_Request_Invalid_Resource_49'),(307,0,'iarmbus','IARMBUS_Request_resource_STRESS_56'),(308,0,'iarmbus','IARMBUS_unregisterEvtHandler_With_PosId_45'),(309,0,'trm','TRM_GetAllTunerStates'),(310,0,'devicesettings','DS_SetAudioLevel_value outof range_test_54'),(311,0,'devicesettings','DS_Resolution test_16'),(312,0,'trm','TRM_GetAllTunerIds'),(313,0,'trm','TRM_GetAllReservations'),(314,0,'trm','TRM_GetVersion'),(315,0,'mediaframework','RMF_QAMSource_OpenClose_02'),(316,0,'trm','TRM_TunerReserveForRecord'),(317,0,'trm','TRM_TunerReserveForLive'),(318,0,'gst-plugins-rdk','GstPluginRdk_Aesdecrypt_DecryptEnable_Negative'),(319,0,'gst-plugins-rdk','GstPluginRdk_Aesencrypt_EncryptionEnable_True'),(320,0,'gst-plugins-rdk','GstPluginRdk_Aesencrypt_EncryptionEnable_False'),(321,0,'gst-plugins-rdk','GstPluginRdk_Aesencrypt_EncryptionEnable_Invalid'),(322,0,'gst-plugins-rdk','GstPluginRdk_Aesencrypt_EncryptionEnable_Negative'),(323,0,'gst-plugins-rdk','GstPluginRdk_Aesencrypt_EncryptEnable_Get_Default'),(324,0,'gst-plugins-rdk','GstPluginRdk_Dvrsrc_RecordId_Set_Prop'),(325,0,'gst-plugins-rdk','GstPluginRdk_Dvrsrc_SegmentName_Get_Prop_Default'),(326,0,'gst-plugins-rdk','GstPluginRdk_Dvrsrc_Ccivalue_Get_Prop_Default'),(327,0,'gst-plugins-rdk','GstPluginRdk_Dvrsrc_Rate_Set_Prop'),(328,0,'gst-plugins-rdk','GstPluginRdk_Dvrsrc_Rate_Set_Prop_ValueGreater_64'),(329,0,'gst-plugins-rdk','GstPluginRdk_Dvrsrc_Rate_Set_Prop_ValueLesser_Negative64'),(330,0,'gst-plugins-rdk','GstPluginRdk_Dvrsrc_Rate_Get_Prop_Default'),(331,0,'gst-plugins-rdk','GstPluginRdk_Dvrsrc_StartTime_Get_Prop_Default'),(332,0,'gst-plugins-rdk',' GstPluginRdk_Dvrsrc_Duration_Get_Prop_Default'),(333,0,'gst-plugins-rdk','GstPluginRdk_Dvrsrc_PlayStartPosition_Set_Prop'),(334,0,'gst-plugins-rdk','GstPluginRdk_Dvrsrc_PlayStartPosition_Set_Prop_Negative'),(335,0,'gst-plugins-rdk','GstPluginRdk_Dvrsrc_PlayStartPosition_Get_Prop_Default'),(336,0,'gst-plugins-rdk',' GstPluginRdk_Dvrsink_RecordId_Set_Prop'),(337,0,'gst-plugins-rdk','GstPluginRdk_Dvrsink_RecordId_Get_Prop_Default'),(338,0,'gst-plugins-rdk','GstPluginRdk_Dvrsink_Ccivalue_Get_Prop_Default'),(339,0,'gst-plugins-rdk',' GstPluginRdk_Aesdecrypt_DecryptEnable_Get_Default'),(340,0,'gst-plugins-rdk','GstPluginRdk_Dvrsrc_RecordId_Get_Prop_Default'),(341,0,'gst-plugins-rdk','GstPluginRdk_Dvrsrc_SegmentName_Set_Prop'),(342,0,'mediaframework','RMF_HNSrcMPSink_Video_MuteUnmute_06'),(343,0,'mediaframework','RMF_HNSrcMPSink_Video_Pause_02'),(344,0,'mediaframework','RMF_HNSrcMPSink_Video_Play_Position_04'),(345,0,'mediaframework','RMF_HNSrcMPSink_Video_Skip_Backward_03'),(346,0,'mediaframework','RMF_HNSrcMPSink_Video_Speed_08'),(347,0,'trm','TRM_ReleaseTunerReservation'),(348,0,'trm','TRM_ValidateTunerReservation'),(349,0,'mediaframework','RMF_HNSrcMPSink_Video_State_05'),(350,0,'mediaframework','RMF_HNSrcMPSink_Video_Volume_07'),(351,0,'mediaframework','RMF_HNSrc_MPSink_DoublePlay_40'),(352,0,'trm','TRM_CancelRecording'),(353,0,'mediaframework','RMF_HNSrc_MPSink_DVRReplay_37'),(354,0,'mediaframework','RMF_HNSrc_MPSink_DVR_FF_16x_30'),(355,0,'mediaframework','RMF_HNSrc_MPSink_DVR_FF_32x_29'),(356,0,'mediaframework','RMF_HNSrc_MPSink_DVR_FF_4x_31'),(357,0,'mediaframework','RMF_HNSrc_MPSink_DVR_FF_64x_32'),(358,0,'mediaframework','RMF_HNSrc_MPSink_DVR_REW_16x_35'),(359,0,'mediaframework','RMF_HNSrc_MPSink_DVR_REW_32x_34'),(360,0,'mediaframework','RMF_HNSrc_MPSink_DVR_REW_4x_36'),(361,0,'mediaframework','RMF_HNSrc_MPSink_DVR_REW_64x_33'),(362,0,'mediaframework','RMF_HNSrc_MPSink_FF_16x_22'),(363,0,'mediaframework','RMF_HNSrc_MPSink_FF_32x_28'),(364,0,'mediaframework','RMF_HNSrc_MPSink_FF_4x_21'),(365,0,'mediaframework','RMF_HNSrc_MPSink_FF_64x_20'),(366,0,'mediaframework','RMF_HNSrc_MPSink_GetState_25'),(367,0,'mediaframework','RMF_HNSrc_MPSink_Startoftsb_27'),(368,0,'trm','TRM_CancelLive'),(369,0,'mediaframework','RMF_HNSrc_MPSink_SetSpeed_32x_11'),(370,0,'mediaframework','RMF_HNSrc_MPSink_REW_4x_24'),(371,0,'mediaframework','RMF_HNSrc_MPSink_REW_16x_23'),(372,0,'mediaframework','RMF_HNSrc_MPSink_Rewind&CheckSpeed_16'),(373,0,'mediaframework','RMF_HNSrc_MPSink_Pause&CheckMediaTime_15'),(374,0,'devicesettings','DS_PowerMode Listener test_13'),(375,0,'devicesettings','DS_SetPowerMode_Invalid_test_98'),(376,0,'devicesettings','DS_SetPowerMode_OFF_test_96'),(377,0,'devicesettings','DS_SetPowerMode_ON_test_95'),(378,0,'devicesettings','DS_SetPowerMode_STANDBY_test_97'),(379,0,'devicesettings','DS_SetPowerMode_STRESS_test_99'),(380,0,'rdk_logger','RDKLogger_EnvGet'),(381,0,'mediaframework','RMF_QAMSrc_06'),(382,0,'mediaframework','RMF_QAMSource_Play_03'),(383,0,'mediaframework','RMF_QAMSource_Pause_04'),(384,0,'mediaframework','RMF_QAMSrc_04'),(385,0,'mediaframework','RMF_QAMSource_ChangeURI_11'),(386,0,'mediaframework','RMF_QAMSource_Play_12'),(387,0,'mediaframework','RMF_QAMSource_Pause_13'),(388,0,'mediaframework','RMF_QAMSource_ChangeURI_14'),(389,0,'mediaframework','RMF_QAMSource_Get_Free_LowLevelElement_09'),(390,0,'mediaframework','RMF_DVRManager_GetRecordingSegmentInfoByIndex'),(391,0,'tr69','TR069_Get_DeviceMoCAInterfaceNumOfEntries_53'),(392,0,'tr69','TR069_Get_DeviceSTBServiceComponentsHDMIDisplayDevice_XCOM_EDID_82'),(393,0,'mediaframework','RMF_DVRSrcMPSink_Play_01'),(394,0,'tr69','TR069_Get_DeviceMoCAInterfaceEnable_54'),(395,0,'tr69','TR069_Get_DeviceMoCAInterfaceStatus_55'),(396,0,'tr69','TR069_Get_DeviceMoCAInterfaceLastChange_56'),(397,0,'tr69','TR069_Get_DeviceMoCAInterfaceUpstream_57'),(398,0,'servicemanager','SM_RegisterService test'),(399,0,'servicemanager','SM_RegisterService_All'),(400,0,'servicemanager','SM_DeviceSetting_GetDeviceInfo'),(401,0,'servicemanager','SM_UnRegisterService test'),(402,0,'servicemanager','SM_UnRegisterService_All'),(403,0,'tr69','TR069_Get_DeviceMoCAInterfaceMACAddress_58'),(404,0,'servicemanager','SM_ScreenCapture_Upload'),(405,0,'tr69','TR069_Get_DeviceMoCAInterfaceFirmwareVersion_59'),(406,0,'servicemanager','SM_DoesServiceExist_All'),(407,0,'servicemanager','SM_WebSocket_GetBufferedAmount'),(408,0,'servicemanager','SM_WebSocket_GetProtocol'),(409,0,'tr69','TR069_Get_DeviceMoCAInterfaceMaxBitRate_60'),(410,0,'servicemanager','SM_WebSocket_GetReadyState'),(411,0,'servicemanager','SM_WebSocket_GetUrl'),(412,0,'tr69','TR069_Get_DeviceMoCAInterfaceMaxIngressBW_61'),(413,0,'tr69','TR069_Get_DeviceMoCAInterfaceMaxEgressBW_62'),(414,0,'tr69','TR069_Get_DeviceMoCAInterfaceHighestVersion_63'),(415,0,'tr69','TR069_Get_DeviceMoCAInterfaceCurrentVersion_64'),(416,0,'tr69','TR069_Get_DeviceMoCAInterfaceNetworkCoordinator_65'),(417,0,'tr69','TR069_Get_DeviceMoCAInterfaceNodeID_66'),(418,0,'devicesettings','DS_SetScroll_Maximum_Value_test_49'),(419,0,'tr69','TR069_Get_DeviceMoCAInterfaceMaxNodes_67'),(420,0,'tr69','TR069_Get_DeviceMoCAInterfaceAssociatedDeviceNumberOfEntries_68'),(421,0,'tr69','TR069_Get_DeviceMoCAInterfaceAssociatedDevice1NodeID_69'),(422,0,'tr69','TR069_Get_DeviceMoCAInterfaceQoSEgressNumFlows_71'),(423,0,'tr69','TR069_Get_DeviceMoCAInterfaceQoSFlowStats1FlowID_72'),(424,0,'tr69','TR069_Get_DeviceServicesSTBServiceNumberOfEntries_73'),(425,0,'tr69','TR069_Get_DeviceServicesSTBServiceComponentsHDMINumberOfEntries_74'),(426,0,'tr69','TR069_Get_DeviceServicesSTBServiceComponentsHDMI1Enable_75'),(427,0,'tr69','TR069_Get_DeviceServicesSTBServiceComponentsHDMI1Status_76'),(428,0,'tr69','TR069_Get_DeviceServicesSTBServiceComponentsHDMI1Name_77'),(429,0,'tr69','TR069_Get_DeviceServicesSTBServiceComponentsHDMI1ResolutionMode_78'),(430,0,'tr69','TR069_Get_DeviceServicesSTBServiceComponentsHDMI1ResolutionValue_79'),(431,0,'tr69','TR069_Get_DeviceServicesSTBServiceComponentsHDMI1DisplayDeviceStatus_80'),(432,0,'servicemanager','SM_GetGlobalService_All'),(433,0,'tr69','TR069_Get_DeviceServicesSTBServiceComponentsHDMI1DisplayDeviceEEDID_81'),(434,0,'tr69','TR069_Get_DeviceServicesSTBServiceComponentsVideoDecoderNumberOfEntries_83'),(435,0,'tr69','TR069_Get_DeviceServicesSTBServiceComponentsVideoDecoder1Name_84'),(436,0,'tr69','TR069_Get_DeviceServicesSTBServiceComponentsVideoDecoder1ContentAspectRatio_85'),(437,0,'mediaframework','RMF_QAMSource_ChangeChannel_Check_SPTS_Error_15'),(438,0,'devicesettings','DS_SetScroll test_05'),(439,0,'servicemanager','SM_GetSetting_All'),(440,0,'servicemanager','SM_CreateService_All'),(441,0,'servicemanager','SM_Services_GetName_All'),(442,0,'mediaframework','RMF_QAMSource_PlayLive_OneHour_18'),(443,0,'devicesettings','DS_mute_test_09'),(444,0,'mediaframework','RMF_QAMSource_ChangeChannelTwice_PlayOneHour_19'),(445,0,'mediaframework','RMF_QAMSource_ChangeChannel_FourTimes_16'),(446,0,'mediaframework','RMF_QAMSource_ChangeChannel_SevenTimes_17'),(447,0,'iarmbus','IARM_BUS_IRMgr_IRKey_Toggle'),(448,0,'devicesettings','DS_SetState_Stress_115'),(449,0,'devicesettings','DS_Brightness_Persistent_116'),(450,0,'devicesettings','DS_TextBrightness_Persistent_117'),(451,0,'devicesettings','DS_Resolution_Persistent_118'),(452,0,'devicesettings','DS_PowerModeToggle_Stress_119'),(453,0,'devicesettings','DS_ResolutionChange_VideoPlay_122'),(454,0,'devicesettings','DS_GetDisplayDetails_OnDisabledPort_123'),(455,0,'devicesettings','DS_Resolution_PortStateChange_120'),(456,0,'devicesettings','DS_Resolution_PowerModeChange_121'),(457,0,'tr69','TR069_Get_DeviceMoCAInterfaceAssociatedDeviceGetNodeID_Neg_70'),(458,0,'iarmbus','IARM_BUS_IRMgr_IRKey_ChangeChannelVol'),(459,0,'iarmbus','IARM_BUS_IRMgr_IRKey_CheckTrickplay'),(460,0,'iarmbus','IARM_BUS_IRMgr_IRKey_CheckSearch'),(461,0,'iarmbus','IARM_BUS_IRMgr_IRKey_CheckSetup'),(462,0,'tr69','TR069_Get_DeviceSevicesSTBServiceComponentsVideoDecoderName_Neg_86'),(463,0,'devicesettings','DS_GetAspect_Ratio_Reboot_test_114'),(464,0,'devicesettings','DS_GetDisplayDetails_Reboot_test_113'),(465,0,'servicemanager','SM_SetApiVersion_All'),(466,0,'servicemanager','SM_ScreenCapture_EventUpload'),(467,0,'servicemanager','SM_WebSocket_EventsAll'),(468,0,'servicemanager','SM_DisplaySetting_SetZoomSettings'),(469,0,'servicemanager','SM_DoesServiceExist Negative test'),(470,0,'servicemanager','SM_EnableMdvr test'),(471,0,'servicemanager','SM_EnableVpop test'),(472,0,'servicemanager','SM_GetGlobal Service test'),(473,0,'servicemanager','SM_GetRegisteredService test'),(474,0,'servicemanager','SM_RegisterForEvents test'),(475,0,'servicemanager','SM_SetApiVersion test'),(476,0,'servicemanager','SM_SetDeviceName test'),(477,0,'servicemanager','SM_SetResolution test'),(478,0,'devicesettings','DS_SetBlink_Invalid_test_39'),(479,0,'mediaframework','RMF_QAMSource_GetLtsId_06'),(480,0,'mediaframework','RMF_QAMSource_GetQAMSourceInstance_10'),(481,0,'mediaframework','RMF_QAMSource_GetTsId_05'),(482,0,'mediaframework','RMF_QAMSource_GetUseFactoryMethods_08'),(483,0,'mediaframework','RMF_QAMSource_InitTerm_01'),(484,0,'mediaframework','RMF_QAMSource_Init_Uninit_Platform_07'),(485,0,'mediaframework','RMF_QAMSrc_01'),(486,0,'mediaframework','RMF_QAMSrc_02'),(487,0,'mediaframework','RMF_QAMSrc_03'),(488,0,'mediaframework','RMF_QAMSrc_05'),(489,0,'mediaframework','RMF_QAMSrc_07'),(490,0,'mediaframework','RMF_QAMSrc_08'),(491,0,'mediaframework','RMF_QAMSrc_09'),(492,0,'devicesettings','DS_IsDynamicResolutionsSupport test_20'),(493,0,'mediaframework','RMF_DVRSrcMPSink_TrickPlayRate_FF4x_08'),(494,0,'mediaframework','RMF_DVRSrcMPSink_TrickPlayRate_FF64x_09'),(495,0,'mediaframework','RMF_DVRSrcMPSink_TrickPlayRate_FR4x_10'),(496,0,'mediaframework','RMF_DVRSrcMPSink_TrickPlayRate_FR64x_11'),(497,0,'mediaframework','RMF_DVRSrcMPSink_Resume_03'),(498,0,'trm','TRM_CT_14'),(499,0,'mediastreamer','RMF_MS_LiveTune_Request'),(500,0,'mediastreamer','RMF_MS_General_Error_Response'),(501,0,'mediastreamer','RMF_MS_Incomplete_URL_Request'),(502,0,'trm','TRM_CT_15'),(503,0,'rdk_logger','RDKLogger_EnvGetValueFromNum'),(504,0,'trm','TRM_CT_21'),(505,0,'mediaframework','RMF_HNSrc_MPSink_ChannelChange_CheckMacroblocking_41'),(506,0,'mediaframework','RMF_HNSrc_MPSink_DVR_FF_RW_CheckMacroblocking_42'),(507,0,'mediaframework','RMF_HNSrc_MPSink_DVR_RW_FF_CheckMacroblocking_43'),(508,0,'mediaframework','RMF_HNSrc_MPSink_DVR_FF_RW_SF_CheckMacroblocking_44'),(509,0,'mediaframework','RMF_HNSrc_MPSink_DVR_RW_FF_SF_CheckMacroblocking_45'),(510,0,'mediaframework','RMF_HNSrc_MPSink_DVR_FF_RW_SB_CheckMacroblocking_46'),(511,0,'mediaframework','RMF_HNSrc_MPSink_DVR_RW_FF_SB_CheckMacroblocking_47'),(512,0,'trm','TRM_CT_19'),(513,0,'mediaframework','RMF_HNSrc_MPSink_DVR_SF_SB_CheckMacroblocking_48'),(514,0,'mediaframework','RMF_HNSrc_MPSink_DVR_SB_SF_CheckMacroblocking_49'),(515,0,'mediaframework','RMF_HNSrc_MPSink_TSB_FF_CheckMacroblocking_50'),(516,0,'mediaframework','RMF_HNSrc_MPSink_TSB_FF_RW_CheckMacroblocking_51'),(517,0,'mediaframework','RMF_HNSrc_MPSink_TSB_SF_CheckMacroblocking_52'),(518,0,'mediaframework','RMF_HNSrc_MPSink_TSB_SF_CheckMacroblocking_53'),(519,0,'mediaframework','RMF_HNSrc_MPSink_TSB_ChangeResolution_Check_54'),(520,0,'trm','TRM_CT_43'),(521,0,'trm','TRM_CT_23'),(522,0,'trm','TRM_CT_25'),(523,0,'trm','TRM_CT_24'),(524,0,'trm','TRM_CT_33'),(525,0,'trm','TRM_CT_34'),(526,0,'dtcp','CT_DTCPAgent_01'),(527,0,'xupnp','CT_XUPNP_01'),(528,0,'trm','TRM_CT_20'),(529,0,'xupnp','CT_XUPNP_02'),(530,0,'trm','TRM_CT_42'),(531,0,'xupnp','CT_XUPNP_03'),(532,0,'xupnp','CT_XUPNP_04'),(533,0,'xupnp','CT_XUPNP_05'),(534,0,'trm','TRM_CT_39'),(535,0,'trm','TRM_CT_31'),(536,0,'xupnp','CT_XUPNP_06'),(537,0,'xupnp','CT_XUPNP_07'),(538,0,'trm','TRM_CT_32'),(539,0,'xupnp','CT_XUPNP_08'),(540,0,'trm','TRM_CT_30'),(541,0,'trm','TRM_CT_27'),(542,0,'xupnp','CT_XUPNP_09'),(543,0,'xupnp','CT_XUPNP_10'),(544,0,'xupnp','CT_XUPNP_11'),(545,0,'xupnp','CT_XUPNP_12'),(546,0,'xupnp','CT_XUPNP_13'),(547,0,'trm','TRM_CT_38'),(548,0,'xupnp','CT_XUPNP_14'),(549,0,'trm','TRM_CT_37'),(550,0,'dtcp','CT_DTCP_02'),(551,0,'dtcp','CT_DTCP_03'),(552,0,'dtcp','CT_DTCP_04'),(553,0,'dtcp','CT_DTCP_05'),(554,0,'dtcp','CT_DTCP_06'),(555,0,'dtcp','CT_DTCP_07'),(556,0,'dtcp','CT_DTCP_08'),(557,0,'dtcp','CT_DTCP_09'),(558,0,'dtcp','CT_DTCP_10'),(559,0,'dtcp','CT_DTCP_11'),(560,0,'trm','TRM_CT_29'),(561,0,'trm','TRM_CT_17'),(562,0,'trm','TRM_CT_18'),(563,0,'trm','TRM_CT_22'),(564,0,'trm','TRM_CT_26'),(565,0,'trm','TRM_CT_28'),(566,0,'trm','TRM_CT_41'),(567,0,'trm','TRM_CT_40'),(568,0,'trm','TRM_CT_35'),(569,0,'trm','TRM_CT_36'),(570,0,'devicesettings','DS_SetColor test_02'),(571,0,'devicesettings','DS_SetColor_green test_33'),(572,0,'devicesettings','DS_SetColor_invalid_test_37'),(573,0,'devicesettings','DS_SetColor_orange test_36'),(574,0,'devicesettings','DS_SetColor_red test_34'),(575,0,'devicesettings','DS_SetColor_STRESS_test_101'),(576,0,'devicesettings','DS_SetColor_yellow test_35'),(577,0,'devicesettings','DS_SetblueColor_INVALID_LED_32'),(578,0,'devicesettings','DS_SetblueColor_MESSAGE_LED_27'),(579,0,'devicesettings','DS_SetblueColor_POWER_LED_31'),(580,0,'devicesettings','DS_SetblueColor_RECORD_LED_28'),(581,0,'devicesettings','DS_SetblueColor_RFBYPASS_LED_29'),(582,0,'trm','TRM_TunerReserveAllForLive'),(583,0,'trm','TRM_TunerReserveForHyBrid'),(584,0,'trm','TRM_TunerReserveAllForRecord'),(585,0,'trm','TRM_CT_16'),(586,0,'mediaframework','RMF_Gst_LongDuration_Check_GstBuffer_Crash_55'),(587,0,'mediaframework','RMF_Gst_LongDuration_Check_GstQamTune_Crash_56'),(588,0,'devicesettings','DS_AddDisplayconnection Listener test_14'),(589,0,'devicesettings','DS_DTCP support test_19'),(590,0,'devicesettings','DS_GetAspect Ratio test_21'),(591,0,'devicesettings','DS_GetDisplayDetails test_22'),(592,0,'devicesettings','DS_HDCP Support test_18'),(593,0,'devicesettings','DS_IsContentProtection test_17'),(594,0,'devicesettings','DS_LoopThru test_08'),(595,0,'devicesettings','DS_SetAudioLevel test_06'),(596,0,'devicesettings','DS_SetAudioLevel_Maximum_test_52'),(597,0,'devicesettings','DS_SetAudioLevel_Minimum_test_51'),(598,0,'devicesettings','DS_SetAudioLevel_STRESS_test_106'),(599,0,'devicesettings','DS_SetAudioLevel_value in range_test_53'),(600,0,'devicesettings','DS_SetBlink test_03'),(601,0,'devicesettings','DS_SetBlink_outofrange_test_40'),(602,0,'devicesettings','DS_SetBlink_STRESS_test_102'),(603,0,'devicesettings','DS_SetBlink_valid_test_38'),(604,0,'devicesettings','DS_SetBrightness test_01'),(605,0,'devicesettings','DS_SetBrightness_Maximum value test_24'),(606,0,'devicesettings','DS_SetBrightness_Minimum value test_23'),(607,0,'devicesettings','DS_SetBrightness_STRESS_test_100'),(608,0,'devicesettings','DS_SetBrightness_value in range test_25'),(609,0,'devicesettings','DS_SetBrightness_value out of range test_26'),(610,0,'devicesettings','DS_SetCompression test_11'),(611,0,'devicesettings','DS_SetCompression_HEAVY_FORMAT_66'),(612,0,'devicesettings','DS_SetCompression_INVALID_FORMAT_68'),(613,0,'devicesettings','DS_SetCompression_LIGHT_FORMAT_64'),(614,0,'devicesettings','DS_SetCompression_MEDIUM_FORMAT_65'),(615,0,'devicesettings','DS_SetCompression_NONE_67'),(616,0,'devicesettings','DS_SetCompression_STRESS_test_109'),(617,0,'devicesettings','DS_SetDB test_07'),(618,0,'devicesettings','DS_SetDB_Maximum_test_55'),(619,0,'devicesettings','DS_SetDB_Minimum_test_56'),(620,0,'devicesettings','DS_SetDb_STRESS_test_107'),(621,0,'devicesettings','DS_SetDB_valid_value_test_57'),(622,0,'devicesettings','DS_SetDFC test_15'),(623,0,'devicesettings','DS_SetDFC_CCO_ZOOM_test_77'),(624,0,'devicesettings','DS_SetDFC_FULL_ZOOM_test_75'),(625,0,'devicesettings','DS_SetDFC_INVALID_ZOOM_test_81'),(626,0,'devicesettings','DS_SetDFC_None_ZOOM_test_74'),(627,0,'devicesettings','DS_SetDFC_PanScan_ZOOM_test_78'),(628,0,'devicesettings','DS_SetDFC_Pillarbox4x3_ZOOM_test_80'),(629,0,'devicesettings','DS_SetDFC_PLATFORM_ZOOM_test_76'),(630,0,'devicesettings','DS_SetDFC_STRESS_test_111'),(631,0,'devicesettings','DS_SetDFC_Zoom16x9_test_79'),(632,0,'devicesettings','DS_SetEncoding test_10'),(633,0,'devicesettings','DS_SetEncoding_AC3_FORMAT_test_59'),(634,0,'devicesettings','DS_SetEncoding_DISPLAY_FORMAT_test_61'),(635,0,'devicesettings','DS_SetEncoding_Invalid_FORMAT_test_63'),(636,0,'devicesettings','DS_SetEncoding_NONE_test_62'),(637,0,'devicesettings','DS_SetEncoding_PCM_FORMAT_test_60'),(638,0,'devicesettings','DS_SetEncoding_STRESS_test_108'),(639,0,'devicesettings','DS_SetScroll_Middle_Value_test_50'),(640,0,'devicesettings','DS_SetScroll_Minimum_Value_test_48'),(641,0,'devicesettings','DS_SetScroll_STRESS_test_105'),(642,0,'devicesettings','DS_SetStereoMode_INVALID_FORMAT_73'),(643,0,'devicesettings','DS_SetTextDisplay_test_46'),(644,0,'devicesettings','DS_SetText_STRESS_test_104'),(645,0,'devicesettings','DS_SetTimeFormat_and_Time test_04'),(646,0,'devicesettings','DS_SetTime_12HR_FORMAT_41'),(647,0,'devicesettings','DS_SetTime_24HR_FORMAT_42'),(648,0,'devicesettings','DS_SetTime_FORMAT_STRESS_test_103'),(649,0,'devicesettings','DS_SetTime_INVALID_45'),(650,0,'devicesettings','DS_SetTime_INVALID_FORMAT_44'),(651,0,'devicesettings','DS_SetTime_STRING_FORMAT_43'),(652,0,'tdk_integration','E2E_Rmf_LinearTV_TuneHD-HD_06'),(653,0,'tdk_integration','E2E_Rmf_LinearTV_TuneHD-SD_05'),(654,0,'tdk_integration','Testing_player_tsb'),(655,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_01'),(656,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_02'),(657,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_03'),(658,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_04'),(659,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_05'),(660,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_06'),(661,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_07'),(662,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_08'),(663,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_09'),(664,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_10'),(665,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_13'),(666,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_14'),(667,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_15'),(668,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_16'),(669,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_17'),(670,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_18'),(671,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_19'),(672,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_20'),(673,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_21'),(674,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_22'),(675,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_25'),(676,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_26'),(677,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_27'),(678,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_28'),(679,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_29'),(680,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_30'),(681,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_31'),(682,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_32'),(683,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_33'),(684,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_34'),(685,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_35'),(686,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_36'),(687,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_37'),(688,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_38'),(689,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_39'),(690,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_40'),(691,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_41'),(692,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_43'),(693,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_44'),(694,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_45'),(695,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_46'),(696,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_48'),(697,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_49'),(698,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_50'),(699,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_51'),(700,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_52'),(701,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_54'),(702,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_55'),(703,0,'tdk_integration','E2E_Rmf_LinearTV_H.264_AAC_26'),(704,0,'tdk_integration','E2E_Rmf_LinearTV_H.264_AC3_25'),(705,0,'tdk_integration','E2E_Rmf_LinearTV_H.264_MP3_27'),(706,0,'tdk_integration','E2E_Rmf_LinearTV_H.264_WAV_28'),(707,0,'tdk_integration','E2E_Rmf_LinearTV_MPEG2_AAC_19'),(708,0,'tdk_integration','E2E_Rmf_LinearTV_MPEG2_AC3_17'),(709,0,'tdk_integration','E2E_Rmf_LinearTV_MPEG2_MP3_21'),(710,0,'tdk_integration','E2E_Rmf_LinearTV_MPEG2_WAV_23'),(711,0,'tdk_integration','E2E_Rmf_LinearTV_MPEG4_AAC_20'),(712,0,'tdk_integration','E2E_Rmf_LinearTV_MPEG4_AC3_18'),(713,0,'tdk_integration','E2E_Rmf_LinearTV_MPEG4_MP3_22'),(714,0,'tdk_integration','E2E_Rmf_LinearTV_MPEG4_WAV_24'),(715,0,'tdk_integration','E2E_RMF_LinearTV_TuneHD_02'),(716,0,'tdk_integration','E2E_Rmf_LinearTV_TuneSD-HD_04'),(717,0,'tdk_integration','E2E_Rmf_LinearTV_TuneSD-SD_03'),(718,0,'tdk_integration','E2E_Rmf_LinearTV_TuneSD_01'),(719,0,'tdk_integration','E2E_RMF_RF_Video_01'),(720,0,'tdk_integration','E2E_RMF_RF_Video_02'),(721,0,'tdk_integration','E2E_RMF_RF_Video_03'),(722,0,'tdk_integration','E2E_RMF_RF_Video_04'),(723,0,'tdk_integration','E2E_RMF_RF_Video_05'),(724,0,'tdk_integration','E2E_RMF_RF_Video_06'),(725,0,'tdk_integration','E2E_RMF_RF_Video_07'),(726,0,'tdk_integration','E2E_RMF_RF_Video_08'),(727,0,'tdk_integration','E2E_RMF_RF_Video_09'),(728,0,'tdk_integration','E2E_RMF_RF_Video_12'),(729,0,'tdk_integration','E2E_RMF_RF_Video_13'),(730,0,'tdk_integration','E2E_RMF_RF_Video_14'),(731,0,'tdk_integration','E2E_RMF_RF_Video_15'),(732,0,'tdk_integration','E2E_RMF_RF_Video_16'),(733,0,'tdk_integration','E2E_RMF_RF_Video_17'),(734,0,'tdk_integration','E2E_RMF_RF_Video_18'),(735,0,'tdk_integration','E2E_RMF_TSB_FFW_30x_07'),(736,0,'tdk_integration','E2E_RMF_TSB_FFW_60x_09'),(737,0,'tdk_integration','E2E_RMF_TSB_FFW_FFW_15x_15x_41'),(738,0,'tdk_integration','E2E_RMF_TSB_FFW_FFW_15x_4x_29'),(739,0,'tdk_integration','E2E_RMF_TSB_FFW_FFW_30x_15_42'),(740,0,'tdk_integration','E2E_RMF_TSB_FFW_FFW_30x_4x_31'),(741,0,'tdk_integration','E2E_RMF_TSB_FFW_FFW_60x_15x_44'),(742,0,'tdk_integration','E2E_RMF_TSB_FFW_FFW_60x_30x_51'),(743,0,'tdk_integration','E2E_RMF_TSB_FFW_FFW_60x_4x_33'),(744,0,'tdk_integration','E2E_RMF_TSB_FFW_FRW_15x_4x_35'),(745,0,'tdk_integration','E2E_RMF_TSB_FFW_FRW_30x_15x_46'),(746,0,'tdk_integration','E2E_RMF_TSB_FFW_FRW_30x_4x_37'),(747,0,'tdk_integration','E2E_RMF_TSB_FFW_FRW_60x_15x_48'),(748,0,'tdk_integration','E2E_RMF_TSB_FFW_FRW_60x_30x_53'),(749,0,'tdk_integration','E2E_RMF_TSB_FFW_FRW_60x_4x_39'),(750,0,'tdk_integration','E2E_RMF_TSB_FFW_SFW_15x_0.5x_14'),(751,0,'tdk_integration','E2E_RMF_TSB_FFW_SFW_30x_0.5x_16'),(752,0,'tdk_integration','E2E_RMF_TSB_FFW_SFW_4x_0.5x_12'),(753,0,'tdk_integration','E2E_RMF_TSB_FFW_SFW_60x_0.5x_18'),(754,0,'tdk_integration','E2E_RMF_TSB_FFW_SRW_15x_0.5x_22'),(755,0,'tdk_integration','E2E_RMF_TSB_FFW_SRW_30x_0.5x_24'),(756,0,'tdk_integration','E2E_RMF_TSB_FFW_SRW_4x_0.5x_20'),(757,0,'tdk_integration','E2E_RMF_TSB_FFW_SRW_60x_0.5x_26'),(758,0,'tdk_integration','E2E_RMF_TSB_FRW_15x_06'),(759,0,'tdk_integration','E2E_RMF_TSB_FRW_30x_08'),(760,0,'tdk_integration','E2E_RMF_TSB_FRW_60x_10'),(761,0,'tdk_integration','E2E_RMF_TSB_FRW_FFW_15x_4x_30'),(762,0,'tdk_integration','E2E_RMF_TSB_FRW_FFW_30x_15x_43'),(763,0,'tdk_integration','E2E_RMF_TSB_FRW_FFW_30x_4x_32'),(764,0,'tdk_integration','E2E_RMF_TSB_FRW_FFW_4x_4x_28'),(765,0,'tdk_integration','E2E_RMF_TSB_FRW_FFW_60x_15x_45'),(766,0,'tdk_integration','E2E_RMF_TSB_FRW_FFW_60x_30x_52'),(767,0,'tdk_integration','E2E_RMF_TSB_FRW_FFW_60x_4x_34'),(768,0,'tdk_integration','E2E_RMF_TSB_FRW_FFW_60x_55'),(769,0,'tdk_integration','E2E_RMF_TSB_FRW_FRW_ 60x_30x_54'),(770,0,'tdk_integration','E2E_RMF_TSB_FRW_FRW_15x_4x_36'),(771,0,'tdk_integration','E2E_RMF_TSB_FRW_FRW_30x_15x_47'),(772,0,'tdk_integration','E2E_RMF_TSB_FRW_FRW_30x_4x_38'),(773,0,'tdk_integration','E2E_RMF_TSB_FRW_FRW_60x_15x_49'),(774,0,'tdk_integration','E2E_RMF_TSB_FRW_FRW_60x_4x_40'),(775,0,'tdk_integration','E2E_RMF_TSB_FRW_SFW_15x_0.5x_15'),(776,0,'tdk_integration','E2E_RMF_TSB_FRW_SFW_30x_0.5x_17'),(777,0,'tdk_integration','E2E_RMF_TSB_FRW_SFW_4x_0.5x_13'),(778,0,'tdk_integration','E2E_RMF_TSB_FRW_SFW_60x_0.5x_19'),(779,0,'tdk_integration','E2E_RMF_TSB_FRW_SRW_15x_0.5x_23'),(780,0,'tdk_integration','E2E_RMF_TSB_FRW_SRW_30x_0.5x_25'),(781,0,'tdk_integration','E2E_RMF_TSB_FRW_SRW_4x_0.5x_21'),(782,0,'tdk_integration','E2E_RMF_TSB_FRW_SRW_60x_0.5x_27'),(783,0,'tdk_integration','E2E_RMF_TSB_FW_0.5x_01'),(784,0,'tdk_integration','E2E_RMF_TSB_FW_15x_05'),(785,0,'tdk_integration','E2E_RMF_TSB_FW_4x_03'),(786,0,'tdk_integration','E2E_RMF_TSB_FW_RW_0.5x_11'),(787,0,'tdk_integration','E2E_RMF_TSB_RFW_FFW_30x_30x_50'),(788,0,'tdk_integration','E2E_RMF_TSB_RW_0.5x_02'),(789,0,'tdk_integration','E2E_RMF_TSB_RW_4x_04'),(790,0,'tdk_integration','E2E_RMF_MDVR_DvrPlay_DiffUrl'),(791,0,'tdk_integration','E2E_RMF_MDVR_LivePlay_DvrPlay'),(792,0,'tdk_integration','E2E_RMF_MDVR_LivePlayPause'),(793,0,'tdk_integration','E2E_RMF_MDVR_TrickPlay_SameRecord'),(794,0,'tdk_integration','E2E_RMF_MDVR_PausePlay_SameRecord'),(795,0,'tdk_integration','E2E_RMF_MDVR_Delete_SameRecord'),(796,0,'tdk_integration','E2E_RMF_MDVR_Delete_PausePlay_SameRecord'),(797,0,'tdk_integration','E2E_RMF_MDVR_Delete_TrickPlay_SameRecord'),(798,0,'tdk_integration','E2E_RMF_MDVR_Gateway_Client_SameRecord'),(799,0,'tdk_integration','E2E_RMF_MDVR_TrickPlay_Gateway_Client_SameRecord'),(800,0,'tdk_integration','E2E_RMF_MDVR_Gateway_Client_PausePlay_SameRecord'),(801,0,'tdk_integration','E2E_RMF_LinearTV_DSSetMute_PowerMode_LivePlayback'),(802,0,'tdk_integration','E2E_RMF_LinearTV_ClosedCaption_LivePlayback'),(803,0,'tdk_integration','E2E_RMF_LinearTV_DSSetPowerMode_LivePlayback'),(804,0,'tdk_integration','E2E_RMF_LinearTV_DSSetResolution_LivePlayback'),(805,0,'tdk_integration','E2E_RMF_LinearTV_DSSetResolution_Reboot_LivePlayback'),(806,0,'tdk_integration','E2E_RMF_LinearTV_Tune_SameChannel'),(807,0,'tdk_integration','E2E_RMF_LinearTV_Tune_InvalidChannel'),(808,0,'rmfapp','E2E_rmfapp_help_and_quit'),(809,0,'rmfapp','E2e_rmfApp_ls_quit'),(810,0,'rmfapp','E2E_rmfApp_play_and_quit'),(811,0,'rmfapp','tdkRmfApp_CreateRecord'),(812,0,'tdk_integration','E2E_RMF_HDtoRadioChannel'),(813,0,'tdk_integration','E2E_RMF_RadioChanneltoHD'),(814,0,'tdk_integration','DVR_sampletest'),(815,0,'tdk_integration','E2E_RMF_RadioChannel_Recording'),(816,0,'tdk_integration','E2E_RMF_DVR_playback_radiochannel'),(817,0,'tdk_integration','E2E_RMF_DVR_playback_reccont_lessthanoneminute'),(818,0,'tdk_integration','E2E_RMF_H264_Recording'),(819,0,'tdk_integration','E2E_RMF_DVR_playback_H264'),(820,0,'tdk_integration','E2E_RMF_DVR_playback_recordcont_liveplayback_AudioChannel'),(821,0,'tdk_integration','E2E_RMF_DVR_playback_ongoingrecord_liverecord'),(822,0,'tdk_integration','E2E_RMF_DVR_trickplay_currentrecord_liveplayback'),(823,0,'tdk_integration','E2E_RMF_MDVR_DVR_SkipForward_backward_Multiple'),(824,0,'tdk_integration','E2E_RMF_Recording_standbymode'),(825,0,'tdk_integration','E2E_RMF_standbymode_beforeRecording'),(826,0,'tdk_integration','E2E_RMF_TSB_Recording'),(827,0,'tdk_integration','E2E_RMF_backtoback_record_samechannel'),(828,0,'tdk_integration','E2E_RMF_recording_alreadyRecordservice'),(829,0,'tdk_integration','E2E_RMF_MDVR_DVR_FastForward_Rewind'),(830,0,'tdk_integration','E2E_RMF_simultaneous_recording'),(831,0,'tdk_integration','E2E_RMF_Multiple_future_recording'),(832,0,'tdk_integration','E2E_RMF_DVR_simultaneous_recording_dvrplayback'),(833,0,'tdk_integration','E2E_RMF_simultaneous_recording_liveplayback'),(834,0,'tdk_integration','E2E_RMF_DVR_trickplay_recordcont_liveplayback_radiochannel'),(835,0,'tdk_integration','E2E_RMF_MDVR_TrickPlay_RadioChannel'),(836,0,'tdk_integration','E2E_RMF_DVR_book_record_playback'),(837,0,'tdk_integration','E2E_RMF_switching_live_TSB'),(838,0,'rmfapp','E2E_rmfapp_record_and_quit'),(839,0,'tdk_integration','TDK_E2E_DVR_Playback_Trickplay_All_Recordings_LongDuration_8hr_test'),(840,0,'tdk_integration','TDK_E2E_LinearTv_SwitchingChannel_DVRTrickplay_LongDuration_8hr_test'),(841,0,'tdk_integration','TDK_E2E_LinearTv_SwitchingChannel_DVRForwardAndRewind_LongDuration_8hr_test'),(842,0,'tdk_integration','TDK_E2E_LinearTv_LinearTrickplay_LongDuration_8hr_Test'),(843,0,'tdk_integration','TDK_E2E_RMF_LinearTV_ChannelChange_Trickplay_LongDuration_8hr_test'),(844,0,'tdk_integration','E2E_RMF_LinearTV_Stress_HD_LivePlayback_Longduration'),(845,0,'tdk_integration','E2E_RMF_LinearTV_Stress_LiveDvrPlay_LongDuration'),(846,0,'tdk_integration','E2E_RMF_LinearTV_Stress_LivePlayback_Longduration'),(847,0,'tdk_integration','E2E_RMF_LinearTV_Stress_LivePlay_SwitchingChannel_LongDuration'),(848,0,'tdk_integration','TDK_E2E_LinearTV_Channelchange_LongDuration_8hr_test'),(849,0,'tdk_integration','TDK_RMF_ScheduleRecording_Playback_LongDuration_8hr_test'),(850,0,'tdk_integration','E2E_RMF_MDVR_DvrPlay_SameUrl'),(851,0,'tdk_integration','E2E_RMF_MDVR_LivePlay_DiffUrl'),(852,0,'tdk_integration','E2E_RMF_MDVR_LivePlay_SameUrl'),(853,0,'tdk_integration','E2E_RMF_MDVR_Max_LivePlay'),(854,0,'tdk_integration','E2E_RMF_MDVR_Max_ScheduleRecording'),(855,0,'tdk_integration','E2E_RMF_MDVR_Max_ScheduleRecording_Neg'),(856,0,'tdk_integration','E2E_RMF_MDVR_SchedLiveRec1_Play2'),(857,0,'tdk_integration','E2E_RMF_MDVR_SchedRec1_Play2'),(858,0,'tdk_integration','E2E_RMF_MDVR_SchedRec_SameChannelSimul'),(859,0,'mediaframework','RMF_DVRManager_GetRecordingDuration'),(860,0,'mediaframework','RMF_MPSink_SetGetMute_03'),(861,0,'mediaframework','RMF_DVRSrcMPSink_SkipNumOfSeconds_SkipFront_07'),(862,0,'mediaframework','RMF_QAMSrc_HNSink_02'),(863,0,'mediaframework','RMF_DVRManager_GetSegmentsCount'),(864,0,'mediaframework','RMF_DVRManager_UpdateRecording'),(865,0,'mediaframework','RMF_DVRSrc_GetSetSpeed_06'),(866,0,'mediaframework','RMF_HNSrc_Play_withoutopen_12'),(867,0,'mediaframework','RMF_QAMSrc_HNSink_14'),(868,0,'mediaframework','RMF_QAMSrc_HNSink_10'),(869,0,'mediaframework','RMF_DVRManager_GetRecordingInfoById'),(870,0,'mediaframework','RMF_HNSink_01'),(871,0,'mediaframework','RMF_DVRSrc_Open_14'),(872,0,'mediaframework','RMF_HNSrc_Open_vodurl_08'),(873,0,'mediaframework','RMF_DVRManager_GetRecordingInfoByIndex'),(874,0,'mediaframework','RMF_DVRManager_GetRecordingInfoById_17'),(875,0,'mediaframework','RMF_DVRSrc_Open_11'),(876,0,'mediaframework','RMF_DVRManager_GetRecordingSize'),(877,0,'mediaframework','RMF_DVRSrcMPSink_ChangeSpeed_12'),(878,0,'mediaframework','RMF_DVRSrc_SetMediaTime_08'),(879,0,'mediaframework','RMF_MPSink_GetMediaTime_05'),(880,0,'mediaframework','RMF_DVRSrc_Play_03'),(881,0,'mediaframework','RMF_DVRManager_GetRecordingCount'),(882,0,'mediaframework','RMF_MPSink_InitTerm_01'),(883,0,'mediaframework','RMF_DVRSrc_Open_16'),(884,0,'mediaframework','RMF_DVRSrc_Open_10'),(885,0,'mediaframework','RMF_QAMSrc_HNSink_01'),(886,0,'mediaframework','RMF_QAMSrc_HNSink_13'),(887,0,'mediaframework','RMF_QAMSrc_HNSink_06'),(888,0,'mediaframework','RMF_DVRSrc_Open_15'),(889,0,'mediaframework','RMF_DVRManager_GetDefaultTSBMaxDuration'),(890,0,'mediaframework','RMF_DVRManager_GetIsRecordingInProgress'),(891,0,'mediaframework','RMF_DVRManager_CreateRecording'),(892,0,'mediaframework','RMF_HNSrc_Open_invalidurl_07'),(893,0,'mediaframework','RMF_MPSink_SetGetVolume_04'),(894,0,'mediaframework','RMF_HNSrc_SetGetSpeed_02'),(895,0,'mediaframework','RMF_DVRSink_InitTerm_01'),(896,0,'mediaframework','RMF_QAMSrc_HNSink_08'),(897,0,'mediaframework','RMF_DVRSrc_InitTerm_01'),(898,0,'mediaframework','RMF_HNSRC_Play_withoutsetsource_10'),(899,0,'mediaframework','RMF_DVRManager_CreateTSB'),(900,0,'mediaframework','RMF_QAMSrc_HNSink_07'),(901,0,'mediaframework','RMF_DVRSrc_GetMediaInfo_09'),(902,0,'mediaframework','RMF_QAMSrc_HNSink_04'),(903,0,'mediaframework','RMF_DVRSrcMPSink_BackToBeg_04'),(904,0,'mediaframework','RMF_HNSrc_MPSink_Clearbuffering&CheckMediaTime_18'),(905,0,'mediaframework','RMF_DVRSrc_Open_12'),(906,0,'mediaframework','RMF_QAMSrc_HNSink_09'),(907,0,'mediaframework','RMF_QAMSrc_HNSink_05'),(908,0,'mediaframework','RMF_DVR_Get_Recording_List'),(909,0,'mediaframework','RMF_DVRSrcMPSink_SkipNumOfSeconds_SkipBack_06'),(910,0,'mediaframework','RMF_QAMSrc_HNSink_12'),(911,0,'mediaframework','RMF_DVRManager_GetRecordingInfoByIndex_16'),(912,0,'mediaframework','RMF_QAMSrc_HNSink_03'),(913,0,'mediaframework','RMF_DVRSrc_Play_04'),(914,0,'mediaframework','RMF_DVRSrc_Open_13'),(915,0,'mediaframework','RMF_HNSrc_Open_validUrl_11'),(916,0,'mediaframework','RMF_DVRSrc_GetMediaTime_07'),(917,0,'mediaframework','RMF_HNSrc_GetState_05'),(918,0,'mediaframework','RMF_QAMSrc_HNSink_11'),(919,0,'mediaframework','RMF_HNSrc_Open_Emptystring_06'),(920,0,'mediaframework','RMF_DVRSrc_OpenClose_02'),(921,0,'mediaframework','RMF_DVRSrcMPSink_Pause_02'),(922,0,'mediaframework','RMF_HNSrc_InitTerm_01'),(923,0,'mediaframework','RMF_MPSink_SetVideoRectangle_02'),(924,0,'mediaframework','RMF_DVRManager_ConvertTSBToRecording'),(925,0,'mediaframework','RMF_DVRManager_GetSpace'),(926,0,'mediaframework','RMF_DVRSrcMPSink_SkipToEnd_05'),(927,0,'mediaframework','RMF_DVRSrc_GetSpeed_05'),(928,0,'mediaframework','RMF_HNSrc_Play_DefaultSpeed_09'),(929,0,'mediaframework','RMF_DVRManager_GetRecordingStartTime'),(930,0,'mediastreamer','MS_LiveTune_Improper_Requesturl_02'),(931,0,'mediastreamer','MS_LiveTune_Playback_07'),(932,0,'mediastreamer','MS_DVRTrickplay_Invalid_Timeposition_11'),(933,0,'mediastreamer','MS_Recording_Metadata_Format_Test_06'),(934,0,'mediastreamer','MS_Recordedcontent_playback_08'),(935,0,'mediastreamer','MS_Recording_Request_03'),(936,0,'mediastreamer','MS_DVRTrickplay_Functionality_Test_09'),(937,0,'mediastreamer','RMF_MS_Stress_LiveTune_Test'),(938,0,'mediastreamer','MS_DVRTrickplay_Invalid_Playspeed_10'),(939,0,'mediastreamer','MS_RecordingList_Format_Test_05'),(940,0,'mediastreamer','MS_LiveTune_Valid_Request_01'),(941,0,'mediastreamer','MS_Recording_Improper_Requesturl_04'),(942,0,'newrmf','test_newrmf_play'),(943,0,'openSource_components','Qt5_Test'),(944,0,'openSource_components','yajl_Test'),(945,0,'openSource_components','GstreamerBasePluginTest'),(946,0,'openSource_components','Glib_Test'),(947,0,'openSource_components','WebkitTest_Intelce'),(948,0,'openSource_components','libsoup_Test'),(949,0,'openSource_components','Openssl_Test'),(950,0,'openSource_components','Qt5Webkit_Test'),(951,0,'openSource_components','QtTest_Intelce'),(952,0,'openSource_components','GstreamerTest'),(953,0,'openSource_components','Jansson_Test'),(954,0,'openSource_components','WebkitTest_DirectFB'),(955,0,'openSource_components','GstreamerGoodPluginTest'),(956,0,'openSource_components','QtTest_DirectFB'),(957,0,'tdk_integration','E2E_DVRTrickPlay_Fwd_0.5x_03'),(958,0,'tdk_integration','E2E_DVRTrickPlay_Fwd_15x_07'),(959,0,'tdk_integration','E2E_DVRTrickPlay_Fwd_30x_09'),(960,0,'tdk_integration','E2E_DVRTrickPlay_Fwd_4x_05'),(961,0,'tdk_integration','E2E_DVRTrickPlay_Fwd_60x_11'),(962,0,'tdk_integration','E2E_DVRTrickPlay_Invalid_PlaySpeed_12'),(963,0,'tdk_integration','E2E_DVRTrickPlay_Rwd_0.5x_02'),(964,0,'tdk_integration','E2E_DVRTrickPlay_Rwd_15x_06'),(965,0,'tdk_integration','E2E_DVRTrickPlay_Rwd_30x_08'),(966,0,'tdk_integration','E2E_DVRTrickPlay_Rwd_4x_04'),(967,0,'tdk_integration','E2E_DVRTrickPlay_Rwd_60x_10'),(968,0,'tdk_integration','E2E_DVR_Invalid_TimePosition_13'),(969,0,'tdk_integration','E2E_DVR_PlayBack_01'),(970,0,'tdk_integration','E2E_DVR_Skip_Fwd_15'),(971,0,'tdk_integration','E2E_DVR_Skip_Rwd_14'),(972,0,'tdk_integration','E2E_LinearTV_H.264_AAC_26'),(973,0,'tdk_integration','E2E_LinearTV_H.264_AC3_25'),(974,0,'tdk_integration','E2E_LinearTV_H.264_MP3_27'),(975,0,'tdk_integration','E2E_LinearTV_H.264_WAV_28'),(976,0,'tdk_integration','E2E_LinearTV_MPEG2_AAC_19'),(977,0,'tdk_integration','E2E_LinearTV_MPEG2_MP3_21'),(978,0,'tdk_integration','E2E_LinearTV_MPEG2_WAV_23'),(979,0,'tdk_integration','E2E_LinearTV_MPEG4_AAC_20'),(980,0,'tdk_integration','E2E_LinearTV_MPEG4_AC3_18'),(981,0,'tdk_integration','E2E_LinearTV_MPEG4_MP3_22'),(982,0,'tdk_integration','E2E_LinearTV_MPEG4_WAV_24'),(983,0,'tdk_integration','E2E_LinearTV_MPEG_AC3_17'),(984,0,'tdk_integration','E2E_LinearTV_TuneHD-HD_06'),(985,0,'tdk_integration','E2E_LinearTV_TuneHD-SD_05'),(986,0,'tdk_integration','E2E_LinearTV_TuneHD_02'),(987,0,'tdk_integration','E2E_LinearTV_TuneSD-HD_04'),(988,0,'tdk_integration','E2E_LinearTV_TuneSD-SD_03'),(989,0,'tdk_integration','E2E_LinearTV_TuneSD_01'),(990,0,'tdk_integration','E2E_LinearTV_Live_Trickplay_FFW_15x_11'),(991,0,'tdk_integration','E2E_LinearTV_Live_Trickplay_FFW_30x_12'),(992,0,'tdk_integration','E2E_LinearTV_Live_Trickplay_FFW_4x_10'),(993,0,'tdk_integration','E2E_LinearTV_Live_Trickplay_FFW_60x_13'),(994,0,'tdk_integration','E2E_LinearTV_Live_Trickplay_FRW_15x_14'),(995,0,'tdk_integration','E2E_LinearTV_Live_Trickplay_FRW_30x_15'),(996,0,'tdk_integration','E2E_LinearTV_Live_Trickplay_FRW_4x_09'),(997,0,'tdk_integration','E2E_LinearTV_Live_Trickplay_FRW_60x_16'),(998,0,'tdk_integration','E2E_LinearTV_Live_Trickplay_SFW_0.5x_08'),(999,0,'tdk_integration','E2E_LinearTV_Live_Trickplay_SRW_0.5x_07'),(1000,0,'rdk_logger','RDKLogger_EnvGetModFromNum'),(1001,0,'rdk_logger','RDKLogger_EnvGetNum'),(1002,0,'rdk_logger','RDKLogger_Init'),(1003,0,'rdk_logger','RDKLogger_Log'),(1004,0,'recorder','RMFMS_ScheduleRecording_12'),(1005,0,'recorder','RMFMS_ScheduleRecording_InvalidSRC_13'),(1006,0,'recorder','RMFMS_Schedule_Big_Recording_14'),(1007,0,'recorder','RMFMS_Schedule_FutureRecording_15'),(1008,0,'recorder','RMFMS_Schedule_MinDuration_Recording_18'),(1009,0,'recorder','RMFMS_Schedule_NegDuration_Recording_19'),(1010,0,'recorder','RMFMS_Schedule_NegStartTime_Recording_20'),(1011,0,'recorder','RMFMS_Schedule_SmallDuration_Recording_17'),(1012,0,'recorder','RMFMS_Schedule_ZeroSize_Recording_16'),(1013,0,'gst-plugins-rdk','GstPluginRdk_Dvrsrc_Duration_Get_Prop_Default'),(1014,0,'gst-plugins-rdk','GstPluginRdk_Aesdecrypt_DecryptEnable_Get_Default'),(1015,0,'gst-plugins-rdk','GstPluginRdk_Dvrsink_RecordId_Set_Prop');
/*!40000 ALTER TABLE `script_file` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `script_group`
--

DROP TABLE IF EXISTS `script_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `script_group` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `version` bigint(20) NOT NULL,
  `name` varchar(255) NOT NULL,
  `status` varchar(255) DEFAULT NULL,
  `groups_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `FKB4D8260B984B586A` (`groups_id`),
  CONSTRAINT `FKB4D8260B984B586A` FOREIGN KEY (`groups_id`) REFERENCES `groups` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=342 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `script_group`
--

LOCK TABLES `script_group` WRITE;
/*!40000 ALTER TABLE `script_group` DISABLE KEYS */;
INSERT INTO `script_group` VALUES (218,160,'closedcaption','FREE',NULL),(220,519,'tdk_integration','FREE',NULL),(221,10,'rmfapp','FREE',NULL),(222,28,'openSource_components','FREE',NULL),(223,245,'iarmbus','FREE',NULL),(224,42,'mediastreamer','FREE',NULL),(225,90,'rdk_logger','FREE',NULL),(226,18,'recorder','FREE',NULL),(227,332,'mediaframework','FREE',NULL),(228,80,'servicemanager','FREE',NULL),(229,2,'newrmf','FREE',NULL),(236,2413,'ComponentSuite','FREE',NULL),(237,3164,'IPClient-3Suite','FREE',NULL),(238,2991,'Hybrid-1Suite','FREE',NULL),(244,180,'tr69','FREE',NULL),(263,647,'E2ESuite','FREE',NULL),(273,57,'gst-plugins-rdk','FREE',NULL),(275,121,'trm','FREE',NULL),(293,20,'MDVR','FREE',NULL),(295,2047,'RDK2.0_IPClient-3','FREE',NULL),(296,1403,'RDK1.3_Hybrid-1','FREE',NULL),(297,203,'RDK1.2_Hybrid-1','FREE',NULL),(298,3337,'RDK2.0_Hybrid-1','FREE',NULL),(299,1033,'RDK1.3_IPClient-3','FREE',NULL),(300,229,'RDK1.2_IPClient-3','FREE',NULL),(311,6,'DVRTest','FREE',NULL),(321,243,'devicesettings','FREE',NULL),(322,21,'tdk_integration_LD','FREE',NULL),(323,21,'E2ESuite_LD','FREE',NULL),(324,15,'IPClient-3Suite_LD','FREE',NULL),(325,27,'Hybrid-1Suite_LD','FREE',NULL),(326,77,'RDK2.0_IPClient-3_LD','FREE',NULL),(327,157,'RDK2.0_Hybrid-1_LD','FREE',NULL),(328,5,'mediaframework_LD','FREE',NULL),(329,5,'ComponentSuite_LD','FREE',NULL),(330,21,'dtcp','FREE',NULL),(331,27,'xupnp','FREE',NULL),(339,2,'RDK1.3_Hybrid-5','FREE',NULL),(340,2,'RDK2.0_Hybrid-5','FREE',NULL),(341,2,'Hybrid-5Suite','FREE',NULL);
/*!40000 ALTER TABLE `script_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `script_group_script`
--

DROP TABLE IF EXISTS `script_group_script`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `script_group_script` (
  `script_group_scripts_id` bigint(20) DEFAULT NULL,
  `script_id` bigint(20) DEFAULT NULL,
  `script_group_scripts_list_id` bigint(20) DEFAULT NULL,
  `scripts_list_idx` int(11) DEFAULT NULL,
  KEY `FKF6D3D57FE2F1DCCF` (`script_id`),
  KEY `FKF6D3D57F6492105` (`script_group_scripts_id`),
  CONSTRAINT `FKF6D3D57F6492105` FOREIGN KEY (`script_group_scripts_id`) REFERENCES `script_group` (`id`),
  CONSTRAINT `FKF6D3D57FE2F1DCCF` FOREIGN KEY (`script_id`) REFERENCES `script` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;



--
-- Table structure for table `script_group_script_file`
--

DROP TABLE IF EXISTS `script_group_script_file`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `script_group_script_file` (
  `script_group_script_list_id` bigint(20) DEFAULT NULL,
  `script_file_id` bigint(20) DEFAULT NULL,
  `script_list_idx` int(11) DEFAULT NULL,
  KEY `FKAB6B703CF95C2361` (`script_file_id`),
  CONSTRAINT `FKAB6B703CF95C2361` FOREIGN KEY (`script_file_id`) REFERENCES `script_file` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `script_group_script_file`
--

LOCK TABLES `script_group_script_file` WRITE;
/*!40000 ALTER TABLE `script_group_script_file` DISABLE KEYS */;
INSERT INTO `script_group_script_file` VALUES (218,1,0),(218,2,1),(218,3,2),(218,4,3),(218,5,4),(218,6,5),(218,7,6),(218,8,7),(218,9,8),(218,10,9),(218,11,10),(218,12,11),(218,13,12),(218,14,13),(218,15,14),(218,16,15),(218,17,16),(218,18,17),(218,19,18),(218,20,19),(218,21,20),(218,22,21),(218,23,22),(218,24,23),(218,25,24),(218,26,25),(218,27,26),(218,28,27),(218,29,28),(218,30,29),(218,31,30),(218,32,31),(218,33,32),(218,34,33),(218,35,34),(218,36,35),(218,37,36),(218,38,37),(218,39,38),(218,40,39),(218,41,40),(218,42,41),(218,43,42),(218,44,43),(218,45,44),(218,46,45),(218,47,46),(218,48,47),(218,49,48),(218,50,49),(218,51,50),(218,52,51),(218,53,52),(218,54,53),(218,55,54),(218,56,55),(218,57,56),(218,58,57),(218,59,58),(218,60,59),(218,61,60),(218,62,61),(218,63,62),(218,64,63),(218,65,64),(218,66,65),(218,67,66),(218,68,67),(218,69,68),(218,70,69),(218,71,70),(218,72,71),(218,73,72),(218,74,73),(218,75,74),(218,76,75),(218,77,76),(218,78,77),(236,79,0),(236,80,1),(236,81,2),(236,82,3),(236,83,4),(236,84,5),(236,85,6),(236,86,7),(236,87,8),(236,88,9),(236,89,10),(236,90,11),(236,91,12),(236,92,13),(236,93,14),(236,94,15),(236,95,16),(236,96,17),(236,97,18),(236,98,19),(236,99,20),(236,100,21),(236,101,22),(236,36,23),(236,102,24),(236,103,25),(236,44,26),(236,104,27),(236,105,28),(236,106,29),(236,107,30),(236,108,31),(236,109,32),(236,110,33),(236,111,34),(236,112,35),(236,113,36),(236,114,37),(236,115,38),(236,116,39),(236,117,40),(236,118,41),(236,119,42),(236,120,43),(236,121,44),(236,122,45),(236,123,46),(236,124,47),(236,125,48),(236,126,49),(236,127,50),(236,128,51),(236,129,52),(236,130,53),(236,131,54),(236,132,55),(236,133,56),(236,134,57),(236,135,58),(236,136,59),(236,137,60),(236,138,61),(236,139,62),(236,22,63),(236,140,64),(236,141,65),(236,142,66),(236,143,67),(236,144,68),(236,145,69),(236,146,70),(236,147,71),(236,148,72),(236,149,73),(236,150,74),(236,151,75),(236,152,76),(236,153,77),(236,154,78),(236,155,79),(236,156,80),(236,157,81),(236,158,82),(236,159,83),(236,160,84),(236,161,85),(236,51,86),(236,162,87),(236,163,88),(236,164,89),(236,165,90),(236,166,91),(236,167,92),(236,63,93),(236,168,94),(236,169,95),(236,170,96),(236,171,97),(236,172,98),(236,173,99),(236,174,100),(236,175,101),(236,6,102),(236,176,103),(236,177,104),(236,178,105),(236,8,106),(236,179,107),(236,180,108),(236,181,109),(236,182,110),(236,183,111),(236,184,112),(236,185,113),(236,186,114),(236,187,115),(236,188,116),(236,189,117),(236,190,118),(236,191,119),(236,192,120),(236,193,121),(236,194,122),(236,195,123),(236,196,124),(236,197,125),(236,198,126),(236,199,127),(236,200,128),(236,201,129),(236,202,130),(236,203,131),(236,204,132),(236,205,133),(236,206,134),(236,207,135),(236,208,136),(236,209,137),(236,210,138),(236,211,139),(236,212,140),(236,213,141),(236,214,142),(236,215,143),(236,216,144),(236,217,145),(236,218,146),(236,219,147),(236,220,148),(236,221,149),(236,222,150),(236,223,151),(236,224,152),(236,225,153),(236,226,154),(236,227,155),(236,228,156),(236,229,157),(236,230,158),(236,231,159),(236,232,160),(236,233,161),(236,234,162),(236,235,163),(236,236,164),(236,34,165),(236,237,166),(236,238,167),(236,239,168),(236,240,169),(236,241,170),(236,242,171),(236,243,172),(236,244,173),(236,245,174),(236,43,175),(236,246,176),(236,247,177),(236,248,178),(236,249,179),(236,55,180),(236,250,181),(236,251,182),(236,252,183),(236,253,184),(236,254,185),(236,255,186),(236,256,187),(236,257,188),(236,258,189),(236,259,190),(236,260,191),(236,261,192),(236,262,193),(236,263,194),(236,264,195),(236,265,196),(236,266,197),(236,267,198),(236,268,199),(236,269,200),(236,270,201),(236,271,202),(236,272,203),(236,273,204),(236,274,205),(236,275,206),(236,276,207),(236,277,208),(236,278,209),(236,279,210),(236,280,211),(236,281,212),(236,282,213),(236,283,214),(236,284,215),(236,285,216),(236,286,217),(236,287,218),(236,288,219),(236,289,220),(236,290,221),(236,291,222),(236,292,223),(236,293,224),(236,294,225),(236,295,226),(236,296,227),(236,297,228),(236,298,229),(236,299,230),(236,300,231),(236,301,232),(236,302,233),(236,303,234),(236,304,235),(236,305,236),(236,306,237),(236,307,238),(236,308,239),(236,309,240),(236,310,241),(236,311,242),(236,312,243),(236,313,244),(236,314,245),(236,315,246),(236,316,247),(236,317,248),(236,318,249),(236,319,250),(236,320,251),(236,321,252),(236,322,253),(236,323,254),(236,324,255),(236,325,256),(236,326,257),(236,327,258),(236,328,259),(236,329,260),(236,330,261),(236,331,262),(236,332,263),(236,333,264),(236,334,265),(236,335,266),(236,336,267),(236,337,268),(236,338,269),(236,339,270),(236,340,271),(236,341,272),(236,342,273),(236,343,274),(236,344,275),(236,345,276),(236,346,277),(236,347,278),(236,348,279),(236,349,280),(236,350,281),(236,351,282),(236,72,283),(236,352,284),(236,353,285),(236,354,286),(236,355,287),(236,356,288),(236,357,289),(236,73,290),(236,358,291),(236,359,292),(236,74,293),(236,360,294),(236,361,295),(236,362,296),(236,363,297),(236,364,298),(236,365,299),(236,366,300),(236,367,301),(236,75,302),(236,368,303),(236,369,304),(236,370,305),(236,371,306),(236,372,307),(236,76,308),(236,373,309),(236,77,310),(236,78,311),(236,374,312),(236,375,313),(236,376,314),(236,377,315),(236,378,316),(236,379,317),(236,380,318),(236,381,319),(236,382,320),(236,383,321),(236,384,322),(236,385,323),(236,386,324),(236,387,325),(236,388,326),(236,389,327),(236,390,328),(236,391,329),(236,392,330),(236,393,331),(236,70,332),(236,394,333),(236,395,334),(236,396,335),(236,397,336),(236,398,337),(236,399,338),(236,400,339),(236,401,340),(236,402,341),(236,403,342),(236,404,343),(236,405,344),(236,406,345),(236,407,346),(236,408,347),(236,409,348),(236,410,349),(236,411,350),(236,412,351),(236,413,352),(236,414,353),(236,415,354),(236,416,355),(236,417,356),(236,418,357),(236,419,358),(236,420,359),(236,421,360),(236,422,361),(236,423,362),(236,424,363),(236,425,364),(236,426,365),(236,427,366),(236,428,367),(236,429,368),(236,430,369),(236,431,370),(236,432,371),(236,433,372),(236,434,373),(236,435,374),(236,436,375),(236,437,376),(236,438,377),(236,439,378),(236,440,379),(236,441,380),(236,442,381),(236,443,382),(236,444,383),(236,445,384),(236,446,385),(236,447,386),(236,448,387),(236,449,388),(236,450,389),(236,451,390),(236,452,391),(236,453,392),(236,454,393),(236,455,394),(236,456,395),(236,457,396),(236,458,397),(236,459,398),(236,460,399),(236,461,400),(236,462,401),(236,463,402),(236,464,403),(236,465,404),(236,466,405),(236,467,406),(236,468,407),(236,469,408),(236,470,409),(236,471,410),(236,472,411),(236,473,412),(236,474,413),(236,475,414),(236,476,415),(236,477,416),(236,478,417),(236,479,418),(236,480,419),(236,481,420),(236,482,421),(236,483,422),(236,484,423),(236,485,424),(236,486,425),(236,487,426),(236,488,427),(236,489,428),(236,490,429),(236,491,430),(236,492,431),(236,493,432),(236,494,433),(236,495,434),(236,496,435),(236,497,436),(236,498,437),(236,499,438),(236,500,439),(236,501,440),(236,502,441),(236,503,442),(236,504,443),(236,505,444),(236,506,445),(236,507,446),(236,508,447),(236,509,448),(236,510,449),(236,511,450),(236,512,451),(236,513,452),(236,514,453),(236,515,454),(236,516,455),(236,517,456),(236,518,457),(236,33,458),(236,519,459),(236,520,460),(236,521,461),(236,522,462),(236,523,463),(236,524,464),(236,525,465),(236,526,466),(236,527,467),(236,528,468),(236,529,469),(236,530,470),(236,531,471),(236,532,472),(236,533,473),(236,534,474),(236,535,475),(236,536,476),(236,537,477),(236,538,478),(236,539,479),(236,540,480),(236,541,481),(236,542,482),(236,543,483),(236,544,484),(236,545,485),(236,546,486),(236,547,487),(236,548,488),(236,549,489),(236,550,490),(236,551,491),(236,552,492),(236,553,493),(236,554,494),(236,555,495),(236,556,496),(236,557,497),(236,558,498),(236,559,499),(236,560,500),(236,561,501),(236,562,502),(236,563,503),(236,564,504),(236,565,505),(236,566,506),(236,567,507),(236,568,508),(236,569,509),(236,570,510),(236,571,511),(236,572,512),(236,573,513),(236,574,514),(236,575,515),(236,576,516),(236,577,517),(236,578,518),(236,579,519),(236,580,520),(236,581,521),(236,582,522),(236,583,523),(236,584,524),(236,585,525),(329,586,0),(329,587,1),(321,588,0),(321,449,1),(321,589,2),(321,590,3),(321,463,4),(321,591,5),(321,454,6),(321,464,7),(321,592,8),(321,593,9),(321,492,10),(321,594,11),(321,443,12),(321,374,13),(321,452,14),(321,311,15),(321,453,16),(321,179,17),(321,191,18),(321,180,19),(321,125,20),(321,84,21),(321,254,22),(321,113,23),(321,226,24),(321,99,25),(321,205,26),(321,133,27),(321,175,28),(321,111,29),(321,451,30),(321,455,31),(321,456,32),(321,120,33),(321,595,34),(321,596,35),(321,597,36),(321,598,37),(321,599,38),(321,310,39),(321,600,40),(321,478,41),(321,601,42),(321,602,43),(321,603,44),(321,577,45),(321,578,46),(321,579,47),(321,580,48),(321,116,49),(321,581,50),(321,604,51),(321,605,52),(321,606,53),(321,607,54),(321,608,55),(321,609,56),(321,570,57),(321,571,58),(321,572,59),(321,573,60),(321,574,61),(321,575,62),(321,576,63),(321,610,64),(321,611,65),(321,612,66),(321,613,67),(321,614,68),(321,615,69),(321,616,70),(321,617,71),(321,154,72),(321,618,73),(321,619,74),(321,620,75),(321,621,76),(321,622,77),(321,623,78),(321,624,79),(321,625,80),(321,626,81),(321,627,82),(321,628,83),(321,629,84),(321,630,85),(321,631,86),(321,632,87),(321,633,88),(321,634,89),(321,635,90),(321,636,91),(321,637,92),(321,638,93),(321,375,94),(321,376,95),(321,377,96),(321,378,97),(321,379,98),(321,438,99),(321,418,100),(321,639,101),(321,640,102),(321,641,103),(321,448,104),(321,167,105),(321,642,106),(321,194,107),(321,119,108),(321,137,109),(321,148,110),(321,150,111),(321,643,112),(321,644,113),(321,645,114),(321,646,115),(321,647,116),(321,648,117),(321,649,118),(321,650,119),(321,651,120),(321,450,121),(330,526,0),(330,550,1),(330,551,2),(330,552,3),(330,553,4),(330,554,5),(330,555,6),(330,556,7),(330,557,8),(330,558,9),(330,559,10),(311,497,0),(311,493,1),(311,494,2),(311,495,3),(311,496,4),(311,346,5),(263,652,0),(263,653,1),(263,654,2),(263,655,3),(263,656,4),(263,657,5),(263,658,6),(263,659,7),(263,660,8),(263,661,9),(263,662,10),(263,663,11),(263,664,12),(263,665,13),(263,666,14),(263,667,15),(263,668,16),(263,669,17),(263,670,18),(263,671,19),(263,672,20),(263,673,21),(263,674,22),(263,675,23),(263,676,24),(263,677,25),(263,678,26),(263,679,27),(263,680,28),(263,681,29),(263,682,30),(263,683,31),(263,684,32),(263,685,33),(263,686,34),(263,687,35),(263,688,36),(263,689,37),(263,690,38),(263,691,39),(263,692,40),(263,693,41),(263,694,42),(263,695,43),(263,696,44),(263,697,45),(263,698,46),(263,699,47),(263,700,48),(263,701,49),(263,702,50),(263,703,51),(263,704,52),(263,705,53),(263,706,54),(263,707,55),(263,708,56),(263,709,57),(263,710,58),(263,711,59),(263,712,60),(263,713,61),(263,714,62),(263,715,63),(263,716,64),(263,717,65),(263,718,66),(263,719,67),(263,720,68),(263,721,69),(263,722,70),(263,723,71),(263,724,72),(263,725,73),(263,726,74),(263,727,75),(263,728,76),(263,729,77),(263,730,78),(263,731,79),(263,732,80),(263,733,81),(263,734,82),(263,735,83),(263,736,84),(263,737,85),(263,738,86),(263,739,87),(263,740,88),(263,741,89),(263,742,90),(263,743,91),(263,744,92),(263,745,93),(263,746,94),(263,747,95),(263,748,96),(263,749,97),(263,750,98),(263,751,99),(263,752,100),(263,753,101),(263,754,102),(263,755,103),(263,756,104),(263,757,105),(263,758,106),(263,759,107),(263,760,108),(263,761,109),(263,762,110),(263,763,111),(263,764,112),(263,765,113),(263,766,114),(263,767,115),(263,768,116),(263,769,117),(263,770,118),(263,771,119),(263,772,120),(263,773,121),(263,774,122),(263,775,123),(263,776,124),(263,777,125),(263,778,126),(263,779,127),(263,780,128),(263,781,129),(263,782,130),(263,783,131),(263,784,132),(263,785,133),(263,786,134),(263,787,135),(263,788,136),(263,789,137),(263,790,138),(263,791,139),(263,792,140),(263,793,141),(263,794,142),(263,795,143),(263,796,144),(263,797,145),(263,798,146),(263,799,147),(263,800,148),(263,801,149),(263,802,150),(263,803,151),(263,804,152),(263,805,153),(263,806,154),(263,807,155),(263,808,156),(263,809,157),(263,810,158),(263,811,159),(263,812,160),(263,813,161),(263,814,162),(263,815,163),(263,816,164),(263,817,165),(263,818,166),(263,819,167),(263,820,168),(263,821,169),(263,822,170),(263,823,171),(263,824,172),(263,825,173),(263,826,174),(263,827,175),(263,828,176),(263,829,177),(263,830,178),(263,831,179),(263,832,180),(263,833,181),(263,834,182),(263,835,183),(263,836,184),(263,837,185),(263,838,186),(323,839,0),(323,840,1),(323,841,2),(323,842,3),(323,843,4),(323,844,5),(323,845,6),(323,846,7),(323,847,8),(323,848,9),(323,849,10),(273,273,0),(273,274,1),(273,275,2),(273,318,3),(273,319,4),(273,320,5),(273,321,6),(273,322,7),(273,323,8),(273,324,9),(273,325,10),(273,326,11),(273,327,12),(273,328,13),(273,329,14),(273,330,15),(273,331,16),(273,332,17),(273,333,18),(273,334,19),(273,335,20),(273,336,21),(273,337,22),(273,338,23),(273,339,24),(273,340,25),(273,341,26),(238,171,0),(238,667,1),(238,172,2),(238,79,3),(238,173,4),(238,174,5),(238,175,6),(238,698,7),(238,668,8),(238,80,9),(238,658,10),(238,6,11),(238,178,12),(238,8,13),(238,84,14),(238,702,15),(238,665,16),(238,86,17),(238,680,18),(238,88,19),(238,676,20),(238,89,21),(238,685,22),(238,183,23),(238,185,24),(238,659,25),(238,186,26),(238,91,27),(238,188,28),(238,187,29),(238,669,30),(238,694,31),(238,699,32),(238,690,33),(238,670,34),(238,95,35),(238,97,36),(238,98,37),(238,100,38),(238,101,39),(238,36,40),(238,688,41),(238,192,42),(238,193,43),(238,194,44),(238,103,45),(238,195,46),(238,675,47),(238,196,48),(238,197,49),(238,44,50),(238,105,51),(238,686,52),(238,107,53),(238,108,54),(238,109,55),(238,198,56),(238,200,57),(238,202,58),(238,691,59),(238,110,60),(238,203,61),(238,111,62),(238,112,63),(238,661,64),(238,692,65),(238,113,66),(238,204,67),(238,206,68),(238,114,69),(238,656,70),(238,209,71),(238,210,72),(238,663,73),(238,674,74),(238,116,75),(238,211,76),(238,693,77),(238,212,78),(238,118,79),(238,213,80),(238,119,81),(238,214,82),(238,120,83),(238,657,84),(238,122,85),(238,216,86),(238,696,87),(238,123,88),(238,217,89),(238,700,90),(238,125,91),(238,689,92),(238,220,93),(238,127,94),(238,221,95),(238,128,96),(238,129,97),(238,681,98),(238,695,99),(238,132,100),(238,133,101),(238,134,102),(238,135,103),(238,224,104),(238,671,105),(238,225,106),(238,137,107),(238,226,108),(238,227,109),(238,138,110),(238,139,111),(238,140,112),(238,22,113),(238,229,114),(238,141,115),(238,679,116),(238,144,117),(238,143,118),(238,146,119),(238,232,120),(238,145,121),(238,234,122),(238,660,123),(238,235,124),(238,236,125),(238,148,126),(238,34,127),(238,237,128),(238,238,129),(238,150,130),(238,151,131),(238,239,132),(238,241,133),(238,152,134),(238,242,135),(238,684,136),(238,243,137),(238,244,138),(238,697,139),(238,664,140),(238,245,141),(238,153,142),(238,43,143),(238,154,144),(238,672,145),(238,687,146),(238,156,147),(238,159,148),(238,160,149),(238,161,150),(238,51,151),(238,701,152),(238,248,153),(238,250,154),(238,55,155),(238,251,156),(238,682,157),(238,252,158),(238,673,159),(238,662,160),(238,164,161),(238,166,162),(238,165,163),(238,683,164),(238,167,165),(238,655,166),(238,677,167),(238,63,168),(238,666,169),(238,254,170),(238,255,171),(238,256,172),(238,257,173),(238,258,174),(238,169,175),(238,678,176),(238,170,177),(238,260,178),(238,790,179),(238,261,180),(238,262,181),(238,652,182),(238,653,183),(238,263,184),(238,264,185),(238,654,186),(238,265,187),(238,266,188),(238,267,189),(238,268,190),(238,269,191),(238,270,192),(238,271,193),(238,272,194),(238,273,195),(238,274,196),(238,275,197),(238,276,198),(238,277,199),(238,278,200),(238,279,201),(238,280,202),(238,281,203),(238,282,204),(238,283,205),(238,284,206),(238,285,207),(238,286,208),(238,287,209),(238,288,210),(238,289,211),(238,290,212),(238,291,213),(238,292,214),(238,293,215),(238,294,216),(238,295,217),(238,296,218),(238,297,219),(238,298,220),(238,299,221),(238,300,222),(238,301,223),(238,302,224),(238,303,225),(238,304,226),(238,305,227),(238,306,228),(238,307,229),(238,308,230),(238,309,231),(238,310,232),(238,179,233),(238,311,234),(238,191,235),(238,180,236),(238,99,237),(238,205,238),(238,312,239),(238,313,240),(238,314,241),(238,315,242),(238,316,243),(238,317,244),(238,318,245),(238,319,246),(238,320,247),(238,321,248),(238,322,249),(238,323,250),(238,324,251),(238,325,252),(238,326,253),(238,327,254),(238,328,255),(238,329,256),(238,330,257),(238,331,258),(238,332,259),(238,333,260),(238,334,261),(238,335,262),(238,336,263),(238,337,264),(238,338,265),(238,339,266),(238,340,267),(238,341,268),(238,342,269),(238,343,270),(238,703,271),(238,704,272),(238,705,273),(238,706,274),(238,707,275),(238,708,276),(238,709,277),(238,710,278),(238,711,279),(238,712,280),(238,713,281),(238,714,282),(238,715,283),(238,716,284),(238,717,285),(238,718,286),(238,735,287),(238,736,288),(238,737,289),(238,738,290),(238,739,291),(238,740,292),(238,741,293),(238,742,294),(238,743,295),(238,744,296),(238,745,297),(238,746,298),(238,747,299),(238,748,300),(238,749,301),(238,750,302),(238,751,303),(238,752,304),(238,753,305),(238,754,306),(238,755,307),(238,756,308),(238,757,309),(238,758,310),(238,759,311),(238,760,312),(238,761,313),(238,762,314),(238,763,315),(238,764,316),(238,765,317),(238,766,318),(238,767,319),(238,768,320),(238,769,321),(238,770,322),(238,771,323),(238,772,324),(238,773,325),(238,774,326),(238,775,327),(238,776,328),(238,777,329),(238,778,330),(238,779,331),(238,780,332),(238,781,333),(238,782,334),(238,783,335),(238,784,336),(238,785,337),(238,786,338),(238,787,339),(238,788,340),(238,789,341),(238,344,342),(238,345,343),(238,346,344),(238,347,345),(238,348,346),(238,349,347),(238,350,348),(238,351,349),(238,72,350),(238,352,351),(238,353,352),(238,354,353),(238,355,354),(238,356,355),(238,357,356),(238,73,357),(238,358,358),(238,359,359),(238,74,360),(238,360,361),(238,361,362),(238,362,363),(238,363,364),(238,364,365),(238,365,366),(238,366,367),(238,367,368),(238,75,369),(238,368,370),(238,369,371),(238,370,372),(238,371,373),(238,372,374),(238,76,375),(238,373,376),(238,77,377),(238,78,378),(238,374,379),(238,375,380),(238,376,381),(238,377,382),(238,378,383),(238,379,384),(238,380,385),(238,791,386),(238,381,387),(238,382,388),(238,383,389),(238,384,390),(238,385,391),(238,386,392),(238,387,393),(238,388,394),(238,389,395),(238,390,396),(238,393,397),(238,70,398),(238,792,399),(238,398,400),(238,793,401),(238,794,402),(238,399,403),(238,795,404),(238,796,405),(238,797,406),(238,400,407),(238,401,408),(238,402,409),(238,404,410),(238,406,411),(238,407,412),(238,408,413),(238,410,414),(238,411,415),(238,798,416),(238,799,417),(238,800,418),(238,418,419),(238,432,420),(238,437,421),(238,438,422),(238,439,423),(238,440,424),(238,441,425),(238,442,426),(238,443,427),(238,444,428),(238,801,429),(238,802,430),(238,803,431),(238,445,432),(238,804,433),(238,446,434),(238,447,435),(238,805,436),(238,448,437),(238,449,438),(238,450,439),(238,451,440),(238,452,441),(238,806,442),(238,807,443),(238,453,444),(238,454,445),(238,808,446),(238,809,447),(238,810,448),(238,811,449),(238,455,450),(238,456,451),(238,458,452),(238,459,453),(238,460,454),(238,461,455),(238,463,456),(238,464,457),(238,465,458),(238,466,459),(238,467,460),(238,468,461),(238,469,462),(238,470,463),(238,471,464),(238,472,465),(238,473,466),(238,474,467),(238,475,468),(238,476,469),(238,477,470),(238,812,471),(238,813,472),(238,478,473),(238,479,474),(238,480,475),(238,481,476),(238,482,477),(238,483,478),(238,484,479),(238,485,480),(238,486,481),(238,487,482),(238,488,483),(238,489,484),(238,490,485),(238,491,486),(238,492,487),(238,493,488),(238,494,489),(238,495,490),(238,496,491),(238,497,492),(238,498,493),(238,499,494),(238,500,495),(238,501,496),(238,502,497),(238,503,498),(238,814,499),(238,504,500),(238,505,501),(238,506,502),(238,507,503),(238,508,504),(238,509,505),(238,510,506),(238,511,507),(238,512,508),(238,513,509),(238,514,510),(238,515,511),(238,516,512),(238,517,513),(238,518,514),(238,33,515),(238,519,516),(238,520,517),(238,521,518),(238,522,519),(238,523,520),(238,524,521),(238,815,522),(238,525,523),(238,816,524),(238,817,525),(238,818,526),(238,819,527),(238,820,528),(238,526,529),(238,821,530),(238,822,531),(238,823,532),(238,824,533),(238,825,534),(238,826,535),(238,827,536),(238,828,537),(238,829,538),(238,830,539),(238,831,540),(238,832,541),(238,833,542),(238,834,543),(238,835,544),(238,527,545),(238,528,546),(238,529,547),(238,836,548),(238,837,549),(238,530,550),(238,531,551),(238,532,552),(238,533,553),(238,534,554),(238,535,555),(238,536,556),(238,537,557),(238,538,558),(238,539,559),(238,540,560),(238,541,561),(238,542,562),(238,543,563),(238,544,564),(238,545,565),(238,546,566),(238,547,567),(238,548,568),(238,549,569),(238,550,570),(238,551,571),(238,552,572),(238,553,573),(238,554,574),(238,555,575),(238,556,576),(238,557,577),(238,558,578),(238,559,579),(238,560,580),(238,561,581),(238,562,582),(238,563,583),(238,564,584),(238,565,585),(238,566,586),(238,567,587),(238,568,588),(238,569,589),(238,570,590),(238,571,591),(238,572,592),(238,573,593),(238,574,594),(238,575,595),(238,576,596),(238,577,597),(238,578,598),(238,579,599),(238,580,600),(238,581,601),(238,582,602),(238,583,603),(238,584,604),(238,585,605),(238,838,606),(325,839,0),(325,840,1),(325,841,2),(325,842,3),(325,843,4),(325,844,5),(325,845,6),(325,846,7),(325,847,8),(325,848,9),(325,849,10),(325,586,11),(325,587,12),(223,214,0),(223,288,1),(223,292,2),(223,303,3),(223,172,4),(223,122,5),(223,79,6),(223,123,7),(223,174,8),(223,217,9),(223,178,10),(223,306,11),(223,282,12),(223,127,13),(223,296,14),(223,294,15),(223,86,16),(223,297,17),(223,129,18),(223,89,19),(223,278,20),(223,132,21),(223,134,22),(223,276,23),(223,135,24),(223,187,25),(223,138,26),(223,304,27),(223,95,28),(223,141,29),(223,295,30),(223,272,31),(223,144,32),(223,143,33),(223,302,34),(223,146,35),(223,287,36),(223,299,37),(223,301,38),(223,286,39),(223,234,40),(223,97,41),(223,236,42),(223,280,43),(223,100,44),(223,307,45),(223,279,46),(223,192,47),(223,239,48),(223,241,49),(223,290,50),(223,103,51),(223,284,52),(223,291,53),(223,245,54),(223,196,55),(223,197,56),(223,289,57),(223,283,58),(223,159,59),(223,281,60),(223,198,61),(223,271,62),(223,285,63),(223,277,64),(223,269,65),(223,308,66),(223,251,67),(223,110,68),(223,252,69),(223,164,70),(223,166,71),(223,165,72),(223,204,73),(223,293,74),(223,255,75),(223,305,76),(223,257,77),(223,210,78),(223,258,79),(223,211,80),(223,298,81),(223,300,82),(223,270,83),(223,169,84),(223,213,85),(223,170,86),(223,168,87),(223,131,88),(223,199,89),(223,83,90),(223,81,91),(223,189,92),(223,249,93),(223,231,94),(223,126,95),(223,200,96),(223,171,97),(223,107,98),(223,88,99),(223,242,100),(223,91,101),(223,101,102),(223,447,103),(223,458,104),(223,459,105),(223,460,106),(223,461,107),(223,262,108),(223,261,109),(237,667,0),(237,79,1),(237,668,2),(237,658,3),(237,80,4),(237,81,5),(237,83,6),(237,82,7),(237,84,8),(237,702,9),(237,86,10),(237,85,11),(237,680,12),(237,676,13),(237,88,14),(237,87,15),(237,89,16),(237,685,17),(237,90,18),(237,659,19),(237,92,20),(237,91,21),(237,694,22),(237,669,23),(237,699,24),(237,690,25),(237,93,26),(237,94,27),(237,95,28),(237,96,29),(237,97,30),(237,100,31),(237,99,32),(237,101,33),(237,36,34),(237,688,35),(237,102,36),(237,103,37),(237,44,38),(237,104,39),(237,105,40),(237,686,41),(237,106,42),(237,107,43),(237,109,44),(237,691,45),(237,110,46),(237,111,47),(237,661,48),(237,112,49),(237,692,50),(237,114,51),(237,656,52),(237,115,53),(237,116,54),(237,117,55),(237,119,56),(237,120,57),(237,121,58),(237,657,59),(237,122,60),(237,123,61),(237,124,62),(237,700,63),(237,126,64),(237,127,65),(237,128,66),(237,129,67),(237,681,68),(237,130,69),(237,131,70),(237,132,71),(237,133,72),(237,134,73),(237,136,74),(237,135,75),(237,671,76),(237,137,77),(237,138,78),(237,139,79),(237,22,80),(237,140,81),(237,141,82),(237,142,83),(237,143,84),(237,144,85),(237,146,86),(237,145,87),(237,147,88),(237,148,89),(237,149,90),(237,150,91),(237,152,92),(237,684,93),(237,664,94),(237,154,95),(237,153,96),(237,155,97),(237,672,98),(237,156,99),(237,157,100),(237,158,101),(237,159,102),(237,161,103),(237,51,104),(237,162,105),(237,163,106),(237,164,107),(237,166,108),(237,165,109),(237,677,110),(237,167,111),(237,63,112),(237,168,113),(237,666,114),(237,169,115),(237,170,116),(237,171,117),(237,172,118),(237,174,119),(237,698,120),(237,175,121),(237,176,122),(237,6,123),(237,177,124),(237,178,125),(237,8,126),(237,179,127),(237,180,128),(237,665,129),(237,181,130),(237,182,131),(237,184,132),(237,186,133),(237,187,134),(237,670,135),(237,189,136),(237,190,137),(237,191,138),(237,192,139),(237,193,140),(237,194,141),(237,675,142),(237,196,143),(237,197,144),(237,198,145),(237,199,146),(237,200,147),(237,201,148),(237,202,149),(237,203,150),(237,205,151),(237,204,152),(237,207,153),(237,206,154),(237,208,155),(237,210,156),(237,663,157),(237,674,158),(237,211,159),(237,693,160),(237,212,161),(237,213,162),(237,214,163),(237,215,164),(237,216,165),(237,696,166),(237,217,167),(237,689,168),(237,218,169),(237,219,170),(237,221,171),(237,695,172),(237,223,173),(237,222,174),(237,224,175),(237,225,176),(237,227,177),(237,228,178),(237,229,179),(237,230,180),(237,679,181),(237,231,182),(237,232,183),(237,233,184),(237,234,185),(237,660,186),(237,235,187),(237,236,188),(237,34,189),(237,237,190),(237,238,191),(237,239,192),(237,240,193),(237,241,194),(237,242,195),(237,243,196),(237,244,197),(237,697,198),(237,43,199),(237,245,200),(237,687,201),(237,246,202),(237,247,203),(237,701,204),(237,248,205),(237,249,206),(237,55,207),(237,251,208),(237,682,209),(237,252,210),(237,673,211),(237,253,212),(237,662,213),(237,683,214),(237,655,215),(237,254,216),(237,255,217),(237,256,218),(237,257,219),(237,258,220),(237,259,221),(237,678,222),(237,261,223),(237,262,224),(237,652,225),(237,653,226),(237,269,227),(237,270,228),(237,271,229),(237,272,230),(237,274,231),(237,275,232),(237,273,233),(237,276,234),(237,277,235),(237,278,236),(237,279,237),(237,280,238),(237,281,239),(237,282,240),(237,283,241),(237,284,242),(237,285,243),(237,286,244),(237,287,245),(237,288,246),(237,289,247),(237,290,248),(237,291,249),(237,292,250),(237,293,251),(237,294,252),(237,295,253),(237,296,254),(237,297,255),(237,298,256),(237,299,257),(237,300,258),(237,301,259),(237,302,260),(237,303,261),(237,304,262),(237,305,263),(237,306,264),(237,307,265),(237,308,266),(237,310,267),(237,311,268),(237,113,269),(237,226,270),(237,125,271),(237,318,272),(237,319,273),(237,320,274),(237,321,275),(237,322,276),(237,323,277),(237,324,278),(237,325,279),(237,326,280),(237,327,281),(237,328,282),(237,329,283),(237,330,284),(237,331,285),(237,332,286),(237,333,287),(237,334,288),(237,335,289),(237,336,290),(237,337,291),(237,338,292),(237,339,293),(237,340,294),(237,341,295),(237,703,296),(237,704,297),(237,705,298),(237,706,299),(237,707,300),(237,708,301),(237,709,302),(237,710,303),(237,711,304),(237,712,305),(237,713,306),(237,714,307),(237,715,308),(237,716,309),(237,717,310),(237,718,311),(237,719,312),(237,720,313),(237,721,314),(237,722,315),(237,723,316),(237,724,317),(237,725,318),(237,726,319),(237,727,320),(237,728,321),(237,729,322),(237,730,323),(237,731,324),(237,732,325),(237,733,326),(237,734,327),(237,735,328),(237,736,329),(237,737,330),(237,738,331),(237,739,332),(237,740,333),(237,741,334),(237,742,335),(237,743,336),(237,744,337),(237,745,338),(237,746,339),(237,747,340),(237,748,341),(237,749,342),(237,750,343),(237,751,344),(237,752,345),(237,753,346),(237,754,347),(237,755,348),(237,756,349),(237,757,350),(237,758,351),(237,759,352),(237,760,353),(237,761,354),(237,762,355),(237,763,356),(237,764,357),(237,765,358),(237,766,359),(237,767,360),(237,768,361),(237,769,362),(237,770,363),(237,771,364),(237,772,365),(237,773,366),(237,774,367),(237,775,368),(237,776,369),(237,777,370),(237,778,371),(237,779,372),(237,780,373),(237,781,374),(237,782,375),(237,783,376),(237,784,377),(237,785,378),(237,786,379),(237,787,380),(237,788,381),(237,789,382),(237,72,383),(237,73,384),(237,74,385),(237,75,386),(237,76,387),(237,77,388),(237,78,389),(237,374,390),(237,375,391),(237,376,392),(237,377,393),(237,378,394),(237,379,395),(237,380,396),(237,391,397),(237,392,398),(237,70,399),(237,394,400),(237,395,401),(237,396,402),(237,397,403),(237,792,404),(237,398,405),(237,399,406),(237,400,407),(237,401,408),(237,402,409),(237,403,410),(237,404,411),(237,405,412),(237,406,413),(237,407,414),(237,408,415),(237,409,416),(237,410,417),(237,411,418),(237,412,419),(237,413,420),(237,414,421),(237,415,422),(237,416,423),(237,417,424),(237,418,425),(237,419,426),(237,420,427),(237,421,428),(237,422,429),(237,423,430),(237,424,431),(237,425,432),(237,426,433),(237,427,434),(237,428,435),(237,429,436),(237,430,437),(237,431,438),(237,432,439),(237,433,440),(237,434,441),(237,435,442),(237,436,443),(237,438,444),(237,439,445),(237,440,446),(237,441,447),(237,443,448),(237,801,449),(237,802,450),(237,803,451),(237,804,452),(237,447,453),(237,805,454),(237,448,455),(237,449,456),(237,450,457),(237,451,458),(237,452,459),(237,806,460),(237,807,461),(237,453,462),(237,454,463),(237,455,464),(237,456,465),(237,457,466),(237,458,467),(237,459,468),(237,460,469),(237,461,470),(237,462,471),(237,463,472),(237,464,473),(237,465,474),(237,466,475),(237,467,476),(237,812,477),(237,813,478),(237,478,479),(237,492,480),(237,503,481),(237,33,482),(237,815,483),(237,816,484),(237,817,485),(237,818,486),(237,819,487),(237,820,488),(237,821,489),(237,822,490),(237,823,491),(237,824,492),(237,825,493),(237,826,494),(237,827,495),(237,828,496),(237,829,497),(237,830,498),(237,831,499),(237,832,500),(237,833,501),(237,834,502),(237,835,503),(237,836,504),(237,837,505),(237,570,506),(237,571,507),(237,572,508),(237,573,509),(237,574,510),(237,575,511),(237,576,512),(237,577,513),(237,578,514),(237,579,515),(237,580,516),(237,581,517),(324,839,0),(324,840,1),(324,841,2),(324,842,3),(324,843,4),(324,845,5),(324,847,6),(324,848,7),(293,796,0),(293,795,1),(293,797,2),(293,790,3),(293,850,4),(293,800,5),(293,798,6),(293,792,7),(293,851,8),(293,791,9),(293,852,10),(293,853,11),(293,854,12),(293,855,13),(293,794,14),(293,856,15),(293,857,16),(293,858,17),(293,799,18),(293,793,19),(227,859,0),(227,860,1),(227,390,2),(227,861,3),(227,371,4),(227,173,5),(227,479,6),(227,263,7),(227,862,8),(227,863,9),(227,864,10),(227,480,11),(227,865,12),(227,384,13),(227,364,14),(227,866,15),(227,387,16),(227,350,17),(227,185,18),(227,358,19),(227,867,20),(227,188,21),(227,389,22),(227,491,23),(227,372,24),(227,868,25),(227,385,26),(227,351,27),(227,869,28),(227,342,29),(227,354,30),(227,490,31),(227,359,32),(227,485,33),(227,870,34),(227,98,35),(227,361,36),(227,488,37),(227,871,38),(227,872,39),(227,873,40),(227,388,41),(227,874,42),(227,195,43),(227,489,44),(227,362,45),(227,875,46),(227,345,47),(227,876,48),(227,877,49),(227,878,50),(227,879,51),(227,108,52),(227,880,53),(227,344,54),(227,881,55),(227,357,56),(227,315,57),(227,360,58),(227,367,59),(227,264,60),(227,493,61),(227,383,62),(227,882,63),(227,883,64),(227,884,65),(227,343,66),(227,885,67),(227,349,68),(227,209,69),(227,886,70),(227,887,71),(227,484,72),(227,888,73),(227,889,74),(227,890,75),(227,891,76),(227,892,77),(227,893,78),(227,894,79),(227,220,80),(227,895,81),(227,381,82),(227,896,83),(227,346,84),(227,897,85),(227,370,86),(227,898,87),(227,899,88),(227,900,89),(227,483,90),(227,363,91),(227,355,92),(227,901,93),(227,386,94),(227,902,95),(227,903,96),(227,904,97),(227,356,98),(227,905,99),(227,906,100),(227,907,101),(227,373,102),(227,908,103),(227,151,104),(227,909,105),(227,910,106),(227,494,107),(227,911,108),(227,382,109),(227,912,110),(227,913,111),(227,914,112),(227,495,113),(227,487,114),(227,915,115),(227,916,116),(227,917,117),(227,160,118),(227,496,119),(227,365,120),(227,918,121),(227,353,122),(227,919,123),(227,497,124),(227,920,125),(227,921,126),(227,250,127),(227,922,128),(227,481,129),(227,486,130),(227,923,131),(227,924,132),(227,925,133),(227,369,134),(227,482,135),(227,366,136),(227,926,137),(227,927,138),(227,928,139),(227,929,140),(227,393,141),(227,260,142),(227,437,143),(227,442,144),(227,444,145),(227,445,146),(227,446,147),(227,505,148),(227,506,149),(227,507,150),(227,508,151),(227,509,152),(227,510,153),(227,511,154),(227,513,155),(227,514,156),(227,515,157),(227,516,158),(227,517,159),(227,518,160),(227,519,161),(328,586,0),(328,587,1),(224,930,0),(224,931,1),(224,932,2),(224,933,3),(224,267,4),(224,934,5),(224,935,6),(224,265,7),(224,936,8),(224,937,9),(224,499,10),(224,266,11),(224,938,12),(224,183,13),(224,268,14),(224,939,15),(224,940,16),(224,118,17),(224,941,18),(224,500,19),(224,501,20),(229,942,0),(222,943,0),(222,944,1),(222,945,2),(222,946,3),(222,947,4),(222,948,5),(222,949,6),(222,950,7),(222,951,8),(222,952,9),(222,953,10),(222,954,11),(222,955,12),(222,956,13),(297,66,0),(297,10,1),(297,35,2),(297,54,3),(297,28,4),(297,19,5),(297,42,6),(297,18,7),(297,36,8),(297,5,9),(297,29,10),(297,26,11),(297,30,12),(297,47,13),(297,24,14),(297,7,15),(297,62,16),(297,1,17),(297,17,18),(297,60,19),(297,58,20),(297,34,21),(297,46,22),(297,15,23),(297,13,24),(297,25,25),(297,53,26),(297,67,27),(297,6,28),(297,65,29),(297,11,30),(297,71,31),(297,45,32),(297,50,33),(297,22,34),(297,2,35),(297,61,36),(297,73,37),(297,76,38),(297,77,39),(297,78,40),(297,21,41),(297,14,42),(297,31,43),(297,59,44),(297,40,45),(297,37,46),(297,12,47),(297,56,48),(297,51,49),(297,9,50),(297,4,51),(297,43,52),(297,52,53),(297,55,54),(297,63,55),(297,8,56),(297,57,57),(297,69,58),(297,68,59),(297,32,60),(297,23,61),(297,48,62),(297,27,63),(297,44,64),(297,41,65),(297,20,66),(297,39,67),(297,16,68),(297,49,69),(297,70,70),(297,64,71),(297,38,72),(297,808,73),(297,809,74),(297,810,75),(297,936,76),(297,938,77),(297,932,78),(297,930,79),(297,931,80),(297,940,81),(297,934,82),(297,939,83),(297,941,84),(297,933,85),(297,935,86),(297,951,87),(297,947,88),(297,455,89),(297,456,90),(297,33,91),(297,811,92),(297,838,93),(300,66,0),(300,10,1),(300,35,2),(300,54,3),(300,28,4),(300,19,5),(300,42,6),(300,18,7),(300,36,8),(300,5,9),(300,29,10),(300,26,11),(300,30,12),(300,47,13),(300,24,14),(300,7,15),(300,62,16),(300,1,17),(300,17,18),(300,60,19),(300,58,20),(300,34,21),(300,46,22),(300,15,23),(300,13,24),(300,25,25),(300,53,26),(300,67,27),(300,6,28),(300,65,29),(300,11,30),(300,71,31),(300,45,32),(300,50,33),(300,22,34),(300,2,35),(300,61,36),(300,73,37),(300,76,38),(300,77,39),(300,78,40),(300,21,41),(300,14,42),(300,31,43),(300,59,44),(300,40,45),(300,37,46),(300,12,47),(300,56,48),(300,51,49),(300,9,50),(300,4,51),(300,43,52),(300,52,53),(300,55,54),(300,63,55),(300,8,56),(300,57,57),(300,69,58),(300,68,59),(300,32,60),(300,23,61),(300,48,62),(300,27,63),(300,44,64),(300,41,65),(300,20,66),(300,39,67),(300,16,68),(300,49,69),(300,70,70),(300,64,71),(300,38,72),(300,957,73),(300,958,74),(300,959,75),(300,960,76),(300,961,77),(300,962,78),(300,963,79),(300,964,80),(300,965,81),(300,966,82),(300,967,83),(300,968,84),(300,969,85),(300,970,86),(300,971,87),(300,972,88),(300,973,89),(300,974,90),(300,975,91),(300,976,92),(300,977,93),(300,978,94),(300,979,95),(300,980,96),(300,981,97),(300,982,98),(300,983,99),(300,984,100),(300,985,101),(300,986,102),(300,987,103),(300,988,104),(300,989,105),(300,956,106),(300,954,107),(300,455,108),(300,456,109),(300,33,110),(296,66,0),(296,10,1),(296,35,2),(296,54,3),(296,28,4),(296,19,5),(296,42,6),(296,18,7),(296,36,8),(296,5,9),(296,29,10),(296,26,11),(296,3,12),(296,30,13),(296,47,14),(296,24,15),(296,7,16),(296,62,17),(296,1,18),(296,17,19),(296,60,20),(296,58,21),(296,34,22),(296,46,23),(296,15,24),(296,13,25),(296,25,26),(296,53,27),(296,67,28),(296,6,29),(296,65,30),(296,11,31),(296,71,32),(296,45,33),(296,50,34),(296,22,35),(296,2,36),(296,61,37),(296,73,38),(296,76,39),(296,77,40),(296,78,41),(296,21,42),(296,14,43),(296,31,44),(296,59,45),(296,40,46),(296,37,47),(296,12,48),(296,56,49),(296,51,50),(296,9,51),(296,4,52),(296,43,53),(296,52,54),(296,55,55),(296,63,56),(296,8,57),(296,57,58),(296,69,59),(296,68,60),(296,32,61),(296,23,62),(296,48,63),(296,27,64),(296,44,65),(296,41,66),(296,20,67),(296,39,68),(296,16,69),(296,49,70),(296,70,71),(296,64,72),(296,38,73),(296,588,74),(296,589,75),(296,590,76),(296,463,77),(296,591,78),(296,464,79),(296,592,80),(296,593,81),(296,594,82),(296,443,83),(296,595,84),(296,596,85),(296,597,86),(296,598,87),(296,599,88),(296,310,89),(296,600,90),(296,601,91),(296,602,92),(296,603,93),(296,604,94),(296,605,95),(296,606,96),(296,607,97),(296,608,98),(296,609,99),(296,610,100),(296,611,101),(296,612,102),(296,613,103),(296,614,104),(296,615,105),(296,616,106),(296,617,107),(296,154,108),(296,618,109),(296,619,110),(296,620,111),(296,621,112),(296,622,113),(296,623,114),(296,624,115),(296,625,116),(296,626,117),(296,627,118),(296,628,119),(296,629,120),(296,630,121),(296,631,122),(296,632,123),(296,633,124),(296,634,125),(296,635,126),(296,636,127),(296,637,128),(296,638,129),(296,438,130),(296,418,131),(296,639,132),(296,640,133),(296,641,134),(296,448,135),(296,167,136),(296,642,137),(296,194,138),(296,119,139),(296,137,140),(296,148,141),(296,150,142),(296,643,143),(296,644,144),(296,645,145),(296,646,146),(296,647,147),(296,648,148),(296,649,149),(296,650,150),(296,651,151),(296,990,152),(296,991,153),(296,992,154),(296,993,155),(296,994,156),(296,995,157),(296,996,158),(296,997,159),(296,998,160),(296,999,161),(296,946,162),(296,945,163),(296,955,164),(296,952,165),(296,123,166),(296,276,167),(296,277,168),(296,271,169),(296,278,170),(296,279,171),(296,280,172),(296,281,173),(296,282,174),(296,283,175),(296,284,176),(296,285,177),(296,286,178),(296,287,179),(296,288,180),(296,289,181),(296,290,182),(296,291,183),(296,292,184),(296,293,185),(296,294,186),(296,295,187),(296,135,188),(296,262,189),(296,261,190),(296,298,191),(296,299,192),(296,300,193),(296,301,194),(296,302,195),(296,303,196),(296,304,197),(296,305,198),(296,306,199),(296,307,200),(296,169,201),(296,308,202),(296,192,203),(296,204,204),(296,245,205),(296,172,206),(296,458,207),(296,460,208),(296,461,209),(296,459,210),(296,447,211),(296,122,212),(296,165,213),(296,174,214),(296,214,215),(296,197,216),(296,143,217),(296,178,218),(296,187,219),(296,211,220),(296,257,221),(296,134,222),(296,144,223),(296,159,224),(296,258,225),(296,89,226),(296,97,227),(296,251,228),(296,95,229),(296,127,230),(296,100,231),(296,196,232),(296,210,233),(296,103,234),(296,234,235),(296,241,236),(296,138,237),(296,252,238),(296,166,239),(296,146,240),(296,239,241),(296,164,242),(296,129,243),(296,213,244),(296,217,245),(296,255,246),(296,132,247),(296,141,248),(296,236,249),(296,110,250),(296,953,251),(296,948,252),(296,936,253),(296,938,254),(296,932,255),(296,930,256),(296,931,257),(296,940,258),(296,934,259),(296,939,260),(296,941,261),(296,933,262),(296,935,263),(296,949,264),(296,950,265),(296,943,266),(296,216,267),(296,380,268),(296,1000,269),(296,1001,270),(296,153,271),(296,202,272),(296,139,273),(296,1002,274),(296,1003,275),(296,225,276),(296,140,277),(296,186,278),(296,152,279),(296,243,280),(296,109,281),(296,156,282),(296,80,283),(296,232,284),(296,227,285),(296,203,286),(296,248,287),(296,238,288),(296,229,289),(296,161,290),(296,145,291),(296,105,292),(296,114,293),(296,212,294),(296,193,295),(296,128,296),(296,235,297),(296,244,298),(296,440,299),(296,468,300),(296,469,301),(296,406,302),(296,470,303),(296,471,304),(296,472,305),(296,432,306),(296,473,307),(296,439,308),(296,474,309),(296,398,310),(296,466,311),(296,404,312),(296,441,313),(296,475,314),(296,465,315),(296,476,316),(296,477,317),(296,401,318),(296,402,319),(296,467,320),(296,407,321),(296,410,322),(296,313,323),(296,312,324),(296,309,325),(296,314,326),(296,944,327),(296,198,328),(296,478,329),(296,449,330),(296,79,331),(296,272,332),(296,270,333),(296,296,334),(296,297,335),(296,311,336),(296,492,337),(296,453,338),(296,179,339),(296,191,340),(296,180,341),(296,125,342),(296,84,343),(296,113,344),(296,226,345),(296,99,346),(296,205,347),(296,133,348),(296,112,349),(296,175,350),(296,111,351),(296,455,352),(296,456,353),(296,120,354),(296,254,355),(296,451,356),(296,170,357),(296,503,358),(296,224,359),(296,221,360),(296,450,361),(296,317,362),(296,348,363),(296,33,364),(296,237,365),(296,206,366),(296,86,367),(296,454,368),(296,256,369),(296,269,370),(296,347,371),(296,368,372),(296,352,373),(296,452,374),(296,375,375),(296,376,376),(296,377,377),(296,378,378),(296,379,379),(296,374,380),(296,570,381),(296,571,382),(296,572,383),(296,573,384),(296,574,385),(296,575,386),(296,576,387),(296,577,388),(296,578,389),(296,579,390),(296,580,391),(296,116,392),(296,581,393),(296,316,394),(296,498,395),(296,582,396),(296,583,397),(296,584,398),(296,502,399),(296,585,400),(296,561,401),(296,562,402),(296,512,403),(296,504,404),(296,528,405),(296,563,406),(296,521,407),(296,523,408),(296,522,409),(296,564,410),(296,541,411),(296,565,412),(296,540,413),(296,560,414),(296,535,415),(296,538,416),(296,524,417),(296,525,418),(296,568,419),(296,569,420),(296,534,421),(296,567,422),(296,566,423),(296,530,424),(296,520,425),(296,549,426),(296,547,427),(299,66,0),(299,10,1),(299,35,2),(299,54,3),(299,28,4),(299,19,5),(299,42,6),(299,18,7),(299,36,8),(299,5,9),(299,29,10),(299,26,11),(299,3,12),(299,30,13),(299,47,14),(299,24,15),(299,7,16),(299,62,17),(299,1,18),(299,17,19),(299,60,20),(299,58,21),(299,34,22),(299,46,23),(299,15,24),(299,13,25),(299,25,26),(299,53,27),(299,67,28),(299,6,29),(299,65,30),(299,11,31),(299,71,32),(299,45,33),(299,50,34),(299,22,35),(299,2,36),(299,61,37),(299,73,38),(299,76,39),(299,77,40),(299,78,41),(299,21,42),(299,14,43),(299,31,44),(299,59,45),(299,40,46),(299,37,47),(299,12,48),(299,56,49),(299,51,50),(299,9,51),(299,4,52),(299,43,53),(299,52,54),(299,55,55),(299,63,56),(299,8,57),(299,57,58),(299,69,59),(299,68,60),(299,32,61),(299,23,62),(299,48,63),(299,27,64),(299,44,65),(299,41,66),(299,20,67),(299,39,68),(299,16,69),(299,49,70),(299,70,71),(299,64,72),(299,38,73),(299,588,74),(299,589,75),(299,590,76),(299,463,77),(299,591,78),(299,464,79),(299,592,80),(299,593,81),(299,594,82),(299,443,83),(299,595,84),(299,596,85),(299,597,86),(299,598,87),(299,599,88),(299,310,89),(299,600,90),(299,601,91),(299,602,92),(299,603,93),(299,604,94),(299,605,95),(299,606,96),(299,607,97),(299,608,98),(299,609,99),(299,610,100),(299,611,101),(299,612,102),(299,613,103),(299,614,104),(299,615,105),(299,616,106),(299,617,107),(299,154,108),(299,618,109),(299,619,110),(299,620,111),(299,621,112),(299,622,113),(299,623,114),(299,624,115),(299,625,116),(299,626,117),(299,627,118),(299,628,119),(299,629,120),(299,630,121),(299,631,122),(299,632,123),(299,633,124),(299,634,125),(299,635,126),(299,636,127),(299,637,128),(299,638,129),(299,438,130),(299,418,131),(299,639,132),(299,640,133),(299,641,134),(299,448,135),(299,167,136),(299,642,137),(299,194,138),(299,119,139),(299,137,140),(299,148,141),(299,150,142),(299,643,143),(299,644,144),(299,645,145),(299,646,146),(299,647,147),(299,648,148),(299,649,149),(299,650,150),(299,651,151),(299,957,152),(299,958,153),(299,959,154),(299,960,155),(299,961,156),(299,962,157),(299,963,158),(299,964,159),(299,965,160),(299,966,161),(299,967,162),(299,968,163),(299,969,164),(299,970,165),(299,971,166),(299,972,167),(299,973,168),(299,974,169),(299,975,170),(299,976,171),(299,977,172),(299,978,173),(299,979,174),(299,980,175),(299,981,176),(299,982,177),(299,983,178),(299,984,179),(299,985,180),(299,986,181),(299,987,182),(299,988,183),(299,989,184),(299,727,185),(299,730,186),(299,731,187),(299,946,188),(299,945,189),(299,955,190),(299,952,191),(299,123,192),(299,276,193),(299,168,194),(299,131,195),(299,199,196),(299,83,197),(299,81,198),(299,189,199),(299,249,200),(299,231,201),(299,126,202),(299,200,203),(299,277,204),(299,271,205),(299,278,206),(299,279,207),(299,280,208),(299,281,209),(299,282,210),(299,283,211),(299,284,212),(299,285,213),(299,286,214),(299,287,215),(299,288,216),(299,289,217),(299,290,218),(299,291,219),(299,292,220),(299,293,221),(299,294,222),(299,91,223),(299,171,224),(299,107,225),(299,88,226),(299,242,227),(299,101,228),(299,295,229),(299,135,230),(299,262,231),(299,261,232),(299,298,233),(299,299,234),(299,300,235),(299,301,236),(299,302,237),(299,303,238),(299,304,239),(299,305,240),(299,306,241),(299,307,242),(299,169,243),(299,308,244),(299,192,245),(299,204,246),(299,245,247),(299,172,248),(299,458,249),(299,460,250),(299,461,251),(299,459,252),(299,447,253),(299,122,254),(299,165,255),(299,174,256),(299,214,257),(299,197,258),(299,143,259),(299,178,260),(299,187,261),(299,211,262),(299,257,263),(299,134,264),(299,144,265),(299,159,266),(299,258,267),(299,89,268),(299,97,269),(299,251,270),(299,95,271),(299,127,272),(299,100,273),(299,196,274),(299,210,275),(299,103,276),(299,234,277),(299,241,278),(299,138,279),(299,252,280),(299,166,281),(299,146,282),(299,239,283),(299,164,284),(299,129,285),(299,213,286),(299,217,287),(299,255,288),(299,132,289),(299,141,290),(299,236,291),(299,110,292),(299,953,293),(299,948,294),(299,949,295),(299,216,296),(299,380,297),(299,1000,298),(299,1001,299),(299,153,300),(299,202,301),(299,139,302),(299,1002,303),(299,1003,304),(299,225,305),(299,140,306),(299,186,307),(299,152,308),(299,243,309),(299,109,310),(299,156,311),(299,80,312),(299,232,313),(299,227,314),(299,203,315),(299,248,316),(299,238,317),(299,229,318),(299,161,319),(299,145,320),(299,105,321),(299,114,322),(299,212,323),(299,193,324),(299,128,325),(299,235,326),(299,244,327),(299,944,328),(299,198,329),(299,478,330),(299,449,331),(299,79,332),(299,272,333),(299,270,334),(299,296,335),(299,297,336),(299,311,337),(299,492,338),(299,453,339),(299,179,340),(299,191,341),(299,180,342),(299,125,343),(299,84,344),(299,113,345),(299,226,346),(299,99,347),(299,205,348),(299,133,349),(299,112,350),(299,175,351),(299,111,352),(299,455,353),(299,456,354),(299,120,355),(299,254,356),(299,451,357),(299,170,358),(299,503,359),(299,224,360),(299,221,361),(299,33,362),(299,237,363),(299,206,364),(299,86,365),(299,454,366),(299,256,367),(299,269,368),(299,452,369),(299,375,370),(299,376,371),(299,377,372),(299,378,373),(299,379,374),(299,374,375),(299,570,376),(299,571,377),(299,572,378),(299,573,379),(299,574,380),(299,575,381),(299,576,382),(299,577,383),(299,578,384),(299,579,385),(299,580,386),(299,116,387),(299,581,388),(298,66,0),(298,10,1),(298,35,2),(298,54,3),(298,28,4),(298,19,5),(298,42,6),(298,18,7),(298,36,8),(298,5,9),(298,29,10),(298,26,11),(298,3,12),(298,30,13),(298,47,14),(298,24,15),(298,7,16),(298,62,17),(298,1,18),(298,17,19),(298,60,20),(298,58,21),(298,34,22),(298,46,23),(298,15,24),(298,13,25),(298,25,26),(298,53,27),(298,67,28),(298,6,29),(298,65,30),(298,11,31),(298,71,32),(298,45,33),(298,50,34),(298,22,35),(298,2,36),(298,61,37),(298,72,38),(298,73,39),(298,74,40),(298,75,41),(298,76,42),(298,77,43),(298,78,44),(298,21,45),(298,14,46),(298,31,47),(298,59,48),(298,40,49),(298,37,50),(298,12,51),(298,56,52),(298,51,53),(298,9,54),(298,4,55),(298,43,56),(298,52,57),(298,55,58),(298,63,59),(298,8,60),(298,57,61),(298,69,62),(298,68,63),(298,32,64),(298,23,65),(298,48,66),(298,27,67),(298,44,68),(298,41,69),(298,20,70),(298,39,71),(298,16,72),(298,49,73),(298,70,74),(298,64,75),(298,38,76),(298,588,77),(298,589,78),(298,590,79),(298,463,80),(298,591,81),(298,464,82),(298,592,83),(298,593,84),(298,594,85),(298,443,86),(298,595,87),(298,596,88),(298,597,89),(298,598,90),(298,599,91),(298,310,92),(298,600,93),(298,601,94),(298,602,95),(298,603,96),(298,604,97),(298,605,98),(298,606,99),(298,607,100),(298,608,101),(298,609,102),(298,610,103),(298,611,104),(298,612,105),(298,613,106),(298,614,107),(298,615,108),(298,616,109),(298,617,110),(298,154,111),(298,618,112),(298,619,113),(298,620,114),(298,621,115),(298,622,116),(298,623,117),(298,624,118),(298,625,119),(298,626,120),(298,627,121),(298,628,122),(298,629,123),(298,630,124),(298,631,125),(298,632,126),(298,633,127),(298,634,128),(298,635,129),(298,636,130),(298,637,131),(298,638,132),(298,438,133),(298,418,134),(298,639,135),(298,640,136),(298,641,137),(298,448,138),(298,167,139),(298,642,140),(298,194,141),(298,119,142),(298,137,143),(298,148,144),(298,150,145),(298,643,146),(298,644,147),(298,645,148),(298,646,149),(298,647,150),(298,648,151),(298,649,152),(298,650,153),(298,651,154),(298,656,155),(298,657,156),(298,658,157),(298,659,158),(298,660,159),(298,661,160),(298,662,161),(298,663,162),(298,664,163),(298,665,164),(298,666,165),(298,667,166),(298,668,167),(298,669,168),(298,670,169),(298,671,170),(298,672,171),(298,673,172),(298,674,173),(298,675,174),(298,677,175),(298,678,176),(298,679,177),(298,680,178),(298,681,179),(298,682,180),(298,683,181),(298,684,182),(298,685,183),(298,686,184),(298,687,185),(298,688,186),(298,689,187),(298,690,188),(298,691,189),(298,692,190),(298,693,191),(298,694,192),(298,695,193),(298,696,194),(298,697,195),(298,698,196),(298,699,197),(298,700,198),(298,701,199),(298,702,200),(298,802,201),(298,801,202),(298,803,203),(298,804,204),(298,805,205),(298,703,206),(298,704,207),(298,705,208),(298,706,209),(298,707,210),(298,708,211),(298,709,212),(298,710,213),(298,711,214),(298,712,215),(298,713,216),(298,714,217),(298,652,218),(298,653,219),(298,715,220),(298,716,221),(298,717,222),(298,718,223),(298,807,224),(298,806,225),(298,796,226),(298,795,227),(298,797,228),(298,850,229),(298,800,230),(298,798,231),(298,792,232),(298,851,233),(298,791,234),(298,852,235),(298,853,236),(298,854,237),(298,855,238),(298,794,239),(298,856,240),(298,857,241),(298,858,242),(298,799,243),(298,793,244),(298,735,245),(298,736,246),(298,737,247),(298,738,248),(298,739,249),(298,740,250),(298,741,251),(298,742,252),(298,743,253),(298,744,254),(298,745,255),(298,746,256),(298,747,257),(298,748,258),(298,749,259),(298,750,260),(298,751,261),(298,752,262),(298,753,263),(298,755,264),(298,756,265),(298,757,266),(298,758,267),(298,759,268),(298,760,269),(298,761,270),(298,762,271),(298,763,272),(298,764,273),(298,765,274),(298,766,275),(298,767,276),(298,768,277),(298,769,278),(298,770,279),(298,771,280),(298,772,281),(298,773,282),(298,774,283),(298,775,284),(298,776,285),(298,777,286),(298,778,287),(298,779,288),(298,780,289),(298,781,290),(298,782,291),(298,783,292),(298,784,293),(298,785,294),(298,786,295),(298,787,296),(298,788,297),(298,789,298),(298,946,299),(298,338,300),(298,330,301),(298,945,302),(298,955,303),(298,952,304),(298,123,305),(298,276,306),(298,277,307),(298,271,308),(298,278,309),(298,279,310),(298,280,311),(298,281,312),(298,282,313),(298,283,314),(298,284,315),(298,285,316),(298,286,317),(298,287,318),(298,288,319),(298,289,320),(298,290,321),(298,291,322),(298,292,323),(298,293,324),(298,294,325),(298,295,326),(298,135,327),(298,262,328),(298,261,329),(298,298,330),(298,299,331),(298,300,332),(298,301,333),(298,302,334),(298,303,335),(298,304,336),(298,305,337),(298,306,338),(298,307,339),(298,169,340),(298,308,341),(298,192,342),(298,204,343),(298,245,344),(298,172,345),(298,458,346),(298,460,347),(298,461,348),(298,459,349),(298,447,350),(298,122,351),(298,165,352),(298,174,353),(298,214,354),(298,197,355),(298,143,356),(298,178,357),(298,187,358),(298,211,359),(298,257,360),(298,134,361),(298,144,362),(298,159,363),(298,258,364),(298,89,365),(298,97,366),(298,251,367),(298,95,368),(298,127,369),(298,100,370),(298,196,371),(298,210,372),(298,103,373),(298,234,374),(298,241,375),(298,138,376),(298,252,377),(298,166,378),(298,146,379),(298,239,380),(298,164,381),(298,129,382),(298,213,383),(298,217,384),(298,255,385),(298,132,386),(298,141,387),(298,236,388),(298,110,389),(298,953,390),(298,948,391),(298,949,392),(298,950,393),(298,943,394),(298,216,395),(298,380,396),(298,1000,397),(298,1001,398),(298,153,399),(298,202,400),(298,139,401),(298,1002,402),(298,1003,403),(298,225,404),(298,140,405),(298,186,406),(298,152,407),(298,243,408),(298,109,409),(298,156,410),(298,80,411),(298,232,412),(298,227,413),(298,203,414),(298,248,415),(298,238,416),(298,229,417),(298,161,418),(298,145,419),(298,105,420),(298,114,421),(298,212,422),(298,193,423),(298,128,424),(298,235,425),(298,244,426),(298,1004,427),(298,1005,428),(298,1006,429),(298,1007,430),(298,1008,431),(298,1009,432),(298,1010,433),(298,1011,434),(298,1012,435),(298,924,436),(298,891,437),(298,899,438),(298,889,439),(298,890,440),(298,881,441),(298,859,442),(298,869,443),(298,874,444),(298,873,445),(298,911,446),(298,390,447),(298,876,448),(298,929,449),(298,863,450),(298,925,451),(298,864,452),(298,895,453),(298,903,454),(298,877,455),(298,921,456),(298,393,457),(298,909,458),(298,861,459),(298,926,460),(298,901,461),(298,916,462),(298,865,463),(298,927,464),(298,897,465),(298,920,466),(298,884,467),(298,875,468),(298,905,469),(298,914,470),(298,871,471),(298,888,472),(298,883,473),(298,880,474),(298,913,475),(298,878,476),(298,908,477),(298,870,478),(298,98,479),(298,220,480),(298,343,481),(298,344,482),(298,345,483),(298,349,484),(298,350,485),(298,260,486),(298,917,487),(298,922,488),(298,173,489),(298,904,490),(298,351,491),(298,353,492),(298,354,493),(298,355,494),(298,357,495),(298,151,496),(298,358,497),(298,359,498),(298,360,499),(298,361,500),(298,362,501),(298,363,502),(298,364,503),(298,366,504),(298,185,505),(298,250,506),(298,373,507),(298,263,508),(298,188,509),(298,372,510),(298,371,511),(298,370,512),(298,369,513),(298,264,514),(298,367,515),(298,919,516),(298,892,517),(298,915,518),(298,872,519),(298,928,520),(298,866,521),(298,898,522),(298,894,523),(298,879,524),(298,882,525),(298,860,526),(298,893,527),(298,923,528),(298,118,529),(298,183,530),(298,265,531),(298,266,532),(298,267,533),(298,937,534),(298,446,535),(298,885,536),(298,862,537),(298,912,538),(298,902,539),(298,907,540),(298,887,541),(298,900,542),(298,896,543),(298,906,544),(298,868,545),(298,918,546),(298,910,547),(298,886,548),(298,867,549),(298,440,550),(298,400,551),(298,468,552),(298,469,553),(298,406,554),(298,470,555),(298,471,556),(298,472,557),(298,432,558),(298,473,559),(298,439,560),(298,474,561),(298,398,562),(298,399,563),(298,466,564),(298,404,565),(298,441,566),(298,475,567),(298,465,568),(298,476,569),(298,477,570),(298,401,571),(298,402,572),(298,467,573),(298,407,574),(298,408,575),(298,410,576),(298,411,577),(298,654,578),(298,313,579),(298,312,580),(298,309,581),(298,314,582),(298,944,583),(298,790,584),(298,198,585),(298,478,586),(298,449,587),(298,79,588),(298,272,589),(298,270,590),(298,296,591),(298,297,592),(298,754,593),(298,445,594),(298,437,595),(298,385,596),(298,388,597),(298,479,598),(298,480,599),(298,482,600),(298,389,601),(298,483,602),(298,484,603),(298,382,604),(298,386,605),(298,485,606),(298,486,607),(298,487,608),(298,384,609),(298,488,610),(298,381,611),(298,489,612),(298,490,613),(298,491,614),(298,481,615),(298,444,616),(298,442,617),(298,311,618),(298,492,619),(298,493,620),(298,346,621),(298,494,622),(298,453,623),(298,495,624),(298,496,625),(298,179,626),(298,191,627),(298,180,628),(298,497,629),(298,125,630),(298,84,631),(298,113,632),(298,226,633),(298,99,634),(298,205,635),(298,133,636),(298,112,637),(298,175,638),(298,111,639),(298,455,640),(298,456,641),(298,120,642),(298,254,643),(298,451,644),(298,160,645),(298,499,646),(298,268,647),(298,500,648),(298,501,649),(298,170,650),(298,387,651),(298,383,652),(298,315,653),(298,503,654),(298,356,655),(298,224,656),(298,221,657),(298,365,658),(298,209,659),(298,450,660),(298,317,661),(298,348,662),(298,33,663),(298,237,664),(298,206,665),(298,86,666),(298,342,667),(298,823,668),(298,454,669),(298,505,670),(298,506,671),(298,256,672),(298,526,673),(298,529,674),(298,531,675),(298,532,676),(298,533,677),(298,536,678),(298,537,679),(298,544,680),(298,545,681),(298,546,682),(298,548,683),(298,108,684),(298,837,685),(298,555,686),(298,556,687),(298,557,688),(298,558,689),(298,269,690),(298,550,691),(298,552,692),(298,553,693),(298,559,694),(298,554,695),(298,655,696),(298,347,697),(298,368,698),(298,352,699),(298,452,700),(298,829,701),(298,375,702),(298,376,703),(298,377,704),(298,378,705),(298,379,706),(298,374,707),(298,570,708),(298,571,709),(298,572,710),(298,573,711),(298,574,712),(298,575,713),(298,576,714),(298,577,715),(298,578,716),(298,579,717),(298,580,718),(298,116,719),(298,581,720),(298,316,721),(298,498,722),(298,582,723),(298,583,724),(298,584,725),(298,502,726),(298,585,727),(298,561,728),(298,814,729),(298,562,730),(298,512,731),(298,504,732),(298,528,733),(298,563,734),(298,521,735),(298,523,736),(298,522,737),(298,564,738),(298,541,739),(298,565,740),(298,195,741),(298,540,742),(298,560,743),(298,535,744),(298,538,745),(298,524,746),(298,525,747),(298,568,748),(298,569,749),(298,534,750),(298,567,751),(298,566,752),(298,530,753),(298,520,754),(298,834,755),(298,812,756),(298,835,757),(298,813,758),(298,820,759),(298,517,760),(298,510,761),(298,507,762),(298,508,763),(298,511,764),(298,509,765),(298,514,766),(298,513,767),(298,515,768),(298,516,769),(298,518,770),(298,676,771),(298,519,772),(298,551,773),(298,549,774),(298,547,775),(298,527,776),(298,539,777),(298,542,778),(298,543,779),(298,816,780),(298,817,781),(298,818,782),(298,815,783),(298,819,784),(298,821,785),(298,822,786),(298,824,787),(298,825,788),(298,826,789),(298,827,790),(298,828,791),(298,836,792),(298,830,793),(298,832,794),(298,833,795),(298,831,796),(327,844,0),(327,845,1),(327,846,2),(327,847,3),(327,842,4),(327,840,5),(327,843,6),(327,848,7),(327,849,8),(327,841,9),(327,839,10),(327,586,11),(327,587,12),(295,339,0),(295,336,1),(295,332,2),(295,66,3),(295,10,4),(295,35,5),(295,54,6),(295,28,7),(295,19,8),(295,42,9),(295,18,10),(295,36,11),(295,5,12),(295,29,13),(295,26,14),(295,3,15),(295,30,16),(295,47,17),(295,24,18),(295,7,19),(295,62,20),(295,1,21),(295,17,22),(295,60,23),(295,58,24),(295,34,25),(295,46,26),(295,15,27),(295,13,28),(295,25,29),(295,53,30),(295,67,31),(295,6,32),(295,65,33),(295,11,34),(295,71,35),(295,45,36),(295,50,37),(295,22,38),(295,2,39),(295,61,40),(295,72,41),(295,73,42),(295,74,43),(295,75,44),(295,76,45),(295,77,46),(295,78,47),(295,21,48),(295,14,49),(295,31,50),(295,59,51),(295,40,52),(295,37,53),(295,12,54),(295,56,55),(295,51,56),(295,9,57),(295,4,58),(295,43,59),(295,52,60),(295,55,61),(295,63,62),(295,8,63),(295,57,64),(295,69,65),(295,68,66),(295,32,67),(295,23,68),(295,48,69),(295,27,70),(295,44,71),(295,41,72),(295,20,73),(295,39,74),(295,16,75),(295,49,76),(295,70,77),(295,64,78),(295,38,79),(295,588,80),(295,589,81),(295,590,82),(295,463,83),(295,591,84),(295,464,85),(295,592,86),(295,593,87),(295,594,88),(295,443,89),(295,595,90),(295,596,91),(295,597,92),(295,598,93),(295,599,94),(295,310,95),(295,600,96),(295,601,97),(295,602,98),(295,603,99),(295,604,100),(295,605,101),(295,606,102),(295,607,103),(295,608,104),(295,609,105),(295,610,106),(295,611,107),(295,612,108),(295,613,109),(295,614,110),(295,615,111),(295,616,112),(295,617,113),(295,154,114),(295,618,115),(295,619,116),(295,620,117),(295,621,118),(295,622,119),(295,623,120),(295,624,121),(295,625,122),(295,626,123),(295,627,124),(295,628,125),(295,629,126),(295,630,127),(295,631,128),(295,632,129),(295,633,130),(295,634,131),(295,635,132),(295,636,133),(295,637,134),(295,638,135),(295,438,136),(295,418,137),(295,639,138),(295,640,139),(295,641,140),(295,448,141),(295,167,142),(295,642,143),(295,194,144),(295,119,145),(295,137,146),(295,148,147),(295,150,148),(295,643,149),(295,644,150),(295,645,151),(295,646,152),(295,647,153),(295,648,154),(295,649,155),(295,650,156),(295,651,157),(295,957,158),(295,958,159),(295,959,160),(295,960,161),(295,961,162),(295,962,163),(295,963,164),(295,964,165),(295,965,166),(295,966,167),(295,967,168),(295,968,169),(295,969,170),(295,970,171),(295,971,172),(295,972,173),(295,973,174),(295,974,175),(295,975,176),(295,976,177),(295,977,178),(295,978,179),(295,979,180),(295,980,181),(295,981,182),(295,982,183),(295,983,184),(295,984,185),(295,985,186),(295,986,187),(295,987,188),(295,988,189),(295,989,190),(295,656,191),(295,657,192),(295,658,193),(295,659,194),(295,660,195),(295,661,196),(295,662,197),(295,663,198),(295,664,199),(295,665,200),(295,666,201),(295,667,202),(295,668,203),(295,669,204),(295,670,205),(295,671,206),(295,672,207),(295,673,208),(295,674,209),(295,675,210),(295,677,211),(295,678,212),(295,679,213),(295,680,214),(295,681,215),(295,682,216),(295,683,217),(295,684,218),(295,685,219),(295,686,220),(295,687,221),(295,688,222),(295,689,223),(295,690,224),(295,691,225),(295,692,226),(295,693,227),(295,694,228),(295,695,229),(295,696,230),(295,697,231),(295,698,232),(295,699,233),(295,700,234),(295,701,235),(295,702,236),(295,802,237),(295,801,238),(295,803,239),(295,804,240),(295,805,241),(295,703,242),(295,704,243),(295,705,244),(295,706,245),(295,707,246),(295,708,247),(295,709,248),(295,710,249),(295,711,250),(295,712,251),(295,713,252),(295,714,253),(295,652,254),(295,653,255),(295,715,256),(295,716,257),(295,717,258),(295,718,259),(295,807,260),(295,806,261),(295,719,262),(295,720,263),(295,721,264),(295,722,265),(295,723,266),(295,724,267),(295,725,268),(295,726,269),(295,727,270),(295,728,271),(295,729,272),(295,730,273),(295,731,274),(295,732,275),(295,733,276),(295,734,277),(295,735,278),(295,736,279),(295,737,280),(295,738,281),(295,739,282),(295,740,283),(295,741,284),(295,742,285),(295,743,286),(295,744,287),(295,745,288),(295,746,289),(295,747,290),(295,748,291),(295,749,292),(295,750,293),(295,751,294),(295,752,295),(295,753,296),(295,755,297),(295,756,298),(295,757,299),(295,758,300),(295,759,301),(295,760,302),(295,761,303),(295,762,304),(295,763,305),(295,764,306),(295,765,307),(295,766,308),(295,767,309),(295,768,310),(295,769,311),(295,770,312),(295,771,313),(295,772,314),(295,773,315),(295,774,316),(295,775,317),(295,776,318),(295,777,319),(295,778,320),(295,779,321),(295,780,322),(295,781,323),(295,782,324),(295,783,325),(295,784,326),(295,785,327),(295,786,328),(295,787,329),(295,788,330),(295,789,331),(295,946,332),(295,274,333),(295,275,334),(295,318,335),(295,273,336),(295,323,337),(295,320,338),(295,321,339),(295,322,340),(295,319,341),(295,338,342),(295,337,343),(295,326,344),(295,335,345),(295,333,346),(295,334,347),(295,330,348),(295,327,349),(295,328,350),(295,329,351),(295,340,352),(295,324,353),(295,325,354),(295,341,355),(295,331,356),(295,945,357),(295,955,358),(295,952,359),(295,123,360),(295,276,361),(295,168,362),(295,131,363),(295,199,364),(295,83,365),(295,81,366),(295,189,367),(295,249,368),(295,231,369),(295,126,370),(295,200,371),(295,277,372),(295,271,373),(295,278,374),(295,279,375),(295,280,376),(295,281,377),(295,282,378),(295,283,379),(295,284,380),(295,285,381),(295,286,382),(295,287,383),(295,288,384),(295,289,385),(295,290,386),(295,291,387),(295,292,388),(295,293,389),(295,294,390),(295,91,391),(295,171,392),(295,107,393),(295,88,394),(295,242,395),(295,101,396),(295,295,397),(295,135,398),(295,262,399),(295,261,400),(295,298,401),(295,299,402),(295,300,403),(295,301,404),(295,302,405),(295,303,406),(295,304,407),(295,305,408),(295,306,409),(295,307,410),(295,169,411),(295,308,412),(295,192,413),(295,204,414),(295,245,415),(295,172,416),(295,458,417),(295,460,418),(295,461,419),(295,459,420),(295,447,421),(295,122,422),(295,165,423),(295,174,424),(295,214,425),(295,197,426),(295,143,427),(295,178,428),(295,187,429),(295,211,430),(295,257,431),(295,134,432),(295,144,433),(295,159,434),(295,258,435),(295,89,436),(295,97,437),(295,251,438),(295,95,439),(295,127,440),(295,100,441),(295,196,442),(295,210,443),(295,103,444),(295,234,445),(295,241,446),(295,138,447),(295,252,448),(295,166,449),(295,146,450),(295,239,451),(295,164,452),(295,129,453),(295,213,454),(295,217,455),(295,255,456),(295,132,457),(295,141,458),(295,236,459),(295,110,460),(295,953,461),(295,948,462),(295,949,463),(295,216,464),(295,380,465),(295,1000,466),(295,1001,467),(295,153,468),(295,202,469),(295,139,470),(295,1002,471),(295,1003,472),(295,225,473),(295,140,474),(295,186,475),(295,152,476),(295,243,477),(295,109,478),(295,156,479),(295,80,480),(295,232,481),(295,227,482),(295,203,483),(295,248,484),(295,238,485),(295,229,486),(295,161,487),(295,145,488),(295,105,489),(295,114,490),(295,212,491),(295,193,492),(295,128,493),(295,235,494),(295,244,495),(295,147,496),(295,208,497),(295,115,498),(295,93,499),(295,233,500),(295,184,501),(295,155,502),(295,163,503),(295,124,504),(295,162,505),(295,94,506),(295,102,507),(295,142,508),(295,218,509),(295,259,510),(295,247,511),(295,106,512),(295,181,513),(295,207,514),(295,201,515),(295,177,516),(295,82,517),(295,117,518),(295,130,519),(295,222,520),(295,136,521),(295,92,522),(295,149,523),(295,240,524),(295,421,525),(295,457,526),(295,420,527),(295,415,528),(295,394,529),(295,405,530),(295,414,531),(295,396,532),(295,403,533),(295,409,534),(295,413,535),(295,412,536),(295,419,537),(295,416,538),(295,417,539),(295,391,540),(295,422,541),(295,423,542),(295,395,543),(295,397,544),(295,85,545),(295,104,546),(295,246,547),(295,87,548),(295,157,549),(295,223,550),(295,253,551),(295,90,552),(295,215,553),(295,121,554),(295,230,555),(295,176,556),(295,433,557),(295,431,558),(295,426,559),(295,428,560),(295,429,561),(295,430,562),(295,427,563),(295,425,564),(295,436,565),(295,435,566),(295,434,567),(295,424,568),(295,462,569),(295,219,570),(295,392,571),(295,190,572),(295,228,573),(295,158,574),(295,96,575),(295,182,576),(295,944,577),(295,198,578),(295,478,579),(295,449,580),(295,79,581),(295,272,582),(295,270,583),(295,296,584),(295,297,585),(295,754,586),(295,311,587),(295,492,588),(295,453,589),(295,179,590),(295,191,591),(295,180,592),(295,125,593),(295,84,594),(295,113,595),(295,226,596),(295,99,597),(295,205,598),(295,133,599),(295,112,600),(295,175,601),(295,111,602),(295,455,603),(295,456,604),(295,120,605),(295,254,606),(295,451,607),(295,170,608),(295,503,609),(295,224,610),(295,221,611),(295,33,612),(295,237,613),(295,206,614),(295,86,615),(295,823,616),(295,454,617),(295,256,618),(295,837,619),(295,269,620),(295,655,621),(295,452,622),(295,829,623),(295,375,624),(295,376,625),(295,377,626),(295,378,627),(295,379,628),(295,374,629),(295,570,630),(295,571,631),(295,572,632),(295,573,633),(295,574,634),(295,575,635),(295,576,636),(295,577,637),(295,578,638),(295,579,639),(295,580,640),(295,116,641),(295,581,642),(295,834,643),(295,812,644),(295,835,645),(295,813,646),(295,820,647),(295,676,648),(326,845,0),(326,847,1),(326,842,2),(326,840,3),(326,843,4),(326,848,5),(225,503,0),(225,193,1),(225,152,2),(225,216,3),(225,243,4),(225,244,5),(225,1000,6),(225,80,7),(225,153,8),(225,156,9),(225,105,10),(225,221,11),(225,161,12),(225,128,13),(225,109,14),(225,248,15),(225,186,16),(225,202,17),(225,224,18),(225,203,19),(225,225,20),(225,112,21),(225,1002,22),(225,227,23),(225,139,24),(225,206,25),(225,114,26),(225,140,27),(225,229,28),(225,256,29),(225,232,30),(225,145,31),(225,1003,32),(225,235,33),(225,380,34),(225,237,35),(225,212,36),(225,238,37),(225,1001,38),(226,1004,0),(226,1006,1),(226,1011,2),(226,1010,3),(226,1008,4),(226,1012,5),(226,1009,6),(226,1005,7),(226,1007,8),(221,809,0),(221,808,1),(221,811,2),(221,838,3),(221,810,4),(228,474,0),(228,475,1),(228,472,2),(228,469,3),(228,473,4),(228,401,5),(228,477,6),(228,471,7),(228,476,8),(228,468,9),(228,398,10),(228,470,11),(228,399,12),(228,400,13),(228,402,14),(228,404,15),(228,406,16),(228,407,17),(228,408,18),(228,410,19),(228,411,20),(228,432,21),(228,439,22),(228,440,23),(228,441,24),(228,465,25),(228,466,26),(228,467,27),(220,667,0),(220,980,1),(220,698,2),(220,967,3),(220,668,4),(220,658,5),(220,979,6),(220,706,7),(220,725,8),(220,772,9),(220,775,10),(220,702,11),(220,665,12),(220,680,13),(220,970,14),(220,676,15),(220,739,16),(220,685,17),(220,741,18),(220,718,19),(220,659,20),(220,753,21),(220,669,22),(220,694,23),(220,995,24),(220,773,25),(220,736,26),(220,719,27),(220,699,28),(220,991,29),(220,690,30),(220,754,31),(220,670,32),(220,774,33),(220,708,34),(220,770,35),(220,787,36),(220,987,37),(220,728,38),(220,786,39),(220,963,40),(220,703,41),(220,688,42),(220,734,43),(220,726,44),(220,999,45),(220,788,46),(220,785,47),(220,968,48),(220,675,49),(220,975,50),(220,720,51),(220,653,52),(220,764,53),(220,686,54),(220,752,55),(220,727,56),(220,998,57),(220,704,58),(220,769,59),(220,747,60),(220,652,61),(220,984,62),(220,691,63),(220,661,64),(220,692,65),(220,729,66),(220,733,67),(220,730,68),(220,709,69),(220,997,70),(220,656,71),(220,751,72),(220,663,73),(220,674,74),(220,957,75),(220,780,76),(220,693,77),(220,756,78),(220,757,79),(220,743,80),(220,657,81),(220,983,82),(220,721,83),(220,711,84),(220,696,85),(220,771,86),(220,716,87),(220,748,88),(220,710,89),(220,762,90),(220,700,91),(220,689,92),(220,755,93),(220,962,94),(220,758,95),(220,722,96),(220,778,97),(220,681,98),(220,717,99),(220,713,100),(220,695,101),(220,971,102),(220,996,103),(220,966,104),(220,671,105),(220,750,106),(220,958,107),(220,761,108),(220,989,109),(220,964,110),(220,789,111),(220,731,112),(220,737,113),(220,679,114),(220,965,115),(220,783,116),(220,660,117),(220,990,118),(220,746,119),(220,732,120),(220,723,121),(220,972,122),(220,765,123),(220,684,124),(220,982,125),(220,697,126),(220,664,127),(220,712,128),(220,986,129),(220,760,130),(220,705,131),(220,742,132),(220,977,133),(220,672,134),(220,687,135),(220,974,136),(220,781,137),(220,766,138),(220,994,139),(220,714,140),(220,985,141),(220,959,142),(220,701,143),(220,749,144),(220,992,145),(220,735,146),(220,973,147),(220,759,148),(220,784,149),(220,978,150),(220,988,151),(220,976,152),(220,961,153),(220,682,154),(220,969,155),(220,993,156),(220,777,157),(220,673,158),(220,740,159),(220,662,160),(220,779,161),(220,715,162),(220,724,163),(220,683,164),(220,782,165),(220,745,166),(220,655,167),(220,677,168),(220,768,169),(220,666,170),(220,744,171),(220,738,172),(220,707,173),(220,981,174),(220,960,175),(220,776,176),(220,678,177),(220,767,178),(220,763,179),(220,801,180),(220,802,181),(220,803,182),(220,804,183),(220,805,184),(220,806,185),(220,807,186),(220,812,187),(220,813,188),(220,814,189),(220,796,190),(220,795,191),(220,797,192),(220,790,193),(220,850,194),(220,800,195),(220,798,196),(220,792,197),(220,851,198),(220,791,199),(220,852,200),(220,853,201),(220,854,202),(220,855,203),(220,794,204),(220,856,205),(220,857,206),(220,858,207),(220,799,208),(220,793,209),(220,654,210),(220,815,211),(220,816,212),(220,817,213),(220,818,214),(220,819,215),(220,820,216),(220,821,217),(220,822,218),(220,823,219),(220,824,220),(220,825,221),(220,826,222),(220,827,223),(220,828,224),(220,829,225),(220,830,226),(220,831,227),(220,832,228),(220,833,229),(220,834,230),(220,835,231),(220,836,232),(220,837,233),(322,839,0),(322,840,1),(322,841,2),(322,842,3),(322,843,4),(322,844,5),(322,845,6),(322,846,7),(322,847,8),(322,848,9),(322,849,10),(244,121,0),(244,215,1),(244,124,2),(244,176,3),(244,177,4),(244,218,5),(244,219,6),(244,82,7),(244,85,8),(244,181,9),(244,87,10),(244,182,11),(244,90,12),(244,223,13),(244,130,14),(244,222,15),(244,184,16),(244,92,17),(244,136,18),(244,93,19),(244,94,20),(244,228,21),(244,96,22),(244,230,23),(244,142,24),(244,190,25),(244,147,26),(244,233,27),(244,149,28),(244,240,29),(244,102,30),(244,155,31),(244,104,32),(244,157,33),(244,246,34),(244,158,35),(244,106,36),(244,247,37),(244,201,38),(244,162,39),(244,253,40),(244,163,41),(244,207,42),(244,208,43),(244,115,44),(244,259,45),(244,117,46),(244,391,47),(244,392,48),(244,394,49),(244,395,50),(244,396,51),(244,397,52),(244,403,53),(244,405,54),(244,409,55),(244,412,56),(244,413,57),(244,414,58),(244,415,59),(244,416,60),(244,417,61),(244,419,62),(244,420,63),(244,421,64),(244,422,65),(244,423,66),(244,424,67),(244,425,68),(244,426,69),(244,427,70),(244,428,71),(244,429,72),(244,430,73),(244,431,74),(244,433,75),(244,434,76),(244,435,77),(244,436,78),(244,457,79),(244,462,80),(275,309,0),(275,312,1),(275,313,2),(275,314,3),(275,316,4),(275,317,5),(275,347,6),(275,348,7),(275,352,8),(275,368,9),(275,498,10),(275,502,11),(275,504,12),(275,512,13),(275,520,14),(275,521,15),(275,522,16),(275,523,17),(275,524,18),(275,525,19),(275,528,20),(275,530,21),(275,534,22),(275,535,23),(275,538,24),(275,540,25),(275,541,26),(275,547,27),(275,549,28),(275,560,29),(275,585,30),(275,561,31),(275,562,32),(275,563,33),(275,564,34),(275,565,35),(275,566,36),(275,567,37),(275,568,38),(275,569,39),(275,582,40),(275,583,41),(275,584,42),(331,527,0),(331,529,1),(331,531,2),(331,532,3),(331,533,4),(331,536,5),(331,537,6),(331,539,7),(331,542,8),(331,543,9),(331,544,10),(331,545,11),(331,546,12),(331,548,13);
/*!40000 ALTER TABLE `script_group_script_file` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `script_rdkversions`
--

DROP TABLE IF EXISTS `script_rdkversions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `script_rdkversions` (
  `script_rdk_versions_id` bigint(20) DEFAULT NULL,
  `rdkversions_id` bigint(20) DEFAULT NULL,
  KEY `FKC95104A078CFB00` (`script_rdk_versions_id`),
  KEY `FKC95104A0D247002A` (`rdkversions_id`),
  CONSTRAINT `FKC95104A078CFB00` FOREIGN KEY (`script_rdk_versions_id`) REFERENCES `script` (`id`),
  CONSTRAINT `FKC95104A0D247002A` FOREIGN KEY (`rdkversions_id`) REFERENCES `rdkversions` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;



--
-- Table structure for table `socvendor`
--

DROP TABLE IF EXISTS `socvendor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `socvendor` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `version` bigint(20) NOT NULL,
  `name` varchar(255) NOT NULL,
  `groups_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `FKE987E18F984B586A` (`groups_id`),
  CONSTRAINT `FKE987E18F984B586A` FOREIGN KEY (`groups_id`) REFERENCES `groups` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `socvendor`
--

LOCK TABLES `socvendor` WRITE;
/*!40000 ALTER TABLE `socvendor` DISABLE KEYS */;
INSERT INTO `socvendor` VALUES (1,0,'Parker',NULL),(2,0,'Px001bn',NULL),(3,0,'Rng150',NULL),(4,0,'Intel',NULL),(5,0,'Broadcom – MIPS',NULL),(6,0,'Broadcom - ARM',NULL);
/*!40000 ALTER TABLE `socvendor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `streaming_details`
--

DROP TABLE IF EXISTS `streaming_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `streaming_details` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `version` bigint(20) NOT NULL,
  `audio_format` varchar(255) NOT NULL,
  `channel_type` varchar(255) NOT NULL,
  `stream_id` varchar(64) NOT NULL,
  `video_format` varchar(255) NOT NULL,
  `gateway_ip` varchar(255) DEFAULT NULL,
  `ocap_id` varchar(255) DEFAULT NULL,
  `recorder_id` varchar(255) DEFAULT NULL,
  `groups_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `stream_id` (`stream_id`),
  KEY `FKD3332F65984B586A` (`groups_id`),
  CONSTRAINT `FKD3332F65984B586A` FOREIGN KEY (`groups_id`) REFERENCES `groups` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `streaming_details`
--

LOCK TABLES `streaming_details` WRITE;
/*!40000 ALTER TABLE `streaming_details` DISABLE KEYS */;
INSERT INTO `streaming_details` VALUES (4,14,'ac3','SD','01','mpeg2',NULL,NULL,NULL,NULL),(5,3,'ac3','HD','02','mpeg4',NULL,NULL,NULL,NULL),(6,4,'aac','SD','03','mpeg2',NULL,NULL,NULL,NULL),(7,4,'aac','HD','04','mpeg4',NULL,NULL,NULL,NULL),(8,1,'mp3','HD','05','mpeg2',NULL,NULL,NULL,NULL),(9,1,'mp3','HD','06','mpeg4',NULL,NULL,NULL,NULL),(10,1,'wav','HD','07','mpeg2',NULL,NULL,NULL,NULL),(11,1,'wav','HD','08','mpeg4',NULL,NULL,NULL,NULL),(12,1,'ac3','HD','09','h264',NULL,NULL,NULL,NULL),(13,1,'aac','HD','10','h264',NULL,NULL,NULL,NULL),(14,1,'mp3','HD','11','h264',NULL,NULL,NULL,NULL),(15,2,'wav','HD','12','h264',NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `streaming_details` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `third_party_execution_details`
--

DROP TABLE IF EXISTS `third_party_execution_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `third_party_execution_details` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `version` bigint(20) NOT NULL,
  `box_type` varchar(255) DEFAULT NULL,
  `callback_url` varchar(255) DEFAULT NULL,
  `exec_name` varchar(255) DEFAULT NULL,
  `execution_id` bigint(20) DEFAULT NULL,
  `execution_start_time` bigint(20) NOT NULL,
  `file_path` varchar(255) DEFAULT NULL,
  `image_name` varchar(255) DEFAULT NULL,
  `url` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `FKA7A4E82A8358C58A` (`execution_id`),
  CONSTRAINT `FKA7A4E82A8358C58A` FOREIGN KEY (`execution_id`) REFERENCES `execution` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;



--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `version` bigint(20) NOT NULL,
  `email` varchar(255) NOT NULL,
  `group_name_id` bigint(20) DEFAULT NULL,
  `name` varchar(255) NOT NULL,
  `password_hash` varchar(255) DEFAULT NULL,
  `status` varchar(255) DEFAULT NULL,
  `username` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  KEY `FK36EBCB5A529693` (`group_name_id`),
  CONSTRAINT `FK36EBCB5A529693` FOREIGN KEY (`group_name_id`) REFERENCES `groups` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,1,'sreejasuma@tataelxsi.co.in',NULL,'ADMINISTRATOR','5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8',NULL,'admin');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_group`
--

DROP TABLE IF EXISTS `user_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_group` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `version` bigint(20) NOT NULL,
  `group_manager_id` bigint(20) NOT NULL,
  `group_name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `FK72A9010B3C9C6FA8` (`group_manager_id`),
  CONSTRAINT `FK72A9010B3C9C6FA8` FOREIGN KEY (`group_manager_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_group`
--

LOCK TABLES `user_group` WRITE;
/*!40000 ALTER TABLE `user_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_group_user`
--

DROP TABLE IF EXISTS `user_group_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_group_user` (
  `user_group_users_id` bigint(20) DEFAULT NULL,
  `user_id` bigint(20) DEFAULT NULL,
  KEY `FK9C06927F5976FFAA` (`user_group_users_id`),
  KEY `FK9C06927F4A160D0A` (`user_id`),
  CONSTRAINT `FK9C06927F4A160D0A` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `FK9C06927F5976FFAA` FOREIGN KEY (`user_group_users_id`) REFERENCES `user_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_group_user`
--

LOCK TABLES `user_group_user` WRITE;
/*!40000 ALTER TABLE `user_group_user` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_group_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_permissions`
--

DROP TABLE IF EXISTS `user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_permissions` (
  `user_id` bigint(20) DEFAULT NULL,
  `permissions_string` varchar(255) DEFAULT NULL,
  KEY `FKE693E6104A160D0A` (`user_id`),
  CONSTRAINT `FKE693E6104A160D0A` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_permissions`
--

LOCK TABLES `user_permissions` WRITE;
/*!40000 ALTER TABLE `user_permissions` DISABLE KEYS */;
INSERT INTO `user_permissions` VALUES (1,'*:*');
/*!40000 ALTER TABLE `user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_roles`
--

DROP TABLE IF EXISTS `user_roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_roles` (
  `user_id` bigint(20) NOT NULL,
  `role_id` bigint(20) NOT NULL,
  PRIMARY KEY (`user_id`,`role_id`),
  KEY `FK73429949A4EB492A` (`role_id`),
  KEY `FK734299494A160D0A` (`user_id`),
  CONSTRAINT `FK734299494A160D0A` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `FK73429949A4EB492A` FOREIGN KEY (`role_id`) REFERENCES `role` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_roles`
--

LOCK TABLES `user_roles` WRITE;
/*!40000 ALTER TABLE `user_roles` DISABLE KEYS */;
INSERT INTO `user_roles` VALUES (1,1),(2,1),(5,1),(6,1);
/*!40000 ALTER TABLE `user_roles` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2014-11-01  1:38:43
