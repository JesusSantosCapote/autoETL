SELECT DISTINCT supplier.s_suppkey AS suppkey, supplier.s_name AS name, supplier.s_phone AS phone, supplier.s_address AS address, nation.n_name AS nation, region.r_name AS region
FROM supplier
JOIN nation ON supplier.s_nationkey = nation.n_nationkey
JOIN region ON nation.n_regionkey = region.r_regionkey;