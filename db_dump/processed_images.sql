-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 01, 2025 at 03:08 PM
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
-- Table structure for table `processed_images`
--

CREATE TABLE `processed_images` (
  `png_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `png_image` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `processed_images`
--

INSERT INTO `processed_images` (`png_id`, `product_id`, `png_image`) VALUES
(1, 1, 'static/processed_images/p1_1.png'),
(2, 38, 'static/processed_images/p38_1.png'),
(3, 53, 'static/processed_images/p53_1.png'),
(4, 42, 'static/processed_images/p42_1.png'),
(5, 2, 'static/processed_images/p2_1.png'),
(6, 54, 'static/processed_images/p54_1.png'),
(7, 56, 'static/processed_images/p56_1.png'),
(8, 14, 'static/processed_images/p14_2.png'),
(9, 48, 'static/processed_images/p48_2.png'),
(10, 9, 'static/processed_images/p9_1.png'),
(11, 10, 'static/processed_images/p10_2.png'),
(12, 58, 'static/processed_images/p58_1.png'),
(13, 44, 'static/processed_images/p44_3.png'),
(14, 49, 'static/processed_images/p49_2.png'),
(15, 46, 'static/processed_images/p46_1.png'),
(16, 13, 'static/processed_images/p13_1.png'),
(17, 3, 'static/processed_images/p3_1.png'),
(18, 57, 'static/processed_images/p57_3.png'),
(19, 4, 'static/processed_images/p4_1.png'),
(20, 5, 'static/processed_images/p5_2.png'),
(21, 6, 'static/processed_images/p6_2.png'),
(22, 7, 'static/processed_images/p7_1.png'),
(23, 8, 'static/processed_images/p8_2.png'),
(24, 12, 'static/processed_images/p12_1.png'),
(25, 30, 'static/processed_images/p30_2.png'),
(26, 43, 'static/processed_images/p43_2.png'),
(27, 47, 'static/processed_images/p47_1.png'),
(28, 55, 'static/processed_images/p55_2.png'),
(29, 59, 'static/processed_images/p59_1.png'),
(30, 40, 'static/processed_images/p40_2.png'),
(31, 33, 'static/processed_images/p33_2.png'),
(32, 32, 'static/processed_images/p32_2.png'),
(33, 31, 'static/processed_images/p31_2.png'),
(34, 11, 'static/processed_images/p11_2.png'),
(35, 15, 'static/processed_images/p15_2.png'),
(36, 16, 'static/processed_images/p16_2.png'),
(37, 17, 'static/processed_images/p17_2.png'),
(38, 18, 'static/processed_images/p18_2.png'),
(39, 19, 'static/processed_images/p19_2.png'),
(40, 20, 'static/processed_images/p20_2.png'),
(41, 21, 'static/processed_images/p21_3.png'),
(42, 22, 'static/processed_images/p22_2.png'),
(43, 23, 'static/processed_images/p23_1.png'),
(44, 24, 'static/processed_images/p24_2.png'),
(45, 25, 'static/processed_images/p25_2.png'),
(46, 26, 'static/processed_images/p26_2.png'),
(47, 27, 'static/processed_images/p27_2.png'),
(48, 28, 'static/processed_images/p28_2.png'),
(49, 29, 'static/processed_images/p29_2.png'),
(50, 39, 'static/processed_images/p39_2.png'),
(51, 41, 'static/processed_images/p41_2.png'),
(52, 45, 'static/processed_images/p45_2.png'),
(53, 50, 'static/processed_images/p50_2.png'),
(54, 51, 'static/processed_images/p51_1.png'),
(55, 52, 'static/processed_images/p52_2.png'),
(56, 60, 'static/processed_images/p60_2.png'),
(57, 34, 'static/processed_images/p34_2.png'),
(58, 35, 'static/processed_images/p35_2.png'),
(59, 36, 'static/processed_images/p36_2.png'),
(60, 37, 'static/processed_images/p37_2.png');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `processed_images`
--
ALTER TABLE `processed_images`
  ADD PRIMARY KEY (`png_id`),
  ADD KEY `product_id` (`product_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `processed_images`
--
ALTER TABLE `processed_images`
  MODIFY `png_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=61;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `processed_images`
--
ALTER TABLE `processed_images`
  ADD CONSTRAINT `processed_images_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
