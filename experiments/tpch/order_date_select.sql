SELECT DISTINCT orders.o_orderdate AS o_date, to_char(orders.o_orderdate, 'Day') AS day, to_char(orders.o_orderdate, 'Month') AS month
FROM orders;