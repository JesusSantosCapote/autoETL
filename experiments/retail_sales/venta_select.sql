SELECT DISTINCT venta.idproducto, venta.idtienda, venta.fecha, SUM(venta.cantidad_vendida) AS cantidad_vendida_total, SUM(venta.pago) AS importe_total, producto.Costo*SUM(venta.cantidad_vendida) AS coste_total, SUM(venta.pago)-producto.Costo*SUM(venta.cantidad_vendida) AS ganancia
FROM venta
JOIN producto ON venta.idproducto = producto.idproducto
GROUP BY venta.idproducto,venta.idtienda,venta.fecha,producto.Costo;