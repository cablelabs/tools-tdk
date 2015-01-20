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
) ENGINE=InnoDB AUTO_INCREMENT=6549 DEFAULT CHARSET=latin1;
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
) ENGINE=InnoDB AUTO_INCREMENT=25345 DEFAULT CHARSET=latin1;
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
) ENGINE=InnoDB AUTO_INCREMENT=133 DEFAULT CHARSET=latin1;
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
) ENGINE=InnoDB AUTO_INCREMENT=1801 DEFAULT CHARSET=latin1;
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
) ENGINE=InnoDB AUTO_INCREMENT=398906 DEFAULT CHARSET=latin1;
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
) ENGINE=InnoDB AUTO_INCREMENT=8067 DEFAULT CHARSET=latin1;
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
) ENGINE=InnoDB AUTO_INCREMENT=8017 DEFAULT CHARSET=latin1;
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
) ENGINE=InnoDB AUTO_INCREMENT=61109 DEFAULT CHARSET=latin1;
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
) ENGINE=InnoDB AUTO_INCREMENT=514 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `function`
--

LOCK TABLES `function` WRITE;
/*!40000 ALTER TABLE `function` DISABLE KEYS */;
INSERT INTO `function` VALUES (18,0,8,'TestMgr_IARMBUS_Init'),(19,0,8,'TestMgr_IARMBUS_Connect'),(20,0,8,'TestMgr_IARMBUS_Disconnect'),(21,0,8,'TestMgr_IARMBUS_Term'),(22,0,8,'TestMgr_IARMBUS_BusCall'),(24,0,8,'TestMgr_IARMBUS_RegisterCall'),(25,0,8,'TestMgr_IARMBUS_RequestResource'),(26,0,8,'TestMgr_IARMBUS_ReleaseResource'),(29,0,8,'TestMgr_IARMBUS_BroadcastEvent'),(30,0,8,'TestMgr_IARMBUS_InvokeSecondApplication'),(31,0,8,'TestMgr_IARMBUS_RegisterEventHandler'),(32,0,8,'TestMgr_IARMBUS_UnRegisterEventHandler'),(37,0,8,'TestMgr_IARMBUS_IsConnected'),(38,0,8,'TestMgr_IARMBUS_RegisterEvent'),(40,0,8,'TestMgr_IARMBUS_GetContext'),(41,0,8,'TestMgr_IARMBUS_GetLastReceivedEventDetails'),(74,0,24,'TestMgr_Opensource_Test_Execute'),(75,0,25,'TestMgr_DS_FP_setColor'),(76,0,25,'TestMgr_DS_managerInitialize'),(77,0,25,'TestMgr_DS_managerDeinitialize'),(78,0,25,'TestMgr_DS_FP_setBrightness'),(79,0,25,'TestMgr_DS_FP_setBlink'),(80,0,25,'TestMgr_DS_FP_setScroll'),(81,0,25,'TestMgr_DS_AOP_setLevel'),(82,0,25,'TestMgr_DS_AOP_setDB'),(83,0,25,'TestMgr_DS_VD_setDFC'),(84,0,25,'TestMgr_DS_AOP_setEncoding'),(85,0,25,'TestMgr_DS_AOP_setCompression'),(86,0,25,'TestMgr_DS_AOP_setStereoMode'),(87,0,25,'TestMgr_DS_HOST_setPowerMode'),(88,0,25,'TestMgr_DS_VOP_setResolution'),(89,0,25,'TestMgr_DS_FP_getIndicators'),(90,0,25,'TestMgr_DS_FP_FP_getSupportedColors'),(91,0,25,'TestMgr_DS_FP_getTextDisplays'),(92,0,25,'TestMgr_DS_FP_setText'),(93,0,25,'TestMgr_DS_FP_setTimeForamt'),(94,0,25,'TestMgr_DS_FP_setTime'),(95,0,25,'TestMgr_DS_AOP_loopThru'),(96,0,25,'TestMgr_DS_AOP_mutedStatus'),(97,0,25,'TestMgr_DS_AOP_getSupportedEncodings'),(98,0,25,'TestMgr_DS_AOP_getSupportedCompressions'),(99,0,25,'TestMgr_DS_AOP_getSupportedStereoModes'),(100,0,25,'TestMgr_DS_HOST_addPowerModeListener'),(101,0,25,'TestMgr_DS_HOST_removePowerModeListener'),(102,0,25,'TestMgr_DS_HOST_Resolutions'),(103,0,25,'TestMgr_DS_VOPTYPE_HDCPSupport'),(104,0,25,'TestMgr_DS_VOPTYPE_DTCPSupport'),(105,0,25,'TestMgr_DS_VOP_getAspectRatio'),(106,0,25,'TestMgr_DS_VOP_getDisplayDetails'),(107,0,25,'TestMgr_DS_VOPTYPE_isDynamicResolutionSupported'),(108,0,22,'TestMgr_MediaStreamer_LiveTune_Request'),(110,0,22,'TestMgr_MediaStreamer_Recorded_Urls'),(111,0,22,'TestMgr_MediaStreamer_Recorded_Metadata'),(112,0,22,'TestMgr_MediaStreamer_Live_Playback'),(113,0,22,'TestMgr_MediaStreamer_Recording_Playback'),(115,0,22,'TestMgr_MediaStreamer_DVR_Trickplay'),(117,0,25,'TestMgr_DS_VOP_isContentProtected'),(118,0,25,'TestMgr_DS_VOP_isDisplayConnected'),(122,0,25,'TestMgr_DS_HOST_addDisplayConnectionListener'),(123,0,25,'TestMgr_DS_HOST_removeDisplayConnectionListener'),(124,0,27,'TestMgr_SM_RegisterService'),(125,0,27,'TestMgr_SM_UnRegisterService'),(126,0,27,'TestMgr_SM_DoesServiceExist'),(128,0,22,'TestMgr_MediaStreamer_Recording_Request'),(129,0,27,'TestMgr_SM_GetRegisteredServices'),(142,0,39,'TestMgr_rmfapp_Test_Execute'),(149,0,27,'TestMgr_SM_GetGlobalService'),(150,0,27,'TestMgr_SM_HN_EnableMDVR'),(151,0,27,'TestMgr_SM_HN_EnableVPOP'),(152,0,27,'TestMgr_SM_HN_SetDeviceName'),(153,0,27,'TestMgr_SM_SetAPIVersion'),(154,0,27,'TestMgr_SM_RegisterForEvents'),(156,0,27,'TestMgr_SM_DisplaySetting_SetZoomSettings'),(157,0,27,'TestMgr_SM_DisplaySetting_SetCurrentResolution'),(158,0,35,'TestMgr_CC_Init'),(164,0,35,'TestMgr_CC_SetGetDigitalChannel'),(166,0,35,'TestMgr_CC_SetGetAnalogChannel'),(167,0,35,'TestMgr_CC_Show'),(168,0,35,'TestMgr_CC_Hide'),(173,0,35,'TestMgr_CC_SetGetAttribute'),(174,0,35,'TestMgr_CC_GetSupportedServiceNumberCount'),(175,0,35,'TestMgr_CC_GetSupportedServiceNumber'),(177,0,35,'TestMgr_CC_SetGetState'),(179,0,35,'TestMgr_CC_OnEasStart'),(180,0,35,'TestMgr_CC_OnEasStop'),(181,0,35,'TestMgr_CC_ResetTrickPlayStatus'),(182,0,35,'TestMgr_CC_SetTrickPlayStatus'),(201,0,44,'TestMgr_MPSink_SetGetMute'),(202,0,44,'TestMgr_MPSink_SetGetVolume'),(207,0,44,'TestMgr_HNSrc_GetBufferedRanges'),(208,0,44,'TestMgr_HNSrc_GetState'),(211,0,44,'TestMgr_HNSrcMPSink_Video_Pause'),(212,0,44,'TestMgr_MPSink_InitTerm'),(216,0,44,'TestMgr_HNSrcMPSink_Video_Speed'),(223,0,44,'TestMgr_HNSrcMPSink_Video_Play'),(224,0,44,'TestMgr_HNSrcMPSink_Video_State'),(227,0,44,'TestMgr_HNSrcMPSink_Video_Skip_Backward'),(230,0,44,'TestMgr_HNSrcMPSink_Video_Volume'),(231,0,44,'TestMgr_HNSrcMPSink_Video_Play_Position'),(232,0,44,'TestMgr_HNSrcMPSink_Video_MuteUnmute'),(270,0,44,'TestMgr_DVRSink_init_term'),(277,0,51,'TestMgr_RDKLogger_Dbg_Enabled_Status'),(278,0,51,'TestMgr_RDKLogger_EnvGet'),(279,0,51,'TestMgr_RDKLogger_EnvGetNum'),(280,0,51,'TestMgr_RDKLogger_EnvGetValueFromNum'),(281,0,51,'TestMgr_RDKLogger_EnvGetModFromNum'),(282,0,51,'TestMgr_RDKLogger_Init'),(283,0,51,'TestMgr_RDKLogger_Log'),(285,0,44,'TestMgr_QAMSource_Play'),(292,0,44,'TestMgr_QAMSource_InitTerm'),(293,0,44,'TestMgr_QAMSource_OpenClose'),(294,0,44,'TestMgr_QAMSource_Pause'),(295,0,44,' TestMgr_QAMSource_GetTsId'),(296,0,44,'TestMgr_QAMSource_GetLtsId'),(297,0,44,'TestMgr_QAMSource_GetQAMSourceInstance'),(298,0,44,'TestMgr_QAMSource_Init_Uninit_Platform'),(299,0,44,'TestMgr_QAMSource_GetUseFactoryMethods'),(300,0,44,'TestMgr_QAMSource_Get_Free_LowLevelElement'),(301,0,44,'TestMgr_QAMSource_ChangeURI'),(302,0,44,'TestMgr_DVRManager_GetSpace'),(303,0,44,'TestMgr_DVRManager_GetRecordingCount'),(304,0,44,'TestMgr_DVRManager_GetRecordingInfoByIndex'),(305,0,44,'TestMgr_DVRManager_GetRecordingInfoById'),(306,0,44,'TestMgr_DVRManager_GetIsRecordingInProgress'),(307,0,44,'TestMgr_DVRManager_GetRecordingSize'),(308,0,44,'TestMgr_DVRManager_GetRecordingDuration'),(309,0,44,'TestMgr_DVRManager_GetRecordingStartTime'),(310,0,44,'TestMgr_DVRManager_GetDefaultTSBMaxDuration'),(311,0,44,'TestMgr_DVRManager_CreateTSB'),(312,0,44,'TestMgr_DVRManager_CreateRecording'),(313,0,44,'TestMgr_DVRManager_UpdateRecording'),(314,0,44,'TestMgr_DVRManager_DeleteRecording'),(315,0,44,'TestMgr_DVRManager_GetSegmentsCount'),(316,0,44,'TestMgr_DVRManager_ConvertTSBToRecording'),(317,0,44,'TestMgr_DVRManager_GetRecordingSegmentInfoByIndex'),(350,0,22,'TestMgr_RMFStreamer_InterfaceTesting'),(351,0,22,'TestMgr_RMFStreamer_Player'),(353,0,44,'TestMgr_DVR_Rec_List'),(354,0,44,'TestMgr_RmfElementCreateInstance'),(355,0,44,'TestMgr_RmfElementInit'),(356,0,44,'TestMgr_RmfElementTerm'),(357,0,44,'TestMgr_RmfElementOpen'),(358,0,44,'TestMgr_RmfElementClose'),(359,0,44,'TestMgr_RmfElementRemoveInstance'),(360,0,44,'TestMgr_RmfElementPlay'),(361,0,44,'TestMgr_RmfElement_Sink_SetSource'),(362,0,44,'TestMgr_RmfElement_MpSink_SetVideoRectangle'),(363,0,44,'TestMgr_RmfElementSetSpeed'),(364,0,44,'TestMgr_RmfElementGetSpeed'),(365,0,44,'TestMgr_RmfElementGetMediaTime'),(366,0,44,'TestMgr_RmfElementGetState'),(367,0,44,'TestMgr_RmfElementPause'),(368,0,44,'TestMgr_RmfElementSetMediaTime'),(369,0,44,'TestMgr_RmfElementGetMediaInfo'),(371,0,58,'TestMgr_Recorder_ScheduleRecording'),(372,0,58,'TestMgr_Recorder_checkRecording_status'),(373,0,44,'TestMgr_DVRManager_CheckRecordingInfoById'),(374,0,44,'TestMgr_DVRManager_CheckRecordingInfoByIndex'),(375,0,59,'TestMgr_HybridE2E_T2pTuning'),(376,0,59,'TestMgr_HybridE2E_T2pTrickMode'),(378,0,59,'TestMgr_E2EStub_PlayURL'),(379,0,59,'TestMgr_E2EStub_GetRecURLS'),(380,0,59,'TestMgr_E2ELinearTV_GetURL'),(381,0,59,'TestMgr_E2ELinearTV_PlayURL'),(382,0,59,'TestMgr_Dvr_Play_Pause'),(383,0,59,'TestMgr_Dvr_Play_TrickPlay_FF_FR'),(384,0,59,'TestMgr_LinearTv_Dvr_Play'),(385,0,59,'TestMgr_Dvr_Play_TrickPlay_RewindFromEndPoint'),(386,0,59,'TestMgr_Dvr_Pause_Play'),(387,0,59,'TestMgr_Dvr_Play_Pause_Play'),(388,0,59,'TestMgr_Dvr_Play_Pause_Play_Repeat'),(389,0,59,'TestMgr_Dvr_Skip_Forward_Play'),(390,0,59,'TestMgr_Dvr_Skip_Forward_From_Middle'),(391,0,59,'TestMgr_Dvr_Skip_Forward_From_End'),(392,0,59,'TestMgr_Dvr_Skip_Backward_From_End'),(393,0,59,'TestMgr_Dvr_Skip_Backward_From_Middle'),(394,0,59,'TestMgr_Dvr_Skip_Backward_From_Starting'),(395,0,59,'TestMgr_Dvr_Play_Rewind_Forward'),(396,0,59,'TestMgr_Dvr_Play_Forward_Rewind'),(397,0,59,'TestMgr_Dvr_Play_FF_FR_Pause_Play'),(398,0,59,'TestMgr_Dvr_Play_Pause_FF_FR'),(399,0,59,'TestMgr_Dvr_Play_Pause_Play_SF_SB'),(400,0,59,'TestMgr_Dvr_Play_FF_FR_SF_SB'),(401,0,59,'TestMgr_Dvr_Play_Pause_Pause'),(402,0,59,'TestMgr_Dvr_Play_Play'),(403,0,59,'TestMgr_LiveTune_GETURL'),(404,0,59,'TestMgr_RF_Video_ChannelChange'),(405,0,44,'TestMgr_RmfElement_DVRManagerCreateRecording'),(407,0,44,'TestMgr_RmfElement_QAMSrc_RmfPlatform_Init'),(408,0,44,'TestMgr_RmfElement_QAMSrc_RmfPlatform_Uninit'),(409,0,44,'TestMgr_RmfElement_QAMSrc_InitPlatform'),(410,0,44,'TestMgr_RmfElement_QAMSrc_UninitPlatform'),(412,0,44,'TestMgr_RmfElement_QAMSrc_GetTSID'),(413,0,44,'TestMgr_RmfElement_QAMSrc_GetLTSID'),(414,0,44,'TestMgr_RmfElement_QAMSrc_GetLowLevelElement'),(415,0,44,'TestMgr_RmfElement_QAMSrc_FreeLowLevelElement'),(416,0,44,'TestMgr_RmfElement_QAMSrc_ChangeURI'),(417,0,44,'TestMgr_RmfElement_QAMSrc_UseFactoryMethods'),(418,0,44,'TestMgr_RmfElement_HNSink_InitPlatform'),(419,0,44,'TestMgr_RmfElement_HNSink_UninitPlatform'),(420,0,44,'TestMgr_RmfElement_HNSink_SetProperties'),(421,0,44,'TestMgr_RmfElement_HNSink_SetSourceType'),(422,0,59,'TestMgr_TSB_Play'),(424,0,39,'TestMgr_CreateRecord'),(425,0,59,'TestMgr_MDVR_Record_Play'),(426,0,59,'TestMgr_MDVR_GetResult'),(427,0,60,'TestMgr_GetParameterValue'),(429,0,51,'TestMgr_RDKLogger_Log_All'),(431,0,51,'TestMgr_RDKLogger_Log_InverseTrace'),(432,0,51,'TestMgr_RDKLogger_Log_Msg'),(433,0,51,'TestMgr_RDKLogger_Log_None'),(434,0,51,'TestMgr_RDKLogger_Log_Trace'),(437,0,51,'TestMgr_RDKLogger_CheckMPELogEnabled'),(438,0,60,'TestMgr_VerifyParameterValue'),(440,0,51,'TestMgr_RDKLogger_SetLogLevel'),(441,0,51,'TestMgr_RDKLogger_GetLogLevel'),(442,0,44,'TestMgr_HNSrc_GetBufferedRanges'),(443,0,61,'TestMgr_Aesdecrypt_DecryptEnable_Prop'),(445,0,62,'TestMgr_TRM_GetAllTunerStates'),(446,0,62,'TestMgr_TRM_GetAllTunerIds'),(447,0,62,'TestMgr_TRM_GetAllReservations'),(448,0,62,'TestMgr_TRM_GetVersion'),(449,0,61,'TestMgr_Aesdecrypt_DecryptEnable_Get_Prop'),(450,0,61,'TestMgr_Aesencrypt_EncryptEnable_Set_Prop'),(453,0,61,'TestMgr_Aesencrypt_EncryptEnable_Get_Prop'),(454,0,61,'TestMgr_Dvrsrc_RecordId_Set_Prop'),(455,0,61,'TestMgr_Dvrsrc_RecordId_Get_Prop'),(456,0,61,'TestMgr_Dvrsrc_SegmentName_Set_Prop'),(457,0,61,'TestMgr_Dvrsrc_SegmentName_Get_Prop'),(458,0,61,'TestMgr_Dvrsrc_Ccivalue_Get_Prop'),(459,0,61,'TestMgr_Dvrsrc_Rate_Set_Prop'),(460,0,62,'TestMgr_TRM_TunerReserveForRecord'),(461,0,62,'TestMgr_TRM_TunerReserveForLive'),(462,0,61,'TestMgr_Dvrsrc_Rate_Get_Prop'),(463,0,61,'TestMgr_Dvrsrc_StartTime_Get_Prop'),(464,0,61,'TestMgr_Dvrsrc_Duration_Get_Prop'),(465,0,61,'TestMgr_Dvrsrc_PlayStartPosition_Set_Prop'),(466,0,61,'TestMgr_Dvrsrc_PlayStartPosition_Get_Prop'),(467,0,61,'TestMgr_Dvrsink_RecordId_Set_Prop'),(468,0,61,'TestMgr_Dvrsink_RecordId_Get_Prop'),(469,0,61,'TestMgr_Dvrsink_Ccivalue_Get_Prop'),(470,0,61,'TestMgr_Dvrsrc_RecordId_Get_Prop'),(471,0,61,'TestMgr_Dvrsrc_SegmentName_Set_Prop'),(472,0,61,'TestMgr_Dvrsrc_SegmentName_Set_Prop'),(474,0,62,'TestMgr_TRM_ReleaseTunerReservation'),(475,0,62,'TestMgr_TRM_ValidateTunerReservation'),(476,0,62,'TestMgr_TRM_CancelRecording'),(477,0,62,'TestMgr_TRM_CancelLive'),(481,0,27,'TestMgr_SM_DeviceSetting_GetDeviceInfo'),(482,0,27,'TestMgr_SM_ScreenCapture_Upload'),(483,0,27,'TestMgr_SM_WebSocket_GetUrl'),(484,0,27,'TestMgr_SM_WebSocket_GetReadyState'),(485,0,27,'TestMgr_SM_WebSocket_GetBufferedAmount'),(486,0,27,'TestMgr_SM_WebSocket_GetProtocol'),(487,0,27,'TestMgr_SM_GetSetting'),(488,0,27,'TestMgr_SM_CreateService'),(489,0,27,'TestMgr_Services_GetName'),(490,0,44,'TestMgr_RmfElement_CheckForSPTSRead_QAMSrc_Error'),(491,0,25,'TestMgr_DS_FP_setState'),(492,0,25,'TestMgr_DS_VOP_setEnable'),(495,0,44,'TestMgr_CheckAudioVideoStatus'),(498,0,65,'TestMgr_XUPNPAgent_checkjson'),(499,0,65,'TestMgr_XUPNPAgent_checkSTRurl'),(500,0,65,'TestMgr_XUPNPAgent_checkSerialNo'),(501,0,65,'TestMgr_XUPNPAgent_checkPBurl'),(502,0,65,'TestMgr_XUPNPAgent_recordId'),(503,0,65,'TestMgr_XUPNPAgent_ModBasicDevice'),(504,0,65,'TestMgr_XUPNPAgent_removeXmls'),(505,0,65,'TestMgr_XUPNPAgent_evtCheck'),(506,0,44,'TestMgr_CheckRmfStreamerCrash'),(507,0,44,'TestMgr_ClearLogFile'),(508,0,44,'TestMgr_DVR_CreateNewRecording'),(509,0,62,'TestMgr_TRM_ReleaseTunerReservation'),(510,0,44,'TestMgr_CommentScirptForQam'),(511,0,44,'TestMgr_UnCommentScirptForQam'),(513,0,64,'TestMgr_DTCP_Test_Execute');
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
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=latin1;
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
) ENGINE=InnoDB AUTO_INCREMENT=67 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `module`
--

LOCK TABLES `module` WRITE;
/*!40000 ALTER TABLE `module` DISABLE KEYS */;
INSERT INTO `module` VALUES (8,8,'iarmbus','1.2','Component',NULL,3),(22,4,'mediastreamer','1.2','Component',NULL,3),(24,2,'openSource_components','1.2','OpenSource',NULL,60),(25,5,'devicesettings','1.2','Component',NULL,3),(27,2,'servicemanager','1.3','Component',NULL,2),(35,2,'closedcaption','1.2','Component',NULL,1),(39,2,'rmfapp','2.0','E2E',NULL,5),(44,3,'mediaframework','2.0','Component',NULL,3),(51,2,'rdk_logger','2.0','Component',NULL,5),(58,2,'recorder','2.0','Component',NULL,10),(59,3,'tdk_integration','1.3','E2E',NULL,5),(60,1,'tr69','1','Component',NULL,5),(61,1,'gst-plugins-rdk','1','Component',NULL,5),(62,1,'trm','1','Component',NULL,10),(64,1,'dtcp','1','Component',NULL,5),(65,1,'xupnp','1','Component',NULL,7);
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
) ENGINE=InnoDB AUTO_INCREMENT=788 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `parameter_type`
--

