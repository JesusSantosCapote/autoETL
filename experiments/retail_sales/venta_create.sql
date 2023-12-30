CREATE TABLE IF NOT EXISTS venta (
idventa serial, 
idproducto INT, 
idtienda INT, 
fecha DATE, 
cantidad_vendida_total INT, 
importe_total INT, 
coste_total INT, 
ganancia INT, 
PRIMARY KEY (idventa), 
FOREIGN KEY (idproducto) REFERENCES producto (idproducto), 
FOREIGN KEY (idtienda) REFERENCES tienda (idtienda), 
FOREIGN KEY (fecha) REFERENCES fecha (fecha), 
UNIQUE(idproducto, idtienda, fecha)
);