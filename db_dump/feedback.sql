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
-- Table structure for table `feedback`
--

CREATE TABLE `feedback` (
  `feedback_id` int(10) NOT NULL,
  `user_id` int(10) DEFAULT NULL,
  `product_id` int(10) DEFAULT NULL,
  `message` text DEFAULT NULL,
  `feedback_date` date DEFAULT NULL,
  `ratings` int(10) DEFAULT NULL CHECK (`ratings` between 1 and 5)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `feedback`
--

INSERT INTO `feedback` (`feedback_id`, `user_id`, `product_id`, `message`, `feedback_date`, `ratings`) VALUES
(1, 2, 1, 'Great product!', '2025-02-01', 5),
(2, 2, 12, 'Average quality', '2025-02-02', 3),
(3, 2, 1, 'bfdvbfdbfd', '2025-02-01', 3),
(4, 2, 2, 'good job at building the website !! proud of you.', '2025-02-02', 5),
(17, 2, 2, 'one more done', '2025-02-02', 3),
(18, 2, 2, 'bgfdbvfb', '2025-02-02', 4),
(19, 2, 13, 'csdcds', '2025-02-02', 4),
(20, 2, 13, 'hobuo', '2025-02-02', 3),
(21, 2, 13, 'beautiful ring', '2025-02-02', 5),
(22, 13, 13, 'nice one', '2025-02-08', 4);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `feedback`
--
ALTER TABLE `feedback`
  ADD PRIMARY KEY (`feedback_id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `product_id` (`product_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `feedback`
--
ALTER TABLE `feedback`
  MODIFY `feedback_id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `feedback`
--
ALTER TABLE `feedback`
  ADD CONSTRAINT `feedback_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`User_ID`),
  ADD CONSTRAINT `feedback_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
