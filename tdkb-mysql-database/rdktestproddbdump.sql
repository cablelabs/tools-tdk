-- MySQL dump 10.13  Distrib 5.5.47, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: rdktesttoolproddb
-- ------------------------------------------------------
-- Server version	5.5.47-0ubuntu0.14.04.1

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
  `category` varchar(255) NOT NULL,
  `groups_id` bigint(20) DEFAULT NULL,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `category` (`category`,`name`),
  KEY `FK3D2E11C5984B586A` (`groups_id`),
  CONSTRAINT `FK3D2E11C5984B586A` FOREIGN KEY (`groups_id`) REFERENCES `groups` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `box_manufacturer`
--

LOCK TABLES `box_manufacturer` WRITE;
/*!40000 ALTER TABLE `box_manufacturer` DISABLE KEYS */;
INSERT INTO `box_manufacturer` VALUES (1,0,'RDKB',4,'Cisco'),(2,0,'RDKV',4,'Cisco'),(3,0,'RDKB',4,'Arris');
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
  `groups_id` bigint(20) DEFAULT NULL,
  `name` varchar(255) NOT NULL,
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
  `category` varchar(255) NOT NULL,
  `groups_id` bigint(20) DEFAULT NULL,
  `type` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name_category` (`name`,`category`),
  KEY `FK863DB12E984B586A` (`groups_id`),
  CONSTRAINT `FK863DB12E984B586A` FOREIGN KEY (`groups_id`) REFERENCES `groups` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `box_type`
--

LOCK TABLES `box_type` WRITE;
/*!40000 ALTER TABLE `box_type` DISABLE KEYS */;
INSERT INTO `box_type` VALUES (1,0,'RDKV',4,'Client','Hybrid-1'),(2,0,'RDKV',4,'Gateway','IPClient-3'),(3,0,'RDKB',4,'Gateway','Hybrid-1'),(6,0,'RDKV',4,'Client','Terminal-RNG'),(8,0,'RDKV',4,'Client','Emulator-Client'),(9,0,'RDKB',4,'Client','BTGateway');
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
  `agent_monitor_port` varchar(255) NOT NULL,
  `box_manufacturer_id` bigint(20) NOT NULL,
  `box_type_id` bigint(20) NOT NULL,
  `category` varchar(255) NOT NULL,
  `device_status` varchar(255) NOT NULL,
  `gateway_ip` varchar(255) DEFAULT NULL,
  `groups_id` bigint(20) DEFAULT NULL,
  `is_child` int(11) NOT NULL,
  `log_transfer_port` varchar(255) NOT NULL,
  `mac_id` varchar(255) DEFAULT NULL,
  `recorder_id` varchar(255) DEFAULT NULL,
  `socvendor_id` bigint(20) NOT NULL,
  `status_port` varchar(255) NOT NULL,
  `stb_ip` varchar(255) NOT NULL,
  `stb_name` varchar(255) NOT NULL,
  `stb_port` varchar(255) NOT NULL,
  `upload_binary_status` varchar(255) NOT NULL,
  `serial_no` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `stb_name` (`stb_name`),
  KEY `FKB06B1E56984B586A` (`groups_id`),
  KEY `FKB06B1E567F41D9E1` (`box_manufacturer_id`),
  KEY `FKB06B1E56DB9F6C41` (`box_type_id`),
  KEY `FKB06B1E565EB4A22A` (`socvendor_id`),
  CONSTRAINT `FKB06B1E565EB4A22A` FOREIGN KEY (`socvendor_id`) REFERENCES `socvendor` (`id`),
  CONSTRAINT `FKB06B1E567F41D9E1` FOREIGN KEY (`box_manufacturer_id`) REFERENCES `box_manufacturer` (`id`),
  CONSTRAINT `FKB06B1E56984B586A` FOREIGN KEY (`groups_id`) REFERENCES `groups` (`id`),
  CONSTRAINT `FKB06B1E56DB9F6C41` FOREIGN KEY (`box_type_id`) REFERENCES `box_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=78 DEFAULT CHARSET=latin1;
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
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
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
  KEY `FKABF7505FEC4FF12A` (`device_id`),
  CONSTRAINT `FKABF7505FEC4FF12A` FOREIGN KEY (`device_id`) REFERENCES `device` (`id`)
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
  `category` varchar(255) NOT NULL,
  `groups_id` bigint(20) DEFAULT NULL,
  `name` varchar(255) NOT NULL,
  `status` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `FKDC71DF56984B586A` (`groups_id`),
  CONSTRAINT `FKDC71DF56984B586A` FOREIGN KEY (`groups_id`) REFERENCES `groups` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
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
  KEY `FKD0056F5FEC4FF12A` (`device_id`),
  KEY `FKD0056F5F8CE1A4DF` (`device_group_devices_id`),
  CONSTRAINT `FKD0056F5F8CE1A4DF` FOREIGN KEY (`device_group_devices_id`) REFERENCES `device_group` (`id`),
  CONSTRAINT `FKD0056F5FEC4FF12A` FOREIGN KEY (`device_id`) REFERENCES `device` (`id`)
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
  KEY `FKC6618189B9FA7CEA` (`stream_id`),
  KEY `FKC6618189EC4FF12A` (`device_id`),
  CONSTRAINT `FKC6618189B9FA7CEA` FOREIGN KEY (`stream_id`) REFERENCES `streaming_details` (`id`),
  CONSTRAINT `FKC6618189EC4FF12A` FOREIGN KEY (`device_id`) REFERENCES `device` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
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
  `category` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `FKA1287DF19FCEDC3B` (`execution_result_id`),
  CONSTRAINT `FKA1287DF19FCEDC3B` FOREIGN KEY (`execution_result_id`) REFERENCES `execution_result` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4157 DEFAULT CHARSET=latin1;
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
  `application_url` varchar(255) DEFAULT NULL,
  `category` varchar(255) NOT NULL,
  `date_of_execution` datetime DEFAULT NULL,
  `device` varchar(255) DEFAULT NULL,
  `device_group` varchar(255) DEFAULT NULL,
  `execution_status` varchar(255) DEFAULT NULL,
  `execution_time` varchar(255) DEFAULT NULL,
  `groups_id` bigint(20) DEFAULT NULL,
  `is_aborted` bit(1) NOT NULL,
  `is_bench_mark_enabled` bit(1) NOT NULL,
  `is_marked` int(11) NOT NULL,
  `is_performance_done` bit(1) NOT NULL,
  `is_rerun_required` bit(1) NOT NULL,
  `is_stb_log_required` bit(1) NOT NULL,
  `is_system_diagnostics_enabled` bit(1) NOT NULL,
  `name` varchar(255) NOT NULL,
  `output_data` longtext,
  `result` varchar(255) DEFAULT NULL,
  `script` varchar(255) DEFAULT NULL,
  `script_count` int(11) NOT NULL,
  `script_group` varchar(255) DEFAULT NULL,
  `third_party_execution_details_id` bigint(20) DEFAULT NULL,
  `real_execution_time` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `FKBEF90B18D2187869` (`third_party_execution_details_id`),
  KEY `FKBEF90B18984B586A` (`groups_id`),
  CONSTRAINT `FKBEF90B18984B586A` FOREIGN KEY (`groups_id`) REFERENCES `groups` (`id`),
  CONSTRAINT `FKBEF90B18D2187869` FOREIGN KEY (`third_party_execution_details_id`) REFERENCES `third_party_execution_details` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=941 DEFAULT CHARSET=latin1;
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
  `category` varchar(255) NOT NULL,
  `date_of_execution` datetime DEFAULT NULL,
  `device` varchar(255) NOT NULL,
  `device_ip` varchar(255) NOT NULL,
  `execution_id` bigint(20) NOT NULL,
  `execution_time` varchar(255) DEFAULT NULL,
  `status` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `FKE2CBE55D8358C58A` (`execution_id`),
  CONSTRAINT `FKE2CBE55D8358C58A` FOREIGN KEY (`execution_id`) REFERENCES `execution` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=940 DEFAULT CHARSET=latin1;
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
  `category` varchar(255) NOT NULL,
  `date_of_execution` datetime DEFAULT NULL,
  `device` varchar(255) NOT NULL,
  `device_id_string` varchar(255) DEFAULT NULL,
  `exec_device_id` bigint(20) DEFAULT NULL,
  `execution_id` bigint(20) NOT NULL,
  `execution_device_id` bigint(20) NOT NULL,
  `execution_output` longtext,
  `execution_time` varchar(255) DEFAULT NULL,
  `script` varchar(255) NOT NULL,
  `status` varchar(255) DEFAULT NULL,
  `module_name` varchar(255) DEFAULT NULL,
  `total_execution_time` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `FKFAAE8F24F5E1059B` (`execution_device_id`),
  KEY `FKFAAE8F241B03E2FC` (`exec_device_id`),
  KEY `FKFAAE8F248358C58A` (`execution_id`),
  CONSTRAINT `FKFAAE8F241B03E2FC` FOREIGN KEY (`exec_device_id`) REFERENCES `device` (`id`),
  CONSTRAINT `FKFAAE8F248358C58A` FOREIGN KEY (`execution_id`) REFERENCES `execution` (`id`),
  CONSTRAINT `FKFAAE8F24F5E1059B` FOREIGN KEY (`execution_device_id`) REFERENCES `execution_device` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3497 DEFAULT CHARSET=latin1;
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
  `category` varchar(255) NOT NULL,
  `module_id` bigint(20) NOT NULL,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `category` (`category`,`name`),
  KEY `FK524F73D89E2CF16A` (`module_id`),
  CONSTRAINT `FK524F73D89E2CF16A` FOREIGN KEY (`module_id`) REFERENCES `module` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=272 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `function`
--

