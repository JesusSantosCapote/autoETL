SELECT part.p_partkey, part.p_name AS name, part.p_brand AS brand, part.p_size
FROM part
GROUP BY part.p_partkey,part.p_name,part.p_brand,part.p_size;