SELECT DISTINCT lineitem.l_partkey AS partkey, lineitem.l_suppkey AS supplierkey, orders.o_orderdate AS order_date, SUM(lineitem.l_extendedprice) AS totalpayment, SUM(lineitem.l_quantity) AS totalquantity, SUM(lineitem.l_extendedprice)-(SUM(lineitem.l_quantity)*partsupp.ps_supplycost)-(SUM(lineitem.l_quantity)*part.p_retailprice) AS earnings
FROM lineitem
JOIN orders ON lineitem.l_orderkey = orders.o_orderkey
JOIN partsupp ON lineitem.l_suppkey = partsupp.ps_suppkey AND lineitem.l_partkey = partsupp.ps_partkey
JOIN part ON partsupp.ps_partkey = part.p_partkey
GROUP BY lineitem.l_partkey,lineitem.l_suppkey,orders.o_orderdate,partsupp.ps_supplycost,part.p_retailprice;