LOCK TABLES `function` WRITE;
/*!40000 ALTER TABLE `function` DISABLE KEYS */;
INSERT INTO `function` VALUES (2,0,'RDKB',26,'WECB_GetParamAttributes'),(3,0,'RDKB',26,'WECB_AddObject'),(4,0,'RDKB',26,'WECB_SetParamValues'),(5,0,'RDKB',26,'WECB_GetParamNames'),(6,0,'RDKB',26,'WECB_SetSessionId'),(7,0,'RDKB',26,'WECB_SetCommit'),(8,0,'RDKB',26,'WECB_GetParamValues'),(9,0,'RDKB',26,'WECB_SetParamAttribute'),(10,0,'RDKB',26,'WECB_DelObject'),(11,0,'RDKB',27,'AdvancedConfig_AddObject'),(12,0,'RDKB',27,'AdvancedConfig_Get'),(13,0,'RDKB',27,'AdvancedConfig_Set'),(14,0,'RDKB',27,'AdvancedConfig_DelObject'),(15,0,'RDKB',19,'ExecuteSNMPCommand'),(16,0,'RDKB',19,'LogValidation'),(17,0,'RDKB',27,'WebPA_SendRequest'),(101,0,'RDKB',38,'CosaCM_GetResetCount'),(102,0,'RDKB',38,'CosaCM_GetCMErrorCodewords'),(108,0,'RDKB',39,'wifi_getencryptmethod'),(110,0,'RDKB',41,'Moca_Enable'),(111,0,'RDKB',42,'CosaWIFI_DmlWiFiSsidGetNumberOfEntries'),(112,0,'RDKB',42,'CosaWIFI_DmlWiFiAPGetNumberOfEntries'),(113,0,'RDKB',42,'CosaWIFI_DmlWiFiRadioApplyCfg'),(133,0,'RDKB',45,'CCSPMBUS_Init'),(134,0,'RDKB',45,'CCSPMBUS_LoadCfg'),(135,0,'RDKB',45,'CCSPMBUS_LoadDmXml'),(136,0,'RDKB',45,'CCSPMBUS_Exit'),(137,0,'RDKB',45,'CCSPMBUS_RegisterPath'),(138,0,'RDKB',45,'CCSPMBUS_RegisterBase'),(139,0,'RDKB',45,'CCSPMBUS_RegisterEvent'),(140,0,'RDKB',45,'CCSPMBUS_UnRegisterEvent'),(141,0,'RDKB',45,'CCSPMBUS_GetRegisteredComponents'),(142,0,'RDKB',45,'CCSPMBUS_IsSystemReady'),(143,0,'RDKB',45,'CCSPMBUS_GetHealth'),(144,0,'RDKB',45,'CCSPMBUS_SendSignal'),(145,0,'RDKB',45,'CCSPMBUS_BusCheck'),(146,0,'RDKB',45,'CCSPMBUS_CheckNamespaceDataType'),(147,0,'RDKB',45,'CCSPMBUS_DiskComponentSupportingDynamicTbl'),(148,0,'RDKB',45,'CCSPMBUS_DiskNamespaceSupportedByComponent'),(149,0,'RDKB',45,'CCSPMBUS_DumpComponentRegistry'),(150,0,'RDKB',45,'CCSPMBUS_GetAllocMemory'),(151,0,'RDKB',45,'CCSPMBUS_GetMaxMemory'),(152,0,'RDKB',45,'CCSPMBUS_InformEndSession'),(153,0,'RDKB',45,'CCSPMBUS_QueryStatus'),(154,0,'RDKB',45,'CCSPMBUS_RegisterCapabilities'),(155,0,'RDKB',45,'CCSPMBUS_ReqSessionId'),(156,0,'RDKB',45,'CCSPMBUS_UnRegisterComponent'),(157,0,'RDKB',45,'CCSPMBUS_UnRegisterNamespace'),(160,0,'RDKB',38,'CosaCM_GetLoopDiagnosticsStart'),(161,0,'RDKB',38,'CosaCM_GetLoopDiagnosticsDetails'),(162,0,'RDKB',38,'COSACM_GetDHCPInfo'),(163,0,'RDKB',38,'COSACM_GetDOCSISInfo'),(164,0,'RDKB',38,'COSACM_GetLog'),(165,0,'RDKB',38,'COSACM_SetLog'),(166,0,'RDKB',38,'CosaCM_GetUpstreamChannelId'),(175,0,'RDKB',38,'COSACM_SetLoopDiagnosticsStart'),(176,0,'RDKB',38,'CosaCM_SetUpstreamChannelId'),(177,0,'RDKB',38,'CosaCM_GetStartDSFrequency'),(178,0,'RDKB',38,'CosaCM_SetStartDSFrequency'),(179,0,'RDKB',38,'COSACM_GetDocsisLog'),(180,0,'RDKB',38,'COSACM_GetDownstreamChannel'),(181,0,'RDKB',38,'COSACM_GetUpstreamChannel'),(182,0,'RDKB',38,'CosaCM_GetProvType'),(183,0,'RDKB',38,'CosaCM_GetIPv6DHCPInfo'),(190,0,'RDKB',51,'MTA_agent_SetParameterAttr'),(191,0,'RDKB',51,'MTA_agent_SetParameterValues'),(192,0,'RDKB',51,'MTA_agent_Init'),(193,0,'RDKB',51,'MTA_agent_Terminate'),(194,0,'RDKB',51,'MTA_agent_GetParameterValues'),(195,0,'RDKB',51,'MTA_agent_GetParameterNames'),(196,0,'RDKB',51,'MTA_agent_GetParameterAttr'),(197,0,'RDKB',51,'MTA_agent_Commit'),(198,0,'RDKB',51,'MTA_agent_GetParameterNames_NextLevel'),(199,0,'RDKB',51,'MTA_agent_AddTbl'),(200,0,'RDKB',51,'MTA_agent_DelTble'),(201,0,'RDKB',51,'MTA_agent_GetHealth'),(202,0,'RDKB',51,'MTA_agent_SetSessionId'),(217,0,'RDKB',54,'WIFIAgent_Get'),(218,0,'RDKB',54,'WIFIAgent_AddObject'),(219,0,'RDKB',54,'WIFIAgent_DelObject'),(220,0,'RDKB',54,'WIFIAgent_GetAttr'),(221,0,'RDKB',54,'WIFIAgent_SetSessionId'),(222,0,'RDKB',54,'WIFIAgent_Set'),(223,0,'RDKB',54,'WIFIAgent_SetCommit'),(224,0,'RDKB',54,'WIFIAgent_SetAttr'),(225,0,'RDKB',54,'WIFIAgent_GetNames'),(226,0,'RDKB',54,'WIFIAgent_GetHealth'),(227,0,'RDKB',54,'WIFIAgent_Set_Get'),(228,0,'RDKB',38,'COSACM_SetMDDIPOverride_ArgMemory_unalloc'),(229,0,'RDKB',38,'COSACM_GetMDDIPOverride_ArgMemory_unalloc'),(230,0,'RDKB',38,'COSACM_GetCMCert_ArgMemory_unalloc'),(231,0,'RDKB',38,'COSACM_GetMarket'),(233,0,'RDKB',38,'COSACM_GetCMCertStatus_InvalidArg'),(234,0,'RDKB',38,'COSACM_GetCPEList_InvalidArg'),(235,0,'RDKB',38,'COSACM_GetMDDIPOverride'),(236,0,'RDKB',38,'COSACM_CableModemInitialize'),(237,0,'RDKB',38,'COSACM_GetCMCert'),(238,0,'RDKB',38,'COSACM_CableModemRemove'),(239,0,'RDKB',38,'COSACM_CableModemCreate'),(240,0,'RDKB',38,'COSACM_GetCMCertStatus'),(241,0,'RDKB',38,'COSACM_GetCPEList'),(242,0,'RDKB',38,'COSACM_GetMarket_ArgMemory_unalloc'),(243,0,'RDKB',38,'COSACM_SetMDDIPOverride'),(244,0,'RDKB',38,'CosaCM_GetTelephonyTftpStatus'),(246,0,'RDKB',55,'CMAgent_Get'),(247,0,'RDKB',55,'CMAgent_AddObject'),(248,0,'RDKB',55,'CMAgent_DelObject'),(249,0,'RDKB',55,'CMAgent_GetAttr'),(250,0,'RDKB',55,'CMAgent_GetNames'),(251,0,'RDKB',55,'CMAgent_GetHealth'),(252,0,'RDKB',55,'CMAgent_Set'),(253,0,'RDKB',55,'CMAgent_SetAttr'),(254,0,'RDKB',38,'CosaCM_GetTelephonyDHCPStatus'),(255,0,'RDKB',55,'CMAgent_SetCommit'),(256,0,'RDKB',55,'CMAgent_SetSessionId'),(258,0,'RDKB',55,'CMAgent_Set_Get'),(259,0,'RDKB',38,'COSACM_GetCMErrorCodewords_InvalidArg'),(260,0,'RDKB',38,'CosaCM_GetTelephonyRegistrationStatus'),(264,0,'RDKB',38,'CosaCM_GetStatus'),(265,0,'RDKB',56,'TR069Agent_GetParameterValues'),(266,0,'RDKB',56,'TR069Agent_SetParameterValues'),(267,0,'RDKB',56,'TR069Agent_Terminate'),(268,0,'RDKB',56,'TR069Agent_Init'),(269,0,'RDKB',56,'TR069Agent_GetParameterNames'),(270,0,'RDKB',56,'TR069Agent_SetParameterAttr'),(271,0,'RDKB',56,'TR069Agent_GetParameterAttr');
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
  `category` varchar(255) NOT NULL,
  `device` varchar(255) DEFAULT NULL,
  `device_group` varchar(255) DEFAULT NULL,
  `end_date` datetime DEFAULT NULL,
  `file_path` varchar(255) NOT NULL,
  `groups_id` bigint(20) DEFAULT NULL,
  `is_bench_mark` varchar(255) DEFAULT NULL,
  `is_stb_log_required` varchar(255) DEFAULT NULL,
  `is_system_diagnostics` varchar(255) DEFAULT NULL,
  `job_name` varchar(255) NOT NULL,
  `one_time_schedule_date` datetime DEFAULT NULL,
  `query_string` varchar(255) DEFAULT NULL,
  `real_path` varchar(255) NOT NULL,
  `repeat_count` int(11) NOT NULL,
  `rerun` varchar(255) DEFAULT NULL,
  `schedule_type` varchar(255) DEFAULT NULL,
  `script_group` varchar(255) DEFAULT NULL,
  `start_date` datetime DEFAULT NULL,
  `trigger_name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `FK3E2527C0984B586A` (`groups_id`),
  CONSTRAINT `FK3E2527C0984B586A` FOREIGN KEY (`groups_id`) REFERENCES `groups` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=latin1;
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
  `category` varchar(255) NOT NULL,
  `execution_time` int(11) NOT NULL,
  `groups_id` bigint(20) DEFAULT NULL,
  `name` varchar(255) NOT NULL,
  `rdk_version` varchar(255) NOT NULL,
  `test_group` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `category` (`category`,`name`),
  KEY `FKC04BA66C984B586A` (`groups_id`),
  CONSTRAINT `FKC04BA66C984B586A` FOREIGN KEY (`groups_id`) REFERENCES `groups` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=57 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `module`
--

LOCK TABLES `module` WRITE;
/*!40000 ALTER TABLE `module` DISABLE KEYS */;
INSERT INTO `module` VALUES (1,0,'RDKV',30,4,'iarmbus','1','Component'),(2,0,'RDKV',0,4,'mediastreamer','1','Component'),(3,0,'RDKV',0,4,'openSource_component','1','OpenSource'),(4,0,'RDKV',0,4,'devicesettings','1','Component'),(5,0,'RDKV',0,4,'servicemanager','1','Component'),(6,0,'RDKV',0,4,'closedcaption','1','Component'),(7,0,'RDKV',0,4,'rmfapp','1','E2E'),(8,0,'RDKV',0,4,'newrmf','1','E2E'),(9,0,'RDKV',0,4,'mediaframework','1','Component'),(10,0,'RDKV',0,4,'rdk_logger','1','Component'),(11,0,'RDKV',0,4,'Xi4Module1','1','Component'),(12,0,'RDKV',0,4,'recorder','1','Component'),(13,0,'RDKV',0,4,'tdk_integration','1','E2E'),(14,0,'RDKV',0,4,'tr69','1','Component'),(15,0,'RDKV',0,4,'gst-plugins-rdk','1','Component'),(16,0,'RDKV',0,4,'trm','1','Component'),(17,0,'RDKV',0,4,'dtcp','1','Component'),(18,0,'RDKV',0,4,'xupnp','1','Component'),(19,0,'RDKB',0,4,'SNMP_PA','1','Component'),(21,0,'RDKB',0,4,'WebPA','1','Component'),(25,0,'RDKB',0,4,'tcl','1','Component'),(26,0,'RDKB',0,4,'WECB','1','Component'),(27,0,'RDKB',0,4,'AdvancedConfig','1','Component'),(38,0,'RDKB',1,4,'CosaCM','1','Component'),(39,0,'RDKB',1,4,'wifi','1','Component'),(41,0,'RDKB',1,4,'MOCA','1','Component'),(42,0,'RDKB',1,4,'CosaWIFI','1','Component'),(45,0,'RDKB',0,4,'ccspcommon_mbus','1','Component'),(51,0,'RDKB',1,4,'MTA_Agent','1','Component'),(54,0,'RDKB',1,4,'WIFIAgent','1','Component'),(55,0,'RDKB',1,4,'CMAgent','1','Component'),(56,0,'RDKB',1,4,'TR069Pa','1','Component');
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
-- Table structure for table `module_stb_log_files`
--

DROP TABLE IF EXISTS `module_stb_log_files`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `module_stb_log_files` (
  `module_id` bigint(20) DEFAULT NULL,
  `stb_log_files_string` varchar(255) DEFAULT NULL,
  KEY `FKB2064C8B9E2CF16A` (`module_id`),
  CONSTRAINT `FKB2064C8B9E2CF16A` FOREIGN KEY (`module_id`) REFERENCES `module` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;


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
  KEY `FK747EB3A9E98C9EFD` (`parameter_type_id`),
  KEY `FK747EB3A98AA44579` (`primitive_test_id`),
  CONSTRAINT `FK747EB3A98AA44579` FOREIGN KEY (`primitive_test_id`) REFERENCES `primitive_test` (`id`),
  CONSTRAINT `FK747EB3A9E98C9EFD` FOREIGN KEY (`parameter_type_id`) REFERENCES `parameter_type` (`id`)
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
  KEY `FK438D76101041DDEA` (`function_id`),
  CONSTRAINT `FK438D76101041DDEA` FOREIGN KEY (`function_id`) REFERENCES `function` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=406 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `parameter_type`
--

LOCK TABLES `parameter_type` WRITE;
/*!40000 ALTER TABLE `parameter_type` DISABLE KEYS */;
INSERT INTO `parameter_type` VALUES (7,0,2,'paramName','STRING','A-Z'),(8,0,3,'paramName','STRING','A-Z'),(9,0,4,'paramName','STRING','A-Z'),(10,0,4,'paramValue','STRING','A-Z'),(11,0,4,'paramType','STRING','A-Z'),(12,0,4,'commit','INTEGER','0-9'),(13,0,5,'commit','INTEGER','0-9'),(14,0,5,'paramType','STRING','A-Z'),(15,0,5,'paramValue','STRING','A-Z'),(16,0,5,'paramName','STRING','A-Z'),(17,0,5,'recursive','INTEGER','0-9'),(18,0,5,'paramList','STRING','A-Z'),(19,0,6,'sessionId','INTEGER','0-9'),(20,0,7,'paramName','STRING','A-Z'),(22,0,10,'paramName','STRING','A-Z'),(25,0,9,'accessControl','STRING','A-Z'),(26,0,9,'notify','STRING','A-Z'),(27,0,9,'paramName','STRING','A-Z'),(28,0,8,'paramName','STRING','A-Z'),(119,0,11,'paramName','STRING','A-Z'),(120,0,12,'paramName','STRING','A-Z'),(121,0,12,'paramType','STRING','A-Z'),(122,0,12,'paramValue','STRING','A-Z'),(123,0,13,'paramType','STRING','A-Z'),(124,0,13,'paramValue','STRING','A-Z'),(125,0,13,'paramName','STRING','A-Z'),(126,0,14,'paramName','STRING','A-Z'),(127,0,15,'SnmpMethod','STRING','A-Z'),(128,0,15,'SnmpCommStr','STRING','A-Z'),(129,0,15,'SnmpIp','STRING','A-Z'),(130,0,15,'SnmpOID','STRING','A-Z'),(131,0,16,'FindStr','STRING','A-Z'),(189,0,101,'handleType','INTEGER','0-9'),(190,0,101,'resetType','STRING','A-Z'),(191,0,102,'handleType','INTEGER','0-9'),(198,0,108,'parmavalue','STRING','A-z'),(200,0,113,'cfgfileName','STRING','a-z A-Z'),(207,0,133,'cfgfileName','STRING','A-Z'),(208,0,134,'cmpCfgFile','STRING','A-Z'),(209,0,135,'xmlfileName','STRING','A-Z'),(210,0,139,'eventName','STRING','A-Z'),(211,0,140,'eventName','STRING','A-Z'),(212,0,143,'cmpId','STRING','A-Z'),(213,0,143,'cmpPath','STRING','A-Z'),(214,0,101,'bufferType','INTEGER','0-9'),(223,0,160,'handleType','INTEGER','0-9'),(224,0,160,'boolValue','INTEGER','0-1'),(225,0,161,'handleType','INTEGER','0-9'),(226,0,161,'bufferType','INTEGER','0-9'),(227,0,162,'handleType','INTEGER','0-9'),(228,0,162,'bufferType','INTEGER','0-9'),(229,0,163,'handleType','INTEGER','0-9'),(230,0,163,'bufferType','INTEGER','0-9'),(231,0,164,'bufferType','INTEGER','0-9'),(232,0,164,'handleType','INTEGER','0-9'),(233,0,165,'handleType','INTEGER','0-9'),(234,0,165,'bufferType','INTEGER','0-9'),(235,0,166,'handleType','INTEGER','0-9'),(247,0,175,'handleType','INTEGER','0-9'),(248,0,175,'boolValue','INTEGER','0-1'),(257,0,176,'handleType','INTEGER','0-9'),(258,0,176,'paramValue','INTEGER','0-9'),(259,0,176,'paramType','STRING','A-Z'),(260,0,177,'handleType','INTEGER','0-9'),(267,0,179,'handleType','INTEGER','0-9'),(268,0,179,'bufferType','INTEGER','0-9'),(269,0,180,'handleType','INTEGER','0-9'),(270,0,180,'bufferType','INTEGER','0-9'),(271,0,181,'handleType','INTEGER','0-9'),(272,0,181,'bufferType','INTEGER','0-9'),(273,0,178,'handleType','INTEGER','0-9'),(274,0,178,'paramValue','INTEGER','0-9'),(275,0,178,'paramType','STRING','A-Z'),(276,0,182,'handleType','INTEGER','0-9'),(277,0,182,'bufferType','INTEGER','0-9'),(278,0,183,'handleType','INTEGER','0-9'),(279,0,183,'bufferType','INTEGER','0-9'),(284,0,190,'Notify','STRING','A-Z'),(285,0,190,'AccessControl','STRING','A-Z'),(286,0,190,'ParamName','STRING','A-Z'),(287,0,191,'Type','STRING','A-Z'),(288,0,191,'ParamValue','STRING','A-Z'),(289,0,191,'ParamName','STRING','A-Z'),(290,0,194,'ParamName','STRING','A-Z'),(291,0,195,'ParamName','STRING','A-Z'),(292,0,195,'ParamList','STRING','A-Z'),(293,0,196,'ParamName','STRING','A-Z'),(294,0,197,'ParamName','STRING','A-Z'),(295,0,197,'ParamValue','STRING','A-Z'),(296,0,197,'Type','STRING','A-Z'),(297,0,198,'ParamName','STRING','A-Z'),(298,0,199,'ParamName','STRING','A-Z'),(299,0,200,'ParamName','STRING','A-Z'),(300,0,201,'ParamName','STRING','A-Z'),(301,0,202,'priority','INTEGER','0-9'),(302,0,202,'sessionId','INTEGER','0-9'),(324,0,217,'paramName','STRING','A-Z'),(325,0,218,'paramName','STRING','A-Z'),(326,0,219,'apiTest','STRING','0-1'),(327,0,219,'paramName','STRING','A-Z'),(328,0,220,'paramname','STRING','A-Z'),(329,0,221,'override','INTEGER','0-1'),(330,0,221,'sessionId','INTEGER','0-1'),(331,0,221,'pathname','STRING','a-z,A-Z'),(332,0,221,'priority','INTEGER','0-1'),(333,0,222,'paramType','STRING','a-z,A-Z'),(334,0,222,'paramName','STRING','a-z,A-Z'),(335,0,222,'paramValue','STRING','a-z,A-Z'),(336,0,223,'paramName','STRING','a-z,A-Z'),(337,0,224,'accessControlChanged','STRING','a-z,A-Z'),(338,0,224,'paramname','STRING','a-z,A-Z'),(339,0,224,'notification','STRING','a-z,A-Z'),(340,0,225,'pathname','STRING','a-z,A-Z'),(341,0,225,'brecursive','INTEGER','0-1'),(342,0,226,'paramName','STRING','a-z,A-Z'),(343,0,227,'paramType','STRING','a-z,A-Z'),(344,0,227,'paramValue','STRING','a-z,A-Z'),(345,0,227,'paramName','STRING','a-z,A-Z'),(346,0,238,'handleType','INTEGER','0-1'),(347,0,236,'handleType','INTEGER','0-1'),(348,0,243,'valueType','INTEGER','0-9'),(349,0,243,'handleType','INTEGER','0-9'),(350,0,244,'handleType','INTEGER','0-9'),(351,0,244,'Value','INTEGER','0-9'),(353,0,247,'paramName','STRING','A-Z'),(354,0,248,'paramName','STRING','A-Z'),(355,0,248,'apiTest','INTEGER','0-1'),(356,0,249,'paramname','STRING','A-Z'),(357,0,250,'pathname','STRING','A-Z'),(358,0,250,'brecursive','INTEGER','0-1'),(359,0,251,'paramName','STRING','A-Z'),(360,0,252,'paramValue','STRING','A-Z'),(361,0,252,'commit','INTEGER','0-9'),(362,0,252,'paramName','STRING','A-Z'),(363,0,252,'paramType','STRING','A-Z'),(364,0,253,'paramname','STRING','A-Z'),(365,0,253,'accessControlChanged','STRING','A-Z'),(366,0,253,'notification','STRING','A-Z'),(368,0,255,'paramName','STRING','A-Z'),(370,0,256,'priority','INTEGER','0-1'),(371,0,256,'override','INTEGER','0-1'),(372,0,256,'sessionId','INTEGER','0-1'),(373,0,256,'pathname','STRING','A-Z'),(374,0,258,'paramValue','STRING','A-Z'),(375,0,258,'paramName','STRING','A-Z'),(376,0,258,'paramType','STRING','A-Z'),(377,0,258,'commit','INTEGER','0-9'),(378,0,254,'handleType','INTEGER','0-9'),(380,0,246,'paramName','STRING','A-Z'),(381,0,254,'Value','INTEGER','0-9'),(385,0,260,'handleType','INTEGER','0-9'),(386,0,260,'bufferType','INTEGER','0-9'),(394,0,264,'handleType','INTEGER','0-9'),(395,0,264,'Value','STRING','0-9'),(396,0,265,'ParamName','STRING','A-Z'),(397,0,266,'Type','STRING','A-Z'),(398,0,266,'ParamValue','STRING','A-Z'),(399,0,266,'ParamName','STRING','A-Z'),(400,0,269,'ParamName','STRING','A-Z'),(401,0,269,'ParamList','STRING','A-Z'),(402,0,270,'ParamName','STRING','A-Z'),(403,0,270,'Notify','STRING','A-Z'),(404,0,270,'AccessControl','STRING','A-Z'),(405,0,271,'ParamName','STRING','A-Z');
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
  `category` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `FKA7C310309FCEDC3B` (`execution_result_id`),
  CONSTRAINT `FKA7C310309FCEDC3B` FOREIGN KEY (`execution_result_id`) REFERENCES `execution_result` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
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
  `groups_id` bigint(20) DEFAULT NULL,
  `module_id` bigint(20) NOT NULL,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `FKA504E8EA984B586A` (`groups_id`),
  KEY `FKA504E8EA9E2CF16A` (`module_id`),
  KEY `FKA504E8EA1041DDEA` (`function_id`),
  CONSTRAINT `FKA504E8EA1041DDEA` FOREIGN KEY (`function_id`) REFERENCES `function` (`id`),
  CONSTRAINT `FKA504E8EA984B586A` FOREIGN KEY (`groups_id`) REFERENCES `groups` (`id`),
  CONSTRAINT `FKA504E8EA9E2CF16A` FOREIGN KEY (`module_id`) REFERENCES `module` (`id`)
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
-- Table structure for table `rdkversions`
--

DROP TABLE IF EXISTS `rdkversions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rdkversions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `version` bigint(20) NOT NULL,
  `build_version` varchar(255) NOT NULL,
  `category` varchar(255) NOT NULL,
  `groups_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `build_version` (`build_version`),
  KEY `FK3CD0AE14984B586A` (`groups_id`),
  CONSTRAINT `FK3CD0AE14984B586A` FOREIGN KEY (`groups_id`) REFERENCES `groups` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rdkversions`
