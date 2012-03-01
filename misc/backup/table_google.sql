/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
DROP TABLE IF EXISTS `douban_feed`;
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
  `time` int(10) unsigned NOT NULL,
  PRIMARY KEY  (`id`),
  KEY `Index_2` (`cid`,`rid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `douban_feed_owner`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `douban_feed_owner` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `owner` varbinary(64) NOT NULL,
  `topic` varbinary(64) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=binary;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `douban_fetched`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `douban_fetched` (
  `id` int(10) unsigned NOT NULL auto_increment,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=binary;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `douban_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `douban_group` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `name` varchar(64) collate utf8_bin NOT NULL,
  `url` varchar(64) collate utf8_bin NOT NULL,
  `member` int(10) unsigned NOT NULL default '0',
  `leader` varchar(64) collate utf8_bin NOT NULL,
  PRIMARY KEY  (`id`),
  KEY `Index_2` (`url`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `douban_rec`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `douban_rec` (
  `id` bigint(20) unsigned NOT NULL auto_increment,
  `cid` tinyint(3) unsigned NOT NULL,
  `htm` text NOT NULL,
  `user_id` int(10) unsigned NOT NULL,
  `time` int(10) unsigned NOT NULL,
  PRIMARY KEY  (`id`),
  KEY `time` (`time`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `douban_site`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `douban_site` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `name` varchar(64) collate utf8_bin NOT NULL,
  `url` varchar(64) collate utf8_bin NOT NULL,
  PRIMARY KEY  (`id`),
  KEY `Index_2` (`url`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `douban_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `douban_user` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `name` varchar(64) collate utf8_bin NOT NULL,
  `url` varchar(64) collate utf8_bin NOT NULL,
  PRIMARY KEY  (`id`),
  KEY `Index_2` (`url`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `douban_user_feed`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `douban_user_feed` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `rid` int(10) unsigned NOT NULL,
  `user_id` int(10) unsigned NOT NULL,
  `cid` smallint(5) unsigned NOT NULL,
  `vote` tinyint(3) unsigned NOT NULL default '1',
  PRIMARY KEY  (`id`),
  KEY `Index_2` USING BTREE (`rid`,`user_id`,`cid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `douban_user_to_fetch`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `douban_user_to_fetch` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `uid` varbinary(64) NOT NULL,
  PRIMARY KEY  (`id`),
  KEY `Index_2` (`uid`)
) ENGINE=MyISAM DEFAULT CHARSET=binary;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `feed_import`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `feed_import` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `title` varbinary(512) NOT NULL,
  `txt` mediumblob NOT NULL,
  `state` tinyint(3) unsigned NOT NULL default '0',
  `zsite_id` int(10) unsigned NOT NULL default '0',
  `rid` int(10) unsigned NOT NULL default '0',
  `url` varbinary(1024) NOT NULL,
  `tag_id_list` varbinary(1024) NOT NULL,
  `cid` smallint(5) unsigned default NULL,
  `rank` int(10) unsigned NOT NULL default '0',
  `po_meta_user_id` int(10) unsigned NOT NULL default '0',
  PRIMARY KEY  (`id`),
  KEY `Index_2` USING BTREE (`zsite_id`,`state`,`rank`)
) ENGINE=MyISAM DEFAULT CHARSET=binary;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `google_rank`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `google_rank` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `uid` char(32) NOT NULL,
  `update_time` int(10) unsigned NOT NULL,
  `follower` int(10) unsigned NOT NULL default '0',
  `ico` varchar(1024) NOT NULL,
  `name` varchar(256) NOT NULL,
  `txt` text NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `uid` (`uid`),
  KEY `Index_3` (`follower`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `netease_album`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `netease_album` (
  `id` int(11) unsigned NOT NULL,
  `title` varchar(256) default NULL,
  `user_id` int(11) unsigned default NULL,
  `place` varchar(20) default NULL,
  `published` varchar(20) default NULL,
  `url` varchar(1024) default NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `netease_photo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `netease_photo` (
  `id` int(11) unsigned NOT NULL auto_increment,
  `url` varchar(1024) NOT NULL,
  `album_id` int(11) unsigned default NULL,
  PRIMARY KEY  (`id`),
  KEY `url_idx` USING HASH (`url`(333))
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `netease_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `netease_user` (
  `id` int(11) unsigned NOT NULL,
  `url` varchar(1024) default NULL,
  `nickname` varchar(256) default NULL,
  `name` varchar(256) default NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `rss`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rss` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `user_id` int(10) unsigned NOT NULL,
  `rss_id` int(10) unsigned NOT NULL,
  `rss_uid` varbinary(128) NOT NULL,
  `title` varbinary(1024) NOT NULL,
  `txt` mediumblob NOT NULL,
  `state` int(10) unsigned NOT NULL,
  `link` varbinary(1000) NOT NULL,
  `site_id` int(10) unsigned NOT NULL default '0',
  PRIMARY KEY  (`id`),
  UNIQUE KEY `Index_3` (`rss_uid`),
  KEY `Index_2` (`rss_id`),
  KEY `link` (`link`)
) ENGINE=MyISAM DEFAULT CHARSET=binary;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `rss_po`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rss_po` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `user_id` int(10) unsigned NOT NULL,
  `rss_id` int(10) unsigned NOT NULL,
  `rss_uid` varbinary(128) NOT NULL,
  `title` varbinary(1024) NOT NULL,
  `txt` mediumblob NOT NULL,
  `state` int(10) unsigned NOT NULL,
  `link` varbinary(1000) NOT NULL,
  `site_id` int(10) unsigned NOT NULL default '0',
  PRIMARY KEY  (`id`),
  UNIQUE KEY `Index_3` (`rss_uid`),
  KEY `Index_2` (`rss_id`),
  KEY `link` (`link`)
) ENGINE=MyISAM DEFAULT CHARSET=binary;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `spider`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `spider` (
  `id` int(11) NOT NULL auto_increment,
  `title` varbinary(256) NOT NULL,
  `tags` varbinary(1024) NOT NULL,
  `content` blob NOT NULL,
  `author` varbinary(128) NOT NULL,
  `rating` int(11) NOT NULL,
  `url_hash` varbinary(64) NOT NULL,
  `url` blob NOT NULL,
  `reply_list` blob NOT NULL,
  `pic_list` blob NOT NULL,
  PRIMARY KEY  (`id`),
  KEY `new_index` (`url_hash`)
) ENGINE=MyISAM DEFAULT CHARSET=binary;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

