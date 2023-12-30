CREATE TABLE IF NOT EXISTS level_metadata (
                                  table_name TEXT,
                                  attribute_name TEXT,
                                  level INT,
                                  PRIMARY KEY (table_name, attribute_name, level));

INSERT INTO level_metadata VALUES('tienda', 'idtienda', 0);
INSERT INTO level_metadata VALUES('tienda', 'nombre', 0);
INSERT INTO level_metadata VALUES('tienda', 'reparto', 0);
INSERT INTO level_metadata VALUES('tienda', 'municipio', 1);
INSERT INTO level_metadata VALUES('tienda', 'provincia', 2);
INSERT INTO level_metadata VALUES('producto', 'idproducto', 0);
INSERT INTO level_metadata VALUES('producto', 'marca', 0);
INSERT INTO level_metadata VALUES('producto', 'categoria', 0);
INSERT INTO level_metadata VALUES('producto', 'paquete', 0);
INSERT INTO level_metadata VALUES('producto', 'departamento', 0);
INSERT INTO level_metadata VALUES('producto', 'descripcion', 0);
INSERT INTO level_metadata VALUES('producto', 'producto', 0);
INSERT INTO level_metadata VALUES('producto', 'precio', 0);
INSERT INTO level_metadata VALUES('producto', 'costo', 0);
INSERT INTO level_metadata VALUES('fecha', 'fecha', 0);
INSERT INTO level_metadata VALUES('fecha', 'Dia', 0);
INSERT INTO level_metadata VALUES('fecha', 'Mes', 1);
INSERT INTO level_metadata VALUES('venta', 'idventa', 0);
INSERT INTO level_metadata VALUES('venta', 'idproducto', 0);
INSERT INTO level_metadata VALUES('venta', 'idtienda', 0);
INSERT INTO level_metadata VALUES('venta', 'fecha', 0);
INSERT INTO level_metadata VALUES('venta', 'cantidad_vendida_total', 0);
INSERT INTO level_metadata VALUES('venta', 'importe_total', 0);
INSERT INTO level_metadata VALUES('venta', 'coste_total', 0);
INSERT INTO level_metadata VALUES('venta', 'ganancia', 0);
