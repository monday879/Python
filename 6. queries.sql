# Display all customer information.
SELECT * FROM customers;

# Display all tools, including jobs, sorted by jobs.
SELECT tools.tool_id,tool_name,job_name,rental_days FROM tools
LEFT JOIN tool_jobs ON tools.tool_id = tool_jobs.tool_id
LEFT JOIN jobs ON jobs.job_id = tool_jobs.job_id
ORDER BY job_name;

# Display all tools for a given job
SELECT tool_name FROM tools
JOIN tool_jobs ON tools.tool_id = tool_jobs.tool_id
JOIN jobs ON jobs.job_id = tool_jobs.job_id
WHERE job_name = 'roofing';

# Display all rentals, including: customer first and last name, tool name, rental date, rental return date.
SELECT fname,lname,tool_name,rental_date,return_date FROM customers
JOIN rentals ON rentals.customer_id = customers.customer_id
JOIN tools ON rentals.tool_id = tools.tool_id;

# Display all rentals for a given customer.
SELECT fname,lname,tool_name,rental_date,return_date FROM customers
JOIN rentals ON rentals.customer_id = customers.customer_id
JOIN tools ON rentals.tool_id = tools.tool_id
WHERE fname = 'Walter' and lname = 'White';

# Display a rental for a given customer and given tool
SELECT tool_name FROM customers
JOIN rentals ON rentals.customer_id = customers.customer_id
JOIN tools ON rentals.tool_id = tools.tool_id
WHERE fname = 'Walter' and lname = 'White' and tool_name = 'Hammer';

# Display all overdue rentals with customer phone number.
SELECT phone,fname,lname,tool_name,rental_date,return_date FROM customers
JOIN rentals ON rentals.customer_id = customers.customer_id
JOIN tools ON rentals.tool_id = tools.tool_id
WHERE return_date < current_date;
