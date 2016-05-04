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
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `box_manufacturer`
--

LOCK TABLES `box_manufacturer` WRITE;
/*!40000 ALTER TABLE `box_manufacturer` DISABLE KEYS */;
INSERT INTO `box_manufacturer` VALUES (1,0,'RDKB',4,'Cisco'),(2,0,'RDKV',4,'Cisco'),(3,0,'RDKB',4,'Arris'),(4,0,'RDKB',4,'Emulator');
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
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;
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
) ENGINE=InnoDB AUTO_INCREMENT=80 DEFAULT CHARSET=latin1;
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
) ENGINE=InnoDB AUTO_INCREMENT=6970 DEFAULT CHARSET=latin1;
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
) ENGINE=InnoDB AUTO_INCREMENT=1018 DEFAULT CHARSET=latin1;
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
) ENGINE=InnoDB AUTO_INCREMENT=1017 DEFAULT CHARSET=latin1;
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
) ENGINE=InnoDB AUTO_INCREMENT=5336 DEFAULT CHARSET=latin1;
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
) ENGINE=InnoDB AUTO_INCREMENT=48 DEFAULT CHARSET=latin1;
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
) ENGINE=InnoDB AUTO_INCREMENT=16624 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `script_file`
--

LOCK TABLES `script_file` WRITE;
/*!40000 ALTER TABLE `script_file` DISABLE KEYS */;
INSERT INTO `script_file` VALUES (11036,0,'RDKB','WIFIAgent','TS_WIFIAGENT_GetParamNames'),(11038,0,'RDKB','WIFIAgent','TS_WIFIAGENT_GetHealth'),(11039,0,'RDKB','WIFIAgent','TS_WIFIAGENT_EnableUAPSD'),(11040,0,'RDKB','WIFIAgent','TS_WIFIAGENT_DelObject'),(11041,0,'RDKB','WIFIAgent','TS_WIFIAGENT_GetValuesOfWMMCapabilitANdUAPSDCapability'),(11042,0,'RDKB','WIFIAgent','TS_WIFIAGENT_GetNumberOfEntries'),(11043,0,'RDKB','WIFIAgent','TS_WIFIAGENT_SetSessionId'),(11044,0,'RDKB','WIFIAgent','TS_WIFIAGENT_SetParamValues'),(11045,0,'RDKB','WIFIAgent','TS_WIFIAGENT_SetAttributes'),(11046,0,'RDKB','WIFIAgent','TS_WIFIAGENT_EnableWMM'),(11047,0,'RDKB','WIFIAgent','TS_WIFIAGENT_EnableAccessPoint'),(11048,0,'RDKB','WIFIAgent','TS_WIFIAGENT_FactoryReset'),(11049,0,'RDKB','WIFIAgent','TS_WIFIAGENT_EnableAccessPointSSIDAdvertisement'),(11050,0,'RDKB','WIFIAgent','TS_WIFIAGENT_AddObject'),(11051,0,'RDKB','WIFIAgent','TS_WIFIAGENT_EnableBssHotSpot'),(11052,0,'RDKB','WIFIAgent','TS_WIFIAGENT_GetAttributes'),(11053,0,'RDKB','WIFIAgent','TS_WIFIAGENT_GetParamValues'),(11054,0,'RDKB','WIFIAgent','TS_WIFIAGENT_EnableSecurityMode'),(11055,0,'RDKB','WIFIAgent','TS_WIFIAGENT_AccessPointRetryLimit'),(13871,0,'RDKB','ccspcommon_mbus','TS_CCSPCOMMON_MBUS_Init'),(13872,0,'RDKB','ccspcommon_mbus','TS_CCSPCOMMON_MBUS_LoadCfg'),(13873,0,'RDKB','ccspcommon_mbus','TS_CCSPCOMMON_MBUS_InvalidLoadCfg'),(13874,0,'RDKB','ccspcommon_mbus','TS_CCSPCOMMON_MBUS_LoadDmXml'),(13875,0,'RDKB','ccspcommon_mbus','TS_CCSPCOMMON_MBUS_InvalidLoadDmXml'),(13876,0,'RDKB','ccspcommon_mbus','TS_CCSPCOMMON_MBUS_Exit'),(13877,0,'RDKB','ccspcommon_mbus','TS_CCSPCOMMON_MBUS_RegisterEvent'),(13878,0,'RDKB','ccspcommon_mbus','TS_CCSPCOMMON_MBUS_UnRegisterEvent'),(14046,0,'RDKB_TCL','tcl','TC_ERTR_0002'),(14050,0,'RDKB_TCL','tcl','TC_ERTR_0042'),(14075,0,'RDKB_TCL','tcl','TC_ERTR_0033'),(14085,0,'RDKB_TCL','tcl','TC_ERTR_0039'),(14091,0,'RDKB_TCL','tcl','TC_ERTR_0032'),(14095,0,'RDKB_TCL','tcl','TC_ERTR_0040'),(14114,0,'RDKB_TCL','tcl','TC_ERTR_0016'),(14323,1,'RDKB','CosaCM','TS_CosaCM_GetCMResetCount'),(14324,1,'RDKB','CosaCM','TS_CosaCM_GetLocalResetCount'),(14325,1,'RDKB','CosaCM','TS_CosaCM_GetDocsisResetCount'),(14326,1,'RDKB','CosaCM','TS_CosaCM_GetErouterResetCount'),(14327,1,'RDKB','CosaCM','TS_CosaCM_GetResetCount_InvalidResetType'),(14329,1,'RDKB','CosaCM','TS_COSACM_GetUpstreamChannel'),(14330,1,'RDKB','CosaCM','TS_COSACM_GetDownstreamChannel'),(14331,1,'RDKB','CosaCM','TS_COSACM_GetDocsisLog'),(14973,0,'RDKB_TCL','tcl','TC_ERTR_0044'),(14974,0,'RDKB_TCL','tcl','TC_ERTR_0023'),(14975,0,'RDKB_TCL','tcl','TC_ERTR_0003'),(14976,0,'RDKB_TCL','tcl','TC_ERTR_0046'),(14977,0,'RDKB_TCL','tcl','TC_ERTR_0010'),(14978,0,'RDKB_TCL','tcl','TC_ERTR_0056'),(14979,0,'RDKB_TCL','tcl','TC_ERTR_0053'),(14980,0,'RDKB_TCL','tcl','TC_ERTR_0006'),(14981,0,'RDKB_TCL','tcl','TC_ERTR_0007'),(14982,0,'RDKB_TCL','tcl','TC_ERTR_0027'),(14983,0,'RDKB_TCL','tcl','TC_ERTR_0017'),(14984,0,'RDKB_TCL','tcl','TC_ERTR_0028'),(14985,0,'RDKB_TCL','tcl','TC_ERTR_0074'),(14986,0,'RDKB_TCL','tcl','TC_ERTR_0013'),(14987,0,'RDKB_TCL','tcl','TC_ERTR_0001'),(14988,0,'RDKB_TCL','tcl','TC_ERTR_0008'),(14989,0,'RDKB_TCL','tcl','TC_ERTR_0057'),(14990,0,'RDKB_TCL','tcl','TC_ERTR_0062'),(14991,0,'RDKB_TCL','tcl','TC_ERTR_0070'),(14992,0,'RDKB_TCL','tcl','TC_ERTR_0073'),(14993,0,'RDKB_TCL','tcl','TC_ERTR_0020'),(14994,0,'RDKB_TCL','tcl','TC_ERTR_0063'),(14995,0,'RDKB_TCL','tcl','TC_ERTR_0047'),(14996,0,'RDKB_TCL','tcl','TC_ERTR_0035'),(14997,0,'RDKB_TCL','tcl','TC_ERTR_0065'),(14998,0,'RDKB_TCL','tcl','TC_ERTR_0052'),(14999,0,'RDKB_TCL','tcl','TC_ERTR_0045'),(15000,0,'RDKB_TCL','tcl','TC_ERTR_0029'),(15001,0,'RDKB_TCL','tcl','TC_ERTR_0012'),(15002,0,'RDKB_TCL','tcl','TC_ERTR_0024'),(15003,0,'RDKB_TCL','tcl','TC_ERTR_0071'),(15004,0,'RDKB_TCL','tcl','TC_ERTR_0048'),(15005,0,'RDKB_TCL','tcl','TC_ERTR_0021'),(15006,0,'RDKB_TCL','tcl','TC_ERTR_0072'),(15007,0,'RDKB_TCL','tcl','TC_ERTR_0067'),(15008,0,'RDKB_TCL','tcl','TC_ERTR_0054'),(15009,0,'RDKB_TCL','tcl','TC_ERTR_0022'),(15010,0,'RDKB_TCL','tcl','TC_ERTR_0068'),(15011,0,'RDKB_TCL','tcl','TC_ERTR_0059'),(15012,0,'RDKB_TCL','tcl','TC_ERTR_0061'),(15013,0,'RDKB_TCL','tcl','TC_ERTR_0050'),(15014,0,'RDKB_TCL','tcl','TC_ERTR_0064'),(15015,0,'RDKB_TCL','tcl','TC_ERTR_0015'),(15016,0,'RDKB_TCL','tcl','TC_ERTR_0049'),(15017,0,'RDKB_TCL','tcl','TC_ERTR_0026'),(15018,0,'RDKB_TCL','tcl','TC_ERTR_0018'),(15019,0,'RDKB_TCL','tcl','TC_ERTR_0014'),(15020,0,'RDKB_TCL','tcl','TC_ERTR_0043'),(15021,0,'RDKB_TCL','tcl','TC_ERTR_0011'),(15022,0,'RDKB_TCL','tcl','TC_ERTR_0060'),(15023,0,'RDKB_TCL','tcl','TC_ERTR_0034'),(15025,0,'RDKB_TCL','tcl','TC_ERTR_0051'),(15027,0,'RDKB_TCL','tcl','TC_ERTR_0055'),(15028,0,'RDKB_TCL','tcl','TC_ERTR_0058'),(15029,0,'RDKB_TCL','tcl','TC_ERTR_0037'),(15030,0,'RDKB_TCL','tcl','TC_ERTR_0019'),(15031,0,'RDKB_TCL','tcl','TC_ERTR_0069'),(15032,0,'RDKB_TCL','tcl','TC_ERTR_0066'),(15033,0,'RDKB_TCL','tcl','TC_ERTR_0036'),(15034,0,'RDKB_TCL','tcl','TC_ERTR_0004'),(15035,0,'RDKB_TCL','tcl','TC_ERTR_0041'),(15036,0,'RDKB_TCL','tcl','TC_ERTR_0030'),(15037,0,'RDKB_TCL','tcl','TC_ERTR_0075'),(15038,0,'RDKB_TCL','tcl','TC_ERTR_0031'),(15039,0,'RDKB_TCL','tcl','TC_ERTR_0038'),(15040,0,'RDKB_TCL','tcl','TC_ERTR_0025'),(15041,0,'RDKB_TCL','tcl','TC_ERTR_0009'),(15042,0,'RDKB_TCL','tcl','TC_ERTR_0005'),(15043,0,'RDKB','ccspcommon_mbus','TS_CCSPCOMMON_MBUS_BusCheck'),(15045,0,'RDKB','ccspcommon_mbus','TS_CCSPCOMMON_MBUS_DiskComponentSupportingDynamicTbl'),(15046,0,'RDKB','ccspcommon_mbus','TS_CCSPCOMMON_MBUS_DiskNamespaceSupportedByComponent'),(15048,0,'RDKB','ccspcommon_mbus','TS_CCSPCOMMON_MBUS_GetAllocMemory'),(15049,0,'RDKB','ccspcommon_mbus','TS_CCSPCOMMON_MBUS_GetMaxMemory'),(15051,0,'RDKB','ccspcommon_mbus','TS_CCSPCOMMON_MBUS_QueryStatus'),(15053,0,'RDKB','ccspcommon_mbus','TS_CCSPCOMMON_MBUS_RegisterCapability'),(15054,0,'RDKB','ccspcommon_mbus','TS_CCSPCOMMON_MBUS_RegisterPath'),(15057,0,'RDKB','ccspcommon_mbus','TS_CCSPCOMMON_MBUS_UnRegisterNamespace'),(15058,0,'RDKB','CosaCM','TS_CosaCM_GetCMResetCount_WithInvalidBuffer'),(15059,0,'RDKB','CosaCM','TS_CosaCM_GetDocsisResetCount_WithInvalidBuffer'),(15060,0,'RDKB','CosaCM','TS_CosaCM_GetLocalResetCount_WithInvalidBuffer'),(15061,0,'RDKB','CosaCM','TS_CosaCM_GetErouterResetCount_WithInvalidBuffer'),(15064,0,'RDKB','CosaCM','TS_COSACM_GetLoopDiagnosticsStart'),(15065,0,'RDKB','CosaCM','TS_COSACM_GetLoopDiagnosticsDetails'),(15072,0,'RDKB','CosaCM','TS_COSACM_GetLog'),(15074,0,'RDKB','CosaCM','TS_COSACM_SetLog'),(15078,0,'RDKB','CosaCM','TS_COSACM_GetTelephonyDHCPStatus'),(15079,0,'RDKB','CosaCM','TS_COSACM_GetTelephonyTftpStatus'),(15080,0,'RDKB','CosaCM','TS_COSACM_GetTelephonyRegistrationStatus'),(15084,0,'RDKB','CosaCM','TS_COSACM_SetLoopDiagnosticsStart'),(15089,0,'RDKB','CosaCM','TS_CosaCM_SetUpstreamChannelId'),(15090,0,'RDKB','CosaCM','TS_CosaCM_GetStartDSFrequency'),(15091,0,'RDKB','CosaCM','TS_CosaCM_SetStartDSFrequency'),(15092,0,'RDKB','CosaCM','TS_CosaCM_GetProvType'),(15093,0,'RDKB','CosaCM','TS_CosaCM_GetProvType_WithInvalidBuffer'),(16582,0,'RDKB','CosaCM','TS_COSACM_GetMarket'),(16583,0,'RDKB','CosaCM','TS_COSACM_SetMDDIPOverride_ArgMemory_unalloc'),(16584,0,'RDKB','CosaCM','TS_COSACM_GetCMCert'),(16586,0,'RDKB','CosaCM','TS_COSACM_SetMDDIPOverride'),(16587,0,'RDKB','CosaCM','TS_COSACM_GetMDDIPOverride'),(16591,0,'RDKB','CosaCM','TS_COSACM_GetCMCertStatus'),(16594,0,'RDKB','CosaCM','TS_COSACM_GetCMCert_ArgMemory_unalloc'),(16600,0,'RDKB','CosaCM','TS_COSACM_GetCMErrorCodewords'),(16619,0,'RDKB','CosaCM','TS_COSACM_GetLogWithInvalidBuffer'),(16620,0,'RDKB','CosaCM','TS_COSACM_GetTelephonyTftpStatus_WithInvalidBuffer'),(16621,0,'RDKB','CosaCM','TS_COSACM_SetLoopDiagnosticsStart_WithInvalidBuffer'),(16622,0,'RDKB','CosaCM','TS_COSACM_GetTelephonyDHCPStatus_WithInvalidBuffer'),(16623,0,'RDKB','CosaCM','TS_CosaCM_GetStatus');
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
) ENGINE=InnoDB AUTO_INCREMENT=171 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `script_group`
--

