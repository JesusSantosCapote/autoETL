SELECT DISTINCT venta.fecha, to_char(venta.fecha, 'Day') AS Dia, to_char(venta.fecha, 'Month') AS Mes
FROM venta;