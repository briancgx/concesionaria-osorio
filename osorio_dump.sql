-- MariaDB dump 10.19  Distrib 10.11.6-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: osorio
-- ------------------------------------------------------
-- Server version	10.11.6-MariaDB-0+deb12u1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Atención_al_Cliente`
--

DROP TABLE IF EXISTS `Atención_al_Cliente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Atención_al_Cliente` (
  `ID_Atención` int(11) NOT NULL AUTO_INCREMENT,
  `ID_Cliente` int(11) DEFAULT NULL,
  `Fecha_atención` date DEFAULT NULL,
  `Descripción` text DEFAULT NULL,
  `Resolución` text DEFAULT NULL,
  PRIMARY KEY (`ID_Atención`),
  KEY `ID_Cliente` (`ID_Cliente`),
  CONSTRAINT `Atención_al_Cliente_ibfk_1` FOREIGN KEY (`ID_Cliente`) REFERENCES `Clientes` (`ID_Cliente`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Atención_al_Cliente`
--

LOCK TABLES `Atención_al_Cliente` WRITE;
/*!40000 ALTER TABLE `Atención_al_Cliente` DISABLE KEYS */;
INSERT INTO `Atención_al_Cliente` VALUES
(1,NULL,'2023-02-20','Consulta sobre saldo de crédito','Se proporcionó el estado del crédito'),
(2,3,'2023-11-15','Reclamo por pagos erróneos','Reclamación resuelta y ajustada en sistema');
/*!40000 ALTER TABLE `Atención_al_Cliente` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Clientes`
--

DROP TABLE IF EXISTS `Clientes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Clientes` (
  `ID_Cliente` int(11) NOT NULL AUTO_INCREMENT,
  `Nombre` varchar(50) NOT NULL,
  `Dirección` varchar(100) DEFAULT NULL,
  `Teléfono` varchar(10) DEFAULT NULL,
  `Correo_electrónico` varchar(50) DEFAULT NULL,
  `Estado_cliente` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`ID_Cliente`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Clientes`
--

LOCK TABLES `Clientes` WRITE;
/*!40000 ALTER TABLE `Clientes` DISABLE KEYS */;
INSERT INTO `Clientes` VALUES
(2,'Ana Rodríguez','Avenida Libertad 890, Guadalajara','3332345678','ana.rodriguez@mail.com','Activo'),
(3,'José López','Callejón del Sol 321, Monterrey','8123456789','jose.lopez@mail.com','Inactivo'),
(4,'Laura Hernández','Paseo de la Reforma 789, CDMX','5534567890','laura.hernandez@mail.com','Inactivo'),
(5,'Miguel García','Avenida Revolución 101, Puebla','2225678901','miguel.garcia@mail.com','Activo'),
(8,'Poncho','Si ','8329428384','poncho@papu.com','Activo');
/*!40000 ALTER TABLE `Clientes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Compra`
--

DROP TABLE IF EXISTS `Compra`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Compra` (
  `ID_Compra` int(11) NOT NULL AUTO_INCREMENT,
  `ID_Cliente` int(11) DEFAULT NULL,
  `ID_Vehículo` int(11) DEFAULT NULL,
  `Fecha_compra` date DEFAULT NULL,
  `Monto` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`ID_Compra`),
  KEY `ID_Cliente` (`ID_Cliente`),
  KEY `ID_Vehículo` (`ID_Vehículo`),
  CONSTRAINT `Compra_ibfk_1` FOREIGN KEY (`ID_Cliente`) REFERENCES `Clientes` (`ID_Cliente`),
  CONSTRAINT `Compra_ibfk_2` FOREIGN KEY (`ID_Vehículo`) REFERENCES `Vehículos` (`ID_Vehículo`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Compra`
--

LOCK TABLES `Compra` WRITE;
/*!40000 ALTER TABLE `Compra` DISABLE KEYS */;
INSERT INTO `Compra` VALUES
(1,NULL,1,'2023-02-15',20000.00),
(2,2,2,'2024-12-01',28000.00),
(3,4,3,'2023-08-25',22000.00);
/*!40000 ALTER TABLE `Compra` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Créditos`
--

DROP TABLE IF EXISTS `Créditos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Créditos` (
  `ID_Crédito` int(11) NOT NULL AUTO_INCREMENT,
  `ID_Cliente` int(11) DEFAULT NULL,
  `Monto_crédito` decimal(10,2) DEFAULT NULL,
  `Interés` decimal(4,2) DEFAULT NULL,
  `Fecha_otorgamiento` date DEFAULT NULL,
  `Estado_Crédito` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`ID_Crédito`),
  KEY `ID_Cliente` (`ID_Cliente`),
  CONSTRAINT `Créditos_ibfk_1` FOREIGN KEY (`ID_Cliente`) REFERENCES `Clientes` (`ID_Cliente`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Créditos`
--

LOCK TABLES `Créditos` WRITE;
/*!40000 ALTER TABLE `Créditos` DISABLE KEYS */;
INSERT INTO `Créditos` VALUES
(1,3,15000.50,7.50,'2023-01-15','Aprobado'),
(2,2,25000.00,6.80,'2023-05-20','Aprobado'),
(4,4,20000.00,7.00,'2023-08-25','Aprobado'),
(5,5,5000.00,9.50,'2024-02-05','Pendiente');
/*!40000 ALTER TABLE `Créditos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Historial_Crédito`
--

DROP TABLE IF EXISTS `Historial_Crédito`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Historial_Crédito` (
  `ID_Historial` int(11) NOT NULL AUTO_INCREMENT,
  `ID_Crédito` int(11) DEFAULT NULL,
  `Fecha_actualización` date DEFAULT NULL,
  `Estado` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`ID_Historial`),
  KEY `ID_Crédito` (`ID_Crédito`),
  CONSTRAINT `Historial_Crédito_ibfk_1` FOREIGN KEY (`ID_Crédito`) REFERENCES `Créditos` (`ID_Crédito`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Historial_Crédito`
--

LOCK TABLES `Historial_Crédito` WRITE;
/*!40000 ALTER TABLE `Historial_Crédito` DISABLE KEYS */;
INSERT INTO `Historial_Crédito` VALUES
(1,1,'2023-02-01','Activo'),
(2,2,'2023-06-01','Pendiente'),
(3,4,'2023-09-15','Activo'),
(4,5,'2024-03-01','Pendiente');
/*!40000 ALTER TABLE `Historial_Crédito` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Inventario`
--

DROP TABLE IF EXISTS `Inventario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Inventario` (
  `ID_Inventario` int(11) NOT NULL AUTO_INCREMENT,
  `ID_Vehículo` int(11) DEFAULT NULL,
  `Ubicación` varchar(50) DEFAULT NULL,
  `Estado` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`ID_Inventario`),
  KEY `ID_Vehículo` (`ID_Vehículo`),
  CONSTRAINT `Inventario_ibfk_1` FOREIGN KEY (`ID_Vehículo`) REFERENCES `Vehículos` (`ID_Vehículo`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Inventario`
--

LOCK TABLES `Inventario` WRITE;
/*!40000 ALTER TABLE `Inventario` DISABLE KEYS */;
INSERT INTO `Inventario` VALUES
(1,1,'Bodega A','No Disponible'),
(2,2,'Bodega B','No Disponible'),
(3,3,'Bodega C','Disponible'),
(4,4,'Bodega D','No Disponible'),
(5,5,'Bodega E','Disponible'),
(6,6,'Bodega F','No Disponible'),
(7,7,'Bodega G','Disponible'),
(8,8,'Bodega H','No Disponible'),
(9,9,'Bodega I','Disponible');
/*!40000 ALTER TABLE `Inventario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Pagos`
--

DROP TABLE IF EXISTS `Pagos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Pagos` (
  `ID_Pago` int(11) NOT NULL AUTO_INCREMENT,
  `ID_Crédito` int(11) DEFAULT NULL,
  `Monto_pago` decimal(10,2) DEFAULT NULL,
  `Fecha_pago` date DEFAULT NULL,
  `Estado` varchar(4) DEFAULT NULL,
  PRIMARY KEY (`ID_Pago`),
  KEY `ID_Crédito` (`ID_Crédito`),
  CONSTRAINT `Pagos_ibfk_1` FOREIGN KEY (`ID_Crédito`) REFERENCES `Créditos` (`ID_Crédito`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Pagos`
--

LOCK TABLES `Pagos` WRITE;
/*!40000 ALTER TABLE `Pagos` DISABLE KEYS */;
INSERT INTO `Pagos` VALUES
(1,1,5000.00,'2023-03-01','debe'),
(2,2,10000.00,'2023-06-15','pago'),
(3,4,20000.00,'2023-09-10','debe'),
(4,5,3000.00,'2024-03-01','pago');
/*!40000 ALTER TABLE `Pagos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Reportes`
--

DROP TABLE IF EXISTS `Reportes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Reportes` (
  `ID_Reporte` int(11) NOT NULL AUTO_INCREMENT,
  `ID_Usuario` int(11) DEFAULT NULL,
  `Fecha` date DEFAULT NULL,
  `Tipo` varchar(50) DEFAULT NULL,
  `Descripción` text DEFAULT NULL,
  PRIMARY KEY (`ID_Reporte`),
  KEY `ID_Usuario` (`ID_Usuario`),
  CONSTRAINT `Reportes_ibfk_1` FOREIGN KEY (`ID_Usuario`) REFERENCES `Usuarios` (`ID_Usuario`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Reportes`
--

LOCK TABLES `Reportes` WRITE;
/*!40000 ALTER TABLE `Reportes` DISABLE KEYS */;
INSERT INTO `Reportes` VALUES
(1,1,'2023-01-10','Análisis de Créditos','Reporte sobre los créditos activos y vencidos.'),
(2,2,'2023-07-05','Reporte de Inventario','Análisis de vehículos disponibles y en venta.'),
(3,3,'2024-03-02','Asesoría','Reporte sobre las ventas y financiamientos en el mes de febrero.');
/*!40000 ALTER TABLE `Reportes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Usuarios`
--

DROP TABLE IF EXISTS `Usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Usuarios` (
  `ID_Usuario` int(11) NOT NULL AUTO_INCREMENT,
  `Nombre_usuario` varchar(50) DEFAULT NULL,
  `Contraseña` varchar(50) DEFAULT NULL,
  `Rol` varchar(20) DEFAULT NULL,
  `Fecha_creacion` datetime NOT NULL DEFAULT current_timestamp(),
  `Ultimo_acceso` datetime NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`ID_Usuario`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Usuarios`
--

LOCK TABLES `Usuarios` WRITE;
/*!40000 ALTER TABLE `Usuarios` DISABLE KEYS */;
INSERT INTO `Usuarios` VALUES
(1,'admin','admin123','Administrador','2024-01-01 10:00:00','2024-01-01 10:00:00'),
(2,'gerente1','gerente123','Gerente','2024-02-01 12:00:00','2024-02-01 12:00:00'),
(3,'asesor1','asesor123','Asesor Ventas','2024-03-01 14:00:00','2024-03-01 14:00:00'),
(4,'asistente1','asistente123','Asistente','2024-12-04 15:09:38','2024-12-04 15:09:38'),
(8,'Poncho','12345678','Administrador','2024-12-04 15:37:00','2024-12-09 03:16:17');
/*!40000 ALTER TABLE `Usuarios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Vehículos`
--

DROP TABLE IF EXISTS `Vehículos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Vehículos` (
  `ID_Vehículo` int(11) NOT NULL AUTO_INCREMENT,
  `ID_Cliente` int(11) DEFAULT NULL,
  `Marca` varchar(50) DEFAULT NULL,
  `Modelo` varchar(50) DEFAULT NULL,
  `Año` int(11) DEFAULT NULL,
  `Tipo` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`ID_Vehículo`),
  KEY `ID_Cliente` (`ID_Cliente`),
  CONSTRAINT `Vehículos_ibfk_1` FOREIGN KEY (`ID_Cliente`) REFERENCES `Clientes` (`ID_Cliente`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Vehículos`
--

LOCK TABLES `Vehículos` WRITE;
/*!40000 ALTER TABLE `Vehículos` DISABLE KEYS */;
INSERT INTO `Vehículos` VALUES
(1,NULL,'Toyota','Corolla',2021,'Sedán'),
(2,2,'Honda','Civic',2020,'Sedán'),
(3,4,'Ford','Focus',2022,'Hatchback'),
(4,5,'Chevrolet','Spark',2019,'Hatchback'),
(5,NULL,'Toyota','Corolla',2020,'Sedán'),
(6,NULL,'Honda','Civic',2019,'Sedán'),
(7,NULL,'Nissan','Altima',2021,'Sedán'),
(8,NULL,'Mazda','3',2020,'Hatchback'),
(9,NULL,'Volkswagen','Jetta',2020,'Sedán'),
(10,NULL,'Ford','Mustang',2017,'Coupé');
/*!40000 ALTER TABLE `Vehículos` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-12-09  3:59:02
