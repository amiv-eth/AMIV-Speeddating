-- Adminer 4.3.1 MySQL dump

SET NAMES utf8;
SET time_zone = '+00:00';
SET foreign_key_checks = 0;
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

SET NAMES utf8mb4;

DROP TABLE IF EXISTS `admin_user`;
CREATE TABLE `admin_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(64) DEFAULT NULL,
  `password` varchar(60) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


DROP TABLE IF EXISTS `events`;
CREATE TABLE `events` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Name` varchar(80) DEFAULT NULL,
  `Year` date DEFAULT NULL,
  `SpecialSlots` tinyint(1) DEFAULT NULL,
  `SpecialSlotsName` text,
  `SpecialSlotsDescription` text,
  `Semester` tinyint(1) DEFAULT NULL,
  `CreationTimestamp` datetime DEFAULT NULL,
  `SignupOpen` tinyint(1) DEFAULT NULL,
  `OpenSignupTimestamp` datetime DEFAULT NULL,
  `CloseSignupTimestamp` datetime DEFAULT NULL,
  `Place` varchar(80) DEFAULT NULL,
  `Active` tinyint(1) DEFAULT NULL,
  `ParticipationFee` varchar(80) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


DROP TABLE IF EXISTS `participants`;
CREATE TABLE `participants` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `DefSlot` int(11) DEFAULT NULL,
  `AvailableSlot` varchar(50) DEFAULT NULL,
  `EventID` int(11) DEFAULT NULL,
  `Name` varchar(80) DEFAULT NULL,
  `Prename` varchar(80) DEFAULT NULL,
  `EMail` varchar(120) DEFAULT NULL,
  `MobileNr` varchar(20) DEFAULT NULL,
  `Address` varchar(200) DEFAULT NULL,
  `Birthday` date DEFAULT NULL,
  `Gender` int(11) DEFAULT NULL,
  `StudyCourse` varchar(80) DEFAULT NULL,
  `StudySemester` varchar(80) DEFAULT NULL,
  `PerfectDate` varchar(300) DEFAULT NULL,
  `Fruit` varchar(300) DEFAULT NULL,
  `CreationTimestamp` datetime DEFAULT NULL,
  `Confirmed` int(11) DEFAULT NULL,
  `Present` int(11) DEFAULT NULL,
  `Payed` int(11) DEFAULT NULL,
  `DateNr` int(11) DEFAULT NULL,
  `ConfirmToken` varchar(64) DEFAULT NULL,
  `EditToken` varchar(64) DEFAULT NULL,
  `CancelToken` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `EMail` (`EMail`),
  UNIQUE KEY `ConfirmToken` (`ConfirmToken`),
  UNIQUE KEY `EditToken` (`EditToken`),
  UNIQUE KEY `CancelToken` (`CancelToken`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


DROP TABLE IF EXISTS `time_slots`;
CREATE TABLE `time_slots` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `EventID` int(11) DEFAULT NULL,
  `Date` date DEFAULT NULL,
  `StartTime` datetime DEFAULT NULL,
  `EndTime` datetime DEFAULT NULL,
  `NrCouples` int(11) DEFAULT NULL,
  `AgeRange` int(11) DEFAULT NULL,
  `SpecialSlot` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- 2017-12-02 16:33:57