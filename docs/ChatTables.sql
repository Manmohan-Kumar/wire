use conversations;

create Database conversations;

CREATE TABLE IF NOT EXISTS Users (
  user_id INT NOT NULL AUTO_INCREMENT,
  display_name VARCHAR(50) NOT NULL,  
  create_date timestamp,
  phone_number varchar(17) NOT NULL,
  country_phone_code int(5) NOT NULL,
  contact_id INT,
  sender_id varchar(12),
  callback_url varchar(255) ,
  password CHAR(41) NOT NULL,
  telesign_api_key varchar(255),
  telesign_customer_id varchar(255),
  PRIMARY KEY (user_id),
  FOREIGN KEY (contact_id) REFERENCES users(user_id),
  UNIQUE INDEX (phone_number, display_name)
)engine=INNODB ;

Alter Table users Modify create_date timestamp DEFAULT current_timestamp;
Alter Table users add update_date timestamp DEFAULT current_timestamp;

alter Table Country add update_date timestamp DEFAULT current_timestamp;
alter Table Country add create_date timestamp DEFAULT current_timestamp;

CREATE TABLE `chat` (
`chat_id` int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
`message` text,
`sender_id_fk` int(11) NOT NULL,
`receiver_id_fk` int(11) NOT NULL,
`create_date` timestamp DEFAULT CURRENT_TIMESTAMP,
FOREIGN KEY (sender_id_fk) REFERENCES users(user_id),
FOREIGN KEY (receiver_id_fk) REFERENCES users(user_id)
)engine = InnoDB;
Alter Table chat add update_date timestamp DEFAULT current_timestamp;

CREATE TABLE `notifications` (
`notification_id` int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
`message` text,
`sender_id_fk` int(11) NOT NULL,
`receiver_id_fk` int(11) NOT NULL,
`read_flag` boolean Default false,
`create_date` timestamp DEFAULT CURRENT_TIMESTAMP,
`update_date` timestamp DEFAULT CURRENT_TIMESTAMP,
FOREIGN KEY (sender_id_fk) REFERENCES users(user_id),
FOREIGN KEY (receiver_id_fk) REFERENCES users(user_id)
)engine = InnoDB;

DELIMITER $$

DROP PROCEDURE IF EXISTS `receiveSMS` $$
CREATE PROCEDURE `receiveSMS`(
  IN sender_mo_phone VARCHAR(12),
  IN receiver_phone VARCHAR(12), -- has sender_id
  IN message VARCHAR(255),
  OUT status VARCHAR(255)
)
BEGIN 
  SET status :='FAILURE';
  SET @receiver_id_fk := (SELECT user_id  
    FROM users
   WHERE phone_number like receiver_phone);
   
  SET @sender_id_fk := (SELECT user_id  
    FROM users
   WHERE phone_number like sender_mo_phone);
   
   Insert into Chat (message, sender_id_fk, receiver_id_fk) values (message, @sender_id_fk,@receiver_id_fk);   
   Insert into Notifications (message, sender_id_fk, receiver_id_fk) values (message, @sender_id_fk,@receiver_id_fk);
   SET status := 'SUCCESS';
END $$

DELIMITER ;

Insert into users (  display_name ,  phone_number ,  country_phone_code ,  password ,  telesign_api_key ,  telesign_customer_id )
  values('Manmohan', '9023051078', '91', 'abcd', 'dfdsfsd', 'dfsfsdfs');
Insert into users (  display_name ,  phone_number ,  country_phone_code ,  password ,  telesign_api_key ,  telesign_customer_id )
  values('Krishna', '8427434777', '91', 'adbcd', 'dfddsfsd', 'ddfsfsdfs');
Insert into users (  display_name ,  phone_number ,  country_phone_code ,  password ,  telesign_api_key ,  telesign_customer_id )
  values('Gurinder', '8427434777', '91', 'afdbcd', 'dgfddsfsd', 'ddfgsfsdfs');
Insert into users (  display_name ,  phone_number ,  country_phone_code ,  password ,  telesign_api_key ,  telesign_customer_id )
  values('Rohit', '8427434777', '91', 'adbcfd', 'dfddsffsd', 'ddfsffsdfs');
Insert into users (  display_name ,  phone_number ,  country_phone_code ,  password ,  telesign_api_key ,  telesign_customer_id )
  values('Harsh', '8427434777', '91', 'adfbcd', 'dffddsfsd', 'dfdfsfsdfs');
  
