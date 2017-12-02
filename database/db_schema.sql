-- Adminer 4.3.1 MySQL dump

SET NAMES utf8;
SET time_zone = '+00:00';
SET foreign_key_checks = 0;
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

SET NAMES utf8mb4;

DROP TABLE IF EXISTS `admin_user`;
CREATE TABLE `admin_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `password` varchar(60) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


DROP TABLE IF EXISTS `events`;
CREATE TABLE `events` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `year` date DEFAULT NULL,
  `special_slots` tinyint(1) DEFAULT NULL,
  `special_slots_name` text COLLATE utf8mb4_unicode_ci,
  `special_slots_description` text COLLATE utf8mb4_unicode_ci,
  `semester` tinyint(1) DEFAULT NULL,
  `creation_timestamp` datetime DEFAULT NULL,
  `signup_open` tinyint(1) DEFAULT NULL,
  `open_signup_timestamp` datetime DEFAULT NULL,
  `close_signup_timestamp` datetime DEFAULT NULL,
  `place` varchar(80) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `active` tinyint(1) DEFAULT NULL,
  `participation_fee` varchar(80) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


DROP TABLE IF EXISTS `participants`;
CREATE TABLE `participants` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `def_slot` int(11) DEFAULT NULL,
  `available_slot` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `event_id` int(11) DEFAULT NULL,
  `name` varchar(80) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `prename` varchar(80) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `email` varchar(120) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `mobile_nr` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `address` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `birthday` date DEFAULT NULL,
  `gender` int(11) DEFAULT NULL,
  `study_course` varchar(80) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `study_semester` varchar(80) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `perfect_date` varchar(300) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `fruit` varchar(300) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `creation_timestamp` datetime DEFAULT NULL,
  `confirmed` int(11) DEFAULT NULL,
  `present` int(11) DEFAULT NULL,
  `payed` int(11) DEFAULT NULL,
  `date_nr` int(11) DEFAULT NULL,
  `confirm_token` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `edit_token` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `cancel_token` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `confirm_token` (`confirm_token`),
  UNIQUE KEY `edit_token` (`edit_token`),
  UNIQUE KEY `cancel_token` (`cancel_token`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


DROP TABLE IF EXISTS `time_slots`;
CREATE TABLE `time_slots` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `event_id` int(11) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `start_time` datetime DEFAULT NULL,
  `end_time` datetime DEFAULT NULL,
  `nr_couples` int(11) DEFAULT NULL,
  `age_range` int(11) DEFAULT NULL,
  `special_slot` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- 2017-12-02 20:24:49