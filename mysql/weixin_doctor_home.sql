-- MySQL dump 10.13  Distrib 8.0.26, for Win64 (x86_64)
--
-- Host: localhost    Database: weixin
-- ------------------------------------------------------
-- Server version	8.0.26

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `doctor_home`
--

DROP TABLE IF EXISTS `doctor_home`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `doctor_home` (
  `doctor-id` varchar(45) NOT NULL,
  `total_source` varchar(45) DEFAULT NULL,
  `m_source` varchar(45) DEFAULT NULL,
  `a_source` varchar(45) DEFAULT NULL,
  `date` char(100) NOT NULL,
  PRIMARY KEY (`doctor-id`,`date`),
  CONSTRAINT `doctor_id` FOREIGN KEY (`doctor-id`) REFERENCES `alldlist` (`doctor_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `doctor_home`
--

LOCK TABLES `doctor_home` WRITE;
/*!40000 ALTER TABLE `doctor_home` DISABLE KEYS */;
INSERT INTO `doctor_home` VALUES ('1001','100','50','50','07-17'),('1001','100','50','50','07-18'),('1001','50','25','25','07-19'),('1001','100','50','50','07-20'),('1001','50','20','30','07-21'),('1001','100','50','50','07-22'),('1001','30','10','20','07-23'),('1002','100','50','50','07-17'),('1002','50','25','25','07-18'),('1002','30','10','20','07-19'),('1002','30','20','10','07-20'),('1002','20','10','10','07-21'),('1002','100','50','50','07-22'),('1002','90','40','50','07-23'),('1003','80','40','40','07-17'),('1003','30','10','20','07-18'),('1003','100','50','50','07-19'),('1003','40','20','20','07-20'),('1003','50','25','25','07-21'),('1003','100','50','50','07-22'),('1003','20','10','10','07-23'),('1004','100','50','50','07-17'),('1004','40','20','20','07-18'),('1004','30','15','15','07-19'),('1004','20','10','10','07-20'),('1004','40','20','20','07-21'),('1004','50','20','30','07-22'),('1004','100','50','50','07-23'),('1005','30','10','20','07-17'),('1005','60','30','30','07-18'),('1005','100','50','50','07-19'),('1005','30','10','20','07-20'),('1005','40','20','20','07-21'),('1005','30','10','20','07-22'),('1005','40','20','20','07-23'),('2001','100','60','40','07-23'),('2003','80','40','40','07-23'),('2004','40','25','15','07-23'),('2005','20','15','5','07-17'),('3001','20','15','5','07-18'),('3002','40','20','20','07-17'),('3003','50','20','30','07-17'),('3004','60','30','30','07-18'),('3005','70','70','0','07-19');
/*!40000 ALTER TABLE `doctor_home` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-07-27 14:59:57