Insert into chat (message, sender_id_fk, receiver_id_fk) values ("Hello Brother", 1,2);
Insert into chat (message, sender_id_fk, receiver_id_fk) values ("Hello Mohan", 2,1);
Insert into chat (message, sender_id_fk, receiver_id_fk) values ("kaise hain", 1,2);
Insert into chat (message, sender_id_fk, receiver_id_fk) values ("badiya ji", 2,1);
Insert into chat (message, sender_id_fk, receiver_id_fk) values ("thats great", 2,1);
Insert into chat (message, sender_id_fk, receiver_id_fk) values ("hey man ", 3,4);
Insert into chat (message, sender_id_fk, receiver_id_fk) values ("hey man ", 3,1);
Insert into chat (message, sender_id_fk, receiver_id_fk) values ("nice ", 1,3);
Insert into chat (message, sender_id_fk, receiver_id_fk) values ("thanos is here", 4,3);

Insert into chat (message, sender_id_fk, receiver_id_fk) values ("Hi what is your name", 4,6);
Insert into chat (message, sender_id_fk, receiver_id_fk) values ("Hi what is your name", 4,9);
Insert into chat (message, sender_id_fk, receiver_id_fk) values ("Hi what is your name", 4,10);
Insert into chat (message, sender_id_fk, receiver_id_fk) values ("Hi what is your name", 4,11);

Insert into chat (message, sender_id_fk, receiver_id_fk) values ("My name is Rekha", 6,4);
Insert into chat (message, sender_id_fk, receiver_id_fk) values ("My name is Indu", 9,4);
Insert into chat (message, sender_id_fk, receiver_id_fk) values ("My name is Bala", 10,4);
Insert into chat (message, sender_id_fk, receiver_id_fk) values ("My name is Billu", 11,4);

Insert into chat (message, sender_id_fk, receiver_id_fk) values ("Such a nice name Rekha", 4,6);
Insert into chat (message, sender_id_fk, receiver_id_fk) values ("Such a nice name Indu", 4,9);
Insert into chat (message, sender_id_fk, receiver_id_fk) values ("Such a nice name Bala", 4,10);
Insert into chat (message, sender_id_fk, receiver_id_fk) values ("Such a nice name Billu", 4,11);

Insert into chat(message, sender_id_fk, receiver_id_fk) values ("Oh thanks Mac", 6,4);
Insert into chat(message, sender_id_fk, receiver_id_fk) values ("Oh thanks Mac", 9,4);
Insert into chat(message, sender_id_fk, receiver_id_fk) values ("Oh thanks Mac", 10,4);
Insert into chat(message, sender_id_fk, receiver_id_fk) values ("Oh thanks Mac", 11,4);

select * from chat c
where c.sender_id_fk in (3,4) and c.receiver_id_fk in (3,4) order by chat_id;

-- Contacts table not needed 
CREATE TABLE `contacts` (
`contact_id` int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
`contact_phone_num` varchar(12) NOT NULL,
`contact_country_code` int(5) NOT NULL,
`user_id` int(11) NOT NULL,
`create_date` timestamp DEFAULT CURRENT_TIMESTAMP,
`update_date` timestamp DEFAULT CURRENT_TIMESTAMP,
FOREIGN KEY (user_id) REFERENCES users(user_id)
)engine = InnoDB;

Insert into contacts (contact_phone_num, contact_country_code, user_id) values ("8427334777", 91,2);
Insert into contacts (contact_phone_num, contact_country_code, user_id) values ("8427336777", 91,2);
Insert into contacts (contact_phone_num, contact_country_code, user_id) values ("8427337777", 91,2);
Insert into contacts (contact_phone_num, contact_country_code, user_id) values ("8427384777", 91,2);
Insert into contacts (contact_phone_num, contact_country_code, user_id) values ("8427384797", 91,2);
Insert into contacts (contact_phone_num, contact_country_code, user_id) values ("8427384797", 91,3);
-- fetch contacts based on user phone number and display name
Select c.contact_country_code,c.contact_phone_num,  c.update_date
from Contacts c
inner join Users u on c.user_id = u.user_id
where u.display_name ='Krishna' and u.phone_number = '8427434777'
order by c.update_date desc;

Select * from users;