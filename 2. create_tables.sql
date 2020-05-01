CREATE TABLE tools (
tool_id serial primary key,
tool_name varchar(50) not null unique,
rental_days smallint not null
);

CREATE TABLE jobs (
job_id serial primary key,
job_name varchar(50) not null
);

CREATE TABLE tool_jobs (
tool_id integer references tools(tool_id),
job_id integer references jobs(job_id)
);

CREATE TABLE customers (
customer_id serial primary key,
fname varchar(50) not null,
lname varchar(50) not null,
postcode char(6) not null,
phone char(10) not null,
member_date date not null
);

CREATE TABLE rentals (
tool_id integer references tools(tool_id),
customer_id integer references customers(customer_id), 
rental_date date not null,
return_date date not null,
primary key(tool_id, customer_id)
);
