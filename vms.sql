-- MySQL dump 10.13  Distrib 5.5.53, for debian-linux-gnu (x86_64)
--
-- Host: 0.0.0.0    Database: vms
-- ------------------------------------------------------
-- Server version	5.5.53-0ubuntu0.14.04.1

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
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`,`permission_id`),
  KEY `auth_group__permission_id_1f49ccbbdc69d2fc_fk_auth_permission_id` (`permission_id`),
  CONSTRAINT `auth_group_permission_group_id_689710a9a73b7457_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_group__permission_id_1f49ccbbdc69d2fc_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`),
  CONSTRAINT `auth__content_type_id_508cf46651277a81_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can add permission',2,'add_permission'),(5,'Can change permission',2,'change_permission'),(6,'Can delete permission',2,'delete_permission'),(7,'Can add group',3,'add_group'),(8,'Can change group',3,'change_group'),(9,'Can delete group',3,'delete_group'),(10,'Can add user',4,'add_user'),(11,'Can change user',4,'change_user'),(12,'Can delete user',4,'delete_user'),(13,'Can add content type',5,'add_contenttype'),(14,'Can change content type',5,'change_contenttype'),(15,'Can delete content type',5,'delete_contenttype'),(16,'Can add session',6,'add_session'),(17,'Can change session',6,'change_session'),(18,'Can delete session',6,'delete_session'),(19,'Can add batch',7,'add_batch'),(20,'Can change batch',7,'change_batch'),(21,'Can delete batch',7,'delete_batch'),(22,'Can add voucher instant',8,'add_voucherinstant'),(23,'Can change voucher instant',8,'change_voucherinstant'),(24,'Can delete voucher instant',8,'delete_voucherinstant'),(25,'Can add voucher standard',9,'add_voucherstandard'),(26,'Can change voucher standard',9,'change_voucherstandard'),(27,'Can delete voucher standard',9,'delete_voucherstandard');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$20000$7Zcux9DmdXC9$8SzRO4S3NUuQVnidqOP7ANhXVeEX+VJXUiSr2fzZX9A=','2017-05-08 14:42:07',1,'dayo@incisia.com','','','dayo@incisia.com',1,1,'2017-05-08 14:41:11'),(2,'pbkdf2_sha256$20000$3XDp8yi39pWu$y0gnBob6ecuBSxgsCES8eFl+VWt02QFvsbQWg4018Fc=','2018-06-08 14:57:58',0,'test@test.com','Test','Test','',0,1,'2017-05-08 14:42:26');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_33ac548dcf5f8e37_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_33ac548dcf5f8e37_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_4b5ed4ffdb8fd9b0_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`permission_id`),
  KEY `auth_user_u_permission_id_384b62483d7071f0_fk_auth_permission_id` (`permission_id`),
  CONSTRAINT `auth_user_user_permissi_user_id_7f0938558328534a_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `auth_user_u_permission_id_384b62483d7071f0_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `djang_content_type_id_697914295151027a_fk_django_content_type_id` (`content_type_id`),
  KEY `django_admin_log_user_id_52fdd58701c5f563_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_user_id_52fdd58701c5f563_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `djang_content_type_id_697914295151027a_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2017-05-08 14:42:26','2','test@test.com',1,'',4,1),(2,'2017-05-08 14:42:37','2','test@test.com',2,'Changed first_name and last_name.',4,1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_45f3b1d93ec8c61c_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(6,'sessions','session'),(7,'vouchers','batch'),(8,'vouchers','voucherinstant'),(9,'vouchers','voucherstandard');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2017-05-08 10:09:18'),(2,'auth','0001_initial','2017-05-08 10:09:18'),(3,'admin','0001_initial','2017-05-08 10:09:18'),(4,'contenttypes','0002_remove_content_type_name','2017-05-08 10:09:18'),(5,'auth','0002_alter_permission_name_max_length','2017-05-08 10:09:18'),(6,'auth','0003_alter_user_email_max_length','2017-05-08 10:09:18'),(7,'auth','0004_alter_user_username_opts','2017-05-08 10:09:18'),(8,'auth','0005_alter_user_last_login_null','2017-05-08 10:09:18'),(9,'auth','0006_require_contenttypes_0002','2017-05-08 10:09:18'),(10,'sessions','0001_initial','2017-05-08 10:09:18'),(11,'vouchers','0001_initial','2017-05-08 10:09:18'),(12,'vouchers','0002_vend','2017-05-08 10:09:18'),(13,'vouchers','0003_voucher_is_sold','2017-05-08 10:09:18'),(14,'vouchers','0004_auto_20151221_0745','2017-05-08 10:09:19'),(15,'vouchers','0005_batch_voucher_type','2017-05-08 10:09:19'),(16,'vouchers','0006_auto_20160103_1458','2017-05-08 10:09:19'),(17,'vouchers','0007_auto_20160103_1922','2017-05-08 10:09:19'),(18,'vouchers','0008_auto_20160106_2323','2017-05-08 10:09:19'),(19,'vouchers','0009_batch_user','2017-05-08 10:09:19'),(20,'vouchers','0010_vend_phone_number','2017-05-08 10:09:19'),(21,'vouchers','0011_auto_20161126_1002','2017-05-08 10:09:19'),(22,'vouchers','0012_auto_20161126_1008','2017-05-08 10:09:19'),(23,'vouchers','0009_auto_20161205_1943','2017-05-08 10:09:19'),(24,'vouchers','0013_merge','2017-05-08 10:09:19'),(25,'vouchers','0014_auto_20161212_0038','2017-05-08 10:09:20'),(26,'vouchers','0015_auto_20161212_0042','2017-05-08 10:09:20'),(27,'vouchers','0016_delete_vend','2017-05-08 10:09:20');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_de54fa62` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('9ic7c2wgwfitol4rohbr3b97o0046g10','MGViOWRhNjM5NTE4ODg1NjQ2NTgxYTBmZDQ2YWJiMzMyZTkwYWJkODp7Il9hdXRoX3VzZXJfaGFzaCI6ImNhYjIyMDM0ZjRhNWJjZDJmOWEyMDBlZjgxZjZjOTRiYzcyODAzMzMiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIyIn0=','2017-07-25 13:01:50'),('ssg7rurnp5as8czagr4qsw55sstd0j2h','MGViOWRhNjM5NTE4ODg1NjQ2NTgxYTBmZDQ2YWJiMzMyZTkwYWJkODp7Il9hdXRoX3VzZXJfaGFzaCI6ImNhYjIyMDM0ZjRhNWJjZDJmOWEyMDBlZjgxZjZjOTRiYzcyODAzMzMiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIyIn0=','2018-06-22 14:57:58');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vouchers_batch`
