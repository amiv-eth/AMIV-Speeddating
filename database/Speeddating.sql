-- Adminer 4.2.5 MySQL dump

SET NAMES utf8;
SET time_zone = '+00:00';

DROP DATABASE IF EXISTS `Speeddating`;
CREATE DATABASE `Speeddating` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `Speeddating`;

DROP TABLE IF EXISTS `Person`;
CREATE TABLE `Person` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `DefSlot` int(11) DEFAULT NULL,
  `AvailableSlot` tinytext,
  `NonceConfirm` text,
  `NonceCancel` text,
  `Name` tinytext,
  `Prename` int(35) DEFAULT NULL,
  `E-Mail` tinytext,
  `Mobile-Nr` int(11) DEFAULT NULL,
  `Address` text,
  `Birthday` date DEFAULT NULL,
  `Sexe` bit(1) DEFAULT NULL,
  `EventYear` year(4) DEFAULT NULL,
  `StudyCourse` tinytext,
  `Semester` tinytext,
  `PerfectDate` text,
  `SingleSince` tinytext,
  `OnlineDating` text,
  `PickupLine` text,
  `Women` text,
  `Men` text,
  `Advantages` text,
  `NrDates` text,
  `LongestRelationship` text,
  `FindDates` text,
  `Fruit` text,
  PRIMARY KEY (`ID`),
  KEY `DefSlot` (`DefSlot`),
  CONSTRAINT `Person_ibfk_1` FOREIGN KEY (`DefSlot`) REFERENCES `TimeSlots` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `TimeSlots`;
CREATE TABLE `TimeSlots` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `EventYear` year(4) NOT NULL,
  `Date` date NOT NULL,
  `StartTime` time NOT NULL,
  `EndTime` time NOT NULL,
  `NrCouples` int(11) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- 2016-12-10 11:24:06
