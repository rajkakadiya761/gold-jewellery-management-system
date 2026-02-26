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
-- Table structure for table `productpricing`
--

CREATE TABLE `productpricing` (
  `price_id` bigint(20) UNSIGNED NOT NULL,
  `product_id` int(11) NOT NULL,
  `price` float NOT NULL,
  `quantity` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `productpricing`
--

INSERT INTO `productpricing` (`price_id`, `product_id`, `price`, `quantity`) VALUES
(1, 1, 56520, 12),
(2, 2, 28260, 10),
(3, 3, 269, 3),
(4, 4, 97128, 4),
(5, 5, 94258.8, 2),
(6, 12, 1800, 7),
(7, 13, 242856, 4),
(8, 14, 323768, 1),
(9, 43, 1815, 7),
(10, 44, 115683, 6),
(11, 38, 330211, 3),
(12, 40, 1822.8, 7),
(13, 42, 206382, 4),
(14, 7, 21775.2, 3),
(15, 47, 12345, 3),
(16, 49, 99297.1, 3),
(17, 46, 12345, 3),
(18, 48, 4560, 4),
(19, 36, 61094.8, 3),
(20, 53, 234567, 4),
(21, 54, 636.86, 4),
(22, 55, 24463.8, 4),
(23, 56, 48927.5, 4),
(24, 57, 363.92, 2),
(25, 58, 953.2, 2),
(26, 59, 1239.81, 2),
(27, 37, 113462, 1),
(28, 6, 953.3, 1),
(29, 8, 1430.1, 4),
(30, 9, 145744, 4),
(31, 10, 68567.6, 3),
(32, 11, 24518.5, 1),
(33, 50, 32676, 2),
(34, 60, 1349.04, 0),
(35, 52, 43554.7, 2),
(36, 51, 112176, 2),
(37, 45, 103506, 1),
(38, 41, 27220.3, 5),
(39, 39, 21778.5, 2),
(40, 29, 16328.9, 3),
(41, 28, 24502.1, 2),
(42, 27, 51723.1, 3),
(43, 26, 60289.2, 3),
(44, 25, 103274, 4),
(45, 24, 120476, 3),
(46, 23, 1032590, 5),
(47, 15, 764.4, 6),
(48, 16, 103173, 3),
(49, 17, 1627.24, 2),
(50, 18, 602046, 4),
(51, 19, 1244.36, 2),
(52, 20, 129100, 7),
(53, 21, 951143, 4),
(54, 22, 990042, 3),
(55, 30, 1165.44, 3),
(56, 31, 38895.2, 2),
(57, 32, 874.62, 3),
(58, 33, 97561.8, 3),
(59, 34, 965.6, 5),
(60, 35, 96006.1, 3);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `productpricing`
--
ALTER TABLE `productpricing`
  ADD PRIMARY KEY (`price_id`),
  ADD KEY `product_id` (`product_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `productpricing`
--
ALTER TABLE `productpricing`
  MODIFY `price_id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=61;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `productpricing`
--
ALTER TABLE `productpricing`
  ADD CONSTRAINT `productpricing_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
