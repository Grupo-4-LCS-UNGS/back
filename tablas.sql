DROP TABLE IF EXISTS asignacion_repuestos;
DROP TABLE IF EXISTS repuesto;
DROP TABLE IF EXISTS mantenimiento;
DROP TABLE IF EXISTS vehiculo;
DROP TABLE IF EXISTS modelo_vehiculo;
DROP TABLE IF EXISTS marca_vehiculo;

CREATE TABLE vehiculo (
	id serial,
	id_modelo int,
	matricula text,
	id_traccar int,
	estado text
);

CREATE TABLE marca_vehiculo (
	id serial,
	nombre text,
	logo text
);

CREATE TABLE modelo_vehiculo(
	id serial,
	id_marca_vehiculo int,
	nombre text
);

CREATE TABLE mantenimiento (
	id serial,
	id_vehiculo int,
	fecha_inicio date,
	fecha_fin date,
	estado text,
	descripcion text
);

CREATE TABLE repuesto (
	id serial,
	id_modelo_vehiculo int,
	nombre text,
	stock int,
	umbral_minimo int
);

CREATE TABLE asignacion_repuestos (
	id_mantenimiento int,
	id_repuesto int
);

ALTER TABLE marca_vehiculo ADD CONSTRAINT marca_vehiculo_pk PRIMARY KEY (id);

ALTER TABLE modelo_vehiculo ADD CONSTRAINT modelo_vehiculo_pk PRIMARY KEY (id);
ALTER TABLE modelo_vehiculo ADD CONSTRAINT modelo_vehiculo_id_marca_vehiculo_fk FOREIGN KEY (id_marca_vehiculo) REFERENCES marca_vehiculo(id);

ALTER TABLE vehiculo ADD CONSTRAINT vehiculo_pk PRIMARY KEY (id);
ALTER TABLE vehiculo ADD CONSTRAINT vehiculo_id_modelo_fk FOREIGN KEY (id_modelo) REFERENCES modelo_vehiculo(id);

ALTER TABLE mantenimiento ADD CONSTRAINT mantenimiento_pk PRIMARY KEY (id);
ALTER TABLE mantenimiento ADD CONSTRAINT mantenimiento_id_vehiculo_fk FOREIGN KEY (id_vehiculo) REFERENCES vehiculo(id);

ALTER TABLE repuesto ADD CONSTRAINT repuesto_pk PRIMARY KEY (id);
ALTER TABLE repuesto ADD CONSTRAINT repuesto_id_modelo_vehiculo_fk FOREIGN KEY (id_modelo_vehiculo) REFERENCES modelo_vehiculo(id);

ALTER TABLE asignacion_repuestos ADD CONSTRAINT asignacion_repuestos_pk PRIMARY KEY (id_mantenimiento, id_repuesto);
ALTER TABLE asignacion_repuestos ADD CONSTRAINT asignacion_repuestos_id_mantenimiento_fk FOREIGN KEY (id_mantenimiento) REFERENCES mantenimiento(id);
ALTER TABLE asignacion_repuestos ADD CONSTRAINT asignacion_repuestos_id_repuesto_fk FOREIGN KEY (id_repuesto) REFERENCES repuesto(id);