--

LOCK TABLES `rdkversions` WRITE;
/*!40000 ALTER TABLE `rdkversions` DISABLE KEYS */;
INSERT INTO `rdkversions` VALUES (1,0,'1.2','RDKV',4),(2,0,'1.3','RDKV',4),(3,0,'RDK2.0','RDKV',4),(4,0,'2.0','RDKV',4),(5,0,'2.1','RDKV',4),(6,0,'1','RDKV',4),(8,0,'RDKB','RDKB',4),(9,0,'RDK3','RDKB',4);
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
  `category` varchar(255) NOT NULL,
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
INSERT INTO `role` VALUES (1,1,'ADMIN'),(2,0,'TESTER');
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
INSERT INTO `role_permissions` VALUES (1,'*:*'),(2,'Execution:*:*'),(2,'Trends:*:*'),(2,'ScriptGroup:*:*'),(2,'DeviceGroup:*:*');
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
  `execution_time` int(11) NOT NULL,
  `groups_id` bigint(20) DEFAULT NULL,
  `long_duration` bit(1) NOT NULL,
  `name` varchar(255) NOT NULL,
  `primitive_test_id` bigint(20) NOT NULL,
  `remarks` varchar(255) NOT NULL,
  `script_content` longtext NOT NULL,
  `skip` bit(1) NOT NULL,
  `status` varchar(255) DEFAULT NULL,
  `synopsis` longtext,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `FKC9E5D0CB984B586A` (`groups_id`),
  KEY `FKC9E5D0CB8AA44579` (`primitive_test_id`),
  CONSTRAINT `FKC9E5D0CB8AA44579` FOREIGN KEY (`primitive_test_id`) REFERENCES `primitive_test` (`id`),
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
  KEY `FK7583C622E88F9584` (`script_box_types_id`),
  KEY `FK7583C622DB9F6C41` (`box_type_id`),
  CONSTRAINT `FK7583C622DB9F6C41` FOREIGN KEY (`box_type_id`) REFERENCES `box_type` (`id`),
  CONSTRAINT `FK7583C622E88F9584` FOREIGN KEY (`script_box_types_id`) REFERENCES `script` (`id`)
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
  `category` varchar(255) NOT NULL,
  `module_name` longtext,
  `script_name` longtext NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16619 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `script_file`
--

