-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Sep 01, 2023 at 11:38 PM
-- Server version: 10.4.21-MariaDB
-- PHP Version: 7.3.31

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `capstone`
--

-- --------------------------------------------------------

--
-- Table structure for table `clients`
--

CREATE TABLE `clients` (
  `id` int(11) NOT NULL,
  `name` text DEFAULT NULL,
  `phone_number` varchar(255) NOT NULL,
  `password` text DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `email` text DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `clients`
--

INSERT INTO `clients` (`id`, `name`, `phone_number`, `password`, `created_at`, `email`, `updated_at`) VALUES
(1, 'mariam', '12345', '123', '2023-08-09 11:00:00', 'mariam@hotmail.com', NULL),
(2, 'mahdii', '71504530', 'mohamad', '2023-08-19 23:20:03', 'Mahd@hotmail.com', NULL),
(3, 'mahdii', '71514530', '1234', '2023-09-01 21:12:45', 'Mahd@hotmail.com', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `offers`
--

CREATE TABLE `offers` (
  `id` int(11) NOT NULL,
  `order_id` int(11) DEFAULT NULL,
  `supplier_id` int(11) DEFAULT NULL,
  `tank_id` int(11) DEFAULT NULL,
  `price` int(11) DEFAULT NULL,
  `payment_method` text DEFAULT NULL,
  `state` text DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `offers`
--

INSERT INTO `offers` (`id`, `order_id`, `supplier_id`, `tank_id`, `price`, `payment_method`, `state`, `created_at`, `updated_at`) VALUES
(2, 4, 1, 2, 50, 'cash', 'declined', '2023-08-19 15:31:08', '2023-08-28 11:33:30'),
(3, 4, 1, 2, 50, 'cash', 'accepted', '2023-08-19 15:32:09', '2023-08-28 11:33:30'),
(4, 4, 1, 2, NULL, 'cash', 'declined', '2023-08-28 11:31:11', '2023-08-28 11:33:30'),
(5, 4, 1, 2, NULL, 'cash', 'declined', '2023-08-28 11:31:16', '2023-08-28 11:33:30');

-- --------------------------------------------------------

--
-- Table structure for table `orders`
--

CREATE TABLE `orders` (
  `id` int(11) NOT NULL,
  `client_id` int(11) DEFAULT NULL,
  `tank_id` int(11) DEFAULT NULL,
  `payment_method` text DEFAULT NULL,
  `price` int(11) DEFAULT NULL,
  `offer_id` int(11) DEFAULT NULL,
  `supplier_id` int(11) DEFAULT NULL,
  `state` varchar(255) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `orders`
--

INSERT INTO `orders` (`id`, `client_id`, `tank_id`, `payment_method`, `price`, `offer_id`, `supplier_id`, `state`, `created_at`, `updated_at`) VALUES
(4, 1, 2, 'cash', 50, 3, 1, 'accepted', NULL, '2023-08-28 11:33:30'),
(5, 1, 2, 'cash', 50, 2, 1, 'accepted', NULL, '2023-08-26 12:47:47'),
(6, 1, 2, 'cash', NULL, NULL, 1, 'pending', NULL, NULL),
(7, 1, 2, 'cash', NULL, NULL, 1, 'pending', NULL, NULL),
(8, 1, 2, 'cash', NULL, NULL, 1, 'pending', NULL, NULL),
(9, 1, 2, 'cash', 50, 3, 1, 'completed', '2023-08-26 12:25:44', '2023-08-28 11:46:35'),
(10, 1, 2, 'cash', NULL, NULL, NULL, 'pending', '2023-08-30 17:09:08', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `payment_methods`
--

CREATE TABLE `payment_methods` (
  `id` int(11) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `payment_methods`
--

INSERT INTO `payment_methods` (`id`, `name`, `created_at`, `updated_at`) VALUES
(1, 'Cash', '2023-08-09 16:43:56', '2023-08-09 16:43:56'),
(2, 'WISH', '2023-08-09 16:43:56', '2023-08-09 16:43:56');

-- --------------------------------------------------------

--
-- Table structure for table `suppliers`
--

CREATE TABLE `suppliers` (
  `id` int(11) NOT NULL,
  `name` text DEFAULT NULL,
  `phone_number` varchar(255) NOT NULL,
  `region` text DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `email` text DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `suppliers`
--

INSERT INTO `suppliers` (`id`, `name`, `phone_number`, `region`, `created_at`, `email`, `password`, `updated_at`) VALUES
(1, 'Mimo', '123453', 'Bekaa', '2023-08-09 11:00:00', 'mariam@hotmail.com', '321', NULL),
(2, 'mahdii', '71503540', 'Beirut', '2023-08-09 11:00:00', 'Mahd@hotmail.com', '123', NULL),
(3, 'mariam', '12345', 'Tripoli', '2023-08-09 11:00:00', 'mariam@hotmail.com', '1234', NULL),
(4, 'mahdi', '717171', 'Beirut', '2023-08-19 23:34:07', 'mariam@hotmail.com', '321', NULL),
(5, 'Mimo', '71503541', 'Bekaa', '2023-09-01 13:39:15', 'mariam@hotmail.com', '1234', '2023-09-01 13:51:13'),
(6, 'mahdi', '717173', 'Beirut', '2023-09-01 13:51:06', 'mariam@hotmail.com', '1234', NULL),
(7, 'mahdi', '717174', 'Beirut', '2023-09-01 21:31:53', 'mariam@hotmail.com', '$2b$12$6VDrfCQfptUgjtjkLh269.elHpRt8GSbI9/OD2oAIVQA8lqCPjsHO', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `tanks`
--

CREATE TABLE `tanks` (
  `ID` int(11) NOT NULL,
  `type` text DEFAULT NULL,
  `size` int(11) DEFAULT NULL,
  `region` varchar(255) DEFAULT NULL,
  `client_id` int(11) DEFAULT NULL,
  `address` text DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `tanks`
--

INSERT INTO `tanks` (`ID`, `type`, `size`, `region`, `client_id`, `address`, `created_at`, `updated_at`) VALUES
(2, 'tank', 10, 'Beirut', 1, 'beirut', '2023-08-18 22:57:45', '2023-08-18 22:57:45');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `clients`
--
ALTER TABLE `clients`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `ID` (`id`),
  ADD UNIQUE KEY `phone_number` (`phone_number`);

--
-- Indexes for table `offers`
--
ALTER TABLE `offers`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `ID` (`id`),
  ADD KEY `order_id` (`order_id`),
  ADD KEY `supplier_id` (`supplier_id`),
  ADD KEY `tank_id` (`tank_id`);

--
-- Indexes for table `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `ID` (`id`),
  ADD KEY `client_id` (`client_id`),
  ADD KEY `tank_id` (`tank_id`),
  ADD KEY `offer_id` (`offer_id`),
  ADD KEY `supplier_id` (`supplier_id`);

--
-- Indexes for table `payment_methods`
--
ALTER TABLE `payment_methods`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `suppliers`
--
ALTER TABLE `suppliers`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `ID` (`id`),
  ADD UNIQUE KEY `phone_number` (`phone_number`);

--
-- Indexes for table `tanks`
--
ALTER TABLE `tanks`
  ADD PRIMARY KEY (`ID`),
  ADD UNIQUE KEY `ID` (`ID`),
  ADD KEY `owner_id` (`client_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `clients`
--
ALTER TABLE `clients`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `offers`
--
ALTER TABLE `offers`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `orders`
--
ALTER TABLE `orders`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `payment_methods`
--
ALTER TABLE `payment_methods`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `suppliers`
--
ALTER TABLE `suppliers`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `tanks`
--
ALTER TABLE `tanks`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `offers`
--
ALTER TABLE `offers`
  ADD CONSTRAINT `offers_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`ID`) ON UPDATE NO ACTION,
  ADD CONSTRAINT `offers_ibfk_2` FOREIGN KEY (`supplier_id`) REFERENCES `suppliers` (`ID`) ON UPDATE NO ACTION,
  ADD CONSTRAINT `offers_ibfk_3` FOREIGN KEY (`tank_id`) REFERENCES `tanks` (`ID`) ON UPDATE NO ACTION;

--
-- Constraints for table `orders`
--
ALTER TABLE `orders`
  ADD CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`client_id`) REFERENCES `clients` (`ID`),
  ADD CONSTRAINT `orders_ibfk_2` FOREIGN KEY (`tank_id`) REFERENCES `tanks` (`ID`) ON UPDATE NO ACTION,
  ADD CONSTRAINT `orders_ibfk_3` FOREIGN KEY (`offer_id`) REFERENCES `offers` (`ID`) ON UPDATE NO ACTION,
  ADD CONSTRAINT `orders_ibfk_4` FOREIGN KEY (`supplier_id`) REFERENCES `suppliers` (`ID`) ON UPDATE NO ACTION;

--
-- Constraints for table `tanks`
--
ALTER TABLE `tanks`
  ADD CONSTRAINT `tanks_ibfk_1` FOREIGN KEY (`client_id`) REFERENCES `clients` (`ID`) ON UPDATE NO ACTION;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
