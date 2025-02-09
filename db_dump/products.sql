-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 09, 2025 at 11:58 AM
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
  `sizes` varchar(255) NOT NULL,
  `category` enum('ring','bracelete','earrings','necklace') NOT NULL,
  `photo1` varchar(255) NOT NULL,
  `photo2` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `products`
--

INSERT INTO `products` (`product_id`, `name`, `description`, `product_weight`, `sizes`, `category`, `photo1`, `photo2`) VALUES
(1, 'Rose Gold CLover Set', 'In life, luck plays a huge factor. Luck combined with hard work and effort reaps great results. The Rose Gold Clover Set is your extra dose of luck.  ', 20, 'small,medium', 'necklace', 'https://www.giva.co/cdn/shop/products/PD0357_ER0441_1.jpg?v=1674540682&width=713', 'https://www.giva.co/cdn/shop/products/PD0357_2_2_1.jpg?v=1674540683&width=713'),
(2, 'Rose Gold Shining Hoop Earrings', 'Early mornings present a completely different version of the world. Cool breeze, birds chirping, it’s a gateway to the best nature has in store! These', 10, 'small', 'earrings', 'https://www.giva.co/cdn/shop/products/ER0273_1_8e9f5943-000a-4b7d-a8e4-728a98f31cbf.jpg?v=1627297765&width=713', 'https://www.giva.co/cdn/shop/products/ER0273_2.jpg?v=1709121216&width=713'),
(3, 'Silver Glittering Ring', 'This silver ring has a circular zircon studded on a two-layer band, with one sporting zircon.\r\n\r\n-925 Silver \r\n-Diameter: 1.66 cm \r\n-Fixed Size\r\n-Ring', 2.99, 'small, large', 'ring', 'https://www.giva.co/cdn/shop/files/R01716_1.jpg?v=1714655525&width=713', 'https://www.giva.co/cdn/shop/files/R01716_5.jpg?v=1714655525&width=713'),
(12, 'Silver Infinity Heart Bracelet', 'The silver bracelet has a very elegant design of an infinity shape - studded with zircons and 3 smaller hearts juxtaposed into the shape.', 20, 'medium', 'bracelete', 'https://www.giva.co/cdn/shop/files/BR0926_1.jpg?v=1702558764&width=713', 'https://www.giva.co/cdn/shop/files/BR0926_2.jpg?v=1702558764&width=713'),
(13, 'Rose Gold Glinting Crown Ring', 'The Rose Gold Glinting Crown Ring is about regal supremacy vibing with a theme of vintage renaissance.', 30, 'small, medium', 'ring', 'https://www.giva.co/cdn/shop/files/R0187_1.jpg?v=1694158687&width=713', 'https://www.giva.co/cdn/shop/files/R0187_2_11ca102d-a580-40b2-adc5-5c88eab03c1b.jpg?v=1694158687&width=713'),
(14, 'Anushka Sharma Silver Heartlock Bracelet', 'Look at this cute Heartlock Bracelet! Adorable silver shine heart locked with single zircons. The perfect shiny bracelet for everyday cuteness!', 40, 'medium, large', 'bracelete', 'https://www.giva.co/cdn/shop/files/BR046_1.jpg?v=1711690610&width=713', 'https://www.giva.co/cdn/shop/files/BR046_5.jpg?v=1711690610&width=713'),
(38, 'Rose Gold Deer Heart Necklace', 'The Rose Gold Deer Heart Necklace is inspired by the beauty and elegance of the deer.\r\nThe rose gold necklace has a beautiful silhouette of a deer wit', 40, 'small,medium', 'necklace', 'https://www.giva.co/cdn/shop/files/PD01335_1_157a015b-84f1-44e5-80b8-ea57e35b3cba.jpg?v=1733144485&width=713', 'https://www.giva.co/cdn/shop/files/PD01335_3_7aaca174-582e-476b-87d7-6253bcb59da6.jpg?v=1734000009&width=713'),
(39, 'Rose Gold Notre Dame Earrings', 'The Rose Gold Notre Dame Earrings are inspired by Notre Dame and a piece of jewellery that is a priceless antique.\r\nThe rose gold earrings captivate t', 12, 'medium', 'earrings', 'https://www.giva.co/cdn/shop/products/ER01275_5.jpg?v=1696512259&width=713', 'https://www.giva.co/cdn/shop/products/ER01275_1_1.jpg?v=1668087893&width=713'),
(40, 'Silver Elegant Butterflies Bracelet', 'The Silver Elegant Butterflies Bracelet is inspired by the moon showing up unexpectedly on a rainy night with a group of three twinkling stars.', 20, 'small,medium', 'bracelete', 'https://www.giva.co/cdn/shop/files/BR0734_1.jpg?v=1694698910&width=713', 'https://www.giva.co/cdn/shop/files/BR0734_5.jpg?v=1694698910&width=1946'),
(41, 'Silver White Pearl Drop Earrings', 'A pearl-fect pair of earrings to make your moment precious. Add this to your accessory collection today.\r\n', 12, 'small,medium', 'earrings', 'https://www.giva.co/cdn/shop/files/ER003_1.jpg?v=1712928438&width=713', 'https://www.giva.co/cdn/shop/files/ER003_5.jpg?v=1712928438&width=713');

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
  MODIFY `product_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=42;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
