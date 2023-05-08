create database project;
use project;

create table customer(
	id varchar(225) primary key,
    name varchar(15) not null,
    phone varchar(20) not null unique,
    tablepref varchar(20) not null
);

create table menu(
	mid int primary key auto_increment,
    mname varchar(20) unique,
    price float
);

select * from menu;

create table orders(
	oid int primary key auto_increment,
	cid varchar(225) not null,
    mname varchar(50) not null,
    odate timestamp default now(),
    price float,
    foreign key (cid) references customer(id)
);
insert into orders(cid,mname,price) values("shlokg123",(select mname from menu where mid=1),(select price from menu where mid=1));

select * from orders;

create table admin(
	aid int primary key,
    uname varchar(20),
    password varchar(20)
);
insert into admin(aid,uname,password) values(101,'sayali','abc'),(102,'shlok','def');


create table cust(
	cid varchar(20) primary key not null unique,
    phone bigint unique,
    cname varchar(20),
    password varchar(225)
); 

select * from cust;


create table recommendation(
	fid int primary key auto_increment,
    cuisine varchar(30),
    menu varchar(30),
    rating int
);

insert into recommendation(cuisine,menu,rating) values
('chinese','Chicken Chilly',3),
('chinese','Veg Fried Rice',4),
('chinese','Veg Schz Fried Rice',3),
('chinese','Veg Hakka Noodles',4),
('chinese','Veg Schz Noodles',3),
('chinese','Soya Chilly',4),
('pasta','White Sauce Pasta',4),
('pasta','Spinach Pasta',3),
('pasta','Red Sauce Pasta',4),
('Frankie','Veg Frankie',4),
('Frankie','Pav Bhaji Frankie',4),
('Frankie','Mayo Veg Frankie',4),
('Frankie','Noodles Frankie',4),
('Sandwich','Cheese Chilly Sandwich',4),
('Sandwich','Corn Sandwich',3),
('Sandwich','Paneer Tikka Sandwich',5),
('Sandwich','Veg Mayo Sandwich Sandwich',4),
('Burger','Peri Peri Aloo Burger',5),
('Burger','Veg Cheese Burger',4);