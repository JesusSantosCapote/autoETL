CREATE TABLE IF NOT EXISTS lineitem (
lnumber serial, 
partkey INT, 
supplierkey INT, 
order_date DATE, 
totalpayment FLOAT, 
totalquantity INT, 
earnings NUMERIC, 
PRIMARY KEY (lnumber), 
FOREIGN KEY (partkey) REFERENCES part (p_partkey), 
FOREIGN KEY (supplierkey) REFERENCES supplier (suppkey), 
FOREIGN KEY (order_date) REFERENCES order_date (o_date), 
UNIQUE(partkey, supplierkey, order_date)
);