LOCK TABLES `parameter_type` WRITE;
/*!40000 ALTER TABLE `parameter_type` DISABLE KEYS */;
INSERT INTO `parameter_type` VALUES (20,0,18,'Process_name','STRING','A-Z'),(21,0,22,'owner_name','STRING','A-Z'),(22,0,22,'method_name','STRING','A-Z'),(24,0,22,'set_timeout','INTEGER','1-65535'),(25,0,22,'newState','INTEGER','0-2'),(26,0,22,'resource_type','INTEGER','0-7'),(27,0,24,'owner_name','STRING','A-Z'),(29,0,25,'resource_type','INTEGER','0-7'),(30,0,26,'resource_type','INTEGER','0-7'),(34,0,29,'event_id','INTEGER','0-2'),(35,0,29,'owner_name','STRING','A-Z'),(37,0,29,'keyType','INTEGER','1-65535'),(38,0,29,'keyCode','INTEGER','1-65535'),(39,0,29,'newState','INTEGER','0-2'),(40,0,29,'resource_type','INTEGER','0-7'),(43,0,31,'event_id','INTEGER','0-2'),(44,0,31,'owner_name','STRING','A-Z'),(45,0,32,'event_id','INTEGER','0-2'),(46,0,32,'owner_name','STRING','A-Z'),(49,0,37,'member_name','STRING','A-Z'),(51,0,38,'max_event','INTEGER','0-2'),(68,0,22,'mfr_param_type','INTEGER','0-9'),(81,0,74,'Opensource_component_type','STRING','qt_non_gfx (or) qt_gfx (or) webkit (or) gstreamer (or) gst_plugin_base (or) gst_plugin_good (or) gst-plugin-custom'),(82,0,74,'Display_option','STRING','directfb (or) eglnullws (or) intelce'),(85,0,78,'indicator_name','STRING','A-Z'),(86,0,78,'brightness','INTEGER','1-100'),(87,0,79,'indicator_name','STRING','A-Z'),(88,0,79,'blink_interval','INTEGER','1-10'),(89,0,79,'blink_iteration','STRING','1-10'),(90,0,80,'viteration','INTEGER','1-10'),(91,0,80,'hiteration','INTEGER','1-10'),(92,0,80,'hold_duration','INTEGER','1-10'),(93,0,80,'text','STRING','A-Z'),(94,0,81,'port_name','STRING','A-Z'),(97,0,82,'port_name','STRING','A-Z'),(98,0,83,'zoom_setting','STRING','A-Z'),(99,0,84,'port_name','STRING','A-Z'),(100,0,84,'encoding_format','STRING','A-Z'),(101,0,85,'port_name','STRING','A-Z'),(102,0,85,'compression_format','STRING','A-Z'),(103,0,86,'port_name','STRING','A-Z'),(104,0,86,'stereo_mode','STRING','A-Z'),(105,0,87,'new_power_state','INTEGER','0-1'),(106,0,88,'port_name','STRING','A-Z'),(107,0,88,'resolution','STRING','A-Z & 0-9'),(108,0,90,'indicator_name','STRING','A-Z'),(109,0,92,'text_display','STRING','A-Z'),(110,0,92,'text','STRING','A-Z'),(111,0,93,'time_format','INTEGER','0-2'),(112,0,93,'text','STRING','A-Z'),(113,0,94,'time_hrs','INTEGER','1-24'),(114,0,94,'time_mins','INTEGER','1-60'),(115,0,94,'text','STRING','A-Z'),(116,0,95,'loop_thru','INTEGER','0-1'),(117,0,95,'port_name','STRING','A-Z'),(118,0,96,'mute_status','INTEGER','0-1'),(119,0,96,'port_name','STRING','A-Z'),(120,0,97,'port_name','STRING','A-Z'),(121,0,98,'port_name','STRING','A-Z'),(122,0,99,'port_name','STRING','A-Z'),(123,0,102,'port_name','STRING','A-Z'),(124,0,103,'port_id','INTEGER','0'),(125,0,104,'port_id','INTEGER','0'),(126,0,105,'port_name','STRING','A-Z'),(127,0,106,'port_name','STRING','A-Z'),(128,0,107,'port_name','STRING','A-Z'),(129,0,108,'ocapId','STRING','A-Z'),(130,0,112,'ocapId','STRING','A-Z'),(134,0,115,'timePosition','STRING','A-Z'),(135,0,115,'PlaySpeed','STRING','A-Z'),(137,0,117,'port_name','STRING','A-Z'),(138,0,118,'port_name','STRING','A-Z'),(139,0,124,'service_name','STRING','A-Z'),(140,0,125,'service_name','STRING','A-Z'),(141,0,126,'service_name','STRING','A-Z'),(142,0,81,'audio_level','FLOAT','1-10'),(143,0,82,'db_level','FLOAT','1-100'),(145,0,128,'recordingId','STRING','A-Z'),(152,0,142,'rmfapp_command','STRING','any alphanumeric sequence'),(154,0,149,'service_name','STRING','A-Z'),(155,0,150,'enable','INTEGER','0,1'),(156,0,151,'enable','INTEGER','0,1'),(158,0,153,'apiVersion','INTEGER','1-1000'),(159,0,154,'service_name','STRING','A-Z'),(160,0,154,'event_name','STRING','A-Z'),(161,0,152,'device_name','STRING','A-Z & 1-1000'),(162,0,153,'service_name','STRING','A-Z'),(163,0,156,'videoDisplay','STRING','A-Z'),(164,0,157,'videoDisplay','STRING','A-Z'),(165,0,156,'zoomLevel','STRING','A-Z'),(166,0,157,'resolution','STRING','A-Z'),(189,0,177,'status','INTEGER','0-1'),(193,0,182,'trickPlayStatus','INTEGER','0-1'),(195,0,173,'Categories','STRING','A-Z'),(196,0,173,'ccAttribute','INTEGER','1 - 14'),(197,0,173,'value','INTEGER','1-8'),(198,0,173,'ccType','INTEGER','0-1'),(199,0,173,'stylevalue','STRING','A-Z'),(201,0,164,'channel_num','INTEGER','1-63'),(202,0,166,'analog_channel_num','INTEGER','1-8'),(212,0,30,'appname','STRING','A-Z'),(214,0,22,'testapp_API1_data','INTEGER','1-1000'),(215,0,22,'testapp_API0_data','INTEGER','1-1000'),(254,0,211,'pauseuri','STRING','A-Z'),(259,0,216,'playuri','STRING','A-Z'),(264,0,224,'playuri','STRING','A-Z'),(266,0,224,'Y','INTEGER','0-1'),(267,0,224,'X','INTEGER','0-1'),(268,0,224,'H','INTEGER','0-10000'),(269,0,224,'W','INTEGER','0-10000'),(277,0,224,'apply','INTEGER','0,1'),(283,0,223,'playuri','STRING','A-Z'),(284,0,202,'Volume','FLOAT','0-100'),(286,0,227,'playuri','STRING','A-Z'),(301,0,230,'Volume','FLOAT','0-100'),(302,0,230,'X','INTEGER','0-1'),(303,0,230,'Y','INTEGER','0-1'),(304,0,230,'H','INTEGER','0-10000'),(305,0,230,'W','INTEGER','0-1000'),(306,0,230,'apply','INTEGER','0,1'),(307,0,230,'playuri','STRING','A-Z'),(313,0,231,'playuri','STRING','A-Z'),(314,0,232,'X','INTEGER','0-1'),(315,0,232,'Y','INTEGER','0-1'),(316,0,232,'H','INTEGER','0-10000'),(317,0,232,'W','INTEGER','0-1000'),(318,0,232,'playuri','STRING','A-Z'),(319,0,232,'apply','INTEGER','0,1'),(374,0,270,'recordingId','INTEGER','usually 5 digit nos '),(375,0,270,'playUrl','STRING','play url'),(385,0,277,'module','STRING','A-Z'),(386,0,277,'level','STRING','A-Z'),(387,0,278,'module','STRING','A-Z'),(390,0,279,'module','STRING','A-Z'),(393,0,283,'module','STRING','A-Z'),(394,0,283,'level','STRING','A-Z'),(395,0,280,'number','INTEGER','0-100'),(396,0,281,'number','INTEGER','0-100'),(397,0,285,'ocaplocator','STRING','A-Z'),(398,0,293,'ocaplocator','STRING','A-Z'),(399,0,294,'ocaplocator','STRING','A-Z'),(400,0,295,'ocaplocator','STRING','A-Z'),(401,0,296,'ocaplocator','STRING','A-Z'),(402,0,297,'ocaplocator','STRING','A-Z'),(403,0,300,'ocaplocator','STRING','A-Z'),(404,0,301,'ocaplocator','STRING','A-Z'),(405,0,301,'newocaplocator','STRING','A-Z'),(406,0,304,'index','INTEGER','0-100'),(407,0,305,'recordingId','STRING','A-Z'),(408,0,306,'recordingId','STRING','A-Z'),(409,0,307,'recordingId','STRING','A-Z'),(410,0,308,'recordingId','STRING','A-Z'),(411,0,309,'recordingId','STRING','A-Z'),(412,0,311,'duration','INTEGER','long long (+positive no)'),(413,0,312,'recordingTitle','STRING','A-Z'),(414,0,312,'recordingId','STRING','A-Z'),(415,0,312,'recordDuration','DOUBLE','+ postive no'),(416,0,312,'qamLocator','STRING','qam locator string'),(417,0,313,'recordingId','STRING','A-Z'),(418,0,314,'recordingId','STRING','A-Z'),(419,0,316,'tsbId','STRING','negative long long'),(420,0,316,'recordingId','STRING','A-Z'),(421,0,317,'index','INTEGER','0-100'),(488,0,350,'URL','STRING','A-Z'),(489,0,351,'VideostreamURL','STRING','A-Z'),(490,0,351,'play_time','INTEGER','0-50'),(492,0,353,'recordingTitle','STRING','A-Z'),(493,0,353,'recordingId','STRING','A-Z'),(494,0,353,'recordDuration','DOUBLE','1-1000'),(495,0,353,'qamLocator','STRING','A-Z'),(496,0,351,'SkipTime','INTEGER','0-100'),(497,0,354,'rmfElement','STRING','A-Z'),(498,0,355,'rmfElement','STRING','A-Z'),(499,0,356,'rmfElement','STRING','A-Z'),(500,0,357,'url','STRING','A-Z'),(501,0,357,'rmfElement','STRING','A-Z'),(502,0,358,'rmfElement','STRING','A-Z'),(503,0,359,'rmfElement','STRING','A-Z'),(504,0,360,'rmfElement','STRING','A-Z'),(505,0,360,'playSpeed','FLOAT','1-100'),(506,0,360,'playTime','DOUBLE','0-100'),(507,0,360,'defaultPlay','INTEGER','0-1'),(508,0,361,'rmfSourceElement','STRING','A-Z'),(509,0,361,'rmfSinkElement','STRING','A-Z'),(510,0,362,'apply','INTEGER','0-1'),(511,0,362,'X','INTEGER','0-100'),(512,0,362,'Y','INTEGER','0-100'),(513,0,362,'height','INTEGER','1-10000'),(514,0,362,'width','INTEGER','1-10000'),(515,0,363,'playSpeed','FLOAT','1-100'),(516,0,364,'rmfElement','STRING','A-Z'),(517,0,363,'rmfElement','STRING','A-Z'),(518,0,365,'rmfElement','STRING','A-Z'),(519,0,366,'rmfElement','STRING','A-Z'),(520,0,367,'rmfElement','STRING','A-Z'),(521,0,368,'rmfElement','STRING','A-Z'),(522,0,368,'mediaTime','DOUBLE','0-10000'),(523,0,369,'rmfElement','STRING','A-Z'),(529,0,372,'Recording_Id','STRING','0-100000'),(530,0,314,'playUrl','STRING','A-Z'),(531,0,305,'playUrl','STRING','A-Z'),(532,0,306,'playUrl','STRING','A-Z'),(533,0,307,'playUrl','STRING','A-Z'),(534,0,308,'playUrl','STRING','A-Z'),(535,0,309,'playUrl','STRING','A-Z'),(536,0,316,'playUrl','STRING','A-Z'),(537,0,313,'playUrl','STRING','A-Z'),(539,0,304,'playUrl','STRING','A-Z'),(540,0,373,'recordingId','STRING','A-Z'),(541,0,374,'index','INTEGER','0-100'),(544,0,380,'Validurl','STRING','A-Z'),(545,0,381,'videoStreamURL','STRING','A-Z'),(546,0,379,'RecordURL','STRING','A-Z'),(547,0,378,'videoStreamURL','STRING','A-Z'),(548,0,382,'playUrl','STRING','A-Z'),(549,0,383,'playUrl','STRING','A-Z'),(550,0,383,'speed','FLOAT','1-100'),(551,0,384,'playUrl','STRING','A-Z'),(552,0,385,'playUrl','STRING','A-Z'),(553,0,354,'dvrSinkRecordId','STRING','A-Z'),(554,0,385,'rewindSpeed','FLOAT','1-100'),(555,0,386,'playUrl','STRING','A-Z'),(556,0,387,'playUrl','STRING','A-Z'),(557,0,388,'playUrl','STRING','A-Z'),(558,0,388,'rCount','INTEGER','1-100'),(559,0,389,'playUrl','STRING','A-Z'),(560,0,389,'seconds','DOUBLE','1-100'),(561,0,389,'rCount','INTEGER','1-100'),(562,0,390,'playUrl','STRING','A-Z'),(564,0,390,'rCount','INTEGER','1-100'),(565,0,390,'seconds','DOUBLE','1-100'),(566,0,391,'playUrl','STRING','A-Z'),(567,0,391,'seconds','DOUBLE','1-100'),(568,0,392,'playUrl','STRING','A-Z'),(569,0,392,'seconds','DOUBLE','1-100'),(570,0,392,'rCount','INTEGER','1-100'),(571,0,393,'playUrl','STRING','A-Z'),(572,0,393,'seconds','DOUBLE','1-100'),(573,0,394,'playUrl','STRING','A-Z'),(574,0,394,'seconds','DOUBLE','1-100'),(575,0,395,'playUrl','STRING','A-Z'),(576,0,395,'rewindSpeed','FLOAT','1-100'),(577,0,395,'forwardSpeed','FLOAT','1-100'),(578,0,396,'playUrl','STRING','A-Z'),(579,0,396,'rewindSpeed','FLOAT','1-100'),(580,0,396,'forwardSpeed','FLOAT','1-100'),(581,0,397,'playUrl','STRING','A-Z'),(582,0,397,'trickPlayRate','FLOAT','1-100'),(583,0,398,'playUrl','STRING','A-Z'),(584,0,398,'trickPlayRate','FLOAT','1-100'),(585,0,399,'playUrl','STRING','A-Z'),(586,0,399,'sfSeconds','DOUBLE','1-100'),(587,0,399,'sbSeconds','DOUBLE','1-100'),(588,0,399,'rCount','INTEGER','1-100'),(589,0,400,'playUrl','STRING','A-Z'),(590,0,400,'rewindSpeed','FLOAT','1-100'),(591,0,400,'forwardSpeed','FLOAT','1-100'),(592,0,400,'sfSeconds','DOUBLE','1-100'),(593,0,400,'sbSeconds','DOUBLE','1-100'),(594,0,400,'rCount','INTEGER','1-100'),(595,0,401,'playUrl','STRING','A-Z'),(596,0,402,'playUrl','STRING','1-100'),(597,0,403,'Validurl','STRING','A-Z'),(599,0,405,'recordingId','STRING','A-Z'),(600,0,405,'url','STRING','A-Z'),(601,0,405,'recDuration','DOUBLE','1-100'),(602,0,371,'Duration','STRING','Inmillsec'),(603,0,371,'Start_time','STRING','In-MilliSec'),(604,0,371,'Recording_Id','STRING','0-10000'),(605,0,371,'Source_id','STRING','A-Z'),(606,0,371,'UTCTime','STRING','mmddHHMMyyyy'),(607,0,404,'playUrl','STRING','A-Z'),(608,0,416,'url','STRING','A-Z'),(609,0,354,'factoryEnable','STRING','A-Z'),(610,0,354,'qamSrcUrl','STRING','A-Z'),(611,0,359,'factoryEnable','STRING','A-Z'),(612,0,420,'url','STRING','A-Z'),(614,0,420,'socketId','INTEGER','0-100'),(615,0,420,'streamIp','STRING','A-Z'),(616,0,420,'typeFlag','INTEGER','0-1'),(617,0,421,'rmfElement','STRING','A-Z'),(618,0,420,'dctpEnable','STRING','A-Z'),(619,0,376,'VideostreamURL','STRING','A-Z'),(620,0,376,'trickPlayRate','FLOAT','0-100'),(621,0,375,'ValidocapId','STRING','A-Z'),(622,0,420,'useChunkTransfer','STRING','A-Z'),(624,0,422,'VideostreamURL','STRING','A-Z'),(625,0,422,'SpeedRate','FLOAT','0-100'),(631,0,425,'playUrl','STRING','A-Z'),(632,0,424,'recordId','STRING','any alphanumeric sequence'),(633,0,424,'recordDuration','STRING','any alphanumeric sequence'),(634,0,424,'recordTitle','STRING','any alphanumeric sequence'),(635,0,424,'ocapId','STRING','any alphanumeric sequence'),(636,0,426,'resultList','STRING','A-Z'),(637,0,427,'path','STRING','A-Z'),(641,0,29,'state','INTEGER','0-100'),(642,0,29,'error','INTEGER','0-100'),(643,0,29,'payload','STRING','A-Z'),(644,0,429,'module','STRING','A-Z'),(645,0,434,'module','STRING','A-Z'),(646,0,431,'module','STRING','A-Z'),(647,0,433,'module','STRING','A-Z'),(648,0,432,'module','STRING','A-Z'),(649,0,432,'level','STRING','A-Z'),(650,0,432,'msg','STRING','A-Z'),(651,0,438,'path','STRING','A-Z'),(652,0,438,'paramValue','STRING','A-Z'),(654,0,30,'argv1','STRING','ON,OFF,PAIR'),(655,0,441,'module','STRING','A-Z'),(656,0,440,'module','STRING','A-Z'),(657,0,440,'level','STRING','A-Z'),(658,0,207,'X','INTEGER','0-1'),(659,0,207,'H','INTEGER','0-10000'),(660,0,207,'playuri','STRING','A-Z'),(661,0,207,'Y','INTEGER','0-1'),(662,0,207,'apply','INTEGER','0-10000'),(663,0,207,'W','INTEGER','0-10000'),(665,0,450,'propValue','INTEGER','0-1000'),(666,0,454,'propValue','STRING','AZ'),(669,0,459,'propValue','STRING','AZ'),(670,0,460,'recordingId','STRING','A-Z'),(671,0,460,'duration','DOUBLE','0-1000000'),(672,0,460,'locator','STRING','A-Z'),(673,0,465,'propValue','STRING','AZ'),(674,0,467,'propValue','STRING','AZ'),(675,0,461,'duration','DOUBLE','0-1000000'),(676,0,461,'locator','STRING','A-Z'),(679,0,456,'propValue','INTEGER','0-100'),(680,0,443,'propValue','INTEGER','0-100'),(684,0,474,'duration','DOUBLE','0-1000000'),(685,0,474,'locator','STRING','A-Z'),(686,0,475,'duration','DOUBLE','0-1000000'),(687,0,475,'locator','STRING','A-Z'),(688,0,476,'recordingId','STRING','A-Z'),(689,0,476,'duration','DOUBLE','0-1000000'),(690,0,476,'locator','STRING','A-Z'),(691,0,477,'duration','DOUBLE','0-1000000'),(692,0,477,'locator','STRING','A-Z'),(698,0,317,'playUrl','STRING','A-Z'),(701,0,482,'url','STRING','A-Z'),(710,0,354,'newQamSrc','STRING','A-Z'),(711,0,354,'newQamSrcUrl','STRING','A-Z'),(712,0,359,'newQamSrc','STRING','A-Z'),(713,0,361,'newQamSrc','STRING','A-Z'),(714,0,360,'newQamSrc','STRING','A-Z'),(715,0,367,'newQamSrc','STRING','A-Z'),(716,0,487,'service_name','STRING','A-Z'),(717,0,488,'service_name','STRING','A-Z'),(718,0,489,'service_name','STRING','A-Z'),(719,0,490,'logPath','STRING','A-Z'),(720,0,78,'get_only','INTEGER','0-1'),(723,0,78,'text','STRING','A-Z'),(725,0,487,'service_name','STRING','A-Z'),(726,0,488,'service_name','STRING','A-Z'),(727,0,489,'service_name','STRING','A-Z'),(728,0,354,'numOfTimeChannelChange','INTEGER','0-100'),(729,0,416,'numOfTimeChannelChange','INTEGER','0-100'),(730,0,361,'numOfTimeChannelChange','INTEGER','0-100'),(731,0,360,'numOfTimeChannelChange','INTEGER','0-100'),(732,0,367,'numOfTimeChannelChange','INTEGER','0-100'),(734,0,359,'numOfTimeChannelChange','INTEGER','0-100'),(735,0,88,'get_only','INTEGER','0-1'),(736,0,491,'state','INTEGER','0-1'),(737,0,492,'enable','INTEGER','0-1'),(738,0,491,'indicator_name','STRING','A-Z'),(739,0,492,'port_name','STRING','A-Z'),(740,0,75,'color','INTEGER','0-4'),(741,0,75,'indicator_name','STRING','A-Z'),(750,0,460,'startTime','DOUBLE','0-1000000'),(751,0,461,'startTime','DOUBLE','0-1000000'),(752,0,460,'deviceNo','INTEGER','0-5'),(753,0,461,'deviceNo','INTEGER','0-5'),(754,0,460,'hot','INTEGER','0-1'),(755,0,495,'audioVideoStatus','STRING','A-Z'),(756,0,474,'deviceNo','INTEGER','0-5'),(757,0,475,'deviceNo','INTEGER','0-5'),(765,0,505,'evtName','STRING','A-Z'),(766,0,505,'evtValue','STRING','A-Z'),(767,0,506,'logFile','STRING','A-Z'),(768,0,506,'FileNameToCpTdkPath','STRING','A-Z'),(769,0,506,'patternToSearch','STRING','A-Z'),(770,0,507,'logFileToClear','STRING','A-Z'),(771,0,508,'recordId','STRING','A-Z'),(772,0,508,'recordDuration','STRING','A-Z'),(773,0,508,'recordTitle','STRING','A-Z'),(774,0,508,'ocapId','STRING','A-Z'),(775,0,475,'activity','INTEGER','1-2'),(776,0,474,'activity','INTEGER','1-2'),(780,0,447,'deviceNo','INTEGER','0-5'),(782,0,513,'funcName','STRING','A-Z'),(783,0,513,'strParam1','STRING','A-Z'),(784,0,513,'intParam2','INTEGER','0-65535'),(785,0,513,'intParam3','INTEGER','0-65535'),(786,0,513,'intParam4','INTEGER','0-65535');
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
) ENGINE=InnoDB AUTO_INCREMENT=86 DEFAULT CHARSET=latin1;
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
-- Dumping data for table `repeat_pending_execution`
--

LOCK TABLES `repeat_pending_execution` WRITE;
/*!40000 ALTER TABLE `repeat_pending_execution` DISABLE KEYS */;
/*!40000 ALTER TABLE `repeat_pending_execution` ENABLE KEYS */;
UNLOCK TABLES;

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
) ENGINE=InnoDB AUTO_INCREMENT=1155 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `script_file`
--

