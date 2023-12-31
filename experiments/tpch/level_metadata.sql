CREATE TABLE IF NOT EXISTS level_metadata (
                                  table_name TEXT,
                                  attribute_name TEXT,
                                  level INT,
                                  PRIMARY KEY (table_name, attribute_name, level));

INSERT INTO level_metadata VALUES('supplier', 'suppkey', 0);
INSERT INTO level_metadata VALUES('supplier', 'name', 0);
INSERT INTO level_metadata VALUES('supplier', 'phone', 0);
INSERT INTO level_metadata VALUES('supplier', 'address', 0);
INSERT INTO level_metadata VALUES('supplier', 'nation', 0);
INSERT INTO level_metadata VALUES('supplier', 'region', 1);
INSERT INTO level_metadata VALUES('part', 'p_partkey', 0);
INSERT INTO level_metadata VALUES('part', 'name', 0);
INSERT INTO level_metadata VALUES('part', 'brand', 0);
INSERT INTO level_metadata VALUES('part', 'p_size', 0);
INSERT INTO level_metadata VALUES('part', 'p_retailprice', 0);
INSERT INTO level_metadata VALUES('order_date', 'o_date', 0);
INSERT INTO level_metadata VALUES('order_date', 'day', 0);
INSERT INTO level_metadata VALUES('order_date', 'month', 1);
INSERT INTO level_metadata VALUES('lineitem', 'lnumber', 0);
INSERT INTO level_metadata VALUES('lineitem', 'partkey', 0);
INSERT INTO level_metadata VALUES('lineitem', 'supplierkey', 0);
INSERT INTO level_metadata VALUES('lineitem', 'order_date', 0);
INSERT INTO level_metadata VALUES('lineitem', 'totalpayment', 0);
INSERT INTO level_metadata VALUES('lineitem', 'totalquantity', 0);
INSERT INTO level_metadata VALUES('lineitem', 'earnings', 0);