LOCK TABLES `script_file` WRITE;
/*!40000 ALTER TABLE `script_file` DISABLE KEYS */;
INSERT INTO `script_file` VALUES (10935,0,'RDKB','SNMP_PA','TS_SNMP_CheckDHCPserverConfigurable'),(10936,0,'RDKB','SNMP_PA','TS_SNMP_CheckBackwardCompatibilityWithSnmpV1'),(10937,0,'RDKB','SNMP_PA','TS_SNMP_WecbNetworkExtender'),(10938,0,'RDKB','SNMP_PA','TS_SNMP_V2cSETandGETWithValidCommunityString'),(10939,0,'RDKB','SNMP_PA','TS_SNMP_DeviceResetDefaultEnable'),(10940,0,'RDKB','SNMP_PA','TS_SNMP_RebootDUT'),(10941,0,'RDKB','SNMP_PA','TS_SNMP_MocaDeviceBase'),(10942,0,'RDKB','SNMP_PA','TS_SNMP_V2cSETandGETWithNoCommunityString'),(10943,0,'RDKB','SNMP_PA','TS_SNMP_RestoreFactorySettings'),(10944,0,'RDKB','SNMP_PA','TS_SNMP_WalkInvalidOID'),(10945,0,'RDKB','SNMP_PA','TS_SNMP_FirewallToDefault'),(10946,0,'RDKB','SNMP_PA','TS_SNMP_RemoteWebAccessPort'),(10947,0,'RDKB','SNMP_PA','TS_SNMP_ChangeValueOfReadOnlyOID'),(10948,0,'RDKB','SNMP_PA','TS_SNMP_V2cSETandGETWithInvalidCommunityString'),(10949,0,'RDKB','SNMP_PA','TS_SNMP_WalkValidOID'),(10950,0,'RDKB','SNMP_PA','TS_SNMP_CheckWiFiHotspotConnectedClients'),(10951,0,'RDKB','SNMP_PA','TS_SNMP_RemoteWebAccessEnable'),(10952,0,'RDKB','SNMP_PA','TS_SNMP_TR069Client'),(10953,0,'RDKB','WECB','TS_WECB_Set_Disconnect_MocaClient'),(10954,0,'RDKB','WECB','TS_WECB_MOCA_Privacy_Enable_Disable'),(10955,0,'RDKB','WECB','TS_WECB_GetParamNames'),(10956,0,'RDKB','WECB','TS_WECB_GetParamValues_EmptyString'),(10957,0,'RDKB','WECB','TS_WECB_SetParamValue_WithChangeIn_SessionId'),(10958,0,'RDKB','WECB','TS_WECB_Set_SSID_Update'),(10959,0,'RDKB','WECB','TS_WECB_Set_BeaconPowerLevel'),(10960,0,'RDKB','WECB','TS_WECB_AddObject_ReadOnlyTable'),(10961,0,'RDKB','WECB','TS_WECB_SetParamAttribute'),(10962,0,'RDKB','WECB','TS_WECB_GetParamValues'),(10963,0,'RDKB','WECB','TS_WECB_SetCommit_WithNoChange'),(10964,0,'RDKB','WECB','TS_WECB_DelObject_ReadOnlyTable'),(10965,0,'RDKB','WECB','TS_WECB_MOCA_Enable_Disable'),(10966,0,'RDKB','WECB','TS_WECB_SetCommit'),(10967,0,'RDKB','WECB','TS_WECB_Set_Radio_Update'),(10968,0,'RDKB','WECB','TS_WECB_MOCA_PreferredNC_Enable_Disable'),(10969,0,'RDKB','WECB','TS_WECB_GetParamAttributes'),(10970,0,'RDKB','WebPA','TS_WEBPA_ValidateLoginCredentials'),(10971,0,'RDKB','WebPA','TS_WEBPA_PTAddEditDeleteARule'),(10972,0,'RDKB','WebPA','TS_WEBPA_AddPTService'),(10973,0,'RDKB','WebPA','TS_WEBPA_DHCPBeginIpError'),(10974,0,'RDKB','WebPA','TS_WEBPADuplicatePTService'),(10975,0,'RDKB','WebPA','TS_WEBPA_PTInvalidPortRange'),(10976,0,'RDKB','WebPA','TS_WEBPA_PTDisabledEditRule'),(10977,0,'RDKB','WebPA','TS_WEBPA_ReservedIPError'),(10978,0,'RDKB','WebPA','TS_WEBPA_AddPTRuleWithoutServiceName'),(10979,0,'RDKB','WebPA','TS_WEBPA_PTDisabledDeleteRule'),(10980,0,'RDKB','AdvancedConfig','TS_ADVANCEDCONFIG_PFServiceName'),(10981,0,'RDKB','AdvancedConfig','TS_ADVANCEDCONFIG_PFDisable'),(10982,0,'RDKB','AdvancedConfig','TS_ADVANCEDCONFIG_PortTriggeringRuleWithSpaceAndBlank'),(10983,0,'RDKB','AdvancedConfig','TS_ADVANCEDCONFIG_PTDisable'),(10984,0,'RDKB','AdvancedConfig','TS_ADVANCEDCONFIG_DuplicatePortTriggeringRulesNotAllowed'),(10985,0,'RDKB','AdvancedConfig','TS_ADVANCEDCONFIG_PFRuleSpaceBlank'),(10986,0,'RDKB','AdvancedConfig','TS_ADVANCEDCONFIG_CheckAddAndDeleteRuleOfPortTriggering'),(10987,0,'RDKB','AdvancedConfig','TS_ADVANCEDCONFIG_PFDuplicateRule'),(10988,0,'RDKB','AdvancedConfig','TS_ADVANCEDCONFIG_PFCreateEditDelete'),(10989,0,'RDKB','AdvancedConfig','TS_ADVANCEDCONFIG_RemoteManagementEnable'),(10990,0,'RDKB','AdvancedConfig','TS_ADVANCEDCONFIG_SSHEnable'),(10991,0,'RDKB','AdvancedConfig','TS_ADVANCEDCONFIG_DMZmodeEnable'),(10992,0,'RDKB','AdvancedConfig','TS_ADVANCEDCONFIG_PTServiceName'),(10993,0,'RDKB','AdvancedConfig','TS_ADVANCEDCONFIG_DMZHostIPRange'),(10994,0,'RDKB','AdvancedConfig','TS_ADVANCEDCONFIG_TelnetEnable'),(10995,0,'RDKB','AdvancedConfig','TS_ADVANCEDCONFIG_PFDisabledAddRule'),(10996,0,'RDKB','AdvancedConfig','TS_ADVANCEDCONFIG_RemoteMgmt_AnyComputer'),(10997,0,'RDKB','AdvancedConfig','TS_ADVANCEDCONFIG_DMZHostAsGatewayIP'),(10998,0,'RDKB','AdvancedConfig','TS_ADVANCEDCONFIG_CheckAddRuleOptionsOfPortTriggering'),(10999,0,'RDKB','AdvancedConfig','TS_ADVANCEDCONFIG_PFAddRuleOptions'),(11001,0,'RDKB','CMAgent','TS_CMAGENT_SetParamValues'),(11002,0,'RDKB','CMAgent','TS_CMAGENT_GetParamValues'),(11003,0,'RDKB','CMAgent','TS_CMAGENT_ToDStatus'),(11004,0,'RDKB','CMAgent','TS_CMAGENT_SetAttributes'),(11005,0,'RDKB','CMAgent','TS_CMAGENT_EnableLog'),(11006,0,'RDKB','CMAgent','TS_CMAGENT_DOCSISVersion'),(11007,0,'RDKB','CMAgent','TS_CMAGENT_SetSessionId'),(11008,0,'RDKB','CMAgent','TS_CMAGENT_BPIState'),(11009,0,'RDKB','CMAgent','TS_CMAGENT_AddObject'),(11010,0,'RDKB','CMAgent','TS_CMAGENT_CMStatus'),(11011,0,'RDKB','CMAgent','TS_CMAGENT_CoreVersion'),(11012,0,'RDKB','CMAgent','TS_CMAGENT_DOCSISDHCPStatus'),(11013,0,'RDKB','CMAgent','TS_CMAGENT_DelObject'),(11014,0,'RDKB','CMAgent','TS_CMAGENT_GetParamNames'),(11015,0,'RDKB','CMAgent','TS_CMAGENT_GetAttributes'),(11016,0,'RDKB','CMAgent','TS_CMAGENT_NetworkAccess'),(11017,0,'RDKB','CMAgent','TS_CMAgent_GetHealth'),(11018,0,'RDKB','CMAgent','TS_CMAGENT_MDDIPOverride'),(11019,0,'RDKB','CMAgent','TS_CMAGENT_SetCommit'),(11020,0,'RDKB','CMAgent','TS_CMAGENT_MaxCpeAllowed'),(11036,0,'RDKB','WIFIAgent','TS_WIFIAGENT_GetParamNames'),(11037,0,'RDKB','WIFIAgent','TS_WIFIAGENT_SetCommit'),(11038,0,'RDKB','WIFIAgent','TS_WIFIAGENT_GetHealth'),(11039,0,'RDKB','WIFIAgent','TS_WIFIAGENT_EnableUAPSD'),(11040,0,'RDKB','WIFIAgent','TS_WIFIAGENT_DelObject'),(11041,0,'RDKB','WIFIAgent','TS_WIFIAGENT_GetValuesOfWMMCapabilitANdUAPSDCapability'),(11042,0,'RDKB','WIFIAgent','TS_WIFIAGENT_GetNumberOfEntries'),(11043,0,'RDKB','WIFIAgent','TS_WIFIAGENT_SetSessionId'),(11044,0,'RDKB','WIFIAgent','TS_WIFIAGENT_SetParamValues'),(11045,0,'RDKB','WIFIAgent','TS_WIFIAGENT_SetAttributes'),(11046,0,'RDKB','WIFIAgent','TS_WIFIAGENT_EnableWMM'),(11047,0,'RDKB','WIFIAgent','TS_WIFIAGENT_EnableAccessPoint'),(11048,0,'RDKB','WIFIAgent','TS_WIFIAGENT_FactoryReset'),(11049,0,'RDKB','WIFIAgent','TS_WIFIAGENT_EnableAccessPointSSIDAdvertisement'),(11050,0,'RDKB','WIFIAgent','TS_WIFIAGENT_AddObject'),(11051,0,'RDKB','WIFIAgent','TS_WIFIAGENT_EnableBssHotSpot'),(11052,0,'RDKB','WIFIAgent','TS_WIFIAGENT_GetAttributes'),(11053,0,'RDKB','WIFIAgent','TS_WIFIAGENT_GetParamValues'),(11054,0,'RDKB','WIFIAgent','TS_WIFIAGENT_EnableSecurityMode'),(11055,0,'RDKB','WIFIAgent','TS_WIFIAGENT_AccessPointRetryLimit'),(13400,0,'RDKB','AdvancedConfig','TS_ADVANCEDCONFIG_RuleforHTTPDownloadWithInvalidIPAddress10.1.10.255'),(13401,0,'RDKB','AdvancedConfig','TS_ADVANCEDCONFIG_HNSValidationForPortNumbers'),(13402,0,'RDKB','AdvancedConfig','TS_ADVANCEDCONFIG_RuleforHTTPDownloadWithInvalidIPAddress10.1.10.0'),(13403,0,'RDKB','AdvancedConfig','TS_ADVANCEDCONFIG_RuleforHTTPDownloadWithInvalidIPAddress10.1.10.256'),(13404,0,'RDKB','AdvancedConfig','TS_ADVANCEDCONFIG_RuleforHTTPDownloadWithInvalidIPAddress10.0.0.1'),(13871,0,'RDKB','ccspcommon_mbus','TS_CCSPCOMMON_MBUS_Init'),(13872,0,'RDKB','ccspcommon_mbus','TS_CCSPCOMMON_MBUS_LoadCfg'),(13873,0,'RDKB','ccspcommon_mbus','TS_CCSPCOMMON_MBUS_InvalidLoadCfg'),(13874,0,'RDKB','ccspcommon_mbus','TS_CCSPCOMMON_MBUS_LoadDmXml'),(13875,0,'RDKB','ccspcommon_mbus','TS_CCSPCOMMON_MBUS_InvalidLoadDmXml'),(13876,0,'RDKB','ccspcommon_mbus','TS_CCSPCOMMON_MBUS_Exit'),(13877,0,'RDKB','ccspcommon_mbus','TS_CCSPCOMMON_MBUS_RegisterEvent'),(13878,0,'RDKB','ccspcommon_mbus','TS_CCSPCOMMON_MBUS_UnRegisterEvent'),(13879,0,'RDKB','ccspcommon_mbus','TS_CCSPCOMMON_MBUS_GetRegisteredComponents'),(13880,0,'RDKB','ccspcommon_mbus','TS_CCSPCOMMON_MBUS_IsSystemReady'),(13881,0,'RDKB','ccspcommon_mbus','TS_CCSPCOMMON_MBUS_GetHealth'),(13960,0,'RDKB','ccspcommon_mbus','TS_CCSPCOMMON_MBUS_SendSignal'),(14046,0,'RDKB_TCL','tcl','TC_ERTR_0002'),(14050,0,'RDKB_TCL','tcl','TC_ERTR_0042'),(14075,0,'RDKB_TCL','tcl','TC_ERTR_0033'),(14085,0,'RDKB_TCL','tcl','TC_ERTR_0039'),(14091,0,'RDKB_TCL','tcl','TC_ERTR_0032'),(14095,0,'RDKB_TCL','tcl','TC_ERTR_0040'),(14114,0,'RDKB_TCL','tcl','TC_ERTR_0016'),(14323,1,'RDKB','CosaCM','TS_CosaCM_GetCMResetCount'),(14324,1,'RDKB','CosaCM','TS_CosaCM_GetLocalResetCount'),(14325,1,'RDKB','CosaCM','TS_CosaCM_GetDocsisResetCount'),(14326,1,'RDKB','CosaCM','TS_CosaCM_GetErouterResetCount'),(14327,1,'RDKB','CosaCM','TS_CosaCM_GetResetCount_InvalidResetType'),(14329,1,'RDKB','CosaCM','TS_COSACM_GetUpstreamChannel'),(14330,1,'RDKB','CosaCM','TS_COSACM_GetDownstreamChannel'),(14331,1,'RDKB','CosaCM','TS_COSACM_GetDocsisLog'),(14973,0,'RDKB_TCL','tcl','TC_ERTR_0044'),(14974,0,'RDKB_TCL','tcl','TC_ERTR_0023'),(14975,0,'RDKB_TCL','tcl','TC_ERTR_0003'),(14976,0,'RDKB_TCL','tcl','TC_ERTR_0046'),(14977,0,'RDKB_TCL','tcl','TC_ERTR_0010'),(14978,0,'RDKB_TCL','tcl','TC_ERTR_0056'),(14979,0,'RDKB_TCL','tcl','TC_ERTR_0053'),(14980,0,'RDKB_TCL','tcl','TC_ERTR_0006'),(14981,0,'RDKB_TCL','tcl','TC_ERTR_0007'),(14982,0,'RDKB_TCL','tcl','TC_ERTR_0027'),(14983,0,'RDKB_TCL','tcl','TC_ERTR_0017'),(14984,0,'RDKB_TCL','tcl','TC_ERTR_0028'),(14985,0,'RDKB_TCL','tcl','TC_ERTR_0074'),(14986,0,'RDKB_TCL','tcl','TC_ERTR_0013'),(14987,0,'RDKB_TCL','tcl','TC_ERTR_0001'),(14988,0,'RDKB_TCL','tcl','TC_ERTR_0008'),(14989,0,'RDKB_TCL','tcl','TC_ERTR_0057'),(14990,0,'RDKB_TCL','tcl','TC_ERTR_0062'),(14991,0,'RDKB_TCL','tcl','TC_ERTR_0070'),(14992,0,'RDKB_TCL','tcl','TC_ERTR_0073'),(14993,0,'RDKB_TCL','tcl','TC_ERTR_0020'),(14994,0,'RDKB_TCL','tcl','TC_ERTR_0063'),(14995,0,'RDKB_TCL','tcl','TC_ERTR_0047'),(14996,0,'RDKB_TCL','tcl','TC_ERTR_0035'),(14997,0,'RDKB_TCL','tcl','TC_ERTR_0065'),(14998,0,'RDKB_TCL','tcl','TC_ERTR_0052'),(14999,0,'RDKB_TCL','tcl','TC_ERTR_0045'),(15000,0,'RDKB_TCL','tcl','TC_ERTR_0029'),(15001,0,'RDKB_TCL','tcl','TC_ERTR_0012'),(15002,0,'RDKB_TCL','tcl','TC_ERTR_0024'),(15003,0,'RDKB_TCL','tcl','TC_ERTR_0071'),(15004,0,'RDKB_TCL','tcl','TC_ERTR_0048'),(15005,0,'RDKB_TCL','tcl','TC_ERTR_0021'),(15006,0,'RDKB_TCL','tcl','TC_ERTR_0072'),(15007,0,'RDKB_TCL','tcl','TC_ERTR_0067'),(15008,0,'RDKB_TCL','tcl','TC_ERTR_0054'),(15009,0,'RDKB_TCL','tcl','TC_ERTR_0022'),(15010,0,'RDKB_TCL','tcl','TC_ERTR_0068'),(15011,0,'RDKB_TCL','tcl','TC_ERTR_0059'),(15012,0,'RDKB_TCL','tcl','TC_ERTR_0061'),(15013,0,'RDKB_TCL','tcl','TC_ERTR_0050'),(15014,0,'RDKB_TCL','tcl','TC_ERTR_0064'),(15015,0,'RDKB_TCL','tcl','TC_ERTR_0015'),(15016,0,'RDKB_TCL','tcl','TC_ERTR_0049'),(15017,0,'RDKB_TCL','tcl','TC_ERTR_0026'),(15018,0,'RDKB_TCL','tcl','TC_ERTR_0018'),(15019,0,'RDKB_TCL','tcl','TC_ERTR_0014'),(15020,0,'RDKB_TCL','tcl','TC_ERTR_0043'),(15021,0,'RDKB_TCL','tcl','TC_ERTR_0011'),(15022,0,'RDKB_TCL','tcl','TC_ERTR_0060'),(15023,0,'RDKB_TCL','tcl','TC_ERTR_0034'),(15025,0,'RDKB_TCL','tcl','TC_ERTR_0051'),(15027,0,'RDKB_TCL','tcl','TC_ERTR_0055'),(15028,0,'RDKB_TCL','tcl','TC_ERTR_0058'),(15029,0,'RDKB_TCL','tcl','TC_ERTR_0037'),(15030,0,'RDKB_TCL','tcl','TC_ERTR_0019'),(15031,0,'RDKB_TCL','tcl','TC_ERTR_0069'),(15032,0,'RDKB_TCL','tcl','TC_ERTR_0066'),(15033,0,'RDKB_TCL','tcl','TC_ERTR_0036'),(15034,0,'RDKB_TCL','tcl','TC_ERTR_0004'),(15035,0,'RDKB_TCL','tcl','TC_ERTR_0041'),(15036,0,'RDKB_TCL','tcl','TC_ERTR_0030'),(15037,0,'RDKB_TCL','tcl','TC_ERTR_0075'),(15038,0,'RDKB_TCL','tcl','TC_ERTR_0031'),(15039,0,'RDKB_TCL','tcl','TC_ERTR_0038'),(15040,0,'RDKB_TCL','tcl','TC_ERTR_0025'),(15041,0,'RDKB_TCL','tcl','TC_ERTR_0009'),(15042,0,'RDKB_TCL','tcl','TC_ERTR_0005'),(15043,0,'RDKB','ccspcommon_mbus','TS_CCSPCOMMON_MBUS_BusCheck'),(15044,0,'RDKB','ccspcommon_mbus','TS_CCSPCOMMON_MBUS_CheckNamespaceDataType'),(15045,0,'RDKB','ccspcommon_mbus','TS_CCSPCOMMON_MBUS_DiskComponentSupportingDynamicTbl'),(15046,0,'RDKB','ccspcommon_mbus','TS_CCSPCOMMON_MBUS_DiskNamespaceSupportedByComponent'),(15047,0,'RDKB','ccspcommon_mbus','TS_CCSPCOMMON_MBUS_DumpComponentRegistry'),(15048,0,'RDKB','ccspcommon_mbus','TS_CCSPCOMMON_MBUS_GetAllocMemory'),(15049,0,'RDKB','ccspcommon_mbus','TS_CCSPCOMMON_MBUS_GetMaxMemory'),(15050,0,'RDKB','ccspcommon_mbus','TS_CCSPCOMMON_MBUS_InformEndOfSession'),(15051,0,'RDKB','ccspcommon_mbus','TS_CCSPCOMMON_MBUS_QueryStatus'),(15052,0,'RDKB','ccspcommon_mbus','TS_CCSPCOMMON_MBUS_RegisterBase'),(15053,0,'RDKB','ccspcommon_mbus','TS_CCSPCOMMON_MBUS_RegisterCapability'),(15054,0,'RDKB','ccspcommon_mbus','TS_CCSPCOMMON_MBUS_RegisterPath'),(15055,0,'RDKB','ccspcommon_mbus','TS_CCSPCOMMON_MBUS_ReqSessionId'),(15056,0,'RDKB','ccspcommon_mbus','TS_CCSPCOMMON_MBUS_UnRegisterComponent'),(15057,0,'RDKB','ccspcommon_mbus','TS_CCSPCOMMON_MBUS_UnRegisterNamespace'),(15058,0,'RDKB','CosaCM','TS_CosaCM_GetCMResetCount_WithInvalidBuffer'),(15059,0,'RDKB','CosaCM','TS_CosaCM_GetDocsisResetCount_WithInvalidBuffer'),(15060,0,'RDKB','CosaCM','TS_CosaCM_GetLocalResetCount_WithInvalidBuffer'),(15061,0,'RDKB','CosaCM','TS_CosaCM_GetErouterResetCount_WithInvalidBuffer'),(15062,0,'RDKB','CosaCM','TS_COSACM_GetStatus'),(15063,0,'RDKB','CosaCM','TS_COSACM_GetStatus_NegArg'),(15064,0,'RDKB','CosaCM','TS_COSACM_GetLoopDiagnosticsStart'),(15065,0,'RDKB','CosaCM','TS_COSACM_GetLoopDiagnosticsDetails'),(15066,0,'RDKB','CosaCM','TS_COSACM_GetLoopDiagnosticsDetails_NegArg'),(15067,0,'RDKB','CosaCM','TS_COSACM_GetLoopDiagnosticsStart_NegArg'),(15068,0,'RDKB','CosaCM','TS_COSACM_GetDHCPInfo'),(15069,0,'RDKB','CosaCM','TS_COSACM_GetDHCPInfoNegativeArg'),(15070,0,'RDKB','CosaCM','TS_COSACM_GetDOCSISInfo'),(15071,0,'RDKB','CosaCM','TS_COSACM_GetDOCSISInfoNegativeArg'),(15072,0,'RDKB','CosaCM','TS_COSACM_GetLog'),(15073,0,'RDKB','CosaCM','TS_COSACM_GetLogNegativeArg'),(15074,0,'RDKB','CosaCM','TS_COSACM_SetLog'),(15075,0,'RDKB','CosaCM','TS_COSACM_SetLogNegativeArg'),(15078,0,'RDKB','CosaCM','TS_COSACM_GetTelephonyDHCPStatus'),(15079,0,'RDKB','CosaCM','TS_COSACM_GetTelephonyTftpStatus'),(15080,0,'RDKB','CosaCM','TS_COSACM_GetTelephonyRegistrationStatus'),(15081,0,'RDKB','CosaCM','TS_COSACM_GetTelephonyDHCPStatus_NegArg'),(15082,0,'RDKB','CosaCM','TS_COSACM_GetTelephonyTftpStatus_NegArg'),(15083,0,'RDKB','CosaCM','TS_COSACM_GetTelephonyRegistrationStatus_NegArg'),(15084,0,'RDKB','CosaCM','TS_COSACM_SetLoopDiagnosticsStart'),(15085,0,'RDKB','CosaCM','TS_COSACM_SetLoopDiagnosticsStart_NegArg'),(15086,0,'RDKB','CosaCM','TS_COSACM_GetDocsisLogNegativeArg'),(15087,0,'RDKB','CosaCM','TS_COSACM_GetDownstreamChannelNegativeArg'),(15088,0,'RDKB','CosaCM','TS_COSACM_GetUpstreamChannelNegativeArg'),(15089,0,'RDKB','CosaCM','TS_CosaCM_SetUpstreamChannelId'),(15090,0,'RDKB','CosaCM','TS_CosaCM_GetStartDSFrequency'),(15091,0,'RDKB','CosaCM','TS_CosaCM_SetStartDSFrequency'),(15092,0,'RDKB','CosaCM','TS_CosaCM_GetProvType'),(15093,0,'RDKB','CosaCM','TS_CosaCM_GetProvType_WithInvalidBuffer'),(15094,0,'RDKB','CosaCM','TS_CosaCM_GetIPv6DHCPInfo_WithInvalidBuffer'),(15095,0,'RDKB','CosaCM','TS_CosaCM_GetIPv6DHCPInfo'),(16560,0,'RDKB','MTA_Agent','TS_MTAAGENT_AddObj_ReadOnlyTbl'),(16561,0,'RDKB','MTA_Agent','TS_MTAAgent_SetParamAttr'),(16562,0,'RDKB','MTA_Agent','TS_MTAAGENT_GetParamValues'),(16563,0,'RDKB','MTA_Agent','TS_MTAAGENT_SetValues_Dect_Data'),(16564,0,'RDKB','MTA_Agent','TS_MTAAGENT_DelObj_ReadOnlyTbl'),(16565,0,'RDKB','MTA_Agent','TS_MTAAGENT_GetParamNames_NextLevel'),(16566,0,'RDKB','MTA_Agent','TS_MTAAGENT_SetValues_with_SetAttr'),(16567,0,'RDKB','MTA_Agent','TS_MTAAGENT_GetHealth'),(16568,0,'RDKB','MTA_Agent','TS_MTAAGENT_SetCommit'),(16569,0,'RDKB','MTA_Agent','TS_MTAAGENT_GetParamAttr'),(16570,0,'RDKB','MTA_Agent','TS_MTAAGENT_SetSessionId'),(16571,0,'RDKB','MTA_Agent','TS_MTAAGENT_GetParamValues_NoParam'),(16572,0,'RDKB','MTA_Agent','TS_MTAAGENT_GetParamName'),(16573,0,'RDKB','MTA_Agent','TS_MTAAGENT_SetAttr_RootDevice'),(16574,0,'RDKB','MTA_Agent','TS_MTAAGENT_SetParamValues'),(16581,0,'RDKB','ccspcommon_mbus','TS_CCSPCOMMON_MBUS_SendSystemReadySignal'),(16582,0,'RDKB','CosaCM','TS_COSACM_GetMarket'),(16583,0,'RDKB','CosaCM','TS_COSACM_SetMDDIPOverride_ArgMemory_unalloc'),(16584,0,'RDKB','CosaCM','TS_COSACM_GetCMCert'),(16585,0,'RDKB','CosaCM','TS_COSACM_CableModemInitialize'),(16586,0,'RDKB','CosaCM','TS_COSACM_SetMDDIPOverride'),(16587,0,'RDKB','CosaCM','TS_COSACM_GetMDDIPOverride'),(16588,0,'RDKB','CosaCM','TS_COSACM_CableModemCreate'),(16589,0,'RDKB','CosaCM','TS_COSACM_GetCMCertStatus_InvalidArg'),(16590,0,'RDKB','CosaCM','TS_COSACM_CableModemIntialize_NULL_Handle'),(16591,0,'RDKB','CosaCM','TS_COSACM_GetCMCertStatus'),(16592,0,'RDKB','CosaCM','TS_COSACM_GetMDDIPOverride_ArgMemory_unalloc'),(16593,0,'RDKB','CosaCM','TS_COSACM_CableModemRemove'),(16594,0,'RDKB','CosaCM','TS_COSACM_GetCMCert_ArgMemory_unalloc'),(16595,0,'RDKB','CosaCM','TS_COSACM_CableModemRemove_NULL_Handle'),(16596,0,'RDKB','CosaCM','TS_COSACM_GetCMErrorCodewords_InvalidArg'),(16597,0,'RDKB','CosaCM','TS_COSACM_GetCPEList'),(16598,0,'RDKB','CosaCM','TS_COSACM_GetMarket_ArgMemory_unalloc'),(16599,0,'RDKB','CosaCM','TS_COSACM_GetCPEList_InvalidArg'),(16600,0,'RDKB','CosaCM','TS_COSACM_GetCMErrorCodewords'),(16612,0,'RDKB','TR069Pa','TS_TR069PA_Enable_CWMP'),(16613,0,'RDKB','TR069Pa','TS_TR069PA_GetParam_Names'),(16614,0,'RDKB','TR069Pa','TS_TR069PA_GetParam_Attributes'),(16615,0,'RDKB','TR069Pa','TS_TR069PA_GetParam_Values'),(16616,0,'RDKB','TR069Pa','TS_TR069PA_SetParam_Attributes'),(16617,0,'RDKB','TR069Pa','TS_TR069PA_SetParam_Values');
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
  `category` varchar(255) NOT NULL,
  `groups_id` bigint(20) DEFAULT NULL,
  `name` varchar(255) NOT NULL,
  `status` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `FKB4D8260B984B586A` (`groups_id`),
  CONSTRAINT `FKB4D8260B984B586A` FOREIGN KEY (`groups_id`) REFERENCES `groups` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=166 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `script_group`