LOCK TABLES `script_file` WRITE;
/*!40000 ALTER TABLE `script_file` DISABLE KEYS */;
INSERT INTO `script_file` VALUES (1,0,'gst-plugins-rdk',' GstPluginRdk_Aesdecrypt_DecryptEnable_Get_Default'),(2,0,'gst-plugins-rdk',' GstPluginRdk_Dvrsink_RecordId_Set_Prop'),(3,0,'gst-plugins-rdk',' GstPluginRdk_Dvrsrc_Duration_Get_Prop_Default'),(4,0,'closedcaption','CC_Get_Attribute_BGOpacity_default_28'),(5,0,'closedcaption','CC_Get_Attribute_BorderColor_default_34'),(6,0,'closedcaption','CC_Get_Attribute_BorderType_default_33'),(7,0,'closedcaption','CC_Get_Attribute_EdgeColor_default_38'),(8,0,'closedcaption','CC_Get_Attribute_EdgeType_default_37'),(9,0,'closedcaption','CC_Get_Attribute_FontColor_default_26'),(10,0,'closedcaption','CC_Get_Attribute_FontItalic_default_31'),(11,0,'closedcaption','CC_Get_Attribute_FontOpacity_default_27'),(12,0,'closedcaption','CC_Get_Attribute_FontSize_default_30'),(13,0,'closedcaption','CC_Get_Attribute_FontStyle_default_29'),(14,0,'closedcaption','CC_Get_Attribute_FontUnderline_default_32'),(15,0,'closedcaption','CC_Get_Attribute_WinBorderColor_default_35'),(16,0,'closedcaption','CC_Get_Attribute_WinOpacity_default_36'),(17,0,'closedcaption','CC_Get_SupportedServiceNumberCount_ServiceNumber_23'),(18,0,'closedcaption','CC_Hide_22'),(19,0,'closedcaption','CC_Initialization_01'),(20,0,'closedcaption','CC_ResetTrickPlayStatus_24'),(21,0,'closedcaption','CC_SetGet_AnalogChannel_19'),(22,0,'closedcaption','CC_SetGet_Attribute_BgColor_04'),(23,0,'closedcaption','CC_SetGet_Attribute_BgColor_BoundHigh_56'),(24,0,'closedcaption','CC_SetGet_Attribute_BgColor_BoundLow_70'),(25,0,'closedcaption','CC_SetGet_Attribute_BgColor_invalid_42'),(26,0,'closedcaption','CC_SetGet_Attribute_BGOpacity_06'),(27,0,'closedcaption','CC_SetGet_Attribute_BGOpacity_BoundHigh_58'),(28,0,'closedcaption','CC_SetGet_Attribute_BGOpacity_BoundLow_72'),(29,0,'closedcaption','CC_SetGet_Attribute_BGOpacity_invalid_44'),(30,0,'closedcaption','CC_SetGet_Attribute_BorderColor_12'),(31,0,'closedcaption','CC_SetGet_Attribute_BorderColor_BoundHigh_64'),(32,0,'closedcaption','CC_SetGet_Attribute_BorderColor_invalid_50'),(33,0,'closedcaption','CC_SetGet_Attribute_BorderType_11'),(34,0,'closedcaption','CC_SetGet_Attribute_BorderType_BoundHigh_63'),(35,0,'closedcaption','CC_SetGet_Attribute_BorderType_invalid_49'),(36,0,'closedcaption','CC_SetGet_Attribute_EdgeColor_16'),(37,0,'closedcaption','CC_SetGet_Attribute_EdgeColor_BoundHigh_68'),(38,0,'closedcaption','CC_SetGet_Attribute_EdgeColor_invalid_54'),(39,0,'closedcaption','CC_SetGet_Attribute_EdgeType_15'),(40,0,'closedcaption','CC_SetGet_Attribute_EdgeType_BoundHigh_67'),(41,0,'closedcaption','CC_SetGet_Attribute_EdgeType_invalid_53'),(42,0,'closedcaption','CC_SetGet_Attribute_FontColor_03'),(43,0,'closedcaption','CC_SetGet_Attribute_FontColor_190'),(44,0,'closedcaption','CC_SetGet_Attribute_FontColor_191'),(45,0,'closedcaption','CC_SetGet_Attribute_FontColor_192'),(46,0,'closedcaption','CC_SetGet_Attribute_FontColor_193'),(47,0,'closedcaption','CC_SetGet_Attribute_FontColor_194'),(48,0,'closedcaption','CC_SetGet_Attribute_FontColor_195'),(49,0,'closedcaption','CC_SetGet_Attribute_FontColor_196'),(50,0,'closedcaption','CC_SetGet_Attribute_FontColor_BoundHigh_55'),(51,0,'closedcaption','CC_SetGet_Attribute_FontColor_BoundLow_69'),(52,0,'closedcaption','CC_SetGet_Attribute_FontColor_invalid_41'),(53,0,'closedcaption','CC_SetGet_Attribute_FontItalic_09'),(54,0,'closedcaption','CC_SetGet_Attribute_FontItalic_BoundHigh_61'),(55,0,'closedcaption','CC_SetGet_Attribute_FontItalic_BoundLow_75'),(56,0,'closedcaption','CC_SetGet_Attribute_FontItalic_invalid_47'),(57,0,'closedcaption','CC_SetGet_Attribute_FontOpacity_05'),(58,0,'closedcaption','CC_SetGet_Attribute_FontOpacity_BoundHigh_57'),(59,0,'closedcaption','CC_SetGet_Attribute_FontOpacity_invalid_43'),(60,0,'closedcaption','CC_SetGet_Attribute_FontSize_08'),(61,0,'closedcaption','CC_SetGet_Attribute_FontSize_BoundHigh_60'),(62,0,'closedcaption','CC_SetGet_Attribute_FontSize_invalid_46'),(63,0,'closedcaption','CC_SetGet_Attribute_FontStyle_07'),(64,0,'closedcaption','CC_SetGet_Attribute_FontStyle_BoundHigh_59'),(65,0,'closedcaption','CC_SetGet_Attribute_FontStyle_invalid_45'),(66,0,'closedcaption','CC_SetGet_Attribute_FontUnderline_10'),(67,0,'closedcaption','CC_SetGet_Attribute_FontUnderline_BoundHigh_62'),(68,0,'closedcaption','CC_SetGet_Attribute_FontUnderline_BoundLow_76'),(69,0,'closedcaption','CC_SetGet_Attribute_FontUnderline_invalid_48'),(70,0,'closedcaption','CC_SetGet_Attribute_WinBorderColor_13'),(71,0,'closedcaption','CC_SetGet_Attribute_WinBorderColor_BoundHigh_65'),(72,0,'closedcaption','CC_SetGet_Attribute_WinBorderColor_invalid_51'),(73,0,'closedcaption','CC_SetGet_Attribute_WindowOpacity_BoundHigh_66'),(74,0,'closedcaption','CC_SetGet_Attribute_WinOpacity_14'),(75,0,'closedcaption','CC_SetGet_Attribute_WinOpacity_invalid_52'),(76,0,'closedcaption','CC_SetGet_DigitalChannel_17'),(77,0,'closedcaption','CC_SetGet_InvalidDigitalChannel_18'),(78,0,'closedcaption','CC_SetGet_Invalid_AnalogChannel_20'),(79,0,'closedcaption','CC_SetGet_State_02'),(80,0,'closedcaption','CC_SetTrickPlayStatus_25'),(81,0,'closedcaption','CC_Show_21'),(93,0,'xupnp','CT_XUPNP_01'),(94,0,'xupnp','CT_XUPNP_02'),(95,0,'xupnp','CT_XUPNP_03'),(96,0,'xupnp','CT_XUPNP_04'),(97,0,'xupnp','CT_XUPNP_05'),(98,0,'xupnp','CT_XUPNP_06'),(99,0,'xupnp','CT_XUPNP_07'),(100,0,'xupnp','CT_XUPNP_08'),(101,0,'xupnp','CT_XUPNP_09'),(102,0,'xupnp','CT_XUPNP_10'),(103,0,'xupnp','CT_XUPNP_11'),(104,0,'xupnp','CT_XUPNP_12'),(105,0,'xupnp','CT_XUPNP_13'),(106,0,'xupnp','CT_XUPNP_14'),(107,0,'devicesettings','DS_AddDisplayconnection Listener test_14'),(108,0,'devicesettings','DS_Brightness_Persistent_116'),(109,0,'devicesettings','DS_DTCP support test_19'),(110,0,'devicesettings','DS_GetAspect Ratio test_21'),(111,0,'devicesettings','DS_GetAspect_Ratio_Reboot_test_114'),(112,0,'devicesettings','DS_GetDisplayDetails test_22'),(113,0,'devicesettings','DS_GetDisplayDetails_OnDisabledPort_123'),(114,0,'devicesettings','DS_GetDisplayDetails_Reboot_test_113'),(115,0,'devicesettings','DS_HDCP Support test_18'),(116,0,'devicesettings','DS_IsContentProtection test_17'),(117,0,'devicesettings','DS_IsDynamicResolutionsSupport test_20'),(118,0,'devicesettings','DS_LoopThru test_08'),(119,0,'devicesettings','DS_mute_test_09'),(120,0,'devicesettings','DS_PowerMode Listener test_13'),(121,0,'devicesettings','DS_PowerModeToggle_Stress_119'),(122,0,'devicesettings','DS_Resolution test_16'),(123,0,'devicesettings','DS_ResolutionChange_VideoPlay_122'),(124,0,'devicesettings','DS_Resolution_1080i50_test_90'),(125,0,'devicesettings','DS_Resolution_1080i_test_84'),(126,0,'devicesettings','DS_Resolution_1080p24_test_88'),(127,0,'devicesettings','DS_Resolution_1080p30_test_91'),(128,0,'devicesettings','DS_Resolution_1080p60_test_92'),(129,0,'devicesettings','DS_Resolution_1080p_test_89'),(130,0,'devicesettings','DS_Resolution_480i_test_82'),(131,0,'devicesettings','DS_Resolution_480p_test_85'),(132,0,'devicesettings','DS_Resolution_576p50_test_86'),(133,0,'devicesettings','DS_Resolution_720p50_test_87'),(134,0,'devicesettings','DS_Resolution_720p_test_83'),(135,0,'devicesettings','DS_Resolution_Invalid_port_test_93'),(136,0,'devicesettings','DS_Resolution_Invalid_value_test_94'),(137,0,'devicesettings','DS_Resolution_Persistent_118'),(138,0,'devicesettings','DS_Resolution_PortStateChange_120'),(139,0,'devicesettings','DS_Resolution_PowerModeChange_121'),(140,0,'devicesettings','DS_Resolution_STRESS_test_112'),(141,0,'devicesettings','DS_SetAudioLevel test_06'),(142,0,'devicesettings','DS_SetAudioLevel_Maximum_test_52'),(143,0,'devicesettings','DS_SetAudioLevel_Minimum_test_51'),(144,0,'devicesettings','DS_SetAudioLevel_STRESS_test_106'),(145,0,'devicesettings','DS_SetAudioLevel_value in range_test_53'),(146,0,'devicesettings','DS_SetAudioLevel_value outof range_test_54'),(147,0,'devicesettings','DS_SetBlink test_03'),(148,0,'devicesettings','DS_SetBlink_Invalid_test_39'),(149,0,'devicesettings','DS_SetBlink_outofrange_test_40'),(150,0,'devicesettings','DS_SetBlink_STRESS_test_102'),(151,0,'devicesettings','DS_SetBlink_valid_test_38'),(152,0,'devicesettings','DS_SetblueColor_INVALID_LED_32'),(153,0,'devicesettings','DS_SetblueColor_MESSAGE_LED_27'),(154,0,'devicesettings','DS_SetblueColor_POWER_LED_31'),(155,0,'devicesettings','DS_SetblueColor_RECORD_LED_28'),(156,0,'devicesettings','DS_SetblueColor_REMOTE_LED_30'),(157,0,'devicesettings','DS_SetblueColor_RFBYPASS_LED_29'),(158,0,'devicesettings','DS_SetBrightness test_01'),(159,0,'devicesettings','DS_SetBrightness_Maximum value test_24'),(160,0,'devicesettings','DS_SetBrightness_Minimum value test_23'),(161,0,'devicesettings','DS_SetBrightness_STRESS_test_100'),(162,0,'devicesettings','DS_SetBrightness_value in range test_25'),(163,0,'devicesettings','DS_SetBrightness_value out of range test_26'),(164,0,'devicesettings','DS_SetColor test_02'),(165,0,'devicesettings','DS_SetColor_green test_33'),(166,0,'devicesettings','DS_SetColor_invalid_test_37'),(167,0,'devicesettings','DS_SetColor_orange test_36'),(168,0,'devicesettings','DS_SetColor_red test_34'),(169,0,'devicesettings','DS_SetColor_STRESS_test_101'),(170,0,'devicesettings','DS_SetColor_yellow test_35'),(171,0,'devicesettings','DS_SetCompression test_11'),(172,0,'devicesettings','DS_SetCompression_HEAVY_FORMAT_66'),(173,0,'devicesettings','DS_SetCompression_INVALID_FORMAT_68'),(174,0,'devicesettings','DS_SetCompression_LIGHT_FORMAT_64'),(175,0,'devicesettings','DS_SetCompression_MEDIUM_FORMAT_65'),(176,0,'devicesettings','DS_SetCompression_NONE_67'),(177,0,'devicesettings','DS_SetCompression_STRESS_test_109'),(178,0,'devicesettings','DS_SetDB test_07'),(179,0,'devicesettings','DS_SetDB_Invalid_Value_test_58'),(180,0,'devicesettings','DS_SetDB_Maximum_test_55'),(181,0,'devicesettings','DS_SetDB_Minimum_test_56'),(182,0,'devicesettings','DS_SetDb_STRESS_test_107'),(183,0,'devicesettings','DS_SetDB_valid_value_test_57'),(184,0,'devicesettings','DS_SetDFC test_15'),(185,0,'devicesettings','DS_SetDFC_CCO_ZOOM_test_77'),(186,0,'devicesettings','DS_SetDFC_FULL_ZOOM_test_75'),(187,0,'devicesettings','DS_SetDFC_INVALID_ZOOM_test_81'),(188,0,'devicesettings','DS_SetDFC_None_ZOOM_test_74'),(189,0,'devicesettings','DS_SetDFC_PanScan_ZOOM_test_78'),(190,0,'devicesettings','DS_SetDFC_Pillarbox4x3_ZOOM_test_80'),(191,0,'devicesettings','DS_SetDFC_PLATFORM_ZOOM_test_76'),(192,0,'devicesettings','DS_SetDFC_STRESS_test_111'),(193,0,'devicesettings','DS_SetDFC_Zoom16x9_test_79'),(194,0,'devicesettings','DS_SetEncoding test_10'),(195,0,'devicesettings','DS_SetEncoding_AC3_FORMAT_test_59'),(196,0,'devicesettings','DS_SetEncoding_DISPLAY_FORMAT_test_61'),(197,0,'devicesettings','DS_SetEncoding_Invalid_FORMAT_test_63'),(198,0,'devicesettings','DS_SetEncoding_NONE_test_62'),(199,0,'devicesettings','DS_SetEncoding_PCM_FORMAT_test_60'),(200,0,'devicesettings','DS_SetEncoding_STRESS_test_108'),(201,0,'devicesettings','DS_SetPowerMode_Invalid_test_98'),(202,0,'devicesettings','DS_SetPowerMode_OFF_test_96'),(203,0,'devicesettings','DS_SetPowerMode_ON_test_95'),(204,0,'devicesettings','DS_SetPowerMode_STANDBY_test_97'),(205,0,'devicesettings','DS_SetPowerMode_STRESS_test_99'),(206,0,'devicesettings','DS_SetScroll test_05'),(207,0,'devicesettings','DS_SetScroll_Maximum_Value_test_49'),(208,0,'devicesettings','DS_SetScroll_Middle_Value_test_50'),(209,0,'devicesettings','DS_SetScroll_Minimum_Value_test_48'),(210,0,'devicesettings','DS_SetScroll_STRESS_test_105'),(211,0,'devicesettings','DS_SetState_Stress_115'),(212,0,'devicesettings','DS_SetStereoModes test_12'),(213,0,'devicesettings','DS_SetStereoMode_INVALID_FORMAT_73'),(214,0,'devicesettings','DS_SetStereoMode_MONO_FORMAT_69'),(215,0,'devicesettings','DS_SetStereoMode_STEREO_FORMAT_70'),(216,0,'devicesettings','DS_SetStereoMode_STRESS_test_110'),(217,0,'devicesettings','DS_SetStereoMode_SURROUND_FORMAT_71'),(218,0,'devicesettings','DS_SetStereoMode_UNKNOWN_72'),(219,0,'devicesettings','DS_SetTextDisplay_test_46'),(220,0,'devicesettings','DS_SetText_STRESS_test_104'),(221,0,'devicesettings','DS_SetTimeFormat_and_Time test_04'),(222,0,'devicesettings','DS_SetTime_12HR_FORMAT_41'),(223,0,'devicesettings','DS_SetTime_24HR_FORMAT_42'),(224,0,'devicesettings','DS_SetTime_FORMAT_STRESS_test_103'),(225,0,'devicesettings','DS_SetTime_INVALID_45'),(226,0,'devicesettings','DS_SetTime_INVALID_FORMAT_44'),(227,0,'devicesettings','DS_SetTime_STRING_FORMAT_43'),(228,0,'devicesettings','DS_TextBrightness_Persistent_117'),(230,0,'tdk_integration','E2E_DVRTrickPlay_Fwd_0.5x_03'),(231,0,'tdk_integration','E2E_DVRTrickPlay_Fwd_15x_07'),(232,0,'tdk_integration','E2E_DVRTrickPlay_Fwd_30x_09'),(233,0,'tdk_integration','E2E_DVRTrickPlay_Fwd_4x_05'),(234,0,'tdk_integration','E2E_DVRTrickPlay_Fwd_60x_11'),(235,0,'tdk_integration','E2E_DVRTrickPlay_Invalid_PlaySpeed_12'),(236,0,'tdk_integration','E2E_DVRTrickPlay_Rwd_0.5x_02'),(237,0,'tdk_integration','E2E_DVRTrickPlay_Rwd_15x_06'),(238,0,'tdk_integration','E2E_DVRTrickPlay_Rwd_30x_08'),(239,0,'tdk_integration','E2E_DVRTrickPlay_Rwd_4x_04'),(240,0,'tdk_integration','E2E_DVRTrickPlay_Rwd_60x_10'),(241,0,'tdk_integration','E2E_DVR_Invalid_TimePosition_13'),(242,0,'tdk_integration','E2E_DVR_PlayBack_01'),(243,0,'tdk_integration','E2E_DVR_Skip_Fwd_15'),(244,0,'tdk_integration','E2E_DVR_Skip_Rwd_14'),(245,0,'tdk_integration','E2E_LinearTV_H.264_AAC_26'),(246,0,'tdk_integration','E2E_LinearTV_H.264_AC3_25'),(247,0,'tdk_integration','E2E_LinearTV_H.264_MP3_27'),(248,0,'tdk_integration','E2E_LinearTV_H.264_WAV_28'),(249,0,'tdk_integration','E2E_LinearTV_Live_Trickplay_FFW_15x_11'),(250,0,'tdk_integration','E2E_LinearTV_Live_Trickplay_FFW_30x_12'),(251,0,'tdk_integration','E2E_LinearTV_Live_Trickplay_FFW_4x_10'),(252,0,'tdk_integration','E2E_LinearTV_Live_Trickplay_FFW_60x_13'),(253,0,'tdk_integration','E2E_LinearTV_Live_Trickplay_FRW_15x_14'),(254,0,'tdk_integration','E2E_LinearTV_Live_Trickplay_FRW_30x_15'),(255,0,'tdk_integration','E2E_LinearTV_Live_Trickplay_FRW_4x_09'),(256,0,'tdk_integration','E2E_LinearTV_Live_Trickplay_FRW_60x_16'),(257,0,'tdk_integration','E2E_LinearTV_Live_Trickplay_SFW_0.5x_08'),(258,0,'tdk_integration','E2E_LinearTV_Live_Trickplay_SRW_0.5x_07'),(259,0,'tdk_integration','E2E_LinearTV_MPEG2_AAC_19'),(260,0,'tdk_integration','E2E_LinearTV_MPEG2_MP3_21'),(261,0,'tdk_integration','E2E_LinearTV_MPEG2_WAV_23'),(262,0,'tdk_integration','E2E_LinearTV_MPEG4_AAC_20'),(263,0,'tdk_integration','E2E_LinearTV_MPEG4_AC3_18'),(264,0,'tdk_integration','E2E_LinearTV_MPEG4_MP3_22'),(265,0,'tdk_integration','E2E_LinearTV_MPEG4_WAV_24'),(266,0,'tdk_integration','E2E_LinearTV_MPEG_AC3_17'),(267,0,'tdk_integration','E2E_LinearTV_TuneHD-HD_06'),(268,0,'tdk_integration','E2E_LinearTV_TuneHD-SD_05'),(269,0,'tdk_integration','E2E_LinearTV_TuneHD_02'),(270,0,'tdk_integration','E2E_LinearTV_TuneSD-HD_04'),(271,0,'tdk_integration','E2E_LinearTV_TuneSD-SD_03'),(272,0,'tdk_integration','E2E_LinearTV_TuneSD_01'),(273,0,'rmfapp','E2E_rmfapp_help_and_quit'),(274,0,'rmfapp','E2e_rmfApp_ls_quit'),(275,0,'rmfapp','E2E_rmfApp_play_and_quit'),(276,0,'rmfapp','E2E_rmfapp_record_and_quit'),(277,0,'tdk_integration','E2E_RMF_backtoback_record_samechannel'),(278,0,'tdk_integration','E2E_RMF_DVR_book_record_playback'),(279,0,'tdk_integration','E2E_RMF_DVR_playback_H264'),(280,0,'tdk_integration','E2E_RMF_DVR_playback_ongoingrecord_liverecord'),(281,0,'tdk_integration','E2E_RMF_DVR_playback_radiochannel'),(282,0,'tdk_integration','E2E_RMF_DVR_playback_reccont_lessthanoneminute'),(283,0,'tdk_integration','E2E_RMF_DVR_playback_recordcont_liveplayback_AudioChannel'),(284,0,'tdk_integration','E2E_RMF_DVR_simultaneous_recording_dvrplayback'),(285,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_01'),(286,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_02'),(287,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_03'),(288,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_04'),(289,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_05'),(290,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_06'),(291,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_07'),(292,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_08'),(293,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_09'),(294,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_10'),(295,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_13'),(296,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_14'),(297,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_15'),(298,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_16'),(299,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_17'),(300,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_18'),(301,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_19'),(302,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_20'),(303,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_21'),(304,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_22'),(305,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_25'),(306,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_26'),(307,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_27'),(308,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_28'),(309,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_29'),(310,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_30'),(311,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_31'),(312,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_32'),(313,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_33'),(314,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_34'),(315,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_35'),(316,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_36'),(317,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_37'),(318,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_38'),(319,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_39'),(320,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_40'),(321,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_41'),(322,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_43'),(323,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_44'),(324,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_45'),(325,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_46'),(326,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_48'),(327,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_49'),(328,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_50'),(329,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_51'),(330,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_52'),(331,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_54'),(332,0,'tdk_integration','E2E_RMF_DVR_TrickPlay_55'),(333,0,'tdk_integration','E2E_RMF_DVR_trickplay_currentrecord_liveplayback'),(334,0,'tdk_integration','E2E_RMF_DVR_trickplay_recordcont_liveplayback_radiochannel'),(335,0,'tdk_integration','E2E_RMF_H264_Recording'),(336,0,'tdk_integration','E2E_RMF_HDtoRadioChannel'),(337,0,'tdk_integration','E2E_RMF_LinearTV_ClosedCaption_LivePlayback'),(338,0,'tdk_integration','E2E_RMF_LinearTV_DSSetMute_PowerMode_LivePlayback'),(339,0,'tdk_integration','E2E_RMF_LinearTV_DSSetPowerMode_LivePlayback'),(340,0,'tdk_integration','E2E_RMF_LinearTV_DSSetResolution_LivePlayback'),(341,0,'tdk_integration','E2E_RMF_LinearTV_DSSetResolution_Reboot_LivePlayback'),(342,0,'tdk_integration','E2E_Rmf_LinearTV_H.264_AAC_26'),(343,0,'tdk_integration','E2E_Rmf_LinearTV_H.264_AC3_25'),(344,0,'tdk_integration','E2E_Rmf_LinearTV_H.264_MP3_27'),(345,0,'tdk_integration','E2E_Rmf_LinearTV_H.264_WAV_28'),(346,0,'tdk_integration','E2E_Rmf_LinearTV_MPEG2_AAC_19'),(347,0,'tdk_integration','E2E_Rmf_LinearTV_MPEG2_AC3_17'),(348,0,'tdk_integration','E2E_Rmf_LinearTV_MPEG2_MP3_21'),(349,0,'tdk_integration','E2E_Rmf_LinearTV_MPEG2_WAV_23'),(350,0,'tdk_integration','E2E_Rmf_LinearTV_MPEG4_AAC_20'),(351,0,'tdk_integration','E2E_Rmf_LinearTV_MPEG4_AC3_18'),(352,0,'tdk_integration','E2E_Rmf_LinearTV_MPEG4_MP3_22'),(353,0,'tdk_integration','E2E_Rmf_LinearTV_MPEG4_WAV_24'),(354,0,'tdk_integration','E2E_RMF_LinearTV_Stress_HD_LivePlayback_Longduration'),(355,0,'tdk_integration','E2E_RMF_LinearTV_Stress_LiveDvrPlay_LongDuration'),(356,0,'tdk_integration','E2E_RMF_LinearTV_Stress_LivePlayback_Longduration'),(357,0,'tdk_integration','E2E_RMF_LinearTV_Stress_LivePlay_SwitchingChannel_LongDuration'),(358,0,'tdk_integration','E2E_Rmf_LinearTV_TuneHD-HD_06'),(359,0,'tdk_integration','E2E_Rmf_LinearTV_TuneHD-SD_05'),(360,0,'tdk_integration','E2E_RMF_LinearTV_TuneHD_02'),(361,0,'tdk_integration','E2E_Rmf_LinearTV_TuneSD-HD_04'),(362,0,'tdk_integration','E2E_Rmf_LinearTV_TuneSD-SD_03'),(363,0,'tdk_integration','E2E_Rmf_LinearTV_TuneSD_01'),(364,0,'tdk_integration','E2E_RMF_LinearTV_Tune_InvalidChannel'),(365,0,'tdk_integration','E2E_RMF_LinearTV_Tune_SameChannel'),(366,0,'tdk_integration','E2E_RMF_MDVR_Delete_PausePlay_SameRecord'),(367,0,'tdk_integration','E2E_RMF_MDVR_Delete_SameRecord'),(368,0,'tdk_integration','E2E_RMF_MDVR_Delete_TrickPlay_SameRecord'),(369,0,'tdk_integration','E2E_RMF_MDVR_DvrPlay_DiffUrl'),(370,0,'tdk_integration','E2E_RMF_MDVR_DvrPlay_SameUrl'),(371,1,'tdk_integration','E2E_RMF_DVR_FastForward_Rewind'),(372,1,'tdk_integration','E2E_RMF_DVR_SkipForward_backward_Multiple'),(373,0,'tdk_integration','E2E_RMF_MDVR_Gateway_Client_PausePlay_SameRecord'),(374,0,'tdk_integration','E2E_RMF_MDVR_Gateway_Client_SameRecord'),(375,0,'tdk_integration','E2E_RMF_MDVR_LivePlayPause'),(376,0,'tdk_integration','E2E_RMF_MDVR_LivePlay_DiffUrl'),(377,0,'tdk_integration','E2E_RMF_MDVR_LivePlay_DvrPlay'),(378,0,'tdk_integration','E2E_RMF_MDVR_LivePlay_SameUrl'),(379,0,'tdk_integration','E2E_RMF_MDVR_Max_LivePlay'),(380,0,'tdk_integration','E2E_RMF_MDVR_Max_ScheduleRecording'),(381,0,'tdk_integration','E2E_RMF_MDVR_Max_ScheduleRecording_Neg'),(382,0,'tdk_integration','E2E_RMF_MDVR_PausePlay_SameRecord'),(383,0,'tdk_integration','E2E_RMF_MDVR_SchedLiveRec1_Play2'),(384,0,'tdk_integration','E2E_RMF_MDVR_SchedRec1_Play2'),(385,0,'tdk_integration','E2E_RMF_MDVR_SchedRec_SameChannelSimul'),(386,0,'tdk_integration','E2E_RMF_MDVR_TrickPlay_Gateway_Client_SameRecord'),(387,0,'tdk_integration','E2E_RMF_MDVR_TrickPlay_RadioChannel'),(388,0,'tdk_integration','E2E_RMF_MDVR_TrickPlay_SameRecord'),(389,0,'tdk_integration','E2E_RMF_Multiple_future_recording'),(390,0,'tdk_integration','E2E_RMF_RadioChanneltoHD'),(391,0,'tdk_integration','E2E_RMF_RadioChannel_Recording'),(392,0,'tdk_integration','E2E_RMF_recording_alreadyRecordservice'),(393,0,'tdk_integration','E2E_RMF_Recording_standbymode'),(394,0,'tdk_integration','E2E_RMF_RF_Video_01'),(395,0,'tdk_integration','E2E_RMF_RF_Video_02'),(396,0,'tdk_integration','E2E_RMF_RF_Video_03'),(397,0,'tdk_integration','E2E_RMF_RF_Video_04'),(398,0,'tdk_integration','E2E_RMF_RF_Video_05'),(399,0,'tdk_integration','E2E_RMF_RF_Video_06'),(400,0,'tdk_integration','E2E_RMF_RF_Video_07'),(401,0,'tdk_integration','E2E_RMF_RF_Video_08'),(402,0,'tdk_integration','E2E_RMF_RF_Video_09'),(403,0,'tdk_integration','E2E_RMF_RF_Video_12'),(404,0,'tdk_integration','E2E_RMF_RF_Video_13'),(405,0,'tdk_integration','E2E_RMF_RF_Video_14'),(406,0,'tdk_integration','E2E_RMF_RF_Video_15'),(407,0,'tdk_integration','E2E_RMF_RF_Video_16'),(408,0,'tdk_integration','E2E_RMF_RF_Video_17'),(409,0,'tdk_integration','E2E_RMF_RF_Video_18'),(410,0,'tdk_integration','E2E_RMF_simultaneous_recording'),(411,0,'tdk_integration','E2E_RMF_simultaneous_recording_liveplayback'),(412,0,'tdk_integration','E2E_RMF_standbymode_beforeRecording'),(413,0,'tdk_integration','E2E_RMF_switching_live_TSB'),(414,0,'tdk_integration','E2E_RMF_TSB_FFW_30x_07'),(415,0,'tdk_integration','E2E_RMF_TSB_FFW_60x_09'),(416,0,'tdk_integration','E2E_RMF_TSB_FFW_FFW_15x_15x_41'),(417,0,'tdk_integration','E2E_RMF_TSB_FFW_FFW_15x_4x_29'),(418,0,'tdk_integration','E2E_RMF_TSB_FFW_FFW_30x_15_42'),(419,0,'tdk_integration','E2E_RMF_TSB_FFW_FFW_30x_4x_31'),(420,0,'tdk_integration','E2E_RMF_TSB_FFW_FFW_60x_15x_44'),(421,0,'tdk_integration','E2E_RMF_TSB_FFW_FFW_60x_30x_51'),(422,0,'tdk_integration','E2E_RMF_TSB_FFW_FFW_60x_4x_33'),(423,0,'tdk_integration','E2E_RMF_TSB_FFW_FRW_15x_4x_35'),(424,0,'tdk_integration','E2E_RMF_TSB_FFW_FRW_30x_15x_46'),(425,0,'tdk_integration','E2E_RMF_TSB_FFW_FRW_30x_4x_37'),(426,0,'tdk_integration','E2E_RMF_TSB_FFW_FRW_60x_15x_48'),(427,0,'tdk_integration','E2E_RMF_TSB_FFW_FRW_60x_30x_53'),(428,0,'tdk_integration','E2E_RMF_TSB_FFW_FRW_60x_4x_39'),(429,0,'tdk_integration','E2E_RMF_TSB_FFW_SFW_15x_0.5x_14'),(430,0,'tdk_integration','E2E_RMF_TSB_FFW_SFW_30x_0.5x_16'),(431,0,'tdk_integration','E2E_RMF_TSB_FFW_SFW_4x_0.5x_12'),(432,0,'tdk_integration','E2E_RMF_TSB_FFW_SFW_60x_0.5x_18'),(433,0,'tdk_integration','E2E_RMF_TSB_FFW_SRW_15x_0.5x_22'),(434,0,'tdk_integration','E2E_RMF_TSB_FFW_SRW_30x_0.5x_24'),(435,0,'tdk_integration','E2E_RMF_TSB_FFW_SRW_4x_0.5x_20'),(436,0,'tdk_integration','E2E_RMF_TSB_FFW_SRW_60x_0.5x_26'),(437,0,'tdk_integration','E2E_RMF_TSB_FRW_15x_06'),(438,0,'tdk_integration','E2E_RMF_TSB_FRW_30x_08'),(439,0,'tdk_integration','E2E_RMF_TSB_FRW_60x_10'),(440,0,'tdk_integration','E2E_RMF_TSB_FRW_FFW_15x_4x_30'),(441,0,'tdk_integration','E2E_RMF_TSB_FRW_FFW_30x_15x_43'),(442,0,'tdk_integration','E2E_RMF_TSB_FRW_FFW_30x_4x_32'),(443,0,'tdk_integration','E2E_RMF_TSB_FRW_FFW_4x_4x_28'),(444,0,'tdk_integration','E2E_RMF_TSB_FRW_FFW_60x_15x_45'),(445,0,'tdk_integration','E2E_RMF_TSB_FRW_FFW_60x_30x_52'),(446,0,'tdk_integration','E2E_RMF_TSB_FRW_FFW_60x_4x_34'),(447,0,'tdk_integration','E2E_RMF_TSB_FRW_FFW_60x_55'),(448,0,'tdk_integration','E2E_RMF_TSB_FRW_FRW_ 60x_30x_54'),(449,0,'tdk_integration','E2E_RMF_TSB_FRW_FRW_15x_4x_36'),(450,0,'tdk_integration','E2E_RMF_TSB_FRW_FRW_30x_15x_47'),(451,0,'tdk_integration','E2E_RMF_TSB_FRW_FRW_30x_4x_38'),(452,0,'tdk_integration','E2E_RMF_TSB_FRW_FRW_60x_15x_49'),(453,0,'tdk_integration','E2E_RMF_TSB_FRW_FRW_60x_4x_40'),(454,0,'tdk_integration','E2E_RMF_TSB_FRW_SFW_15x_0.5x_15'),(455,0,'tdk_integration','E2E_RMF_TSB_FRW_SFW_30x_0.5x_17'),(456,0,'tdk_integration','E2E_RMF_TSB_FRW_SFW_4x_0.5x_13'),(457,0,'tdk_integration','E2E_RMF_TSB_FRW_SFW_60x_0.5x_19'),(458,0,'tdk_integration','E2E_RMF_TSB_FRW_SRW_15x_0.5x_23'),(459,0,'tdk_integration','E2E_RMF_TSB_FRW_SRW_30x_0.5x_25'),(460,0,'tdk_integration','E2E_RMF_TSB_FRW_SRW_4x_0.5x_21'),(461,0,'tdk_integration','E2E_RMF_TSB_FRW_SRW_60x_0.5x_27'),(462,0,'tdk_integration','E2E_RMF_TSB_FW_0.5x_01'),(463,0,'tdk_integration','E2E_RMF_TSB_FW_15x_05'),(464,0,'tdk_integration','E2E_RMF_TSB_FW_4x_03'),(465,0,'tdk_integration','E2E_RMF_TSB_FW_RW_0.5x_11'),(466,0,'tdk_integration','E2E_RMF_TSB_Recording'),(467,0,'tdk_integration','E2E_RMF_TSB_RFW_FFW_30x_30x_50'),(468,0,'tdk_integration','E2E_RMF_TSB_RW_0.5x_02'),(469,0,'tdk_integration','E2E_RMF_TSB_RW_4x_04'),(470,0,'openSource_components','Glib_Test'),(471,0,'gst-plugins-rdk','GstPluginRdk_Aesdecrypt_DecryptEnable_False'),(472,0,'gst-plugins-rdk','GstPluginRdk_Aesdecrypt_DecryptEnable_Get_Default'),(473,0,'gst-plugins-rdk','GstPluginRdk_Aesdecrypt_DecryptEnable_Invalid'),(474,0,'gst-plugins-rdk','GstPluginRdk_Aesdecrypt_DecryptEnable_Negative'),(475,0,'gst-plugins-rdk','GstPluginRdk_Aesdecrypt_DecryptEnable_True'),(476,0,'gst-plugins-rdk','GstPluginRdk_Aesencrypt_EncryptEnable_Get_Default'),(477,0,'gst-plugins-rdk','GstPluginRdk_Aesencrypt_EncryptionEnable_False'),(478,0,'gst-plugins-rdk','GstPluginRdk_Aesencrypt_EncryptionEnable_Invalid'),(479,0,'gst-plugins-rdk','GstPluginRdk_Aesencrypt_EncryptionEnable_Negative'),(480,0,'gst-plugins-rdk','GstPluginRdk_Aesencrypt_EncryptionEnable_True'),(481,0,'gst-plugins-rdk','GstPluginRdk_Dvrsink_Ccivalue_Get_Prop_Default'),(482,0,'gst-plugins-rdk','GstPluginRdk_Dvrsink_RecordId_Get_Prop_Default'),(483,0,'gst-plugins-rdk','GstPluginRdk_Dvrsink_RecordId_Set_Prop'),(484,0,'gst-plugins-rdk','GstPluginRdk_Dvrsrc_Ccivalue_Get_Prop_Default'),(485,0,'gst-plugins-rdk','GstPluginRdk_Dvrsrc_Duration_Get_Prop_Default'),(486,0,'gst-plugins-rdk','GstPluginRdk_Dvrsrc_PlayStartPosition_Get_Prop_Default'),(487,0,'gst-plugins-rdk','GstPluginRdk_Dvrsrc_PlayStartPosition_Set_Prop'),(488,0,'gst-plugins-rdk','GstPluginRdk_Dvrsrc_PlayStartPosition_Set_Prop_Negative'),(489,0,'gst-plugins-rdk','GstPluginRdk_Dvrsrc_Rate_Get_Prop_Default'),(490,0,'gst-plugins-rdk','GstPluginRdk_Dvrsrc_Rate_Set_Prop'),(491,0,'gst-plugins-rdk','GstPluginRdk_Dvrsrc_Rate_Set_Prop_ValueGreater_64'),(492,0,'gst-plugins-rdk','GstPluginRdk_Dvrsrc_Rate_Set_Prop_ValueLesser_Negative64'),(493,0,'gst-plugins-rdk','GstPluginRdk_Dvrsrc_RecordId_Get_Prop_Default'),(494,0,'gst-plugins-rdk','GstPluginRdk_Dvrsrc_RecordId_Set_Prop'),(495,0,'gst-plugins-rdk','GstPluginRdk_Dvrsrc_SegmentName_Get_Prop_Default'),(496,0,'gst-plugins-rdk','GstPluginRdk_Dvrsrc_SegmentName_Set_Prop'),(497,0,'gst-plugins-rdk','GstPluginRdk_Dvrsrc_StartTime_Get_Prop_Default'),(498,0,'openSource_components','GstreamerBasePluginTest'),(499,0,'openSource_components','GstreamerGoodPluginTest'),(500,0,'openSource_components','GstreamerTest'),(501,0,'iarmbus','IARMBUS Broadcast IR event'),(502,0,'iarmbus','IARMBUS Broadcast ResolutionChange Event test'),(503,0,'iarmbus','IARMBUS BusCall MFR- Provision Code test'),(504,0,'iarmbus','IARMBUS BusCall MFR-Board description test'),(505,0,'iarmbus','IARMBUS BusCall MFR-Board Product Class test'),(506,0,'iarmbus','IARMBUS BusCall MFR-First Use Date test'),(507,0,'iarmbus','IARMBUS BusCall MFR-Hardware version test'),(508,0,'iarmbus','IARMBUS BusCall MFR-Model Name test'),(509,0,'iarmbus','IARMBUS BusCall MFR-OUI test'),(510,0,'iarmbus','IARMBUS BusCall MFR-SerialNumber test'),(511,0,'iarmbus','IARMBUS BusCall MFR-Software version test'),(512,0,'iarmbus','IARMBUS BusCall MFR-STB Manufature Name test'),(513,0,'iarmbus','IARMBUS BusCall test'),(514,0,'iarmbus','IARMBUS Connect & Disconnect test'),(515,0,'iarmbus','IARMBUS Init Negative test'),(516,0,'iarmbus','IARMBUS IsConnected test'),(517,0,'iarmbus','IARMBUS Query Key Repeat Interval test'),(518,0,'iarmbus','IARMBUS Query Power state'),(519,0,'iarmbus','IARMBUS Register for Resource Available event test'),(520,0,'iarmbus','IARMBUS RegisterCall test'),(521,0,'iarmbus','IARMBUS RegisterEventMax'),(522,0,'iarmbus','IARMBUS Release Resource test'),(523,0,'iarmbus','IARMBUS Request decoder-0 test'),(524,0,'iarmbus','IARMBUS Request decoder-1 test'),(525,0,'iarmbus','IARMBUS Request display_resolution_change  test'),(526,0,'iarmbus','IARMBUS Request graphics plane-0 test'),(527,0,'iarmbus','IARMBUS Request graphics plane-1 test'),(528,0,'iarmbus','IARMBUS Request power  test'),(529,0,'iarmbus','IARMBUS Request same resource from same application test'),(530,0,'iarmbus','IARMBUS Request same resource in different application test'),(531,0,'iarmbus','IARMBUS Set Key Repeat Interval test'),(532,0,'iarmbus','IARMBUS Set Power state'),(533,0,'iarmbus','IARMBUS Unregister with out Register Event Handler test'),(534,0,'iarmbus','IARMBUS unregisterEvt Handler test'),(535,0,'iarmbus','IARMBUS_BusCall_MFR-DeletePDRI_image_61'),(536,0,'iarmbus','IARMBUS_BusCall_MFR-Device_MAC_58'),(537,0,'iarmbus','IARMBUS_BusCall_MFR-HDMIHDCP_60'),(538,0,'iarmbus','IARMBUS_BusCall_MFR-MOCA_MAC_59'),(539,0,'iarmbus','IARMBUS_BusCall_MFR-Scruballbanks_62'),(540,0,'iarmbus','IARMBUS_BusCall_MFR-Validateandwriteimage_into_flash_63'),(541,0,'iarmbus','IARMBUS_Disconnect_without_connect_55'),(542,0,'iarmbus','IARMBUS_DiskMgr_Event_HwDisk_18'),(543,0,'iarmbus','IARMBUS_DummyCall_Persistent_test'),(544,0,'iarmbus','IARMBUS_DummyEvt_Persistent_test'),(545,0,'iarmbus','IARMBUS_Init_with_Invalidparameter_test_43'),(546,0,'iarmbus','IARMBUS_Init_with_Invalid_App_test_44'),(547,0,'iarmbus','IARMBUS_IsConnected_Invalid_Membername_54'),(548,0,'iarmbus','IARMBUS_IsConnect_STRESS_57'),(549,0,'iarmbus','IARMBUS_IsConnect_Without_Connect_53'),(550,0,'iarmbus','IARMBUS_RegisterEvtHandler_With_NegId_48'),(551,0,'iarmbus','IARMBUS_RegisterEvtHandler_With_PosId_47'),(552,0,'iarmbus','IARMBUS_RegUnReg_STRESS_51'),(553,0,'iarmbus','IARMBUS_Release_Invalid_Resource_52'),(554,0,'iarmbus','IARMBUS_Request_FOCUS_Resource_50'),(555,0,'iarmbus','IARMBUS_Request_Invalid_Resource_49'),(556,0,'iarmbus','IARMBUS_Request_resource_STRESS_56'),(557,0,'iarmbus','IARMBUS_Reset_WareHouse_state_64'),(558,0,'iarmbus','IARMBUS_Term_Without_Init_42'),(559,0,'iarmbus','IARMBUS_unregisterEvtHandler_With_PosId_45'),(560,0,'iarmbus','IARM_BUS_DiskMgr_Event_ExtHDD_19'),(561,0,'iarmbus','IARM_BUS_DiskMgr_Event_ExtHDD_Off_22'),(562,0,'iarmbus','IARM_BUS_DiskMgr_Event_ExtHDD_On_21'),(563,0,'iarmbus','IARM_BUS_DiskMgr_Event_ExtHDD_Pair_20'),(564,0,'iarmbus','IARM_BUS_IRMgr_IRKey_ChangeChannelVol'),(565,0,'iarmbus','IARM_BUS_IRMgr_IRKey_CheckSearch'),(566,0,'iarmbus','IARM_BUS_IRMgr_IRKey_CheckSetup'),(567,0,'iarmbus','IARM_BUS_IRMgr_IRKey_CheckTrickplay'),(568,0,'iarmbus','IARM_BUS_IRMgr_IRKey_Toggle'),(569,0,'iarmbus','IARM_BUS_SysMgr_Event_Card_FwDNLD_73'),(570,0,'iarmbus','IARM_BUS_SysMgr_Event_HDCPProfile_update_74'),(571,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_70'),(572,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_BootUp_66'),(573,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_CableCardDWLD_99'),(574,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_CableCard_98'),(575,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_CableCard_SerialNo_104'),(576,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_CardCisco_Status_82'),(577,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_CASystem_90'),(578,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_ChannelMap_75'),(579,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_CMAC_79'),(580,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_CVRSubsystem_100'),(581,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_DACId_106'),(582,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_DAC_InitTimeStamp_103'),(583,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_DisconnectMGR_76'),(584,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_Docsis_95'),(585,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_Download_101'),(586,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_DsgBroadCastChannel_96'),(587,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_DSG_CATunnel_97'),(588,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_ECMIP_92'),(589,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_ECMMac_105'),(590,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_EstbIP_91'),(591,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_ExitOk_78'),(592,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_FirmwareDWLD_87'),(593,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_GetSetHDCPProfile_67'),(594,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_HDCPEnabled_85'),(595,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_HDCPProfileEvent_68'),(596,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_HDMIOut_84'),(597,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_HDMI_EDID_Ready_86'),(598,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_LANIP_93'),(599,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_Moca_94'),(600,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_MotoEntitlement_80'),(601,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_MotoHRVRX_81'),(602,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_PlantId_107'),(603,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_StbSerialNo_65'),(604,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_TimeSource_88'),(605,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_TimeZone_89'),(606,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_TuneReady_77'),(607,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_VideoPresenting_83'),(608,0,'iarmbus','IARM_BUS_SysMgr_Event_SysState_VOD_AD_102'),(609,0,'iarmbus','IARM_BUS_SysMgr_Event_XUPNP_Data_Request_71'),(610,0,'iarmbus','IARM_BUS_SysMgr_Event_XUPNP_Data_Update_72'),(611,0,'openSource_components','Jansson_Test'),(612,0,'openSource_components','libsoup_Test'),(613,0,'mediastreamer','MS_DVRTrickplay_Functionality_Test_09'),(614,0,'mediastreamer','MS_DVRTrickplay_Invalid_Playspeed_10'),(615,0,'mediastreamer','MS_DVRTrickplay_Invalid_Timeposition_11'),(616,0,'mediastreamer','MS_LiveTune_Improper_Requesturl_02'),(617,0,'mediastreamer','MS_LiveTune_Playback_07'),(618,0,'mediastreamer','MS_LiveTune_Valid_Request_01'),(619,0,'mediastreamer','MS_Recordedcontent_playback_08'),(620,0,'mediastreamer','MS_RecordingList_Format_Test_05'),(621,0,'mediastreamer','MS_Recording_Improper_Requesturl_04'),(622,0,'mediastreamer','MS_Recording_Metadata_Format_Test_06'),(623,0,'mediastreamer','MS_Recording_Request_03'),(624,0,'openSource_components','Openssl_Test'),(625,0,'openSource_components','Qt5Webkit_Test'),(626,0,'openSource_components','Qt5_Test'),(627,0,'openSource_components','QtTest_DirectFB'),(628,0,'openSource_components','QtTest_Intelce'),(629,0,'rdk_logger','RDKLogger_CheckMPELogEnabled'),(630,0,'rdk_logger','RDKLogger_Dbg_Enabled_Status'),(631,0,'rdk_logger','RDKLogger_EnvGet'),(632,0,'rdk_logger','RDKLogger_EnvGetModFromNum'),(633,0,'rdk_logger','RDKLogger_EnvGetNum'),(634,0,'rdk_logger','RDKLogger_EnvGetValueFromNum'),(635,0,'rdk_logger','RDKLogger_GetDefaultLevel'),(636,0,'rdk_logger','RDKLogger_GetEnv_UnknownModule'),(637,0,'rdk_logger','RDKLogger_GetLogLevel'),(638,0,'rdk_logger','RDKLogger_Init'),(639,0,'rdk_logger','RDKLogger_Log'),(640,0,'rdk_logger','RDKLogger_Log_All'),(641,0,'rdk_logger','RDKLogger_Log_All_None'),(642,0,'rdk_logger','RDKLogger_Log_Debug'),(643,0,'rdk_logger','RDKLogger_Log_DefaultLevel'),(644,0,'rdk_logger','RDKLogger_Log_Error'),(645,0,'rdk_logger','RDKLogger_Log_Fatal'),(646,0,'rdk_logger','RDKLogger_Log_Info'),(647,0,'rdk_logger','RDKLogger_Log_InvalidLevel'),(648,0,'rdk_logger','RDKLogger_Log_InverseLevel'),(649,0,'rdk_logger','RDKLogger_Log_InverseTrace'),(650,0,'rdk_logger','RDKLogger_Log_MPEOSDisabled'),(651,0,'rdk_logger','RDKLogger_Log_None'),(652,0,'rdk_logger','RDKLogger_Log_None_All'),(653,0,'rdk_logger','RDKLogger_Log_Notice'),(654,0,'rdk_logger','RDKLogger_Log_Trace'),(655,0,'rdk_logger','RDKLogger_Log_Trace1'),(656,0,'rdk_logger','RDKLogger_Log_Trace2'),(657,0,'rdk_logger','RDKLogger_Log_Trace3'),(658,0,'rdk_logger','RDKLogger_Log_Trace4'),(659,0,'rdk_logger','RDKLogger_Log_Trace5'),(660,0,'rdk_logger','RDKLogger_Log_Trace6'),(661,0,'rdk_logger','RDKLogger_Log_Trace7'),(662,0,'rdk_logger','RDKLogger_Log_Trace8'),(663,0,'rdk_logger','RDKLogger_Log_Trace9'),(664,0,'rdk_logger','RDKLogger_Log_UnknownModule'),(665,0,'rdk_logger','RDKLogger_Log_Warning'),(666,0,'rdk_logger','RDKLogger_MaxLogLine'),(667,0,'rdk_logger','RDKLogger_SetLogLevel'),(668,0,'recorder','RMFMS_ScheduleRecording_12'),(669,0,'recorder','RMFMS_ScheduleRecording_InvalidSRC_13'),(670,0,'recorder','RMFMS_Schedule_Big_Recording_14'),(671,0,'recorder','RMFMS_Schedule_FutureRecording_15'),(672,0,'recorder','RMFMS_Schedule_MinDuration_Recording_18'),(673,0,'recorder','RMFMS_Schedule_NegDuration_Recording_19'),(674,0,'recorder','RMFMS_Schedule_NegStartTime_Recording_20'),(675,0,'recorder','RMFMS_Schedule_SmallDuration_Recording_17'),(676,0,'recorder','RMFMS_Schedule_ZeroSize_Recording_16'),(677,0,'mediaframework','RMF_DVRManager_ConvertTSBToRecording'),(678,0,'mediaframework','RMF_DVRManager_CreateRecording'),(679,0,'mediaframework','RMF_DVRManager_CreateTSB'),(680,0,'mediaframework','RMF_DVRManager_DeleteRecording'),(681,0,'mediaframework','RMF_DVRManager_GetDefaultTSBMaxDuration'),(682,0,'mediaframework','RMF_DVRManager_GetIsRecordingInProgress'),(683,0,'mediaframework','RMF_DVRManager_GetRecordingCount'),(684,0,'mediaframework','RMF_DVRManager_GetRecordingDuration'),(685,0,'mediaframework','RMF_DVRManager_GetRecordingInfoById'),(686,0,'mediaframework','RMF_DVRManager_GetRecordingInfoById_17'),(687,0,'mediaframework','RMF_DVRManager_GetRecordingInfoByIndex'),(688,0,'mediaframework','RMF_DVRManager_GetRecordingInfoByIndex_16'),(689,0,'mediaframework','RMF_DVRManager_GetRecordingSegmentInfoByIndex'),(690,0,'mediaframework','RMF_DVRManager_GetRecordingSize'),(691,0,'mediaframework','RMF_DVRManager_GetRecordingStartTime'),(692,0,'mediaframework','RMF_DVRManager_GetSegmentsCount'),(693,0,'mediaframework','RMF_DVRManager_GetSpace'),(694,0,'mediaframework','RMF_DVRManager_UpdateRecording'),(695,0,'mediaframework','RMF_DVRSink_InitTerm_01'),(696,0,'mediaframework','RMF_DVRSrcMPSink_BackToBeg_04'),(697,0,'mediaframework','RMF_DVRSrcMPSink_ChangeSpeed_12'),(698,0,'mediaframework','RMF_DVRSrcMPSink_Pause_02'),(699,0,'mediaframework','RMF_DVRSrcMPSink_Play_01'),(700,0,'mediaframework','RMF_DVRSrcMPSink_Resume_03'),(701,0,'mediaframework','RMF_DVRSrcMPSink_SkipNumOfSeconds_SkipBack_06'),(702,0,'mediaframework','RMF_DVRSrcMPSink_SkipNumOfSeconds_SkipFront_07'),(703,0,'mediaframework','RMF_DVRSrcMPSink_SkipToEnd_05'),(704,0,'mediaframework','RMF_DVRSrcMPSink_TrickPlayRate_FF4x_08'),(705,0,'mediaframework','RMF_DVRSrcMPSink_TrickPlayRate_FF64x_09'),(706,0,'mediaframework','RMF_DVRSrcMPSink_TrickPlayRate_FR4x_10'),(707,0,'mediaframework','RMF_DVRSrcMPSink_TrickPlayRate_FR64x_11'),(708,0,'mediaframework','RMF_DVRSrc_GetMediaInfo_09'),(709,0,'mediaframework','RMF_DVRSrc_GetMediaTime_07'),(710,0,'mediaframework','RMF_DVRSrc_GetSetSpeed_06'),(711,0,'mediaframework','RMF_DVRSrc_GetSpeed_05'),(712,0,'mediaframework','RMF_DVRSrc_InitTerm_01'),(713,0,'mediaframework','RMF_DVRSrc_OpenClose_02'),(714,0,'mediaframework','RMF_DVRSrc_Open_10'),(715,0,'mediaframework','RMF_DVRSrc_Open_11'),(716,0,'mediaframework','RMF_DVRSrc_Open_12'),(717,0,'mediaframework','RMF_DVRSrc_Open_13'),(718,0,'mediaframework','RMF_DVRSrc_Open_14'),(719,0,'mediaframework','RMF_DVRSrc_Open_15'),(720,0,'mediaframework','RMF_DVRSrc_Open_16'),(721,0,'mediaframework','RMF_DVRSrc_Play_03'),(722,0,'mediaframework','RMF_DVRSrc_Play_04'),(723,0,'mediaframework','RMF_DVRSrc_SetMediaTime_08'),(724,0,'mediaframework','RMF_DVR_Get_Recording_List'),(725,0,'mediaframework','RMF_Gst_LongDuration_Check_GstBuffer_Crash_55'),(726,0,'mediaframework','RMF_Gst_LongDuration_Check_GstQamTune_Crash_56'),(727,0,'mediaframework','RMF_HNSink_01'),(728,0,'mediaframework','RMF_HNSrcMPSink_InvalidRewindSpeed_10'),(729,0,'mediaframework','RMF_HNSrcMPSink_InvalidSpeed_09'),(730,0,'mediaframework','RMF_HNSrcMPSink_Video_MuteUnmute_06'),(731,0,'mediaframework','RMF_HNSrcMPSink_Video_Pause_02'),(732,0,'mediaframework','RMF_HNSrcMPSink_Video_Play_01'),(733,0,'mediaframework','RMF_HNSrcMPSink_Video_Play_Position_04'),(734,0,'mediaframework','RMF_HNSrcMPSink_Video_Skip_Backward_03'),(735,0,'mediaframework','RMF_HNSrcMPSink_Video_Speed_08'),(736,0,'mediaframework','RMF_HNSrcMPSink_Video_State_05'),(737,0,'mediaframework','RMF_HNSrcMPSink_Video_Volume_07'),(738,0,'mediaframework','RMF_HNSrc_GetBufferedRanges_04'),(739,0,'mediaframework','RMF_HNSrc_GetState_05'),(740,0,'mediaframework','RMF_HNSrc_InitTerm_01'),(741,0,'mediaframework','RMF_HNSrc_MPSink_BufferClearing_17'),(742,0,'mediaframework','RMF_HNSrc_MPSink_ChannelChange_CheckMacroblocking_41'),(743,0,'mediaframework','RMF_HNSrc_MPSink_Clearbuffering&CheckMediaTime_18'),(744,0,'mediaframework','RMF_HNSrc_MPSink_DoublePlay_40'),(745,0,'mediaframework','RMF_HNSrc_MPSink_DVRReplay_37'),(746,0,'mediaframework','RMF_HNSrc_MPSink_DVR_FF_16x_30'),(747,0,'mediaframework','RMF_HNSrc_MPSink_DVR_FF_32x_29'),(748,0,'mediaframework','RMF_HNSrc_MPSink_DVR_FF_4x_31'),(749,0,'mediaframework','RMF_HNSrc_MPSink_DVR_FF_64x_32'),(750,0,'mediaframework','RMF_HNSrc_MPSink_DVR_FF_RW_CheckMacroblocking_42'),(751,0,'mediaframework','RMF_HNSrc_MPSink_DVR_FF_RW_SB_CheckMacroblocking_46'),(752,0,'mediaframework','RMF_HNSrc_MPSink_DVR_FF_RW_SF_CheckMacroblocking_44'),(753,0,'mediaframework','RMF_HNSrc_MPSink_DVR_Play_26'),(754,0,'mediaframework','RMF_HNSrc_MPSink_DVR_REW_16x_35'),(755,0,'mediaframework','RMF_HNSrc_MPSink_DVR_REW_32x_34'),(756,0,'mediaframework','RMF_HNSrc_MPSink_DVR_REW_4x_36'),(757,0,'mediaframework','RMF_HNSrc_MPSink_DVR_REW_64x_33'),(758,0,'mediaframework','RMF_HNSrc_MPSink_DVR_RW_FF_CheckMacroblocking_43'),(759,0,'mediaframework','RMF_HNSrc_MPSink_DVR_RW_FF_SB_CheckMacroblocking_47'),(760,0,'mediaframework','RMF_HNSrc_MPSink_DVR_RW_FF_SF_CheckMacroblocking_45'),(761,0,'mediaframework','RMF_HNSrc_MPSink_DVR_SB_SF_CheckMacroblocking_49'),(762,0,'mediaframework','RMF_HNSrc_MPSink_DVR_SF_SB_CheckMacroblocking_48'),(763,0,'mediaframework','RMF_HNSrc_MPSink_FF_16x_22'),(764,0,'mediaframework','RMF_HNSrc_MPSink_FF_32x_28'),(765,0,'mediaframework','RMF_HNSrc_MPSink_FF_4x_21'),(766,0,'mediaframework','RMF_HNSrc_MPSink_FF_64x_20'),(767,0,'mediaframework','RMF_HNSrc_MPSink_GetState_25'),(768,0,'mediaframework','RMF_HNSrc_MPSink_InvalidMediaTime_13'),(769,0,'mediaframework','RMF_HNSrc_MPSink_InvalidMediaTime_14'),(770,0,'mediaframework','RMF_HNSrc_MPSink_LivetsbReset_19'),(771,0,'mediaframework','RMF_HNSrc_MPSink_Pause&CheckMediaTime_15'),(772,0,'mediaframework','RMF_HNSrc_MPSink_Pause&FF_39'),(773,0,'mediaframework','RMF_HNSrc_MPSink_Pause&Rewind_38'),(774,0,'mediaframework','RMF_HNSrc_MPSink_Rewind&CheckSpeed_16'),(775,0,'mediaframework','RMF_HNSrc_MPSink_REW_16x_23'),(776,0,'mediaframework','RMF_HNSrc_MPSink_REW_4x_24'),(777,0,'mediaframework','RMF_HNSrc_MPSink_SetGetmediaTime_03'),(778,0,'mediaframework','RMF_HNSrc_MPSink_SetSpeed_32x_11'),(779,0,'mediaframework','RMF_HNSrc_MPSink_SetSpeed_64x_12'),(780,0,'mediaframework','RMF_HNSrc_MPSink_Startoftsb_27'),(781,0,'mediaframework','RMF_HNSrc_MPSink_TSB_ChangeResolution_Check_54'),(782,0,'mediaframework','RMF_HNSrc_MPSink_TSB_FF_CheckMacroblocking_50'),(783,0,'mediaframework','RMF_HNSrc_MPSink_TSB_FF_RW_CheckMacroblocking_51'),(784,0,'mediaframework','RMF_HNSrc_MPSink_TSB_SF_CheckMacroblocking_52'),(785,0,'mediaframework','RMF_HNSrc_MPSink_TSB_SF_CheckMacroblocking_53'),(786,0,'mediaframework','RMF_HNSrc_Open_Emptystring_06'),(787,0,'mediaframework','RMF_HNSrc_Open_invalidurl_07'),(788,0,'mediaframework','RMF_HNSrc_Open_validUrl_11'),(789,0,'mediaframework','RMF_HNSrc_Open_vodurl_08'),(790,0,'mediaframework','RMF_HNSrc_Play_DefaultSpeed_09'),(791,0,'mediaframework','RMF_HNSrc_Play_withoutopen_12'),(792,0,'mediaframework','RMF_HNSRC_Play_withoutsetsource_10'),(793,0,'mediaframework','RMF_HNSrc_SetGetSpeed_02'),(794,0,'mediaframework','RMF_MPSink_GetMediaTime_05'),(795,0,'mediaframework','RMF_MPSink_InitTerm_01'),(796,0,'mediaframework','RMF_MPSink_SetGetMute_03'),(797,0,'mediaframework','RMF_MPSink_SetGetVolume_04'),(798,0,'mediaframework','RMF_MPSink_SetVideoRectangle_02'),(799,0,'mediastreamer','RMF_MS_ContinousCH_Change_test'),(800,0,'mediastreamer','RMF_MS_ContionusDVR_Playback'),(801,0,'mediastreamer','RMF_MS_General_Error_Response'),(802,0,'mediastreamer','RMF_MS_Incomplete_URL_Request'),(803,0,'mediastreamer','RMF_MS_LivePlayback_test'),(804,0,'mediastreamer','RMF_MS_LiveTune_Request'),(805,0,'mediastreamer','RMF_MS_LongTime_LivePlayback'),(806,0,'mediastreamer','RMF_MS_RecordingPlayback'),(807,0,'mediastreamer','RMF_MS_Stress_LiveTune_Test'),(808,0,'mediastreamer','RMF_MS_Without_StreamInit'),(809,0,'mediaframework','RMF_QAMSource_ChangeChannelTwice_PlayOneHour_19'),(810,0,'mediaframework','RMF_QAMSource_ChangeChannel_Check_SPTS_Error_15'),(811,0,'mediaframework','RMF_QAMSource_ChangeChannel_FourTimes_16'),(812,0,'mediaframework','RMF_QAMSource_ChangeChannel_SevenTimes_17'),(813,0,'mediaframework','RMF_QAMSource_ChangeURI_11'),(814,0,'mediaframework','RMF_QAMSource_ChangeURI_14'),(815,0,'mediaframework','RMF_QAMSource_GetLtsId_06'),(816,0,'mediaframework','RMF_QAMSource_GetQAMSourceInstance_10'),(817,0,'mediaframework','RMF_QAMSource_GetTsId_05'),(818,0,'mediaframework','RMF_QAMSource_GetUseFactoryMethods_08'),(819,0,'mediaframework','RMF_QAMSource_Get_Free_LowLevelElement_09'),(820,0,'mediaframework','RMF_QAMSource_InitTerm_01'),(821,0,'mediaframework','RMF_QAMSource_Init_Uninit_Platform_07'),(822,0,'mediaframework','RMF_QAMSource_OpenClose_02'),(823,0,'mediaframework','RMF_QAMSource_Pause_04'),(824,0,'mediaframework','RMF_QAMSource_Pause_13'),(825,0,'mediaframework','RMF_QAMSource_PlayLive_OneHour_18'),(826,0,'mediaframework','RMF_QAMSource_Play_03'),(827,0,'mediaframework','RMF_QAMSource_Play_12'),(828,0,'mediaframework','RMF_QAMSrc_01'),(829,0,'mediaframework','RMF_QAMSrc_02'),(830,0,'mediaframework','RMF_QAMSrc_03'),(831,0,'mediaframework','RMF_QAMSrc_04'),(832,0,'mediaframework','RMF_QAMSrc_05'),(833,0,'mediaframework','RMF_QAMSrc_06'),(834,0,'mediaframework','RMF_QAMSrc_07'),(835,0,'mediaframework','RMF_QAMSrc_08'),(836,0,'mediaframework','RMF_QAMSrc_09'),(837,0,'mediaframework','RMF_QAMSrc_HNSink_01'),(838,0,'mediaframework','RMF_QAMSrc_HNSink_02'),(839,0,'mediaframework','RMF_QAMSrc_HNSink_03'),(840,0,'mediaframework','RMF_QAMSrc_HNSink_04'),(841,0,'mediaframework','RMF_QAMSrc_HNSink_05'),(842,0,'mediaframework','RMF_QAMSrc_HNSink_06'),(843,0,'mediaframework','RMF_QAMSrc_HNSink_07'),(844,0,'mediaframework','RMF_QAMSrc_HNSink_08'),(845,0,'mediaframework','RMF_QAMSrc_HNSink_09'),(846,0,'mediaframework','RMF_QAMSrc_HNSink_10'),(847,0,'mediaframework','RMF_QAMSrc_HNSink_11'),(848,0,'mediaframework','RMF_QAMSrc_HNSink_12'),(849,0,'mediaframework','RMF_QAMSrc_HNSink_13'),(850,0,'mediaframework','RMF_QAMSrc_HNSink_14'),(851,0,'servicemanager','SM_CreateService_All'),(852,0,'servicemanager','SM_DeviceSetting_GetDeviceInfo'),(853,0,'servicemanager','SM_DisplaySetting_SetZoomSettings'),(854,0,'servicemanager','SM_DoesServiceExist Negative test'),(855,0,'servicemanager','SM_DoesServiceExist_All'),(856,0,'servicemanager','SM_EnableMdvr test'),(857,0,'servicemanager','SM_EnableVpop test'),(858,0,'servicemanager','SM_GetGlobal Service test'),(859,0,'servicemanager','SM_GetGlobalService_All'),(860,0,'servicemanager','SM_GetRegisteredService test'),(861,0,'servicemanager','SM_GetSetting_All'),(862,0,'servicemanager','SM_RegisterForEvents test'),(863,0,'servicemanager','SM_RegisterService test'),(864,0,'servicemanager','SM_RegisterService_All'),(865,0,'servicemanager','SM_ScreenCapture_EventUpload'),(866,0,'servicemanager','SM_ScreenCapture_Upload'),(867,0,'servicemanager','SM_Services_GetName_All'),(868,0,'servicemanager','SM_SetApiVersion test'),(869,0,'servicemanager','SM_SetApiVersion_All'),(870,0,'servicemanager','SM_SetDeviceName test'),(871,0,'servicemanager','SM_SetResolution test'),(872,0,'servicemanager','SM_UnRegisterService test'),(873,0,'servicemanager','SM_UnRegisterService_All'),(874,0,'servicemanager','SM_WebSocket_EventsAll'),(875,0,'servicemanager','SM_WebSocket_GetBufferedAmount'),(876,0,'servicemanager','SM_WebSocket_GetProtocol'),(877,0,'servicemanager','SM_WebSocket_GetReadyState'),(878,0,'servicemanager','SM_WebSocket_GetUrl'),(879,0,'rmfapp','tdkRmfApp_CreateRecord'),(880,0,'tdk_integration','TDK_E2E_DVR_Playback_Trickplay_All_Recordings_LongDuration_8hr_test'),(881,0,'tdk_integration','TDK_E2E_LinearTV_Channelchange_LongDuration_8hr_test'),(882,0,'tdk_integration','TDK_E2E_LinearTv_LinearTrickplay_LongDuration_8hr_Test'),(883,0,'tdk_integration','TDK_E2E_LinearTv_SwitchingChannel_DVRForwardAndRewind_LongDuration_8hr_test'),(884,0,'tdk_integration','TDK_E2E_LinearTv_SwitchingChannel_DVRTrickplay_LongDuration_8hr_test'),(885,0,'tdk_integration','TDK_E2E_RMF_LinearTV_ChannelChange_Trickplay_LongDuration_8hr_test'),(886,0,'tdk_integration','TDK_RMF_ScheduleRecording_Playback_LongDuration_8hr_test'),(889,0,'tr69','TR069_Get_DeviceAdditionalSoftwareVersion_09'),(890,0,'tr69','TR069_Get_DeviceDeviceInfoNegative_51'),(891,0,'tr69','TR069_Get_DeviceEthernetInterfaceDefaultDuplexMode_50'),(892,0,'tr69','TR069_Get_DeviceEthernetInterfaceDefaultEnable_44'),(893,0,'tr69','TR069_Get_DeviceEthernetInterfaceDefaultMACAddress_48'),(894,0,'tr69','TR069_Get_DeviceEthernetInterfaceDefaultMaxBitRate_49'),(895,0,'tr69','TR069_Get_DeviceEthernetInterfaceDefaultName_46'),(896,0,'tr69','TR069_Get_DeviceEthernetInterfaceDefaultStatus_45'),(897,0,'tr69','TR069_Get_DeviceEthernetInterfaceDefaultUpstream_47'),(898,0,'tr69','TR069_Get_DeviceEthernetInterfaceNumOfEntries_43'),(899,0,'tr69','TR069_Get_DeviceFirstUseDate_12'),(900,0,'tr69','TR069_Get_DeviceHardwareVersion_07'),(901,0,'tr69','TR069_Get_DeviceIPActivePortNumOfEntries_33'),(902,0,'tr69','TR069_Get_DeviceIPDefaultInterfaceEnable_34'),(903,0,'tr69','TR069_Get_DeviceIPDefaultInterfaceIPv4Enable_35'),(904,0,'tr69','TR069_Get_DeviceIPDefaultInterfaceLoopback_41'),(905,0,'tr69','TR069_Get_DeviceIPDefaultInterfaceMaxMTUSize_39'),(906,0,'tr69','TR069_Get_DeviceIPDefaultInterfaceName_37'),(907,0,'tr69','TR069_Get_DeviceIPDefaultInterfaceReset_38'),(908,0,'tr69','TR069_Get_DeviceIPDefaultInterfaceStatus_36'),(909,0,'tr69','TR069_Get_DeviceIPDefaultInterfaceType_40'),(910,0,'tr69','TR069_Get_DeviceIPInterfaceNumOfEntries_32'),(911,0,'tr69','TR069_Get_DeviceIPv4Capable_29'),(912,0,'tr69','TR069_Get_DeviceIPv4Enable_30'),(913,0,'tr69','TR069_Get_DeviceIPv4Status_31'),(914,0,'tr69','TR069_Get_DeviceManufacturerOUI_02'),(915,0,'tr69','TR069_Get_DeviceManufacturer_01'),(916,0,'tr69','TR069_Get_DeviceMemoryStatusFree_27'),(917,0,'tr69','TR069_Get_DeviceMemoryStatusTotal_26'),(918,0,'tr69','TR069_Get_DeviceMoCAInterfaceAssociatedDevice1NodeID_69'),(919,0,'tr69','TR069_Get_DeviceMoCAInterfaceAssociatedDeviceGetNodeID_Neg_70'),(920,0,'tr69','TR069_Get_DeviceMoCAInterfaceAssociatedDeviceNumberOfEntries_68'),(921,0,'tr69','TR069_Get_DeviceMoCAInterfaceCurrentVersion_64'),(922,0,'tr69','TR069_Get_DeviceMoCAInterfaceEnable_54'),(923,0,'tr69','TR069_Get_DeviceMoCAInterfaceFirmwareVersion_59'),(924,0,'tr69','TR069_Get_DeviceMoCAInterfaceHighestVersion_63'),(925,0,'tr69','TR069_Get_DeviceMoCAInterfaceLastChange_56'),(926,0,'tr69','TR069_Get_DeviceMoCAInterfaceMACAddress_58'),(927,0,'tr69','TR069_Get_DeviceMoCAInterfaceMaxBitRate_60'),(928,0,'tr69','TR069_Get_DeviceMoCAInterfaceMaxEgressBW_62'),(929,0,'tr69','TR069_Get_DeviceMoCAInterfaceMaxIngressBW_61'),(930,0,'tr69','TR069_Get_DeviceMoCAInterfaceMaxNodes_67'),(931,0,'tr69','TR069_Get_DeviceMoCAInterfaceNetworkCoordinator_65'),(932,0,'tr69','TR069_Get_DeviceMoCAInterfaceNodeID_66'),(933,0,'tr69','TR069_Get_DeviceMoCAInterfaceNumOfEntries_53'),(934,0,'tr69','TR069_Get_DeviceMoCAInterfaceQoSEgressNumFlows_71'),(935,0,'tr69','TR069_Get_DeviceMoCAInterfaceQoSFlowStats1FlowID_72'),(936,0,'tr69','TR069_Get_DeviceMoCAInterfaceStatus_55'),(937,0,'tr69','TR069_Get_DeviceMoCAInterfaceUpstream_57'),(938,0,'tr69','TR069_Get_DeviceModelName_03'),(939,0,'tr69','TR069_Get_DeviceProcessorArchitecture_25'),(940,0,'tr69','TR069_Get_DeviceProcessorNumOfEntries_17'),(941,0,'tr69','TR069_Get_DeviceProcessStatusCommandDefaultProcess_20'),(942,0,'tr69','TR069_Get_DeviceProcessStatusCPUTimeDefaultProcess_23'),(943,0,'tr69','TR069_Get_DeviceProcessStatusCPUUsage_18'),(944,0,'tr69','TR069_Get_DeviceProcessStatusPIDDefaultProcess_19'),(945,0,'tr69','TR069_Get_DeviceProcessStatusPriorityDefaultProcess_22'),(946,0,'tr69','TR069_Get_DeviceProcessStatusSizeDefaultProcess_21'),(947,0,'tr69','TR069_Get_DeviceProcessStatusStateDefaultProcess_24'),(948,0,'tr69','TR069_Get_DeviceProvisioningCode_10'),(949,0,'tr69','TR069_Get_DeviceSerialNumber_06'),(950,0,'tr69','TR069_Get_DeviceServicesSTBServiceComponentsHDMI1DisplayDeviceEEDID_81'),(951,0,'tr69','TR069_Get_DeviceServicesSTBServiceComponentsHDMI1DisplayDeviceStatus_80'),(952,0,'tr69','TR069_Get_DeviceServicesSTBServiceComponentsHDMI1Enable_75'),(953,0,'tr69','TR069_Get_DeviceServicesSTBServiceComponentsHDMI1Name_77'),(954,0,'tr69','TR069_Get_DeviceServicesSTBServiceComponentsHDMI1ResolutionMode_78'),(955,0,'tr69','TR069_Get_DeviceServicesSTBServiceComponentsHDMI1ResolutionValue_79'),(956,0,'tr69','TR069_Get_DeviceServicesSTBServiceComponentsHDMI1Status_76'),(957,0,'tr69','TR069_Get_DeviceServicesSTBServiceComponentsHDMINumberOfEntries_74'),(958,0,'tr69','TR069_Get_DeviceServicesSTBServiceComponentsVideoDecoder1ContentAspectRatio_85'),(959,0,'tr69','TR069_Get_DeviceServicesSTBServiceComponentsVideoDecoder1Name_84'),(960,0,'tr69','TR069_Get_DeviceServicesSTBServiceComponentsVideoDecoderNumberOfEntries_83'),(961,0,'tr69','TR069_Get_DeviceServicesSTBServiceNumberOfEntries_73'),(962,0,'tr69','TR069_Get_DeviceSevicesSTBServiceComponentsVideoDecoderName_Neg_86'),(963,0,'tr69','TR069_Get_DeviceSoftwareVersion_08'),(964,0,'tr69','TR069_Get_DeviceSTBServiceComponentsHDMIDisplayDevice_XCOM_EDID_82'),(965,0,'tr69','TR069_Get_DeviceUpTime_11'),(966,0,'tr69','TR069_Get_DeviceXCOMFirmwareFileName_15'),(967,0,'tr69','TR069_Get_DeviceXCOMPowerStatus_16'),(968,0,'tr69','TR069_Get_DeviceXCOMSTBIP_14'),(969,0,'tr69','TR069_Get_DeviceXCOMSTBMAC_13'),(970,0,'trm','TRM_CancelLive'),(971,0,'trm','TRM_CancelRecording'),(972,0,'trm','TRM_CT_14'),(973,0,'trm','TRM_CT_15'),(974,0,'trm','TRM_CT_16'),(975,0,'trm','TRM_CT_17'),(976,0,'trm','TRM_CT_18'),(977,0,'trm','TRM_CT_19'),(978,0,'trm','TRM_CT_20'),(979,0,'trm','TRM_CT_21'),(980,0,'trm','TRM_CT_22'),(981,0,'trm','TRM_CT_23'),(982,0,'trm','TRM_CT_24'),(983,0,'trm','TRM_CT_25'),(984,0,'trm','TRM_CT_26'),(985,0,'trm','TRM_CT_27'),(986,0,'trm','TRM_CT_28'),(987,0,'trm','TRM_CT_29'),(988,0,'trm','TRM_CT_30'),(989,0,'trm','TRM_CT_31'),(990,0,'trm','TRM_CT_32'),(991,0,'trm','TRM_CT_33'),(992,0,'trm','TRM_CT_34'),(993,0,'trm','TRM_CT_35'),(994,0,'trm','TRM_CT_36'),(995,0,'trm','TRM_CT_37'),(996,0,'trm','TRM_CT_38'),(997,0,'trm','TRM_CT_39'),(998,0,'trm','TRM_CT_40'),(999,0,'trm','TRM_CT_41'),(1000,0,'trm','TRM_CT_42'),(1001,0,'trm','TRM_CT_43'),(1002,0,'trm','TRM_GetAllReservations'),(1003,0,'trm','TRM_GetAllTunerIds'),(1004,0,'trm','TRM_GetAllTunerStates'),(1005,0,'trm','TRM_GetVersion'),(1007,0,'trm','TRM_TunerReserveAllForLive'),(1008,0,'trm','TRM_TunerReserveAllForRecord'),(1009,0,'trm','TRM_TunerReserveForHyBrid'),(1010,0,'trm','TRM_TunerReserveForLive'),(1011,0,'trm','TRM_TunerReserveForRecord'),(1012,0,'trm','TRM_ValidateTunerReservation'),(1013,0,'openSource_components','WebkitTest_DirectFB'),(1014,0,'openSource_components','WebkitTest_Intelce'),(1015,0,'openSource_components','yajl_Test'),(1019,0,'trm','TRM_ReleaseTunerReservation'),(1024,0,'iarmbus','IARMBUS_PowerModeToggle_Stress'),(1025,0,'tdk_integration','E2E_RMF_delete_liverecord_lessthanonemin'),(1026,0,'tdk_integration','E2E_RMF_delete_ongoingRecord_liverecord_Inprogress'),(1028,0,'tdk_integration','E2E_RMF_DVR_recording_liveStream_watching_liveStream'),(1029,0,'tdk_integration','E2E_RMF_delete_recordcontent_with_another_liverecord'),(1030,0,'tdk_integration','E2E_RMF_DVR_delete_recording'),(1031,0,'tdk_integration','E2E_RMF_DVR_delete_recording_trickplay'),(1032,0,'mediaframework','RMF_Hybrid_Test'),(1037,0,'mediaframework','RMF_DS_Resolution_Hang_Check_01'),(1038,1,'mediaframework','RMF_TSB_Check_Pause_Failure_02'),(1040,0,'mediaframework','RMF_TSB_SlowRewind_Error_Check_03'),(1042,0,NULL,'E2E_RMF_LIVEplayback_delete_recording'),(1043,0,'tdk_integration','E2E_RMF_LIVE_playback_delete_recording'),(1044,0,'mediaframework','RMF_DVRSrcMPSink_FF_Rewind_error_Check_04'),(1047,0,'mediaframework','RMF_TSB_FF_Play_FreezeError_Check_05'),(1050,0,'tdk_integration','DVR_sampletest'),(1052,0,'tdk_integration','E2E_RMF_FFW_LiveVideo'),(1053,0,'iarmbus','IARMBUS_PowerModeToggle_Trickplay'),(1054,0,'trm','TRM_CT_44'),(1055,0,'trm','TRM_CT_45'),(1056,0,'devicesettings','DS_SetTime_VALID_124'),(1057,0,'devicesettings','DS_SetTextBrightness_125'),(1058,0,'devicesettings','DS_Resolution480p_VideoPlay_126'),(1060,0,'tdk_integration','E2E_RMF_DVR_Playback_Gateway_Client'),(1061,0,'mediaframework','RMF_HNSrc_MPSink_DVR_RW_FF_CheckMacroblocking_57'),(1062,0,'mediaframework','RMF_DVRManager_DeleteInvalidRecordingId'),(1063,0,'openSource_components','GstreamerPluginCustomTest'),(1076,0,'dtcp','DTCP_StartSource_02'),(1077,0,'dtcp','DTCP_StopSource_03'),(1078,0,'dtcp','DTCP_SetLogLevel_11'),(1079,0,'dtcp','DTCP_GetNumSessions_09'),(1080,0,'dtcp','DTCP_CreateSrcSess_04'),(1081,0,'dtcp','DTCP_CreateSinkSess_05'),(1082,0,'dtcp','DTCP_DeleteSrcSess_08'),(1083,0,'dtcp','DTCP_GetSrcSessInfo_10'),(1084,0,'dtcp','DTCP_Init_01'),(1085,0,'dtcp','DTCP_ProcessSrcPacket_06'),(1086,0,'dtcp','DTCP_ReleaseSrcPacket_07'),(1088,0,'dtcp','DTCP_GetSinkSessInfo_12'),(1090,0,'dtcp','DTCP_CreateSrcSess_InvalidIp_13'),(1091,0,'dtcp','DTCP_CreateSinkSess_InvalidIp_14'),(1093,0,'dtcp','DTCP_GetNumSess_InvalidType_15'),(1094,0,'dtcp','DTCP_SetInvalidLogLevel_16'),(1095,1,'dtcp','DTCP_StartStopSrc_MultiIface_17'),(1098,0,'tdk_integration','E2E_RMF_LivePlayback_StandbyMode_to_ONMode'),(1099,0,'tdk_integration','E2E_RMF_LivePlayback_StandbyMode'),(1100,0,'tdk_integration','E2E_RMF_DVR_Recording_Reboot_Test'),(1101,0,'tdk_integration','E2E_RMF_DVR_Future_Recording_Reboot_Test'),(1102,0,'tdk_integration','E2E_RMF_DVR_LongDuration_DurationCheck'),(1103,0,'tdk_integration','E2E_RMF_DVR_ShortDuration_DurationCheck'),(1114,0,'dtcp','DTCP_DeleteSinkSess_20'),(1115,0,'dtcp','DTCP_StopWithoutStartSrc_21'),(1116,0,'dtcp','DTCP_StartSource_InvalidPort_22'),(1117,0,'dtcp','DTCP_StartSource_InvalidIfName_23'),(1118,0,'dtcp','DTCP_GetSessInfo_Neg_24'),(1119,0,'dtcp','DTCP_ProcessPacket_Neg_26'),(1120,0,'dtcp','DTCP_CreateSinkSess_InvalidPort_25'),(1121,0,'dtcp','DTCP_ProcessSinkPacket_27'),(1122,0,'dtcp','DTCP_ReleaseSinkPacket_28'),(1123,0,'dtcp','DTCP_DeleteSinkSess_Neg_29'),(1124,0,'dtcp','DTCP_DeleteSrcSess_Neg_30'),(1125,0,'dtcp','DTCP_Init_Stress_31'),(1126,0,'dtcp','DTCP_StopSrcwithActiveSessions_32'),(1127,0,'dtcp','DTCP_GetNumSessions_Sink_18'),(1128,0,'dtcp','DTCP_GetNumSessions_Src_19'),(1131,0,'tdk_integration','E2E_RMF_DVRPlayback_OFF_to_ONMode'),(1132,0,'tdk_integration','E2E_RMF_DVRPlayback_OFFMode'),(1133,0,'tdk_integration','E2E_RMF_DVRPlayback_StandbyMode'),(1134,0,'tdk_integration','E2E_RMF_DVRPlayback_StandbyMode_to_ONMode'),(1135,0,'tdk_integration','E2E_RMF_LivePlayback_OFF_to_ONMode'),(1136,0,'tdk_integration','E2E_RMF_LivePlayback_OFFMode'),(1138,0,'dtcp','DTCP_CreateSrcSessWithoutStartSrc_33'),(1139,0,'dtcp','DTCP_CreateSinkSessWithoutStartSrc_34'),(1142,0,'dtcp','DTCP_MultiStartSource_37'),(1143,0,'dtcp','DTCP_StopAllSources_38'),(1144,0,'dtcp','DTCP_CreateSinkSessOnLoSrcIp_39'),(1145,0,'dtcp','DTCP_UniqueKeyExchange_40'),(1146,0,'tdk_integration','E2E_Set_Resolution_During_Standby'),(1147,0,'tdk_integration','E2E_RMF_LivePlayback_TSB_Increase_StandbyMode'),(1148,0,'tdk_integration','E2E_RMF_LivePlayback_Change_Zoom'),(1149,0,'tdk_integration','E2E_RMF_DVRPlayback_Change_Zoom'),(1150,0,'tdk_integration','E2E_Get_Resolution_During_Standby'),(1152,0,'dtcp','DTCP_CreateMaxSrcSess_36'),(1153,0,'dtcp','DTCP_CreateMaxSinkSess_35');
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
) ENGINE=InnoDB AUTO_INCREMENT=372 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `script_group`
--

