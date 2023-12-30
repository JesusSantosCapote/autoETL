SELECT DISTINCT producto.idproducto, marca.nombre AS marca, categoria.nombre AS categoria, tipopaquete.nombre AS paquete, departamento.nombre AS departamento, departamento.descripcion AS descripcion, producto.nombre AS producto, producto.precio, producto.costo
FROM producto
JOIN departamento ON producto.iddepartamento = departamento.iddepartamento
JOIN tipopaquete ON producto.idtipopaquete = tipopaquete.idtipopaquete
JOIN categoria ON producto.idcategoria = categoria.idcategoria
JOIN marca ON producto.idmarca = marca.idmarca;