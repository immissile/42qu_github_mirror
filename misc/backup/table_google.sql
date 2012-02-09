DROP TABLE IF EXISTS `netease_album`;
CREATE TABLE `netease_album` (
  `id` int(11) unsigned NOT NULL,
  `title` varchar(256) DEFAULT NULL,
  `user_id` int(11) unsigned DEFAULT NULL,
  `place` varchar(20) DEFAULT NULL,
  `published` varchar(20) DEFAULT NULL,
  `url` varchar(1024) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
DROP TABLE IF EXISTS `netease_photo`;
CREATE TABLE `netease_photo` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `url` varchar(1024) NOT NULL,
  `album_id` int(11) unsigned DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `url_idx` (`url`(333)) USING HASH
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
DROP TABLE IF EXISTS `netease_user`;
CREATE TABLE `netease_user` (
  `id` int(11) unsigned NOT NULL,
  `url` varchar(1024) DEFAULT NULL,
  `nickname` varchar(256) DEFAULT NULL,
  `name` varchar(256) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