LOCK TABLES `script_group` WRITE;
/*!40000 ALTER TABLE `script_group` DISABLE KEYS */;
INSERT INTO `script_group` VALUES (218,88,'closedcaption','FREE',NULL),(220,348,'tdk_integration','FREE',NULL),(221,9,'rmfapp','FREE',NULL),(222,19,'openSource_components','FREE',NULL),(223,145,'iarmbus','FREE',NULL),(224,25,'mediastreamer','FREE',NULL),(225,53,'rdk_logger','FREE',NULL),(226,13,'recorder','FREE',NULL),(227,199,'mediaframework','FREE',NULL),(228,58,'servicemanager','FREE',NULL),(236,2312,'ComponentSuite','FREE',NULL),(237,4062,'IPClient-3Suite','FREE',NULL),(238,5220,'Hybrid-1Suite','FREE',NULL),(244,101,'tr69','FREE',NULL),(263,637,'E2ESuite','FREE',NULL),(273,39,'gst-plugins-rdk','FREE',NULL),(275,102,'trm','FREE',NULL),(295,2674,'RDK2.0_IPClient-3','FREE',NULL),(296,1303,'RDK1.3_Hybrid-1','FREE',NULL),(297,206,'RDK1.2_Hybrid-1','FREE',NULL),(298,5085,'RDK2.0_Hybrid-1','FREE',NULL),(299,971,'RDK1.3_IPClient-3','FREE',NULL),(300,240,'RDK1.2_IPClient-3','FREE',NULL),(321,136,'devicesettings','FREE',NULL),(323,15,'E2ESuite_LD','FREE',NULL),(324,12,'IPClient-3Suite_LD','FREE',NULL),(325,19,'Hybrid-1Suite_LD','FREE',NULL),(326,76,'RDK2.0_IPClient-3_LD','FREE',NULL),(327,149,'RDK2.0_Hybrid-1_LD','FREE',NULL),(328,7,'mediaframework_LD','FREE',NULL),(329,7,'ComponentSuite_LD','FREE',NULL),(330,91,'dtcp','FREE',NULL),(331,17,'xupnp','FREE',NULL),(339,4,'Hybrid-5Suite','FREE',NULL),(340,4,'RDK1.3_Hybrid-5','FREE',NULL),(341,4,'RDK2.0_Hybrid-5','FREE',NULL),(342,3,'tdk_integration_LD','FREE',NULL),(347,2,'RDK1.2_Hybrid-5','FREE',NULL),(360,15,'OpenSourceSuite','FREE',NULL),(371,0,'tdkintegration_new','FREE',NULL);
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
INSERT INTO `script_group_script_file` VALUES (218,23,0),(218,41,1),(218,17,2),(218,60,3),(218,14,4),(218,34,5),(218,21,6),(218,65,7),(218,59,8),(218,5,9),(218,36,10),(218,56,11),(218,30,12),(218,51,13),(218,29,14),(218,77,15),(218,24,16),(218,12,17),(218,10,18),(218,75,19),(218,50,20),(218,40,21),(218,70,22),(218,20,23),(218,31,24),(218,16,25),(218,72,26),(218,9,27),(218,15,28),(218,18,29),(218,52,30),(218,69,31),(218,7,32),(218,27,33),(218,6,34),(218,13,35),(218,55,36),(218,81,37),(218,76,38),(218,54,39),(218,74,40),(218,11,41),(218,61,42),(218,73,43),(218,38,44),(218,28,45),(218,19,46),(218,71,47),(218,78,48),(218,39,49),(218,58,50),(218,62,51),(218,32,52),(218,8,53),(218,63,54),(218,57,55),(218,66,56),(218,26,57),(218,53,58),(218,25,59),(218,42,60),(218,22,61),(218,64,62),(218,80,63),(218,35,64),(218,4,65),(218,33,66),(218,68,67),(218,67,68),(218,79,69),(218,37,70),(218,43,71),(218,44,72),(218,45,73),(218,46,74),(218,47,75),(218,48,76),(218,49,77),(236,582,0),(236,649,1),(236,507,2),(236,910,3),(236,506,4),(236,128,5),(236,938,6),(236,587,7),(236,941,8),(236,538,9),(236,584,10),(236,945,11),(236,535,12),(236,915,13),(236,892,14),(236,899,15),(236,588,16),(236,968,17),(236,585,18),(236,728,19),(236,132,20),(236,590,21),(236,540,22),(236,13,23),(236,900,24),(236,593,25),(236,73,26),(236,939,27),(236,660,28),(236,905,29),(236,537,30),(236,680,31),(236,647,32),(236,610,33),(236,136,34),(236,667,35),(236,130,36),(236,661,37),(236,891,38),(236,156,39),(236,911,40),(236,799,41),(236,215,42),(236,140,43),(236,947,44),(236,569,45),(236,501,46),(236,897,47),(236,127,48),(236,511,49),(236,589,50),(236,664,51),(236,602,52),(236,912,53),(236,504,54),(236,607,55),(236,134,56),(236,579,57),(236,542,58),(236,914,59),(236,216,60),(236,596,61),(236,637,62),(236,40,63),(236,641,64),(236,608,65),(236,901,66),(236,574,67),(236,580,68),(236,658,69),(236,599,70),(236,889,71),(236,217,72),(236,916,73),(236,218,74),(236,753,75),(236,644,76),(236,635,77),(236,179,78),(236,895,79),(236,648,80),(236,942,81),(236,967,82),(236,581,83),(236,777,84),(236,657,85),(236,58,86),(236,898,87),(236,896,88),(236,601,89),(236,570,90),(236,598,91),(236,212,92),(236,64,93),(236,503,94),(236,557,95),(236,603,96),(236,536,97),(236,563,98),(236,741,99),(236,571,100),(236,135,101),(236,34,102),(236,949,103),(236,909,104),(236,575,105),(236,65,106),(236,124,107),(236,126,108),(236,906,109),(236,969,110),(236,800,111),(236,894,112),(236,768,113),(236,643,114),(236,576,115),(236,773,116),(236,508,117),(236,965,118),(236,125,119),(236,560,120),(236,663,121),(236,214,122),(236,732,123),(236,591,124),(236,573,125),(236,532,126),(236,505,127),(236,512,128),(236,908,129),(236,636,130),(236,652,131),(236,561,132),(236,133,133),(236,653,134),(236,907,135),(236,890,136),(236,770,137),(236,592,138),(236,577,139),(236,662,140),(236,604,141),(236,572,142),(236,946,143),(236,630,144),(236,605,145),(236,902,146),(236,963,147),(236,729,148),(236,642,149),(236,913,150),(236,943,151),(236,646,152),(236,640,153),(236,131,154),(236,651,155),(236,966,156),(236,656,157),(236,948,158),(236,510,159),(236,650,160),(236,893,161),(236,594,162),(236,665,163),(236,609,164),(236,27,165),(236,659,166),(236,655,167),(236,600,168),(236,917,169),(236,595,170),(236,539,171),(236,645,172),(236,666,173),(236,562,174),(236,61,175),(236,940,176),(236,904,177),(236,654,178),(236,509,179),(236,63,180),(236,769,181),(236,586,182),(236,597,183),(236,944,184),(236,129,185),(236,606,186),(236,629,187),(236,578,188),(236,583,189),(236,903,190),(236,738,191),(236,544,192),(236,543,193),(236,772,194),(236,779,195),(236,803,196),(236,805,197),(236,806,198),(236,808,199),(236,514,200),(236,558,201),(236,516,202),(236,515,203),(236,475,204),(236,471,205),(236,473,206),(236,502,207),(236,513,208),(236,517,209),(236,518,210),(236,519,211),(236,520,212),(236,521,213),(236,522,214),(236,523,215),(236,524,216),(236,525,217),(236,526,218),(236,527,219),(236,528,220),(236,529,221),(236,530,222),(236,531,223),(236,533,224),(236,534,225),(236,541,226),(236,545,227),(236,546,228),(236,547,229),(236,548,230),(236,549,231),(236,550,232),(236,551,233),(236,552,234),(236,553,235),(236,554,236),(236,555,237),(236,556,238),(236,559,239),(236,1004,240),(236,146,241),(236,122,242),(236,1003,243),(236,1002,244),(236,1005,245),(236,822,246),(236,1011,247),(236,1010,248),(236,474,249),(236,480,250),(236,477,251),(236,478,252),(236,479,253),(236,476,254),(236,494,255),(236,495,256),(236,484,257),(236,490,258),(236,491,259),(236,492,260),(236,489,261),(236,497,262),(236,488,264),(236,486,265),(236,482,266),(236,493,268),(236,496,269),(236,731,271),(236,733,272),(236,734,273),(236,735,274),(236,1012,275),(236,736,276),(236,737,277),(236,744,278),(236,43,279),(236,971,280),(236,745,281),(236,746,282),(236,747,283),(236,748,284),(236,749,285),(236,44,286),(236,754,287),(236,755,288),(236,45,289),(236,756,290),(236,757,291),(236,763,292),(236,764,293),(236,765,294),(236,766,295),(236,767,296),(236,780,297),(236,46,298),(236,970,299),(236,778,300),(236,776,301),(236,775,302),(236,774,303),(236,47,304),(236,771,305),(236,48,306),(236,49,307),(236,120,308),(236,201,309),(236,202,310),(236,203,311),(236,204,312),(236,205,313),(236,631,314),(236,833,315),(236,826,316),(236,823,317),(236,831,318),(236,813,319),(236,827,320),(236,824,321),(236,814,322),(236,819,323),(236,689,324),(236,933,325),(236,964,326),(236,699,327),(236,79,328),(236,922,329),(236,936,330),(236,925,331),(236,937,332),(236,863,333),(236,864,334),(236,852,335),(236,872,336),(236,873,337),(236,926,338),(236,866,339),(236,923,340),(236,855,341),(236,875,342),(236,876,343),(236,927,344),(236,877,345),(236,878,346),(236,929,347),(236,928,348),(236,924,349),(236,921,350),(236,931,351),(236,932,352),(236,207,353),(236,930,354),(236,920,355),(236,918,356),(236,934,357),(236,935,358),(236,961,359),(236,957,360),(236,952,361),(236,956,362),(236,953,363),(236,954,364),(236,955,365),(236,951,366),(236,859,367),(236,950,368),(236,960,369),(236,959,370),(236,958,371),(236,810,372),(236,206,373),(236,861,374),(236,851,375),(236,867,376),(236,825,377),(236,119,378),(236,809,379),(236,811,380),(236,812,381),(236,568,382),(236,211,383),(236,108,384),(236,228,385),(236,137,386),(236,121,387),(236,123,388),(236,113,389),(236,138,390),(236,139,391),(236,919,392),(236,564,393),(236,567,394),(236,565,395),(236,566,396),(236,962,397),(236,111,398),(236,114,399),(236,869,400),(236,865,401),(236,874,402),(236,853,403),(236,854,404),(236,856,405),(236,857,406),(236,858,407),(236,860,408),(236,862,409),(236,868,410),(236,870,411),(236,871,412),(236,148,413),(236,815,414),(236,816,415),(236,817,416),(236,818,417),(236,820,418),(236,821,419),(236,828,420),(236,829,421),(236,830,422),(236,832,423),(236,834,424),(236,835,425),(236,836,426),(236,117,427),(236,704,428),(236,705,429),(236,706,430),(236,707,431),(236,700,432),(236,972,433),(236,804,434),(236,801,435),(236,802,436),(236,973,437),(236,634,438),(236,979,439),(236,742,440),(236,750,441),(236,758,442),(236,752,443),(236,760,444),(236,751,445),(236,759,446),(236,977,447),(236,762,448),(236,761,449),(236,782,450),(236,783,451),(236,784,452),(236,785,453),(236,7,454),(236,781,455),(236,1001,456),(236,981,457),(236,983,458),(236,982,459),(236,991,460),(236,992,461),(236,93,462),(236,978,463),(236,94,464),(236,1000,465),(236,95,466),(236,96,467),(236,97,468),(236,997,469),(236,989,470),(236,98,471),(236,99,472),(236,990,473),(236,100,474),(236,988,475),(236,985,476),(236,101,477),(236,102,478),(236,103,479),(236,104,480),(236,105,481),(236,996,482),(236,106,483),(236,995,484),(236,987,485),(236,975,486),(236,976,487),(236,980,488),(236,984,489),(236,986,490),(236,999,491),(236,998,492),(236,993,493),(236,994,494),(236,164,495),(236,165,496),(236,166,497),(236,167,498),(236,168,499),(236,169,500),(236,170,501),(236,152,502),(236,153,503),(236,154,504),(236,155,505),(236,157,506),(236,1007,507),(236,1009,508),(236,1008,509),(236,974,510),(236,1019,511),(236,638,512),(236,1024,513),(236,1032,514),(236,698,515),(236,696,516),(236,703,517),(236,701,518),(236,702,519),(236,1037,520),(236,1038,521),(236,697,522),(236,1040,523),(236,713,524),(236,721,525),(329,725,0),(329,726,1),(321,107,0),(321,108,1),(321,109,2),(321,110,3),(321,111,4),(321,112,5),(321,113,6),(321,114,7),(321,115,8),(321,116,9),(321,117,10),(321,118,11),(321,119,12),(321,120,13),(321,121,14),(321,122,15),(321,123,16),(321,124,17),(321,125,18),(321,126,19),(321,127,20),(321,128,21),(321,129,22),(321,130,23),(321,131,24),(321,132,25),(321,133,26),(321,134,27),(321,135,28),(321,136,29),(321,137,30),(321,138,31),(321,139,32),(321,140,33),(321,141,34),(321,142,35),(321,143,36),(321,144,37),(321,145,38),(321,146,39),(321,147,40),(321,148,41),(321,149,42),(321,150,43),(321,151,44),(321,152,45),(321,153,46),(321,154,47),(321,155,48),(321,156,49),(321,157,50),(321,158,51),(321,159,52),(321,160,53),(321,161,54),(321,162,55),(321,163,56),(321,164,57),(321,165,58),(321,166,59),(321,167,60),(321,168,61),(321,169,62),(321,170,63),(321,171,64),(321,172,65),(321,173,66),(321,174,67),(321,175,68),(321,176,69),(321,177,70),(321,178,71),(321,179,72),(321,180,73),(321,181,74),(321,182,75),(321,183,76),(321,184,77),(321,185,78),(321,186,79),(321,187,80),(321,188,81),(321,189,82),(321,190,83),(321,191,84),(321,192,85),(321,193,86),(321,194,87),(321,195,88),(321,196,89),(321,197,90),(321,198,91),(321,199,92),(321,200,93),(321,201,94),(321,202,95),(321,203,96),(321,204,97),(321,205,98),(321,206,99),(321,207,100),(321,208,101),(321,209,102),(321,210,103),(321,211,104),(321,212,105),(321,213,106),(321,214,107),(321,215,108),(321,216,109),(321,217,110),(321,218,111),(321,219,112),(321,220,113),(321,221,114),(321,222,115),(321,223,116),(321,224,117),(321,225,118),(321,226,119),(321,227,120),(321,228,121),(330,1076,0),(330,1077,1),(330,1078,2),(330,1079,3),(330,1080,4),(330,1081,5),(330,1082,6),(330,1083,7),(330,1084,8),(330,1085,9),(330,1086,10),(263,358,0),(263,359,1),(263,285,2),(263,286,3),(263,287,4),(263,288,5),(263,289,6),(263,290,7),(263,291,8),(263,292,9),(263,293,10),(263,294,11),(263,295,12),(263,296,13),(263,297,14),(263,298,15),(263,299,16),(263,300,17),(263,301,18),(263,302,19),(263,303,20),(263,304,21),(263,305,22),(263,306,23),(263,307,24),(263,308,25),(263,309,26),(263,310,27),(263,311,28),(263,312,29),(263,313,30),(263,314,31),(263,315,32),(263,316,33),(263,317,34),(263,318,35),(263,319,36),(263,320,37),(263,321,38),(263,322,39),(263,323,40),(263,324,41),(263,325,42),(263,326,43),(263,327,44),(263,328,45),(263,329,46),(263,330,47),(263,331,48),(263,332,49),(263,342,50),(263,343,51),(263,344,52),(263,345,53),(263,346,54),(263,347,55),(263,348,56),(263,349,57),(263,350,58),(263,351,59),(263,352,60),(263,353,61),(263,360,62),(263,361,63),(263,362,64),(263,363,65),(263,394,66),(263,395,67),(263,396,68),(263,397,69),(263,398,70),(263,399,71),(263,400,72),(263,401,73),(263,402,74),(263,403,75),(263,404,76),(263,405,77),(263,406,78),(263,407,79),(263,408,80),(263,409,81),(263,414,82),(263,415,83),(263,416,84),(263,417,85),(263,418,86),(263,419,87),(263,420,88),(263,421,89),(263,422,90),(263,423,91),(263,424,92),(263,425,93),(263,426,94),(263,427,95),(263,428,96),(263,429,97),(263,430,98),(263,431,99),(263,432,100),(263,433,101),(263,434,102),(263,435,103),(263,436,104),(263,437,105),(263,438,106),(263,439,107),(263,440,108),(263,441,109),(263,442,110),(263,443,111),(263,444,112),(263,445,113),(263,446,114),(263,447,115),(263,448,116),(263,449,117),(263,450,118),(263,451,119),(263,452,120),(263,453,121),(263,454,122),(263,455,123),(263,456,124),(263,457,125),(263,458,126),(263,459,127),(263,460,128),(263,461,129),(263,462,130),(263,463,131),(263,464,132),(263,465,133),(263,467,134),(263,468,135),(263,469,136),(263,369,137),(263,377,138),(263,375,139),(263,388,140),(263,382,141),(263,367,142),(263,366,143),(263,368,144),(263,374,145),(263,386,146),(263,373,147),(263,338,148),(263,337,149),(263,339,150),(263,340,151),(263,341,152),(263,365,153),(263,364,154),(263,273,155),(263,274,156),(263,275,157),(263,879,158),(263,336,159),(263,390,160),(263,391,161),(263,281,162),(263,282,163),(263,335,164),(263,279,165),(263,283,166),(263,280,167),(263,333,168),(263,372,169),(263,393,170),(263,412,171),(263,466,172),(263,277,173),(263,392,174),(263,371,175),(263,410,176),(263,389,177),(263,284,178),(263,411,179),(263,334,180),(263,387,181),(263,278,182),(263,413,183),(263,276,184),(263,357,185),(263,1025,186),(323,880,0),(323,884,1),(323,883,2),(323,882,3),(323,885,4),(323,354,5),(323,355,6),(323,356,7),(323,881,8),(323,886,9),(273,475,0),(273,471,1),(273,473,2),(273,474,3),(273,480,4),(273,477,5),(273,478,6),(273,479,7),(273,476,8),(273,494,9),(273,495,10),(273,484,11),(273,490,12),(273,491,13),(273,492,14),(273,489,15),(273,497,16),(273,488,18),(273,486,19),(273,482,20),(273,493,22),(273,496,23),(273,472,25),(273,485,26),(238,536,0),(238,563,1),(238,582,2),(238,741,3),(238,571,4),(238,135,5),(238,328,6),(238,649,7),(238,34,8),(238,575,9),(238,65,10),(238,128,11),(238,332,12),(238,587,13),(238,310,14),(238,538,15),(238,584,16),(238,315,17),(238,800,18),(238,768,19),(238,643,20),(238,535,21),(238,773,22),(238,576,23),(238,324,24),(238,329,25),(238,320,26),(238,588,27),(238,585,28),(238,728,29),(238,590,30),(238,540,31),(238,13,32),(238,318,33),(238,560,34),(238,663,35),(238,214,36),(238,593,37),(238,732,38),(238,591,39),(238,573,40),(238,73,41),(238,660,42),(238,316,43),(238,537,44),(238,647,45),(238,532,46),(238,512,47),(238,636,48),(238,321,49),(238,610,50),(238,652,51),(238,136,52),(238,667,53),(238,322,54),(238,130,55),(238,561,56),(238,653,57),(238,661,58),(238,592,59),(238,577,60),(238,323,61),(238,662,62),(238,799,63),(238,604,64),(238,215,65),(238,572,66),(238,140,67),(238,569,68),(238,630,69),(238,326,70),(238,501,71),(238,605,72),(238,330,73),(238,127,74),(238,319,75),(238,729,76),(238,589,77),(238,642,78),(238,664,79),(238,602,80),(238,311,81),(238,325,82),(238,607,83),(238,134,84),(238,579,85),(238,542,86),(238,646,87),(238,640,88),(238,216,89),(238,131,90),(238,651,91),(238,596,92),(238,637,93),(238,641,94),(238,40,95),(238,656,96),(238,608,97),(238,309,98),(238,580,99),(238,574,100),(238,599,101),(238,650,102),(238,658,103),(238,594,104),(238,665,105),(238,609,106),(238,217,107),(238,27,108),(238,659,109),(238,655,110),(238,218,111),(238,600,112),(238,595,113),(238,644,114),(238,539,115),(238,314,116),(238,645,117),(238,666,118),(238,327,119),(238,562,120),(238,635,121),(238,61,122),(238,179,123),(238,317,124),(238,648,125),(238,581,126),(238,777,127),(238,58,128),(238,331,129),(238,654,130),(238,769,131),(238,63,132),(238,586,133),(238,312,134),(238,597,135),(238,601,136),(238,598,137),(238,570,138),(238,313,139),(238,212,140),(238,64,141),(238,129,142),(238,606,143),(238,629,144),(238,578,145),(238,583,146),(238,557,147),(238,308,148),(238,603,149),(238,738,150),(238,369,151),(238,358,152),(238,359,153),(238,779,154),(238,803,155),(238,805,156),(238,806,157),(238,808,158),(238,514,159),(238,558,160),(238,516,161),(238,515,162),(238,475,163),(238,471,164),(238,473,165),(238,502,166),(238,513,167),(238,517,168),(238,518,169),(238,519,170),(238,520,171),(238,521,172),(238,522,173),(238,523,174),(238,524,175),(238,525,176),(238,526,177),(238,527,178),(238,528,179),(238,529,180),(238,530,181),(238,531,182),(238,533,183),(238,534,184),(238,541,185),(238,545,186),(238,546,187),(238,547,188),(238,548,189),(238,549,190),(238,551,191),(238,552,192),(238,553,193),(238,554,194),(238,555,195),(238,556,196),(238,559,197),(238,1004,198),(238,146,199),(238,124,200),(238,122,201),(238,125,202),(238,126,203),(238,132,204),(238,133,205),(238,1003,206),(238,1005,207),(238,1011,208),(238,1010,209),(238,474,210),(238,480,211),(238,477,212),(238,478,213),(238,479,214),(238,476,215),(238,494,216),(238,495,217),(238,484,218),(238,490,219),(238,491,220),(238,492,221),(238,497,222),(238,488,224),(238,486,225),(238,482,226),(238,496,228),(238,731,230),(238,342,231),(238,343,232),(238,344,233),(238,345,234),(238,346,235),(238,347,236),(238,348,237),(238,349,238),(238,350,239),(238,351,240),(238,352,241),(238,353,242),(238,360,243),(238,361,244),(238,362,245),(238,414,246),(238,415,247),(238,416,248),(238,417,249),(238,418,250),(238,419,251),(238,420,252),(238,421,253),(238,422,254),(238,423,255),(238,424,256),(238,425,257),(238,426,258),(238,427,259),(238,428,260),(238,429,261),(238,430,262),(238,431,263),(238,432,264),(238,433,265),(238,434,266),(238,435,267),(238,436,268),(238,437,269),(238,438,270),(238,439,271),(238,440,272),(238,441,273),(238,442,274),(238,443,275),(238,444,276),(238,445,277),(238,446,278),(238,447,279),(238,448,280),(238,449,281),(238,450,282),(238,451,283),(238,452,284),(238,453,285),(238,454,286),(238,455,287),(238,456,288),(238,457,289),(238,458,290),(238,459,291),(238,460,292),(238,461,293),(238,462,294),(238,463,295),(238,464,296),(238,465,297),(238,467,298),(238,468,299),(238,469,300),(238,733,301),(238,734,302),(238,735,303),(238,736,304),(238,737,305),(238,43,306),(238,44,307),(238,45,308),(238,763,309),(238,764,310),(238,765,311),(238,780,312),(238,46,313),(238,778,314),(238,776,315),(238,775,316),(238,774,317),(238,47,318),(238,771,319),(238,48,320),(238,49,321),(238,120,322),(238,201,323),(238,202,324),(238,203,325),(238,204,326),(238,205,327),(238,631,328),(238,377,329),(238,833,330),(238,823,331),(238,831,332),(238,813,333),(238,827,334),(238,824,335),(238,814,336),(238,819,337),(238,689,338),(238,79,339),(238,375,340),(238,863,341),(238,388,342),(238,382,343),(238,864,344),(238,367,345),(238,366,346),(238,368,347),(238,852,348),(238,872,349),(238,873,350),(238,855,351),(238,875,352),(238,877,353),(238,374,354),(238,386,355),(238,373,356),(238,207,357),(238,859,358),(238,810,359),(238,206,360),(238,851,361),(238,867,362),(238,825,363),(238,119,364),(238,809,365),(238,811,366),(238,812,367),(238,568,368),(238,121,369),(238,113,370),(238,273,371),(238,274,372),(238,275,373),(238,138,374),(238,564,375),(238,567,376),(238,565,377),(238,566,378),(238,111,379),(238,869,380),(238,865,381),(238,874,382),(238,853,383),(238,854,384),(238,856,385),(238,857,386),(238,858,387),(238,860,388),(238,862,389),(238,868,390),(238,870,391),(238,871,392),(238,336,393),(238,390,394),(238,148,395),(238,815,396),(238,816,397),(238,818,398),(238,821,399),(238,829,400),(238,830,401),(238,832,402),(238,834,403),(238,835,404),(238,836,405),(238,117,406),(238,972,407),(238,804,408),(238,801,409),(238,802,410),(238,973,411),(238,634,412),(238,979,413),(238,742,414),(238,977,415),(238,782,416),(238,783,417),(238,784,418),(238,785,419),(238,7,420),(238,781,421),(238,991,422),(238,391,423),(238,992,424),(238,281,425),(238,282,426),(238,335,427),(238,279,428),(238,283,429),(238,280,430),(238,333,431),(238,393,432),(238,412,433),(238,466,434),(238,277,435),(238,392,436),(238,410,437),(238,389,438),(238,284,439),(238,411,440),(238,334,441),(238,387,442),(238,93,443),(238,978,444),(238,278,445),(238,413,446),(238,1000,447),(238,96,448),(238,989,449),(238,990,450),(238,996,451),(238,995,452),(238,987,453),(238,975,454),(238,976,455),(238,984,456),(238,998,457),(238,993,458),(238,994,459),(238,168,460),(238,1007,461),(238,1009,462),(238,1008,463),(238,974,464),(238,276,465),(238,363,466),(238,338,467),(238,340,468),(238,337,469),(238,341,470),(238,365,471),(238,114,472),(238,878,473),(238,1019,474),(238,982,475),(238,985,476),(238,988,477),(238,1012,478),(238,983,479),(238,986,480),(238,1002,481),(238,876,482),(238,866,483),(238,861,484),(238,638,485),(238,94,486),(238,95,487),(238,97,488),(238,98,489),(238,103,490),(238,102,491),(238,101,492),(238,100,493),(238,105,494),(238,106,495),(238,104,496),(238,766,497),(238,657,498),(238,170,499),(238,166,500),(238,1025,501),(238,1026,502),(238,1030,503),(238,970,504),(238,1032,505),(238,997,506),(238,999,507),(238,971,508),(238,155,509),(238,1028,510),(238,157,511),(238,156,512),(238,154,513),(238,165,514),(238,164,515),(238,169,516),(238,153,517),(238,167,518),(238,1031,519),(238,149,520),(238,1043,521),(238,550,522),(238,698,523),(238,700,524),(238,696,525),(238,703,526),(238,701,527),(238,702,528),(238,704,529),(238,705,530),(238,706,531),(238,707,532),(238,697,533),(238,713,534),(238,721,535),(238,722,536),(238,711,537),(238,719,538),(238,1024,539),(238,123,540),(238,1029,541),(238,1038,542),(238,1040,543),(238,708,544),(238,1054,545),(238,1037,546),(238,139,547),(238,1060,548),(238,1052,549),(238,99,550),(238,1055,551),(238,152,552),(238,1044,553),(238,1053,554),(238,1056,555),(238,1058,556),(238,228,557),(238,137,558),(238,1047,559),(238,1062,560),(238,820,561),(238,1015,562),(238,612,563),(238,498,564),(238,628,565),(238,625,566),(238,470,567),(238,624,568),(238,500,569),(238,611,570),(238,1014,571),(238,626,572),(238,499,573),(238,613,574),(238,618,575),(238,623,576),(238,614,577),(238,615,578),(238,619,579),(238,621,580),(238,622,581),(238,807,582),(238,617,583),(238,616,584),(238,620,585),(238,682,586),(238,794,587),(238,840,588),(238,790,589),(238,679,590),(238,693,591),(238,789,592),(238,795,593),(238,839,594),(238,845,595),(238,683,596),(238,716,597),(238,709,598),(238,677,599),(238,787,600),(238,727,601),(238,850,602),(238,797,603),(238,788,604),(238,686,605),(325,880,0),(325,884,1),(325,883,2),(325,882,3),(325,885,4),(325,354,5),(325,355,6),(325,356,7),(325,881,8),(325,886,9),(325,725,10),(325,726,11),(223,572,0),(223,527,1),(223,531,2),(223,552,3),(223,563,4),(223,569,5),(223,582,6),(223,501,7),(223,571,8),(223,605,9),(223,575,10),(223,555,11),(223,521,12),(223,589,13),(223,545,14),(223,534,15),(223,587,16),(223,546,17),(223,602,18),(223,584,19),(223,517,20),(223,607,21),(223,579,22),(223,502,23),(223,542,24),(223,576,25),(223,596,26),(223,553,27),(223,588,28),(223,608,29),(223,541,30),(223,515,31),(223,580,32),(223,574,33),(223,551,34),(223,599,35),(223,526,36),(223,548,37),(223,550,38),(223,525,39),(223,594,40),(223,585,41),(223,609,42),(223,519,43),(223,590,44),(223,556,45),(223,518,46),(223,560,47),(223,600,48),(223,595,49),(223,529,50),(223,593,51),(223,523,52),(223,530,53),(223,562,54),(223,591,55),(223,573,56),(223,528,57),(223,522,58),(223,581,59),(223,520,60),(223,532,61),(223,516,62),(223,524,63),(223,513,64),(223,514,65),(223,559,66),(223,586,67),(223,610,68),(223,597,69),(223,601,70),(223,598,71),(223,570,72),(223,561,73),(223,533,74),(223,606,75),(223,554,76),(223,578,77),(223,592,78),(223,583,79),(223,577,80),(223,547,81),(223,549,82),(223,558,83),(223,557,84),(223,604,85),(223,603,86),(223,503,87),(223,504,88),(223,505,89),(223,506,90),(223,507,91),(223,508,92),(223,509,93),(223,510,94),(223,511,95),(223,512,96),(223,536,97),(223,537,98),(223,538,99),(223,539,100),(223,535,101),(223,540,102),(223,568,103),(223,564,104),(223,567,105),(223,565,106),(223,566,107),(223,543,108),(223,544,109),(237,582,0),(237,649,1),(237,507,2),(237,506,3),(237,128,4),(237,332,5),(237,587,6),(237,938,7),(237,310,8),(237,538,9),(237,941,10),(237,584,11),(237,315,12),(237,945,13),(237,915,14),(237,535,15),(237,324,16),(237,329,17),(237,320,18),(237,588,19),(237,585,20),(237,590,21),(237,132,22),(237,540,23),(237,13,24),(237,318,25),(237,593,26),(237,73,27),(237,939,28),(237,660,29),(237,316,30),(237,537,31),(237,647,32),(237,321,33),(237,610,34),(237,136,35),(237,667,36),(237,322,37),(237,661,38),(237,215,39),(237,140,40),(237,947,41),(237,569,42),(237,501,43),(237,330,44),(237,511,45),(237,589,46),(237,664,47),(237,602,48),(237,311,49),(237,504,50),(237,607,51),(237,134,52),(237,579,53),(237,914,54),(237,542,55),(237,216,56),(237,596,57),(237,637,58),(237,40,59),(237,641,60),(237,608,61),(237,574,62),(237,580,63),(237,599,64),(237,658,65),(237,217,66),(237,916,67),(237,218,68),(237,644,69),(237,314,70),(237,179,71),(237,635,72),(237,648,73),(237,942,74),(237,581,75),(237,58,76),(237,601,77),(237,598,78),(237,570,79),(237,212,80),(237,64,81),(237,503,82),(237,557,83),(237,603,84),(237,536,85),(237,563,86),(237,571,87),(237,328,88),(237,135,89),(237,949,90),(237,34,91),(237,575,92),(237,65,93),(237,124,94),(237,126,95),(237,643,96),(237,576,97),(237,508,98),(237,965,99),(237,125,100),(237,560,101),(237,663,102),(237,214,103),(237,591,104),(237,573,105),(237,532,106),(237,505,107),(237,512,108),(237,636,109),(237,652,110),(237,133,111),(237,561,112),(237,653,113),(237,592,114),(237,577,115),(237,323,116),(237,662,117),(237,604,118),(237,572,119),(237,946,120),(237,630,121),(237,326,122),(237,605,123),(237,319,124),(237,963,125),(237,642,126),(237,325,127),(237,943,128),(237,646,129),(237,640,130),(237,651,131),(237,656,132),(237,948,133),(237,309,134),(237,510,135),(237,650,136),(237,594,137),(237,665,138),(237,609,139),(237,27,140),(237,659,141),(237,655,142),(237,600,143),(237,917,144),(237,595,145),(237,539,146),(237,645,147),(237,666,148),(237,327,149),(237,61,150),(237,562,151),(237,317,152),(237,940,153),(237,331,154),(237,654,155),(237,509,156),(237,63,157),(237,586,158),(237,312,159),(237,597,160),(237,944,161),(237,313,162),(237,129,163),(237,606,164),(237,629,165),(237,578,166),(237,583,167),(237,308,168),(237,358,169),(237,359,170),(237,514,171),(237,558,172),(237,516,173),(237,515,174),(237,471,175),(237,473,176),(237,475,177),(237,502,178),(237,513,179),(237,517,180),(237,518,181),(237,519,182),(237,520,183),(237,521,184),(237,522,185),(237,523,186),(237,524,187),(237,525,188),(237,526,189),(237,527,190),(237,528,191),(237,529,192),(237,530,193),(237,531,194),(237,533,195),(237,534,196),(237,541,197),(237,545,198),(237,546,199),(237,547,200),(237,548,201),(237,549,202),(237,551,203),(237,552,204),(237,553,205),(237,554,206),(237,555,207),(237,556,208),(237,559,209),(237,146,210),(237,122,211),(237,130,212),(237,131,213),(237,127,214),(237,474,215),(237,480,216),(237,477,217),(237,478,218),(237,479,219),(237,476,220),(237,494,221),(237,495,222),(237,484,223),(237,490,224),(237,491,225),(237,492,226),(237,497,227),(237,488,229),(237,486,230),(237,482,231),(237,496,233),(237,343,235),(237,344,236),(237,345,237),(237,346,238),(237,347,239),(237,348,240),(237,349,241),(237,350,242),(237,351,243),(237,352,244),(237,353,245),(237,360,246),(237,361,247),(237,362,248),(237,394,249),(237,395,250),(237,396,251),(237,397,252),(237,398,253),(237,399,254),(237,400,255),(237,401,256),(237,402,257),(237,403,258),(237,404,259),(237,405,260),(237,406,261),(237,407,262),(237,408,263),(237,409,264),(237,414,265),(237,415,266),(237,416,267),(237,417,268),(237,418,269),(237,419,270),(237,420,271),(237,421,272),(237,422,273),(237,423,274),(237,424,275),(237,425,276),(237,426,277),(237,427,278),(237,428,279),(237,429,280),(237,430,281),(237,431,282),(237,432,283),(237,433,284),(237,434,285),(237,435,286),(237,436,287),(237,437,288),(237,438,289),(237,439,290),(237,440,291),(237,441,292),(237,442,293),(237,443,294),(237,444,295),(237,445,296),(237,446,297),(237,447,298),(237,448,299),(237,449,300),(237,450,301),(237,451,302),(237,452,303),(237,453,304),(237,454,305),(237,455,306),(237,456,307),(237,457,308),(237,458,309),(237,459,310),(237,460,311),(237,461,312),(237,462,313),(237,463,314),(237,464,315),(237,465,316),(237,467,317),(237,468,318),(237,469,319),(237,43,320),(237,44,321),(237,45,322),(237,46,323),(237,47,324),(237,48,325),(237,49,326),(237,120,327),(237,201,328),(237,202,329),(237,203,330),(237,204,331),(237,205,332),(237,631,333),(237,933,334),(237,79,335),(237,936,336),(237,925,337),(237,375,338),(237,863,339),(237,864,340),(237,852,341),(237,872,342),(237,873,343),(237,926,344),(237,923,345),(237,855,346),(237,875,347),(237,927,348),(237,877,349),(237,929,350),(237,928,351),(237,924,352),(237,921,353),(237,931,354),(237,932,355),(237,207,356),(237,930,357),(237,920,358),(237,918,359),(237,961,360),(237,957,361),(237,952,362),(237,956,363),(237,954,364),(237,859,365),(237,960,366),(237,959,367),(237,206,368),(237,851,369),(237,867,370),(237,119,371),(237,568,372),(237,121,373),(237,113,374),(237,138,375),(237,564,376),(237,567,377),(237,565,378),(237,566,379),(237,111,380),(237,869,381),(237,865,382),(237,874,383),(237,336,384),(237,390,385),(237,148,386),(237,117,387),(237,634,388),(237,7,389),(237,391,390),(237,281,391),(237,282,392),(237,335,393),(237,279,394),(237,283,395),(237,280,396),(237,333,397),(237,393,398),(237,412,399),(237,466,400),(237,277,401),(237,392,402),(237,410,403),(237,389,404),(237,284,405),(237,411,406),(237,334,407),(237,387,408),(237,278,409),(237,413,410),(237,168,411),(237,363,412),(237,338,413),(237,340,414),(237,337,415),(237,341,416),(237,365,417),(237,114,418),(237,889,419),(237,893,420),(237,894,421),(237,895,422),(237,898,423),(237,899,424),(237,900,425),(237,901,426),(237,905,427),(237,906,428),(237,910,429),(237,911,430),(237,912,431),(237,913,432),(237,638,433),(237,657,434),(237,170,435),(237,892,436),(237,896,437),(237,897,438),(237,902,439),(237,903,440),(237,904,441),(237,907,442),(237,166,443),(237,908,444),(237,909,445),(237,922,446),(237,966,447),(237,967,448),(237,968,449),(237,969,450),(237,891,451),(237,964,452),(237,935,453),(237,934,454),(237,937,455),(237,953,456),(237,955,457),(237,1032,458),(237,951,459),(237,962,460),(237,919,461),(237,958,462),(237,155,463),(237,157,464),(237,156,465),(237,154,466),(237,165,467),(237,164,468),(237,169,469),(237,153,470),(237,167,471),(237,950,472),(237,890,473),(237,149,474),(237,550,475),(237,1024,476),(237,123,477),(237,139,478),(237,1052,479),(237,152,480),(237,1063,481),(237,1053,482),(237,1056,483),(237,1058,484),(237,137,485),(237,1015,486),(237,612,487),(237,498,488),(237,1013,489),(237,470,490),(237,624,491),(237,500,492),(237,627,493),(237,611,494),(237,499,495),(237,483,496),(237,472,497),(237,485,498),(237,35,499),(237,30,500),(237,67,501),(237,80,502),(237,19,503),(237,57,504),(237,6,505),(237,66,506),(237,12,507),(237,5,508),(237,81,509),(237,70,510),(237,17,511),(237,77,512),(237,36,513),(237,18,514),(324,880,0),(324,884,1),(324,883,2),(324,882,3),(324,885,4),(324,355,5),(324,881,6),(227,684,0),(227,796,1),(227,689,2),(227,702,3),(227,775,4),(227,741,5),(227,815,6),(227,772,7),(227,838,8),(227,692,9),(227,694,10),(227,816,11),(227,710,12),(227,831,13),(227,765,14),(227,791,15),(227,824,16),(227,737,17),(227,768,18),(227,754,19),(227,850,20),(227,773,21),(227,819,22),(227,836,23),(227,774,24),(227,846,25),(227,813,26),(227,744,27),(227,685,28),(227,730,29),(227,746,30),(227,835,31),(227,755,32),(227,828,33),(227,727,34),(227,728,35),(227,757,36),(227,832,37),(227,718,38),(227,789,39),(227,687,40),(227,814,41),(227,686,42),(227,732,43),(227,834,44),(227,763,45),(227,715,46),(227,734,47),(227,690,48),(227,697,49),(227,723,50),(227,794,51),(227,680,52),(227,721,53),(227,733,54),(227,683,55),(227,749,56),(227,822,57),(227,756,58),(227,780,59),(227,779,60),(227,704,61),(227,823,62),(227,795,63),(227,720,64),(227,714,65),(227,731,66),(227,837,67),(227,736,68),(227,770,69),(227,849,70),(227,842,71),(227,821,72),(227,719,73),(227,681,74),(227,682,75),(227,678,76),(227,787,77),(227,797,78),(227,793,79),(227,729,80),(227,695,81),(227,833,82),(227,844,83),(227,735,84),(227,712,85),(227,776,86),(227,792,87),(227,679,88),(227,843,89),(227,820,90),(227,764,91),(227,747,92),(227,708,93),(227,827,94),(227,840,95),(227,696,96),(227,743,97),(227,748,98),(227,716,99),(227,845,100),(227,841,101),(227,771,102),(227,724,103),(227,753,104),(227,701,105),(227,848,106),(227,705,107),(227,688,108),(227,826,109),(227,839,110),(227,722,111),(227,717,112),(227,706,113),(227,830,114),(227,788,115),(227,709,116),(227,739,117),(227,777,118),(227,707,119),(227,766,120),(227,847,121),(227,745,122),(227,786,123),(227,700,124),(227,713,125),(227,698,126),(227,769,127),(227,740,128),(227,817,129),(227,829,130),(227,798,131),(227,677,132),(227,693,133),(227,778,134),(227,818,135),(227,767,136),(227,703,137),(227,711,138),(227,790,139),(227,691,140),(227,699,141),(227,738,142),(227,810,143),(227,825,144),(227,809,145),(227,811,146),(227,812,147),(227,742,148),(227,750,149),(227,758,150),(227,752,151),(227,760,152),(227,751,153),(227,759,154),(227,762,155),(227,761,156),(227,782,157),(227,783,158),(227,784,159),(227,785,160),(227,781,161),(328,725,0),(328,726,1),(224,616,0),(224,617,1),(224,615,2),(224,622,3),(224,806,4),(224,619,5),(224,623,6),(224,803,7),(224,613,8),(224,807,9),(224,804,10),(224,805,11),(224,614,12),(224,800,13),(224,808,14),(224,620,15),(224,618,16),(224,799,17),(224,621,18),(224,801,19),(224,802,20),(222,626,0),(222,1015,1),(222,498,2),(222,470,3),(222,1014,4),(222,612,5),(222,624,6),(222,625,7),(222,628,8),(222,500,9),(222,611,10),(222,1013,11),(222,499,12),(222,627,13),(297,4,0),(297,5,1),(297,6,2),(297,8,3),(297,9,4),(297,10,5),(297,11,6),(297,12,7),(297,13,8),(297,14,9),(297,15,10),(297,16,11),(297,18,12),(297,19,13),(297,20,14),(297,21,15),(297,22,16),(297,23,17),(297,24,18),(297,25,19),(297,26,20),(297,27,21),(297,28,22),(297,29,23),(297,30,24),(297,31,25),(297,32,26),(297,33,27),(297,34,28),(297,35,29),(297,36,30),(297,37,31),(297,38,32),(297,39,33),(297,40,34),(297,41,35),(297,42,36),(297,44,37),(297,47,38),(297,48,39),(297,49,40),(297,50,41),(297,51,42),(297,52,43),(297,53,44),(297,54,45),(297,55,46),(297,56,47),(297,57,48),(297,58,49),(297,59,50),(297,60,51),(297,61,52),(297,62,53),(297,63,54),(297,64,55),(297,65,56),(297,66,57),(297,67,58),(297,68,59),(297,69,60),(297,70,61),(297,71,62),(297,72,63),(297,73,64),(297,74,65),(297,75,66),(297,76,67),(297,77,68),(297,78,69),(297,79,70),(297,80,71),(297,81,72),(297,273,73),(297,274,74),(297,275,75),(297,613,76),(297,614,77),(297,615,78),(297,616,79),(297,617,80),(297,618,81),(297,619,82),(297,620,83),(297,621,84),(297,622,85),(297,623,86),(297,628,87),(297,1014,88),(297,138,89),(297,7,90),(297,276,91),(297,1024,92),(300,4,0),(300,5,1),(300,6,2),(300,8,3),(300,9,4),(300,10,5),(300,11,6),(300,12,7),(300,13,8),(300,14,9),(300,15,10),(300,16,11),(300,18,12),(300,19,13),(300,20,14),(300,21,15),(300,22,16),(300,23,17),(300,24,18),(300,25,19),(300,26,20),(300,27,21),(300,28,22),(300,29,23),(300,30,24),(300,31,25),(300,32,26),(300,33,27),(300,34,28),(300,35,29),(300,36,30),(300,37,31),(300,38,32),(300,39,33),(300,40,34),(300,41,35),(300,42,36),(300,44,37),(300,47,38),(300,48,39),(300,49,40),(300,50,41),(300,51,42),(300,52,43),(300,53,44),(300,54,45),(300,55,46),(300,56,47),(300,57,48),(300,58,49),(300,59,50),(300,60,51),(300,61,52),(300,62,53),(300,63,54),(300,64,55),(300,65,56),(300,66,57),(300,67,58),(300,68,59),(300,69,60),(300,70,61),(300,71,62),(300,72,63),(300,73,64),(300,74,65),(300,75,66),(300,76,67),(300,77,68),(300,78,69),(300,79,70),(300,80,71),(300,81,72),(300,627,73),(300,1013,74),(300,138,75),(300,7,76),(300,1024,77),(300,139,78),(300,1053,79),(296,4,0),(296,5,1),(296,6,2),(296,8,3),(296,9,4),(296,10,5),(296,11,6),(296,12,7),(296,13,8),(296,14,9),(296,15,10),(296,16,11),(296,17,12),(296,18,13),(296,19,14),(296,20,15),(296,21,16),(296,22,17),(296,23,18),(296,24,19),(296,25,20),(296,26,21),(296,27,22),(296,28,23),(296,29,24),(296,30,25),(296,31,26),(296,32,27),(296,33,28),(296,34,29),(296,35,30),(296,36,31),(296,37,32),(296,38,33),(296,39,34),(296,40,35),(296,41,36),(296,42,37),(296,44,38),(296,47,39),(296,48,40),(296,49,41),(296,50,42),(296,51,43),(296,52,44),(296,53,45),(296,54,46),(296,55,47),(296,56,48),(296,57,49),(296,58,50),(296,59,51),(296,60,52),(296,61,53),(296,62,54),(296,63,55),(296,64,56),(296,65,57),(296,66,58),(296,67,59),(296,68,60),(296,69,61),(296,70,62),(296,71,63),(296,72,64),(296,73,65),(296,74,66),(296,75,67),(296,76,68),(296,77,69),(296,78,70),(296,79,71),(296,80,72),(296,81,73),(296,107,74),(296,109,75),(296,110,76),(296,111,77),(296,112,78),(296,115,79),(296,116,80),(296,118,81),(296,119,82),(296,141,83),(296,142,84),(296,143,85),(296,144,86),(296,145,87),(296,146,88),(296,147,89),(296,150,90),(296,151,91),(296,158,92),(296,159,93),(296,160,94),(296,161,95),(296,162,96),(296,163,97),(296,171,98),(296,172,99),(296,173,100),(296,174,101),(296,175,102),(296,176,103),(296,177,104),(296,178,105),(296,179,106),(296,180,107),(296,181,108),(296,182,109),(296,183,110),(296,184,111),(296,185,112),(296,186,113),(296,187,114),(296,188,115),(296,189,116),(296,190,117),(296,191,118),(296,192,119),(296,193,120),(296,194,121),(296,195,122),(296,196,123),(296,197,124),(296,198,125),(296,199,126),(296,200,127),(296,206,128),(296,207,129),(296,208,130),(296,209,131),(296,210,132),(296,212,133),(296,213,134),(296,214,135),(296,215,136),(296,216,137),(296,217,138),(296,218,139),(296,219,140),(296,220,141),(296,221,142),(296,222,143),(296,223,144),(296,224,145),(296,225,146),(296,226,147),(296,249,148),(296,250,149),(296,251,150),(296,252,151),(296,253,152),(296,254,153),(296,255,154),(296,256,155),(296,257,156),(296,258,157),(296,470,158),(296,498,159),(296,499,160),(296,500,161),(296,501,162),(296,502,163),(296,513,164),(296,516,165),(296,517,166),(296,518,167),(296,519,168),(296,520,169),(296,521,170),(296,522,171),(296,523,172),(296,524,173),(296,525,174),(296,526,175),(296,527,176),(296,528,177),(296,529,178),(296,530,179),(296,531,180),(296,533,181),(296,534,182),(296,541,183),(296,542,184),(296,547,185),(296,548,186),(296,549,187),(296,551,188),(296,552,189),(296,553,190),(296,554,191),(296,555,192),(296,556,193),(296,557,194),(296,559,195),(296,560,196),(296,561,197),(296,562,198),(296,563,199),(296,564,200),(296,565,201),(296,566,202),(296,567,203),(296,568,204),(296,569,205),(296,570,206),(296,571,207),(296,572,208),(296,573,209),(296,574,210),(296,575,211),(296,576,212),(296,577,213),(296,578,214),(296,579,215),(296,580,216),(296,581,217),(296,583,218),(296,584,219),(296,585,220),(296,586,221),(296,588,222),(296,589,223),(296,590,224),(296,591,225),(296,592,226),(296,593,227),(296,594,228),(296,595,229),(296,596,230),(296,597,231),(296,598,232),(296,599,233),(296,600,234),(296,601,235),(296,602,236),(296,604,237),(296,605,238),(296,606,239),(296,607,240),(296,608,241),(296,609,242),(296,610,243),(296,611,244),(296,612,245),(296,613,246),(296,614,247),(296,615,248),(296,616,249),(296,617,250),(296,618,251),(296,619,252),(296,620,253),(296,621,254),(296,622,255),(296,623,256),(296,624,257),(296,625,258),(296,626,259),(296,630,260),(296,631,261),(296,632,262),(296,633,263),(296,635,264),(296,636,265),(296,637,266),(296,639,267),(296,640,268),(296,641,269),(296,643,270),(296,644,271),(296,645,272),(296,647,273),(296,648,274),(296,649,275),(296,650,276),(296,651,277),(296,652,278),(296,654,279),(296,655,280),(296,656,281),(296,658,282),(296,660,283),(296,661,284),(296,662,285),(296,663,286),(296,664,287),(296,665,288),(296,666,289),(296,851,290),(296,853,291),(296,854,292),(296,855,293),(296,856,294),(296,857,295),(296,858,296),(296,859,297),(296,860,298),(296,862,299),(296,863,300),(296,865,301),(296,867,302),(296,868,303),(296,869,304),(296,870,305),(296,871,306),(296,872,307),(296,873,308),(296,874,309),(296,875,310),(296,877,311),(296,1003,312),(296,1004,313),(296,1005,314),(296,1015,315),(296,532,316),(296,148,317),(296,582,318),(296,515,319),(296,558,320),(296,545,321),(296,546,322),(296,122,323),(296,117,324),(296,124,325),(296,125,326),(296,126,327),(296,127,328),(296,128,329),(296,130,330),(296,131,331),(296,132,332),(296,133,333),(296,134,334),(296,667,335),(296,135,336),(296,136,337),(296,138,338),(296,140,339),(296,129,340),(296,603,341),(296,634,342),(296,646,343),(296,642,344),(296,1010,345),(296,7,346),(296,659,347),(296,653,348),(296,587,349),(296,113,350),(296,629,351),(296,514,352),(296,121,353),(296,201,354),(296,202,355),(296,203,356),(296,204,357),(296,205,358),(296,120,359),(296,168,360),(296,1011,361),(296,972,362),(296,1007,363),(296,1009,364),(296,1008,365),(296,973,366),(296,974,367),(296,975,368),(296,976,369),(296,977,370),(296,979,371),(296,978,372),(296,984,373),(296,987,374),(296,989,375),(296,990,376),(296,991,377),(296,992,378),(296,993,379),(296,994,380),(296,998,381),(296,1000,382),(296,995,383),(296,996,384),(296,114,385),(296,982,386),(296,985,387),(296,988,388),(296,1012,389),(296,983,390),(296,986,391),(296,1002,392),(296,866,393),(296,861,394),(296,638,395),(296,657,396),(296,170,397),(296,166,398),(296,970,399),(296,997,400),(296,999,401),(296,971,402),(296,155,403),(296,157,404),(296,156,405),(296,154,406),(296,165,407),(296,164,408),(296,169,409),(296,153,410),(296,167,411),(296,149,412),(296,550,413),(296,1024,414),(296,123,415),(296,139,416),(296,152,417),(296,1053,418),(296,1056,419),(296,1058,420),(296,228,421),(296,137,422),(296,1057,423),(296,1001,424),(296,543,425),(299,4,0),(299,5,1),(299,6,2),(299,8,3),(299,9,4),(299,10,5),(299,11,6),(299,12,7),(299,13,8),(299,14,9),(299,15,10),(299,16,11),(299,17,12),(299,18,13),(299,19,14),(299,20,15),(299,21,16),(299,22,17),(299,23,18),(299,24,19),(299,25,20),(299,26,21),(299,27,22),(299,28,23),(299,29,24),(299,30,25),(299,31,26),(299,32,27),(299,33,28),(299,34,29),(299,35,30),(299,36,31),(299,37,32),(299,38,33),(299,39,34),(299,40,35),(299,41,36),(299,42,37),(299,44,38),(299,47,39),(299,48,40),(299,49,41),(299,50,42),(299,51,43),(299,52,44),(299,53,45),(299,54,46),(299,55,47),(299,56,48),(299,57,49),(299,58,50),(299,59,51),(299,60,52),(299,61,53),(299,62,54),(299,63,55),(299,64,56),(299,65,57),(299,66,58),(299,67,59),(299,68,60),(299,69,61),(299,70,62),(299,71,63),(299,72,64),(299,73,65),(299,74,66),(299,75,67),(299,76,68),(299,77,69),(299,78,70),(299,79,71),(299,80,72),(299,81,73),(299,107,74),(299,109,75),(299,110,76),(299,111,77),(299,112,78),(299,115,79),(299,116,80),(299,118,81),(299,119,82),(299,141,83),(299,142,84),(299,143,85),(299,144,86),(299,145,87),(299,146,88),(299,147,89),(299,150,90),(299,151,91),(299,158,92),(299,159,93),(299,160,94),(299,161,95),(299,162,96),(299,163,97),(299,171,98),(299,172,99),(299,173,100),(299,174,101),(299,175,102),(299,176,103),(299,177,104),(299,178,105),(299,179,106),(299,180,107),(299,181,108),(299,182,109),(299,183,110),(299,184,111),(299,185,112),(299,186,113),(299,187,114),(299,188,115),(299,189,116),(299,190,117),(299,191,118),(299,192,119),(299,193,120),(299,194,121),(299,195,122),(299,196,123),(299,197,124),(299,198,125),(299,199,126),(299,200,127),(299,206,128),(299,207,129),(299,208,130),(299,209,131),(299,210,132),(299,212,133),(299,213,134),(299,214,135),(299,215,136),(299,216,137),(299,217,138),(299,218,139),(299,219,140),(299,220,141),(299,221,142),(299,222,143),(299,223,144),(299,224,145),(299,225,146),(299,226,147),(299,402,148),(299,405,149),(299,406,150),(299,470,151),(299,498,152),(299,499,153),(299,500,154),(299,501,155),(299,502,156),(299,503,157),(299,504,158),(299,505,159),(299,506,160),(299,507,161),(299,508,162),(299,509,163),(299,510,164),(299,511,165),(299,512,166),(299,513,167),(299,516,168),(299,517,169),(299,518,170),(299,519,171),(299,520,172),(299,521,173),(299,522,174),(299,523,175),(299,524,176),(299,525,177),(299,526,178),(299,527,179),(299,528,180),(299,529,181),(299,530,182),(299,531,183),(299,533,184),(299,534,185),(299,535,186),(299,536,187),(299,537,188),(299,538,189),(299,539,190),(299,540,191),(299,541,192),(299,542,193),(299,547,194),(299,548,195),(299,549,196),(299,551,197),(299,552,198),(299,553,199),(299,554,200),(299,555,201),(299,556,202),(299,557,203),(299,559,204),(299,560,205),(299,561,206),(299,562,207),(299,563,208),(299,564,209),(299,565,210),(299,566,211),(299,567,212),(299,568,213),(299,569,214),(299,570,215),(299,571,216),(299,572,217),(299,573,218),(299,574,219),(299,575,220),(299,576,221),(299,577,222),(299,578,223),(299,579,224),(299,580,225),(299,581,226),(299,583,227),(299,584,228),(299,585,229),(299,586,230),(299,588,231),(299,589,232),(299,590,233),(299,591,234),(299,592,235),(299,593,236),(299,594,237),(299,595,238),(299,596,239),(299,597,240),(299,598,241),(299,599,242),(299,600,243),(299,601,244),(299,602,245),(299,604,246),(299,605,247),(299,606,248),(299,607,249),(299,608,250),(299,609,251),(299,610,252),(299,611,253),(299,612,254),(299,624,255),(299,630,256),(299,631,257),(299,632,258),(299,633,259),(299,635,260),(299,636,261),(299,637,262),(299,639,263),(299,640,264),(299,641,265),(299,643,266),(299,644,267),(299,645,268),(299,647,269),(299,648,270),(299,649,271),(299,650,272),(299,651,273),(299,652,274),(299,654,275),(299,655,276),(299,656,277),(299,658,278),(299,660,279),(299,661,280),(299,662,281),(299,663,282),(299,664,283),(299,665,284),(299,666,285),(299,1015,286),(299,532,287),(299,148,288),(299,582,289),(299,515,290),(299,558,291),(299,545,292),(299,546,293),(299,122,294),(299,117,295),(299,124,296),(299,125,297),(299,126,298),(299,127,299),(299,128,300),(299,130,301),(299,131,302),(299,132,303),(299,133,304),(299,134,305),(299,667,306),(299,135,307),(299,136,308),(299,138,309),(299,140,310),(299,129,311),(299,603,312),(299,634,313),(299,646,314),(299,642,315),(299,7,316),(299,659,317),(299,653,318),(299,587,319),(299,113,320),(299,629,321),(299,514,322),(299,121,323),(299,201,324),(299,202,325),(299,203,326),(299,204,327),(299,205,328),(299,120,329),(299,168,330),(299,114,331),(299,638,332),(299,657,333),(299,170,334),(299,166,335),(299,155,336),(299,157,337),(299,156,338),(299,154,339),(299,165,340),(299,164,341),(299,169,342),(299,153,343),(299,167,344),(299,149,345),(299,550,346),(299,1024,347),(299,123,348),(299,139,349),(299,152,350),(299,1063,351),(299,1053,352),(299,1056,353),(299,1058,354),(299,137,355),(299,241,356),(299,244,357),(299,243,358),(299,230,359),(299,231,360),(299,232,361),(299,233,362),(299,234,363),(299,235,364),(299,236,365),(299,237,366),(299,238,367),(299,240,368),(299,242,369),(299,245,370),(299,246,371),(299,247,372),(299,248,373),(299,259,374),(299,260,375),(299,261,376),(299,262,377),(299,263,378),(299,264,379),(299,265,380),(299,266,381),(299,267,382),(299,268,383),(299,269,384),(299,270,385),(299,271,386),(299,272,387),(298,4,0),(298,5,1),(298,6,2),(298,8,3),(298,9,4),(298,10,5),(298,11,6),(298,12,7),(298,13,8),(298,14,9),(298,15,10),(298,16,11),(298,17,12),(298,18,13),(298,19,14),(298,20,15),(298,21,16),(298,22,17),(298,23,18),(298,24,19),(298,25,20),(298,26,21),(298,27,22),(298,28,23),(298,29,24),(298,30,25),(298,31,26),(298,32,27),(298,33,28),(298,34,29),(298,35,30),(298,36,31),(298,37,32),(298,38,33),(298,39,34),(298,40,35),(298,41,36),(298,42,37),(298,43,38),(298,44,39),(298,45,40),(298,46,41),(298,47,42),(298,48,43),(298,49,44),(298,50,45),(298,51,46),(298,52,47),(298,53,48),(298,54,49),(298,55,50),(298,56,51),(298,57,52),(298,58,53),(298,59,54),(298,60,55),(298,61,56),(298,62,57),(298,63,58),(298,64,59),(298,65,60),(298,66,61),(298,67,62),(298,68,63),(298,69,64),(298,70,65),(298,71,66),(298,72,67),(298,73,68),(298,74,69),(298,75,70),(298,76,71),(298,77,72),(298,78,73),(298,79,74),(298,80,75),(298,81,76),(298,107,77),(298,109,78),(298,110,79),(298,111,80),(298,112,81),(298,115,82),(298,116,83),(298,118,84),(298,119,85),(298,141,86),(298,142,87),(298,143,88),(298,144,89),(298,145,90),(298,146,91),(298,147,92),(298,150,93),(298,151,94),(298,158,95),(298,159,96),(298,160,97),(298,161,98),(298,162,99),(298,163,100),(298,171,101),(298,172,102),(298,173,103),(298,174,104),(298,175,105),(298,176,106),(298,177,107),(298,178,108),(298,179,109),(298,180,110),(298,181,111),(298,182,112),(298,183,113),(298,184,114),(298,185,115),(298,186,116),(298,187,117),(298,188,118),(298,189,119),(298,190,120),(298,191,121),(298,192,122),(298,193,123),(298,194,124),(298,195,125),(298,196,126),(298,197,127),(298,198,128),(298,199,129),(298,200,130),(298,206,131),(298,207,132),(298,208,133),(298,209,134),(298,210,135),(298,212,136),(298,213,137),(298,214,138),(298,215,139),(298,216,140),(298,217,141),(298,218,142),(298,219,143),(298,220,144),(298,221,145),(298,222,146),(298,223,147),(298,224,148),(298,225,149),(298,226,150),(298,308,151),(298,309,152),(298,310,153),(298,311,154),(298,312,155),(298,313,156),(298,314,157),(298,315,158),(298,316,159),(298,317,160),(298,318,161),(298,319,162),(298,320,163),(298,321,164),(298,322,165),(298,323,166),(298,324,167),(298,325,168),(298,326,169),(298,327,170),(298,328,171),(298,329,172),(298,330,173),(298,331,174),(298,332,175),(298,342,176),(298,343,177),(298,344,178),(298,345,179),(298,346,180),(298,347,181),(298,348,182),(298,349,183),(298,350,184),(298,351,185),(298,352,186),(298,353,187),(298,358,188),(298,359,189),(298,360,190),(298,361,191),(298,362,192),(298,366,193),(298,367,194),(298,368,195),(298,370,196),(298,373,197),(298,374,198),(298,375,199),(298,376,200),(298,377,201),(298,378,202),(298,379,203),(298,380,204),(298,381,205),(298,382,206),(298,383,207),(298,384,208),(298,385,209),(298,386,210),(298,388,211),(298,414,212),(298,415,213),(298,416,214),(298,417,215),(298,418,216),(298,419,217),(298,420,218),(298,421,219),(298,422,220),(298,423,221),(298,424,222),(298,425,223),(298,426,224),(298,427,225),(298,428,226),(298,429,227),(298,430,228),(298,431,229),(298,432,230),(298,434,231),(298,435,232),(298,436,233),(298,437,234),(298,438,235),(298,439,236),(298,440,237),(298,441,238),(298,442,239),(298,443,240),(298,444,241),(298,445,242),(298,446,243),(298,447,244),(298,448,245),(298,449,246),(298,450,247),(298,451,248),(298,452,249),(298,453,250),(298,454,251),(298,455,252),(298,456,253),(298,457,254),(298,458,255),(298,459,256),(298,460,257),(298,461,258),(298,462,259),(298,463,260),(298,464,261),(298,465,262),(298,467,263),(298,468,264),(298,469,265),(298,470,266),(298,498,267),(298,499,268),(298,500,269),(298,501,270),(298,502,271),(298,513,272),(298,516,273),(298,517,274),(298,518,275),(298,519,276),(298,520,277),(298,521,278),(298,522,279),(298,523,280),(298,524,281),(298,525,282),(298,526,283),(298,527,284),(298,528,285),(298,529,286),(298,530,287),(298,531,288),(298,533,289),(298,534,290),(298,541,291),(298,542,292),(298,547,293),(298,548,294),(298,549,295),(298,551,296),(298,552,297),(298,553,298),(298,554,299),(298,555,300),(298,556,301),(298,557,302),(298,559,303),(298,560,304),(298,561,305),(298,562,306),(298,563,307),(298,564,308),(298,565,309),(298,566,310),(298,567,311),(298,568,312),(298,569,313),(298,570,314),(298,571,315),(298,572,316),(298,573,317),(298,574,318),(298,575,319),(298,576,320),(298,577,321),(298,578,322),(298,579,323),(298,580,324),(298,581,325),(298,583,326),(298,584,327),(298,585,328),(298,586,329),(298,588,330),(298,589,331),(298,590,332),(298,591,333),(298,592,334),(298,593,335),(298,594,336),(298,595,337),(298,596,338),(298,597,339),(298,598,340),(298,599,341),(298,600,342),(298,601,343),(298,602,344),(298,604,345),(298,605,346),(298,606,347),(298,607,348),(298,608,349),(298,609,350),(298,610,351),(298,611,352),(298,612,353),(298,624,354),(298,625,355),(298,626,356),(298,630,357),(298,631,358),(298,632,359),(298,633,360),(298,635,361),(298,636,362),(298,637,363),(298,639,364),(298,640,365),(298,641,366),(298,643,367),(298,644,368),(298,645,369),(298,647,370),(298,648,371),(298,649,372),(298,650,373),(298,651,374),(298,652,375),(298,654,376),(298,655,377),(298,656,378),(298,658,379),(298,660,380),(298,661,381),(298,662,382),(298,663,383),(298,664,384),(298,665,385),(298,666,386),(298,668,387),(298,669,388),(298,670,389),(298,671,390),(298,672,391),(298,673,392),(298,674,393),(298,675,394),(298,676,395),(298,677,396),(298,678,397),(298,679,398),(298,681,399),(298,682,400),(298,683,401),(298,685,402),(298,686,403),(298,687,404),(298,688,405),(298,689,406),(298,690,407),(298,692,408),(298,693,409),(298,694,410),(298,695,411),(298,709,412),(298,710,413),(298,712,414),(298,714,415),(298,715,416),(298,716,417),(298,717,418),(298,718,419),(298,720,420),(298,723,421),(298,724,422),(298,727,423),(298,728,424),(298,729,425),(298,731,426),(298,733,427),(298,734,428),(298,736,429),(298,737,430),(298,738,431),(298,739,432),(298,740,433),(298,741,434),(298,743,435),(298,763,436),(298,764,437),(298,765,438),(298,768,439),(298,769,440),(298,771,441),(298,773,442),(298,774,443),(298,775,444),(298,776,445),(298,778,446),(298,779,447),(298,780,448),(298,786,449),(298,787,450),(298,788,451),(298,789,452),(298,790,453),(298,791,454),(298,792,455),(298,793,456),(298,794,457),(298,795,458),(298,796,459),(298,797,460),(298,798,461),(298,799,462),(298,800,463),(298,803,464),(298,805,465),(298,806,466),(298,807,467),(298,812,468),(298,837,469),(298,838,470),(298,839,471),(298,840,472),(298,841,473),(298,842,474),(298,843,475),(298,844,476),(298,845,477),(298,846,478),(298,847,479),(298,848,480),(298,849,481),(298,850,482),(298,851,483),(298,852,484),(298,853,485),(298,854,486),(298,855,487),(298,856,488),(298,857,489),(298,858,490),(298,859,491),(298,860,492),(298,862,493),(298,863,494),(298,864,495),(298,865,496),(298,867,497),(298,868,498),(298,869,499),(298,870,500),(298,871,501),(298,872,502),(298,873,503),(298,874,504),(298,875,505),(298,877,506),(298,1003,507),(298,1004,508),(298,1005,509),(298,1015,510),(298,369,511),(298,532,512),(298,148,513),(298,582,514),(298,515,515),(298,558,516),(298,545,517),(298,546,518),(298,433,519),(298,811,520),(298,810,521),(298,813,522),(298,814,523),(298,815,524),(298,816,525),(298,818,526),(298,819,527),(298,821,528),(298,827,529),(298,829,530),(298,830,531),(298,831,532),(298,832,533),(298,833,534),(298,834,535),(298,835,536),(298,836,537),(298,809,538),(298,825,539),(298,122,540),(298,117,541),(298,735,542),(298,124,543),(298,125,544),(298,126,545),(298,127,546),(298,128,547),(298,130,548),(298,131,549),(298,132,550),(298,133,551),(298,134,552),(298,667,553),(298,135,554),(298,136,555),(298,138,556),(298,140,557),(298,129,558),(298,777,559),(298,804,560),(298,808,561),(298,801,562),(298,802,563),(298,603,564),(298,824,565),(298,823,566),(298,634,567),(298,646,568),(298,642,569),(298,1010,570),(298,7,571),(298,659,572),(298,653,573),(298,587,574),(298,730,575),(298,113,576),(298,742,577),(298,629,578),(298,96,579),(298,413,580),(298,514,581),(298,121,582),(298,201,583),(298,202,584),(298,203,585),(298,204,586),(298,205,587),(298,120,588),(298,168,589),(298,1011,590),(298,972,591),(298,1007,592),(298,1009,593),(298,1008,594),(298,973,595),(298,974,596),(298,975,597),(298,976,598),(298,977,599),(298,979,600),(298,978,601),(298,984,602),(298,732,603),(298,987,604),(298,989,605),(298,990,606),(298,991,607),(298,992,608),(298,993,609),(298,994,610),(298,998,611),(298,1000,612),(298,334,613),(298,336,614),(298,387,615),(298,390,616),(298,283,617),(298,784,618),(298,782,619),(298,783,620),(298,785,621),(298,781,622),(298,995,623),(298,996,624),(298,93,625),(298,281,626),(298,282,627),(298,335,628),(298,391,629),(298,279,630),(298,280,631),(298,333,632),(298,393,633),(298,412,634),(298,466,635),(298,277,636),(298,392,637),(298,278,638),(298,410,639),(298,284,640),(298,411,641),(298,389,642),(298,363,643),(298,338,644),(298,340,645),(298,337,646),(298,341,647),(298,365,648),(298,114,649),(298,878,650),(298,1019,651),(298,982,652),(298,985,653),(298,988,654),(298,1012,655),(298,983,656),(298,986,657),(298,1002,658),(298,876,659),(298,866,660),(298,861,661),(298,638,662),(298,94,663),(298,95,664),(298,97,665),(298,98,666),(298,103,667),(298,102,668),(298,101,669),(298,100,670),(298,105,671),(298,106,672),(298,104,673),(298,766,674),(298,657,675),(298,170,676),(298,166,677),(298,1025,678),(298,1026,679),(298,1030,680),(298,970,681),(298,1032,682),(298,997,683),(298,999,684),(298,971,685),(298,155,686),(298,1028,687),(298,157,688),(298,156,689),(298,154,690),(298,165,691),(298,164,692),(298,169,693),(298,153,694),(298,167,695),(298,1031,696),(298,149,697),(298,1043,698),(298,550,699),(298,698,700),(298,700,701),(298,696,702),(298,703,703),(298,701,704),(298,702,705),(298,704,706),(298,705,707),(298,706,708),(298,707,709),(298,697,710),(298,713,711),(298,721,712),(298,722,713),(298,711,714),(298,719,715),(298,1024,716),(298,123,717),(298,1029,718),(298,1038,719),(298,1040,720),(298,708,721),(298,1054,722),(298,1037,723),(298,139,724),(298,1060,725),(298,1052,726),(298,99,727),(298,1055,728),(298,152,729),(298,1044,730),(298,1053,731),(298,1056,732),(298,1058,733),(298,228,734),(298,137,735),(298,1047,736),(298,1062,737),(298,820,738),(298,371,739),(298,372,740),(298,1057,741),(298,770,742),(298,1001,743),(298,543,744),(298,544,745),(298,828,746),(298,227,747),(298,684,748),(298,1103,749),(298,1102,750),(298,745,751),(298,746,752),(298,759,753),(298,760,754),(298,761,755),(298,762,756),(298,980,757),(298,981,758),(298,744,759),(298,767,760),(298,822,761),(298,749,762),(298,748,763),(298,750,764),(298,1061,765),(298,751,766),(298,752,767),(298,753,768),(298,756,769),(298,754,770),(298,755,771),(298,757,772),(298,758,773),(298,339,774),(298,1098,775),(298,1099,776),(298,1131,777),(298,1132,778),(298,1133,779),(298,1134,780),(298,1135,781),(298,1136,782),(298,879,783),(298,357,784),(298,1100,785),(298,1101,786),(298,826,787),(298,817,788),(298,1148,789),(298,1149,790),(298,1146,791),(298,1150,792),(298,1147,793),(298,1091,794),(298,1120,795),(298,1081,796),(327,354,0),(327,355,1),(327,356,2),(327,882,3),(327,884,4),(327,885,5),(327,881,6),(327,886,7),(327,883,8),(327,880,9),(327,725,10),(327,726,11),(295,8,3),(295,9,4),(295,10,5),(295,11,6),(295,12,7),(295,13,8),(295,14,9),(295,15,10),(295,16,11),(295,17,12),(295,18,13),(295,19,14),(295,20,15),(295,21,16),(295,22,17),(295,23,18),(295,24,19),(295,25,20),(295,26,21),(295,27,22),(295,28,23),(295,29,24),(295,30,25),(295,31,26),(295,32,27),(295,33,28),(295,34,29),(295,35,30),(295,36,31),(295,37,32),(295,38,33),(295,39,34),(295,40,35),(295,41,36),(295,42,37),(295,43,38),(295,44,39),(295,45,40),(295,46,41),(295,47,42),(295,48,43),(295,49,44),(295,50,45),(295,51,46),(295,52,47),(295,53,48),(295,54,49),(295,55,50),(295,56,51),(295,57,52),(295,58,53),(295,59,54),(295,60,55),(295,61,56),(295,62,57),(295,63,58),(295,64,59),(295,65,60),(295,66,61),(295,67,62),(295,68,63),(295,69,64),(295,70,65),(295,71,66),(295,72,67),(295,73,68),(295,74,69),(295,75,70),(295,76,71),(295,77,72),(295,78,73),(295,79,74),(295,80,75),(295,81,76),(295,107,77),(295,109,78),(295,110,79),(295,111,80),(295,112,81),(295,115,82),(295,116,83),(295,118,84),(295,119,85),(295,141,86),(295,142,87),(295,143,88),(295,144,89),(295,145,90),(295,146,91),(295,147,92),(295,150,93),(295,151,94),(295,158,95),(295,159,96),(295,160,97),(295,161,98),(295,162,99),(295,163,100),(295,171,101),(295,172,102),(295,173,103),(295,174,104),(295,175,105),(295,176,106),(295,177,107),(295,178,108),(295,179,109),(295,180,110),(295,181,111),(295,182,112),(295,183,113),(295,184,114),(295,185,115),(295,186,116),(295,187,117),(295,188,118),(295,189,119),(295,190,120),(295,191,121),(295,192,122),(295,193,123),(295,194,124),(295,195,125),(295,196,126),(295,197,127),(295,198,128),(295,199,129),(295,200,130),(295,206,131),(295,207,132),(295,208,133),(295,209,134),(295,210,135),(295,212,136),(295,213,137),(295,214,138),(295,215,139),(295,216,140),(295,217,141),(295,218,142),(295,219,143),(295,220,144),(295,221,145),(295,222,146),(295,223,147),(295,224,148),(295,225,149),(295,226,150),(295,308,151),(295,309,152),(295,310,153),(295,311,154),(295,312,155),(295,313,156),(295,314,157),(295,315,158),(295,316,159),(295,317,160),(295,318,161),(295,319,162),(295,320,163),(295,321,164),(295,322,165),(295,323,166),(295,324,167),(295,325,168),(295,326,169),(295,327,170),(295,328,171),(295,329,172),(295,330,173),(295,331,174),(295,332,175),(295,342,176),(295,343,177),(295,344,178),(295,345,179),(295,346,180),(295,347,181),(295,348,182),(295,349,183),(295,350,184),(295,351,185),(295,352,186),(295,353,187),(295,358,188),(295,359,189),(295,360,190),(295,361,191),(295,362,192),(295,394,193),(295,395,194),(295,396,195),(295,397,196),(295,398,197),(295,399,198),(295,400,199),(295,401,200),(295,402,201),(295,403,202),(295,404,203),(295,405,204),(295,406,205),(295,407,206),(295,408,207),(295,409,208),(295,414,209),(295,415,210),(295,416,211),(295,417,212),(295,418,213),(295,419,214),(295,420,215),(295,421,216),(295,422,217),(295,423,218),(295,424,219),(295,425,220),(295,426,221),(295,427,222),(295,428,223),(295,429,224),(295,430,225),(295,431,226),(295,432,227),(295,434,228),(295,435,229),(295,436,230),(295,437,231),(295,438,232),(295,439,233),(295,440,234),(295,441,235),(295,442,236),(295,443,237),(295,444,238),(295,445,239),(295,446,240),(295,447,241),(295,448,242),(295,449,243),(295,450,244),(295,451,245),(295,452,246),(295,453,247),(295,454,248),(295,455,249),(295,456,250),(295,457,251),(295,458,252),(295,459,253),(295,460,254),(295,461,255),(295,462,256),(295,463,257),(295,464,258),(295,465,259),(295,467,260),(295,468,261),(295,469,262),(295,470,263),(295,471,264),(295,473,265),(295,474,266),(295,475,267),(295,476,268),(295,477,269),(295,478,270),(295,479,271),(295,480,272),(295,482,273),(295,484,274),(295,486,275),(295,487,276),(295,488,277),(295,490,278),(295,491,279),(295,492,280),(295,493,281),(295,494,282),(295,495,283),(295,496,284),(295,497,285),(295,498,286),(295,499,287),(295,500,288),(295,501,289),(295,502,290),(295,503,291),(295,504,292),(295,505,293),(295,506,294),(295,507,295),(295,508,296),(295,509,297),(295,510,298),(295,511,299),(295,512,300),(295,513,301),(295,516,302),(295,517,303),(295,518,304),(295,519,305),(295,520,306),(295,521,307),(295,522,308),(295,523,309),(295,524,310),(295,525,311),(295,526,312),(295,527,313),(295,528,314),(295,529,315),(295,530,316),(295,531,317),(295,533,318),(295,534,319),(295,535,320),(295,536,321),(295,537,322),(295,538,323),(295,539,324),(295,540,325),(295,541,326),(295,542,327),(295,547,328),(295,548,329),(295,549,330),(295,551,331),(295,552,332),(295,553,333),(295,554,334),(295,555,335),(295,556,336),(295,557,337),(295,559,338),(295,560,339),(295,561,340),(295,562,341),(295,563,342),(295,564,343),(295,565,344),(295,566,345),(295,567,346),(295,568,347),(295,569,348),(295,570,349),(295,571,350),(295,572,351),(295,573,352),(295,574,353),(295,575,354),(295,576,355),(295,577,356),(295,578,357),(295,579,358),(295,580,359),(295,581,360),(295,583,361),(295,584,362),(295,585,363),(295,586,364),(295,588,365),(295,589,366),(295,590,367),(295,591,368),(295,592,369),(295,593,370),(295,594,371),(295,595,372),(295,596,373),(295,597,374),(295,598,375),(295,599,376),(295,600,377),(295,601,378),(295,602,379),(295,604,380),(295,605,381),(295,606,382),(295,607,383),(295,608,384),(295,609,385),(295,610,386),(295,611,387),(295,612,388),(295,624,389),(295,630,390),(295,631,391),(295,632,392),(295,633,393),(295,635,394),(295,636,395),(295,637,396),(295,639,397),(295,640,398),(295,641,399),(295,643,400),(295,644,401),(295,645,402),(295,647,403),(295,648,404),(295,649,405),(295,650,406),(295,651,407),(295,652,408),(295,654,409),(295,655,410),(295,656,411),(295,658,412),(295,660,413),(295,661,414),(295,662,415),(295,663,416),(295,664,417),(295,665,418),(295,666,419),(295,914,420),(295,915,421),(295,916,422),(295,917,423),(295,918,424),(295,920,425),(295,921,426),(295,923,427),(295,924,428),(295,925,429),(295,926,430),(295,927,431),(295,928,432),(295,929,433),(295,930,434),(295,931,435),(295,932,436),(295,933,437),(295,936,438),(295,938,439),(295,939,440),(295,940,441),(295,941,442),(295,942,443),(295,943,444),(295,944,445),(295,945,446),(295,946,447),(295,947,448),(295,948,449),(295,949,450),(295,952,451),(295,954,452),(295,956,453),(295,957,454),(295,959,455),(295,960,456),(295,961,457),(295,963,458),(295,965,459),(295,1015,460),(295,532,461),(295,148,462),(295,582,463),(295,515,464),(295,558,465),(295,545,466),(295,546,467),(295,433,468),(295,122,469),(295,117,470),(295,124,471),(295,125,472),(295,126,473),(295,127,474),(295,128,475),(295,130,476),(295,131,477),(295,132,478),(295,133,479),(295,134,480),(295,667,481),(295,135,482),(295,136,483),(295,138,484),(295,140,485),(295,129,486),(295,603,487),(295,634,488),(295,646,489),(295,642,490),(295,7,491),(295,659,492),(295,653,493),(295,587,494),(295,113,495),(295,629,496),(295,413,497),(295,514,498),(295,121,499),(295,201,500),(295,202,501),(295,203,502),(295,204,503),(295,205,504),(295,120,505),(295,168,506),(295,334,507),(295,336,508),(295,387,509),(295,390,510),(295,283,511),(295,363,512),(295,338,513),(295,340,514),(295,337,515),(295,341,516),(295,365,517),(295,114,518),(295,889,519),(295,893,520),(295,894,521),(295,895,522),(295,898,523),(295,899,524),(295,900,525),(295,901,526),(295,905,527),(295,906,528),(295,910,529),(295,911,530),(295,912,531),(295,913,532),(295,638,533),(295,657,534),(295,170,535),(295,892,536),(295,896,537),(295,897,538),(295,902,539),(295,903,540),(295,904,541),(295,907,542),(295,166,543),(295,908,544),(295,909,545),(295,922,546),(295,966,547),(295,967,548),(295,968,549),(295,969,550),(295,891,551),(295,964,552),(295,935,553),(295,934,554),(295,937,555),(295,953,556),(295,955,557),(295,1032,558),(295,951,559),(295,962,560),(295,919,561),(295,958,562),(295,155,563),(295,157,564),(295,156,565),(295,154,566),(295,165,567),(295,164,568),(295,169,569),(295,153,570),(295,167,571),(295,950,572),(295,890,573),(295,149,574),(295,550,575),(295,1024,576),(295,123,577),(295,139,578),(295,1052,579),(295,152,580),(295,1063,581),(295,1053,582),(295,1056,583),(295,1058,584),(295,137,585),(295,483,586),(295,472,587),(295,485,588),(295,371,589),(295,372,590),(295,543,591),(295,544,592),(295,481,593),(295,489,594),(295,339,595),(295,1098,596),(295,1099,597),(295,1131,598),(295,1132,599),(295,1133,600),(295,1134,601),(295,1135,602),(295,1136,603),(295,357,604),(295,1148,605),(295,1149,606),(295,1146,607),(295,1150,608),(295,211,609),(295,364,610),(295,288,611),(295,289,612),(295,286,613),(295,287,614),(295,290,615),(295,291,616),(295,292,617),(295,293,618),(295,294,619),(295,295,620),(295,296,621),(295,297,622),(295,298,623),(295,299,624),(295,300,625),(326,355,0),(326,882,1),(326,884,2),(326,885,3),(326,881,4),(225,634,0),(225,663,1),(225,644,2),(225,630,3),(225,645,4),(225,666,5),(225,632,6),(225,649,7),(225,635,8),(225,648,9),(225,660,10),(225,642,11),(225,657,12),(225,664,13),(225,647,14),(225,654,15),(225,643,16),(225,636,17),(225,646,18),(225,652,19),(225,640,20),(225,667,21),(225,638,22),(225,651,23),(225,637,24),(225,653,25),(225,661,26),(225,641,27),(225,656,28),(225,629,29),(225,650,30),(225,658,31),(225,639,32),(225,665,33),(225,631,34),(225,659,35),(225,662,36),(225,655,37),(225,633,38),(226,668,0),(226,670,1),(226,675,2),(226,674,3),(226,672,4),(226,676,5),(226,673,6),(226,669,7),(226,671,8),(221,274,0),(221,273,1),(221,879,2),(221,276,3),(221,275,4),(228,862,0),(228,868,1),(228,858,2),(228,854,3),(228,860,4),(228,872,5),(228,871,6),(228,857,7),(228,870,8),(228,853,9),(228,863,10),(228,856,11),(228,864,12),(228,852,13),(228,873,14),(228,866,15),(228,855,16),(228,875,17),(228,876,18),(228,877,19),(228,878,20),(228,859,21),(228,861,22),(228,851,23),(228,867,24),(228,869,25),(228,865,26),(228,874,27),(220,297,0),(220,263,1),(220,328,2),(220,240,3),(220,298,4),(220,288,5),(220,262,6),(220,345,7),(220,400,8),(220,451,9),(220,454,10),(220,332,11),(220,295,12),(220,310,13),(220,243,14),(220,306,15),(220,418,16),(220,315,17),(220,420,18),(220,363,19),(220,289,20),(220,432,21),(220,299,22),(220,324,23),(220,254,24),(220,452,25),(220,415,26),(220,394,27),(220,329,28),(220,250,29),(220,320,30),(220,433,31),(220,300,32),(220,453,33),(220,347,34),(220,449,35),(220,467,36),(220,270,37),(220,403,38),(220,465,39),(220,236,40),(220,342,41),(220,318,42),(220,409,43),(220,401,44),(220,258,45),(220,468,46),(220,464,47),(220,241,48),(220,305,49),(220,248,50),(220,395,51),(220,359,52),(220,443,53),(220,316,54),(220,431,55),(220,402,56),(220,257,57),(220,343,58),(220,448,59),(220,426,60),(220,358,61),(220,267,62),(220,321,63),(220,291,64),(220,322,65),(220,404,66),(220,408,67),(220,405,68),(220,348,69),(220,256,70),(220,286,71),(220,430,72),(220,293,73),(220,304,74),(220,230,75),(220,459,76),(220,323,77),(220,435,78),(220,436,79),(220,422,80),(220,287,81),(220,266,82),(220,396,83),(220,350,84),(220,326,85),(220,450,86),(220,361,87),(220,427,88),(220,349,89),(220,441,90),(220,330,91),(220,319,92),(220,434,93),(220,235,94),(220,437,95),(220,397,96),(220,457,97),(220,311,98),(220,362,99),(220,352,100),(220,325,101),(220,244,102),(220,255,103),(220,239,104),(220,301,105),(220,429,106),(220,231,107),(220,440,108),(220,272,109),(220,237,110),(220,469,111),(220,406,112),(220,416,113),(220,309,114),(220,238,115),(220,462,116),(220,290,117),(220,249,118),(220,425,119),(220,407,120),(220,398,121),(220,245,122),(220,444,123),(220,314,124),(220,265,125),(220,327,126),(220,294,127),(220,351,128),(220,269,129),(220,439,130),(220,344,131),(220,421,132),(220,260,133),(220,302,134),(220,317,135),(220,247,136),(220,460,137),(220,445,138),(220,253,139),(220,353,140),(220,268,141),(220,232,142),(220,331,143),(220,428,144),(220,251,145),(220,414,146),(220,246,147),(220,438,148),(220,463,149),(220,261,150),(220,271,151),(220,259,152),(220,234,153),(220,312,154),(220,242,155),(220,252,156),(220,456,157),(220,303,158),(220,419,159),(220,292,160),(220,458,161),(220,360,162),(220,399,163),(220,313,164),(220,461,165),(220,424,166),(220,285,167),(220,307,168),(220,447,169),(220,296,170),(220,423,171),(220,417,172),(220,346,173),(220,264,174),(220,233,175),(220,455,176),(220,308,177),(220,446,178),(220,442,179),(220,338,180),(220,337,181),(220,339,182),(220,340,183),(220,341,184),(220,365,185),(220,364,186),(220,336,187),(220,390,188),(220,366,189),(220,367,190),(220,368,191),(220,369,192),(220,370,193),(220,373,194),(220,374,195),(220,375,196),(220,376,197),(220,377,198),(220,378,199),(220,379,200),(220,380,201),(220,381,202),(220,382,203),(220,383,204),(220,384,205),(220,385,206),(220,386,207),(220,388,208),(220,391,209),(220,281,210),(220,282,211),(220,335,212),(220,279,213),(220,283,214),(220,280,215),(220,333,216),(220,372,217),(220,393,218),(220,412,219),(220,466,220),(220,277,221),(220,392,222),(220,371,223),(220,410,224),(220,389,225),(220,284,226),(220,411,227),(220,334,228),(220,387,229),(220,278,230),(220,413,231),(220,357,232),(220,1025,233),(342,880,0),(342,884,1),(342,883,2),(342,882,3),(342,885,4),(342,354,5),(342,355,6),(342,356,7),(342,357,8),(342,881,9),(342,886,10),(244,947,0),(244,946,1),(244,897,2),(244,949,3),(244,909,4),(244,902,5),(244,963,6),(244,910,7),(244,938,8),(244,906,9),(244,941,10),(244,969,11),(244,945,12),(244,943,13),(244,912,14),(244,913,15),(244,894,16),(244,915,17),(244,914,18),(244,892,19),(244,899,20),(244,966,21),(244,968,22),(244,948,23),(244,901,24),(244,965,25),(244,889,26),(244,893,27),(244,916,28),(244,917,29),(244,900,30),(244,895,31),(244,939,32),(244,942,33),(244,940,34),(244,967,35),(244,905,36),(244,904,37),(244,908,38),(244,898,39),(244,944,40),(244,896,41),(244,907,42),(244,890,43),(244,891,44),(244,903,45),(244,911,46),(244,933,47),(244,964,48),(244,922,49),(244,936,50),(244,925,51),(244,937,52),(244,926,53),(244,923,54),(244,927,55),(244,929,56),(244,928,57),(244,924,58),(244,921,59),(244,931,60),(244,932,61),(244,930,62),(244,920,63),(244,918,64),(244,934,65),(244,935,66),(244,961,67),(244,957,68),(244,952,69),(244,956,70),(244,953,71),(244,954,72),(244,955,73),(244,951,74),(244,950,75),(244,960,76),(244,959,77),(244,958,78),(244,919,79),(244,962,80),(275,1004,0),(275,1003,1),(275,1002,2),(275,1005,3),(275,1011,4),(275,1010,5),(275,1012,6),(275,971,7),(275,970,8),(275,972,9),(275,973,10),(275,979,11),(275,977,12),(275,1001,13),(275,981,14),(275,983,15),(275,982,16),(275,991,17),(275,992,18),(275,978,19),(275,1000,20),(275,997,21),(275,989,22),(275,990,23),(275,988,24),(275,985,25),(275,996,26),(275,995,27),(275,987,28),(275,974,29),(275,975,30),(275,976,31),(275,980,32),(275,984,33),(275,986,34),(275,999,35),(275,998,36),(275,993,37),(275,994,38),(275,1007,39),(275,1009,40),(275,1008,41),(331,93,0),(331,94,1),(331,95,2),(331,96,3),(331,97,4),(331,98,5),(331,99,6),(331,100,7),(331,101,8),(331,102,9),(331,103,10),(331,104,11),(331,105,12),(331,106,13),(238,844,606),(298,1080,797),(220,1026,234),(263,1026,187),(238,740,607),(298,1082,798),(227,1032,162),(275,1019,42),(236,722,526),(238,793,608),(296,544,426),(298,1093,799),(275,1054,43),(236,711,527),(296,227,427),(238,694,609),(298,1083,800),(227,1037,163),(236,719,528),(238,847,610),(236,708,529),(238,688,611),(298,1118,801),(237,32,515),(227,1038,164),(236,149,530),(299,543,388),(296,980,428),(237,53,516),(237,22,517),(237,16,518),(237,42,519),(238,838,612),(237,23,520),(298,1088,802),(223,1024,110),(299,544,389),(296,981,429),(297,139,93),(298,1084,803),(236,1044,531),(238,718,613),(220,1028,235),(298,1125,804),(263,1028,188),(238,841,614),(220,1029,236),(298,1119,805),(263,1029,189),(238,743,615),(298,1121,806),(299,1146,390),(236,1047,532),(238,843,616),(220,1030,237),(298,1085,807),(263,1030,190),(238,695,617),(220,1031,238),(298,1122,808),(263,1031,191),(238,720,618),(220,1043,239),(298,1086,809),(263,1043,192),(238,739,619),(296,1146,430),(238,712,620),(298,1078,810),(227,1040,165),(236,1053,533),(238,690,621),(298,1076,811),(236,1054,534),(238,692,622),(297,1053,94),(299,1150,391),(321,1056,122),(236,1055,535),(321,1057,123),(238,710,623),(236,1056,536),(238,681,624),(236,1057,537),(238,792,625),(236,1058,538),(238,842,626),(236,1061,539),(238,678,627),(298,1117,812),(227,1044,166),(236,1062,540),(238,798,628),(298,1116,813),(227,1047,167),(236,613,541),(238,786,629),(298,1077,814),(236,618,542),(238,714,630),(236,623,543),(238,715,631),(227,1061,168),(236,614,544),(236,615,545),(238,849,632),(298,772,815),(321,1058,124),(236,619,546),(238,687,633),(236,621,547),(238,796,634),(236,622,548),(238,723,635),(236,807,549),(238,837,636),(236,617,550),(238,717,637),(236,616,551),(238,848,638),(236,620,552),(238,791,639),(298,1114,816),(220,1052,240),(298,1095,817),(263,1052,193),(238,685,640),(227,1062,169),(236,682,553),(238,846,641),(298,1094,818),(236,794,554),(238,724,642),(298,1079,819),(238,668,643),(220,1060,241),(263,1060,194),(223,1053,111),(275,1055,44),(237,24,521),(299,239,392),(222,1063,14),(237,39,522),(237,37,523),(360,1015,0),(238,674,644),(237,71,524),(360,612,1),(238,675,645),(237,62,525),(360,498,2),(238,669,646),(237,59,526),(360,628,3),(238,670,647),(360,1013,4),(237,9,527),(360,1063,5),(360,625,6),(238,671,648),(360,470,7),(238,676,649),(237,78,528),(360,624,8),(238,673,650),(237,56,529),(360,500,9),(238,672,651),(237,41,530),(360,627,10),(237,8,531),(360,611,11),(238,35,652),(237,69,532),(360,1014,12),(238,30,653),(360,626,13),(238,67,654),(360,499,14),(238,80,655),(237,74,533),(236,840,555),(238,19,656),(236,790,556),(238,57,657),(236,679,557),(238,6,658),(236,693,558),(238,66,659),(236,789,559),(238,12,660),(236,795,560),(238,5,661),(236,839,561),(238,81,662),(236,845,562),(238,70,663),(236,683,563),(238,17,664),(236,716,564),(238,77,665),(236,709,565),(238,36,666),(236,677,566),(238,18,667),(236,787,567),(238,32,668),(236,727,568),(238,53,669),(236,850,569),(238,22,670),(236,797,570),(238,16,671),(236,788,571),(238,42,672),(236,686,572),(238,23,673),(236,844,573),(238,24,674),(236,740,574),(238,39,675),(236,793,575),(238,37,676),(236,694,576),(238,71,677),(236,847,577),(238,62,678),(236,688,578),(238,59,679),(236,838,579),(238,9,680),(236,718,580),(238,78,681),(236,841,581),(238,56,682),(236,743,582),(238,41,683),(236,843,583),(238,8,684),(236,695,584),(238,69,685),(236,720,585),(238,74,686),(236,739,586),(238,4,687),(236,712,587),(238,26,688),(236,684,588),(238,20,689),(236,690,589),(238,14,690),(236,692,590),(238,33,691),(236,710,591),(238,55,692),(236,681,592),(238,21,693),(236,792,593),(238,76,694),(236,842,594),(238,31,695),(236,678,595),(238,28,696),(236,798,596),(238,75,697),(236,786,597),(238,51,698),(236,714,598),(238,60,699),(236,715,599),(238,68,700),(236,849,600),(238,72,701),(236,687,601),(238,52,702),(236,796,602),(238,29,703),(236,723,603),(238,54,704),(236,837,604),(238,11,705),(236,717,605),(238,50,706),(236,691,606),(238,10,707),(236,848,607),(238,15,708),(236,791,608),(238,25,709),(236,685,609),(238,38,710),(236,846,610),(238,632,711),(236,724,611),(238,633,712),(236,668,612),(238,639,713),(236,674,613),(238,196,714),(236,675,614),(238,197,715),(236,669,615),(238,143,716),(236,670,616),(238,219,717),(236,671,617),(238,186,718),(236,676,618),(238,141,719),(236,673,619),(238,176,720),(236,672,620),(238,213,721),(236,483,621),(238,142,722),(236,472,622),(238,150,723),(236,485,623),(238,224,724),(236,35,624),(238,223,725),(236,30,625),(238,182,726),(236,67,626),(238,187,727),(236,80,627),(238,174,728),(236,19,628),(238,118,729),(236,57,629),(238,221,730),(236,6,630),(238,180,731),(236,66,631),(238,147,732),(236,12,632),(238,208,733),(236,5,633),(238,185,734),(236,81,634),(238,175,735),(236,70,635),(238,145,736),(236,17,636),(237,4,534),(236,77,637),(237,26,535),(236,36,638),(237,20,536),(236,18,639),(238,115,737),(237,14,537),(236,32,640),(238,195,738),(237,33,538),(236,53,641),(238,109,739),(237,55,539),(236,22,642),(238,220,740),(237,21,540),(236,16,643),(238,107,741),(237,76,541),(236,42,644),(238,160,742),(237,31,542),(236,23,645),(238,151,743),(237,28,543),(236,24,646),(238,210,744),(237,75,544),(236,39,647),(238,225,745),(237,51,545),(236,37,648),(238,189,746),(237,60,546),(236,71,649),(238,144,747),(237,68,547),(236,62,650),(238,198,748),(237,72,548),(236,59,651),(238,194,749),(237,52,549),(236,9,652),(238,184,750),(237,29,550),(236,78,653),(238,177,751),(237,54,551),(236,56,654),(238,190,752),(237,11,552),(236,41,655),(238,159,753),(237,50,553),(236,8,656),(238,226,754),(237,10,554),(236,69,657),(238,116,755),(237,15,555),(236,74,658),(238,173,756),(237,25,556),(236,4,659),(238,188,757),(237,38,557),(236,26,660),(238,209,758),(237,632,558),(236,20,661),(238,199,759),(237,633,559),(236,14,662),(238,178,760),(237,639,560),(236,33,663),(238,200,761),(237,196,561),(236,55,664),(238,193,762),(237,197,562),(236,21,665),(238,163,763),(237,143,563),(236,76,666),(238,158,764),(237,219,564),(236,31,667),(238,110,765),(237,186,565),(236,28,668),(238,112,766),(237,141,566),(236,75,669),(238,172,767),(237,176,567),(236,51,670),(238,162,768),(237,213,568),(236,60,671),(238,181,769),(237,142,569),(236,68,672),(238,161,770),(237,150,570),(236,72,673),(238,191,771),(237,224,571),(236,52,674),(238,222,772),(237,223,572),(236,29,675),(238,192,773),(237,182,573),(236,54,676),(238,183,774),(237,187,574),(236,11,677),(238,171,775),(237,174,575),(236,50,678),(238,257,776),(237,118,576),(236,10,679),(238,253,777),(237,221,577),(236,15,680),(238,379,778),(237,180,578),(236,25,681),(238,256,779),(237,147,579),(236,38,682),(238,380,780),(237,208,580),(236,632,683),(238,370,781),(237,185,581),(236,633,684),(238,378,782),(237,175,582),(236,639,685),(238,249,783),(237,145,583),(236,196,686),(238,252,784),(237,115,584),(236,197,687),(238,251,785),(237,195,585),(236,143,688),(238,250,786),(237,109,586),(236,219,689),(238,254,787),(237,220,587),(236,186,690),(238,376,788),(237,107,588),(236,141,691),(238,385,789),(237,160,589),(236,176,692),(238,381,790),(237,151,590),(236,213,693),(238,383,791),(237,210,591),(236,142,694),(238,255,792),(237,225,592),(236,150,695),(238,384,793),(237,189,593),(236,224,696),(238,258,794),(237,144,594),(236,223,697),(238,371,795),(237,198,595),(236,182,698),(238,372,796),(237,194,596),(236,187,699),(238,1057,797),(237,184,597),(236,174,700),(238,770,798),(237,177,598),(236,118,701),(238,1001,799),(237,190,599),(236,221,702),(238,543,800),(237,159,600),(236,180,703),(238,544,801),(237,226,601),(236,147,704),(238,828,802),(237,116,602),(236,208,705),(238,227,803),(237,173,603),(236,185,706),(238,684,804),(237,188,604),(236,175,707),(238,1103,805),(237,209,605),(236,145,708),(238,1102,806),(237,199,606),(236,115,709),(238,745,807),(237,178,607),(236,195,710),(238,746,808),(237,200,608),(236,109,711),(238,759,809),(237,193,609),(236,220,712),(238,760,810),(237,163,610),(236,107,713),(238,761,811),(237,158,611),(236,160,714),(238,762,812),(237,110,612),(236,151,715),(238,980,813),(237,112,613),(236,210,716),(238,981,814),(237,172,614),(236,225,717),(238,744,815),(237,162,615),(236,189,718),(238,767,816),(237,181,616),(236,144,719),(238,822,817),(237,161,617),(236,198,720),(238,749,818),(237,191,618),(236,194,721),(238,748,819),(237,222,619),(236,184,722),(238,750,820),(237,192,620),(236,177,723),(238,1061,821),(237,183,621),(236,190,724),(238,751,822),(237,171,622),(236,159,725),(238,752,823),(237,371,623),(236,226,726),(238,753,824),(237,372,624),(236,116,727),(238,756,825),(237,241,625),(236,173,728),(238,754,826),(237,244,626),(236,188,729),(238,755,827),(237,243,627),(236,209,730),(238,757,828),(237,230,628),(236,199,731),(238,758,829),(237,231,629),(236,178,732),(238,339,830),(237,232,630),(236,200,733),(238,1098,831),(237,233,631),(236,193,734),(238,1099,832),(237,234,632),(236,163,735),(238,1131,833),(237,235,633),(236,158,736),(238,1132,834),(237,236,634),(236,110,737),(238,1133,835),(237,237,635),(236,112,738),(238,1134,836),(237,238,636),(236,227,739),(238,1135,837),(237,240,637),(236,172,740),(238,1136,838),(237,242,638),(236,162,741),(238,879,839),(237,245,639),(236,181,742),(238,357,840),(237,246,640),(236,161,743),(238,1100,841),(237,247,641),(236,191,744),(238,1101,842),(237,248,642),(236,222,745),(238,826,843),(237,259,643),(236,192,746),(238,817,844),(237,260,644),(236,183,747),(238,1148,845),(237,261,645),(236,171,748),(238,1149,846),(237,262,646),(236,1076,749),(238,1146,847),(237,263,647),(236,1077,750),(238,1150,848),(237,264,648),(236,1078,751),(238,1147,849),(237,265,649),(236,1079,752),(238,1091,850),(237,266,650),(236,1080,753),(238,1120,851),(237,267,651),(236,1081,754),(238,1081,852),(237,268,652),(236,1082,755),(238,1080,853),(237,269,653),(236,1083,756),(238,1082,854),(237,270,654),(236,1084,757),(238,1093,855),(237,271,655),(236,1085,758),(238,1083,856),(237,272,656),(236,1086,759),(238,1118,857),(237,543,657),(236,1088,760),(238,1088,858),(237,544,658),(236,1090,761),(238,1084,859),(237,481,659),(236,1091,762),(238,1125,860),(237,489,660),(236,1093,763),(238,1119,861),(237,339,661),(263,260,195),(237,1098,662),(263,266,196),(237,1099,663),(263,244,197),(237,1131,664),(263,269,198),(237,1132,665),(263,272,199),(237,1133,666),(263,263,200),(237,1134,667),(263,257,201),(238,1121,862),(263,253,202),(238,1085,863),(263,379,203),(238,1122,864),(263,241,204),(237,1135,668),(263,245,205),(237,1136,669),(263,256,206),(238,1086,865),(263,232,207),(237,357,670),(263,380,208),(238,1078,866),(263,237,209),(237,1148,671),(263,370,210),(238,1076,867),(263,268,211),(237,1149,672),(263,264,212),(237,1146,673),(263,235,213),(237,1150,674),(263,247,214),(237,239,675),(263,270,215),(237,211,676),(263,246,216),(237,364,677),(263,261,217),(237,288,678),(263,243,218),(237,289,679),(263,378,219),(238,1117,868),(263,239,220),(237,286,680),(263,249,221),(238,1116,869),(263,271,222),(237,287,681),(263,233,223),(237,290,682),(263,252,224),(238,1077,870),(263,230,225),(237,291,683),(263,251,226),(238,772,871),(263,248,227),(237,292,684),(263,250,228),(238,1114,872),(263,254,229),(238,1095,873),(263,259,230),(237,293,685),(263,376,231),(238,1094,874),(263,385,232),(238,1079,875),(263,381,233),(238,1127,876),(263,383,234),(238,1128,877),(263,236,235),(237,294,686),(263,255,236),(238,1115,878),(263,262,237),(237,295,687),(263,231,238),(237,296,688),(263,242,239),(237,297,689),(263,265,240),(237,298,690),(263,384,241),(238,1126,879),(263,234,242),(237,299,691),(263,267,243),(237,300,692),(263,258,244),(263,238,245),(263,240,246),(297,1057,95),(238,1138,880),(298,1127,820),(236,1094,764),(238,1139,881),(298,1128,821),(298,1115,822),(236,1095,765),(238,1153,882),(236,1114,766),(238,1152,883),(298,1126,823),(330,1088,11),(236,1115,767),(238,1143,884),(298,1138,824),(330,1090,12),(298,1139,825),(236,1116,768),(238,1144,885),(330,1091,13),(236,1117,769),(238,1145,886),(298,1153,826),(330,1093,14),(236,1118,770),(238,1123,887),(298,1152,827),(330,1094,15),(236,1119,771),(238,1124,888),(298,1143,828),(330,1095,16),(236,1120,772),(238,1090,889),(298,1144,829),(238,1142,890),(298,1145,830),(238,747,891),(237,301,693),(298,1123,831),(295,301,626),(298,1124,832),(295,302,627),(238,211,892),(237,302,694),(237,303,695),(295,303,628),(238,364,893),(298,1090,833),(237,304,696),(238,108,894),(295,304,629),(298,1142,834),(237,305,697),(295,305,630),(238,691,895),(298,747,835),(298,211,836),(295,306,631),(238,680,896),(237,306,698),(237,307,699),(295,307,632),(238,699,897),(298,364,837),(295,285,633),(237,285,700),(238,288,898),(298,108,838),(238,289,899),(298,691,839),(298,680,840),(238,286,900),(238,287,901),(298,699,841),(220,1098,242),(263,1098,247),(238,290,902),(298,288,842),(238,291,903),(298,289,843),(220,1099,243),(263,1099,248),(238,292,904),(298,286,844),(220,1100,244),(263,1100,249),(238,293,905),(298,287,845),(298,290,846),(238,294,906),(220,1101,245),(263,1101,250),(238,295,907),(298,291,847),(220,1102,246),(263,1102,251),(238,296,908),(298,292,848),(220,1103,247),(298,293,849),(263,1103,252),(238,297,909),(220,1131,248),(263,1131,253),(220,1132,249),(263,1132,254),(220,1133,250),(263,1133,255),(220,1134,251),(263,1134,256),(220,1135,252),(263,1135,257),(220,1136,253),(263,1136,258),(220,1146,254),(263,1146,259),(220,1147,255),(263,1147,260),(220,1148,256),(263,1148,261),(220,1149,257),(263,1149,262),(220,1150,258),(263,1150,263),(238,298,910),(298,294,850),(330,1114,17),(298,295,851),(236,1121,773),(238,299,911),(330,1115,18),(298,296,852),(236,1122,774),(238,300,912),(330,1116,19),(298,297,853),(236,1123,775),(238,301,913),(330,1117,20),(298,298,854),(236,1124,776),(238,302,914),(330,1118,21),(236,1125,777),(238,303,915),(298,299,855),(330,1119,22),(298,300,856),(236,1126,778),(238,304,916),(330,1120,23),(298,301,857),(236,1127,779),(238,305,917),(330,1121,24),(236,1128,780),(330,1122,25),(236,1138,781),(330,1123,26),(236,1139,782),(330,1124,27),(330,1125,28),(330,1126,29),(296,1150,431),(238,306,918),(298,302,858),(330,1127,30),(298,303,859),(236,1142,783),(238,307,919),(330,1128,31),(236,1143,784),(238,285,920),(298,304,860),(298,305,861),(298,306,862),(298,307,863),(330,1138,32),(236,1144,785),(330,1139,33),(236,1145,786),(330,1142,34),(236,1152,787),(330,1143,35),(236,1153,788),(330,1144,36),(330,1145,37),(330,1152,38),(330,1153,39),(296,211,432),(299,211,393),(371,277,0),(371,1025,1),(371,1026,2),(371,1029,3),(371,392,4),(371,410,5),(371,411,6),(371,412,7),(371,413,8),(371,391,9),(371,390,10),(371,393,11),(371,389,12),(371,364,13),(371,365,14),(371,1148,15),(371,1136,16),(371,1135,17),(371,1099,18),(371,1098,19),(371,1147,20),(371,1052,21),(371,335,22),(371,336,23),(371,282,24),(371,283,25),(371,1028,26),(371,284,27),(371,333,28),(371,334,29),(371,1043,30),(371,337,31),(371,338,32),(371,339,33),(371,340,34),(371,341,35),(371,278,36),(371,1030,37),(371,1031,38),(371,279,39),(371,280,40),(371,281,41),(371,1150,42),(371,1149,43),(371,1132,44),(371,1131,45),(371,1133,46),(371,1134,47),(371,371,48),(371,1101,49),(371,1102,50),(371,1060,51),(371,1100,52),(371,1103,53),(371,372,54),(371,466,55),(371,1146,56),(296,108,433),(298,285,864),(236,730,270),(238,730,229),(273,483,24),(295,4,0),(237,342,234),(236,481,267),(236,487,263),(238,493,227),(238,487,223),(273,481,21),(273,487,17),(295,5,1),(295,6,2),(237,487,228),(237,493,232);
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

-- Dump completed on 2015-01-02 17:02:21
