-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 09, 2025 at 10:56 AM
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
(1, 1, 3),
(2, 2, 3),
(3, 3, 2),
(6, 12, 2),
(7, 13, 1),
(8, 14, 1);

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
  MODIFY `product_material_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=32;

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
