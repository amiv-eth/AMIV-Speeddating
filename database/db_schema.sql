-- Adminer 4.3.1 MySQL dump

SET NAMES utf8;
SET time_zone = '+00:00';
SET foreign_key_checks = 0;
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

DROP TABLE IF EXISTS `events`;
CREATE TABLE `events` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Name` tinytext,
  `Semester` tinyint(1) DEFAULT NULL COMMENT '0: FS, 1: HS',
  `ParticipationFee` tinytext,
  `Place` tinytext,
  `Year` year(4) DEFAULT NULL,
  `SpecialSlots` tinyint(1) DEFAULT NULL COMMENT '0: no special slots, 1 special slots',
  `SpecialSlotsName` text,
  `SpecialSlotsDescription` text,
  `CreationTimestamp` timestamp NULL DEFAULT NULL,
  `SignupOpen` tinyint(1) DEFAULT NULL COMMENT '0: closed, 1: open',
  `OpenSignupTimestamp` datetime DEFAULT NULL,
  `CloseSignupTimestamp` datetime DEFAULT NULL,
  `Active` tinyint(1) DEFAULT NULL COMMENT '0: inactive, 1: active',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `participants`;
CREATE TABLE `participants` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `EventID` int(11) DEFAULT NULL,
  `CreationTimestamp` timestamp NULL DEFAULT NULL,
  `DefSlot` int(11) DEFAULT NULL,
  `AvailableSlot` tinytext,
  `Name` tinytext,
  `Prename` tinytext,
  `EMail` tinytext,
  `MobileNr` tinytext,
  `Address` text,
  `Birthday` date DEFAULT NULL,
  `Gender` tinyint(1) DEFAULT NULL,
  `StudyCourse` tinytext,
  `StudySemester` tinytext,
  `PerfectDate` text,
  `Fruit` text,
  `Confirmed` int(11) DEFAULT '1',
  `Present` int(11) DEFAULT '0',
  `Payed` int(11) DEFAULT '0',
  `DateNr` int(20) DEFAULT '0',
  PRIMARY KEY (`ID`),
  KEY `DefSlot` (`DefSlot`),
  CONSTRAINT `participants_ibfk_1` FOREIGN KEY (`DefSlot`) REFERENCES `time_slots` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `time_slots`;
CREATE TABLE `time_slots` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `EventID` int(11) NOT NULL,
  `SpecialSlot` tinyint(1) DEFAULT NULL,
  `Date` date NOT NULL,
  `StartTime` time NOT NULL,
  `EndTime` time NOT NULL,
  `NrCouples` int(11) NOT NULL,
  `AgeRange` int(2) NOT NULL COMMENT '0: 22; 1:22-25; 2: 25, 3:unknown',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- 2017-12-01 22:55:04