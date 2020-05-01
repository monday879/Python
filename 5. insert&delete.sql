INSERT INTO rentals(tool_id, customer_id, rental_date, return_date) VALUES ((SELECT tool_id FROM tools WHERE tool_name = 'Hacksaw' ), (SELECT customer_id FROM customers WHERE fname = 'Walter'), current_date, (current_date + (SELECT rental_days FROM tools WHERE tool_name = 'Hacksaw')));

DELETE FROM rentals WHERE tool_id = 1 and customer_id = 2;