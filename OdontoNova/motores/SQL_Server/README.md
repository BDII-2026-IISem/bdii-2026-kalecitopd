Módulo de Consultas y Reportes - OdontoNova

Este directorio contiene las consultas SQL analíticas, reportes operativos y cruces multitabla diseñados para la gestión integral del sistema OdontoNova. Estas consultas permiten extraer información clave sobre citas, pacientes, pagos y tratamientos.

📋 Consultas Clave Implementadas

1. Listado completo de citas con detalles cruzados

Permite visualizar todas las citas programadas relacionando la información del paciente, el odontólogo asignado y el sillón odontológico correspondiente mediante múltiples operaciones INNER JOIN.

SELECT 
    c.id AS cita_id,
    p.nombre AS paciente,
    o.nombre AS odontologo,
    s.codigo AS sillon,
    c.fecha_inicio,
    c.fecha_fin,
    c.motivo,
    c.estado
FROM citas c
INNER JOIN pacientes p ON c.paciente_id = p.id
INNER JOIN odontologos o ON c.odontologo_id = o.id
INNER JOIN sillones s ON c.sillon_id = s.id;


2. Reporte financiero de recaudación por método de pago

Agrupa los pagos completados por método, calculando el volumen total de transacciones, la recaudación acumulada y el promedio por transacción utilizando funciones de agregación (COUNT, SUM, AVG) y agrupamiento (GROUP BY).

SELECT 
    metodo AS metodo_pago,
    COUNT(id) AS total_transacciones,
    SUM(monto) AS recaudacion_total,
    AVG(monto) AS promedio_monto
FROM pagos
WHERE estado = 'Completado'
GROUP BY metodo;


3. Historial detallado de tratamientos por paciente

Cruza la información de los planes de tratamiento, los procedimientos realizados, los detalles económicos y los datos personales del paciente para un seguimiento clínico y administrativo preciso.

SELECT 
    p.nombre AS paciente,
    pt.nombre AS plan_tratamiento,
    pr.nombre AS procedimiento_realizado,
    dt.cantidad,
    dt.valor_unitario,
    dt.total
FROM detalles_tratamiento dt
INNER JOIN planes_tratamiento pt ON dt.cabecera_id = pt.id
INNER JOIN pacientes p ON pt.paciente_id = p.id
INNER JOIN procedimientos pr ON dt.item_id = pr.id
WHERE p.id = 1;


4. Resumen de historias clínicas y antecedentes médicos

Consulta los datos de las historias clínicas vinculados directamente con la información de identificación y perfil básico de cada paciente.

SELECT 
    hc.id AS historia_id,
    p.nombre AS paciente,
    p.numero_documento,
    hc.grupo_sanguineo,
    hc.alergias,
    hc.antecedentes
FROM historias_clinicas hc
INNER JOIN pacientes p ON hc.paciente_id = p.id;
