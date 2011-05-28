/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
DROP TABLE IF EXISTS `failed_mq`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `failed_mq` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `body` mediumblob NOT NULL,
  `exc` text CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `func` varbinary(255) NOT NULL,
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `func` (`func`),
  KEY `time` (`time`)
) ENGINE=MyISAM AUTO_INCREMENT=25 DEFAULT CHARSET=binary;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `feed`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `feed` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `zsite_id` int(10) unsigned NOT NULL,
  `cid` tinyint(3) unsigned NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=33 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `feed_entry`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `feed_entry` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `feed_id` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `feed_id` (`feed_id`)
) ENGINE=MyISAM AUTO_INCREMENT=361 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `follow`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `follow` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `from_id` int(10) unsigned NOT NULL,
  `to_id` int(10) unsigned NOT NULL,
  `cid` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `from_id_2` (`from_id`,`to_id`),
  KEY `from_id` (`from_id`,`cid`),
  KEY `to_id` (`to_id`,`cid`),
  KEY `cid` (`cid`)
) ENGINE=MyISAM AUTO_INCREMENT=196 DEFAULT CHARSET=binary;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `gid`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gid` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=386 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `ico`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ico` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `value` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=10024756 DEFAULT CHARSET=binary;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `motto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `motto` (
  `id` int(10) unsigned NOT NULL,
  `value` varchar(48) COLLATE utf8_bin NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `namecard`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `namecard` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int(10) unsigned NOT NULL,
  `pid` bigint(20) unsigned NOT NULL DEFAULT '0',
  `name` varbinary(45) NOT NULL DEFAULT '',
  `phone` varbinary(32) NOT NULL,
  `mail` varbinary(64) NOT NULL,
  `address` varbinary(255) NOT NULL DEFAULT '',
  `state` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`,`state`),
  KEY `pid` (`pid`),
  KEY `mail` (`mail`),
  KEY `name` (`name`)
) ENGINE=MyISAM AUTO_INCREMENT=3738 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `pic`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pic` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int(10) unsigned NOT NULL,
  `create_time` int(10) unsigned NOT NULL DEFAULT '0',
  `cid` tinyint(3) unsigned NOT NULL,
  `admin_id` int(10) unsigned NOT NULL DEFAULT '0',
  `state` tinyint(3) unsigned NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`),
  KEY `AdminId` (`admin_id`),
  KEY `State` (`state`)
) ENGINE=MyISAM AUTO_INCREMENT=19416 DEFAULT CHARSET=binary;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `po`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `po` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(142) CHARACTER SET utf8 NOT NULL,
  `create_time` int(10) unsigned NOT NULL,
  `user_id` int(10) unsigned NOT NULL,
  `cid` tinyint(3) unsigned NOT NULL,
  `state` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Index_2` (`user_id`,`cid`,`state`,`create_time`),
  KEY `Index_3` (`user_id`,`state`,`create_time`) USING BTREE
) ENGINE=MyISAM AUTO_INCREMENT=361 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `po_pic`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `po_pic` (
  `id` int(10) unsigned NOT NULL,
  `user_id` int(10) unsigned NOT NULL,
  `po_id` int(10) unsigned NOT NULL DEFAULT '0',
  `seq` tinyint(3) unsigned NOT NULL,
  `align` tinyint(4) NOT NULL DEFAULT '0',
  `title` varbinary(60) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`,`po_id`,`seq`)
) ENGINE=MyISAM DEFAULT CHARSET=binary;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `rank`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rank` (
  `id` int(10) unsigned NOT NULL,
  `po_id` int(10) unsigned NOT NULL,
  `zsite_id` int(10) unsigned NOT NULL,
  `cid` tinyint(3) unsigned NOT NULL,
  `confidence` smallint(5) unsigned NOT NULL DEFAULT '0',
  `hot` mediumint(9) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `po_id` (`po_id`,`zsite_id`),
  KEY `zsite_id` (`zsite_id`,`confidence`),
  KEY `zsite_id_2` (`zsite_id`,`cid`,`confidence`),
  KEY `zsite_id_3` (`zsite_id`,`hot`),
  KEY `zsite_id_4` (`zsite_id`,`cid`,`hot`)
) ENGINE=MyISAM DEFAULT CHARSET=binary;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `rate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rate` (
  `id` int(10) unsigned NOT NULL,
  `up` smallint(5) unsigned NOT NULL DEFAULT '0',
  `down` smallint(5) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=binary;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `reply`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `reply` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `rid` int(10) unsigned NOT NULL,
  `user_id` int(10) unsigned NOT NULL,
  `state` int(10) unsigned NOT NULL,
  `cid` int(10) unsigned NOT NULL,
  `create_time` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `rs` (`cid`,`rid`,`state`),
  KEY `Index_3` (`user_id`,`state`)
) ENGINE=MyISAM AUTO_INCREMENT=386 DEFAULT CHARSET=binary;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `tag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tag` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `value` varbinary(45) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `Index_2` (`value`) USING BTREE
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `txt`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `txt` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `txt` mediumblob NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=386 DEFAULT CHARSET=binary;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `txt_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `txt_history` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `txt` mediumblob NOT NULL,
  `create_time` int(10) unsigned NOT NULL,
  `rid` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `rc` (`rid`,`create_time`)
) ENGINE=MyISAM AUTO_INCREMENT=15 DEFAULT CHARSET=binary;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `url`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `url` (
  `id` int(10) unsigned NOT NULL,
  `url` char(32) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `url` (`url`)
) ENGINE=MyISAM DEFAULT CHARSET=ascii;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `user_login_time`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_login_time` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int(10) unsigned NOT NULL,
  `create_time` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=32 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `user_mail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_mail` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int(10) unsigned NOT NULL,
  `mail` varchar(255) COLLATE utf8_bin NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `Index_2` (`user_id`,`mail`),
  KEY `mail` (`mail`)
) ENGINE=MyISAM AUTO_INCREMENT=24182 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `user_password`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_password` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `password` binary(32) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=10024772 DEFAULT CHARSET=binary;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `user_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_session` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `value` binary(12) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=10024762 DEFAULT CHARSET=binary;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `user_task`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_task` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int(10) unsigned NOT NULL,
  `cid` int(10) unsigned NOT NULL,
  `rid` int(10) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `Index_2` (`user_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `user_verify`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_verify` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int(10) unsigned NOT NULL,
  `value` binary(16) NOT NULL,
  `create_time` int(10) unsigned NOT NULL,
  `cid` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Index_2` (`user_id`),
  KEY `Index_3` (`create_time`,`cid`)
) ENGINE=MyISAM DEFAULT CHARSET=binary;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `vote`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vote` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int(10) unsigned NOT NULL,
  `po_id` int(10) unsigned NOT NULL,
  `state` tinyint(4) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`po_id`),
  KEY `po_id` (`po_id`,`state`)
) ENGINE=MyISAM DEFAULT CHARSET=binary;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `zpage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `zpage` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varbinary(255) NOT NULL,
  `zsite_id` int(10) unsigned NOT NULL DEFAULT '1',
  `state` tinyint(3) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `zsite_id` (`zsite_id`,`state`)
) ENGINE=MyISAM DEFAULT CHARSET=binary;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `zsite`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `zsite` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varbinary(255) NOT NULL,
  `cid` smallint(5) unsigned NOT NULL DEFAULT '1',
  `state` tinyint(3) unsigned NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=10024770 DEFAULT CHARSET=binary;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