LOCK TABLES `script_group` WRITE;
/*!40000 ALTER TABLE `script_group` DISABLE KEYS */;
INSERT INTO `script_group` VALUES (117,715,'RDKB',NULL,'RDKB_Hybrid-1','FREE'),(118,715,'RDKB',NULL,'RDKB_Hybrid-1_NO_OS','FREE'),(119,278,'RDKB',NULL,'ComponentSuite','FREE'),(120,300,'RDKB',NULL,'Hybrid-1Suite','FREE'),(125,66,'RDKB',NULL,'E2ESuite','FREE'),(127,24,'RDKB',NULL,'WIFIAgent','FREE'),(150,77,'RDKB',NULL,'CosaCM','FREE'),(151,0,'RDKB_TCL',4,'TCL_ERTR_WIFI','FREE'),(157,7,'RDKB',4,'ALL_Components','FREE'),(159,1,'RDKB',4,'WIFI_1','FREE'),(160,1,'RDKB',4,'ccspcommon_mbus','FREE'),(162,4,'RDKB',4,'Batch_Run','FREE'),(165,0,'RDKB_TCL',4,'TCL_SCRIPTS','FREE');
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
INSERT INTO `script_group_script_file` VALUES (117,11036,0),(118,11036,0),(119,13871,0),(120,11036,0),(117,11038,1),(118,11038,1),(119,13872,1),(120,11038,1),(117,11039,2),(118,11039,2),(119,13873,2),(120,11039,2),(117,11040,3),(118,11040,3),(119,13874,3),(120,11040,3),(117,11041,4),(118,11041,4),(119,13875,4),(120,11041,4),(117,11042,5),(118,11042,5),(119,13876,5),(120,11042,5),(117,11043,6),(118,11043,6),(119,13877,6),(120,11043,6),(117,11044,7),(118,11044,7),(119,13878,7),(120,11044,7),(117,11045,8),(118,11045,8),(119,14323,8),(120,11045,8),(117,11046,9),(118,11046,9),(119,14324,9),(120,11046,9),(117,11047,10),(118,11047,10),(119,14325,10),(120,11047,10),(117,11048,11),(118,11048,11),(119,14326,11),(120,11048,11),(117,11049,12),(118,11049,12),(119,14327,12),(120,11049,12),(117,11050,13),(118,11050,13),(119,14329,13),(120,11050,13),(117,11051,14),(118,11051,14),(119,14330,14),(120,11051,14),(117,11052,15),(118,11052,15),(119,14331,15),(120,11052,15),(117,11054,16),(118,11054,16),(119,15043,16),(120,11053,16),(117,11055,17),(118,11055,17),(119,15045,17),(120,11054,17),(117,11053,18),(118,11053,18),(119,15046,18),(120,11055,18),(117,15045,19),(118,15045,19),(119,15048,19),(120,13871,19),(117,15046,20),(118,15046,20),(119,15049,20),(120,13872,20),(117,15048,21),(118,15048,21),(119,15051,21),(120,13873,21),(117,15049,22),(118,15049,22),(119,15053,22),(120,13874,22),(117,15051,23),(118,15051,23),(119,15054,23),(120,13875,23),(117,15053,24),(118,15053,24),(119,15057,24),(120,13876,24),(117,15054,25),(118,15054,25),(119,15058,25),(120,13877,25),(117,15057,26),(118,15057,26),(119,15059,26),(120,13878,26),(117,13873,27),(118,13873,27),(119,15060,27),(120,14323,27),(117,13875,28),(118,13875,28),(119,15061,28),(120,14324,28),(117,14323,29),(118,14323,29),(119,15064,29),(120,14325,29),(117,14325,30),(118,14325,30),(119,15065,30),(120,14326,30),(117,14324,31),(118,14324,31),(119,15072,31),(120,14327,31),(117,14326,32),(118,14326,32),(119,15074,32),(120,14329,32),(117,14327,33),(118,14327,33),(119,15078,33),(120,14330,33),(117,15065,34),(118,15065,34),(119,15079,34),(120,14331,34),(117,15072,35),(118,15072,35),(119,15080,35),(120,15043,35),(117,15074,36),(118,15074,36),(119,15084,36),(120,15045,36),(117,15078,37),(118,15078,37),(119,15089,37),(120,15046,37),(117,15079,38),(118,15079,38),(119,15090,38),(120,15048,38),(117,14331,39),(118,14331,39),(119,15091,39),(120,15049,39),(117,14330,40),(118,14330,40),(119,15092,40),(120,15051,40),(117,14329,41),(118,14329,41),(119,15093,41),(120,15053,41),(117,15089,42),(118,15089,42),(119,16586,42),(120,15054,42),(117,15090,43),(118,15090,43),(119,16587,43),(120,15057,43),(117,15064,44),(118,15064,44),(119,11042,44),(120,15058,44),(117,15084,45),(118,15084,45),(119,11044,45),(120,15059,45),(117,15091,46),(118,15091,46),(119,11041,46),(120,15060,46),(117,15092,47),(118,15092,47),(119,11055,47),(120,15061,47),(117,15093,48),(118,15093,48),(119,11048,48),(120,15064,48),(117,15058,49),(118,15058,49),(119,11054,49),(120,15065,49),(117,15059,50),(118,15059,50),(119,11052,50),(120,15072,50),(117,15061,51),(118,15061,51),(119,11046,51),(120,15074,51),(117,15060,52),(118,15060,52),(119,11053,52),(120,15078,52),(117,15043,53),(118,15043,53),(119,11045,53),(120,15079,53),(117,13876,54),(118,13876,54),(119,11039,54),(120,15080,54),(117,13871,55),(118,13871,55),(119,11043,55),(120,15084,55),(117,13872,56),(118,13872,56),(119,11051,56),(120,15089,56),(117,13874,57),(118,13874,57),(119,11047,57),(120,15090,57),(117,13877,58),(118,13877,58),(119,11036,58),(120,15091,58),(117,13878,59),(118,13878,59),(119,11050,59),(120,15092,59),(117,16587,60),(118,16587,60),(119,11040,60),(120,15093,60),(117,16586,61),(118,16586,61),(119,11049,61),(120,16586,61),(117,16582,62),(118,16582,62),(119,11038,62),(120,16587,62),(117,16583,63),(118,16583,63),(119,16582,63),(120,16582,63),(117,16584,64),(118,16584,64),(119,16583,64),(120,16583,64),(117,16591,65),(118,16591,65),(119,16584,65),(120,16584,65),(117,16594,66),(118,16594,66),(125,11036,0),(120,16591,66),(117,16600,67),(118,16600,67),(125,11038,1),(120,16594,67),(117,15080,68),(118,15080,68),(125,11039,2),(120,16600,68),(117,16619,69),(118,16619,69),(125,11040,3),(120,16619,69),(117,16620,70),(118,16620,70),(125,11041,4),(120,16620,70),(117,16621,71),(118,16621,71),(125,11042,5),(120,16621,71),(117,16622,72),(118,16622,72),(125,11043,6),(120,16622,72),(125,11044,7),(125,11045,8),(125,11046,9),(125,11047,10),(125,11048,11),(125,11049,12),(125,11050,13),(125,11051,14),(125,11052,15),(125,11053,16),(125,11054,17),(125,11055,18),(127,11036,0),(127,11038,1),(127,11039,2),(127,11040,3),(127,11041,4),(127,11042,5),(127,11043,6),(127,11044,7),(127,11045,8),(127,11046,9),(127,11047,10),(127,11048,11),(127,11049,12),(127,11050,13),(127,11051,14),(127,11052,15),(127,11053,16),(127,11054,17),(127,11055,18),(119,16591,66),(119,16594,67),(119,16600,68),(119,16619,69),(119,16620,70),(119,16621,71),(119,16622,72),(150,14323,0),(150,14324,1),(150,14325,2),(150,14326,3),(150,14327,4),(150,14329,5),(150,14330,6),(150,14331,7),(150,15058,8),(150,15059,9),(150,15060,10),(151,14046,0),(151,14114,1),(151,14091,2),(151,14075,3),(151,14085,4),(151,14095,5),(151,14050,6),(150,15061,11),(150,15064,12),(150,15065,13),(150,15072,14),(150,15074,15),(150,15078,16),(150,15079,17),(150,15080,18),(150,15084,19),(150,15089,20),(150,15090,21),(150,15091,22),(150,15092,23),(150,15093,24),(150,16586,25),(150,16587,26),(150,16582,27),(150,16583,28),(150,16584,29),(150,16591,30),(150,16594,31),(150,16600,32),(150,16619,33),(150,16620,34),(150,16621,35),(150,16622,36),(157,15043,0),(157,15045,1),(157,15046,2),(157,13876,3),(157,15048,4),(157,15049,5),(157,13871,6),(157,13873,7),(157,13875,8),(157,13872,9),(157,13874,10),(157,15051,11),(157,15053,12),(157,13877,13),(157,15054,14),(157,13878,15),(157,15057,16),(157,14330,17),(157,15072,18),(157,14323,19),(157,14325,20),(159,11055,0),(159,11050,1),(159,11040,2),(159,11047,3),(159,11049,4),(159,11051,5),(159,11054,6),(159,11039,7),(159,11046,8),(159,11048,9),(159,11052,10),(159,11038,11),(159,11042,12),(159,11036,13),(159,11053,14),(159,11041,15),(159,11045,16),(159,11044,17),(159,11043,18),(160,15043,0),(160,15045,1),(160,15046,2),(160,13876,3),(160,15048,4),(160,15049,5),(160,13871,6),(160,13873,7),(160,13875,8),(160,13872,9),(160,13874,10),(160,15051,11),(160,15053,12),(160,13877,13),(160,15054,14),(160,13878,15),(160,15057,16),(157,14326,21),(157,14324,22),(157,15090,23),(157,15091,24),(157,15078,25),(157,15079,26),(157,14329,27),(157,15074,28),(157,15084,29),(157,16586,30),(157,15080,31),(157,16587,32),(157,15065,33),(157,14331,34),(157,16600,35),(157,16591,36),(157,16582,37),(157,11055,38),(157,11050,39),(157,11040,40),(157,11047,41),(157,11049,42),(157,11051,43),(157,11054,44),(157,11039,45),(157,11046,46),(157,11048,47),(157,11052,48),(157,11038,49),(157,11042,50),(157,11036,51),(157,11053,52),(157,11041,53),(157,11045,54),(157,11044,55),(157,11043,56),(162,15043,0),(162,15045,1),(162,15046,2),(162,13876,3),(162,15048,4),(162,15049,5),(162,13871,6),(162,13873,7),(162,13875,8),(162,13872,9),(162,13874,10),(162,15051,11),(162,15053,12),(162,13877,13),(162,15054,14),(162,13878,15),(162,15057,16),(162,16584,17),(162,16591,18),(162,16594,19),(162,16600,20),(162,14331,21),(162,14330,22),(162,15072,23),(162,15065,24),(162,15064,25),(162,16587,26),(162,16582,27),(162,15078,28),(162,15080,29),(162,15079,30),(162,14329,31),(162,15074,32),(162,15084,33),(162,16586,34),(162,16583,35),(162,14323,36),(162,15058,37),(162,14325,38),(162,15059,39),(162,14326,40),(162,15061,41),(162,14324,42),(162,15060,43),(162,15092,44),(162,15093,45),(162,14327,46),(162,15090,47),(162,15091,48),(162,15089,49),(162,11055,50),(162,11050,51),(162,11040,52),(162,11047,53),(162,11049,54),(162,11051,55),(162,11054,56),(162,11039,57),(162,11046,58),(162,11048,59),(162,11052,60),(162,11038,61),(162,11042,62),(162,11036,63),(162,11053,64),(162,11041,65),(162,11045,66),(162,11044,67),(162,11043,68),(165,14987,0),(165,14046,1),(165,14975,2),(165,15034,3),(165,15042,4),(165,14980,5),(165,14981,6),(165,14988,7),(165,15041,8),(165,14977,9),(165,15021,10),(165,15001,11),(165,14986,12),(165,15019,13),(165,15015,14),(165,14114,15),(165,14983,16),(165,15018,17),(165,15030,18),(165,14993,19),(165,15005,20),(165,15009,21),(165,14974,22),(165,15002,23),(165,15040,24),(165,15017,25),(165,14982,26),(165,14984,27),(165,15000,28),(165,15036,29),(165,15038,30),(165,14091,31),(165,14075,32),(165,15023,33),(165,14996,34),(165,15033,35),(165,15029,36),(165,15039,37),(165,14085,38),(165,14095,39),(165,15035,40),(165,14050,41),(165,15020,42),(165,14973,43),(165,14999,44),(165,14976,45),(165,14995,46),(165,15004,47),(165,15016,48),(165,15013,49),(165,15025,50),(165,14998,51),(165,14979,52),(165,15008,53),(165,15027,54),(165,14978,55),(165,14989,56),(165,15028,57),(165,15011,58),(165,15022,59),(165,15012,60),(165,14990,61),(165,14994,62),(165,15014,63),(165,14997,64),(165,15032,65),(165,15007,66),(165,15010,67),(165,15031,68),(165,14991,69),(165,15003,70),(165,15006,71),(165,14992,72),(165,14985,73),(165,15037,74),(150,16623,37),(117,16623,73),(118,16623,73),(119,16623,73),(120,16623,73),(162,16619,69),(162,16622,70),(162,16620,71),(162,16621,72),(162,16623,73);
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
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `socvendor`
--

LOCK TABLES `socvendor` WRITE;
/*!40000 ALTER TABLE `socvendor` DISABLE KEYS */;
INSERT INTO `socvendor` VALUES (1,0,'RDKB',4,'Intel'),(2,0,'RDKV',4,'Intel'),(3,0,'RDKB',4,'Broadcom'),(4,0,'RDKB',4,'Emulator');
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
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=latin1;
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

-- Dump completed on 2016-05-02 16:20:35
