#############################################################
# Project: Adlibris database set up
#############################################################

DROP SCHEMA `adlibris` ;

CREATE SCHEMA `adlibris` ;

CREATE TABLE `adlibris`.`books`(
`isbn` BIGINT NOT NULL,
`pages` INT,
`ratingCount`INT,
`rating` FLOAT,
`language`TEXT,
`pubYear`INT(4),
`title` TEXT NOT NULL,
PRIMARY KEY (`isbn`)
);

CREATE TABLE `adlibris`.`books_authors`(
`isbn` BIGINT NOT NULL,
`author` VARCHAR(50),
PRIMARY KEY (`isbn`, `author`)
);

CREATE TABLE `adlibris`.`authors`(
`author` VARCHAR(50),
PRIMARY KEY (`author`)
);

CREATE TABLE `adlibris`.`books_categories`(
`isbn` BIGINT NOT NULL,
`category` VARCHAR(50),
PRIMARY KEY (`isbn`, `category`)
);

CREATE TABLE `adlibris`.`categories`(
`category` VARCHAR(50),
PRIMARY KEY (`category`)
);

ALTER TABLE `adlibris`.`books_authors` ADD FOREIGN KEY (`author`) REFERENCES authors(`author`);
ALTER TABLE `adlibris`.`books_authors` ADD FOREIGN KEY (`isbn`) REFERENCES books(`isbn`);
ALTER TABLE `adlibris`.`books_categories` ADD FOREIGN KEY (`category`) REFERENCES categories(`category`);
ALTER TABLE `adlibris`.`books_categories` ADD FOREIGN KEY (`isbn`) REFERENCES books(`isbn`);


