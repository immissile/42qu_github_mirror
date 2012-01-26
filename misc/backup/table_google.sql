/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `douban_feed` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `cid` int(10) unsigned NOT NULL,
  `rid` int(10) unsigned NOT NULL,
  `rec` int(10) unsigned NOT NULL,
  `like` int(10) unsigned NOT NULL,
  `user_id` int(10) unsigned NOT NULL default '0',
  `topic_id` int(10) unsigned NOT NULL default '0',
  `title` varchar(255) collate utf8_bin NOT NULL,
  `htm` mediumtext collate utf8_bin NOT NULL,
  `state` tinyint(3) unsigned NOT NULL default '0',
  PRIMARY KEY  (`id`),
  KEY `Index_2` (`cid`,`rid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `douban_rec` (
  `id` bigint(20) unsigned NOT NULL auto_increment,
  `cid` tinyint(3) unsigned NOT NULL,
  `htm` text NOT NULL,
  `user_id` int(10) unsigned NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `douban_url` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `cid` int(10) unsigned NOT NULL,
  `rid` int(10) unsigned NOT NULL,
  `url` varchar(64) collate utf8_bin NOT NULL,
  `name` varchar(128) collate utf8_bin NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `Index_3` USING BTREE (`cid`,`rid`,`url`),
  KEY `Index_2` (`cid`,`url`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `douban_user_feed` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `rid` int(10) unsigned NOT NULL,
  `user_id` int(10) unsigned NOT NULL,
  `cid` smallint(5) unsigned NOT NULL,
  PRIMARY KEY  (`id`),
  KEY `Index_2` USING BTREE (`rid`,`user_id`,`cid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;