--

DROP TABLE IF EXISTS `vouchers_batch`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vouchers_batch` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `value` decimal(4,2) NOT NULL,
  `quantity` smallint(5) unsigned NOT NULL,
  `date_created` datetime NOT NULL,
  `is_downloaded` tinyint(1) NOT NULL,
  `voucher_type` varchar(3) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `vouchers_batch_e8701ad4` (`user_id`),
  CONSTRAINT `vouchers_batch_user_id_40269b6536e84c6f_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=55 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vouchers_batch`
--

LOCK TABLES `vouchers_batch` WRITE;
/*!40000 ALTER TABLE `vouchers_batch` DISABLE KEYS */;
INSERT INTO `vouchers_batch` VALUES (52,1.00,20,'2017-05-27 14:27:46',0,'INS',2),(53,2.00,20,'2018-06-06 13:02:57',0,'STD',2),(54,5.00,50,'2018-06-08 14:53:30',0,'STD',2);
/*!40000 ALTER TABLE `vouchers_batch` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vouchers_voucherinstant`
--

DROP TABLE IF EXISTS `vouchers_voucherinstant`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vouchers_voucherinstant` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `value` decimal(4,2) NOT NULL,
  `date_created` datetime NOT NULL,
  `is_valid` tinyint(1) NOT NULL,
  `is_sold` tinyint(1) NOT NULL,
  `username` varchar(24) NOT NULL,
  `password` varchar(6) NOT NULL,
  `batch_id` int(11) NOT NULL,
  `sold_to` smallint(5) unsigned DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `vouchers_voucherinstant_username_2058490bcc469507_uniq` (`username`),
  KEY `vouchers_voucheri_batch_id_50c98cc10a5f8e8f_fk_vouchers_batch_id` (`batch_id`),
  CONSTRAINT `vouchers_voucheri_batch_id_50c98cc10a5f8e8f_fk_vouchers_batch_id` FOREIGN KEY (`batch_id`) REFERENCES `vouchers_batch` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vouchers_voucherinstant`
--

