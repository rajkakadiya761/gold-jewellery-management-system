-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 28, 2025 at 06:40 PM
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
-- Table structure for table `products`
--

CREATE TABLE `products` (
  `product_id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `description` varchar(150) NOT NULL,
  `product_weight` float NOT NULL,
  `size` enum('small','medium','large') NOT NULL,
  `category` enum('ring','necklace','earring','bracelet') NOT NULL,
  `photo1` varchar(255) NOT NULL,
  `photo2` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `products`
--

INSERT INTO `products` (`product_id`, `name`, `description`, `product_weight`, `size`, `category`, `photo1`, `photo2`) VALUES
(1, 'Rose Gold CLover Set', 'In life, luck plays a huge factor. Luck combined with hard work and effort reaps great results. The Rose Gold Clover Set is your extra dose of luck.  ', 20, 'medium', 'necklace', 'https://www.giva.co/cdn/shop/products/PD0357_ER0441_1.jpg?v=1674540682&width=713', 'C:\\Users\\krish\\OneDrive\\Desktop\\project jewelery\\static\\images\\ari.png'),
(2, 'Rose Gold Shining Hoop Earrings', 'Early mornings present a completely different version of the world. Cool breeze, birds chirping, it’s a gateway to the best nature has in store! These', 10, 'small', 'earring', 'https://www.giva.co/cdn/shop/products/ER0273_1_8e9f5943-000a-4b7d-a8e4-728a98f31cbf.jpg?v=1627297765&width=713', 'https://www.giva.co/cdn/shop/products/ER0273_2.jpg?v=1709121216&width=713'),
(3, 'krisha', 'azxscdvf', 2.99, 'small', 'ring', 'https://www.giva.co/cdn/shop/products/ER0273_1_8e9f5943-000a-4b7d-a8e4-728a98f31cbf.jpg?v=1627297765&width=713', 'https://www.giva.co/cdn/shop/products/ER0273_2.jpg?v=1709121216&width=713');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`product_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `products`
--
ALTER TABLE `products`
  MODIFY `product_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
