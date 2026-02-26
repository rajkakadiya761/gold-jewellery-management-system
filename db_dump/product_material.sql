-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 02, 2025 at 08:47 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `arihant`
--

-- --------------------------------------------------------

--
-- Table structure for table `product_material`
--

CREATE TABLE `product_material` (
  `product_material_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `material_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `product_material`
--

INSERT INTO `product_material` (`product_material_id`, `product_id`, `material_id`) VALUES
(1, 1, 1),
(2, 2, 1),
(3, 3, 2),
(4, 37, 1),
(5, 36, 1),
(6, 12, 2),
(7, 13, 1),
(8, 14, 2),
(9, 35, 1),
(10, 34, 2),
(11, 33, 1),
(12, 22, 1),
(13, 30, 2),
(14, 31, 3),
(15, 32, 2),
(16, 21, 1),
(17, 20, 1),
(18, 19, 2),
(19, 18, 1),
(20, 17, 2),
(21, 16, 1),
(22, 25, 1),
(23, 15, 2),
(24, 23, 1),
(25, 24, 1),
(26, 26, 1),
(27, 27, 1),
(28, 28, 3),
(29, 29, 3),
(30, 39, 3),
(31, 41, 3),
(32, 5, 1),
(33, 40, 2),
(34, 4, 2),
(35, 38, 1),
(36, 42, 1),
(37, 43, 1),
(38, 44, 1),
(39, 45, 1),
(40, 46, 2),
(41, 47, 2),
(42, 48, 1),
(43, 49, 1),
(44, 51, 1),
(45, 52, 3),
(46, 60, 2),
(47, 53, 1),
(48, 54, 2),
(49, 55, 2),
(50, 56, 1),
(51, 57, 2),
(52, 6, 2),
(53, 7, 3),
(54, 8, 2),
(55, 58, 2),
(56, 59, 2),
(57, 9, 1),
(58, 10, 2),
(59, 11, 3),
(60, 50, 3);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `product_material`
--
ALTER TABLE `product_material`
  ADD PRIMARY KEY (`product_material_id`),
  ADD KEY `product_id` (`product_id`),
  ADD KEY `material_id` (`material_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `product_material`
--
ALTER TABLE `product_material`
  MODIFY `product_material_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=61;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `product_material`
--
ALTER TABLE `product_material`
  ADD CONSTRAINT `product_material_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `product_material_ibfk_2` FOREIGN KEY (`material_id`) REFERENCES `materials` (`material_id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
