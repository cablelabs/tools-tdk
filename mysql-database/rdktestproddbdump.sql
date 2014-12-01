-- MySQL dump 10.13  Distrib 5.5.34, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: rdktesttoolproddb
-- ------------------------------------------------------
-- Server version	5.5.34-0ubuntu0.13.04.1

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
-- Dumping data for table `box_model`
--

LOCK TABLES `box_model` WRITE;
/*!40000 ALTER TABLE `box_model` DISABLE KEYS */;
/*!40000 ALTER TABLE `box_model` ENABLE KEYS */;
UNLOCK TABLES;

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
) ENGINE=InnoDB AUTO_INCREMENT=6486 DEFAULT CHARSET=latin1;
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
) ENGINE=InnoDB AUTO_INCREMENT=24585 DEFAULT CHARSET=latin1;
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
  CONSTRAINT `FK81A39F8D3DFB26A5` FOREIGN KEY (`stream_id`) REFERENCES `radio_streaming_details` (`id`),
  CONSTRAINT `FK81A39F8DEC4FF12A` FOREIGN KEY (`device_id`) REFERENCES `device` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=63 DEFAULT CHARSET=latin1;
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
) ENGINE=InnoDB AUTO_INCREMENT=1381 DEFAULT CHARSET=latin1;
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
) ENGINE=InnoDB AUTO_INCREMENT=307962 DEFAULT CHARSET=latin1;
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
) ENGINE=InnoDB AUTO_INCREMENT=6471 DEFAULT CHARSET=latin1;
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
) ENGINE=InnoDB AUTO_INCREMENT=6421 DEFAULT CHARSET=latin1;
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
) ENGINE=InnoDB AUTO_INCREMENT=46328 DEFAULT CHARSET=latin1;
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
) ENGINE=InnoDB AUTO_INCREMENT=512 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `function`
--

LOCK TABLES `function` WRITE;
/*!40000 ALTER TABLE `function` DISABLE KEYS */;
INSERT INTO `function` VALUES (18,0,8,'TestMgr_IARMBUS_Init'),(19,0,8,'TestMgr_IARMBUS_Connect'),(20,0,8,'TestMgr_IARMBUS_Disconnect'),(21,0,8,'TestMgr_IARMBUS_Term'),(22,0,8,'TestMgr_IARMBUS_BusCall'),(24,0,8,'TestMgr_IARMBUS_RegisterCall'),(25,0,8,'TestMgr_IARMBUS_RequestResource'),(26,0,8,'TestMgr_IARMBUS_ReleaseResource'),(29,0,8,'TestMgr_IARMBUS_BroadcastEvent'),(30,0,8,'TestMgr_IARMBUS_InvokeSecondApplication'),(31,0,8,'TestMgr_IARMBUS_RegisterEventHandler'),(32,0,8,'TestMgr_IARMBUS_UnRegisterEventHandler'),(37,0,8,'TestMgr_IARMBUS_IsConnected'),(38,0,8,'TestMgr_IARMBUS_RegisterEvent'),(40,0,8,'TestMgr_IARMBUS_GetContext'),(41,0,8,'TestMgr_IARMBUS_GetLastReceivedEventDetails'),(74,0,24,'TestMgr_Opensource_Test_Execute'),(75,0,25,'TestMgr_DS_FP_setColor'),(76,0,25,'TestMgr_DS_managerInitialize'),(77,0,25,'TestMgr_DS_managerDeinitialize'),(78,0,25,'TestMgr_DS_FP_setBrightness'),(79,0,25,'TestMgr_DS_FP_setBlink'),(80,0,25,'TestMgr_DS_FP_setScroll'),(81,0,25,'TestMgr_DS_AOP_setLevel'),(82,0,25,'TestMgr_DS_AOP_setDB'),(83,0,25,'TestMgr_DS_VD_setDFC'),(84,0,25,'TestMgr_DS_AOP_setEncoding'),(85,0,25,'TestMgr_DS_AOP_setCompression'),(86,0,25,'TestMgr_DS_AOP_setStereoMode'),(87,0,25,'TestMgr_DS_HOST_setPowerMode'),(88,0,25,'TestMgr_DS_VOP_setResolution'),(89,0,25,'TestMgr_DS_FP_getIndicators'),(90,0,25,'TestMgr_DS_FP_FP_getSupportedColors'),(91,0,25,'TestMgr_DS_FP_getTextDisplays'),(92,0,25,'TestMgr_DS_FP_setText'),(93,0,25,'TestMgr_DS_FP_setTimeForamt'),(94,0,25,'TestMgr_DS_FP_setTime'),(95,0,25,'TestMgr_DS_AOP_loopThru'),(96,0,25,'TestMgr_DS_AOP_mutedStatus'),(97,0,25,'TestMgr_DS_AOP_getSupportedEncodings'),(98,0,25,'TestMgr_DS_AOP_getSupportedCompressions'),(99,0,25,'TestMgr_DS_AOP_getSupportedStereoModes'),(100,0,25,'TestMgr_DS_HOST_addPowerModeListener'),(101,0,25,'TestMgr_DS_HOST_removePowerModeListener'),(102,0,25,'TestMgr_DS_HOST_Resolutions'),(103,0,25,'TestMgr_DS_VOPTYPE_HDCPSupport'),(104,0,25,'TestMgr_DS_VOPTYPE_DTCPSupport'),(105,0,25,'TestMgr_DS_VOP_getAspectRatio'),(106,0,25,'TestMgr_DS_VOP_getDisplayDetails'),(107,0,25,'TestMgr_DS_VOPTYPE_isDynamicResolutionSupported'),(108,0,22,'TestMgr_MediaStreamer_LiveTune_Request'),(110,0,22,'TestMgr_MediaStreamer_Recorded_Urls'),(111,0,22,'TestMgr_MediaStreamer_Recorded_Metadata'),(112,0,22,'TestMgr_MediaStreamer_Live_Playback'),(113,0,22,'TestMgr_MediaStreamer_Recording_Playback'),(115,0,22,'TestMgr_MediaStreamer_DVR_Trickplay'),(117,0,25,'TestMgr_DS_VOP_isContentProtected'),(118,0,25,'TestMgr_DS_VOP_isDisplayConnected'),(122,0,25,'TestMgr_DS_HOST_addDisplayConnectionListener'),(123,0,25,'TestMgr_DS_HOST_removeDisplayConnectionListener'),(124,0,27,'TestMgr_SM_RegisterService'),(125,0,27,'TestMgr_SM_UnRegisterService'),(126,0,27,'TestMgr_SM_DoesServiceExist'),(128,0,22,'TestMgr_MediaStreamer_Recording_Request'),(129,0,27,'TestMgr_SM_GetRegisteredServices'),(142,0,39,'TestMgr_rmfapp_Test_Execute'),(149,0,27,'TestMgr_SM_GetGlobalService'),(150,0,27,'TestMgr_SM_HN_EnableMDVR'),(151,0,27,'TestMgr_SM_HN_EnableVPOP'),(152,0,27,'TestMgr_SM_HN_SetDeviceName'),(153,0,27,'TestMgr_SM_SetAPIVersion'),(154,0,27,'TestMgr_SM_RegisterForEvents'),(156,0,27,'TestMgr_SM_DisplaySetting_SetZoomSettings'),(157,0,27,'TestMgr_SM_DisplaySetting_SetCurrentResolution'),(158,0,35,'TestMgr_CC_Init'),(164,0,35,'TestMgr_CC_SetGetDigitalChannel'),(166,0,35,'TestMgr_CC_SetGetAnalogChannel'),(167,0,35,'TestMgr_CC_Show'),(168,0,35,'TestMgr_CC_Hide'),(173,0,35,'TestMgr_CC_SetGetAttribute'),(174,0,35,'TestMgr_CC_GetSupportedServiceNumberCount'),(175,0,35,'TestMgr_CC_GetSupportedServiceNumber'),(177,0,35,'TestMgr_CC_SetGetState'),(179,0,35,'TestMgr_CC_OnEasStart'),(180,0,35,'TestMgr_CC_OnEasStop'),(181,0,35,'TestMgr_CC_ResetTrickPlayStatus'),(182,0,35,'TestMgr_CC_SetTrickPlayStatus'),(192,0,42,'TestMgr_newrmf_Appplay'),(201,0,44,'TestMgr_MPSink_SetGetMute'),(202,0,44,'TestMgr_MPSink_SetGetVolume'),(207,0,44,'TestMgr_HNSrc_GetBufferedRanges'),(208,0,44,'TestMgr_HNSrc_GetState'),(211,0,44,'TestMgr_HNSrcMPSink_Video_Pause'),(212,0,44,'TestMgr_MPSink_InitTerm'),(216,0,44,'TestMgr_HNSrcMPSink_Video_Speed'),(223,0,44,'TestMgr_HNSrcMPSink_Video_Play'),(224,0,44,'TestMgr_HNSrcMPSink_Video_State'),(227,0,44,'TestMgr_HNSrcMPSink_Video_Skip_Backward'),(230,0,44,'TestMgr_HNSrcMPSink_Video_Volume'),(231,0,44,'TestMgr_HNSrcMPSink_Video_Play_Position'),(232,0,44,'TestMgr_HNSrcMPSink_Video_MuteUnmute'),(270,0,44,'TestMgr_DVRSink_init_term'),(277,0,51,'TestMgr_RDKLogger_Dbg_Enabled_Status'),(278,0,51,'TestMgr_RDKLogger_EnvGet'),(279,0,51,'TestMgr_RDKLogger_EnvGetNum'),(280,0,51,'TestMgr_RDKLogger_EnvGetValueFromNum'),(281,0,51,'TestMgr_RDKLogger_EnvGetModFromNum'),(282,0,51,'TestMgr_RDKLogger_Init'),(283,0,51,'TestMgr_RDKLogger_Log'),(285,0,44,'TestMgr_QAMSource_Play'),(292,0,44,'TestMgr_QAMSource_InitTerm'),(293,0,44,'TestMgr_QAMSource_OpenClose'),(294,0,44,'TestMgr_QAMSource_Pause'),(295,0,44,' TestMgr_QAMSource_GetTsId'),(296,0,44,'TestMgr_QAMSource_GetLtsId'),(297,0,44,'TestMgr_QAMSource_GetQAMSourceInstance'),(298,0,44,'TestMgr_QAMSource_Init_Uninit_Platform'),(299,0,44,'TestMgr_QAMSource_GetUseFactoryMethods'),(300,0,44,'TestMgr_QAMSource_Get_Free_LowLevelElement'),(301,0,44,'TestMgr_QAMSource_ChangeURI'),(302,0,44,'TestMgr_DVRManager_GetSpace'),(303,0,44,'TestMgr_DVRManager_GetRecordingCount'),(304,0,44,'TestMgr_DVRManager_GetRecordingInfoByIndex'),(305,0,44,'TestMgr_DVRManager_GetRecordingInfoById'),(306,0,44,'TestMgr_DVRManager_GetIsRecordingInProgress'),(307,0,44,'TestMgr_DVRManager_GetRecordingSize'),(308,0,44,'TestMgr_DVRManager_GetRecordingDuration'),(309,0,44,'TestMgr_DVRManager_GetRecordingStartTime'),(310,0,44,'TestMgr_DVRManager_GetDefaultTSBMaxDuration'),(311,0,44,'TestMgr_DVRManager_CreateTSB'),(312,0,44,'TestMgr_DVRManager_CreateRecording'),(313,0,44,'TestMgr_DVRManager_UpdateRecording'),(314,0,44,'TestMgr_DVRManager_DeleteRecording'),(315,0,44,'TestMgr_DVRManager_GetSegmentsCount'),(316,0,44,'TestMgr_DVRManager_ConvertTSBToRecording'),(317,0,44,'TestMgr_DVRManager_GetRecordingSegmentInfoByIndex'),(350,0,22,'TestMgr_RMFStreamer_InterfaceTesting'),(351,0,22,'TestMgr_RMFStreamer_Player'),(353,0,44,'TestMgr_DVR_Rec_List'),(354,0,44,'TestMgr_RmfElementCreateInstance'),(355,0,44,'TestMgr_RmfElementInit'),(356,0,44,'TestMgr_RmfElementTerm'),(357,0,44,'TestMgr_RmfElementOpen'),(358,0,44,'TestMgr_RmfElementClose'),(359,0,44,'TestMgr_RmfElementRemoveInstance'),(360,0,44,'TestMgr_RmfElementPlay'),(361,0,44,'TestMgr_RmfElement_Sink_SetSource'),(362,0,44,'TestMgr_RmfElement_MpSink_SetVideoRectangle'),(363,0,44,'TestMgr_RmfElementSetSpeed'),(364,0,44,'TestMgr_RmfElementGetSpeed'),(365,0,44,'TestMgr_RmfElementGetMediaTime'),(366,0,44,'TestMgr_RmfElementGetState'),(367,0,44,'TestMgr_RmfElementPause'),(368,0,44,'TestMgr_RmfElementSetMediaTime'),(369,0,44,'TestMgr_RmfElementGetMediaInfo'),(370,0,57,'Xi4Init'),(371,0,58,'TestMgr_Recorder_ScheduleRecording'),(372,0,58,'TestMgr_Recorder_checkRecording_status'),(373,0,44,'TestMgr_DVRManager_CheckRecordingInfoById'),(374,0,44,'TestMgr_DVRManager_CheckRecordingInfoByIndex'),(375,0,59,'TestMgr_HybridE2E_T2pTuning'),(376,0,59,'TestMgr_HybridE2E_T2pTrickMode'),(378,0,59,'TestMgr_E2EStub_PlayURL'),(379,0,59,'TestMgr_E2EStub_GetRecURLS'),(380,0,59,'TestMgr_E2ELinearTV_GetURL'),(381,0,59,'TestMgr_E2ELinearTV_PlayURL'),(382,0,59,'TestMgr_Dvr_Play_Pause'),(383,0,59,'TestMgr_Dvr_Play_TrickPlay_FF_FR'),(384,0,59,'TestMgr_LinearTv_Dvr_Play'),(385,0,59,'TestMgr_Dvr_Play_TrickPlay_RewindFromEndPoint'),(386,0,59,'TestMgr_Dvr_Pause_Play'),(387,0,59,'TestMgr_Dvr_Play_Pause_Play'),(388,0,59,'TestMgr_Dvr_Play_Pause_Play_Repeat'),(389,0,59,'TestMgr_Dvr_Skip_Forward_Play'),(390,0,59,'TestMgr_Dvr_Skip_Forward_From_Middle'),(391,0,59,'TestMgr_Dvr_Skip_Forward_From_End'),(392,0,59,'TestMgr_Dvr_Skip_Backward_From_End'),(393,0,59,'TestMgr_Dvr_Skip_Backward_From_Middle'),(394,0,59,'TestMgr_Dvr_Skip_Backward_From_Starting'),(395,0,59,'TestMgr_Dvr_Play_Rewind_Forward'),(396,0,59,'TestMgr_Dvr_Play_Forward_Rewind'),(397,0,59,'TestMgr_Dvr_Play_FF_FR_Pause_Play'),(398,0,59,'TestMgr_Dvr_Play_Pause_FF_FR'),(399,0,59,'TestMgr_Dvr_Play_Pause_Play_SF_SB'),(400,0,59,'TestMgr_Dvr_Play_FF_FR_SF_SB'),(401,0,59,'TestMgr_Dvr_Play_Pause_Pause'),(402,0,59,'TestMgr_Dvr_Play_Play'),(403,0,59,'TestMgr_LiveTune_GETURL'),(404,0,59,'TestMgr_RF_Video_ChannelChange'),(405,0,44,'TestMgr_RmfElement_DVRManagerCreateRecording'),(407,0,44,'TestMgr_RmfElement_QAMSrc_RmfPlatform_Init'),(408,0,44,'TestMgr_RmfElement_QAMSrc_RmfPlatform_Uninit'),(409,0,44,'TestMgr_RmfElement_QAMSrc_InitPlatform'),(410,0,44,'TestMgr_RmfElement_QAMSrc_UninitPlatform'),(412,0,44,'TestMgr_RmfElement_QAMSrc_GetTSID'),(413,0,44,'TestMgr_RmfElement_QAMSrc_GetLTSID'),(414,0,44,'TestMgr_RmfElement_QAMSrc_GetLowLevelElement'),(415,0,44,'TestMgr_RmfElement_QAMSrc_FreeLowLevelElement'),(416,0,44,'TestMgr_RmfElement_QAMSrc_ChangeURI'),(417,0,44,'TestMgr_RmfElement_QAMSrc_UseFactoryMethods'),(418,0,44,'TestMgr_RmfElement_HNSink_InitPlatform'),(419,0,44,'TestMgr_RmfElement_HNSink_UninitPlatform'),(420,0,44,'TestMgr_RmfElement_HNSink_SetProperties'),(421,0,44,'TestMgr_RmfElement_HNSink_SetSourceType'),(422,0,59,'TestMgr_TSB_Play'),(424,0,39,'TestMgr_CreateRecord'),(425,0,59,'TestMgr_MDVR_Record_Play'),(426,0,59,'TestMgr_MDVR_GetResult'),(427,0,60,'TestMgr_GetParameterValue'),(429,0,51,'TestMgr_RDKLogger_Log_All'),(431,0,51,'TestMgr_RDKLogger_Log_InverseTrace'),(432,0,51,'TestMgr_RDKLogger_Log_Msg'),(433,0,51,'TestMgr_RDKLogger_Log_None'),(434,0,51,'TestMgr_RDKLogger_Log_Trace'),(437,0,51,'TestMgr_RDKLogger_CheckMPELogEnabled'),(438,0,60,'TestMgr_VerifyParameterValue'),(440,0,51,'TestMgr_RDKLogger_SetLogLevel'),(441,0,51,'TestMgr_RDKLogger_GetLogLevel'),(442,0,44,'TestMgr_HNSrc_GetBufferedRanges'),(443,0,61,'TestMgr_Aesdecrypt_DecryptEnable_Prop'),(445,0,62,'TestMgr_TRM_GetAllTunerStates'),(446,0,62,'TestMgr_TRM_GetAllTunerIds'),(447,0,62,'TestMgr_TRM_GetAllReservations'),(448,0,62,'TestMgr_TRM_GetVersion'),(449,0,61,'TestMgr_Aesdecrypt_DecryptEnable_Get_Prop'),(450,0,61,'TestMgr_Aesencrypt_EncryptEnable_Set_Prop'),(453,0,61,'TestMgr_Aesencrypt_EncryptEnable_Get_Prop'),(454,0,61,'TestMgr_Dvrsrc_RecordId_Set_Prop'),(455,0,61,'TestMgr_Dvrsrc_RecordId_Get_Prop'),(456,0,61,'TestMgr_Dvrsrc_SegmentName_Set_Prop'),(457,0,61,'TestMgr_Dvrsrc_SegmentName_Get_Prop'),(458,0,61,'TestMgr_Dvrsrc_Ccivalue_Get_Prop'),(459,0,61,'TestMgr_Dvrsrc_Rate_Set_Prop'),(460,0,62,'TestMgr_TRM_TunerReserveForRecord'),(461,0,62,'TestMgr_TRM_TunerReserveForLive'),(462,0,61,'TestMgr_Dvrsrc_Rate_Get_Prop'),(463,0,61,'TestMgr_Dvrsrc_StartTime_Get_Prop'),(464,0,61,'TestMgr_Dvrsrc_Duration_Get_Prop'),(465,0,61,'TestMgr_Dvrsrc_PlayStartPosition_Set_Prop'),(466,0,61,'TestMgr_Dvrsrc_PlayStartPosition_Get_Prop'),(467,0,61,'TestMgr_Dvrsink_RecordId_Set_Prop'),(468,0,61,'TestMgr_Dvrsink_RecordId_Get_Prop'),(469,0,61,'TestMgr_Dvrsink_Ccivalue_Get_Prop'),(470,0,61,'TestMgr_Dvrsrc_RecordId_Get_Prop'),(471,0,61,'TestMgr_Dvrsrc_SegmentName_Set_Prop'),(472,0,61,'TestMgr_Dvrsrc_SegmentName_Set_Prop'),(474,0,62,'TestMgr_TRM_ReleaseTunerReservation'),(475,0,62,'TestMgr_TRM_ValidateTunerReservation'),(476,0,62,'TestMgr_TRM_CancelRecording'),(477,0,62,'TestMgr_TRM_CancelLive'),(481,0,27,'TestMgr_SM_DeviceSetting_GetDeviceInfo'),(482,0,27,'TestMgr_SM_ScreenCapture_Upload'),(483,0,27,'TestMgr_SM_WebSocket_GetUrl'),(484,0,27,'TestMgr_SM_WebSocket_GetReadyState'),(485,0,27,'TestMgr_SM_WebSocket_GetBufferedAmount'),(486,0,27,'TestMgr_SM_WebSocket_GetProtocol'),(487,0,27,'TestMgr_SM_GetSetting'),(488,0,27,'TestMgr_SM_CreateService'),(489,0,27,'TestMgr_Services_GetName'),(490,0,44,'TestMgr_RmfElement_CheckForSPTSRead_QAMSrc_Error'),(491,0,25,'TestMgr_DS_FP_setState'),(492,0,25,'TestMgr_DS_VOP_setEnable'),(495,0,44,'TestMgr_CheckAudioVideoStatus'),(497,0,64,'TestMgr_DTCPAgent_Init'),(498,0,65,'TestMgr_XUPNPAgent_checkjson'),(499,0,65,'TestMgr_XUPNPAgent_checkSTRurl'),(500,0,65,'TestMgr_XUPNPAgent_checkSerialNo'),(501,0,65,'TestMgr_XUPNPAgent_checkPBurl'),(502,0,65,'TestMgr_XUPNPAgent_recordId'),(503,0,65,'TestMgr_XUPNPAgent_ModBasicDevice'),(504,0,65,'TestMgr_XUPNPAgent_removeXmls'),(505,0,65,'TestMgr_XUPNPAgent_evtCheck'),(506,0,44,'TestMgr_CheckRmfStreamerCrash'),(507,0,44,'TestMgr_ClearLogFile'),(508,0,44,'TestMgr_DVR_CreateNewRecording'),(509,0,62,'TestMgr_TRM_ReleaseTunerReservation'),(510,0,44,'TestMgr_CommentScirptForQam'),(511,0,44,'TestMgr_UnCommentScirptForQam');
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
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=latin1;
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
INSERT INTO `module` VALUES (8,8,'iarmbus','1.2','Component',NULL,3),(22,4,'mediastreamer','1.2','Component',NULL,3),(24,2,'openSource_components','1.2','OpenSource',NULL,60),(25,5,'devicesettings','1.2','Component',NULL,3),(27,2,'servicemanager','1.3','Component',NULL,2),(35,2,'closedcaption','1.2','Component',NULL,1),(39,2,'rmfapp','2.0','E2E',NULL,5),(42,2,'newrmf','RDK2.0','Component',NULL,5),(44,3,'mediaframework','2.0','Component',NULL,3),(51,2,'rdk_logger','2.0','Component',NULL,5),(57,1,'Xi4Module1','2.1','Component',NULL,2),(58,2,'recorder','2.0','Component',NULL,10),(59,3,'tdk_integration','1.3','E2E',NULL,5),(60,1,'tr69','1','Component',NULL,5),(61,1,'gst-plugins-rdk','1','Component',NULL,5),(62,1,'trm','1','Component',NULL,10),(64,1,'dtcp','1','Component',NULL,5),(65,1,'xupnp','1','Component',NULL,7);
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
INSERT INTO `module_log_file_names` VALUES (8,'/opt/logs/uimgr_log.txt'),(22,'/opt/logs/ocapri_log.txt'),(59,'/opt/logs/ocapri_log.txt'),(25,'/opt/logs/uimgr_log.txt'),(58,'/opt/logs/ocapri_log.txt');
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
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
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
) ENGINE=InnoDB AUTO_INCREMENT=781 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `parameter_type`
--