--

LOCK TABLES `script_group` WRITE;
/*!40000 ALTER TABLE `script_group` DISABLE KEYS */;
INSERT INTO `script_group` VALUES (116,17,'RDKB',NULL,'SNMP_PA','FREE'),(117,703,'RDKB',NULL,'RDKB_Hybrid-1','FREE'),(118,703,'RDKB',NULL,'RDKB_Hybrid-1_NO_OS','FREE'),(119,270,'RDKB',NULL,'ComponentSuite','FREE'),(120,292,'RDKB',NULL,'Hybrid-1Suite','FREE'),(121,16,'RDKB',NULL,'WECB','FREE'),(122,9,'RDKB',NULL,'WebPA','FREE'),(123,30,'RDKB',NULL,'AdvancedConfig','FREE'),(124,19,'RDKB',NULL,'CMAgent','FREE'),(125,65,'RDKB',NULL,'E2ESuite','FREE'),(127,23,'RDKB',NULL,'WIFIAgent','FREE'),(150,69,'RDKB',NULL,'CosaCM','FREE'),(151,0,'RDKB_TCL',4,'TCL_ERTR_WIFI','FREE'),(156,0,'RDKB',4,'TR069_1','FREE'),(157,6,'RDKB',4,'ALL_Components','FREE'),(159,0,'RDKB',4,'WIFI_1','FREE'),(160,0,'RDKB',4,'ccspcommon_mbus','FREE'),(162,2,'RDKB',4,'Batch_Run','FREE'),(163,14,'RDKB',NULL,'MTA_Agent','FREE'),(164,5,'RDKB',NULL,'TR069Pa','FREE'),(165,0,'RDKB_TCL',4,'TCL_SCRIPTS','FREE');
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
  KEY `FKF6D3D57F132FE10A` (`script_id`),
  KEY `FKF6D3D57F84DB89AA` (`script_group_scripts_id`),
  CONSTRAINT `FKF6D3D57F132FE10A` FOREIGN KEY (`script_id`) REFERENCES `script` (`id`),
  CONSTRAINT `FKF6D3D57F84DB89AA` FOREIGN KEY (`script_group_scripts_id`) REFERENCES `script_group` (`id`)
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
INSERT INTO `script_group_script_file` VALUES (116,10935,0),(117,10935,0),(118,10935,0),(119,10935,0),(120,10935,0),(116,10936,1),(117,10936,1),(118,10936,1),(119,10936,1),(120,10936,1),(116,10937,2),(117,10937,2),(118,10937,2),(119,10937,2),(120,10937,2),(116,10938,3),(117,10938,3),(118,10938,3),(119,10938,3),(120,10938,3),(116,10939,4),(117,10939,4),(118,10939,4),(119,10939,4),(120,10939,4),(116,10940,5),(117,10940,5),(118,10940,5),(119,10940,5),(120,10940,5),(116,10941,6),(117,10941,6),(118,10941,6),(119,10941,6),(120,10941,6),(116,10942,7),(117,10943,7),(118,10943,7),(119,10942,7),(120,10942,7),(116,10943,8),(117,10944,8),(118,10944,8),(119,10943,8),(120,10943,8),(116,10944,9),(117,10945,9),(118,10945,9),(119,10944,9),(120,10944,9),(116,10945,10),(117,10946,10),(118,10946,10),(119,10945,10),(120,10945,10),(116,10946,11),(117,10947,11),(118,10947,11),(119,10946,11),(120,10946,11),(116,10947,12),(117,10948,12),(118,10948,12),(119,10947,12),(120,10947,12),(116,10948,13),(117,10949,13),(118,10949,13),(119,10948,13),(120,10948,13),(116,10949,14),(117,10950,14),(118,10950,14),(119,10949,14),(120,10949,14),(116,10950,15),(117,10951,15),(118,10951,15),(119,10950,15),(120,10950,15),(116,10951,16),(117,10952,16),(118,10952,16),(119,10951,16),(120,10951,16),(116,10952,17),(117,10953,17),(118,10953,17),(119,10952,17),(120,10952,17),(117,10954,18),(121,10953,0),(118,10954,18),(119,10953,18),(120,10953,18),(121,10954,1),(117,10955,19),(118,10955,19),(119,10954,19),(120,10954,19),(121,10955,2),(117,10956,20),(118,10956,20),(119,10955,20),(120,10955,20),(121,10956,3),(117,10957,21),(118,10957,21),(119,10956,21),(120,10956,21),(121,10957,4),(117,10958,22),(118,10958,22),(119,10957,22),(120,10957,22),(121,10958,5),(117,10959,23),(118,10959,23),(119,10958,23),(120,10958,23),(121,10959,6),(117,10960,24),(118,10960,24),(119,10959,24),(120,10959,24),(121,10960,7),(117,10961,25),(118,10961,25),(119,10960,25),(120,10960,25),(121,10961,8),(117,10962,26),(118,10962,26),(119,10961,26),(120,10961,26),(121,10962,9),(117,10963,27),(118,10963,27),(119,10962,27),(120,10962,27),(121,10963,10),(117,10964,28),(118,10964,28),(119,10963,28),(120,10963,28),(121,10964,11),(117,10965,29),(118,10965,29),(119,10964,29),(120,10964,29),(121,10965,12),(117,10966,30),(118,10966,30),(119,10965,30),(120,10965,30),(121,10966,13),(117,10967,31),(118,10967,31),(119,10966,31),(120,10966,31),(121,10967,14),(117,10968,32),(118,10968,32),(119,10967,32),(120,10967,32),(121,10968,15),(117,10969,33),(118,10969,33),(119,10968,33),(120,10968,33),(121,10969,16),(117,10970,34),(118,10970,34),(119,10969,34),(120,10969,34),(117,10971,35),(122,10970,0),(118,10971,35),(119,10970,35),(120,10970,35),(122,10971,1),(117,10972,36),(118,10972,36),(119,10971,36),(120,10971,36),(122,10972,2),(117,10973,37),(118,10973,37),(119,10972,37),(120,10972,37),(122,10973,3),(117,10974,38),(118,10974,38),(119,10973,38),(120,10973,38),(122,10974,4),(117,10975,39),(118,10975,39),(119,10974,39),(120,10974,39),(122,10975,5),(117,10976,40),(118,10976,40),(119,10975,40),(120,10975,40),(122,10976,6),(117,10977,41),(118,10977,41),(119,10976,41),(120,10976,41),(122,10977,7),(117,10978,42),(118,10978,42),(119,10977,42),(120,10977,42),(122,10978,8),(117,10979,43),(118,10979,43),(119,10978,43),(120,10978,43),(122,10979,9),(117,10980,44),(118,10980,44),(119,10979,44),(120,10979,44),(117,10981,45),(123,10980,0),(118,10981,45),(119,10980,45),(120,10980,45),(123,10981,1),(117,10982,46),(118,10982,46),(119,10981,46),(120,10981,46),(123,10982,2),(117,10983,47),(118,10983,47),(119,10982,47),(120,10982,47),(123,10983,3),(117,10984,48),(118,10984,48),(119,10983,48),(120,10983,48),(123,10984,4),(117,10985,49),(118,10985,49),(119,10984,49),(120,10984,49),(123,10985,5),(117,10986,50),(118,10986,50),(119,10985,50),(120,10985,50),(123,10986,6),(117,10987,51),(118,10987,51),(119,10986,51),(120,10986,51),(123,10987,7),(117,10988,52),(118,10988,52),(119,10987,52),(120,10987,52),(123,10988,8),(117,10989,53),(118,10989,53),(119,10988,53),(120,10988,53),(123,10989,9),(117,10990,54),(118,10990,54),(119,10989,54),(120,10989,54),(123,10990,10),(117,10991,55),(118,10991,55),(119,10990,55),(120,10990,55),(123,10991,11),(117,10992,56),(118,10992,56),(119,10991,56),(120,10991,56),(123,10992,12),(117,10993,57),(118,10993,57),(119,10992,57),(120,10992,57),(123,10993,13),(117,10994,58),(118,10994,58),(119,10993,58),(120,10993,58),(123,10994,14),(117,10995,59),(118,10995,59),(119,10994,59),(120,10994,59),(123,10995,15),(117,10996,60),(118,10996,60),(119,10995,60),(120,10995,60),(123,10996,16),(117,10997,61),(118,10997,61),(119,10996,61),(120,10996,61),(123,10997,17),(117,10998,62),(118,10998,62),(119,10997,62),(120,10997,62),(123,10998,18),(117,10999,63),(118,10999,63),(119,10998,63),(120,10998,63),(123,10999,19),(117,11001,64),(118,11001,64),(119,10999,64),(120,10999,64),(123,13400,20),(117,11002,65),(118,11002,65),(119,13400,65),(120,11001,65),(117,11003,66),(124,11001,0),(118,11003,66),(125,11001,0),(120,11002,66),(124,11002,1),(117,11004,67),(118,11004,67),(125,11002,1),(120,11003,67),(124,11003,2),(117,11005,68),(118,11005,68),(125,11003,2),(120,11004,68),(124,11004,3),(117,11006,69),(118,11006,69),(125,11004,3),(120,11005,69),(124,11005,4),(117,11007,70),(118,11007,70),(125,11005,4),(120,11006,70),(124,11006,5),(117,11008,71),(118,11008,71),(125,11006,5),(120,11007,71),(124,11007,6),(117,11009,72),(118,11009,72),(125,11007,6),(120,11008,72),(124,11008,7),(117,11010,73),(118,11010,73),(125,11008,7),(120,11009,73),(124,11009,8),(117,11011,74),(118,11011,74),(125,11009,8),(120,11010,74),(124,11010,9),(117,11012,75),(118,11012,75),(125,11010,9),(120,11011,75),(124,11011,10),(117,11013,76),(118,11013,76),(125,11011,10),(120,11012,76),(124,11012,11),(117,11014,77),(118,11014,77),(125,11012,11),(120,11013,77),(124,11013,12),(117,11015,78),(118,11015,78),(125,11013,12),(120,11014,78),(124,11014,13),(117,11016,79),(118,11016,79),(125,11014,13),(120,11015,79),(124,11015,14),(117,11017,80),(118,11017,80),(125,11015,14),(120,11016,80),(124,11016,15),(117,11018,81),(118,11018,81),(125,11016,15),(120,11017,81),(124,11017,16),(117,11019,82),(118,11019,82),(125,11017,16),(120,11018,82),(124,11018,17),(117,11020,83),(118,11020,83),(125,11018,17),(120,11019,83),(124,11019,18),(117,11036,84),(118,11036,84),(125,11019,18),(120,11020,84),(124,11020,19),(117,11037,85),(118,11037,85),(125,11020,19),(120,11036,85),(117,11038,86),(118,11038,86),(125,11036,20),(120,11037,86),(117,11039,87),(118,11039,87),(125,11037,21),(120,11038,87),(117,11040,88),(118,11040,88),(125,11038,22),(120,11039,88),(117,11041,89),(118,11041,89),(125,11039,23),(120,11040,89),(117,11042,90),(118,11042,90),(125,11040,24),(120,11041,90),(117,11043,91),(118,11043,91),(125,11041,25),(120,11042,91),(117,11044,92),(118,11044,92),(125,11042,26),(120,11043,92),(117,11045,93),(118,11045,93),(125,11043,27),(120,11044,93),(117,11046,94),(118,11046,94),(125,11044,28),(120,11045,94),(117,11047,95),(118,11047,95),(125,11045,29),(120,11046,95),(117,11048,96),(118,11048,96),(125,11046,30),(120,11047,96),(117,11049,97),(118,11049,97),(125,11047,31),(120,11048,97),(117,11050,98),(118,11050,98),(125,11048,32),(120,11049,98),(117,11051,99),(118,11051,99),(125,11049,33),(120,11050,99),(117,11052,100),(118,11052,100),(125,11050,34),(120,11051,100),(117,11054,101),(127,11036,0),(118,11054,101),(125,11051,35),(120,11052,101),(127,11037,1),(117,11055,102),(118,11055,102),(125,11052,36),(120,11053,102),(127,11038,2),(117,13400,103),(118,13400,103),(125,11053,37),(120,11054,103),(127,11039,3),(117,13401,104),(118,13401,104),(125,11054,38),(120,11055,104),(127,11040,4),(117,13402,105),(118,13402,105),(125,11055,39),(120,13400,105),(127,11041,5),(117,13403,106),(118,13403,106),(120,13401,106),(127,11042,6),(117,13404,107),(118,13404,107),(120,13402,107),(127,11043,7),(117,10942,108),(118,10942,108),(120,13403,108),(127,11044,8),(117,11053,109),(118,11053,109),(120,13404,109),(127,11045,9),(117,15044,110),(118,15044,110),(120,13871,110),(127,11046,10),(117,15045,111),(118,15045,111),(120,13872,111),(127,11047,11),(117,15046,112),(118,15046,112),(120,13873,112),(127,11048,12),(117,15048,113),(118,15048,113),(120,13874,113),(127,11049,13),(117,15049,114),(118,15049,114),(120,13875,114),(127,11050,14),(117,15050,115),(118,15050,115),(120,13876,115),(127,11051,15),(117,15051,116),(118,15051,116),(120,13877,116),(127,11052,16),(117,15052,117),(118,15052,117),(120,13878,117),(127,11053,17),(117,15053,118),(118,15053,118),(120,13879,118),(127,11054,18),(117,15054,119),(118,15054,119),(120,13880,119),(127,11055,19),(117,15055,120),(118,15055,120),(120,13881,120),(117,15047,121),(118,15047,121),(120,13960,121),(117,15056,122),(118,15056,122),(120,14323,122),(117,15057,123),(118,15057,123),(120,14324,123),(117,13873,124),(118,13873,124),(120,14325,124),(117,13875,125),(118,13875,125),(120,14326,125),(117,14323,126),(118,14323,126),(120,14327,126),(117,14325,127),(118,14325,127),(120,14329,127),(117,14324,128),(118,14324,128),(120,14330,128),(117,14326,129),(118,14326,129),(120,14331,129),(117,14327,130),(118,14327,130),(120,15043,130),(117,15065,131),(118,15065,131),(120,15044,131),(117,15066,132),(118,15066,132),(120,15045,132),(117,15068,133),(118,15068,133),(120,15046,133),(117,15069,134),(118,15069,134),(120,15047,134),(117,15071,135),(118,15071,135),(120,15048,135),(117,15072,136),(118,15072,136),(120,15049,136),(117,15074,137),(118,15074,137),(120,15050,137),(117,15078,138),(118,15078,138),(120,15051,138),(117,15079,139),(118,15079,139),(120,15052,139),(117,15081,140),(118,15081,140),(120,15053,140),(117,15082,141),(118,15082,141),(120,15054,141),(117,15086,142),(118,15086,142),(120,15055,142),(117,15087,143),(118,15087,143),(120,15056,143),(117,15088,144),(118,15088,144),(120,15057,144),(117,15083,145),(118,15083,145),(120,15058,145),(117,14331,146),(118,14331,146),(120,15059,146),(117,14330,147),(118,14330,147),(120,15060,147),(117,14329,148),(118,14329,148),(120,15061,148),(117,15089,149),(118,15089,149),(120,15062,149),(117,15090,150),(118,15090,150),(120,15063,150),(117,15064,151),(118,15064,151),(120,15064,151),(123,13401,21),(117,15067,152),(118,15067,152),(119,13401,66),(120,15065,152),(123,13402,22),(117,15085,153),(118,15085,153),(119,13402,67),(120,15066,153),(123,13403,23),(117,15084,154),(118,15084,154),(119,13403,68),(120,15067,154),(123,13404,24),(117,15091,155),(118,15091,155),(119,13404,69),(120,15068,155),(117,15092,156),(118,15092,156),(119,13871,70),(120,15069,156),(119,13872,71),(119,13873,72),(119,13874,73),(119,13875,74),(119,13876,75),(119,13877,76),(119,13878,77),(119,13879,78),(119,13880,79),(119,13881,80),(119,13960,81),(119,14323,82),(119,14324,83),(119,14325,84),(119,14326,85),(119,14327,86),(119,14329,87),(119,14330,88),(119,14331,89),(119,15043,90),(119,15044,91),(119,15045,92),(119,15046,93),(119,15047,94),(119,15048,95),(119,15049,96),(119,15050,97),(120,15070,157),(119,15051,98),(120,15071,158),(117,15093,157),(118,15093,157),(117,15058,158),(118,15058,158),(119,15052,99),(120,15072,159),(119,15053,100),(120,15073,160),(117,15059,159),(118,15059,159),(119,15054,101),(120,15074,161),(117,15061,160),(118,15061,160),(119,15055,102),(120,15075,162),(117,15060,161),(118,15060,161),(117,15094,162),(118,15094,162),(119,15056,103),(120,15078,163),(119,15057,104),(120,15079,164),(117,15095,163),(118,15095,163),(117,15063,164),(118,15063,164),(119,15058,105),(120,15080,165),(119,15059,106),(120,15081,166),(117,15073,165),(118,15073,165),(119,15060,107),(120,15082,167),(117,15075,166),(118,15075,166),(119,15061,108),(120,15083,168),(117,15043,167),(118,15043,167),(119,15062,109),(120,15084,169),(117,13876,168),(118,13876,168),(117,13881,169),(150,14323,0),(118,13881,169),(119,15063,110),(120,15085,170),(150,14324,1),(117,13879,170),(118,13879,170),(119,15064,111),(120,15086,171),(150,14325,2),(117,13871,171),(118,13871,171),(119,15065,112),(120,15087,172),(150,14326,3),(117,16612,172),(118,16612,172),(119,15066,113),(120,15088,173),(150,14327,4),(117,13880,173),(118,13880,173),(119,15067,114),(120,15089,174),(150,14329,5),(117,13872,174),(118,13872,174),(119,15068,115),(120,15090,175),(150,14330,6),(117,13874,175),(118,13874,175),(119,15069,116),(120,15091,176),(150,14331,7),(117,16581,176),(118,16581,176),(119,15070,117),(120,15092,177),(150,15058,8),(117,13877,177),(118,13877,177),(119,15071,118),(120,15093,178),(150,15059,9),(117,13878,178),(118,13878,178),(119,15072,119),(120,15094,179),(150,15060,10),(119,15073,120),(120,15095,180),(117,13960,179),(118,13960,179),(117,16565,180),(118,16565,180),(120,16581,181),(120,16612,182),(151,14046,0),(151,14114,1),(151,14091,2),(151,14075,3),(151,14085,4),(151,14095,5),(151,14050,6),(117,16587,181),(118,16587,181),(117,16586,182),(118,16586,182),(119,15074,121),(120,16565,183),(117,16560,183),(118,16560,183),(120,16586,184),(117,16561,184),(118,16561,184),(119,15075,122),(120,16587,185),(119,15078,123),(120,16560,186),(117,16562,185),(118,16562,185),(119,15079,124),(120,16561,187),(117,16563,186),(118,16563,186),(117,16564,187),(118,16564,187),(119,15080,125),(120,16562,188),(117,16566,188),(118,16566,188),(119,15081,126),(120,16563,189),(117,16567,189),(118,16567,189),(119,15082,127),(120,16564,190),(117,16568,190),(118,16568,190),(119,15083,128),(120,16566,191),(117,16569,191),(118,16569,191),(119,15084,129),(120,16567,192),(117,16570,192),(118,16570,192),(119,15085,130),(120,16568,193),(117,16571,193),(118,16571,193),(119,15086,131),(120,16569,194),(117,16572,194),(118,16572,194),(119,15087,132),(120,16570,195),(117,16573,195),(118,16573,195),(119,15088,133),(120,16571,196),(117,16574,196),(118,16574,196),(119,15089,134),(120,16572,197),(117,16582,197),(118,16582,197),(119,15090,135),(120,16573,198),(117,16583,198),(118,16583,198),(119,15091,136),(120,16574,199),(117,16584,199),(118,16584,199),(119,15092,137),(120,16582,200),(117,16585,200),(118,16585,200),(119,15093,138),(120,16583,201),(119,15094,139),(120,16584,202),(117,16588,201),(118,16588,201),(150,15061,11),(117,16589,202),(118,16589,202),(119,15095,140),(120,16585,203),(150,15062,12),(117,16590,203),(118,16590,203),(119,16581,141),(120,16588,204),(150,15063,13),(119,16612,142),(120,16589,205),(117,16591,204),(118,16591,204),(150,15064,14),(119,16565,143),(120,16590,206),(117,16592,205),(118,16592,205),(150,15065,15),(119,16586,144),(120,16591,207),(117,16593,206),(118,16593,206),(150,15066,16),(119,16587,145),(120,16592,208),(117,16594,207),(118,16594,207),(150,15067,17),(119,11042,146),(120,16593,209),(117,16595,208),(118,16595,208),(150,15068,18),(117,16596,209),(118,16596,209),(119,11044,147),(120,16594,210),(150,15069,19),(117,16597,210),(118,16597,210),(119,11037,148),(120,16595,211),(150,15070,20),(119,11041,149),(120,16596,212),(117,16598,211),(118,16598,211),(150,15071,21),(117,16599,212),(118,16599,212),(119,11055,150),(120,16597,213),(150,15072,22),(117,16600,213),(118,16600,213),(119,11048,151),(120,16598,214),(150,15073,23),(117,15080,214),(118,15080,214),(119,11054,152),(120,16599,215),(150,15074,24),(117,15062,215),(118,15062,215),(119,11052,153),(120,16600,216),(150,15075,25),(117,15070,216),(118,15070,216),(119,11046,154),(120,16613,217),(150,15078,26),(117,16613,217),(118,16613,217),(119,11053,155),(120,16614,218),(150,15079,27),(117,16614,218),(118,16614,218),(119,11045,156),(120,16615,219),(150,15080,28),(119,11039,157),(120,16616,220),(117,16615,219),(118,16615,219),(150,15081,29),(119,11043,158),(120,16617,221),(117,16616,220),(118,16616,220),(119,11051,159),(117,16617,221),(118,16617,221),(150,15082,30),(119,11047,160),(150,15083,31),(119,11036,161),(150,15084,32),(119,11050,162),(150,15085,33),(119,11040,163),(150,15086,34),(119,11049,164),(150,15087,35),(119,11038,165),(150,15088,36),(119,16560,166),(150,15089,37),(119,16561,167),(150,15090,38),(119,16562,168),(150,15091,39),(119,16563,169),(150,15092,40),(119,16564,170),(150,15093,41),(119,16566,171),(150,15094,42),(119,16567,172),(150,15095,43),(119,16568,173),(150,16586,44),(119,16569,174),(150,16587,45),(119,16570,175),(150,16582,46),(119,16571,176),(150,16583,47),(119,16572,177),(119,16573,178),(156,16612,0),(156,16614,1),(156,16613,2),(156,16615,3),(156,16616,4),(156,16617,5),(157,16614,0),(157,16613,1),(157,16615,2),(157,16616,3),(157,16617,4),(157,16612,5),(157,16560,6),(157,16564,7),(157,16567,8),(157,16569,9),(157,16572,10),(157,16565,11),(157,16562,12),(157,16571,13),(157,16573,14),(157,16568,15),(157,16574,16),(157,16570,17),(157,16563,18),(157,16566,19),(157,16561,20),(119,16574,179),(159,11055,0),(159,11050,1),(159,11040,2),(159,11047,3),(159,11049,4),(159,11051,5),(159,11054,6),(159,11039,7),(159,11046,8),(159,11048,9),(159,11052,10),(159,11038,11),(159,11042,12),(159,11036,13),(159,11053,14),(159,11041,15),(159,11045,16),(159,11037,17),(159,11044,18),(159,11043,19),(160,15043,0),(160,15044,1),(160,15045,2),(160,15046,3),(160,15047,4),(160,13876,5),(160,15048,6),(160,13881,7),(160,15049,8),(160,13879,9),(160,15050,10),(160,13871,11),(160,13873,12),(160,13875,13),(160,13880,14),(160,13872,15),(160,13874,16),(160,15051,17),(160,15052,18),(160,15053,19),(160,13877,20),(160,15054,21),(160,15055,22),(160,13960,23),(160,16581,24),(160,15056,25),(160,13878,26),(160,15057,27),(119,11011,180),(150,16584,48),(119,11017,181),(150,16585,49),(119,11009,182),(157,15043,21),(157,15044,22),(157,15045,23),(157,15046,24),(157,15047,25),(157,13876,26),(157,15048,27),(157,13881,28),(157,15049,29),(157,13879,30),(157,15050,31),(157,13871,32),(157,13873,33),(157,13875,34),(157,13880,35),(157,13872,36),(157,13874,37),(157,15051,38),(157,15052,39),(157,15053,40),(157,13877,41),(157,15054,42),(157,15055,43),(157,13960,44),(157,16581,45),(157,15056,46),(157,13878,47),(157,15057,48),(157,16588,49),(157,16585,50),(157,16593,51),(157,14330,52),(157,15072,53),(157,14323,54),(157,14325,55),(157,14326,56),(157,14324,57),(157,15090,58),(157,15091,59),(157,15078,60),(157,15079,61),(157,14329,62),(157,15074,63),(157,15084,64),(157,16586,65),(157,15080,66),(157,16587,67),(157,15065,68),(157,14331,69),(157,16600,70),(157,16591,71),(157,16582,72),(157,10960,73),(157,10964,74),(157,10969,75),(157,10955,76),(157,10962,77),(157,10956,78),(157,10965,79),(157,10968,80),(157,10954,81),(157,10966,82),(157,10963,83),(157,10961,84),(157,10957,85),(157,10959,86),(157,10953,87),(157,10967,88),(157,10958,89),(157,11055,90),(157,11050,91),(157,11040,92),(157,11047,93),(157,11049,94),(157,11051,95),(157,11054,96),(157,11039,97),(157,11046,98),(157,11048,99),(157,11052,100),(157,11038,101),(157,11042,102),(157,11036,103),(157,11053,104),(157,11041,105),(157,11045,106),(157,11037,107),(157,11044,108),(157,11043,109),(157,11009,110),(157,11008,111),(157,11010,112),(157,11011,113),(157,11012,114),(157,11006,115),(157,11013,116),(157,11005,117),(157,11015,118),(157,11014,119),(157,11002,120),(157,11018,121),(157,11020,122),(157,11016,123),(157,11004,124),(157,11019,125),(157,11001,126),(157,11007,127),(157,11003,128),(157,11017,129),(119,11018,183),(119,11012,184),(119,11001,185),(119,11019,186),(119,11013,187),(119,11006,188),(119,11010,189),(119,11008,190),(119,11003,191),(119,11016,192),(119,11014,193),(119,11004,194),(119,11005,195),(119,11007,196),(119,11002,197),(119,11015,198),(119,11020,199),(119,16582,200),(119,16583,201),(119,16584,202),(119,16585,203),(119,16588,204),(119,16589,205),(119,16590,206),(119,16591,207),(119,16592,208),(119,16593,209),(119,16594,210),(119,16595,211),(119,16596,212),(119,16597,213),(119,16598,214),(119,16599,215),(119,16600,216),(119,16613,217),(119,16614,218),(119,16615,219),(119,16616,220),(119,16617,221),(150,16588,50),(150,16589,51),(150,16590,52),(150,16591,53),(150,16592,54),(150,16593,55),(150,16594,56),(150,16595,57),(150,16596,58),(150,16597,59),(150,16598,60),(150,16599,61),(150,16600,62),(162,15043,0),(162,15044,1),(162,15045,2),(162,15046,3),(162,15047,4),(162,13876,5),(162,15048,6),(162,13881,7),(162,15049,8),(162,13879,9),(162,15050,10),(162,13871,11),(162,13873,12),(162,13875,13),(162,13880,14),(162,13872,15),(162,13874,16),(162,15051,17),(162,15052,18),(162,15053,19),(162,13877,20),(162,15054,21),(162,15055,22),(162,13960,23),(162,16581,24),(162,15056,25),(162,13878,26),(162,15057,27),(162,11009,28),(162,11008,29),(162,11010,30),(162,11011,31),(162,11012,32),(162,11006,33),(162,11013,34),(162,11005,35),(162,11015,36),(162,11014,37),(162,11002,38),(162,11018,39),(162,11020,40),(162,11016,41),(162,11004,42),(162,11019,43),(162,11001,44),(162,11007,45),(162,11003,46),(162,11017,47),(162,16588,48),(162,16585,49),(162,16590,50),(162,16593,51),(162,16595,52),(162,16584,53),(162,16591,54),(162,16589,55),(162,16594,56),(162,16600,57),(162,16596,58),(162,16597,59),(162,16599,60),(162,15068,61),(162,15069,62),(162,15070,63),(162,15071,64),(162,14331,65),(162,15086,66),(162,14330,67),(162,15087,68),(162,15072,69),(162,15073,70),(162,15065,71),(162,15066,72),(162,15064,73),(162,15067,74),(162,16587,75),(162,16592,76),(162,16582,77),(162,16598,78),(162,15062,79),(162,15063,80),(162,15078,81),(162,15081,82),(162,15080,83),(162,15083,84),(162,15079,85),(162,15082,86),(162,14329,87),(162,15088,88),(162,15074,89),(162,15075,90),(162,15084,91),(162,15085,92),(162,16586,93),(162,16583,94),(162,14323,95),(162,15058,96),(162,14325,97),(162,15059,98),(162,14326,99),(162,15061,100),(162,15095,101),(162,15094,102),(162,14324,103),(162,15060,104),(162,15092,105),(162,15093,106),(162,14327,107),(162,15090,108),(162,15091,109),(162,15089,110),(162,16560,111),(162,16564,112),(162,16567,113),(162,16569,114),(162,16572,115),(162,16565,116),(162,16562,117),(162,16571,118),(162,16573,119),(162,16568,120),(162,16574,121),(162,16570,122),(162,16563,123),(162,16566,124),(162,16561,125),(162,10947,126),(162,10936,127),(162,10935,128),(162,10950,129),(162,10939,130),(162,10945,131),(162,10941,132),(162,10940,133),(162,10951,134),(162,10946,135),(162,10943,136),(162,10952,137),(162,10948,138),(162,10942,139),(162,10938,140),(162,10944,141),(162,10949,142),(162,10937,143),(162,10974,144),(162,10978,145),(162,10972,146),(162,10973,147),(162,10971,148),(162,10979,149),(162,10976,150),(162,10975,151),(162,10977,152),(162,10970,153),(162,10960,154),(162,10964,155),(162,10969,156),(162,10955,157),(162,10962,158),(162,10956,159),(162,10965,160),(162,10968,161),(162,10954,162),(162,10966,163),(162,10963,164),(162,10961,165),(162,10957,166),(162,10959,167),(162,10953,168),(162,10967,169),(162,10958,170),(162,11055,171),(162,11050,172),(162,11040,173),(162,11047,174),(162,11049,175),(162,11051,176),(162,11054,177),(162,11039,178),(162,11046,179),(162,11048,180),(162,11052,181),(162,11038,182),(162,11042,183),(162,11036,184),(162,11053,185),(162,11041,186),(162,11045,187),(162,11037,188),(162,11044,189),(162,11043,190),(162,10997,191),(162,10993,192),(162,10991,193),(162,10984,194),(162,13401,195),(162,10999,196),(162,10988,197),(162,10981,198),(162,10995,199),(162,10987,200),(162,10985,201),(162,10980,202),(162,10983,203),(162,10992,204),(162,10982,205),(162,10989,206),(162,10996,207),(162,13404,208),(162,13402,209),(162,13400,210),(162,13403,211),(162,10990,212),(162,10994,213),(162,10986,214),(162,10998,215),(163,16560,0),(163,16561,1),(163,16562,2),(163,16563,3),(163,16564,4),(163,16565,5),(163,16566,6),(163,16567,7),(163,16568,8),(163,16569,9),(163,16570,10),(163,16571,11),(163,16572,12),(163,16573,13),(163,16574,14),(164,16612,0),(164,16613,1),(164,16614,2),(164,16615,3),(164,16616,4),(164,16617,5),(162,16612,216),(162,16614,217),(162,16613,218),(162,16615,219),(162,16616,220),(162,16617,221),(165,14987,0),(165,14046,1),(165,14975,2),(165,15034,3),(165,15042,4),(165,14980,5),(165,14981,6),(165,14988,7),(165,15041,8),(165,14977,9),(165,15021,10),(165,15001,11),(165,14986,12),(165,15019,13),(165,15015,14),(165,14114,15),(165,14983,16),(165,15018,17),(165,15030,18),(165,14993,19),(165,15005,20),(165,15009,21),(165,14974,22),(165,15002,23),(165,15040,24),(165,15017,25),(165,14982,26),(165,14984,27),(165,15000,28),(165,15036,29),(165,15038,30),(165,14091,31),(165,14075,32),(165,15023,33),(165,14996,34),(165,15033,35),(165,15029,36),(165,15039,37),(165,14085,38),(165,14095,39),(165,15035,40),(165,14050,41),(165,15020,42),(165,14973,43),(165,14999,44),(165,14976,45),(165,14995,46),(165,15004,47),(165,15016,48),(165,15013,49),(165,15025,50),(165,14998,51),(165,14979,52),(165,15008,53),(165,15027,54),(165,14978,55),(165,14989,56),(165,15028,57),(165,15011,58),(165,15022,59),(165,15012,60),(165,14990,61),(165,14994,62),(165,15014,63),(165,14997,64),(165,15032,65),(165,15007,66),(165,15010,67),(165,15031,68),(165,14991,69),(165,15003,70),(165,15006,71),(165,14992,72),(165,14985,73),(165,15037,74);
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
-- Table structure for table `script_tag`
--

