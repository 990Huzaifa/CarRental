-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 22, 2023 at 12:36 PM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `car_rental`
--

-- --------------------------------------------------------

--
-- Table structure for table `booking`
--

CREATE TABLE `booking` (
  `id` int(11) NOT NULL,
  `car_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `departure` varchar(100) NOT NULL,
  `arrival` varchar(100) NOT NULL,
  `phone` bigint(20) NOT NULL,
  `pickup_date` varchar(40) NOT NULL,
  `pickup_time` varchar(40) NOT NULL,
  `service_id` int(11) NOT NULL,
  `t_amount` float NOT NULL,
  `status` varchar(40) NOT NULL,
  `date` date NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `booking`
--

INSERT INTO `booking` (`id`, `car_id`, `user_id`, `departure`, `arrival`, `phone`, `pickup_date`, `pickup_time`, `service_id`, `t_amount`, `status`, `date`) VALUES
(6, 6, 1, 'abc', 'xyz', 3482352412, '2023-12-22', '18:47', 2, 8000, 'cancel', '2023-12-19'),
(7, 4, 3, 'ho no 34 full add', 'h no 23 full add', 3123452785, '2023-12-14', '14:10', 4, 5200, 'request', '2023-12-20');

-- --------------------------------------------------------

--
-- Table structure for table `brand`
--

CREATE TABLE `brand` (
  `id` int(11) NOT NULL,
  `name` varchar(40) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `brand`
--

INSERT INTO `brand` (`id`, `name`) VALUES
(1, 'Honda'),
(2, 'Toyota'),
(4, 'KIA'),
(5, 'Daihatsu');

-- --------------------------------------------------------

--
-- Table structure for table `car`
--

CREATE TABLE `car` (
  `id` int(11) NOT NULL,
  `brand_id` int(11) NOT NULL,
  `name` varchar(40) NOT NULL,
  `extra_charges` double NOT NULL,
  `seaters` int(11) NOT NULL,
  `model` int(11) NOT NULL,
  `img` varchar(225) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `car`
--

INSERT INTO `car` (`id`, `brand_id`, `name`, `extra_charges`, `seaters`, `model`, `img`) VALUES
(4, 1, 'City', 1200, 4, 2022, '20210917123645_Honda_city_hybrid_front.jpg'),
(5, 2, 'Corolla GLI', 0, 4, 2020, 'WhatsApp_Image_2023-12-13_at_23.17.50_5ebbac2e.jpg'),
(6, 1, 'Civic', 1500, 4, 2021, 'WhatsApp_Image_2023-12-13_at_22.38.10_4868fddd.jpg'),
(7, 4, 'Sportage', 2000, 5, 2023, 'file_2023-12-21_06.54.30.png'),
(8, 2, 'Yaris', 0, 4, 2023, 'Toyota-Yaris-GLI-CVT-1.3-Price-in-Pakistan-2023.png'),
(9, 4, 'Stonic', 1800, 5, 2023, 'WhatsApp_Image_2023-12-21_at_11.53.21_b300d85b.jpg'),
(10, 1, 'BRV', 1800, 5, 2023, '2023-honda-br-v-17-1668995280.jpg'),
(11, 4, 'Picanto', 1000, 4, 2023, 'https___www.carscoops.com_wp-content_uploads_2023_07_2023-Kia-Picanto-GT-Line-1-1024x576-1-1.jpg'),
(12, 5, 'Copen', 1000, 2, 2023, 'IMG_7608_50.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `contact`
--

CREATE TABLE `contact` (
  `id` int(11) NOT NULL,
  `name` varchar(40) NOT NULL,
  `email` varchar(40) NOT NULL,
  `subject` varchar(225) NOT NULL,
  `message` varchar(525) NOT NULL,
  `date` date NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `contact`
--

INSERT INTO `contact` (`id`, `name`, `email`, `subject`, `message`, `date`) VALUES
(1, 'esha', 'esha123@gmail.com', 'Location issue', 'non', '2023-12-20'),
(2, 'faraz', 'faraz123@gmail.com', 'some issue', 'not yet', '2023-12-20'),
(3, 'faraz', 'faraz123@gmail.com', 'some issue', 'not yet', '2023-12-20');

-- --------------------------------------------------------

--
-- Table structure for table `contact_details`
--

CREATE TABLE `contact_details` (
  `id` int(11) NOT NULL,
  `email` varchar(40) NOT NULL,
  `phone` bigint(20) NOT NULL,
  `location` varchar(225) NOT NULL,
  `form` varchar(40) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `contact_details`
--

INSERT INTO `contact_details` (`id`, `email`, `phone`, `location`, `form`) VALUES
(1, 'rentalcar@gmail.com', 3001234534, 'DHA phase 2 karachi', 'checked');

-- --------------------------------------------------------

--
-- Table structure for table `general`
--

CREATE TABLE `general` (
  `id` int(11) NOT NULL,
  `site_title` varchar(40) NOT NULL,
  `site_description` varchar(512) NOT NULL,
  `site_tag` varchar(512) NOT NULL,
  `mm` varchar(40) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `general`
--

INSERT INTO `general` (`id`, `site_title`, `site_description`, `site_tag`, `mm`) VALUES
(1, 'Car Rental', 'this is..', 'car rental,car booking', '');

-- --------------------------------------------------------

--
-- Table structure for table `services`
--

CREATE TABLE `services` (
  `id` int(11) NOT NULL,
  `name` varchar(200) NOT NULL,
  `price` double NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `services`
--

INSERT INTO `services` (`id`, `name`, `price`) VALUES
(2, 'hyd to khi', 6500),
(4, 'wedding ceremony', 4000),
(5, 'khi tour per day', 10000);

-- --------------------------------------------------------

--
-- Table structure for table `testimonials`
--

CREATE TABLE `testimonials` (
  `id` int(11) NOT NULL,
  `fullname` varchar(40) NOT NULL,
  `occupation` varchar(40) NOT NULL,
  `message` varchar(525) NOT NULL,
  `status` varchar(40) NOT NULL,
  `date` date NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `testimonials`
--

INSERT INTO `testimonials` (`id`, `fullname`, `occupation`, `message`, `status`, `date`) VALUES
(1, 'ansh kumar', 'Markiting manager', 'This website is one of the best website for the customer. prices is afordable and their services is so comfortable. I love their services, their timings.', 'active', '2023-12-20');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `fullname` varchar(40) NOT NULL,
  `email` varchar(40) NOT NULL,
  `phone` bigint(20) NOT NULL,
  `password` varchar(225) NOT NULL,
  `account_type` varchar(40) NOT NULL,
  `date` date NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `fullname`, `email`, `phone`, `password`, `account_type`, `date`) VALUES
(1, 'Ansh kumar', 'anshkumar@gmail.com', 3482352412, '$pbkdf2-sha256$29000$DUHoPSckRMj5vxdCaG0NIQ$k66Wo6knvOfjAUTsKmZVY0hEwALH4p3Vxhn9wDT43lw', 'customer', '2023-12-06'),
(2, 'admin', 'admin@gmail.com', 31234567899, '$pbkdf2-sha256$29000$AECI0bo3hvBe651zTimFEA$ufbQFp18ZUUpHUitxSRd0UsqlJYGHrUeUO/Cgk4dNCs', 'admin', '2023-12-12'),
(3, 'saad ali', 'saadali123@gmail.com', 3123452785, '$pbkdf2-sha256$29000$BwBgzHmPMUao9T4npLRWyg$LwcQ17BPshwz34I6e5WbwI8SmivZlgm2yVQIcnkf/WI', 'customer', '2023-12-20');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `booking`
--
ALTER TABLE `booking`
  ADD PRIMARY KEY (`id`),
  ADD KEY `car_id` (`car_id`),
  ADD KEY `service_id` (`service_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `brand`
--
ALTER TABLE `brand`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `car`
--
ALTER TABLE `car`
  ADD PRIMARY KEY (`id`),
  ADD KEY `brand_id` (`brand_id`);

--
-- Indexes for table `contact`
--
ALTER TABLE `contact`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `contact_details`
--
ALTER TABLE `contact_details`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `general`
--
ALTER TABLE `general`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `services`
--
ALTER TABLE `services`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `testimonials`
--
ALTER TABLE `testimonials`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `booking`
--
ALTER TABLE `booking`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `brand`
--
ALTER TABLE `brand`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `car`
--
ALTER TABLE `car`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `contact`
--
ALTER TABLE `contact`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `contact_details`
--
ALTER TABLE `contact_details`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `general`
--
ALTER TABLE `general`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `services`
--
ALTER TABLE `services`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `testimonials`
--
ALTER TABLE `testimonials`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `booking`
--
ALTER TABLE `booking`
  ADD CONSTRAINT `booking_ibfk_1` FOREIGN KEY (`car_id`) REFERENCES `car` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `booking_ibfk_2` FOREIGN KEY (`service_id`) REFERENCES `services` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `booking_ibfk_3` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `car`
--
ALTER TABLE `car`
  ADD CONSTRAINT `car_ibfk_1` FOREIGN KEY (`brand_id`) REFERENCES `brand` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