LOCK TABLES `parameter_type` WRITE;
/*!40000 ALTER TABLE `parameter_type` DISABLE KEYS */;
INSERT INTO `parameter_type` VALUES (20,0,18,'Process_name','STRING','A-Z'),(21,0,22,'owner_name','STRING','A-Z'),(22,0,22,'method_name','STRING','A-Z'),(24,0,22,'set_timeout','INTEGER','1-65535'),(25,0,22,'newState','INTEGER','0-2'),(26,0,22,'resource_type','INTEGER','0-7'),(27,0,24,'owner_name','STRING','A-Z'),(29,0,25,'resource_type','INTEGER','0-7'),(30,0,26,'resource_type','INTEGER','0-7'),(34,0,29,'event_id','INTEGER','0-2'),(35,0,29,'owner_name','STRING','A-Z'),(37,0,29,'keyType','INTEGER','1-65535'),(38,0,29,'keyCode','INTEGER','1-65535'),(39,0,29,'newState','INTEGER','0-2'),(40,0,29,'resource_type','INTEGER','0-7'),(43,0,31,'event_id','INTEGER','0-2'),(44,0,31,'owner_name','STRING','A-Z'),(45,0,32,'event_id','INTEGER','0-2'),(46,0,32,'owner_name','STRING','A-Z'),(49,0,37,'member_name','STRING','A-Z'),(51,0,38,'max_event','INTEGER','0-2'),(68,0,22,'mfr_param_type','INTEGER','0-9'),(81,0,74,'Opensource_component_type','STRING','qt_non_gfx (or) qt_gfx (or) webkit (or) gstreamer (or) gst_plugin_base (or) gst_plugin_good (or) gst-plugin-custom'),(82,0,74,'Display_option','STRING','directfb (or) eglnullws (or) intelce'),(85,0,78,'indicator_name','STRING','A-Z'),(86,0,78,'brightness','INTEGER','1-100'),(87,0,79,'indicator_name','STRING','A-Z'),(88,0,79,'blink_interval','INTEGER','1-10'),(89,0,79,'blink_iteration','STRING','1-10'),(90,0,80,'viteration','INTEGER','1-10'),(91,0,80,'hiteration','INTEGER','1-10'),(92,0,80,'hold_duration','INTEGER','1-10'),(93,0,80,'text','STRING','A-Z'),(94,0,81,'port_name','STRING','A-Z'),(97,0,82,'port_name','STRING','A-Z'),(98,0,83,'zoom_setting','STRING','A-Z'),(99,0,84,'port_name','STRING','A-Z'),(100,0,84,'encoding_format','STRING','A-Z'),(101,0,85,'port_name','STRING','A-Z'),(102,0,85,'compression_format','STRING','A-Z'),(103,0,86,'port_name','STRING','A-Z'),(104,0,86,'stereo_mode','STRING','A-Z'),(105,0,87,'new_power_state','INTEGER','0-1'),(106,0,88,'port_name','STRING','A-Z'),(107,0,88,'resolution','STRING','A-Z & 0-9'),(108,0,90,'indicator_name','STRING','A-Z'),(109,0,92,'text_display','STRING','A-Z'),(110,0,92,'text','STRING','A-Z'),(111,0,93,'time_format','INTEGER','0-2'),(112,0,93,'text','STRING','A-Z'),(113,0,94,'time_hrs','INTEGER','1-24'),(114,0,94,'time_mins','INTEGER','1-60'),(115,0,94,'text','STRING','A-Z'),(116,0,95,'loop_thru','INTEGER','0-1'),(117,0,95,'port_name','STRING','A-Z'),(118,0,96,'mute_status','INTEGER','0-1'),(119,0,96,'port_name','STRING','A-Z'),(120,0,97,'port_name','STRING','A-Z'),(121,0,98,'port_name','STRING','A-Z'),(122,0,99,'port_name','STRING','A-Z'),(123,0,102,'port_name','STRING','A-Z'),(124,0,103,'port_id','INTEGER','0'),(125,0,104,'port_id','INTEGER','0'),(126,0,105,'port_name','STRING','A-Z'),(127,0,106,'port_name','STRING','A-Z'),(128,0,107,'port_name','STRING','A-Z'),(129,0,108,'ocapId','STRING','A-Z'),(130,0,112,'ocapId','STRING','A-Z'),(134,0,115,'timePosition','STRING','A-Z'),(135,0,115,'PlaySpeed','STRING','A-Z'),(137,0,117,'port_name','STRING','A-Z'),(138,0,118,'port_name','STRING','A-Z'),(139,0,124,'service_name','STRING','A-Z'),(140,0,125,'service_name','STRING','A-Z'),(141,0,126,'service_name','STRING','A-Z'),(142,0,81,'audio_level','FLOAT','1-10'),(143,0,82,'db_level','FLOAT','1-100'),(145,0,128,'recordingId','STRING','A-Z'),(152,0,142,'rmfapp_command','STRING','any alphanumeric sequence'),(154,0,149,'service_name','STRING','A-Z'),(155,0,150,'enable','INTEGER','0,1'),(156,0,151,'enable','INTEGER','0,1'),(158,0,153,'apiVersion','INTEGER','1-1000'),(159,0,154,'service_name','STRING','A-Z'),(160,0,154,'event_name','STRING','A-Z'),(161,0,152,'device_name','STRING','A-Z & 1-1000'),(162,0,153,'service_name','STRING','A-Z'),(163,0,156,'videoDisplay','STRING','A-Z'),(164,0,157,'videoDisplay','STRING','A-Z'),(165,0,156,'zoomLevel','STRING','A-Z'),(166,0,157,'resolution','STRING','A-Z'),(189,0,177,'status','INTEGER','0-1'),(193,0,182,'trickPlayStatus','INTEGER','0-1'),(195,0,173,'Categories','STRING','A-Z'),(196,0,173,'ccAttribute','INTEGER','1 - 14'),(197,0,173,'value','INTEGER','1-8'),(198,0,173,'ccType','INTEGER','0-1'),(199,0,173,'stylevalue','STRING','A-Z'),(201,0,164,'channel_num','INTEGER','1-63'),(202,0,166,'analog_channel_num','INTEGER','1-8'),(209,0,192,'ocapid','STRING','A-Z'),(212,0,30,'appname','STRING','A-Z'),(214,0,22,'testapp_API1_data','INTEGER','1-1000'),(215,0,22,'testapp_API0_data','INTEGER','1-1000'),(254,0,211,'pauseuri','STRING','A-Z'),(259,0,216,'playuri','STRING','A-Z'),(264,0,224,'playuri','STRING','A-Z'),(266,0,224,'Y','INTEGER','0-1'),(267,0,224,'X','INTEGER','0-1'),(268,0,224,'H','INTEGER','0-10000'),(269,0,224,'W','INTEGER','0-10000'),(277,0,224,'apply','INTEGER','0,1'),(283,0,223,'playuri','STRING','A-Z'),(284,0,202,'Volume','FLOAT','0-100'),(286,0,227,'playuri','STRING','A-Z'),(301,0,230,'Volume','FLOAT','0-100'),(302,0,230,'X','INTEGER','0-1'),(303,0,230,'Y','INTEGER','0-1'),(304,0,230,'H','INTEGER','0-10000'),(305,0,230,'W','INTEGER','0-1000'),(306,0,230,'apply','INTEGER','0,1'),(307,0,230,'playuri','STRING','A-Z'),(313,0,231,'playuri','STRING','A-Z'),(314,0,232,'X','INTEGER','0-1'),(315,0,232,'Y','INTEGER','0-1'),(316,0,232,'H','INTEGER','0-10000'),(317,0,232,'W','INTEGER','0-1000'),(318,0,232,'playuri','STRING','A-Z'),(319,0,232,'apply','INTEGER','0,1'),(374,0,270,'recordingId','INTEGER','usually 5 digit nos '),(375,0,270,'playUrl','STRING','play url'),(385,0,277,'module','STRING','A-Z'),(386,0,277,'level','STRING','A-Z'),(387,0,278,'module','STRING','A-Z'),(390,0,279,'module','STRING','A-Z'),(393,0,283,'module','STRING','A-Z'),(394,0,283,'level','STRING','A-Z'),(395,0,280,'number','INTEGER','0-100'),(396,0,281,'number','INTEGER','0-100'),(397,0,285,'ocaplocator','STRING','A-Z'),(398,0,293,'ocaplocator','STRING','A-Z'),(399,0,294,'ocaplocator','STRING','A-Z'),(400,0,295,'ocaplocator','STRING','A-Z'),(401,0,296,'ocaplocator','STRING','A-Z'),(402,0,297,'ocaplocator','STRING','A-Z'),(403,0,300,'ocaplocator','STRING','A-Z'),(404,0,301,'ocaplocator','STRING','A-Z'),(405,0,301,'newocaplocator','STRING','A-Z'),(406,0,304,'index','INTEGER','0-100'),(407,0,305,'recordingId','STRING','A-Z'),(408,0,306,'recordingId','STRING','A-Z'),(409,0,307,'recordingId','STRING','A-Z'),(410,0,308,'recordingId','STRING','A-Z'),(411,0,309,'recordingId','STRING','A-Z'),(412,0,311,'duration','INTEGER','long long (+positive no)'),(413,0,312,'recordingTitle','STRING','A-Z'),(414,0,312,'recordingId','STRING','A-Z'),(415,0,312,'recordDuration','DOUBLE','+ postive no'),(416,0,312,'qamLocator','STRING','qam locator string'),(417,0,313,'recordingId','STRING','A-Z'),(418,0,314,'recordingId','STRING','A-Z'),(419,0,316,'tsbId','STRING','negative long long'),(420,0,316,'recordingId','STRING','A-Z'),(421,0,317,'index','INTEGER','0-100'),(488,0,350,'URL','STRING','A-Z'),(489,0,351,'VideostreamURL','STRING','A-Z'),(490,0,351,'play_time','INTEGER','0-50'),(492,0,353,'recordingTitle','STRING','A-Z'),(493,0,353,'recordingId','STRING','A-Z'),(494,0,353,'recordDuration','DOUBLE','1-1000'),(495,0,353,'qamLocator','STRING','A-Z'),(496,0,351,'SkipTime','INTEGER','0-100'),(497,0,354,'rmfElement','STRING','A-Z'),(498,0,355,'rmfElement','STRING','A-Z'),(499,0,356,'rmfElement','STRING','A-Z'),(500,0,357,'url','STRING','A-Z'),(501,0,357,'rmfElement','STRING','A-Z'),(502,0,358,'rmfElement','STRING','A-Z'),(503,0,359,'rmfElement','STRING','A-Z'),(504,0,360,'rmfElement','STRING','A-Z'),(505,0,360,'playSpeed','FLOAT','1-100'),(506,0,360,'playTime','DOUBLE','0-100'),(507,0,360,'defaultPlay','INTEGER','0-1'),(508,0,361,'rmfSourceElement','STRING','A-Z'),(509,0,361,'rmfSinkElement','STRING','A-Z'),(510,0,362,'apply','INTEGER','0-1'),(511,0,362,'X','INTEGER','0-100'),(512,0,362,'Y','INTEGER','0-100'),(513,0,362,'height','INTEGER','1-10000'),(514,0,362,'width','INTEGER','1-10000'),(515,0,363,'playSpeed','FLOAT','1-100'),(516,0,364,'rmfElement','STRING','A-Z'),(517,0,363,'rmfElement','STRING','A-Z'),(518,0,365,'rmfElement','STRING','A-Z'),(519,0,366,'rmfElement','STRING','A-Z'),(520,0,367,'rmfElement','STRING','A-Z'),(521,0,368,'rmfElement','STRING','A-Z'),(522,0,368,'mediaTime','DOUBLE','0-10000'),(523,0,369,'rmfElement','STRING','A-Z'),(524,0,370,'Input1','INTEGER','1-100'),(529,0,372,'Recording_Id','STRING','0-100000'),(530,0,314,'playUrl','STRING','A-Z'),(531,0,305,'playUrl','STRING','A-Z'),(532,0,306,'playUrl','STRING','A-Z'),(533,0,307,'playUrl','STRING','A-Z'),(534,0,308,'playUrl','STRING','A-Z'),(535,0,309,'playUrl','STRING','A-Z'),(536,0,316,'playUrl','STRING','A-Z'),(537,0,313,'playUrl','STRING','A-Z'),(539,0,304,'playUrl','STRING','A-Z'),(540,0,373,'recordingId','STRING','A-Z'),(541,0,374,'index','INTEGER','0-100'),(544,0,380,'Validurl','STRING','A-Z'),(545,0,381,'videoStreamURL','STRING','A-Z'),(546,0,379,'RecordURL','STRING','A-Z'),(547,0,378,'videoStreamURL','STRING','A-Z'),(548,0,382,'playUrl','STRING','A-Z'),(549,0,383,'playUrl','STRING','A-Z'),(550,0,383,'speed','FLOAT','1-100'),(551,0,384,'playUrl','STRING','A-Z'),(552,0,385,'playUrl','STRING','A-Z'),(553,0,354,'dvrSinkRecordId','STRING','A-Z'),(554,0,385,'rewindSpeed','FLOAT','1-100'),(555,0,386,'playUrl','STRING','A-Z'),(556,0,387,'playUrl','STRING','A-Z'),(557,0,388,'playUrl','STRING','A-Z'),(558,0,388,'rCount','INTEGER','1-100'),(559,0,389,'playUrl','STRING','A-Z'),(560,0,389,'seconds','DOUBLE','1-100'),(561,0,389,'rCount','INTEGER','1-100'),(562,0,390,'playUrl','STRING','A-Z'),(564,0,390,'rCount','INTEGER','1-100'),(565,0,390,'seconds','DOUBLE','1-100'),(566,0,391,'playUrl','STRING','A-Z'),(567,0,391,'seconds','DOUBLE','1-100'),(568,0,392,'playUrl','STRING','A-Z'),(569,0,392,'seconds','DOUBLE','1-100'),(570,0,392,'rCount','INTEGER','1-100'),(571,0,393,'playUrl','STRING','A-Z'),(572,0,393,'seconds','DOUBLE','1-100'),(573,0,394,'playUrl','STRING','A-Z'),(574,0,394,'seconds','DOUBLE','1-100'),(575,0,395,'playUrl','STRING','A-Z'),(576,0,395,'rewindSpeed','FLOAT','1-100'),(577,0,395,'forwardSpeed','FLOAT','1-100'),(578,0,396,'playUrl','STRING','A-Z'),(579,0,396,'rewindSpeed','FLOAT','1-100'),(580,0,396,'forwardSpeed','FLOAT','1-100'),(581,0,397,'playUrl','STRING','A-Z'),(582,0,397,'trickPlayRate','FLOAT','1-100'),(583,0,398,'playUrl','STRING','A-Z'),(584,0,398,'trickPlayRate','FLOAT','1-100'),(585,0,399,'playUrl','STRING','A-Z'),(586,0,399,'sfSeconds','DOUBLE','1-100'),(587,0,399,'sbSeconds','DOUBLE','1-100'),(588,0,399,'rCount','INTEGER','1-100'),(589,0,400,'playUrl','STRING','A-Z'),(590,0,400,'rewindSpeed','FLOAT','1-100'),(591,0,400,'forwardSpeed','FLOAT','1-100'),(592,0,400,'sfSeconds','DOUBLE','1-100'),(593,0,400,'sbSeconds','DOUBLE','1-100'),(594,0,400,'rCount','INTEGER','1-100'),(595,0,401,'playUrl','STRING','A-Z'),(596,0,402,'playUrl','STRING','1-100'),(597,0,403,'Validurl','STRING','A-Z'),(599,0,405,'recordingId','STRING','A-Z'),(600,0,405,'url','STRING','A-Z'),(601,0,405,'recDuration','DOUBLE','1-100'),(602,0,371,'Duration','STRING','Inmillsec'),(603,0,371,'Start_time','STRING','In-MilliSec'),(604,0,371,'Recording_Id','STRING','0-10000'),(605,0,371,'Source_id','STRING','A-Z'),(606,0,371,'UTCTime','STRING','mmddHHMMyyyy'),(607,0,404,'playUrl','STRING','A-Z'),(608,0,416,'url','STRING','A-Z'),(609,0,354,'factoryEnable','STRING','A-Z'),(610,0,354,'qamSrcUrl','STRING','A-Z'),(611,0,359,'factoryEnable','STRING','A-Z'),(612,0,420,'url','STRING','A-Z'),(614,0,420,'socketId','INTEGER','0-100'),(615,0,420,'streamIp','STRING','A-Z'),(616,0,420,'typeFlag','INTEGER','0-1'),(617,0,421,'rmfElement','STRING','A-Z'),(618,0,420,'dctpEnable','STRING','A-Z'),(619,0,376,'VideostreamURL','STRING','A-Z'),(620,0,376,'trickPlayRate','FLOAT','0-100'),(621,0,375,'ValidocapId','STRING','A-Z'),(622,0,420,'useChunkTransfer','STRING','A-Z'),(624,0,422,'VideostreamURL','STRING','A-Z'),(625,0,422,'SpeedRate','FLOAT','0-100'),(631,0,425,'playUrl','STRING','A-Z'),(632,0,424,'recordId','STRING','any alphanumeric sequence'),(633,0,424,'recordDuration','STRING','any alphanumeric sequence'),(634,0,424,'recordTitle','STRING','any alphanumeric sequence'),(635,0,424,'ocapId','STRING','any alphanumeric sequence'),(636,0,426,'resultList','STRING','A-Z'),(637,0,427,'path','STRING','A-Z'),(641,0,29,'state','INTEGER','0-100'),(642,0,29,'error','INTEGER','0-100'),(643,0,29,'payload','STRING','A-Z'),(644,0,429,'module','STRING','A-Z'),(645,0,434,'module','STRING','A-Z'),(646,0,431,'module','STRING','A-Z'),(647,0,433,'module','STRING','A-Z'),(648,0,432,'module','STRING','A-Z'),(649,0,432,'level','STRING','A-Z'),(650,0,432,'msg','STRING','A-Z'),(651,0,438,'path','STRING','A-Z'),(652,0,438,'paramValue','STRING','A-Z'),(654,0,30,'argv1','STRING','ON,OFF,PAIR'),(655,0,441,'module','STRING','A-Z'),(656,0,440,'module','STRING','A-Z'),(657,0,440,'level','STRING','A-Z'),(658,0,207,'X','INTEGER','0-1'),(659,0,207,'H','INTEGER','0-10000'),(660,0,207,'playuri','STRING','A-Z'),(661,0,207,'Y','INTEGER','0-1'),(662,0,207,'apply','INTEGER','0-10000'),(663,0,207,'W','INTEGER','0-10000'),(665,0,450,'propValue','INTEGER','0-1000'),(666,0,454,'propValue','STRING','AZ'),(669,0,459,'propValue','STRING','AZ'),(670,0,460,'recordingId','STRING','A-Z'),(671,0,460,'duration','DOUBLE','0-1000000'),(672,0,460,'locator','STRING','A-Z'),(673,0,465,'propValue','STRING','AZ'),(674,0,467,'propValue','STRING','AZ'),(675,0,461,'duration','DOUBLE','0-1000000'),(676,0,461,'locator','STRING','A-Z'),(679,0,456,'propValue','INTEGER','0-100'),(680,0,443,'propValue','INTEGER','0-100'),(684,0,474,'duration','DOUBLE','0-1000000'),(685,0,474,'locator','STRING','A-Z'),(686,0,475,'duration','DOUBLE','0-1000000'),(687,0,475,'locator','STRING','A-Z'),(688,0,476,'recordingId','STRING','A-Z'),(689,0,476,'duration','DOUBLE','0-1000000'),(690,0,476,'locator','STRING','A-Z'),(691,0,477,'duration','DOUBLE','0-1000000'),(692,0,477,'locator','STRING','A-Z'),(698,0,317,'playUrl','STRING','A-Z'),(701,0,482,'url','STRING','A-Z'),(710,0,354,'newQamSrc','STRING','A-Z'),(711,0,354,'newQamSrcUrl','STRING','A-Z'),(712,0,359,'newQamSrc','STRING','A-Z'),(713,0,361,'newQamSrc','STRING','A-Z'),(714,0,360,'newQamSrc','STRING','A-Z'),(715,0,367,'newQamSrc','STRING','A-Z'),(716,0,487,'service_name','STRING','A-Z'),(717,0,488,'service_name','STRING','A-Z'),(718,0,489,'service_name','STRING','A-Z'),(719,0,490,'logPath','STRING','A-Z'),(720,0,78,'get_only','INTEGER','0-1'),(723,0,78,'text','STRING','A-Z'),(725,0,487,'service_name','STRING','A-Z'),(726,0,488,'service_name','STRING','A-Z'),(727,0,489,'service_name','STRING','A-Z'),(728,0,354,'numOfTimeChannelChange','INTEGER','0-100'),(729,0,416,'numOfTimeChannelChange','INTEGER','0-100'),(730,0,361,'numOfTimeChannelChange','INTEGER','0-100'),(731,0,360,'numOfTimeChannelChange','INTEGER','0-100'),(732,0,367,'numOfTimeChannelChange','INTEGER','0-100'),(734,0,359,'numOfTimeChannelChange','INTEGER','0-100'),(735,0,88,'get_only','INTEGER','0-1'),(736,0,491,'state','INTEGER','0-1'),(737,0,492,'enable','INTEGER','0-1'),(738,0,491,'indicator_name','STRING','A-Z'),(739,0,492,'port_name','STRING','A-Z'),(740,0,75,'color','INTEGER','0-4'),(741,0,75,'indicator_name','STRING','A-Z'),(750,0,460,'startTime','DOUBLE','0-1000000'),(751,0,461,'startTime','DOUBLE','0-1000000'),(752,0,460,'deviceNo','INTEGER','0-5'),(753,0,461,'deviceNo','INTEGER','0-5'),(754,0,460,'hot','INTEGER','0-1'),(755,0,495,'audioVideoStatus','STRING','A-Z'),(756,0,474,'deviceNo','INTEGER','0-5'),(757,0,475,'deviceNo','INTEGER','0-5'),(758,0,497,'funcName','STRING','A-Z'),(759,0,497,'param1','STRING','A-Z'),(762,0,497,'param4','INTEGER','0-100'),(763,0,497,'param2','INTEGER','0-100'),(764,0,497,'param3','INTEGER','0-100'),(765,0,505,'evtName','STRING','A-Z'),(766,0,505,'evtValue','STRING','A-Z'),(767,0,506,'logFile','STRING','A-Z'),(768,0,506,'FileNameToCpTdkPath','STRING','A-Z'),(769,0,506,'patternToSearch','STRING','A-Z'),(770,0,507,'logFileToClear','STRING','A-Z'),(771,0,508,'recordId','STRING','A-Z'),(772,0,508,'recordDuration','STRING','A-Z'),(773,0,508,'recordTitle','STRING','A-Z'),(774,0,508,'ocapId','STRING','A-Z'),(775,0,475,'activity','INTEGER','1-2'),(776,0,474,'activity','INTEGER','1-2'),(780,0,447,'deviceNo','INTEGER','0-5');
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
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=latin1;
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
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
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
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
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
) ENGINE=InnoDB AUTO_INCREMENT=1064 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `script_file`
--

