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
-- Table structure for table `payments`
--

CREATE TABLE `payments` (
  `payment_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `product_ids` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`product_ids`)),
  `quantities` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`quantities`)),
  `transaction_id` varchar(255) DEFAULT NULL,
  `price` decimal(18,2) NOT NULL,
  `payment_date` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `payments`
--

INSERT INTO `payments` (`payment_id`, `user_id`, `product_ids`, `quantities`, `transaction_id`, `price`, `payment_date`) VALUES
(1, 2, '[\"3\", \"12\", \"40\"]', '[2, 2, 1]', 'order_QF40O9l4Z3oOzD', 5960.80, '2025-04-04 17:31:02'),
(2, 13, '[\"2\"]', '[2]', 'order_QF42D5tSPpcPDn', 56520.00, '2025-04-04 17:32:45'),
(3, 2, '[\"5\", \"6\", \"29\"]', '[1, 1, 1]', 'order_QFINTGJ518kcWQ', 111541.00, '2025-04-05 07:34:34'),
(4, 2, '[\"16\"]', '[2]', 'order_QFJYEv0ngD6wPV', 206346.00, '2025-04-05 08:43:27'),
(5, 13, '[\"16\"]', '[1]', 'order_QFJebcwmnCJtMO', 103173.00, '2025-04-05 08:49:29'),
(28, 2, '[\"3\"]', '[1]', 'pay_QPwbAEM3bxIV3l', 269.00, '2025-05-02 05:25:41'),
(29, 2, '[\"3\", \"6\"]', '[1, 1]', 'pay_QPxUQzPX9b1dEZ', 1222.30, '2025-05-02 06:17:55');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `payments`
--
ALTER TABLE `payments`
  ADD PRIMARY KEY (`payment_id`),
  ADD KEY `user_id` (`user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `payments`
--
ALTER TABLE `payments`
  MODIFY `payment_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=30;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `payments`
--
ALTER TABLE `payments`
  ADD CONSTRAINT `payments_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`User_ID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
