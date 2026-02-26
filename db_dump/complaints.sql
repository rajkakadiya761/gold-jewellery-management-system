-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 02, 2025 at 08:46 AM
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
-- Table structure for table `complaints`
--

CREATE TABLE `complaints` (
  `complaint_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `message` text NOT NULL,
  `status` enum('pending','inprocess','resolved') DEFAULT 'pending',
  `type` enum('delivery','product','packaging','others') NOT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  `payment_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `complaints`
--

INSERT INTO `complaints` (`complaint_id`, `user_id`, `message`, `status`, `type`, `created_at`, `payment_id`) VALUES
(1, 2, 'The packaging was damaged', 'inprocess', 'delivery', '2025-01-28 13:06:54', 1),
(2, 13, 'product was broekn', 'resolved', 'product', '2025-02-02 20:59:46', 2),
(3, 2, 'trying others', 'pending', 'others', '2025-03-30 17:03:52', 1),
(4, 2, 'checking sql query', 'pending', 'delivery', '2025-03-30 16:40:15', 1),
(5, 13, 'cewou', 'resolved', 'delivery', '2025-04-05 13:53:01', 2),
(6, 2, 'filing complaint', 'inprocess', 'others', '2025-05-02 00:08:55', 1),
(7, 2, 'kricurk', 'pending', 'others', '2025-05-02 11:49:41', 1),
(8, 2, 'kricurk', 'pending', 'others', '2025-05-02 12:09:55', 1),
(9, 2, 'kricurk', 'pending', 'others', '2025-05-02 12:11:47', 1);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `complaints`
--
ALTER TABLE `complaints`
  ADD PRIMARY KEY (`complaint_id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `fk_complaints_payments` (`payment_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `complaints`
--
ALTER TABLE `complaints`
  MODIFY `complaint_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `complaints`
--
ALTER TABLE `complaints`
  ADD CONSTRAINT `complaints_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`User_ID`),
  ADD CONSTRAINT `fk_complaints_payments` FOREIGN KEY (`payment_id`) REFERENCES `payments` (`payment_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