LOCK TABLES `script_file` WRITE;
/*!40000 ALTER TABLE `script_file` DISABLE KEYS */;
INSERT INTO `script_file` VALUES (1,0,'gst-plugins-rdk',' GstPluginRdk_Aesdecrypt_DecryptEnable_Get_Default'),(2,0,'gst-plugins-rdk',' GstPluginRdk_Dvrsink_RecordId_Set_Prop'),(3,0,'gst-plugins-rdk',' GstPluginRdk_Dvrsrc_Duration_Get_Prop_Default'),(4,0,'closedcaption','CC_Get_Attribute_BGOpacity_default_28'),(5,0,'closedcaption','CC_Get_Attribute_BorderColor_default_34'),(6,0,'closedcaption','CC_Get_Attribute_BorderType_default_33'),(7,0,'closedcaption','CC_Get_Attribute_EdgeColor_default_38'),(8,0,'closedcaption','CC_Get_Attribute_EdgeType_default_37'),(9,0,'closedcaption','CC_Get_Attribute_FontColor_default_26'),(10,0,'closedcaption','CC_Get_Attribute_FontItalic_default_31'),(11,0,'closedcaption','CC_Get_Attribute_FontOpacity_default_27'),(12,0,'closedcaption','CC_Get_Attribute_FontSize_default_30'),(13,0,'closedcaption','CC_Get_Attribute_FontStyle_default_29'),(14,0,'closedcaption','CC_Get_Attribute_FontUnderline_default_32'),(15,0,'closedcaption','CC_Get_Attribute_WinBorderColor_default_35'),(16,0,'closedcaption','CC_Get_Attribute_WinOpacity_default_36'),(17,0,'closedcaption','CC_Get_SupportedServiceNumberCount_ServiceNumber_23'),(18,0,'closedcaption','CC_Hide_22'),(19,0,'closedcaption','CC_Initialization_01'),(20,0,'closedcaption','CC_ResetTrickPlayStatus_24'),(21,0,'closedcaption','CC_SetGet_AnalogChannel_19'),(22,0,'closedcaption','CC_SetGet_Attribute_BgColor_04'),(23,0,'closedcaption','CC_SetGet_Attribute_BgColor_BoundHigh_56'),(24,0,'closedcaption','CC_SetGet_Attribute_BgColor_BoundLow_70'),(25,0,'closedcaption','CC_SetGet_Attribute_BgColor_invalid_42'),(26,0,'closedcaption','CC_SetGet_Attribute_BGOpacity_06'),(27,0,'closedcaption','CC_SetGet_Attribute_BGOpacity_BoundHigh_58'),(28,0,'closedcaption','CC_SetGet_Attribute_BGOpacity_BoundLow_72'),(29,0,'closedcaption','CC_SetGet_Attribute_BGOpacity_invalid_44'),(30,0,'closedcaption','CC_SetGet_Attribute_BorderColor_12'),(31,0,'closedcaption','CC_SetGet_Attribute_BorderColor_BoundHigh_64'),(32,0,'closedcaption','CC_SetGet_Attribute_BorderColor_invalid_50'),(33,0,'closedcaption','CC_SetGet_Attribute_BorderType_11'),(34,0,'closedcaption','CC_SetGet_Attribute_BorderType_BoundHigh_63'),(35,0,'closedcaption','CC_SetGet_Attribute_BorderType_invalid_49'),(36,0,'closedcaption','CC_SetGet_Attribute_EdgeColor_16'),(37,0,'closedcaption','CC_SetGet_Attribute_EdgeColor_BoundHigh_68'),(38,0,'closedcaption','CC_SetGet_Attribute_EdgeColor_invalid_54'),(39,0,'closedcaption','CC_SetGet_Attribute_EdgeType_15'),(40,0,'closedcaption','CC_SetGet_Attribute_EdgeType_BoundHigh_67'),(41,0,'closedcaption','CC_SetGet_Attribute_EdgeType_invalid_53'),(42,0,'closedcaption','CC_SetGet_Attribute_FontColor_03'),(43,0,'closedcaption','CC_SetGet_Attribute_FontColor_190'),(44,0,'closedcaption','CC_SetGet_Attribute_FontColor_191'),(45,0,'closedcaption','CC_SetGet_Attribute_FontColor_192'),(46,0,'closedcaption','CC_SetGet_Attribute_FontColor_193'),(47,0,'closedcaption','CC_SetGet_Attribute_FontColor_194'),(48,0,'closedcaption','CC_SetGet_Attribute_FontColor_195'),(49,0,'closedcaption','CC_SetGet_Attribute_FontColor_196'),(50,0,'closedcaption','CC_SetGet_Attribute_FontColor_BoundHigh_55'),(51,0,'closedcaption','CC_SetGet_Attribute_FontColor_BoundLow_69'),(52,0,'closedcaption','CC_SetGet_Attribute_FontColor_invalid_41'),(53,0,'closedcaption','CC_SetGet_Attribute_FontItalic_09'),(54,0,'closedcaption','CC_SetGet_Attribute_FontItalic_BoundHigh_61'),(55,0,'closedcaption','CC_SetGet_Attribute_FontItalic_BoundLow_75'),(56,0,'closedcaption','CC_SetGet_Attribute_FontItalic_invalid_47'),(57,0,'closedcaption','CC_SetGet_Attribute_FontOpacity_05'),(58,0,'closedcaption','CC_SetGet_Attribute_FontOpacity_BoundHigh_57'),(59,0,'closedcaption','CC_SetGet_Attribute_FontOpacity_invalid_43'),(60,0,'closedcaption','CC_SetGet_Attribute_FontSize_08'),(61,0,'closedcaption','CC_SetGet_Attribute_FontSize_BoundHigh_60'),(62,0,'closedcaption','CC_SetGet_Attribute_FontSize_invalid_46'),(63,0,'closedcaption','CC_SetGet_Attribute_FontStyle_07'),(64,0,'closedcaption','CC_SetGet_Attribute_FontStyle_BoundHigh_59'),(65,0,'closedcaption','CC_SetGet_Attribute_FontStyle_invalid_45'),(66,0,'closedcaption','CC_SetGet_Attribute_FontUnderline_10'),(67,0,'closedcaption','CC_SetGet_Attribute_FontUnderline_BoundHigh_62'),(68,0,'closedcaption','CC_SetGet_Attribute_FontUnderline_BoundLow_76'),(69,0,'closedcaption','CC_SetGet_Attribute_FontUnderline_invalid_48'),(70,0,'closedcaption','CC_SetGet_Attribute_WinBorderColor_13'),(71,0,'closedcaption','CC_SetGet_Attribute_WinBorderColor_BoundHigh_65'),(72,0,'closedcaption','CC_SetGet_Attribute_WinBorderColor_invalid_51'),(73,0,'closedcaption','CC_SetGet_Attribute_WindowOpacity_BoundHigh_66'),(74,0,'closedcaption','CC_SetGet_Attribute_WinOpacity_14'),(75,0,'closedcaption','CC_SetGet_Attribute_WinOpacity_invalid_52'),(76,0,'closedcaption','CC_SetGet_DigitalChannel_17'),(77,0,'closedcaption','CC_SetGet_InvalidDigitalChannel_18'),(78,0,'closedcaption','CC_SetGet_Invalid_AnalogChannel_20'),(79,0,'closedcaption','CC_SetGet_State_02'),(80,0,'closedcaption','CC_SetTrickPlayStatus_25'),(81,0,'closedcaption','CC_Show_21'),(82,0,'dtcp','CT_DTCPAgent_01'),(83,0,'dtcp','CT_DTCP_02'),(84,0,'dtcp','CT_DTCP_03'),(85,0,'dtcp','CT_DTCP_04'),(86,0,'dtcp','CT_DTCP_05'),(87,0,'dtcp','CT_DTCP_06'),(88,0,'dtcp','CT_DTCP_07'),(89,0,'dtcp','CT_DTCP_08'),(90,0,'dtcp','CT_DTCP_09'),(91,0,'dtcp','CT_DTCP_10'),(92,0,'dtcp','CT_DTCP_11'),(93,0,'xupnp','CT_XUPNP_01'),(94,0,'xupnp','CT_XUPNP_02'),(95,0,'xupnp','CT_XUPNP_03'),(96,0,'xupnp','CT_XUPNP_04'),(97,0,'xupnp','CT_XUPNP_05'),(98,0,'xupnp','CT_XUPNP_06'),(99,0,'xupnp','CT_XUPNP_07'),(100,0,'xupnp','CT_XUPNP_08'),(101,0,'xupnp','CT_XUPNP_09'),(102,0,'xupnp','CT_XUPNP_10'),(103,0,'xupnp','CT_XUPNP_11'),(104,0,'xupnp','CT_XUPNP_12'),(105,0,'xupnp','CT_XUPNP_13'),(106,0,'xupnp','CT_XUPNP_14'),(107,0,'devicesettings','DS_AddDisplayconnection Listener test_14'),(108,0,'devicesettings','DS_Brightness_Persistent_116'),(109,0,'devicesettings','DS_DTCP support test_19'),(110,0,'devicesettings','DS_GetAspect Ratio test_21'),(111,0,'devicesettings','DS_GetAspect_Ratio_Reboot_test_114'),(112,0,'devicesettings','DS_GetDisplayDetails test_22'),(113,0,'devicesettings','DS_GetDisplayDetails_OnDisabledPort_123'),(114,0,'devicesettings','DS_GetDisplayDetails_Reboot_test_113'),(115,0,'devicesettings','DS_HDCP Support test_18'),(116,0,'devicesettings','DS_IsContentProtection test_17'),(117,0,'devicesettings','DS_IsDynamicResolutionsSupport test_20'),(118,0,'devicesettings','DS_LoopThru test_08'),(119,0,'devicesettings','DS_mute_test_09'),(120,0,'devicesettings','DS_PowerMode Listener test_13'),(121,0,'devicesettings','DS_PowerModeToggle_Stress_119'),(122,0,'devicesettings','DS_Resolution test_16'),(123,0,'devicesettings','DS_ResolutionChange_VideoPlay_122'),(124,0,'devicesettings','DS_Resolution_1080i50_test_90'),(125,0,'devicesettings','DS_Resolution_1080i_test_84'),(126,0,'devicesettings','DS_Resolution_1080p24_test_88'),(127,0,'devicesettings','DS_Resolution_1080p30_test_91'),(128,0,'devicesettings','DS_Resolution_1080p60_test_92'),(129,0,'devicesettings','DS_Resolution_1080p_test_89'),(130,0,'devicesettings','DS_Resolution_480i_test_82'),(131,0,'devicesettings','DS_Resolution_480p_test_85'),(132,0,'devicesettings','DS_Resolution_576p50_test_86'),(133,0,'devicesettings','DS_Resolution_720p50_test_87'),(134,0,'devicesettings','DS_Resolution_720p_test_83'),(135,0,'devicesettings','DS_Resolution_Invalid_port_test_93'),(136,0,'devicesettings','DS_Resolution_Invalid_value_test_94'),(137,0,'devicesettings','DS_Resolution_Persistent_118'),(138,0,'devicesettings','DS_Resolution_PortStateChange_120'),(139,0,'devicesettings','DS_Resolution_PowerModeChange_121'),(140,0,'devicesettings','DS_Resolution_STRESS_test_112'),(141,0,'devicesettings','DS_SetAudioLevel test_06'),(142,0,'devicesettings','DS_SetAudioLevel_Maximum_test_52'),(143,0,'devicesettings','DS_SetAudioLevel_Minimum_test_51'),(144,0,'devicesettings','DS_SetAudioLevel_STRESS_test_106'),(145,0,'devicesettings','DS_SetAudioLevel_value in range_test_53'),(146,0,'devicesettings','DS_SetAudioLevel_value outof range_test_54'),(147,0,'devicesettings','DS_SetBlink test_03'),(148,0,'devicesettings','DS_SetBlink_Invalid_test_39'),(149,0,'devicesettings','DS_SetBlink_outofrange_test_40'),(150,0,'devicesettings','DS_SetBlink_STRESS_test_102'),(151,0,'devicesettings','DS_SetBlink_valid_test_38'),(152,0,'devicesettings','DS_SetblueColor_INVALID_LED_32'),(153,0,'devicesettings','DS_SetblueColor_MESSAGE_LED_27'),(154,0,'devicesettings','DS_SetblueColor_POWER_LED_31'),(155,0,'devicesettings','DS_SetblueColor_RECORD_LED_28'),(156,0,'devicesettings','DS_SetblueColor_REMOTE_LED_30'),(157,0,'devicesettings','DS_SetblueColor_RFBYPASS_LED_29'),(158,0,'devicesettings','DS_SetBrightness test_01'),(159,0,'devicesettings','DS_SetBrightness_Maximum value test_24'),(160,0,'devicesettings','DS_SetBrightness_Minimum value test_23'),(161,0,'devicesettings','DS_SetBrightness_STRESS_test_100'),(162,0,'devicesettings','DS_SetBrightness_value in range test_25'),(163,0,'devicesettings','DS_SetBrightness_value out of range test_26'),(164,0,'devicesettings','DS_SetColor test_02'),(165,0,'devicesettings','DS_SetColor_green test_33'),(166,0,'devicesettings','DS_SetColor_invalid_test_37'),(167,0,'devicesettings','DS_SetColor_orange test_36'),(168,0,'devicesettings','DS_SetColor_red test_34'),(169,0,'devicesettings','DS_SetColor_STRESS_test_101'),(170,0,'devicesettings','DS_SetColor_yellow test_35'),(171,0,'devicesettings','DS_SetCompression test_11'),(172,0,'devicesettings','DS_SetCompression_HEAVY_FORMAT_66'),(173,0,'devicesettings','DS_SetCompression_INVALID_FORMAT_68'),(174,0,'devicesettings','DS_SetCompression_LIGHT_FORMAT_64'),(175,0,'devicesettings','DS_SetCompression_MEDIUM_FORMAT_65'),(176,0,'devicesettings','DS_SetCompression_NONE_67'),(177,0,'devicesettings','DS_SetCompression_STRESS_test_109'),(178,0,'devicesettings','DS_SetDB test_07'),(179,0,'devicesettings','DS_SetDB_Invalid_Value_test_58'),(180,0,'devicesettings','DS_SetDB_Maximum_test_55'),(181,0,'devicesettings','DS_SetDB_Minimum_test_56'),(182,0,'devicesettings','DS_SetDb_STRESS_test_107'),(183,0,'devicesettings','DS_SetDB_valid_value_test_57'),(184,0,'devicesettings','DS_SetDFC test_15'),(185,0,'devicesettings','DS_SetDFC_CCO_ZOOM_test_77'),(186,0,'devicesettings','DS_SetDFC_FULL_ZOOM_test_75'),(187,0,'devicesettings','DS_SetDFC_INVALID_ZOOM_test_81'),(188,0,'devicesettings','DS_SetDFC_None_ZOOM_test_74'),(189,0,'devicesettings','DS_SetDFC_PanScan_ZOOM_test_78'),(190,0,'devicesettings','DS_SetDFC_Pillarbox4x3_ZOOM_test_80'),(191,0,'devicesettings','DS_SetDFC_PLATFORM_ZOOM_test_76'),(192,0,'devicesettings','DS_SetDFC_STRESS_test_111'),(193,0,'devicesettings','DS_SetDFC_Zoom16x9_test_79'),(194,0,'devicesettings','DS_SetEncoding test_10'),(195,0,'devicesettings','DS_SetEncoding_AC3_FORMAT_test_59'),(196,0,'devicesettings','DS_SetEncoding_DISPLAY_FORMAT_test_61'),(197,0,'devicesettings','DS_SetEncoding_Invalid_FORMAT_test_63'),(198,0,'devicesettings','DS_SetEncoding_NONE_test_62'),(199,0,'devicesettings','DS_SetEncoding_PCM_FORMAT_test_60'),(200,0,'devicesettings','DS_SetEncoding_STRESS_test_108'),(201,0,'devicesettings','DS_SetPowerMode_Invalid_test_98'),(202,0,'devicesettings','DS_SetPowerMode_OFF_test_96'),(203,0,'devicesettings','DS_SetPowerMode_ON_test_95'),(204,0,'devicesettings','DS_SetPowerMode_STANDBY_test_97'),(205,0,'devicesettings','DS_SetPowerMode_STRESS_test_99'),(206,0,'devicesettings','DS_SetScroll test_05'),(207,0,'devicesettings','DS_SetScroll_Maximum_Value_test_49'),(208,0,'devicesettings','DS_SetScroll_Middle_Value_test_50'),(209,0,'devicesettings','DS_SetScroll_Minimum_Value_test_48'),(210,0,'devicesettings','DS_SetScroll_STRESS_test_105'),(211,0,'devicesettings','DS_SetState_Stress_115'),(212,0,'devicesettings','DS_SetStereoModes test_12'),(213,0,'devicesettings','DS_SetStereoMode_INVALID_FORMAT_73'),(214,0,'devicesettings','DS_SetStereoMode_MONO_FORMAT_69'),(215,0,'devicesettings','DS_SetStereoMode_STEREO_FORMAT_70'),(216,0,'devicesettings','DS_SetStereoMode_STRESS_test_110'),(217,0,'devicesettings','DS_SetStereoMode_SURROUND_FORMAT_71'),(218,0,'devicesettings','DS_SetStereoMode_UNKNOWN_72'),(219,0,'devicesettings','DS_SetTextDisplay_test_46'),(220,0,'devicesettings','DS_SetText_STRESS_test_104'),(221,0,'devicesettings','DS_SetTimeFormat_and_Time test_04'),(222,0,'devicesettings','DS_SetTime_12HR_FORMAT_41'),(223,0,'devicesettings','DS_SetTime_24HR_FORMAT_42'),(224,0,'devicesettings','DS_SetTime_FORMAT_STRESS_test_103'),(225,0,'devicesettings','DS_SetTime_INVALID_45'),(226,0,'devicesettings','DS_SetTime_INVALID_FORMAT_44'),(227,0,'devicesettings','DS_SetTime_STRING_FORMAT_43'),(228,0,'devicesettings','DS_TextBrightness_Persistent_117'),(230,0,'tdk_integration','E2E_DVRTrickPlay_Fwd_0.5x_03'),(231,0,'tdk_integration','E2E_DVRTrickPlay_Fwd_15x_07'),(232,0,'tdk_integration','E2E_DVRTrickPlay_Fwd_30x_09'),(233,0,'tdk_integration','E2E_DVRTrickPlay_Fwd_4x_05'),(234,0,'tdk_integration','E2E_DVRTrickPlay_Fwd_60x_11'),(235,0,'tdk_integration','E2E_DVRTrickPlay_Invalid_PlaySpeed_12'),(236,0,'tdk_integration','E2E_DVRTrickPlay_Rwd_0.5x_02'),(237,0,'tdk_integration','E2E_DVRTrickPlay_Rwd_15x_06'),(238,0,'tdk_integration','E2E_DVRTrickPlay_Rwd_30x_08'),(239,0,'tdk_integration','E2E_DVRTrickPlay_Rwd_4x_04'),(240,0,'tdk_integration','E2E_DVRTrickPlay_Rwd_60x_10'),(241,0,'tdk_integration','E2E_DVR_Invalid_TimePosition_13'),(242,0,'tdk_integration','E2E_DVR_PlayBack_01'),(243,0,'tdk_integration','E2E_DVR_Skip_Fwd_15'),(244,0,'tdk_integration','E2E_DVR_Skip_Rwd_14'),(245,0,'tdk_integration','E2E_LinearTV_H.264_AAC_26'),(246,0,'tdk_integration','E2E_LinearTV_H.264_AC3_25'),(247,0,'tdk_integration','E2E_LinearTV_H.264_MP3_27'),(248,0,'tdk_integration','E2E_LinearTV_H.264_WAV_28'),(249,0,'tdk_integration','E2E_LinearTV_Live_Trickplay_FFW_15x_11'),(250,0,'tdk_integration','E2E_LinearTV_Live_Trickplay_FFW_30x_12'),(251,0,'tdk_integration','E2E_LinearTV_Live_Trickplay_FFW_4x_10'),(252,0,'tdk_integration','E2E_LinearTV_Live_Trickplay_FFW_60x_13'),(253,0,'tdk_integration','E2E_LinearTV_Live_Trickplay_FRW_15x_14'),(254,0,'tdk_integration','E2E_LinearTV_Live_Trickplay_FRW_30x_15'),(255,0,'tdk_integration','E2E_LinearTV_Live_Trickplay_FRW_4x_09'),(256,0,'tdk_integration','E2E_LinearTV_Live_Trickplay_FRW_60x_16'),(257,0,'tdk_integration','E2E_LinearTV_Live_Trickplay_SFW_0.5x_08'),(258,0,'tdk_integration','E2E_LinearTV_Live_Trickplay_SRW_0.5x_07'),(259,0,'tdk_integration','E2E_LinearTV_MPEG2_AAC_19'),(260,0,'tdk_integration','E2E_LinearTV_MPEG2_MP3_21'),(261,0,'tdk_integration','E2E_LinearTV_MPEG2_WAV_23'),(262,0,'tdk_integration','E2E_LinearTV_MPEG4_AAC_20'),(263,0,'tdk_integration','E2E_LinearTV_MPEG4_AC3_18'),(264,0,'tdk_integration','E2E_LinearTV_MPEG4_MP3_22'),(265,0,'tdk_integration','E2E_LinearTV_MPEG4_WAV_24'),(266,0,'tdk_integration','E2E_LinearTV_MPEG_AC3_17'),(267,0,'tdk_integration','E2E_LinearTV_TuneHD-HD_06'),(268,0,'tdk_integration','E2E_LinearTV_TuneHD-SD_05'),(269,0,'tdk_integration','E2E_LinearTV_TuneHD_02'),(270,0,'tdk_integration','E2E_LinearTV_TuneSD-HD_04'),(271,0,'tdk_integration','E2E_LinearTV_TuneSD-SD_03'),(272,0,'tdk_integration','E2E_LinearTV_TuneSD_01'),(273,0,'rmfapp','E2E_rmfapp_help_and_quit'),(274,0,'rmfapp','E2e_rmfApp_ls_quit'),(275,0,'rmfapp','E2E_rmfApp_play_and_quit'),(276,0,'rmfapp','E2E_rmfapp_record_and_quit'),(277,0,'tdk_integration','E2E_RMF_backtoback_record_samechannel'),(278,0,'tdk_integration','E2E_RMF_DVR_book_record_playback'),(279,0,'tdk_integration','E2E_RMF_DVR_playback_H264'),(280,0,'tdk_integration','E2E_RMF_DVR_playback_ongoingrecord_liverecord'),(281,0,'tdk_integration','E2E_RMF_DVR_playback_radiochannel'),(282,0,'tdk_integration','E2E_RMF_DVR_playback_reccont_lessthanoneminute'),(283,0,'tdk_integration','E2E_RMF_DVR_playback_recordcont_liveplayback_AudioChannel'),(284,0,'tdk_integration','E2E_RMF_DVR_simultaneous_recording_dvrplayback'),(285,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_01'),(286,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_02'),(287,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_03'),(288,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_04'),(289,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_05'),(290,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_06'),(291,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_07'),(292,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_08'),(293,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_09'),(294,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_10'),(295,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_13'),(296,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_14'),(297,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_15'),(298,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_16'),(299,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_17'),(300,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_18'),(301,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_19'),(302,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_20'),(303,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_21'),(304,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_22'),(305,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_25'),(306,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_26'),(307,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_27'),(308,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_28'),(309,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_29'),(310,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_30'),(311,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_31'),(312,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_32'),(313,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_33'),(314,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_34'),(315,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_35'),(316,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_36'),(317,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_37'),(318,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_38'),(319,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_39'),(320,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_40'),(321,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_41'),(322,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_43'),(323,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_44'),(324,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_45'),(325,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_46'),(326,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_48'),(327,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_49'),(328,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_50'),(329,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_51'),(330,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_52'),(331,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_54'),(332,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_55'),(333,0,'tdk_integration','E2E_RMF_DVR_trickplay_currentrecord_liveplayback'),(334,0,'tdk_integration','E2E_RMF_DVR_trickplay_recordcont_liveplayback_radiochannel'),(335,0,'tdk_integration','E2E_RMF_H264_Recording'),(336,0,'tdk_integration','E2E_RMF_HDtoRadioChannel'),(337,0,'tdk_integration','E2E_RMF_LinearTV_ClosedCaption_LivePlayback'),(338,0,'tdk_integration','E2E_RMF_LinearTV_DSSetMute_PowerMode_LivePlayback'),(339,0,'tdk_integration','E2E_RMF_LinearTV_DSSetPowerMode_LivePlayback'),(340,0,'tdk_integration','E2E_RMF_LinearTV_DSSetResolution_LivePlayback'),(341,0,'tdk_integration','E2E_RMF_LinearTV_DSSetResolution_Reboot_LivePlayback'),(342,0,'tdk_integration','E2E_Rmf_LinearTV_H.264_AAC_26'),(343,0,'tdk_integration','E2E_Rmf_LinearTV_H.264_AC3_25'),(344,0,'tdk_integration','E2E_Rmf_LinearTV_H.264_MP3_27'),(345,0,'tdk_integration','E2E_Rmf_LinearTV_H.264_WAV_28'),(346,0,'tdk_integration','E2E_Rmf_LinearTV_MPEG2_AAC_19'),(347,0,'tdk_integration','E2E_Rmf_LinearTV_MPEG2_AC3_17'),(348,0,'tdk_integration','E2E_Rmf_LinearTV_MPEG2_MP3_21'),(349,0,'tdk_integration','E2E_Rmf_LinearTV_MPEG2_WAV_23'),(350,0,'tdk_integration','E2E_Rmf_LinearTV_MPEG4_AAC_20'),(351,0,'tdk_integration','E2E_Rmf_LinearTV_MPEG4_AC3_18'),(352,0,'tdk_integration','E2E_Rmf_LinearTV_MPEG4_MP3_22'),(353,0,'tdk_integration','E2E_Rmf_LinearTV_MPEG4_WAV_24'),(354,0,'tdk_integration','E2E_RMF_LinearTV_Stress_HD_LivePlayback_Longduration'),(355,0,'tdk_integration','E2E_RMF_LinearTV_Stress_LiveDvrPlay_LongDuration'),(356,0,'tdk_integration','E2E_RMF_LinearTV_Stress_LivePlayback_Longduration'),(357,0,'tdk_integration','E2E_RMF_LinearTV_Stress_LivePlay_SwitchingChannel_LongDuration'),(358,0,'tdk_integration','E2E_Rmf_LinearTV_TuneHD-HD_06'),(359,0,'tdk_integration','E2E_Rmf_LinearTV_TuneHD-SD_05'),(360,0,'tdk_integration','E2E_RMF_LinearTV_TuneHD_02'),(361,0,'tdk_integration','E2E_Rmf_LinearTV_TuneSD-HD_04'),(362,0,'tdk_integration','E2E_Rmf_LinearTV_TuneSD-SD_03'),(363,0,'tdk_integration','E2E_Rmf_LinearTV_TuneSD_01'),(364,0,'tdk_integration','E2E_RMF_LinearTV_Tune_InvalidChannel'),(365,0,'tdk_integration','E2E_RMF_LinearTV_Tune_SameChannel'),(366,0,'tdk_integration','E2E_RMF_MDVR_Delete_PausePlay_SameRecord'),(367,0,'tdk_integration','E2E_RMF_MDVR_Delete_SameRecord'),(368,0,'tdk_integration','E2E_RMF_MDVR_Delete_TrickPlay_SameRecord'),(369,0,'tdk_integration','E2E_RMF_MDVR_DvrPlay_DiffUrl'),(370,0,'tdk_integration','E2E_RMF_MDVR_DvrPlay_SameUrl'),(371,0,'tdk_integration','E2E_RMF_MDVR_DVR_FastForward_Rewind'),(372,0,'tdk_integration','E2E_RMF_MDVR_DVR_SkipForward_backward_Multiple'),(373,0,'tdk_integration','E2E_RMF_MDVR_Gateway_Client_PausePlay_SameRecord'),(374,0,'tdk_integration','E2E_RMF_MDVR_Gateway_Client_SameRecord'),(375,0,'tdk_integration','E2E_RMF_MDVR_LivePlayPause'),(376,0,'tdk_integration','E2E_RMF_MDVR_LivePlay_DiffUrl'),(377,0,'tdk_integration','E2E_RMF_MDVR_LivePlay_DvrPlay'),(378,0,'tdk_integration','E2E_RMF_MDVR_LivePlay_SameUrl'),(379,0,'tdk_integration','E2E_RMF_MDVR_Max_LivePlay'),(380,0,'tdk_integration','E2E_RMF_MDVR_Max_ScheduleRecording'),(381,0,'tdk_integration','E2E_RMF_MDVR_Max_ScheduleRecording_Neg'),(382,0,'tdk_integration','E2E_RMF_MDVR_PausePlay_SameRecord'),(383,0,'tdk_integration','E2E_RMF_MDVR_SchedLiveRec1_Play2'),(384,0,'tdk_integration','E2E_RMF_MDVR_SchedRec1_Play2'),(385,0,'tdk_integration','E2E_RMF_MDVR_SchedRec_SameChannelSimul'),(386,0,'tdk_integration','E2E_RMF_MDVR_TrickPlay_Gateway_Client_SameRecord'),(387,0,'tdk_integration','E2E_RMF_MDVR_TrickPlay_RadioChannel'),(388,0,'tdk_integration','E2E_RMF_MDVR_TrickPlay_SameRecord'),(389,0,'tdk_integration','E2E_RMF_Multiple_future_recording'),(390,0,'tdk_integration','E2E_RMF_RadioChanneltoHD'),(391,0,'tdk_integration','E2E_RMF_RadioChannel_Recording'),(392,0,'tdk_integration','E2E_RMF_recording_alreadyRecordservice'),(393,0,'tdk_integration','E2E_RMF_Recording_standbymode'),(394,0,'tdk_integration','E2E_RMF_RF_Video_01'),(395,0,'tdk_integration','E2E_RMF_RF_Video_02'),(396,0,'tdk_integration','E2E_RMF_RF_Video_03'),(397,0,'tdk_integration','E2E_RMF_RF_Video_04'),(398,0,'tdk_integration','E2E_RMF_RF_Video_05'),(399,0,'tdk_integration','E2E_RMF_RF_Video_06'),(400,0,'tdk_integration','E2E_RMF_RF_Video_07'),(401,0,'tdk_integration','E2E_RMF_RF_Video_08'),(402,0,'tdk_integration','E2E_RMF_RF_Video_09'),(403,0,'tdk_integration','E2E_RMF_RF_Video_12'),(404,0,'tdk_integration','E2E_RMF_RF_Video_13'),(405,0,'tdk_integration','E2E_RMF_RF_Video_14'),(406,0,'tdk_integration','E2E_RMF_RF_Video_15'),(407,0,'tdk_integration','E2E_RMF_RF_Video_16'),(408,0,'tdk_integration','E2E_RMF_RF_Video_17'),(409,0,'tdk_integration','E2E_RMF_RF_Video_18'),(410,0,'tdk_integration','E2E_RMF_simultaneous_recording'),(411,0,'tdk_integration','E2E_RMF_simultaneous_recording_liveplayback'),(412,0,'tdk_integration','E2E_RMF_standbymode_beforeRecording'),(413,0,'tdk_integration','E2E_RMF_switching_live_TSB'),(414,0,'tdk_integration','E2E_RMF_TSB_FFW_30x_07'),(415,0,'tdk_integration','E2E_RMF_TSB_FFW_60x_09'),(416,0,'tdk_integration','E2E_RMF_TSB_FFW_FFW_15x_15x_41'),(417,0,'tdk_integration','E2E_RMF_TSB_FFW_FFW_15x_4x_29'),(418,0,'tdk_integration','E2E_RMF_TSB_FFW_FFW_30x_15_42'),(419,0,'tdk_integration','E2E_RMF_TSB_FFW_FFW_30x_4x_31'),(420,0,'tdk_integration','E2E_RMF_TSB_FFW_FFW_60x_15x_44'),(421,0,'tdk_integration','E2E_RMF_TSB_FFW_FFW_60x_30x_51'),(422,0,'tdk_integration','E2E_RMF_TSB_FFW_FFW_60x_4x_33'),(423,0,'tdk_integration','E2E_RMF_TSB_FFW_FRW_15x_4x_35'),(424,0,'tdk_integration','E2E_RMF_TSB_FFW_FRW_30x_15x_46'),(425,0,'tdk_integration','E2E_RMF_TSB_FFW_FRW_30x_4x_37'),(426,0,'tdk_integration','E2E_RMF_TSB_FFW_FRW_60x_15x_48'),(427,0,'tdk_integration','E2E_RMF_TSB_FFW_FRW_60x_30x_53'),(428,0,'tdk_integration','E2E_RMF_TSB_FFW_FRW_60x_4x_39'),(429,0,'tdk_integration','E2E_RMF_TSB_FFW_SFW_15x_0.5x_14'),(430,0,'tdk_integration','E2E_RMF_TSB_FFW_SFW_30x_0.5x_16'),(431,0,'tdk_integration','E2E_RMF_TSB_FFW_SFW_4x_0.5x_12'),(432,0,'tdk_integration','E2E_RMF_TSB_FFW_SFW_60x_0.5x_18'),(433,0,'tdk_integration','E2E_RMF_TSB_FFW_SRW_15x_0.5x_22'),(434,0,'tdk_integration','E2E_RMF_TSB_FFW_SRW_30x_0.5x_24'),(435,0,'tdk_integration','E2E_RMF_TSB_FFW_SRW_4x_0.5x_20'),(436,0,'tdk_integration','E2E_RMF_TSB_FFW_SRW_60x_0.5x_26'),(437,0,'tdk_integration','E2E_RMF_TSB_FRW_15x_06'),(438,0,'tdk_integration','E2E_RMF_TSB_FRW_30x_08'),(439,0,'tdk_integration','E2E_RMF_TSB_FRW_60x_10'),(440,0,'tdk_integration','E2E_RMF_TSB_FRW_FFW_15x_4x_30'),(441,0,'tdk_integration','E2E_RMF_TSB_FRW_FFW_30x_15x_43'),(442,0,'tdk_integration','E2E_RMF_TSB_FRW_FFW_30x_4x_32'),(443,0,'tdk_integration','E2E_RMF_TSB_FRW_FFW_4x_4x_28'),(444,0,'tdk_integration','E2E_RMF_TSB_FRW_FFW_60x_15x_45'),(445,0,'tdk_integration','E2E_RMF_TSB_FRW_FFW_60x_30x_52'),(446,0,'tdk_integration','E2E_RMF_TSB_FRW_FFW_60x_4x_34'),(447,0,'tdk_integration','E2E_RMF_TSB_FRW_FFW_60x_55'),(448,0,'tdk_integration','E2E_RMF_TSB_FRW_FRW_ 60x_30x_54'),(449,0,'tdk_integration','E2E_RMF_TSB_FRW_FRW_15x_4x_36'),(450,0,'tdk_integration','E2E_RMF_TSB_FRW_FRW_30x_15x_47'),(451,0,'tdk_integration','E2E_RMF_TSB_FRW_FRW_30x_4x_38'),(452,0,'tdk_integration','E2E_RMF_TSB_FRW_FRW_60x_15x_49'),(453,0,'tdk_integration','E2E_RMF_TSB_FRW_FRW_60x_4x_40'),(454,0,'tdk_integration','E2E_RMF_TSB_FRW_SFW_15x_0.5x_15'),(455,0,'tdk_integration','E2E_RMF_TSB_FRW_SFW_30x_0.5x_17'),(456,0,'tdk_integration','E2E_RMF_TSB_FRW_SFW_4x_0.5x_13'),(457,0,'tdk_integration','E2E_RMF_TSB_FRW_SFW_60x_0.5x_19'),(458,0,'tdk_integration','E2E_RMF_TSB_FRW_SRW_15x_0.5x_23'),(459,0,'tdk_integration','E2E_RMF_TSB_FRW_SRW_30x_0.5x_25'),(460,0,'tdk_integration','E2E_RMF_TSB_FRW_SRW_4x_0.5x_21'),(461,0,'tdk_integration','E2E_RMF_TSB_FRW_SRW_60x_0.5x_27'),(462,0,'tdk_integration','E2E_RMF_TSB_FW_0.5x_01'),(463,0,'tdk_integration','E2E_RMF_TSB_FW_15x_05'),(464,0,'tdk_integration','E2E_RMF_TSB_FW_4x_03'),(465,0,'tdk_integration','E2E_RMF_TSB_FW_RW_0.5x_11'),(466,0,'tdk_integration','E2E_RMF_TSB_Recording'),(467,0,'tdk_integration','E2E_RMF_TSB_RFW_FFW_30x_30x_50'),(468,0,'tdk_integration','E2E_RMF_TSB_RW_0.5x_02'),(469,0,'tdk_integration','E2E_RMF_TSB_RW_4x_04'),(470,0,'openSource_components','Glib_Test'),(471,0,'gst-plugins-rdk','GstPluginRdk_Aesdecrypt_DecryptEnable_False'),(472,0,'gst-plugins-rdk','GstPluginRdk_Aesdecrypt_DecryptEnable_Get_Default'),(473,0,'gst-plugins-rdk','GstPluginRdk_Aesdecrypt_DecryptEnable_Invalid'),(474,0,'gst-plugins-rdk','GstPluginRdk_Aesdecrypt_DecryptEnable_Negative'),(475,0,'gst-plugins-rdk','GstPluginRdk_Aesdecrypt_DecryptEnable_True'),(476,0,'gst-plugins-rdk','GstPluginRdk_Aesencrypt_EncryptEnable_Get_Default'),(477,0,'gst-plugins-rdk','GstPluginRdk_Aesencrypt_EncryptionEnable_False'),(478,0,'gst-plugins-rdk','GstPluginRdk_Aesencrypt_EncryptionEnable_Invalid'),(479,0,'gst-plugins-rdk','GstPluginRdk_Aesencrypt_EncryptionEnable_Negative'),(480,0,'gst-plugins-rdk','GstPluginRdk_Aesencrypt_EncryptionEnable_True'),(481,0,'gst-plugins-rdk','GstPluginRdk_Dvrsink_Ccivalue_Get_Prop_Default'),(482,0,'gst-plugins-rdk','GstPluginRdk_Dvrsink_RecordId_Get_Prop_Default'),(483,0,'gst-plugins-rdk','GstPluginRdk_Dvrsink_RecordId_Set_Prop'),(484,0,'gst-plugins-rdk','GstPluginRdk_Dvrsrc_Ccivalue_Get_Prop_Default'),(485,0,'gst-plugins-rdk','GstPluginRdk_Dvrsrc_Duration_Get_Prop_Default'),(486,0,'gst-plugins-rdk','GstPluginRdk_Dvrsrc_PlayStartPosition_Get_Prop_Default'),(487,0,'gst-plugins-rdk','GstPluginRdk_Dvrsrc_PlayStartPosition_Set_Prop'),(488,0,'gst-plugins-rdk','GstPluginRdk_Dvrsrc_PlayStartPosition_Set_Prop_Negative'),(489,0,'gst-plugins-rdk','GstPluginRdk_Dvrsrc_Rate_Get_Prop_Default'),(490,0,'gst-plugins-rdk','GstPluginRdk_Dvrsrc_Rate_Set_Prop'),(491,0,'gst-plugins-rdk','GstPluginRdk_Dvrsrc_Rate_Set_Prop_ValueGreater_64'),(492,0,'gst-plugins-rdk','GstPluginRdk_Dvrsrc_Rate_Set_Prop_ValueLesser_Negative64'),(493,0,'gst-plugins-rdk','GstPluginRdk_Dvrsrc_RecordId_Get_Prop_Default'),(494,0,'gst-plugins-rdk','GstPluginRdk_Dvrsrc_RecordId_Set_Prop'),(495,0,'gst-plugins-rdk','GstPluginRdk_Dvrsrc_SegmentName_Get_Prop_Default'),(496,0,'gst-plugins-rdk','GstPluginRdk_Dvrsrc_SegmentName_Set_Prop'),(497,0,'gst-plugins-rdk','GstPluginRdk_Dvrsrc_StartTime_Get_Prop_Default'),(498,0,'openSource_components','GstreamerBasePluginTest'),(499,0,'openSource_components','GstreamerGoodPluginTest'),(500,0,'openSource_components','GstreamerTest'),(501,0,'iarmbus','IARMBUS Broadcast IR event'),(502,0,'iarmbus','IARMBUS Broadcast ResolutionChange Event test'),(503,0,'iarmbus','IARMBUS BusCall MFR- Provision Code test'),(504,0,'iarmbus','IARMBUS BusCall MFR-Board description test'),(505,0,'iarmbus','IARMBUS BusCall MFR-Board Product Class test'),(506,0,'iarmbus','IARMBUS BusCall MFR-First Use Date test'),(507,0,'iarmbus','IARMBUS BusCall MFR-Hardware version test'),(508,0,'iarmbus','IARMBUS BusCall MFR-Model Name test'),(509,0,'iarmbus','IARMBUS BusCall MFR-OUI test'),(510,0,'iarmbus','IARMBUS BusCall MFR-SerialNumber test'),(511,0,'iarmbus','IARMBUS BusCall MFR-Software version test'),(512,0,'iarmbus','IARMBUS BusCall MFR-STB Manufature Name test'),(513,0,'iarmbus','IARMBUS BusCall test'),(514,0,'iarmbus','IARMBUS Connect & Disconnect test'),(515,0,'iarmbus','IARMBUS Init Negative test'),(516,0,'iarmbus','IARMBUS IsConnected test'),(517,0,'iarmbus','IARMBUS Query Key Repeat Interval test'),(518,0,'iarmbus','IARMBUS Query Power state'),(519,0,'iarmbus','IARMBUS Register for Resource Available event test'),(520,0,'iarmbus','IARMBUS RegisterCall test'),(521,0,'iarmbus','IARMBUS RegisterEventMax'),(522,0,'iarmbus','IARMBUS Release Resource test'),(523,0,'iarmbus','IARMBUS Request decoder-0 test'),(524,0,'iarmbus','IARMBUS Request decoder-1 test'),(525,0,'iarmbus','IARMBUS Request display_resolution_change  test'),(526,0,'iarmbus','IARMBUS Request graphics plane-0 test'),(527,0,'iarmbus','IARMBUS Request graphics plane-1 test'),(528,0,'iarmbus','IARMBUS Request power  test'),(529,0,'iarmbus','IARMBUS Request same resource from same application test'),(530,0,'iarmbus','IARMBUS Request same resource in different application test'),(531,0,'iarmbus','IARMBUS Set Key Repeat Interval test'),(532,0,'iarmbus','IARMBUS Set Power state'),(533,0,'iarmbus','IARMBUS Unregister with out Register Event Handler test'),(534,0,'iarmbus','IARMBUS unregisterEvt Handler test'),(535,0,'iarmbus','IARMBUS_BusCall_MFR-DeletePDRI_image_61'),(536,0,'iarmbus','IARMBUS_BusCall_MFR-Device_MAC_58'),(537,0,'iarmbus','IARMBUS_BusCall_MFR-HDMIHDCP_60'),(538,0,'iarmbus','IARMBUS_BusCall_MFR-MOCA_MAC_59'),(539,0,'iarmbus','IARMBUS_BusCall_MFR-Scruballbanks_62'),(540,0,'iarmbus','IARMBUS_BusCall_MFR-Validateandwriteimage_into_flash_63'),(541,0,'iarmbus','IARMBUS_Disconnect_without_connect_55'),(542,0,'iarmbus','IARMBUS_DiskMgr_Event_HwDisk_18'),(543,0,'iarmbus','IARMBUS_DummyCall_Persistent_test'),(544,0,'iarmbus','IARMBUS_DummyEvt_Persistent_test'),(545,0,'iarmbus','IARMBUS_Init_with_Invalidparameter_test_43'),(546,0,'iarmbus','IARMBUS_Init_with_Invalid_App_test_44'),(547,0,'iarmbus','IARMBUS_IsConnected_Invalid_Membername_54'),(548,0,'iarmbus','IARMBUS_IsConnect_STRESS_57'),(549,0,'iarmbus','IARMBUS_IsConnect_Without_Connect_53'),(550,0,'iarmbus','IARMBUS_RegisterEvtHandler_With_NegId_48'),(551,0,'iarmbus','IARMBUS_RegisterEvtHandler_With_PosId_47'),(552,0,'iarmbus','IARMBUS_RegUnReg_STRESS_51'),(553,0,'iarmbus','IARMBUS_Release_Invalid_Resource_52'),(554,0,'iarmbus','IARMBUS_Request_FOCUS_Resource_50'),(555,0,'iarmbus','IARMBUS_Request_Invalid_Resource_49'),(556,0,'iarmbus','IARMBUS_Request_resource_STRESS_56'),(557,0,'iarmbus','IARMBUS_Reset_WareHouse_state_64'),(558,0,'iarmbus','IARMBUS_Term_Without_Init_42'),(559,0,'iarmbus','IARMBUS_unregisterEvtHandler_With_PosId_45'),(560,0,'iarmbus','IARM_BUS_DiskMgr_Event_ExtHDD_19'),(561,0,'iarmbus','IARM_BUS_DiskMgr_Event_ExtHDD_Off_22'),(562,0,'iarmbus','IARM_BUS_DiskMgr_Event_ExtHDD_On_21'),(563,0,'iarmbus','IARM_BUS_DiskMgr_Event_ExtHDD_Pair_20'),(564,0,'iarmbus','IARM_BUS_IRMgr_IRKey_ChangeChannelVol'),(565,0,'iarmbus','IARM_BUS_IRMgr_IRKey_CheckSearch'),(566,0,'iarmbus','IARM_BUS_IRMgr_IRKey_CheckSetup'),(567,0,'iarmbus','IARM_BUS_IRMgr_IRKey_CheckTrickplay'),(568,0,'iarmbus','IARM_BUS_IRMgr_IRKey_Toggle'),(569,0,'iarmbus','IARM_BUS_SysMgr_Event_Card_FwDNLD_73'),(570,0,'iarmbus','IARM_BUS_SysMgr_Event_HDCPProfile_update_74'),(571,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_70'),(572,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_BootUp_66'),(573,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_CableCardDWLD_99'),(574,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_CableCard_98'),(575,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_CableCard_SerialNo_104'),(576,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_CardCisco_Status_82'),(577,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_CASystem_90'),(578,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_ChannelMap_75'),(579,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_CMAC_79'),(580,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_CVRSubsystem_100'),(581,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_DACId_106'),(582,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_DAC_InitTimeStamp_103'),(583,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_DisconnectMGR_76'),(584,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_Docsis_95'),(585,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_Download_101'),(586,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_DsgBroadCastChannel_96'),(587,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_DSG_CATunnel_97'),(588,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_ECMIP_92'),(589,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_ECMMac_105'),(590,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_EstbIP_91'),(591,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_ExitOk_78'),(592,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_FirmwareDWLD_87'),(593,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_GetSetHDCPProfile_67'),(594,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_HDCPEnabled_85'),(595,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_HDCPProfileEvent_68'),(596,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_HDMIOut_84'),(597,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_HDMI_EDID_Ready_86'),(598,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_LANIP_93'),(599,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_Moca_94'),(600,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_MotoEntitlement_80'),(601,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_MotoHRVRX_81'),(602,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_PlantId_107'),(603,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_StbSerialNo_65'),(604,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_TimeSource_88'),(605,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_TimeZone_89'),(606,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_TuneReady_77'),(607,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_VideoPresenting_83'),(608,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_VOD_AD_102'),(609,0,'iarmbus','IARM_BUS_SysMgr_Event_XUPNP_Data_Request_71'),(610,0,'iarmbus','IARM_BUS_SysMgr_Event_XUPNP_Data_Update_72'),(611,0,'openSource_components','Jansson_Test'),(612,0,'openSource_components','libsoup_Test'),(613,0,'mediastreamer','MS_DVRTrickplay_Functionality_Test_09'),(614,0,'mediastreamer','MS_DVRTrickplay_Invalid_Playspeed_10'),(615,0,'mediastreamer','MS_DVRTrickplay_Invalid_Timeposition_11'),(616,0,'mediastreamer','MS_LiveTune_Improper_Requesturl_02'),(617,0,'mediastreamer','MS_LiveTune_Playback_07'),(618,0,'mediastreamer','MS_LiveTune_Valid_Request_01'),(619,0,'mediastreamer','MS_Recordedcontent_playback_08'),(620,0,'mediastreamer','MS_RecordingList_Format_Test_05'),(621,0,'mediastreamer','MS_Recording_Improper_Requesturl_04'),(622,0,'mediastreamer','MS_Recording_Metadata_Format_Test_06'),(623,0,'mediastreamer','MS_Recording_Request_03'),(624,0,'openSource_components','Openssl_Test'),(625,0,'openSource_components','Qt5Webkit_Test'),(626,0,'openSource_components','Qt5_Test'),(627,0,'openSource_components','QtTest_DirectFB'),(628,0,'openSource_components','QtTest_Intelce'),(629,0,'rdk_logger','RDKLogger_CheckMPELogEnabled'),(630,0,'rdk_logger','RDKLogger_Dbg_Enabled_Status'),(631,0,'rdk_logger','RDKLogger_EnvGet'),(632,0,'rdk_logger','RDKLogger_EnvGetModFromNum'),(633,0,'rdk_logger','RDKLogger_EnvGetNum'),(634,0,'rdk_logger','RDKLogger_EnvGetValueFromNum'),(635,0,'rdk_logger','RDKLogger_GetDefaultLevel'),(636,0,'rdk_logger','RDKLogger_GetEnv_UnknownModule'),(637,0,'rdk_logger','RDKLogger_GetLogLevel'),(638,0,'rdk_logger','RDKLogger_Init'),(639,0,'rdk_logger','RDKLogger_Log'),(640,0,'rdk_logger','RDKLogger_Log_All'),(641,0,'rdk_logger','RDKLogger_Log_All_None'),(642,0,'rdk_logger','RDKLogger_Log_Debug'),(643,0,'rdk_logger','RDKLogger_Log_DefaultLevel'),(644,0,'rdk_logger','RDKLogger_Log_Error'),(645,0,'rdk_logger','RDKLogger_Log_Fatal'),(646,0,'rdk_logger','RDKLogger_Log_Info'),(647,0,'rdk_logger','RDKLogger_Log_InvalidLevel'),(648,0,'rdk_logger','RDKLogger_Log_InverseLevel'),(649,0,'rdk_logger','RDKLogger_Log_InverseTrace'),(650,0,'rdk_logger','RDKLogger_Log_MPEOSDisabled'),(651,0,'rdk_logger','RDKLogger_Log_None'),(652,0,'rdk_logger','RDKLogger_Log_None_All'),(653,0,'rdk_logger','RDKLogger_Log_Notice'),(654,0,'rdk_logger','RDKLogger_Log_Trace'),(655,0,'rdk_logger','RDKLogger_Log_Trace1'),(656,0,'rdk_logger','RDKLogger_Log_Trace2'),(657,0,'rdk_logger','RDKLogger_Log_Trace3'),(658,0,'rdk_logger','RDKLogger_Log_Trace4'),(659,0,'rdk_logger','RDKLogger_Log_Trace5'),(660,0,'rdk_logger','RDKLogger_Log_Trace6'),(661,0,'rdk_logger','RDKLogger_Log_Trace7'),(662,0,'rdk_logger','RDKLogger_Log_Trace8'),(663,0,'rdk_logger','RDKLogger_Log_Trace9'),(664,0,'rdk_logger','RDKLogger_Log_UnknownModule'),(665,0,'rdk_logger','RDKLogger_Log_Warning'),(666,0,'rdk_logger','RDKLogger_MaxLogLine'),(667,0,'rdk_logger','RDKLogger_SetLogLevel'),(668,0,'recorder','RMFMS_ScheduleRecording_12'),(669,0,'recorder','RMFMS_ScheduleRecording_InvalidSRC_13'),(670,0,'recorder','RMFMS_Schedule_Big_Recording_14'),(671,0,'recorder','RMFMS_Schedule_FutureRecording_15'),(672,0,'recorder','RMFMS_Schedule_MinDuration_Recording_18'),(673,0,'recorder','RMFMS_Schedule_NegDuration_Recording_19'),(674,0,'recorder','RMFMS_Schedule_NegStartTime_Recording_20'),(675,0,'recorder','RMFMS_Schedule_SmallDuration_Recording_17'),(676,0,'recorder','RMFMS_Schedule_ZeroSize_Recording_16'),(677,0,'mediaframework','RMF_DVRManager_ConvertTSBToRecording'),(678,0,'mediaframework','RMF_DVRManager_CreateRecording'),(679,0,'mediaframework','RMF_DVRManager_CreateTSB'),(680,0,'mediaframework','RMF_DVRManager_DeleteRecording'),(681,0,'mediaframework','RMF_DVRManager_GetDefaultTSBMaxDuration'),(682,0,'mediaframework','RMF_DVRManager_GetIsRecordingInProgress'),(683,0,'mediaframework','RMF_DVRManager_GetRecordingCount'),(684,0,'mediaframework','RMF_DVRManager_GetRecordingDuration'),(685,0,'mediaframework','RMF_DVRManager_GetRecordingInfoById'),(686,0,'mediaframework','RMF_DVRManager_GetRecordingInfoById_17'),(687,0,'mediaframework','RMF_DVRManager_GetRecordingInfoByIndex'),(688,0,'mediaframework','RMF_DVRManager_GetRecordingInfoByIndex_16'),(689,0,'mediaframework','RMF_DVRManager_GetRecordingSegmentInfoByIndex'),(690,0,'mediaframework','RMF_DVRManager_GetRecordingSize'),(691,0,'mediaframework','RMF_DVRManager_GetRecordingStartTime'),(692,0,'mediaframework','RMF_DVRManager_GetSegmentsCount'),(693,0,'mediaframework','RMF_DVRManager_GetSpace'),(694,0,'mediaframework','RMF_DVRManager_UpdateRecording'),(695,0,'mediaframework','RMF_DVRSink_InitTerm_01'),(696,0,'mediaframework','RMF_DVRSrcMPSink_BackToBeg_04'),(697,0,'mediaframework','RMF_DVRSrcMPSink_ChangeSpeed_12'),(698,0,'mediaframework','RMF_DVRSrcMPSink_Pause_02'),(699,0,'mediaframework','RMF_DVRSrcMPSink_Play_01'),(700,0,'mediaframework','RMF_DVRSrcMPSink_Resume_03'),(701,0,'mediaframework','RMF_DVRSrcMPSink_SkipNumOfSeconds_SkipBack_06'),(702,0,'mediaframework','RMF_DVRSrcMPSink_SkipNumOfSeconds_SkipFront_07'),(703,0,'mediaframework','RMF_DVRSrcMPSink_SkipToEnd_05'),(704,0,'mediaframework','RMF_DVRSrcMPSink_TrickPlayRate_FF4x_08'),(705,0,'mediaframework','RMF_DVRSrcMPSink_TrickPlayRate_FF64x_09'),(706,0,'mediaframework','RMF_DVRSrcMPSink_TrickPlayRate_FR4x_10'),(707,0,'mediaframework','RMF_DVRSrcMPSink_TrickPlayRate_FR64x_11'),(708,0,'mediaframework','RMF_DVRSrc_GetMediaInfo_09'),(709,0,'mediaframework','RMF_DVRSrc_GetMediaTime_07'),(710,0,'mediaframework','RMF_DVRSrc_GetSetSpeed_06'),(711,0,'mediaframework','RMF_DVRSrc_GetSpeed_05'),(712,0,'mediaframework','RMF_DVRSrc_InitTerm_01'),(713,0,'mediaframework','RMF_DVRSrc_OpenClose_02'),(714,0,'mediaframework','RMF_DVRSrc_Open_10'),(715,0,'mediaframework','RMF_DVRSrc_Open_11'),(716,0,'mediaframework','RMF_DVRSrc_Open_12'),(717,0,'mediaframework','RMF_DVRSrc_Open_13'),(718,0,'mediaframework','RMF_DVRSrc_Open_14'),(719,0,'mediaframework','RMF_DVRSrc_Open_15'),(720,0,'mediaframework','RMF_DVRSrc_Open_16'),(721,0,'mediaframework','RMF_DVRSrc_Play_03'),(722,0,'mediaframework','RMF_DVRSrc_Play_04'),(723,0,'mediaframework','RMF_DVRSrc_SetMediaTime_08'),(724,0,'mediaframework','RMF_DVR_Get_Recording_List'),(725,0,'mediaframework','RMF_Gst_LongDuration_Check_GstBuffer_Crash_55'),(726,0,'mediaframework','RMF_Gst_LongDuration_Check_GstQamTune_Crash_56'),(727,0,'mediaframework','RMF_HNSink_01'),(728,0,'mediaframework','RMF_HNSrcMPSink_InvalidRewindSpeed_10'),(729,0,'mediaframework','RMF_HNSrcMPSink_InvalidSpeed_09'),(730,0,'mediaframework','RMF_HNSrcMPSink_Video_MuteUnmute_06'),(731,0,'mediaframework','RMF_HNSrcMPSink_Video_Pause_02'),(732,0,'mediaframework','RMF_HNSrcMPSink_Video_Play_01'),(733,0,'mediaframework','RMF_HNSrcMPSink_Video_Play_Position_04'),(734,0,'mediaframework','RMF_HNSrcMPSink_Video_Skip_Backward_03'),(735,0,'mediaframework','RMF_HNSrcMPSink_Video_Speed_08'),(736,0,'mediaframework','RMF_HNSrcMPSink_Video_State_05'),(737,0,'mediaframework','RMF_HNSrcMPSink_Video_Volume_07'),(738,0,'mediaframework','RMF_HNSrc_GetBufferedRanges_04'),(739,0,'mediaframework','RMF_HNSrc_GetState_05'),(740,0,'mediaframework','RMF_HNSrc_InitTerm_01'),(741,0,'mediaframework','RMF_HNSrc_MPSink_BufferClearing_17'),(742,0,'mediaframework','RMF_HNSrc_MPSink_ChannelChange_CheckMacroblocking_41'),(743,0,'mediaframework','RMF_HNSrc_MPSink_Clearbuffering&CheckMediaTime_18'),(744,0,'mediaframework','RMF_HNSrc_MPSink_DoublePlay_40'),(745,0,'mediaframework','RMF_HNSrc_MPSink_DVRReplay_37'),(746,0,'mediaframework','RMF_HNSrc_MPSink_DVR_FF_16x_30'),(747,0,'mediaframework','RMF_HNSrc_MPSink_DVR_FF_32x_29'),(748,0,'mediaframework','RMF_HNSrc_MPSink_DVR_FF_4x_31'),(749,0,'mediaframework','RMF_HNSrc_MPSink_DVR_FF_64x_32'),(750,0,'mediaframework','RMF_HNSrc_MPSink_DVR_FF_RW_CheckMacroblocking_42'),(751,0,'mediaframework','RMF_HNSrc_MPSink_DVR_FF_RW_SB_CheckMacroblocking_46'),(752,0,'mediaframework','RMF_HNSrc_MPSink_DVR_FF_RW_SF_CheckMacroblocking_44'),(753,0,'mediaframework','RMF_HNSrc_MPSink_DVR_Play_26'),(754,0,'mediaframework','RMF_HNSrc_MPSink_DVR_REW_16x_35'),(755,0,'mediaframework','RMF_HNSrc_MPSink_DVR_REW_32x_34'),(756,0,'mediaframework','RMF_HNSrc_MPSink_DVR_REW_4x_36'),(757,0,'mediaframework','RMF_HNSrc_MPSink_DVR_REW_64x_33'),(758,0,'mediaframework','RMF_HNSrc_MPSink_DVR_RW_FF_CheckMacroblocking_43'),(759,0,'mediaframework','RMF_HNSrc_MPSink_DVR_RW_FF_SB_CheckMacroblocking_47'),(760,0,'mediaframework','RMF_HNSrc_MPSink_DVR_RW_FF_SF_CheckMacroblocking_45'),(761,0,'mediaframework','RMF_HNSrc_MPSink_DVR_SB_SF_CheckMacroblocking_49'),(762,0,'mediaframework','RMF_HNSrc_MPSink_DVR_SF_SB_CheckMacroblocking_48'),(763,0,'mediaframework','RMF_HNSrc_MPSink_FF_16x_22'),(764,0,'mediaframework','RMF_HNSrc_MPSink_FF_32x_28'),(765,0,'mediaframework','RMF_HNSrc_MPSink_FF_4x_21'),(766,0,'mediaframework','RMF_HNSrc_MPSink_FF_64x_20'),(767,0,'mediaframework','RMF_HNSrc_MPSink_GetState_25'),(768,0,'mediaframework','RMF_HNSrc_MPSink_InvalidMediaTime_13'),(769,0,'mediaframework','RMF_HNSrc_MPSink_InvalidMediaTime_14'),(770,0,'mediaframework','RMF_HNSrc_MPSink_LivetsbReset_19'),(771,0,'mediaframework','RMF_HNSrc_MPSink_Pause&CheckMediaTime_15'),(772,0,'mediaframework','RMF_HNSrc_MPSink_Pause&FF_39'),(773,0,'mediaframework','RMF_HNSrc_MPSink_Pause&Rewind_38'),(774,0,'mediaframework','RMF_HNSrc_MPSink_Rewind&CheckSpeed_16'),(775,0,'mediaframework','RMF_HNSrc_MPSink_REW_16x_23'),(776,0,'mediaframework','RMF_HNSrc_MPSink_REW_4x_24'),(777,0,'mediaframework','RMF_HNSrc_MPSink_SetGetmediaTime_03'),(778,0,'mediaframework','RMF_HNSrc_MPSink_SetSpeed_32x_11'),(779,0,'mediaframework','RMF_HNSrc_MPSink_SetSpeed_64x_12'),(780,0,'mediaframework','RMF_HNSrc_MPSink_Startoftsb_27'),(781,0,'mediaframework','RMF_HNSrc_MPSink_TSB_ChangeResolution_Check_54'),(782,0,'mediaframework','RMF_HNSrc_MPSink_TSB_FF_CheckMacroblocking_50'),(783,0,'mediaframework','RMF_HNSrc_MPSink_TSB_FF_RW_CheckMacroblocking_51'),(784,0,'mediaframework','RMF_HNSrc_MPSink_TSB_SF_CheckMacroblocking_52'),(785,0,'mediaframework','RMF_HNSrc_MPSink_TSB_SF_CheckMacroblocking_53'),(786,0,'mediaframework','RMF_HNSrc_Open_Emptystring_06'),(787,0,'mediaframework','RMF_HNSrc_Open_invalidurl_07'),(788,0,'mediaframework','RMF_HNSrc_Open_validUrl_11'),(789,0,'mediaframework','RMF_HNSrc_Open_vodurl_08'),(790,0,'mediaframework','RMF_HNSrc_Play_DefaultSpeed_09'),(791,0,'mediaframework','RMF_HNSrc_Play_withoutopen_12'),(792,0,'mediaframework','RMF_HNSRC_Play_withoutsetsource_10'),(793,0,'mediaframework','RMF_HNSrc_SetGetSpeed_02'),(794,0,'mediaframework','RMF_MPSink_GetMediaTime_05'),(795,0,'mediaframework','RMF_MPSink_InitTerm_01'),(796,0,'mediaframework','RMF_MPSink_SetGetMute_03'),(797,0,'mediaframework','RMF_MPSink_SetGetVolume_04'),(798,0,'mediaframework','RMF_MPSink_SetVideoRectangle_02'),(799,0,'mediastreamer','RMF_MS_ContinousCH_Change_test'),(800,0,'mediastreamer','RMF_MS_ContionusDVR_Playback'),(801,0,'mediastreamer','RMF_MS_General_Error_Response'),(802,0,'mediastreamer','RMF_MS_Incomplete_URL_Request'),(803,0,'mediastreamer','RMF_MS_LivePlayback_test'),(804,0,'mediastreamer','RMF_MS_LiveTune_Request'),(805,0,'mediastreamer','RMF_MS_LongTime_LivePlayback'),(806,0,'mediastreamer','RMF_MS_RecordingPlayback'),(807,0,'mediastreamer','RMF_MS_Stress_LiveTune_Test'),(808,0,'mediastreamer','RMF_MS_Without_StreamInit'),(809,0,'mediaframework','RMF_QAMSource_ChangeChannelTwice_PlayOneHour_19'),(810,0,'mediaframework','RMF_QAMSource_ChangeChannel_Check_SPTS_Error_15'),(811,0,'mediaframework','RMF_QAMSource_ChangeChannel_FourTimes_16'),(812,0,'mediaframework','RMF_QAMSource_ChangeChannel_SevenTimes_17'),(813,0,'mediaframework','RMF_QAMSource_ChangeURI_11'),(814,0,'mediaframework','RMF_QAMSource_ChangeURI_14'),(815,0,'mediaframework','RMF_QAMSource_GetLtsId_06'),(816,0,'mediaframework','RMF_QAMSource_GetQAMSourceInstance_10'),(817,0,'mediaframework','RMF_QAMSource_GetTsId_05'),(818,0,'mediaframework','RMF_QAMSource_GetUseFactoryMethods_08'),(819,0,'mediaframework','RMF_QAMSource_Get_Free_LowLevelElement_09'),(820,0,'mediaframework','RMF_QAMSource_InitTerm_01'),(821,0,'mediaframework','RMF_QAMSource_Init_Uninit_Platform_07'),(822,0,'mediaframework','RMF_QAMSource_OpenClose_02'),(823,0,'mediaframework','RMF_QAMSource_Pause_04'),(824,0,'mediaframework','RMF_QAMSource_Pause_13'),(825,0,'mediaframework','RMF_QAMSource_PlayLive_OneHour_18'),(826,0,'mediaframework','RMF_QAMSource_Play_03'),(827,0,'mediaframework','RMF_QAMSource_Play_12'),(828,0,'mediaframework','RMF_QAMSrc_01'),(829,0,'mediaframework','RMF_QAMSrc_02'),(830,0,'mediaframework','RMF_QAMSrc_03'),(831,0,'mediaframework','RMF_QAMSrc_04'),(832,0,'mediaframework','RMF_QAMSrc_05'),(833,0,'mediaframework','RMF_QAMSrc_06'),(834,0,'mediaframework','RMF_QAMSrc_07'),(835,0,'mediaframework','RMF_QAMSrc_08'),(836,0,'mediaframework','RMF_QAMSrc_09'),(837,0,'mediaframework','RMF_QAMSrc_HNSink_01'),(838,0,'mediaframework','RMF_QAMSrc_HNSink_02'),(839,0,'mediaframework','RMF_QAMSrc_HNSink_03'),(840,0,'mediaframework','RMF_QAMSrc_HNSink_04'),(841,0,'mediaframework','RMF_QAMSrc_HNSink_05'),(842,0,'mediaframework','RMF_QAMSrc_HNSink_06'),(843,0,'mediaframework','RMF_QAMSrc_HNSink_07'),(844,0,'mediaframework','RMF_QAMSrc_HNSink_08'),(845,0,'mediaframework','RMF_QAMSrc_HNSink_09'),(846,0,'mediaframework','RMF_QAMSrc_HNSink_10'),(847,0,'mediaframework','RMF_QAMSrc_HNSink_11'),(848,0,'mediaframework','RMF_QAMSrc_HNSink_12'),(849,0,'mediaframework','RMF_QAMSrc_HNSink_13'),(850,0,'mediaframework','RMF_QAMSrc_HNSink_14'),(851,0,'servicemanager','SM_CreateService_All'),(852,0,'servicemanager','SM_DeviceSetting_GetDeviceInfo'),(853,0,'servicemanager','SM_DisplaySetting_SetZoomSettings'),(854,0,'servicemanager','SM_DoesServiceExist Negative test'),(855,0,'servicemanager','SM_DoesServiceExist_All'),(856,0,'servicemanager','SM_EnableMdvr test'),(857,0,'servicemanager','SM_EnableVpop test'),(858,0,'servicemanager','SM_GetGlobal Service test'),(859,0,'servicemanager','SM_GetGlobalService_All'),(860,0,'servicemanager','SM_GetRegisteredService test'),(861,0,'servicemanager','SM_GetSetting_All'),(862,0,'servicemanager','SM_RegisterForEvents test'),(863,0,'servicemanager','SM_RegisterService test'),(864,0,'servicemanager','SM_RegisterService_All'),(865,0,'servicemanager','SM_ScreenCapture_EventUpload'),(866,0,'servicemanager','SM_ScreenCapture_Upload'),(867,0,'servicemanager','SM_Services_GetName_All'),(868,0,'servicemanager','SM_SetApiVersion test'),(869,0,'servicemanager','SM_SetApiVersion_All'),(870,0,'servicemanager','SM_SetDeviceName test'),(871,0,'servicemanager','SM_SetResolution test'),(872,0,'servicemanager','SM_UnRegisterService test'),(873,0,'servicemanager','SM_UnRegisterService_All'),(874,0,'servicemanager','SM_WebSocket_EventsAll'),(875,0,'servicemanager','SM_WebSocket_GetBufferedAmount'),(876,0,'servicemanager','SM_WebSocket_GetProtocol'),(877,0,'servicemanager','SM_WebSocket_GetReadyState'),(878,0,'servicemanager','SM_WebSocket_GetUrl'),(879,0,'rmfapp','tdkRmfApp_CreateRecord'),(880,0,'tdk_integration','TDK_E2E_DVR_Playback_Trickplay_All_Recordings_LongDuration_8hr_test'),(881,0,'tdk_integration','TDK_E2E_LinearTV_Channelchange_LongDuration_8hr_test'),(882,0,'tdk_integration','TDK_E2E_LinearTv_LinearTrickplay_LongDuration_8hr_Test'),(883,0,'tdk_integration','TDK_E2E_LinearTv_SwitchingChannel_DVRForwardAndRewind_LongDuration_8hr_test'),(884,0,'tdk_integration','TDK_E2E_LinearTv_SwitchingChannel_DVRTrickplay_LongDuration_8hr_test'),(885,0,'tdk_integration','TDK_E2E_RMF_LinearTV_ChannelChange_Trickplay_LongDuration_8hr_test'),(886,0,'tdk_integration','TDK_RMF_ScheduleRecording_Playback_LongDuration_8hr_test'),(888,0,'newrmf','test_newrmf_play'),(889,0,'tr69','TR069_Get_DeviceAdditionalSoftwareVersion_09'),(890,0,'tr69','TR069_Get_DeviceDeviceInfoNegative_51'),(891,0,'tr69','TR069_Get_DeviceEthernetInterfaceDefaultDuplexMode_50'),(892,0,'tr69','TR069_Get_DeviceEthernetInterfaceDefaultEnable_44'),(893,0,'tr69','TR069_Get_DeviceEthernetInterfaceDefaultMACAddress_48'),(894,0,'tr69','TR069_Get_DeviceEthernetInterfaceDefaultMaxBitRate_49'),(895,0,'tr69','TR069_Get_DeviceEthernetInterfaceDefaultName_46'),(896,0,'tr69','TR069_Get_DeviceEthernetInterfaceDefaultStatus_45'),(897,0,'tr69','TR069_Get_DeviceEthernetInterfaceDefaultUpstream_47'),(898,0,'tr69','TR069_Get_DeviceEthernetInterfaceNumOfEntries_43'),(899,0,'tr69','TR069_Get_DeviceFirstUseDate_12'),(900,0,'tr69','TR069_Get_DeviceHardwareVersion_07'),(901,0,'tr69','TR069_Get_DeviceIPActivePortNumOfEntries_33'),(902,0,'tr69','TR069_Get_DeviceIPDefaultInterfaceEnable_34'),(903,0,'tr69','TR069_Get_DeviceIPDefaultInterfaceIPv4Enable_35'),(904,0,'tr69','TR069_Get_DeviceIPDefaultInterfaceLoopback_41'),(905,0,'tr69','TR069_Get_DeviceIPDefaultInterfaceMaxMTUSize_39'),(906,0,'tr69','TR069_Get_DeviceIPDefaultInterfaceName_37'),(907,0,'tr69','TR069_Get_DeviceIPDefaultInterfaceReset_38'),(908,0,'tr69','TR069_Get_DeviceIPDefaultInterfaceStatus_36'),(909,0,'tr69','TR069_Get_DeviceIPDefaultInterfaceType_40'),(910,0,'tr69','TR069_Get_DeviceIPInterfaceNumOfEntries_32'),(911,0,'tr69','TR069_Get_DeviceIPv4Capable_29'),(912,0,'tr69','TR069_Get_DeviceIPv4Enable_30'),(913,0,'tr69','TR069_Get_DeviceIPv4Status_31'),(914,0,'tr69','TR069_Get_DeviceManufacturerOUI_02'),(915,0,'tr69','TR069_Get_DeviceManufacturer_01'),(916,0,'tr69','TR069_Get_DeviceMemoryStatusFree_27'),(917,0,'tr69','TR069_Get_DeviceMemoryStatusTotal_26'),(918,0,'tr69','TR069_Get_DeviceMoCAInterfaceAssociatedDevice1NodeID_69'),(919,0,'tr69','TR069_Get_DeviceMoCAInterfaceAssociatedDeviceGetNodeID_Neg_70'),(920,0,'tr69','TR069_Get_DeviceMoCAInterfaceAssociatedDeviceNumberOfEntries_68'),(921,0,'tr69','TR069_Get_DeviceMoCAInterfaceCurrentVersion_64'),(922,0,'tr69','TR069_Get_DeviceMoCAInterfaceEnable_54'),(923,0,'tr69','TR069_Get_DeviceMoCAInterfaceFirmwareVersion_59'),(924,0,'tr69','TR069_Get_DeviceMoCAInterfaceHighestVersion_63'),(925,0,'tr69','TR069_Get_DeviceMoCAInterfaceLastChange_56'),(926,0,'tr69','TR069_Get_DeviceMoCAInterfaceMACAddress_58'),(927,0,'tr69','TR069_Get_DeviceMoCAInterfaceMaxBitRate_60'),(928,0,'tr69','TR069_Get_DeviceMoCAInterfaceMaxEgressBW_62'),(929,0,'tr69','TR069_Get_DeviceMoCAInterfaceMaxIngressBW_61'),(930,0,'tr69','TR069_Get_DeviceMoCAInterfaceMaxNodes_67'),(931,0,'tr69','TR069_Get_DeviceMoCAInterfaceNetworkCoordinator_65'),(932,0,'tr69','TR069_Get_DeviceMoCAInterfaceNodeID_66'),(933,0,'tr69','TR069_Get_DeviceMoCAInterfaceNumOfEntries_53'),(934,0,'tr69','TR069_Get_DeviceMoCAInterfaceQoSEgressNumFlows_71'),(935,0,'tr69','TR069_Get_DeviceMoCAInterfaceQoSFlowStats1FlowID_72'),(936,0,'tr69','TR069_Get_DeviceMoCAInterfaceStatus_55'),(937,0,'tr69','TR069_Get_DeviceMoCAInterfaceUpstream_57'),(938,0,'tr69','TR069_Get_DeviceModelName_03'),(939,0,'tr69','TR069_Get_DeviceProcessorArchitecture_25'),(940,0,'tr69','TR069_Get_DeviceProcessorNumOfEntries_17'),(941,0,'tr69','TR069_Get_DeviceProcessStatusCommandDefaultProcess_20'),(942,0,'tr69','TR069_Get_DeviceProcessStatusCPUTimeDefaultProcess_23'),(943,0,'tr69','TR069_Get_DeviceProcessStatusCPUUsage_18'),(944,0,'tr69','TR069_Get_DeviceProcessStatusPIDDefaultProcess_19'),(945,0,'tr69','TR069_Get_DeviceProcessStatusPriorityDefaultProcess_22'),(946,0,'tr69','TR069_Get_DeviceProcessStatusSizeDefaultProcess_21'),(947,0,'tr69','TR069_Get_DeviceProcessStatusStateDefaultProcess_24'),(948,0,'tr69','TR069_Get_DeviceProvisioningCode_10'),(949,0,'tr69','TR069_Get_DeviceSerialNumber_06'),(950,0,'tr69','TR069_Get_DeviceServicesSTBServiceComponentsHDMI1DisplayDeviceEEDID_81'),(951,0,'tr69','TR069_Get_DeviceServicesSTBServiceComponentsHDMI1DisplayDeviceStatus_80'),(952,0,'tr69','TR069_Get_DeviceServicesSTBServiceComponentsHDMI1Enable_75'),(953,0,'tr69','TR069_Get_DeviceServicesSTBServiceComponentsHDMI1Name_77'),(954,0,'tr69','TR069_Get_DeviceServicesSTBServiceComponentsHDMI1ResolutionMode_78'),(955,0,'tr69','TR069_Get_DeviceServicesSTBServiceComponentsHDMI1ResolutionValue_79'),(956,0,'tr69','TR069_Get_DeviceServicesSTBServiceComponentsHDMI1Status_76'),(957,0,'tr69','TR069_Get_DeviceServicesSTBServiceComponentsHDMINumberOfEntries_74'),(958,0,'tr69','TR069_Get_DeviceServicesSTBServiceComponentsVideoDecoder1ContentAspectRatio_85'),(959,0,'tr69','TR069_Get_DeviceServicesSTBServiceComponentsVideoDecoder1Name_84'),(960,0,'tr69','TR069_Get_DeviceServicesSTBServiceComponentsVideoDecoderNumberOfEntries_83'),(961,0,'tr69','TR069_Get_DeviceServicesSTBServiceNumberOfEntries_73'),(962,0,'tr69','TR069_Get_DeviceSevicesSTBServiceComponentsVideoDecoderName_Neg_86'),(963,0,'tr69','TR069_Get_DeviceSoftwareVersion_08'),(964,0,'tr69','TR069_Get_DeviceSTBServiceComponentsHDMIDisplayDevice_XCOM_EDID_82'),(965,0,'tr69','TR069_Get_DeviceUpTime_11'),(966,0,'tr69','TR069_Get_DeviceXCOMFirmwareFileName_15'),(967,0,'tr69','TR069_Get_DeviceXCOMPowerStatus_16'),(968,0,'tr69','TR069_Get_DeviceXCOMSTBIP_14'),(969,0,'tr69','TR069_Get_DeviceXCOMSTBMAC_13'),(970,0,'trm','TRM_CancelLive'),(971,0,'trm','TRM_CancelRecording'),(972,0,'trm','TRM_CT_14'),(973,0,'trm','TRM_CT_15'),(974,0,'trm','TRM_CT_16'),(975,0,'trm','TRM_CT_17'),(976,0,'trm','TRM_CT_18'),(977,0,'trm','TRM_CT_19'),(978,0,'trm','TRM_CT_20'),(979,0,'trm','TRM_CT_21'),(980,0,'trm','TRM_CT_22'),(981,0,'trm','TRM_CT_23'),(982,0,'trm','TRM_CT_24'),(983,0,'trm','TRM_CT_25'),(984,0,'trm','TRM_CT_26'),(985,0,'trm','TRM_CT_27'),(986,0,'trm','TRM_CT_28'),(987,0,'trm','TRM_CT_29'),(988,0,'trm','TRM_CT_30'),(989,0,'trm','TRM_CT_31'),(990,0,'trm','TRM_CT_32'),(991,0,'trm','TRM_CT_33'),(992,0,'trm','TRM_CT_34'),(993,0,'trm','TRM_CT_35'),(994,0,'trm','TRM_CT_36'),(995,0,'trm','TRM_CT_37'),(996,0,'trm','TRM_CT_38'),(997,0,'trm','TRM_CT_39'),(998,0,'trm','TRM_CT_40'),(999,0,'trm','TRM_CT_41'),(1000,0,'trm','TRM_CT_42'),(1001,0,'trm','TRM_CT_43'),(1002,0,'trm','TRM_GetAllReservations'),(1003,0,'trm','TRM_GetAllTunerIds'),(1004,0,'trm','TRM_GetAllTunerStates'),(1005,0,'trm','TRM_GetVersion'),(1007,0,'trm','TRM_TunerReserveAllForLive'),(1008,0,'trm','TRM_TunerReserveAllForRecord'),(1009,0,'trm','TRM_TunerReserveForHyBrid'),(1010,0,'trm','TRM_TunerReserveForLive'),(1011,0,'trm','TRM_TunerReserveForRecord'),(1012,0,'trm','TRM_ValidateTunerReservation'),(1013,0,'openSource_components','WebkitTest_DirectFB'),(1014,0,'openSource_components','WebkitTest_Intelce'),(1015,0,'openSource_components','yajl_Test'),(1019,0,'trm','TRM_ReleaseTunerReservation'),(1024,0,'iarmbus','IARMBUS_PowerModeToggle_Stress'),(1025,0,'tdk_integration','E2E_RMF_delete_liverecord_lessthanonemin'),(1026,0,'tdk_integration','E2E_RMF_delete_ongoingRecord_liverecord_Inprogress'),(1028,0,'tdk_integration','E2E_RMF_DVR_recording_liveStream_watching_liveStream'),(1029,0,'tdk_integration','E2E_RMF_delete_recordcontent_with_another_liverecord'),(1030,0,'tdk_integration','E2E_RMF_DVR_delete_recording'),(1031,0,'tdk_integration','E2E_RMF_DVR_delete_recording_trickplay'),(1032,0,'mediaframework','RMF_Hybrid_Test'),(1037,0,'mediaframework','RMF_DS_Resolution_Hang_Check_01'),(1038,1,'mediaframework','RMF_TSB_Check_Pause_Failure_02'),(1040,0,'mediaframework','RMF_TSB_SlowRewind_Error_Check_03'),(1042,0,NULL,'E2E_RMF_LIVEplayback_delete_recording'),(1043,0,'tdk_integration','E2E_RMF_LIVE_playback_delete_recording'),(1044,0,'mediaframework','RMF_DVRSrcMPSink_FF_Rewind_error_Check_04'),(1047,0,'mediaframework','RMF_TSB_FF_Play_FreezeError_Check_05'),(1050,0,'tdk_integration','DVR_sampletest'),(1052,0,'tdk_integration','E2E_RMF_FFW_LiveVideo'),(1053,0,'iarmbus','IARMBUS_PowerModeToggle_Trickplay'),(1054,0,'trm','TRM_CT_44'),(1055,0,'trm','TRM_CT_45'),(1056,0,'devicesettings','DS_SetTime_VALID_124'),(1057,0,'devicesettings','DS_SetTextBrightness_125'),(1058,0,'devicesettings','DS_Resolution480p_VideoPlay_126'),(1060,0,'tdk_integration','E2E_RMF_DVR_Playback_Gateway_Client'),(1061,0,'mediaframework','RMF_HNSrc_MPSink_DVR_RW_FF_CheckMacroblocking_57'),(1062,0,'mediaframework','RMF_DVRManager_DeleteInvalidRecordingId'),(1063,0,'openSource_components','GstreamerPluginCustomTest');
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
) ENGINE=InnoDB AUTO_INCREMENT=359 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `script_group`
--

