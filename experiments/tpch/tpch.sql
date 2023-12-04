-- region
CREATE TABLE IF NOT EXISTS region (
  r_regionkey  INT,
  r_name       TEXT,
  PRIMARY KEY (r_regionkey));

-- nation
CREATE TABLE IF NOT EXISTS nation (
  n_nationkey  INT,
  n_name       TEXT,
  n_regionkey  INT,
  PRIMARY KEY (n_nationkey),
  FOREIGN KEY (n_regionkey) REFERENCES region (r_regionkey) ON DELETE CASCADE);

-- supplier
CREATE TABLE IF NOT EXISTS supplier (
  s_suppkey     INT,
  s_name        TEXT,
  s_address     TEXT,
  s_nationkey   INT,
  s_phone       TEXT,
  PRIMARY KEY (s_suppkey),
  FOREIGN KEY (s_nationkey) REFERENCES nation (n_nationkey) ON DELETE CASCADE);

-- customer
CREATE TABLE IF NOT EXISTS customer (
  c_custkey     INT,
  c_name        TEXT,
  c_address     TEXT,
  c_nationkey   INT,
  c_phone       TEXT,
  PRIMARY KEY (c_custkey), 
  FOREIGN KEY (c_nationkey) REFERENCES nation (n_nationkey) ON DELETE CASCADE);

-- part
CREATE TABLE IF NOT EXISTS part (
  p_partkey     INT,
  p_name        TEXT,
  p_brand       TEXT,
  p_size        INT,
  p_retailprice DECIMAL(15,2) ,
  PRIMARY KEY (p_partkey));

-- partsupp
CREATE TABLE IF NOT EXISTS partsupp (
  ps_partkey     INT,
  ps_suppkey     INT,
  ps_supplycost  DECIMAL(15,2),
  PRIMARY KEY (ps_partkey, ps_suppkey),
  FOREIGN KEY (ps_partkey) REFERENCES part (p_partkey) ON DELETE CASCADE,
  FOREIGN KEY (ps_suppkey) REFERENCES supplier (s_suppkey) ON DELETE CASCADE);

-- orders
CREATE TABLE IF NOT EXISTS orders (
  o_orderkey       INT,
  o_custkey        INT,
  o_orderstatus    CHAR(1),
  o_orderdate      DATE,
  PRIMARY KEY (o_orderkey),
  FOREIGN KEY (o_custkey) REFERENCES customer (c_custkey) ON DELETE CASCADE);

-- lineitem
CREATE TABLE IF NOT EXISTS lineitem (
  l_orderkey          INT,
  l_partkey           INT,
  l_suppkey           INT,
  l_linenumber        INT,
  l_quantity          INT,
  l_extendedprice     FLOAT,
  PRIMARY KEY (l_linenumber),
  FOREIGN KEY (l_orderkey) REFERENCES orders (o_orderkey) ON DELETE CASCADE,
  FOREIGN KEY (l_partkey) REFERENCES part (p_partkey) ON DELETE CASCADE,
  FOREIGN KEY (l_suppkey) REFERENCES supplier (s_suppkey) ON DELETE CASCADE);