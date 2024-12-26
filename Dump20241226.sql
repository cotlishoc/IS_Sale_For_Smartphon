-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: 127.0.0.2    Database: sellsmartphone
-- ------------------------------------------------------
-- Server version	8.0.40

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
-- Table structure for table `brand`
--

DROP TABLE IF EXISTS `brand`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `brand` (
  `Brand_ID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(20) NOT NULL,
  PRIMARY KEY (`Brand_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `brand`
--

LOCK TABLES `brand` WRITE;
/*!40000 ALTER TABLE `brand` DISABLE KEYS */;
INSERT INTO `brand` VALUES (1,'samsunge'),(2,'Apple'),(3,'Honor'),(4,'ы');
/*!40000 ALTER TABLE `brand` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cart`
--

DROP TABLE IF EXISTS `cart`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cart` (
  `Cart_ID` int NOT NULL AUTO_INCREMENT,
  `Client_ID` int NOT NULL,
  `Discount` int DEFAULT '0',
  PRIMARY KEY (`Cart_ID`),
  KEY `Client_ID` (`Client_ID`),
  CONSTRAINT `cart_ibfk_1` FOREIGN KEY (`Client_ID`) REFERENCES `client` (`Client_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cart`
--

LOCK TABLES `cart` WRITE;
/*!40000 ALTER TABLE `cart` DISABLE KEYS */;
/*!40000 ALTER TABLE `cart` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cart_smartphone`
--

DROP TABLE IF EXISTS `cart_smartphone`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cart_smartphone` (
  `Smartphone_ID` int NOT NULL,
  `Cart_ID` int NOT NULL,
  `Quantity` int NOT NULL,
  KEY `Smartphone_ID` (`Smartphone_ID`),
  KEY `Cart_ID` (`Cart_ID`),
  CONSTRAINT `cart_smartphone_ibfk_1` FOREIGN KEY (`Smartphone_ID`) REFERENCES `smartphone` (`Smartphone_ID`),
  CONSTRAINT `cart_smartphone_ibfk_2` FOREIGN KEY (`Cart_ID`) REFERENCES `cart` (`Cart_ID`),
  CONSTRAINT `cart_smartphone_chk_1` CHECK ((`Quantity` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cart_smartphone`
--

LOCK TABLES `cart_smartphone` WRITE;
/*!40000 ALTER TABLE `cart_smartphone` DISABLE KEYS */;
/*!40000 ALTER TABLE `cart_smartphone` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `client`
--

DROP TABLE IF EXISTS `client`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `client` (
  `Client_ID` int NOT NULL AUTO_INCREMENT,
  `Lastname` varchar(50) NOT NULL,
  `Firstname` varchar(50) NOT NULL,
  `Patronymic` varchar(50) DEFAULT NULL,
  `Phone_Number` varchar(17) NOT NULL,
  PRIMARY KEY (`Client_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `client`
--

LOCK TABLES `client` WRITE;
/*!40000 ALTER TABLE `client` DISABLE KEYS */;
/*!40000 ALTER TABLE `client` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `photo`
--

DROP TABLE IF EXISTS `photo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `photo` (
  `Photo_ID` int NOT NULL AUTO_INCREMENT,
  `Photo` blob NOT NULL,
  PRIMARY KEY (`Photo_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `photo`
--

LOCK TABLES `photo` WRITE;
/*!40000 ALTER TABLE `photo` DISABLE KEYS */;
/*!40000 ALTER TABLE `photo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `photosmartphone`
--

DROP TABLE IF EXISTS `photosmartphone`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `photosmartphone` (
  `Smartphone_ID` int NOT NULL,
  `Photo_ID` int NOT NULL,
  PRIMARY KEY (`Smartphone_ID`,`Photo_ID`),
  KEY `Photo_ID` (`Photo_ID`),
  CONSTRAINT `photosmartphone_ibfk_1` FOREIGN KEY (`Smartphone_ID`) REFERENCES `smartphone` (`Smartphone_ID`),
  CONSTRAINT `photosmartphone_ibfk_2` FOREIGN KEY (`Photo_ID`) REFERENCES `photo` (`Photo_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `photosmartphone`
--

LOCK TABLES `photosmartphone` WRITE;
/*!40000 ALTER TABLE `photosmartphone` DISABLE KEYS */;
/*!40000 ALTER TABLE `photosmartphone` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sell`
--

DROP TABLE IF EXISTS `sell`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sell` (
  `Sell_ID` int NOT NULL AUTO_INCREMENT,
  `Date_Sell` date NOT NULL,
  `Client_ID` int NOT NULL,
  `Total_Price` decimal(10,2) NOT NULL,
  PRIMARY KEY (`Sell_ID`),
  KEY `Client_ID` (`Client_ID`),
  CONSTRAINT `sell_ibfk_1` FOREIGN KEY (`Client_ID`) REFERENCES `client` (`Client_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sell`
--

LOCK TABLES `sell` WRITE;
/*!40000 ALTER TABLE `sell` DISABLE KEYS */;
/*!40000 ALTER TABLE `sell` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `smartphone`
--

DROP TABLE IF EXISTS `smartphone`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `smartphone` (
  `Smartphone_ID` int NOT NULL AUTO_INCREMENT,
  `Article` varchar(20) NOT NULL,
  `Model` varchar(20) NOT NULL,
  `Brand_ID` int NOT NULL,
  `Price` decimal(10,2) NOT NULL,
  `Characteristic` text NOT NULL,
  `In_Stock` int NOT NULL,
  PRIMARY KEY (`Smartphone_ID`),
  KEY `Brand_ID` (`Brand_ID`),
  CONSTRAINT `smartphone_ibfk_1` FOREIGN KEY (`Brand_ID`) REFERENCES `brand` (`Brand_ID`),
  CONSTRAINT `smartphone_chk_1` CHECK ((`In_Stock` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `smartphone`
--

LOCK TABLES `smartphone` WRITE;
/*!40000 ALTER TABLE `smartphone` DISABLE KEYS */;
INSERT INTO `smartphone` VALUES (1,'12','S24',1,90999.00,'тип йоу',1),(2,'111111','S23',1,75000.00,'wdfrghytrjh',5),(3,'111111','S23',1,75000.00,'wdfrghytrjh',2),(4,'111111','S23',1,75000.00,'wdfrghytrjh',2),(5,'111111','S23',1,75000.00,'wdfrghytrjh',10),(6,'222222','IPhone 12',2,55000.00,'dsfgdfgbvdfb',1),(7,'213','efrc',1,2.00,'вуыпв',2),(8,'12','S24',1,90999.00,'тип йоу',12),(9,'222222','IPhone 12',2,55000.00,'dsfgdfgbvdfb',1),(10,'12','S24',1,90999.00,'тип йоу',22);
/*!40000 ALTER TABLE `smartphone` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-12-26 11:13:33
