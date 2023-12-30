SELECT DISTINCT tienda.idtienda, tienda.nombre, reparto.nombre AS reparto, municipio.nombre AS municipio, provincia.nombre AS provincia
FROM tienda
JOIN reparto ON tienda.idreparto = reparto.idreparto
JOIN municipio ON reparto.idmunicipio = municipio.idmunicipio
JOIN provincia ON municipio.idprovincia = provincia.idprovincia;