LOCK TABLES `vouchers_voucherinstant` WRITE;
/*!40000 ALTER TABLE `vouchers_voucherinstant` DISABLE KEYS */;
INSERT INTO `vouchers_voucherinstant` VALUES (8,1.00,'2017-05-27 14:27:46',0,1,'ltat@sw.gh','GCR1',52,1),(9,1.00,'2017-05-27 14:27:47',1,0,'kfzv@sw.gh','49DB',52,NULL),(10,1.00,'2017-05-27 14:27:48',1,0,'jsvt@sw.gh','Z8UI',52,NULL),(11,1.00,'2017-05-27 14:27:49',1,0,'zmnd@sw.gh','5NYV',52,NULL),(12,1.00,'2017-05-27 14:27:50',1,0,'sydq@sw.gh','66K5',52,NULL),(13,1.00,'2017-05-27 14:27:52',1,0,'dide@sw.gh','U4CX',52,NULL),(14,1.00,'2017-05-27 14:27:53',1,0,'oudm@sw.gh','U935',52,NULL),(15,1.00,'2017-05-27 14:27:54',1,0,'pxup@sw.gh','QTDH',52,NULL),(16,1.00,'2017-05-27 14:27:55',1,0,'cftm@sw.gh','7A1Z',52,NULL),(17,1.00,'2017-05-27 14:27:56',1,0,'onqn@sw.gh','3K5C',52,NULL),(18,1.00,'2017-05-27 14:27:57',1,0,'vrya@sw.gh','S5F9',52,NULL),(19,1.00,'2017-05-27 14:27:58',1,0,'vhvn@sw.gh','EVU2',52,NULL),(20,1.00,'2017-05-27 14:27:59',1,0,'xtzn@sw.gh','XFL2',52,NULL),(21,1.00,'2017-05-27 14:28:00',1,0,'eeen@sw.gh','N35T',52,NULL),(22,1.00,'2017-05-27 14:28:01',1,0,'hbgs@sw.gh','FKW6',52,NULL),(23,1.00,'2017-05-27 14:28:02',1,0,'ryqq@sw.gh','PW5B',52,NULL),(24,1.00,'2017-05-27 14:28:03',1,0,'kvos@sw.gh','2VNX',52,NULL),(25,1.00,'2017-05-27 14:28:04',1,0,'hshd@sw.gh','1Z2S',52,NULL),(26,1.00,'2017-05-27 14:28:06',1,0,'yxbb@sw.gh','D2HI',52,NULL),(27,1.00,'2017-05-27 14:28:07',1,0,'pmac@sw.gh','L6SN',52,NULL);
/*!40000 ALTER TABLE `vouchers_voucherinstant` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vouchers_voucherstandard`
--

DROP TABLE IF EXISTS `vouchers_voucherstandard`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vouchers_voucherstandard` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `value` decimal(4,2) NOT NULL,
  `date_created` datetime NOT NULL,
  `is_valid` tinyint(1) NOT NULL,
  `is_sold` tinyint(1) NOT NULL,
  `pin` varchar(14) NOT NULL,
  `batch_id` int(11) NOT NULL,
  `sold_to` smallint(5) unsigned DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `vouchers_vouchers_batch_id_5c6f3062a4190ace_fk_vouchers_batch_id` (`batch_id`),
  CONSTRAINT `vouchers_vouchers_batch_id_5c6f3062a4190ace_fk_vouchers_batch_id` FOREIGN KEY (`batch_id`) REFERENCES `vouchers_batch` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=71 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vouchers_voucherstandard`
--

LOCK TABLES `vouchers_voucherstandard` WRITE;
/*!40000 ALTER TABLE `vouchers_voucherstandard` DISABLE KEYS */;
INSERT INTO `vouchers_voucherstandard` VALUES (1,2.00,'2018-06-06 13:02:57',0,1,'36291020375745',53,1),(2,2.00,'2018-06-06 13:02:57',1,0,'82671699530393',53,NULL),(3,2.00,'2018-06-06 13:02:57',1,0,'51674392600197',53,NULL),(4,2.00,'2018-06-06 13:02:57',1,0,'80221670571926',53,NULL),(5,2.00,'2018-06-06 13:02:57',1,0,'23935728938373',53,NULL),(6,2.00,'2018-06-06 13:02:57',1,0,'42606236727937',53,NULL),(7,2.00,'2018-06-06 13:02:57',1,0,'51591160587968',53,NULL),(8,2.00,'2018-06-06 13:02:57',1,0,'79769550424294',53,NULL),(9,2.00,'2018-06-06 13:02:57',1,0,'57632635836888',53,NULL),(10,2.00,'2018-06-06 13:02:57',1,0,'12513948396253',53,NULL),(11,2.00,'2018-06-06 13:02:57',1,0,'61933918305370',53,NULL),(12,2.00,'2018-06-06 13:02:57',1,0,'04104610392307',53,NULL),(13,2.00,'2018-06-06 13:02:57',1,0,'95800448910569',53,NULL),(14,2.00,'2018-06-06 13:02:57',1,0,'22749343222526',53,NULL),(15,2.00,'2018-06-06 13:02:57',1,0,'07488211100810',53,NULL),(16,2.00,'2018-06-06 13:02:57',1,0,'82299621009271',53,NULL),(17,2.00,'2018-06-06 13:02:57',1,0,'28809094513101',53,NULL),(18,2.00,'2018-06-06 13:02:57',1,0,'11858054050990',53,NULL),(19,2.00,'2018-06-06 13:02:57',1,0,'81654764537603',53,NULL),(20,2.00,'2018-06-06 13:02:57',1,0,'86842207188919',53,NULL),(21,5.00,'2018-06-08 14:53:30',0,1,'49350388933115',54,29),(22,5.00,'2018-06-08 14:53:30',1,0,'15952160208549',54,NULL),(23,5.00,'2018-06-08 14:53:30',1,0,'42191967453243',54,NULL),(24,5.00,'2018-06-08 14:53:30',1,0,'71016245022911',54,NULL),(25,5.00,'2018-06-08 14:53:30',1,0,'23130184165397',54,NULL),(26,5.00,'2018-06-08 14:53:30',1,0,'46916716062909',54,NULL),(27,5.00,'2018-06-08 14:53:30',1,0,'44421975733744',54,NULL),(28,5.00,'2018-06-08 14:53:30',1,0,'39837785654322',54,NULL),(29,5.00,'2018-06-08 14:53:30',1,0,'07780379929054',54,NULL),(30,5.00,'2018-06-08 14:53:31',1,0,'90967487384084',54,NULL),(31,5.00,'2018-06-08 14:53:31',1,0,'00443924672798',54,NULL),(32,5.00,'2018-06-08 14:53:31',1,0,'87154718709251',54,NULL),(33,5.00,'2018-06-08 14:53:31',1,0,'82712219493038',54,NULL),(34,5.00,'2018-06-08 14:53:31',1,0,'65016132167446',54,NULL),(35,5.00,'2018-06-08 14:53:31',1,0,'26689542525259',54,NULL),(36,5.00,'2018-06-08 14:53:31',1,0,'16714832926949',54,NULL),(37,5.00,'2018-06-08 14:53:31',1,0,'44525749947481',54,NULL),(38,5.00,'2018-06-08 14:53:31',1,0,'91661928036813',54,NULL),(39,5.00,'2018-06-08 14:53:31',1,0,'09315177563385',54,NULL),(40,5.00,'2018-06-08 14:53:31',1,0,'34270612964575',54,NULL),(41,5.00,'2018-06-08 14:53:31',1,0,'30611454681108',54,NULL),(42,5.00,'2018-06-08 14:53:31',1,0,'43162255650957',54,NULL),(43,5.00,'2018-06-08 14:53:31',1,0,'23562452821649',54,NULL),(44,5.00,'2018-06-08 14:53:31',1,0,'96216793666315',54,NULL),(45,5.00,'2018-06-08 14:53:31',1,0,'40386412860170',54,NULL),(46,5.00,'2018-06-08 14:53:31',1,0,'76807031436738',54,NULL),(47,5.00,'2018-06-08 14:53:31',1,0,'15734656436429',54,NULL),(48,5.00,'2018-06-08 14:53:31',1,0,'02182750523773',54,NULL),(49,5.00,'2018-06-08 14:53:31',1,0,'33291501472960',54,NULL),(50,5.00,'2018-06-08 14:53:31',1,0,'14767835773682',54,NULL),(51,5.00,'2018-06-08 14:53:31',1,0,'14404304949583',54,NULL),(52,5.00,'2018-06-08 14:53:31',1,0,'38835634319660',54,NULL),(53,5.00,'2018-06-08 14:53:31',1,0,'95082949282159',54,NULL),(54,5.00,'2018-06-08 14:53:31',1,0,'64830320158822',54,NULL),(55,5.00,'2018-06-08 14:53:31',1,0,'36524978854191',54,NULL),(56,5.00,'2018-06-08 14:53:31',1,0,'45039049780996',54,NULL),(57,5.00,'2018-06-08 14:53:31',1,0,'37895664270601',54,NULL),(58,5.00,'2018-06-08 14:53:31',1,0,'61700058756779',54,NULL),(59,5.00,'2018-06-08 14:53:31',1,0,'68522722970754',54,NULL),(60,5.00,'2018-06-08 14:53:31',1,0,'69848511086349',54,NULL),(61,5.00,'2018-06-08 14:53:31',1,0,'56409204837804',54,NULL),(62,5.00,'2018-06-08 14:53:31',1,0,'22229644689917',54,NULL),(63,5.00,'2018-06-08 14:53:31',1,0,'93540752995678',54,NULL),(64,5.00,'2018-06-08 14:53:31',1,0,'07432726890807',54,NULL),(65,5.00,'2018-06-08 14:53:31',1,0,'45401961399879',54,NULL),(66,5.00,'2018-06-08 14:53:31',1,0,'78185042592733',54,NULL),(67,5.00,'2018-06-08 14:53:31',1,0,'52673339795035',54,NULL),(68,5.00,'2018-06-08 14:53:31',1,0,'57163691824277',54,NULL),(69,5.00,'2018-06-08 14:53:31',1,0,'16045981886531',54,NULL),(70,5.00,'2018-06-08 14:53:31',1,0,'87404160819177',54,NULL);
/*!40000 ALTER TABLE `vouchers_voucherstandard` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-06-17 13:36:30