DROP TABLE IF EXISTS `script_tag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `script_tag` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `version` bigint(20) NOT NULL,
  `groups_id` bigint(20) DEFAULT NULL,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `FKCDD76226984B586A` (`groups_id`),
  CONSTRAINT `FKCDD76226984B586A` FOREIGN KEY (`groups_id`) REFERENCES `groups` (`id`)
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
  `category` varchar(255) NOT NULL,
  `groups_id` bigint(20) DEFAULT NULL,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `category` (`category`,`name`),
  KEY `FKE987E18F984B586A` (`groups_id`),
  CONSTRAINT `FKE987E18F984B586A` FOREIGN KEY (`groups_id`) REFERENCES `groups` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `socvendor`
--

LOCK TABLES `socvendor` WRITE;
/*!40000 ALTER TABLE `socvendor` DISABLE KEYS */;
INSERT INTO `socvendor` VALUES (1,0,'RDKB',4,'Intel'),(2,0,'RDKV',4,'Intel'),(3,0,'RDKB',4,'Broadcom');
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
  `groups_id` bigint(20) DEFAULT NULL,
  `stream_id` varchar(64) NOT NULL,
  `video_format` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `stream_id` (`stream_id`),
  KEY `FKD3332F65984B586A` (`groups_id`),
  CONSTRAINT `FKD3332F65984B586A` FOREIGN KEY (`groups_id`) REFERENCES `groups` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `streaming_details`
--

LOCK TABLES `streaming_details` WRITE;
/*!40000 ALTER TABLE `streaming_details` DISABLE KEYS */;
INSERT INTO `streaming_details` VALUES (1,1,'ac3','SD',NULL,'1','mpeg2'),(2,1,'ac3','HD',NULL,'2','mpeg4'),(3,1,'aac','SD',NULL,'3','mpeg2'),(4,1,'aac','HD',NULL,'4','mpeg4'),(5,1,'mp3','HD',NULL,'5','mpeg2'),(6,1,'mp3','HD',NULL,'6','mpeg4'),(7,1,'wav','HD',NULL,'7','mpeg2'),(8,1,'wav','HD',NULL,'8','mpeg4'),(9,1,'ac3','HD',NULL,'9','h264'),(10,1,'aac','HD',NULL,'10','h264'),(11,1,'mp3','HD',NULL,'11','h264'),(12,1,'wav','HD',NULL,'12','h264');
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
  `category` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `FKA7A4E82A8358C58A` (`execution_id`),
  CONSTRAINT `FKA7A4E82A8358C58A` FOREIGN KEY (`execution_id`) REFERENCES `execution` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,2,'sreelal@tataelxsi.co.in',4,'ADMINISTRATOR','5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8',NULL,'admin');
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
  `role_id` bigint(20) NOT NULL,
  `user_id` bigint(20) NOT NULL,
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
INSERT INTO `user_roles` VALUES (1,1);
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

-- Dump completed on 2016-04-26 19:14:35