LOCK TABLES `script_group` WRITE;
/*!40000 ALTER TABLE `script_group` DISABLE KEYS */;
INSERT INTO `script_group` VALUES (218,88,'closedcaption','FREE',NULL),(220,299,'tdk_integration','FREE',NULL),(221,9,'rmfapp','FREE',NULL),(222,19,'openSource_components','FREE',NULL),(223,143,'iarmbus','FREE',NULL),(224,25,'mediastreamer','FREE',NULL),(225,53,'rdk_logger','FREE',NULL),(226,13,'recorder','FREE',NULL),(227,199,'mediaframework','FREE',NULL),(228,58,'servicemanager','FREE',NULL),(229,5,'newrmf','FREE',NULL),(236,2001,'ComponentSuite','FREE',NULL),(237,3202,'IPClient-3Suite','FREE',NULL),(238,3502,'Hybrid-1Suite','FREE',NULL),(244,101,'tr69','FREE',NULL),(263,476,'E2ESuite','FREE',NULL),(273,32,'gst-plugins-rdk','FREE',NULL),(275,94,'trm','FREE',NULL),(295,2047,'RDK2.0_IPClient-3','FREE',NULL),(296,1259,'RDK1.3_Hybrid-1','FREE',NULL),(297,200,'RDK1.2_Hybrid-1','FREE',NULL),(298,3679,'RDK2.0_Hybrid-1','FREE',NULL),(299,868,'RDK1.3_IPClient-3','FREE',NULL),(300,206,'RDK1.2_IPClient-3','FREE',NULL),(321,136,'devicesettings','FREE',NULL),(323,15,'E2ESuite_LD','FREE',NULL),(324,12,'IPClient-3Suite_LD','FREE',NULL),(325,19,'Hybrid-1Suite_LD','FREE',NULL),(326,76,'RDK2.0_IPClient-3_LD','FREE',NULL),(327,149,'RDK2.0_Hybrid-1_LD','FREE',NULL),(328,7,'mediaframework_LD','FREE',NULL),(329,7,'ComponentSuite_LD','FREE',NULL),(330,14,'dtcp','FREE',NULL),(331,17,'xupnp','FREE',NULL),(339,4,'Hybrid-5Suite','FREE',NULL),(340,4,'RDK1.3_Hybrid-5','FREE',NULL),(341,4,'RDK2.0_Hybrid-5','FREE',NULL),(342,3,'tdk_integration_LD','FREE',NULL),(347,2,'RDK1.2_Hybrid-5','FREE',NULL);
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
INSERT INTO `script_group_script_file` VALUES (218,23,0),(218,41,1),(218,17,2),(218,60,3),(218,14,4),(218,34,5),(218,21,6),(218,65,7),(218,59,8),(218,5,9),(218,36,10),(218,56,11),(218,30,12),(218,51,13),(218,29,14),(218,77,15),(218,24,16),(218,12,17),(218,10,18),(218,75,19),(218,50,20),(218,40,21),(218,70,22),(218,20,23),(218,31,24),(218,16,25),(218,72,26),(218,9,27),(218,15,28),(218,18,29),(218,52,30),(218,69,31),(218,7,32),(218,27,33),(218,6,34),(218,13,35),(218,55,36),(218,81,37),(218,76,38),(218,54,39),(218,74,40),(218,11,41),(218,61,42),(218,73,43),(218,38,44),(218,28,45),(218,19,46),(218,71,47),(218,78,48),(218,39,49),(218,58,50),(218,62,51),(218,32,52),(218,8,53),(218,63,54),(218,57,55),(218,66,56),(218,26,57),(218,53,58),(218,25,59),(218,42,60),(218,22,61),(218,64,62),(218,80,63),(218,35,64),(218,4,65),(218,33,66),(218,68,67),(218,67,68),(218,79,69),(218,37,70),(218,43,71),(218,44,72),(218,45,73),(218,46,74),(218,47,75),(218,48,76),(218,49,77),(236,582,0),(236,649,1),(236,507,2),(236,910,3),(236,506,4),(236,128,5),(236,938,6),(236,587,7),(236,941,8),(236,538,9),(236,584,10),(236,945,11),(236,535,12),(236,915,13),(236,892,14),(236,899,15),(236,588,16),(236,968,17),(236,585,18),(236,728,19),(236,132,20),(236,590,21),(236,540,22),(236,13,23),(236,900,24),(236,593,25),(236,73,26),(236,939,27),(236,660,28),(236,905,29),(236,537,30),(236,680,31),(236,647,32),(236,610,33),(236,136,34),(236,667,35),(236,130,36),(236,661,37),(236,891,38),(236,156,39),(236,911,40),(236,799,41),(236,215,42),(236,140,43),(236,947,44),(236,569,45),(236,501,46),(236,897,47),(236,127,48),(236,511,49),(236,589,50),(236,664,51),(236,602,52),(236,912,53),(236,504,54),(236,607,55),(236,134,56),(236,579,57),(236,542,58),(236,914,59),(236,216,60),(236,596,61),(236,637,62),(236,40,63),(236,641,64),(236,608,65),(236,901,66),(236,574,67),(236,580,68),(236,658,69),(236,599,70),(236,889,71),(236,217,72),(236,916,73),(236,218,74),(236,753,75),(236,644,76),(236,635,77),(236,179,78),(236,895,79),(236,648,80),(236,942,81),(236,967,82),(236,581,83),(236,777,84),(236,657,85),(236,58,86),(236,898,87),(236,896,88),(236,601,89),(236,570,90),(236,598,91),(236,212,92),(236,64,93),(236,503,94),(236,557,95),(236,603,96),(236,536,97),(236,563,98),(236,741,99),(236,571,100),(236,135,101),(236,34,102),(236,949,103),(236,909,104),(236,575,105),(236,65,106),(236,124,107),(236,126,108),(236,906,109),(236,969,110),(236,800,111),(236,894,112),(236,768,113),(236,643,114),(236,576,115),(236,773,116),(236,508,117),(236,965,118),(236,125,119),(236,560,120),(236,663,121),(236,214,122),(236,732,123),(236,591,124),(236,573,125),(236,532,126),(236,505,127),(236,512,128),(236,908,129),(236,636,130),(236,652,131),(236,561,132),(236,133,133),(236,653,134),(236,907,135),(236,890,136),(236,770,137),(236,592,138),(236,577,139),(236,662,140),(236,604,141),(236,572,142),(236,946,143),(236,630,144),(236,605,145),(236,902,146),(236,963,147),(236,729,148),(236,642,149),(236,913,150),(236,943,151),(236,646,152),(236,640,153),(236,131,154),(236,651,155),(236,966,156),(236,656,157),(236,948,158),(236,510,159),(236,650,160),(236,893,161),(236,594,162),(236,665,163),(236,609,164),(236,27,165),(236,659,166),(236,655,167),(236,600,168),(236,917,169),(236,595,170),(236,539,171),(236,645,172),(236,666,173),(236,562,174),(236,61,175),(236,940,176),(236,904,177),(236,654,178),(236,509,179),(236,63,180),(236,769,181),(236,586,182),(236,597,183),(236,944,184),(236,129,185),(236,606,186),(236,629,187),(236,578,188),(236,583,189),(236,903,190),(236,738,191),(236,544,192),(236,543,193),(236,772,194),(236,779,195),(236,803,196),(236,805,197),(236,806,198),(236,808,199),(236,514,200),(236,558,201),(236,516,202),(236,515,203),(236,475,204),(236,471,205),(236,473,206),(236,502,207),(236,513,208),(236,517,209),(236,518,210),(236,519,211),(236,520,212),(236,521,213),(236,522,214),(236,523,215),(236,524,216),(236,525,217),(236,526,218),(236,527,219),(236,528,220),(236,529,221),(236,530,222),(236,531,223),(236,533,224),(236,534,225),(236,541,226),(236,545,227),(236,546,228),(236,547,229),(236,548,230),(236,549,231),(236,550,232),(236,551,233),(236,552,234),(236,553,235),(236,554,236),(236,555,237),(236,556,238),(236,559,239),(236,1004,240),(236,146,241),(236,122,242),(236,1003,243),(236,1002,244),(236,1005,245),(236,822,246),(236,1011,247),(236,1010,248),(236,474,249),(236,480,250),(236,477,251),(236,478,252),(236,479,253),(236,476,254),(236,494,255),(236,495,256),(236,484,257),(236,490,258),(236,491,259),(236,492,260),(236,489,261),(236,497,262),(236,3,263),(236,487,264),(236,488,265),(236,486,266),(236,2,267),(236,482,268),(236,481,269),(236,1,270),(236,493,271),(236,496,272),(236,730,273),(236,731,274),(236,733,275),(236,734,276),(236,735,277),(236,1012,278),(236,736,279),(236,737,280),(236,744,281),(236,43,282),(236,971,283),(236,745,284),(236,746,285),(236,747,286),(236,748,287),(236,749,288),(236,44,289),(236,754,290),(236,755,291),(236,45,292),(236,756,293),(236,757,294),(236,763,295),(236,764,296),(236,765,297),(236,766,298),(236,767,299),(236,780,300),(236,46,301),(236,970,302),(236,778,303),(236,776,304),(236,775,305),(236,774,306),(236,47,307),(236,771,308),(236,48,309),(236,49,310),(236,120,311),(236,201,312),(236,202,313),(236,203,314),(236,204,315),(236,205,316),(236,631,317),(236,833,318),(236,826,319),(236,823,320),(236,831,321),(236,813,322),(236,827,323),(236,824,324),(236,814,325),(236,819,326),(236,689,327),(236,933,328),(236,964,329),(236,699,330),(236,79,331),(236,922,332),(236,936,333),(236,925,334),(236,937,335),(236,863,336),(236,864,337),(236,852,338),(236,872,339),(236,873,340),(236,926,341),(236,866,342),(236,923,343),(236,855,344),(236,875,345),(236,876,346),(236,927,347),(236,877,348),(236,878,349),(236,929,350),(236,928,351),(236,924,352),(236,921,353),(236,931,354),(236,932,355),(236,207,356),(236,930,357),(236,920,358),(236,918,359),(236,934,360),(236,935,361),(236,961,362),(236,957,363),(236,952,364),(236,956,365),(236,953,366),(236,954,367),(236,955,368),(236,951,369),(236,859,370),(236,950,371),(236,960,372),(236,959,373),(236,958,374),(236,810,375),(236,206,376),(236,861,377),(236,851,378),(236,867,379),(236,825,380),(236,119,381),(236,809,382),(236,811,383),(236,812,384),(236,568,385),(236,211,386),(236,108,387),(236,228,388),(236,137,389),(236,121,390),(236,123,391),(236,113,392),(236,138,393),(236,139,394),(236,919,395),(236,564,396),(236,567,397),(236,565,398),(236,566,399),(236,962,400),(236,111,401),(236,114,402),(236,869,403),(236,865,404),(236,874,405),(236,853,406),(236,854,407),(236,856,408),(236,857,409),(236,858,410),(236,860,411),(236,862,412),(236,868,413),(236,870,414),(236,871,415),(236,148,416),(236,815,417),(236,816,418),(236,817,419),(236,818,420),(236,820,421),(236,821,422),(236,828,423),(236,829,424),(236,830,425),(236,832,426),(236,834,427),(236,835,428),(236,836,429),(236,117,430),(236,704,431),(236,705,432),(236,706,433),(236,707,434),(236,700,435),(236,972,436),(236,804,437),(236,801,438),(236,802,439),(236,973,440),(236,634,441),(236,979,442),(236,742,443),(236,750,444),(236,758,445),(236,752,446),(236,760,447),(236,751,448),(236,759,449),(236,977,450),(236,762,451),(236,761,452),(236,782,453),(236,783,454),(236,784,455),(236,785,456),(236,7,457),(236,781,458),(236,1001,459),(236,981,460),(236,983,461),(236,982,462),(236,991,463),(236,992,464),(236,82,465),(236,93,466),(236,978,467),(236,94,468),(236,1000,469),(236,95,470),(236,96,471),(236,97,472),(236,997,473),(236,989,474),(236,98,475),(236,99,476),(236,990,477),(236,100,478),(236,988,479),(236,985,480),(236,101,481),(236,102,482),(236,103,483),(236,104,484),(236,105,485),(236,996,486),(236,106,487),(236,995,488),(236,83,489),(236,84,490),(236,85,491),(236,86,492),(236,87,493),(236,88,494),(236,89,495),(236,90,496),(236,91,497),(236,92,498),(236,987,499),(236,975,500),(236,976,501),(236,980,502),(236,984,503),(236,986,504),(236,999,505),(236,998,506),(236,993,507),(236,994,508),(236,164,509),(236,165,510),(236,166,511),(236,167,512),(236,168,513),(236,169,514),(236,170,515),(236,152,516),(236,153,517),(236,154,518),(236,155,519),(236,157,520),(236,1007,521),(236,1009,522),(236,1008,523),(236,974,524),(236,1019,525),(329,725,0),(329,726,1),(321,107,0),(321,108,1),(321,109,2),(321,110,3),(321,111,4),(321,112,5),(321,113,6),(321,114,7),(321,115,8),(321,116,9),(321,117,10),(321,118,11),(321,119,12),(321,120,13),(321,121,14),(321,122,15),(321,123,16),(321,124,17),(321,125,18),(321,126,19),(321,127,20),(321,128,21),(321,129,22),(321,130,23),(321,131,24),(321,132,25),(321,133,26),(321,134,27),(321,135,28),(321,136,29),(321,137,30),(321,138,31),(321,139,32),(321,140,33),(321,141,34),(321,142,35),(321,143,36),(321,144,37),(321,145,38),(321,146,39),(321,147,40),(321,148,41),(321,149,42),(321,150,43),(321,151,44),(321,152,45),(321,153,46),(321,154,47),(321,155,48),(321,156,49),(321,157,50),(321,158,51),(321,159,52),(321,160,53),(321,161,54),(321,162,55),(321,163,56),(321,164,57),(321,165,58),(321,166,59),(321,167,60),(321,168,61),(321,169,62),(321,170,63),(321,171,64),(321,172,65),(321,173,66),(321,174,67),(321,175,68),(321,176,69),(321,177,70),(321,178,71),(321,179,72),(321,180,73),(321,181,74),(321,182,75),(321,183,76),(321,184,77),(321,185,78),(321,186,79),(321,187,80),(321,188,81),(321,189,82),(321,190,83),(321,191,84),(321,192,85),(321,193,86),(321,194,87),(321,195,88),(321,196,89),(321,197,90),(321,198,91),(321,199,92),(321,200,93),(321,201,94),(321,202,95),(321,203,96),(321,204,97),(321,205,98),(321,206,99),(321,207,100),(321,208,101),(321,209,102),(321,210,103),(321,211,104),(321,212,105),(321,213,106),(321,214,107),(321,215,108),(321,216,109),(321,217,110),(321,218,111),(321,219,112),(321,220,113),(321,221,114),(321,222,115),(321,223,116),(321,224,117),(321,225,118),(321,226,119),(321,227,120),(321,228,121),(330,82,0),(330,83,1),(330,84,2),(330,85,3),(330,86,4),(330,87,5),(330,88,6),(330,89,7),(330,90,8),(330,91,9),(330,92,10),(263,358,0),(263,359,1),(263,285,2),(263,286,3),(263,287,4),(263,288,5),(263,289,6),(263,290,7),(263,291,8),(263,292,9),(263,293,10),(263,294,11),(263,295,12),(263,296,13),(263,297,14),(263,298,15),(263,299,16),(263,300,17),(263,301,18),(263,302,19),(263,303,20),(263,304,21),(263,305,22),(263,306,23),(263,307,24),(263,308,25),(263,309,26),(263,310,27),(263,311,28),(263,312,29),(263,313,30),(263,314,31),(263,315,32),(263,316,33),(263,317,34),(263,318,35),(263,319,36),(263,320,37),(263,321,38),(263,322,39),(263,323,40),(263,324,41),(263,325,42),(263,326,43),(263,327,44),(263,328,45),(263,329,46),(263,330,47),(263,331,48),(263,332,49),(263,342,50),(263,343,51),(263,344,52),(263,345,53),(263,346,54),(263,347,55),(263,348,56),(263,349,57),(263,350,58),(263,351,59),(263,352,60),(263,353,61),(263,360,62),(263,361,63),(263,362,64),(263,363,65),(263,394,66),(263,395,67),(263,396,68),(263,397,69),(263,398,70),(263,399,71),(263,400,72),(263,401,73),(263,402,74),(263,403,75),(263,404,76),(263,405,77),(263,406,78),(263,407,79),(263,408,80),(263,409,81),(263,414,82),(263,415,83),(263,416,84),(263,417,85),(263,418,86),(263,419,87),(263,420,88),(263,421,89),(263,422,90),(263,423,91),(263,424,92),(263,425,93),(263,426,94),(263,427,95),(263,428,96),(263,429,97),(263,430,98),(263,431,99),(263,432,100),(263,433,101),(263,434,102),(263,435,103),(263,436,104),(263,437,105),(263,438,106),(263,439,107),(263,440,108),(263,441,109),(263,442,110),(263,443,111),(263,444,112),(263,445,113),(263,446,114),(263,447,115),(263,448,116),(263,449,117),(263,450,118),(263,451,119),(263,452,120),(263,453,121),(263,454,122),(263,455,123),(263,456,124),(263,457,125),(263,458,126),(263,459,127),(263,460,128),(263,461,129),(263,462,130),(263,463,131),(263,464,132),(263,465,133),(263,467,134),(263,468,135),(263,469,136),(263,369,137),(263,377,138),(263,375,139),(263,388,140),(263,382,141),(263,367,142),(263,366,143),(263,368,144),(263,374,145),(263,386,146),(263,373,147),(263,338,148),(263,337,149),(263,339,150),(263,340,151),(263,341,152),(263,365,153),(263,364,154),(263,273,155),(263,274,156),(263,275,157),(263,879,158),(263,336,159),(263,390,160),(263,391,161),(263,281,162),(263,282,163),(263,335,164),(263,279,165),(263,283,166),(263,280,167),(263,333,168),(263,372,169),(263,393,170),(263,412,171),(263,466,172),(263,277,173),(263,392,174),(263,371,175),(263,410,176),(263,389,177),(263,284,178),(263,411,179),(263,334,180),(263,387,181),(263,278,182),(263,413,183),(263,276,184),(263,357,185),(263,1025,186),(323,880,0),(323,884,1),(323,883,2),(323,882,3),(323,885,4),(323,354,5),(323,355,6),(323,356,7),(323,881,8),(323,886,9),(273,475,0),(273,471,1),(273,473,2),(273,474,3),(273,480,4),(273,477,5),(273,478,6),(273,479,7),(273,476,8),(273,494,9),(273,495,10),(273,484,11),(273,490,12),(273,491,13),(273,492,14),(273,489,15),(273,497,16),(273,3,17),(273,487,18),(273,488,19),(273,486,20),(273,2,21),(273,482,22),(273,481,23),(273,1,24),(273,493,25),(273,496,26),(238,536,0),(238,297,1),(238,563,2),(238,582,3),(238,741,4),(238,571,5),(238,135,6),(238,328,7),(238,298,8),(238,649,9),(238,288,10),(238,34,11),(238,575,12),(238,65,13),(238,128,14),(238,332,15),(238,295,16),(238,587,17),(238,310,18),(238,538,19),(238,306,20),(238,584,21),(238,315,22),(238,800,23),(238,768,24),(238,289,25),(238,643,26),(238,535,27),(238,773,28),(238,576,29),(238,299,30),(238,324,31),(238,329,32),(238,320,33),(238,300,34),(238,588,35),(238,585,36),(238,728,37),(238,590,38),(238,540,39),(238,13,40),(238,318,41),(238,560,42),(238,663,43),(238,214,44),(238,593,45),(238,732,46),(238,305,47),(238,591,48),(238,573,49),(238,73,50),(238,660,51),(238,316,52),(238,537,53),(238,647,54),(238,532,55),(238,512,56),(238,636,57),(238,321,58),(238,610,59),(238,652,60),(238,136,61),(238,667,62),(238,291,63),(238,322,64),(238,130,65),(238,561,66),(238,653,67),(238,661,68),(238,286,69),(238,592,70),(238,293,71),(238,304,72),(238,577,73),(238,323,74),(238,662,75),(238,799,76),(238,604,77),(238,215,78),(238,572,79),(238,140,80),(238,287,81),(238,569,82),(238,630,83),(238,326,84),(238,501,85),(238,605,86),(238,330,87),(238,127,88),(238,319,89),(238,729,90),(238,589,91),(238,642,92),(238,664,93),(238,602,94),(238,311,95),(238,325,96),(238,607,97),(238,134,98),(238,579,99),(238,542,100),(238,646,101),(238,301,102),(238,640,103),(238,216,104),(238,131,105),(238,651,106),(238,596,107),(238,637,108),(238,641,109),(238,40,110),(238,656,111),(238,608,112),(238,309,113),(238,580,114),(238,574,115),(238,599,116),(238,650,117),(238,658,118),(238,594,119),(238,290,120),(238,665,121),(238,609,122),(238,217,123),(238,27,124),(238,659,125),(238,655,126),(238,218,127),(238,753,128),(238,600,129),(238,595,130),(238,644,131),(238,539,132),(238,314,133),(238,645,134),(238,666,135),(238,327,136),(238,294,137),(238,562,138),(238,635,139),(238,61,140),(238,179,141),(238,302,142),(238,317,143),(238,648,144),(238,581,145),(238,777,146),(238,58,147),(238,331,148),(238,654,149),(238,769,150),(238,63,151),(238,586,152),(238,312,153),(238,597,154),(238,303,155),(238,292,156),(238,601,157),(238,598,158),(238,570,159),(238,313,160),(238,212,161),(238,285,162),(238,307,163),(238,64,164),(238,296,165),(238,129,166),(238,606,167),(238,629,168),(238,578,169),(238,583,170),(238,557,171),(238,308,172),(238,603,173),(238,738,174),(238,369,175),(238,544,176),(238,543,177),(238,358,178),(238,359,179),(238,772,180),(238,779,181),(238,803,182),(238,805,183),(238,806,184),(238,808,185),(238,514,186),(238,558,187),(238,516,188),(238,515,189),(238,475,190),(238,471,191),(238,473,192),(238,502,193),(238,513,194),(238,517,195),(238,518,196),(238,519,197),(238,520,198),(238,521,199),(238,522,200),(238,523,201),(238,524,202),(238,525,203),(238,526,204),(238,527,205),(238,528,206),(238,529,207),(238,530,208),(238,531,209),(238,533,210),(238,534,211),(238,541,212),(238,545,213),(238,546,214),(238,547,215),(238,548,216),(238,549,217),(238,551,218),(238,552,219),(238,553,220),(238,554,221),(238,555,222),(238,556,223),(238,559,224),(238,1004,225),(238,146,226),(238,124,227),(238,122,228),(238,125,229),(238,126,230),(238,132,231),(238,133,232),(238,1003,233),(238,1005,234),(238,822,235),(238,1011,236),(238,1010,237),(238,474,238),(238,480,239),(238,477,240),(238,478,241),(238,479,242),(238,476,243),(238,494,244),(238,495,245),(238,484,246),(238,490,247),(238,491,248),(238,492,249),(238,489,250),(238,497,251),(238,3,252),(238,487,253),(238,488,254),(238,486,255),(238,2,256),(238,482,257),(238,481,258),(238,1,259),(238,493,260),(238,496,261),(238,730,262),(238,731,263),(238,342,264),(238,343,265),(238,344,266),(238,345,267),(238,346,268),(238,347,269),(238,348,270),(238,349,271),(238,350,272),(238,351,273),(238,352,274),(238,353,275),(238,360,276),(238,361,277),(238,362,278),(238,414,279),(238,415,280),(238,416,281),(238,417,282),(238,418,283),(238,419,284),(238,420,285),(238,421,286),(238,422,287),(238,423,288),(238,424,289),(238,425,290),(238,426,291),(238,427,292),(238,428,293),(238,429,294),(238,430,295),(238,431,296),(238,432,297),(238,433,298),(238,434,299),(238,435,300),(238,436,301),(238,437,302),(238,438,303),(238,439,304),(238,440,305),(238,441,306),(238,442,307),(238,443,308),(238,444,309),(238,445,310),(238,446,311),(238,447,312),(238,448,313),(238,449,314),(238,450,315),(238,451,316),(238,452,317),(238,453,318),(238,454,319),(238,455,320),(238,456,321),(238,457,322),(238,458,323),(238,459,324),(238,460,325),(238,461,326),(238,462,327),(238,463,328),(238,464,329),(238,465,330),(238,467,331),(238,468,332),(238,469,333),(238,733,334),(238,734,335),(238,735,336),(238,736,337),(238,737,338),(238,744,339),(238,43,340),(238,745,341),(238,746,342),(238,747,343),(238,748,344),(238,749,345),(238,44,346),(238,754,347),(238,755,348),(238,45,349),(238,756,350),(238,757,351),(238,763,352),(238,764,353),(238,765,354),(238,767,355),(238,780,356),(238,46,357),(238,778,358),(238,776,359),(238,775,360),(238,774,361),(238,47,362),(238,771,363),(238,48,364),(238,49,365),(238,120,366),(238,201,367),(238,202,368),(238,203,369),(238,204,370),(238,205,371),(238,631,372),(238,377,373),(238,833,374),(238,823,375),(238,831,376),(238,813,377),(238,827,378),(238,824,379),(238,814,380),(238,819,381),(238,689,382),(238,79,383),(238,375,384),(238,863,385),(238,388,386),(238,382,387),(238,864,388),(238,367,389),(238,366,390),(238,368,391),(238,852,392),(238,872,393),(238,873,394),(238,855,395),(238,875,396),(238,877,397),(238,374,398),(238,386,399),(238,373,400),(238,207,401),(238,859,402),(238,810,403),(238,206,404),(238,851,405),(238,867,406),(238,825,407),(238,119,408),(238,809,409),(238,811,410),(238,812,411),(238,568,412),(238,211,413),(238,121,414),(238,113,415),(238,273,416),(238,274,417),(238,275,418),(238,138,419),(238,564,420),(238,567,421),(238,565,422),(238,566,423),(238,111,424),(238,869,425),(238,865,426),(238,874,427),(238,853,428),(238,854,429),(238,856,430),(238,857,431),(238,858,432),(238,860,433),(238,862,434),(238,868,435),(238,870,436),(238,871,437),(238,336,438),(238,390,439),(238,148,440),(238,815,441),(238,816,442),(238,818,443),(238,821,444),(238,828,445),(238,829,446),(238,830,447),(238,832,448),(238,834,449),(238,835,450),(238,836,451),(238,117,452),(238,972,453),(238,804,454),(238,801,455),(238,802,456),(238,973,457),(238,634,458),(238,979,459),(238,742,460),(238,750,461),(238,758,462),(238,752,463),(238,760,464),(238,751,465),(238,759,466),(238,977,467),(238,762,468),(238,761,469),(238,782,470),(238,783,471),(238,784,472),(238,785,473),(238,7,474),(238,781,475),(238,1001,476),(238,981,477),(238,991,478),(238,391,479),(238,992,480),(238,281,481),(238,282,482),(238,335,483),(238,279,484),(238,283,485),(238,280,486),(238,333,487),(238,372,488),(238,393,489),(238,412,490),(238,466,491),(238,277,492),(238,392,493),(238,371,494),(238,410,495),(238,389,496),(238,284,497),(238,411,498),(238,334,499),(238,387,500),(238,93,501),(238,978,502),(238,278,503),(238,413,504),(238,1000,505),(238,96,506),(238,989,507),(238,990,508),(238,996,509),(238,995,510),(238,85,511),(238,86,512),(238,88,513),(238,91,514),(238,92,515),(238,987,516),(238,975,517),(238,976,518),(238,984,519),(238,998,520),(238,993,521),(238,994,522),(238,168,523),(238,1007,524),(238,1009,525),(238,1008,526),(238,974,527),(238,276,528),(238,879,529),(238,363,530),(238,338,531),(238,340,532),(238,337,533),(238,341,534),(238,357,535),(238,364,536),(238,365,537),(238,339,538),(238,114,539),(238,878,540),(238,1019,541),(238,982,542),(238,985,543),(238,988,544),(238,1012,545),(238,983,546),(238,986,547),(238,1002,548),(238,876,549),(238,866,550),(238,861,551),(238,638,552),(238,84,553),(238,94,554),(238,95,555),(238,97,556),(238,98,557),(238,103,558),(238,102,559),(238,101,560),(238,100,561),(238,105,562),(238,106,563),(238,104,564),(238,766,565),(238,657,566),(238,170,567),(238,826,568),(238,166,569),(238,1025,570),(238,1026,571),(238,1030,572),(238,970,573),(238,1032,574),(238,980,575),(238,997,576),(238,999,577),(238,971,578),(238,155,579),(238,1028,580),(238,157,581),(238,156,582),(238,154,583),(238,165,584),(238,164,585),(238,169,586),(238,153,587),(238,167,588),(238,1031,589),(238,149,590),(238,1043,591),(238,550,592),(238,699,593),(238,698,594),(238,700,595),(238,696,596),(238,703,597),(238,701,598),(238,702,599),(238,704,600),(238,705,601),(238,706,602),(238,707,603),(238,697,604),(238,713,605),(325,880,0),(325,884,1),(325,883,2),(325,882,3),(325,885,4),(325,354,5),(325,355,6),(325,356,7),(325,881,8),(325,886,9),(325,725,10),(325,726,11),(223,572,0),(223,527,1),(223,531,2),(223,552,3),(223,563,4),(223,569,5),(223,582,6),(223,501,7),(223,571,8),(223,605,9),(223,575,10),(223,555,11),(223,521,12),(223,589,13),(223,545,14),(223,534,15),(223,587,16),(223,546,17),(223,602,18),(223,584,19),(223,517,20),(223,607,21),(223,579,22),(223,502,23),(223,542,24),(223,576,25),(223,596,26),(223,553,27),(223,588,28),(223,608,29),(223,541,30),(223,515,31),(223,580,32),(223,574,33),(223,551,34),(223,599,35),(223,526,36),(223,548,37),(223,550,38),(223,525,39),(223,594,40),(223,585,41),(223,609,42),(223,519,43),(223,590,44),(223,556,45),(223,518,46),(223,560,47),(223,600,48),(223,595,49),(223,529,50),(223,593,51),(223,523,52),(223,530,53),(223,562,54),(223,591,55),(223,573,56),(223,528,57),(223,522,58),(223,581,59),(223,520,60),(223,532,61),(223,516,62),(223,524,63),(223,513,64),(223,514,65),(223,559,66),(223,586,67),(223,610,68),(223,597,69),(223,601,70),(223,598,71),(223,570,72),(223,561,73),(223,533,74),(223,606,75),(223,554,76),(223,578,77),(223,592,78),(223,583,79),(223,577,80),(223,547,81),(223,549,82),(223,558,83),(223,557,84),(223,604,85),(223,603,86),(223,503,87),(223,504,88),(223,505,89),(223,506,90),(223,507,91),(223,508,92),(223,509,93),(223,510,94),(223,511,95),(223,512,96),(223,536,97),(223,537,98),(223,538,99),(223,539,100),(223,535,101),(223,540,102),(223,568,103),(223,564,104),(223,567,105),(223,565,106),(223,566,107),(223,543,108),(223,544,109),(237,297,0),(237,582,1),(237,298,2),(237,288,3),(237,649,4),(237,507,5),(237,506,6),(237,128,7),(237,332,8),(237,587,9),(237,938,10),(237,310,11),(237,306,12),(237,538,13),(237,941,14),(237,584,15),(237,315,16),(237,945,17),(237,289,18),(237,915,19),(237,535,20),(237,324,21),(237,299,22),(237,329,23),(237,320,24),(237,588,25),(237,585,26),(237,590,27),(237,132,28),(237,540,29),(237,13,30),(237,318,31),(237,593,32),(237,73,33),(237,939,34),(237,660,35),(237,316,36),(237,537,37),(237,647,38),(237,321,39),(237,610,40),(237,136,41),(237,291,42),(237,667,43),(237,322,44),(237,661,45),(237,286,46),(237,215,47),(237,140,48),(237,947,49),(237,287,50),(237,569,51),(237,501,52),(237,330,53),(237,511,54),(237,589,55),(237,664,56),(237,602,57),(237,311,58),(237,504,59),(237,607,60),(237,134,61),(237,579,62),(237,914,63),(237,542,64),(237,301,65),(237,216,66),(237,596,67),(237,637,68),(237,40,69),(237,641,70),(237,608,71),(237,574,72),(237,580,73),(237,599,74),(237,658,75),(237,217,76),(237,916,77),(237,218,78),(237,644,79),(237,314,80),(237,294,81),(237,179,82),(237,635,83),(237,302,84),(237,648,85),(237,942,86),(237,581,87),(237,58,88),(237,601,89),(237,598,90),(237,570,91),(237,307,92),(237,212,93),(237,64,94),(237,503,95),(237,296,96),(237,557,97),(237,603,98),(237,536,99),(237,563,100),(237,571,101),(237,328,102),(237,135,103),(237,949,104),(237,34,105),(237,575,106),(237,65,107),(237,124,108),(237,126,109),(237,295,110),(237,643,111),(237,576,112),(237,300,113),(237,508,114),(237,965,115),(237,125,116),(237,560,117),(237,663,118),(237,214,119),(237,305,120),(237,591,121),(237,573,122),(237,532,123),(237,505,124),(237,512,125),(237,636,126),(237,652,127),(237,133,128),(237,561,129),(237,653,130),(237,592,131),(237,293,132),(237,304,133),(237,577,134),(237,323,135),(237,662,136),(237,604,137),(237,572,138),(237,946,139),(237,630,140),(237,326,141),(237,605,142),(237,319,143),(237,963,144),(237,642,145),(237,325,146),(237,943,147),(237,646,148),(237,640,149),(237,651,150),(237,656,151),(237,948,152),(237,309,153),(237,510,154),(237,650,155),(237,594,156),(237,290,157),(237,665,158),(237,609,159),(237,27,160),(237,659,161),(237,655,162),(237,600,163),(237,917,164),(237,595,165),(237,539,166),(237,645,167),(237,666,168),(237,327,169),(237,61,170),(237,562,171),(237,317,172),(237,940,173),(237,331,174),(237,654,175),(237,509,176),(237,63,177),(237,586,178),(237,312,179),(237,597,180),(237,303,181),(237,944,182),(237,292,183),(237,313,184),(237,285,185),(237,129,186),(237,606,187),(237,629,188),(237,578,189),(237,583,190),(237,308,191),(237,544,192),(237,543,193),(237,358,194),(237,359,195),(237,514,196),(237,558,197),(237,516,198),(237,515,199),(237,471,200),(237,473,201),(237,475,202),(237,502,203),(237,513,204),(237,517,205),(237,518,206),(237,519,207),(237,520,208),(237,521,209),(237,522,210),(237,523,211),(237,524,212),(237,525,213),(237,526,214),(237,527,215),(237,528,216),(237,529,217),(237,530,218),(237,531,219),(237,533,220),(237,534,221),(237,541,222),(237,545,223),(237,546,224),(237,547,225),(237,548,226),(237,549,227),(237,551,228),(237,552,229),(237,553,230),(237,554,231),(237,555,232),(237,556,233),(237,559,234),(237,146,235),(237,122,236),(237,130,237),(237,131,238),(237,127,239),(237,474,240),(237,480,241),(237,477,242),(237,478,243),(237,479,244),(237,476,245),(237,494,246),(237,495,247),(237,484,248),(237,490,249),(237,491,250),(237,492,251),(237,489,252),(237,497,253),(237,3,254),(237,487,255),(237,488,256),(237,486,257),(237,2,258),(237,482,259),(237,481,260),(237,1,261),(237,493,262),(237,496,263),(237,342,264),(237,343,265),(237,344,266),(237,345,267),(237,346,268),(237,347,269),(237,348,270),(237,349,271),(237,350,272),(237,351,273),(237,352,274),(237,353,275),(237,360,276),(237,361,277),(237,362,278),(237,394,279),(237,395,280),(237,396,281),(237,397,282),(237,398,283),(237,399,284),(237,400,285),(237,401,286),(237,402,287),(237,403,288),(237,404,289),(237,405,290),(237,406,291),(237,407,292),(237,408,293),(237,409,294),(237,414,295),(237,415,296),(237,416,297),(237,417,298),(237,418,299),(237,419,300),(237,420,301),(237,421,302),(237,422,303),(237,423,304),(237,424,305),(237,425,306),(237,426,307),(237,427,308),(237,428,309),(237,429,310),(237,430,311),(237,431,312),(237,432,313),(237,433,314),(237,434,315),(237,435,316),(237,436,317),(237,437,318),(237,438,319),(237,439,320),(237,440,321),(237,441,322),(237,442,323),(237,443,324),(237,444,325),(237,445,326),(237,446,327),(237,447,328),(237,448,329),(237,449,330),(237,450,331),(237,451,332),(237,452,333),(237,453,334),(237,454,335),(237,455,336),(237,456,337),(237,457,338),(237,458,339),(237,459,340),(237,460,341),(237,461,342),(237,462,343),(237,463,344),(237,464,345),(237,465,346),(237,467,347),(237,468,348),(237,469,349),(237,43,350),(237,44,351),(237,45,352),(237,46,353),(237,47,354),(237,48,355),(237,49,356),(237,120,357),(237,201,358),(237,202,359),(237,203,360),(237,204,361),(237,205,362),(237,631,363),(237,933,364),(237,79,365),(237,936,366),(237,925,367),(237,375,368),(237,863,369),(237,864,370),(237,852,371),(237,872,372),(237,873,373),(237,926,374),(237,923,375),(237,855,376),(237,875,377),(237,927,378),(237,877,379),(237,929,380),(237,928,381),(237,924,382),(237,921,383),(237,931,384),(237,932,385),(237,207,386),(237,930,387),(237,920,388),(237,918,389),(237,961,390),(237,957,391),(237,952,392),(237,956,393),(237,954,394),(237,859,395),(237,960,396),(237,959,397),(237,206,398),(237,851,399),(237,867,400),(237,119,401),(237,568,402),(237,211,403),(237,121,404),(237,113,405),(237,138,406),(237,564,407),(237,567,408),(237,565,409),(237,566,410),(237,111,411),(237,869,412),(237,865,413),(237,874,414),(237,336,415),(237,390,416),(237,148,417),(237,117,418),(237,634,419),(237,7,420),(237,391,421),(237,281,422),(237,282,423),(237,335,424),(237,279,425),(237,283,426),(237,280,427),(237,333,428),(237,372,429),(237,393,430),(237,412,431),(237,466,432),(237,277,433),(237,392,434),(237,371,435),(237,410,436),(237,389,437),(237,284,438),(237,411,439),(237,334,440),(237,387,441),(237,278,442),(237,413,443),(237,168,444),(237,363,445),(237,338,446),(237,340,447),(237,337,448),(237,341,449),(237,357,450),(237,364,451),(237,365,452),(237,339,453),(237,114,454),(237,889,455),(237,893,456),(237,894,457),(237,895,458),(237,898,459),(237,899,460),(237,900,461),(237,901,462),(237,905,463),(237,906,464),(237,910,465),(237,911,466),(237,912,467),(237,913,468),(237,638,469),(237,657,470),(237,170,471),(237,892,472),(237,896,473),(237,897,474),(237,902,475),(237,903,476),(237,904,477),(237,907,478),(237,166,479),(237,908,480),(237,909,481),(237,922,482),(237,966,483),(237,967,484),(237,968,485),(237,969,486),(237,891,487),(237,964,488),(237,935,489),(237,934,490),(237,937,491),(237,953,492),(237,955,493),(237,1032,494),(237,951,495),(237,962,496),(237,919,497),(237,958,498),(237,155,499),(237,157,500),(237,156,501),(237,154,502),(237,165,503),(237,164,504),(237,169,505),(237,153,506),(237,167,507),(237,950,508),(237,890,509),(237,149,510),(237,550,511),(237,1024,512),(237,123,513),(237,1057,514),(324,880,0),(324,884,1),(324,883,2),(324,882,3),(324,885,4),(324,355,5),(324,881,6),(227,684,0),(227,796,1),(227,689,2),(227,702,3),(227,775,4),(227,741,5),(227,815,6),(227,772,7),(227,838,8),(227,692,9),(227,694,10),(227,816,11),(227,710,12),(227,831,13),(227,765,14),(227,791,15),(227,824,16),(227,737,17),(227,768,18),(227,754,19),(227,850,20),(227,773,21),(227,819,22),(227,836,23),(227,774,24),(227,846,25),(227,813,26),(227,744,27),(227,685,28),(227,730,29),(227,746,30),(227,835,31),(227,755,32),(227,828,33),(227,727,34),(227,728,35),(227,757,36),(227,832,37),(227,718,38),(227,789,39),(227,687,40),(227,814,41),(227,686,42),(227,732,43),(227,834,44),(227,763,45),(227,715,46),(227,734,47),(227,690,48),(227,697,49),(227,723,50),(227,794,51),(227,680,52),(227,721,53),(227,733,54),(227,683,55),(227,749,56),(227,822,57),(227,756,58),(227,780,59),(227,779,60),(227,704,61),(227,823,62),(227,795,63),(227,720,64),(227,714,65),(227,731,66),(227,837,67),(227,736,68),(227,770,69),(227,849,70),(227,842,71),(227,821,72),(227,719,73),(227,681,74),(227,682,75),(227,678,76),(227,787,77),(227,797,78),(227,793,79),(227,729,80),(227,695,81),(227,833,82),(227,844,83),(227,735,84),(227,712,85),(227,776,86),(227,792,87),(227,679,88),(227,843,89),(227,820,90),(227,764,91),(227,747,92),(227,708,93),(227,827,94),(227,840,95),(227,696,96),(227,743,97),(227,748,98),(227,716,99),(227,845,100),(227,841,101),(227,771,102),(227,724,103),(227,753,104),(227,701,105),(227,848,106),(227,705,107),(227,688,108),(227,826,109),(227,839,110),(227,722,111),(227,717,112),(227,706,113),(227,830,114),(227,788,115),(227,709,116),(227,739,117),(227,777,118),(227,707,119),(227,766,120),(227,847,121),(227,745,122),(227,786,123),(227,700,124),(227,713,125),(227,698,126),(227,769,127),(227,740,128),(227,817,129),(227,829,130),(227,798,131),(227,677,132),(227,693,133),(227,778,134),(227,818,135),(227,767,136),(227,703,137),(227,711,138),(227,790,139),(227,691,140),(227,699,141),(227,738,142),(227,810,143),(227,825,144),(227,809,145),(227,811,146),(227,812,147),(227,742,148),(227,750,149),(227,758,150),(227,752,151),(227,760,152),(227,751,153),(227,759,154),(227,762,155),(227,761,156),(227,782,157),(227,783,158),(227,784,159),(227,785,160),(227,781,161),(328,725,0),(328,726,1),(224,616,0),(224,617,1),(224,615,2),(224,622,3),(224,806,4),(224,619,5),(224,623,6),(224,803,7),(224,613,8),(224,807,9),(224,804,10),(224,805,11),(224,614,12),(224,800,13),(224,808,14),(224,620,15),(224,618,16),(224,799,17),(224,621,18),(224,801,19),(224,802,20),(229,888,0),(222,626,0),(222,1015,1),(222,498,2),(222,470,3),(222,1014,4),(222,612,5),(222,624,6),(222,625,7),(222,628,8),(222,500,9),(222,611,10),(222,1013,11),(222,499,12),(222,627,13),(297,4,0),(297,5,1),(297,6,2),(297,8,3),(297,9,4),(297,10,5),(297,11,6),(297,12,7),(297,13,8),(297,14,9),(297,15,10),(297,16,11),(297,18,12),(297,19,13),(297,20,14),(297,21,15),(297,22,16),(297,23,17),(297,24,18),(297,25,19),(297,26,20),(297,27,21),(297,28,22),(297,29,23),(297,30,24),(297,31,25),(297,32,26),(297,33,27),(297,34,28),(297,35,29),(297,36,30),(297,37,31),(297,38,32),(297,39,33),(297,40,34),(297,41,35),(297,42,36),(297,44,37),(297,47,38),(297,48,39),(297,49,40),(297,50,41),(297,51,42),(297,52,43),(297,53,44),(297,54,45),(297,55,46),(297,56,47),(297,57,48),(297,58,49),(297,59,50),(297,60,51),(297,61,52),(297,62,53),(297,63,54),(297,64,55),(297,65,56),(297,66,57),(297,67,58),(297,68,59),(297,69,60),(297,70,61),(297,71,62),(297,72,63),(297,73,64),(297,74,65),(297,75,66),(297,76,67),(297,77,68),(297,78,69),(297,79,70),(297,80,71),(297,81,72),(297,273,73),(297,274,74),(297,275,75),(297,613,76),(297,614,77),(297,615,78),(297,616,79),(297,617,80),(297,618,81),(297,619,82),(297,620,83),(297,621,84),(297,622,85),(297,623,86),(297,628,87),(297,1014,88),(297,138,89),(297,7,90),(297,276,91),(297,1024,92),(300,4,0),(300,5,1),(300,6,2),(300,8,3),(300,9,4),(300,10,5),(300,11,6),(300,12,7),(300,13,8),(300,14,9),(300,15,10),(300,16,11),(300,18,12),(300,19,13),(300,20,14),(300,21,15),(300,22,16),(300,23,17),(300,24,18),(300,25,19),(300,26,20),(300,27,21),(300,28,22),(300,29,23),(300,30,24),(300,31,25),(300,32,26),(300,33,27),(300,34,28),(300,35,29),(300,36,30),(300,37,31),(300,38,32),(300,39,33),(300,40,34),(300,41,35),(300,42,36),(300,44,37),(300,47,38),(300,48,39),(300,49,40),(300,50,41),(300,51,42),(300,52,43),(300,53,44),(300,54,45),(300,55,46),(300,56,47),(300,57,48),(300,58,49),(300,59,50),(300,60,51),(300,61,52),(300,62,53),(300,63,54),(300,64,55),(300,65,56),(300,66,57),(300,67,58),(300,68,59),(300,69,60),(300,70,61),(300,71,62),(300,72,63),(300,73,64),(300,74,65),(300,75,66),(300,76,67),(300,77,68),(300,78,69),(300,79,70),(300,80,71),(300,81,72),(300,230,73),(300,231,74),(300,232,75),(300,233,76),(300,234,77),(300,235,78),(300,236,79),(300,237,80),(300,238,81),(300,239,82),(300,240,83),(300,241,84),(300,242,85),(300,243,86),(300,244,87),(300,245,88),(300,246,89),(300,247,90),(300,248,91),(300,259,92),(300,260,93),(300,261,94),(300,262,95),(300,263,96),(300,264,97),(300,265,98),(300,266,99),(300,267,100),(300,268,101),(300,269,102),(300,270,103),(300,271,104),(300,272,105),(300,627,106),(300,1013,107),(300,138,108),(300,7,109),(300,1024,110),(296,4,0),(296,5,1),(296,6,2),(296,8,3),(296,9,4),(296,10,5),(296,11,6),(296,12,7),(296,13,8),(296,14,9),(296,15,10),(296,16,11),(296,17,12),(296,18,13),(296,19,14),(296,20,15),(296,21,16),(296,22,17),(296,23,18),(296,24,19),(296,25,20),(296,26,21),(296,27,22),(296,28,23),(296,29,24),(296,30,25),(296,31,26),(296,32,27),(296,33,28),(296,34,29),(296,35,30),(296,36,31),(296,37,32),(296,38,33),(296,39,34),(296,40,35),(296,41,36),(296,42,37),(296,44,38),(296,47,39),(296,48,40),(296,49,41),(296,50,42),(296,51,43),(296,52,44),(296,53,45),(296,54,46),(296,55,47),(296,56,48),(296,57,49),(296,58,50),(296,59,51),(296,60,52),(296,61,53),(296,62,54),(296,63,55),(296,64,56),(296,65,57),(296,66,58),(296,67,59),(296,68,60),(296,69,61),(296,70,62),(296,71,63),(296,72,64),(296,73,65),(296,74,66),(296,75,67),(296,76,68),(296,77,69),(296,78,70),(296,79,71),(296,80,72),(296,81,73),(296,107,74),(296,109,75),(296,110,76),(296,111,77),(296,112,78),(296,115,79),(296,116,80),(296,118,81),(296,119,82),(296,141,83),(296,142,84),(296,143,85),(296,144,86),(296,145,87),(296,146,88),(296,147,89),(296,150,90),(296,151,91),(296,158,92),(296,159,93),(296,160,94),(296,161,95),(296,162,96),(296,163,97),(296,171,98),(296,172,99),(296,173,100),(296,174,101),(296,175,102),(296,176,103),(296,177,104),(296,178,105),(296,179,106),(296,180,107),(296,181,108),(296,182,109),(296,183,110),(296,184,111),(296,185,112),(296,186,113),(296,187,114),(296,188,115),(296,189,116),(296,190,117),(296,191,118),(296,192,119),(296,193,120),(296,194,121),(296,195,122),(296,196,123),(296,197,124),(296,198,125),(296,199,126),(296,200,127),(296,206,128),(296,207,129),(296,208,130),(296,209,131),(296,210,132),(296,211,133),(296,212,134),(296,213,135),(296,214,136),(296,215,137),(296,216,138),(296,217,139),(296,218,140),(296,219,141),(296,220,142),(296,221,143),(296,222,144),(296,223,145),(296,224,146),(296,225,147),(296,226,148),(296,227,149),(296,249,150),(296,250,151),(296,251,152),(296,252,153),(296,253,154),(296,254,155),(296,255,156),(296,256,157),(296,257,158),(296,258,159),(296,470,160),(296,498,161),(296,499,162),(296,500,163),(296,501,164),(296,502,165),(296,513,166),(296,516,167),(296,517,168),(296,518,169),(296,519,170),(296,520,171),(296,521,172),(296,522,173),(296,523,174),(296,524,175),(296,525,176),(296,526,177),(296,527,178),(296,528,179),(296,529,180),(296,530,181),(296,531,182),(296,533,183),(296,534,184),(296,541,185),(296,542,186),(296,543,187),(296,544,188),(296,547,189),(296,548,190),(296,549,191),(296,551,192),(296,552,193),(296,553,194),(296,554,195),(296,555,196),(296,556,197),(296,557,198),(296,559,199),(296,560,200),(296,561,201),(296,562,202),(296,563,203),(296,564,204),(296,565,205),(296,566,206),(296,567,207),(296,568,208),(296,569,209),(296,570,210),(296,571,211),(296,572,212),(296,573,213),(296,574,214),(296,575,215),(296,576,216),(296,577,217),(296,578,218),(296,579,219),(296,580,220),(296,581,221),(296,583,222),(296,584,223),(296,585,224),(296,586,225),(296,588,226),(296,589,227),(296,590,228),(296,591,229),(296,592,230),(296,593,231),(296,594,232),(296,595,233),(296,596,234),(296,597,235),(296,598,236),(296,599,237),(296,600,238),(296,601,239),(296,602,240),(296,604,241),(296,605,242),(296,606,243),(296,607,244),(296,608,245),(296,609,246),(296,610,247),(296,611,248),(296,612,249),(296,613,250),(296,614,251),(296,615,252),(296,616,253),(296,617,254),(296,618,255),(296,619,256),(296,620,257),(296,621,258),(296,622,259),(296,623,260),(296,624,261),(296,625,262),(296,626,263),(296,630,264),(296,631,265),(296,632,266),(296,633,267),(296,635,268),(296,636,269),(296,637,270),(296,639,271),(296,640,272),(296,641,273),(296,643,274),(296,644,275),(296,645,276),(296,647,277),(296,648,278),(296,649,279),(296,650,280),(296,651,281),(296,652,282),(296,654,283),(296,655,284),(296,656,285),(296,658,286),(296,660,287),(296,661,288),(296,662,289),(296,663,290),(296,664,291),(296,665,292),(296,666,293),(296,851,294),(296,853,295),(296,854,296),(296,855,297),(296,856,298),(296,857,299),(296,858,300),(296,859,301),(296,860,302),(296,862,303),(296,863,304),(296,865,305),(296,867,306),(296,868,307),(296,869,308),(296,870,309),(296,871,310),(296,872,311),(296,873,312),(296,874,313),(296,875,314),(296,877,315),(296,1003,316),(296,1004,317),(296,1005,318),(296,1015,319),(296,532,320),(296,148,321),(296,582,322),(296,515,323),(296,558,324),(296,545,325),(296,546,326),(296,122,327),(296,117,328),(296,124,329),(296,125,330),(296,126,331),(296,127,332),(296,128,333),(296,130,334),(296,131,335),(296,132,336),(296,133,337),(296,134,338),(296,667,339),(296,135,340),(296,136,341),(296,138,342),(296,140,343),(296,129,344),(296,603,345),(296,634,346),(296,646,347),(296,642,348),(296,1010,349),(296,7,350),(296,659,351),(296,653,352),(296,587,353),(296,113,354),(296,629,355),(296,514,356),(296,121,357),(296,201,358),(296,202,359),(296,203,360),(296,204,361),(296,205,362),(296,120,363),(296,168,364),(296,1011,365),(296,972,366),(296,1007,367),(296,1009,368),(296,1008,369),(296,973,370),(296,974,371),(296,975,372),(296,976,373),(296,977,374),(296,979,375),(296,978,376),(296,981,377),(296,984,378),(296,987,379),(296,989,380),(296,990,381),(296,991,382),(296,992,383),(296,993,384),(296,994,385),(296,998,386),(296,1000,387),(296,1001,388),(296,995,389),(296,996,390),(296,114,391),(296,982,392),(296,985,393),(296,988,394),(296,1012,395),(296,983,396),(296,986,397),(296,1002,398),(296,866,399),(296,861,400),(296,638,401),(296,657,402),(296,170,403),(296,166,404),(296,970,405),(296,980,406),(296,997,407),(296,999,408),(296,971,409),(296,155,410),(296,157,411),(296,156,412),(296,154,413),(296,165,414),(296,164,415),(296,169,416),(296,153,417),(296,167,418),(296,149,419),(296,550,420),(296,1024,421),(296,123,422),(296,1057,423),(296,139,424),(296,152,425),(299,4,0),(299,5,1),(299,6,2),(299,8,3),(299,9,4),(299,10,5),(299,11,6),(299,12,7),(299,13,8),(299,14,9),(299,15,10),(299,16,11),(299,17,12),(299,18,13),(299,19,14),(299,20,15),(299,21,16),(299,22,17),(299,23,18),(299,24,19),(299,25,20),(299,26,21),(299,27,22),(299,28,23),(299,29,24),(299,30,25),(299,31,26),(299,32,27),(299,33,28),(299,34,29),(299,35,30),(299,36,31),(299,37,32),(299,38,33),(299,39,34),(299,40,35),(299,41,36),(299,42,37),(299,44,38),(299,47,39),(299,48,40),(299,49,41),(299,50,42),(299,51,43),(299,52,44),(299,53,45),(299,54,46),(299,55,47),(299,56,48),(299,57,49),(299,58,50),(299,59,51),(299,60,52),(299,61,53),(299,62,54),(299,63,55),(299,64,56),(299,65,57),(299,66,58),(299,67,59),(299,68,60),(299,69,61),(299,70,62),(299,71,63),(299,72,64),(299,73,65),(299,74,66),(299,75,67),(299,76,68),(299,77,69),(299,78,70),(299,79,71),(299,80,72),(299,81,73),(299,107,74),(299,109,75),(299,110,76),(299,111,77),(299,112,78),(299,115,79),(299,116,80),(299,118,81),(299,119,82),(299,141,83),(299,142,84),(299,143,85),(299,144,86),(299,145,87),(299,146,88),(299,147,89),(299,150,90),(299,151,91),(299,158,92),(299,159,93),(299,160,94),(299,161,95),(299,162,96),(299,163,97),(299,171,98),(299,172,99),(299,173,100),(299,174,101),(299,175,102),(299,176,103),(299,177,104),(299,178,105),(299,179,106),(299,180,107),(299,181,108),(299,182,109),(299,183,110),(299,184,111),(299,185,112),(299,186,113),(299,187,114),(299,188,115),(299,189,116),(299,190,117),(299,191,118),(299,192,119),(299,193,120),(299,194,121),(299,195,122),(299,196,123),(299,197,124),(299,198,125),(299,199,126),(299,200,127),(299,206,128),(299,207,129),(299,208,130),(299,209,131),(299,210,132),(299,211,133),(299,212,134),(299,213,135),(299,214,136),(299,215,137),(299,216,138),(299,217,139),(299,218,140),(299,219,141),(299,220,142),(299,221,143),(299,222,144),(299,223,145),(299,224,146),(299,225,147),(299,226,148),(299,227,149),(299,230,150),(299,231,151),(299,232,152),(299,233,153),(299,234,154),(299,235,155),(299,236,156),(299,237,157),(299,238,158),(299,239,159),(299,240,160),(299,241,161),(299,242,162),(299,243,163),(299,244,164),(299,245,165),(299,246,166),(299,247,167),(299,248,168),(299,259,169),(299,260,170),(299,261,171),(299,262,172),(299,263,173),(299,264,174),(299,265,175),(299,266,176),(299,267,177),(299,268,178),(299,269,179),(299,270,180),(299,271,181),(299,272,182),(299,402,183),(299,405,184),(299,406,185),(299,470,186),(299,498,187),(299,499,188),(299,500,189),(299,501,190),(299,502,191),(299,503,192),(299,504,193),(299,505,194),(299,506,195),(299,507,196),(299,508,197),(299,509,198),(299,510,199),(299,511,200),(299,512,201),(299,513,202),(299,516,203),(299,517,204),(299,518,205),(299,519,206),(299,520,207),(299,521,208),(299,522,209),(299,523,210),(299,524,211),(299,525,212),(299,526,213),(299,527,214),(299,528,215),(299,529,216),(299,530,217),(299,531,218),(299,533,219),(299,534,220),(299,535,221),(299,536,222),(299,537,223),(299,538,224),(299,539,225),(299,540,226),(299,541,227),(299,542,228),(299,543,229),(299,544,230),(299,547,231),(299,548,232),(299,549,233),(299,551,234),(299,552,235),(299,553,236),(299,554,237),(299,555,238),(299,556,239),(299,557,240),(299,559,241),(299,560,242),(299,561,243),(299,562,244),(299,563,245),(299,564,246),(299,565,247),(299,566,248),(299,567,249),(299,568,250),(299,569,251),(299,570,252),(299,571,253),(299,572,254),(299,573,255),(299,574,256),(299,575,257),(299,576,258),(299,577,259),(299,578,260),(299,579,261),(299,580,262),(299,581,263),(299,583,264),(299,584,265),(299,585,266),(299,586,267),(299,588,268),(299,589,269),(299,590,270),(299,591,271),(299,592,272),(299,593,273),(299,594,274),(299,595,275),(299,596,276),(299,597,277),(299,598,278),(299,599,279),(299,600,280),(299,601,281),(299,602,282),(299,604,283),(299,605,284),(299,606,285),(299,607,286),(299,608,287),(299,609,288),(299,610,289),(299,611,290),(299,612,291),(299,624,292),(299,630,293),(299,631,294),(299,632,295),(299,633,296),(299,635,297),(299,636,298),(299,637,299),(299,639,300),(299,640,301),(299,641,302),(299,643,303),(299,644,304),(299,645,305),(299,647,306),(299,648,307),(299,649,308),(299,650,309),(299,651,310),(299,652,311),(299,654,312),(299,655,313),(299,656,314),(299,658,315),(299,660,316),(299,661,317),(299,662,318),(299,663,319),(299,664,320),(299,665,321),(299,666,322),(299,1015,323),(299,532,324),(299,148,325),(299,582,326),(299,515,327),(299,558,328),(299,545,329),(299,546,330),(299,122,331),(299,117,332),(299,124,333),(299,125,334),(299,126,335),(299,127,336),(299,128,337),(299,130,338),(299,131,339),(299,132,340),(299,133,341),(299,134,342),(299,667,343),(299,135,344),(299,136,345),(299,138,346),(299,140,347),(299,129,348),(299,603,349),(299,634,350),(299,646,351),(299,642,352),(299,7,353),(299,659,354),(299,653,355),(299,587,356),(299,113,357),(299,629,358),(299,514,359),(299,121,360),(299,201,361),(299,202,362),(299,203,363),(299,204,364),(299,205,365),(299,120,366),(299,168,367),(299,114,368),(299,638,369),(299,657,370),(299,170,371),(299,166,372),(299,155,373),(299,157,374),(299,156,375),(299,154,376),(299,165,377),(299,164,378),(299,169,379),(299,153,380),(299,167,381),(299,149,382),(299,550,383),(299,1024,384),(299,123,385),(299,1057,386),(299,139,387),(298,4,0),(298,5,1),(298,6,2),(298,8,3),(298,9,4),(298,10,5),(298,11,6),(298,12,7),(298,13,8),(298,14,9),(298,15,10),(298,16,11),(298,17,12),(298,18,13),(298,19,14),(298,20,15),(298,21,16),(298,22,17),(298,23,18),(298,24,19),(298,25,20),(298,26,21),(298,27,22),(298,28,23),(298,29,24),(298,30,25),(298,31,26),(298,32,27),(298,33,28),(298,34,29),(298,35,30),(298,36,31),(298,37,32),(298,38,33),(298,39,34),(298,40,35),(298,41,36),(298,42,37),(298,43,38),(298,44,39),(298,45,40),(298,46,41),(298,47,42),(298,48,43),(298,49,44),(298,50,45),(298,51,46),(298,52,47),(298,53,48),(298,54,49),(298,55,50),(298,56,51),(298,57,52),(298,58,53),(298,59,54),(298,60,55),(298,61,56),(298,62,57),(298,63,58),(298,64,59),(298,65,60),(298,66,61),(298,67,62),(298,68,63),(298,69,64),(298,70,65),(298,71,66),(298,72,67),(298,73,68),(298,74,69),(298,75,70),(298,76,71),(298,77,72),(298,78,73),(298,79,74),(298,80,75),(298,81,76),(298,107,77),(298,109,78),(298,110,79),(298,111,80),(298,112,81),(298,115,82),(298,116,83),(298,118,84),(298,119,85),(298,141,86),(298,142,87),(298,143,88),(298,144,89),(298,145,90),(298,146,91),(298,147,92),(298,150,93),(298,151,94),(298,158,95),(298,159,96),(298,160,97),(298,161,98),(298,162,99),(298,163,100),(298,171,101),(298,172,102),(298,173,103),(298,174,104),(298,175,105),(298,176,106),(298,177,107),(298,178,108),(298,179,109),(298,180,110),(298,181,111),(298,182,112),(298,183,113),(298,184,114),(298,185,115),(298,186,116),(298,187,117),(298,188,118),(298,189,119),(298,190,120),(298,191,121),(298,192,122),(298,193,123),(298,194,124),(298,195,125),(298,196,126),(298,197,127),(298,198,128),(298,199,129),(298,200,130),(298,206,131),(298,207,132),(298,208,133),(298,209,134),(298,210,135),(298,211,136),(298,212,137),(298,213,138),(298,214,139),(298,215,140),(298,216,141),(298,217,142),(298,218,143),(298,219,144),(298,220,145),(298,221,146),(298,222,147),(298,223,148),(298,224,149),(298,225,150),(298,226,151),(298,227,152),(298,286,153),(298,287,154),(298,288,155),(298,289,156),(298,290,157),(298,291,158),(298,292,159),(298,293,160),(298,294,161),(298,295,162),(298,296,163),(298,297,164),(298,298,165),(298,299,166),(298,300,167),(298,301,168),(298,302,169),(298,303,170),(298,304,171),(298,305,172),(298,307,173),(298,308,174),(298,309,175),(298,310,176),(298,311,177),(298,312,178),(298,313,179),(298,314,180),(298,315,181),(298,316,182),(298,317,183),(298,318,184),(298,319,185),(298,320,186),(298,321,187),(298,322,188),(298,323,189),(298,324,190),(298,325,191),(298,326,192),(298,327,193),(298,328,194),(298,329,195),(298,330,196),(298,331,197),(298,332,198),(298,342,199),(298,343,200),(298,344,201),(298,345,202),(298,346,203),(298,347,204),(298,348,205),(298,349,206),(298,350,207),(298,351,208),(298,352,209),(298,353,210),(298,358,211),(298,359,212),(298,360,213),(298,361,214),(298,362,215),(298,366,216),(298,367,217),(298,368,218),(298,370,219),(298,373,220),(298,374,221),(298,375,222),(298,376,223),(298,377,224),(298,378,225),(298,379,226),(298,380,227),(298,381,228),(298,382,229),(298,383,230),(298,384,231),(298,385,232),(298,386,233),(298,388,234),(298,414,235),(298,415,236),(298,416,237),(298,417,238),(298,418,239),(298,419,240),(298,420,241),(298,421,242),(298,422,243),(298,423,244),(298,424,245),(298,425,246),(298,426,247),(298,427,248),(298,428,249),(298,429,250),(298,430,251),(298,431,252),(298,432,253),(298,434,254),(298,435,255),(298,436,256),(298,437,257),(298,438,258),(298,439,259),(298,440,260),(298,441,261),(298,442,262),(298,443,263),(298,444,264),(298,445,265),(298,446,266),(298,447,267),(298,448,268),(298,449,269),(298,450,270),(298,451,271),(298,452,272),(298,453,273),(298,454,274),(298,455,275),(298,456,276),(298,457,277),(298,458,278),(298,459,279),(298,460,280),(298,461,281),(298,462,282),(298,463,283),(298,464,284),(298,465,285),(298,467,286),(298,468,287),(298,469,288),(298,470,289),(298,481,290),(298,489,291),(298,498,292),(298,499,293),(298,500,294),(298,501,295),(298,502,296),(298,513,297),(298,516,298),(298,517,299),(298,518,300),(298,519,301),(298,520,302),(298,521,303),(298,522,304),(298,523,305),(298,524,306),(298,525,307),(298,526,308),(298,527,309),(298,528,310),(298,529,311),(298,530,312),(298,531,313),(298,533,314),(298,534,315),(298,541,316),(298,542,317),(298,543,318),(298,544,319),(298,547,320),(298,548,321),(298,549,322),(298,551,323),(298,552,324),(298,553,325),(298,554,326),(298,555,327),(298,556,328),(298,557,329),(298,559,330),(298,560,331),(298,561,332),(298,562,333),(298,563,334),(298,564,335),(298,565,336),(298,566,337),(298,567,338),(298,568,339),(298,569,340),(298,570,341),(298,571,342),(298,572,343),(298,573,344),(298,574,345),(298,575,346),(298,576,347),(298,577,348),(298,578,349),(298,579,350),(298,580,351),(298,581,352),(298,583,353),(298,584,354),(298,585,355),(298,586,356),(298,588,357),(298,589,358),(298,590,359),(298,591,360),(298,592,361),(298,593,362),(298,594,363),(298,595,364),(298,596,365),(298,597,366),(298,598,367),(298,599,368),(298,600,369),(298,601,370),(298,602,371),(298,604,372),(298,605,373),(298,606,374),(298,607,375),(298,608,376),(298,609,377),(298,610,378),(298,611,379),(298,612,380),(298,624,381),(298,625,382),(298,626,383),(298,630,384),(298,631,385),(298,632,386),(298,633,387),(298,635,388),(298,636,389),(298,637,390),(298,639,391),(298,640,392),(298,641,393),(298,643,394),(298,644,395),(298,645,396),(298,647,397),(298,648,398),(298,649,399),(298,650,400),(298,651,401),(298,652,402),(298,654,403),(298,655,404),(298,656,405),(298,658,406),(298,660,407),(298,661,408),(298,662,409),(298,663,410),(298,664,411),(298,665,412),(298,666,413),(298,668,414),(298,669,415),(298,670,416),(298,671,417),(298,672,418),(298,673,419),(298,674,420),(298,675,421),(298,676,422),(298,677,423),(298,678,424),(298,679,425),(298,681,426),(298,682,427),(298,683,428),(298,684,429),(298,685,430),(298,686,431),(298,687,432),(298,688,433),(298,689,434),(298,690,435),(298,691,436),(298,692,437),(298,693,438),(298,694,439),(298,695,440),(298,709,441),(298,710,442),(298,712,443),(298,714,444),(298,715,445),(298,716,446),(298,717,447),(298,718,448),(298,720,449),(298,723,450),(298,724,451),(298,727,452),(298,728,453),(298,729,454),(298,731,455),(298,733,456),(298,734,457),(298,736,458),(298,737,459),(298,738,460),(298,739,461),(298,740,462),(298,741,463),(298,743,464),(298,744,465),(298,745,466),(298,746,467),(298,747,468),(298,749,469),(298,753,470),(298,754,471),(298,755,472),(298,756,473),(298,757,474),(298,763,475),(298,764,476),(298,765,477),(298,767,478),(298,768,479),(298,769,480),(298,771,481),(298,772,482),(298,773,483),(298,774,484),(298,775,485),(298,776,486),(298,778,487),(298,779,488),(298,780,489),(298,786,490),(298,787,491),(298,788,492),(298,789,493),(298,790,494),(298,791,495),(298,792,496),(298,793,497),(298,794,498),(298,795,499),(298,796,500),(298,797,501),(298,798,502),(298,799,503),(298,800,504),(298,803,505),(298,805,506),(298,806,507),(298,807,508),(298,812,509),(298,837,510),(298,838,511),(298,839,512),(298,840,513),(298,841,514),(298,842,515),(298,843,516),(298,844,517),(298,845,518),(298,846,519),(298,847,520),(298,848,521),(298,849,522),(298,850,523),(298,851,524),(298,852,525),(298,853,526),(298,854,527),(298,855,528),(298,856,529),(298,857,530),(298,858,531),(298,859,532),(298,860,533),(298,862,534),(298,863,535),(298,864,536),(298,865,537),(298,867,538),(298,868,539),(298,869,540),(298,870,541),(298,871,542),(298,872,543),(298,873,544),(298,874,545),(298,875,546),(298,877,547),(298,1003,548),(298,1004,549),(298,1005,550),(298,1015,551),(298,369,552),(298,532,553),(298,148,554),(298,582,555),(298,515,556),(298,558,557),(298,545,558),(298,546,559),(298,433,560),(298,811,561),(298,810,562),(298,813,563),(298,814,564),(298,815,565),(298,816,566),(298,818,567),(298,819,568),(298,821,569),(298,827,570),(298,828,571),(298,829,572),(298,830,573),(298,831,574),(298,832,575),(298,833,576),(298,834,577),(298,835,578),(298,836,579),(298,809,580),(298,825,581),(298,122,582),(298,117,583),(298,735,584),(298,124,585),(298,125,586),(298,126,587),(298,127,588),(298,128,589),(298,130,590),(298,131,591),(298,132,592),(298,133,593),(298,134,594),(298,667,595),(298,135,596),(298,136,597),(298,138,598),(298,140,599),(298,129,600),(298,777,601),(298,804,602),(298,808,603),(298,801,604),(298,802,605),(298,603,606),(298,824,607),(298,823,608),(298,822,609),(298,634,610),(298,748,611),(298,646,612),(298,642,613),(298,1010,614),(298,7,615),(298,659,616),(298,653,617),(298,587,618),(298,730,619),(298,372,620),(298,113,621),(298,742,622),(298,750,623),(298,629,624),(298,96,625),(298,413,626),(298,88,627),(298,91,628),(298,514,629),(298,85,630),(298,86,631),(298,92,632),(298,285,633),(298,121,634),(298,371,635),(298,201,636),(298,202,637),(298,203,638),(298,204,639),(298,205,640),(298,120,641),(298,168,642),(298,1011,643),(298,972,644),(298,1007,645),(298,1009,646),(298,1008,647),(298,973,648),(298,974,649),(298,975,650),(298,976,651),(298,977,652),(298,979,653),(298,978,654),(298,981,655),(298,984,656),(298,732,657),(298,987,658),(298,989,659),(298,990,660),(298,991,661),(298,992,662),(298,993,663),(298,994,664),(298,998,665),(298,1000,666),(298,1001,667),(298,334,668),(298,336,669),(298,387,670),(298,390,671),(298,283,672),(298,784,673),(298,751,674),(298,758,675),(298,752,676),(298,759,677),(298,760,678),(298,761,679),(298,762,680),(298,782,681),(298,783,682),(298,785,683),(298,306,684),(298,781,685),(298,995,686),(298,996,687),(298,93,688),(298,281,689),(298,282,690),(298,335,691),(298,391,692),(298,279,693),(298,280,694),(298,333,695),(298,393,696),(298,412,697),(298,466,698),(298,277,699),(298,392,700),(298,278,701),(298,410,702),(298,284,703),(298,411,704),(298,389,705),(298,879,706),(298,363,707),(298,338,708),(298,340,709),(298,337,710),(298,341,711),(298,357,712),(298,364,713),(298,365,714),(298,339,715),(298,114,716),(298,878,717),(298,1019,718),(298,982,719),(298,985,720),(298,988,721),(298,1012,722),(298,983,723),(298,986,724),(298,1002,725),(298,876,726),(298,866,727),(298,861,728),(298,638,729),(298,84,730),(298,94,731),(298,95,732),(298,97,733),(298,98,734),(298,103,735),(298,102,736),(298,101,737),(298,100,738),(298,105,739),(298,106,740),(298,104,741),(298,766,742),(298,657,743),(298,170,744),(298,826,745),(298,166,746),(298,1025,747),(298,1026,748),(298,1030,749),(298,970,750),(298,1032,751),(298,980,752),(298,997,753),(298,999,754),(298,971,755),(298,155,756),(298,1028,757),(298,157,758),(298,156,759),(298,154,760),(298,165,761),(298,164,762),(298,169,763),(298,153,764),(298,167,765),(298,1031,766),(298,149,767),(298,1043,768),(298,550,769),(298,699,770),(298,698,771),(298,700,772),(298,696,773),(298,703,774),(298,701,775),(298,702,776),(298,704,777),(298,705,778),(298,706,779),(298,707,780),(298,697,781),(298,713,782),(298,721,783),(298,722,784),(298,711,785),(298,719,786),(298,1024,787),(298,123,788),(298,1029,789),(298,1038,790),(298,1040,791),(298,1057,792),(298,708,793),(298,1054,794),(298,1037,795),(298,82,796),(327,354,0),(327,355,1),(327,356,2),(327,882,3),(327,884,4),(327,885,5),(327,881,6),(327,886,7),(327,883,8),(327,880,9),(327,725,10),(327,726,11),(295,1,0),(295,2,1),(295,3,2),(295,4,3),(295,5,4),(295,6,5),(295,8,6),(295,9,7),(295,10,8),(295,11,9),(295,12,10),(295,13,11),(295,14,12),(295,15,13),(295,16,14),(295,17,15),(295,18,16),(295,19,17),(295,20,18),(295,21,19),(295,22,20),(295,23,21),(295,24,22),(295,25,23),(295,26,24),(295,27,25),(295,28,26),(295,29,27),(295,30,28),(295,31,29),(295,32,30),(295,33,31),(295,34,32),(295,35,33),(295,36,34),(295,37,35),(295,38,36),(295,39,37),(295,40,38),(295,41,39),(295,42,40),(295,43,41),(295,44,42),(295,45,43),(295,46,44),(295,47,45),(295,48,46),(295,49,47),(295,50,48),(295,51,49),(295,52,50),(295,53,51),(295,54,52),(295,55,53),(295,56,54),(295,57,55),(295,58,56),(295,59,57),(295,60,58),(295,61,59),(295,62,60),(295,63,61),(295,64,62),(295,65,63),(295,66,64),(295,67,65),(295,68,66),(295,69,67),(295,70,68),(295,71,69),(295,72,70),(295,73,71),(295,74,72),(295,75,73),(295,76,74),(295,77,75),(295,78,76),(295,79,77),(295,80,78),(295,81,79),(295,107,80),(295,109,81),(295,110,82),(295,111,83),(295,112,84),(295,115,85),(295,116,86),(295,118,87),(295,119,88),(295,141,89),(295,142,90),(295,143,91),(295,144,92),(295,145,93),(295,146,94),(295,147,95),(295,150,96),(295,151,97),(295,158,98),(295,159,99),(295,160,100),(295,161,101),(295,162,102),(295,163,103),(295,171,104),(295,172,105),(295,173,106),(295,174,107),(295,175,108),(295,176,109),(295,177,110),(295,178,111),(295,179,112),(295,180,113),(295,181,114),(295,182,115),(295,183,116),(295,184,117),(295,185,118),(295,186,119),(295,187,120),(295,188,121),(295,189,122),(295,190,123),(295,191,124),(295,192,125),(295,193,126),(295,194,127),(295,195,128),(295,196,129),(295,197,130),(295,198,131),(295,199,132),(295,200,133),(295,206,134),(295,207,135),(295,208,136),(295,209,137),(295,210,138),(295,211,139),(295,212,140),(295,213,141),(295,214,142),(295,215,143),(295,216,144),(295,217,145),(295,218,146),(295,219,147),(295,220,148),(295,221,149),(295,222,150),(295,223,151),(295,224,152),(295,225,153),(295,226,154),(295,227,155),(295,230,156),(295,231,157),(295,232,158),(295,233,159),(295,234,160),(295,235,161),(295,236,162),(295,237,163),(295,238,164),(295,239,165),(295,240,166),(295,241,167),(295,242,168),(295,243,169),(295,244,170),(295,245,171),(295,246,172),(295,247,173),(295,248,174),(295,259,175),(295,260,176),(295,261,177),(295,262,178),(295,263,179),(295,264,180),(295,265,181),(295,266,182),(295,267,183),(295,268,184),(295,269,185),(295,270,186),(295,271,187),(295,272,188),(295,286,189),(295,287,190),(295,288,191),(295,289,192),(295,290,193),(295,291,194),(295,292,195),(295,293,196),(295,294,197),(295,295,198),(295,296,199),(295,297,200),(295,298,201),(295,299,202),(295,300,203),(295,301,204),(295,302,205),(295,303,206),(295,304,207),(295,305,208),(295,307,209),(295,308,210),(295,309,211),(295,310,212),(295,311,213),(295,312,214),(295,313,215),(295,314,216),(295,315,217),(295,316,218),(295,317,219),(295,318,220),(295,319,221),(295,320,222),(295,321,223),(295,322,224),(295,323,225),(295,324,226),(295,325,227),(295,326,228),(295,327,229),(295,328,230),(295,329,231),(295,330,232),(295,331,233),(295,332,234),(295,342,235),(295,343,236),(295,344,237),(295,345,238),(295,346,239),(295,347,240),(295,348,241),(295,349,242),(295,350,243),(295,351,244),(295,352,245),(295,353,246),(295,358,247),(295,359,248),(295,360,249),(295,361,250),(295,362,251),(295,394,252),(295,395,253),(295,396,254),(295,397,255),(295,398,256),(295,399,257),(295,400,258),(295,401,259),(295,402,260),(295,403,261),(295,404,262),(295,405,263),(295,406,264),(295,407,265),(295,408,266),(295,409,267),(295,414,268),(295,415,269),(295,416,270),(295,417,271),(295,418,272),(295,419,273),(295,420,274),(295,421,275),(295,422,276),(295,423,277),(295,424,278),(295,425,279),(295,426,280),(295,427,281),(295,428,282),(295,429,283),(295,430,284),(295,431,285),(295,432,286),(295,434,287),(295,435,288),(295,436,289),(295,437,290),(295,438,291),(295,439,292),(295,440,293),(295,441,294),(295,442,295),(295,443,296),(295,444,297),(295,445,298),(295,446,299),(295,447,300),(295,448,301),(295,449,302),(295,450,303),(295,451,304),(295,452,305),(295,453,306),(295,454,307),(295,455,308),(295,456,309),(295,457,310),(295,458,311),(295,459,312),(295,460,313),(295,461,314),(295,462,315),(295,463,316),(295,464,317),(295,465,318),(295,467,319),(295,468,320),(295,469,321),(295,470,322),(295,471,323),(295,473,324),(295,474,325),(295,475,326),(295,476,327),(295,477,328),(295,478,329),(295,479,330),(295,480,331),(295,481,332),(295,482,333),(295,484,334),(295,486,335),(295,487,336),(295,488,337),(295,489,338),(295,490,339),(295,491,340),(295,492,341),(295,493,342),(295,494,343),(295,495,344),(295,496,345),(295,497,346),(295,498,347),(295,499,348),(295,500,349),(295,501,350),(295,502,351),(295,503,352),(295,504,353),(295,505,354),(295,506,355),(295,507,356),(295,508,357),(295,509,358),(295,510,359),(295,511,360),(295,512,361),(295,513,362),(295,516,363),(295,517,364),(295,518,365),(295,519,366),(295,520,367),(295,521,368),(295,522,369),(295,523,370),(295,524,371),(295,525,372),(295,526,373),(295,527,374),(295,528,375),(295,529,376),(295,530,377),(295,531,378),(295,533,379),(295,534,380),(295,535,381),(295,536,382),(295,537,383),(295,538,384),(295,539,385),(295,540,386),(295,541,387),(295,542,388),(295,543,389),(295,544,390),(295,547,391),(295,548,392),(295,549,393),(295,551,394),(295,552,395),(295,553,396),(295,554,397),(295,555,398),(295,556,399),(295,557,400),(295,559,401),(295,560,402),(295,561,403),(295,562,404),(295,563,405),(295,564,406),(295,565,407),(295,566,408),(295,567,409),(295,568,410),(295,569,411),(295,570,412),(295,571,413),(295,572,414),(295,573,415),(295,574,416),(295,575,417),(295,576,418),(295,577,419),(295,578,420),(295,579,421),(295,580,422),(295,581,423),(295,583,424),(295,584,425),(295,585,426),(295,586,427),(295,588,428),(295,589,429),(295,590,430),(295,591,431),(295,592,432),(295,593,433),(295,594,434),(295,595,435),(295,596,436),(295,597,437),(295,598,438),(295,599,439),(295,600,440),(295,601,441),(295,602,442),(295,604,443),(295,605,444),(295,606,445),(295,607,446),(295,608,447),(295,609,448),(295,610,449),(295,611,450),(295,612,451),(295,624,452),(295,630,453),(295,631,454),(295,632,455),(295,633,456),(295,635,457),(295,636,458),(295,637,459),(295,639,460),(295,640,461),(295,641,462),(295,643,463),(295,644,464),(295,645,465),(295,647,466),(295,648,467),(295,649,468),(295,650,469),(295,651,470),(295,652,471),(295,654,472),(295,655,473),(295,656,474),(295,658,475),(295,660,476),(295,661,477),(295,662,478),(295,663,479),(295,664,480),(295,665,481),(295,666,482),(295,914,483),(295,915,484),(295,916,485),(295,917,486),(295,918,487),(295,920,488),(295,921,489),(295,923,490),(295,924,491),(295,925,492),(295,926,493),(295,927,494),(295,928,495),(295,929,496),(295,930,497),(295,931,498),(295,932,499),(295,933,500),(295,936,501),(295,938,502),(295,939,503),(295,940,504),(295,941,505),(295,942,506),(295,943,507),(295,944,508),(295,945,509),(295,946,510),(295,947,511),(295,948,512),(295,949,513),(295,952,514),(295,954,515),(295,956,516),(295,957,517),(295,959,518),(295,960,519),(295,961,520),(295,963,521),(295,965,522),(295,1015,523),(295,532,524),(295,148,525),(295,582,526),(295,515,527),(295,558,528),(295,545,529),(295,546,530),(295,433,531),(295,122,532),(295,117,533),(295,124,534),(295,125,535),(295,126,536),(295,127,537),(295,128,538),(295,130,539),(295,131,540),(295,132,541),(295,133,542),(295,134,543),(295,667,544),(295,135,545),(295,136,546),(295,138,547),(295,140,548),(295,129,549),(295,603,550),(295,634,551),(295,646,552),(295,642,553),(295,7,554),(295,659,555),(295,653,556),(295,587,557),(295,372,558),(295,113,559),(295,629,560),(295,413,561),(295,514,562),(295,285,563),(295,121,564),(295,371,565),(295,201,566),(295,202,567),(295,203,568),(295,204,569),(295,205,570),(295,120,571),(295,168,572),(295,334,573),(295,336,574),(295,387,575),(295,390,576),(295,283,577),(295,306,578),(295,363,579),(295,338,580),(295,340,581),(295,337,582),(295,341,583),(295,357,584),(295,364,585),(295,365,586),(295,339,587),(295,114,588),(295,889,589),(295,893,590),(295,894,591),(295,895,592),(295,898,593),(295,899,594),(295,900,595),(295,901,596),(295,905,597),(295,906,598),(295,910,599),(295,911,600),(295,912,601),(295,913,602),(295,638,603),(295,657,604),(295,170,605),(295,892,606),(295,896,607),(295,897,608),(295,902,609),(295,903,610),(295,904,611),(295,907,612),(295,166,613),(295,908,614),(295,909,615),(295,922,616),(295,966,617),(295,967,618),(295,968,619),(295,969,620),(295,891,621),(295,964,622),(295,935,623),(295,934,624),(295,937,625),(295,953,626),(295,955,627),(295,1032,628),(295,951,629),(295,962,630),(295,919,631),(295,958,632),(295,155,633),(295,157,634),(295,156,635),(295,154,636),(295,165,637),(295,164,638),(295,169,639),(295,153,640),(295,167,641),(295,950,642),(295,890,643),(295,149,644),(295,550,645),(295,1024,646),(295,123,647),(326,355,0),(326,882,1),(326,884,2),(326,885,3),(326,881,4),(225,634,0),(225,663,1),(225,644,2),(225,630,3),(225,645,4),(225,666,5),(225,632,6),(225,649,7),(225,635,8),(225,648,9),(225,660,10),(225,642,11),(225,657,12),(225,664,13),(225,647,14),(225,654,15),(225,643,16),(225,636,17),(225,646,18),(225,652,19),(225,640,20),(225,667,21),(225,638,22),(225,651,23),(225,637,24),(225,653,25),(225,661,26),(225,641,27),(225,656,28),(225,629,29),(225,650,30),(225,658,31),(225,639,32),(225,665,33),(225,631,34),(225,659,35),(225,662,36),(225,655,37),(225,633,38),(226,668,0),(226,670,1),(226,675,2),(226,674,3),(226,672,4),(226,676,5),(226,673,6),(226,669,7),(226,671,8),(221,274,0),(221,273,1),(221,879,2),(221,276,3),(221,275,4),(228,862,0),(228,868,1),(228,858,2),(228,854,3),(228,860,4),(228,872,5),(228,871,6),(228,857,7),(228,870,8),(228,853,9),(228,863,10),(228,856,11),(228,864,12),(228,852,13),(228,873,14),(228,866,15),(228,855,16),(228,875,17),(228,876,18),(228,877,19),(228,878,20),(228,859,21),(228,861,22),(228,851,23),(228,867,24),(228,869,25),(228,865,26),(228,874,27),(220,297,0),(220,263,1),(220,328,2),(220,240,3),(220,298,4),(220,288,5),(220,262,6),(220,345,7),(220,400,8),(220,451,9),(220,454,10),(220,332,11),(220,295,12),(220,310,13),(220,243,14),(220,306,15),(220,418,16),(220,315,17),(220,420,18),(220,363,19),(220,289,20),(220,432,21),(220,299,22),(220,324,23),(220,254,24),(220,452,25),(220,415,26),(220,394,27),(220,329,28),(220,250,29),(220,320,30),(220,433,31),(220,300,32),(220,453,33),(220,347,34),(220,449,35),(220,467,36),(220,270,37),(220,403,38),(220,465,39),(220,236,40),(220,342,41),(220,318,42),(220,409,43),(220,401,44),(220,258,45),(220,468,46),(220,464,47),(220,241,48),(220,305,49),(220,248,50),(220,395,51),(220,359,52),(220,443,53),(220,316,54),(220,431,55),(220,402,56),(220,257,57),(220,343,58),(220,448,59),(220,426,60),(220,358,61),(220,267,62),(220,321,63),(220,291,64),(220,322,65),(220,404,66),(220,408,67),(220,405,68),(220,348,69),(220,256,70),(220,286,71),(220,430,72),(220,293,73),(220,304,74),(220,230,75),(220,459,76),(220,323,77),(220,435,78),(220,436,79),(220,422,80),(220,287,81),(220,266,82),(220,396,83),(220,350,84),(220,326,85),(220,450,86),(220,361,87),(220,427,88),(220,349,89),(220,441,90),(220,330,91),(220,319,92),(220,434,93),(220,235,94),(220,437,95),(220,397,96),(220,457,97),(220,311,98),(220,362,99),(220,352,100),(220,325,101),(220,244,102),(220,255,103),(220,239,104),(220,301,105),(220,429,106),(220,231,107),(220,440,108),(220,272,109),(220,237,110),(220,469,111),(220,406,112),(220,416,113),(220,309,114),(220,238,115),(220,462,116),(220,290,117),(220,249,118),(220,425,119),(220,407,120),(220,398,121),(220,245,122),(220,444,123),(220,314,124),(220,265,125),(220,327,126),(220,294,127),(220,351,128),(220,269,129),(220,439,130),(220,344,131),(220,421,132),(220,260,133),(220,302,134),(220,317,135),(220,247,136),(220,460,137),(220,445,138),(220,253,139),(220,353,140),(220,268,141),(220,232,142),(220,331,143),(220,428,144),(220,251,145),(220,414,146),(220,246,147),(220,438,148),(220,463,149),(220,261,150),(220,271,151),(220,259,152),(220,234,153),(220,312,154),(220,242,155),(220,252,156),(220,456,157),(220,303,158),(220,419,159),(220,292,160),(220,458,161),(220,360,162),(220,399,163),(220,313,164),(220,461,165),(220,424,166),(220,285,167),(220,307,168),(220,447,169),(220,296,170),(220,423,171),(220,417,172),(220,346,173),(220,264,174),(220,233,175),(220,455,176),(220,308,177),(220,446,178),(220,442,179),(220,338,180),(220,337,181),(220,339,182),(220,340,183),(220,341,184),(220,365,185),(220,364,186),(220,336,187),(220,390,188),(220,366,189),(220,367,190),(220,368,191),(220,369,192),(220,370,193),(220,373,194),(220,374,195),(220,375,196),(220,376,197),(220,377,198),(220,378,199),(220,379,200),(220,380,201),(220,381,202),(220,382,203),(220,383,204),(220,384,205),(220,385,206),(220,386,207),(220,388,208),(220,391,209),(220,281,210),(220,282,211),(220,335,212),(220,279,213),(220,283,214),(220,280,215),(220,333,216),(220,372,217),(220,393,218),(220,412,219),(220,466,220),(220,277,221),(220,392,222),(220,371,223),(220,410,224),(220,389,225),(220,284,226),(220,411,227),(220,334,228),(220,387,229),(220,278,230),(220,413,231),(220,357,232),(220,1025,233),(342,880,0),(342,884,1),(342,883,2),(342,882,3),(342,885,4),(342,354,5),(342,355,6),(342,356,7),(342,357,8),(342,881,9),(342,886,10),(244,947,0),(244,946,1),(244,897,2),(244,949,3),(244,909,4),(244,902,5),(244,963,6),(244,910,7),(244,938,8),(244,906,9),(244,941,10),(244,969,11),(244,945,12),(244,943,13),(244,912,14),(244,913,15),(244,894,16),(244,915,17),(244,914,18),(244,892,19),(244,899,20),(244,966,21),(244,968,22),(244,948,23),(244,901,24),(244,965,25),(244,889,26),(244,893,27),(244,916,28),(244,917,29),(244,900,30),(244,895,31),(244,939,32),(244,942,33),(244,940,34),(244,967,35),(244,905,36),(244,904,37),(244,908,38),(244,898,39),(244,944,40),(244,896,41),(244,907,42),(244,890,43),(244,891,44),(244,903,45),(244,911,46),(244,933,47),(244,964,48),(244,922,49),(244,936,50),(244,925,51),(244,937,52),(244,926,53),(244,923,54),(244,927,55),(244,929,56),(244,928,57),(244,924,58),(244,921,59),(244,931,60),(244,932,61),(244,930,62),(244,920,63),(244,918,64),(244,934,65),(244,935,66),(244,961,67),(244,957,68),(244,952,69),(244,956,70),(244,953,71),(244,954,72),(244,955,73),(244,951,74),(244,950,75),(244,960,76),(244,959,77),(244,958,78),(244,919,79),(244,962,80),(275,1004,0),(275,1003,1),(275,1002,2),(275,1005,3),(275,1011,4),(275,1010,5),(275,1012,6),(275,971,7),(275,970,8),(275,972,9),(275,973,10),(275,979,11),(275,977,12),(275,1001,13),(275,981,14),(275,983,15),(275,982,16),(275,991,17),(275,992,18),(275,978,19),(275,1000,20),(275,997,21),(275,989,22),(275,990,23),(275,988,24),(275,985,25),(275,996,26),(275,995,27),(275,987,28),(275,974,29),(275,975,30),(275,976,31),(275,980,32),(275,984,33),(275,986,34),(275,999,35),(275,998,36),(275,993,37),(275,994,38),(275,1007,39),(275,1009,40),(275,1008,41),(331,93,0),(331,94,1),(331,95,2),(331,96,3),(331,97,4),(331,98,5),(331,99,6),(331,100,7),(331,101,8),(331,102,9),(331,103,10),(331,104,11),(331,105,12),(331,106,13),(238,721,606),(298,83,797),(295,1057,648),(220,1026,234),(263,1026,187),(238,722,607),(298,89,798),(227,1032,162),(275,1019,42),(236,638,526),(238,711,608),(296,1053,426),(298,90,799),(275,1054,43),(236,1024,527),(296,1056,427),(238,719,609),(298,817,800),(227,1037,163),(236,1032,528),(238,1024,610),(236,698,529),(238,123,611),(298,770,801),(237,139,515),(295,139,649),(227,1038,164),(236,696,530),(299,152,388),(296,1058,428),(237,1052,516),(295,1052,650),(237,152,517),(295,152,651),(237,1063,518),(295,1063,652),(237,1053,519),(295,1053,653),(238,1029,612),(237,1056,520),(298,139,802),(295,1056,654),(223,1024,110),(299,1063,389),(300,1057,111),(296,108,429),(297,1057,93),(298,1061,803),(236,703,531),(238,1038,613),(220,1028,235),(298,1060,804),(263,1028,188),(238,1040,614),(220,1029,236),(298,1052,805),(263,1029,189),(238,1057,615),(298,99,806),(299,1053,390),(236,701,532),(238,708,616),(220,1030,237),(298,1055,807),(263,1030,190),(238,1054,617),(220,1031,238),(298,152,808),(263,1031,191),(238,1037,618),(220,1043,239),(298,87,809),(263,1043,192),(238,82,619),(296,228,430),(238,83,620),(298,1044,810),(227,1040,165),(236,702,533),(238,89,621),(298,1053,811),(236,1037,534),(238,90,622),(297,139,94),(300,139,112),(299,1056,391),(321,1056,122),(236,1038,535),(321,1057,123),(238,817,623),(236,697,536),(238,770,624),(236,1040,537),(238,139,625),(236,713,538),(238,1061,626),(236,721,539),(238,1060,627),(298,1056,812),(227,1044,166),(236,722,540),(238,1052,628),(298,1058,813),(227,1047,167),(236,711,541),(238,99,629),(298,108,814),(236,719,542),(238,1055,630),(236,708,543),(238,152,631),(227,1061,168),(236,149,544),(236,1044,545),(238,87,632),(298,228,815),(321,1058,124),(236,1047,546),(238,1044,633),(236,1053,547),(238,1053,634),(236,1054,548),(238,1056,635),(236,1055,549),(238,1058,636),(236,1056,550),(238,108,637),(236,1057,551),(238,228,638),(236,1058,552),(238,137,639),(298,137,816),(220,1052,240),(298,1047,817),(263,1052,193),(238,1047,640),(227,1062,169),(236,1061,553),(238,1062,641),(298,1062,818),(236,1062,554),(238,680,642),(298,680,819),(298,820,820),(238,820,643),(220,1060,241),(263,1060,194),(223,1053,111),(275,1055,44),(237,1058,521),(299,1058,392),(295,1058,655),(222,1063,14),(237,108,522),(295,108,656),(299,108,393),(300,1053,113),(297,1053,95),(237,137,523),(296,137,431),(295,137,657),(299,137,394);
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

-- Dump completed on 2014-11-28 19:00:48
