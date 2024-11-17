DROP TABLE IF EXISTS bitacora_asig_operador;
DROP TABLE IF EXISTS asignacion_repuestos;
DROP TABLE IF EXISTS orden_compra;
DROP TABLE IF EXISTS repuesto;
DROP TABLE IF EXISTS mantenimiento;
DROP TABLE IF EXISTS vehiculo;
DROP TABLE IF EXISTS modelo_vehiculo;
DROP TABLE IF EXISTS marca_vehiculo;
DROP TABLE IF EXISTS proveedor;
DROP TABLE IF EXISTS gasto;
DROP TABLE IF EXISTS usuario;
DROP TABLE IF EXISTS cliente;

CREATE TABLE vehiculo (
	id serial,
	id_modelo int,
	id_operador int,
	matricula text UNIQUE NOT NULL,
	id_traccar int,
	estado text
);

CREATE TABLE marca_vehiculo (
	id serial,
	nombre text UNIQUE NOT NULL,
	logo text
);

CREATE TABLE modelo_vehiculo(
	id serial,
	id_marca_vehiculo int,
	nombre text UNIQUE NOT NULL
	litrosx100km DOUBLE PRECISION,
);

CREATE TABLE mantenimiento (
	id serial,
	id_vehiculo int,
	fecha_inicio date,
	fecha_fin date,
	estado text,
	descripcion text,
	tipo text
);

CREATE TABLE repuesto (
	id serial,
	id_proveedor int,
	id_modelo_vehiculo int,
	nombre text,
	stock int,
	umbral_minimo int,
	umbral_maximo int,
	costo DOUBLE PRECISION
);

CREATE TABLE asignacion_repuestos (
	id serial,
	id_mantenimiento int,
	id_repuesto int,
	cantidad int,
	fecha TIMESTAMP
);

CREATE TABLE proveedor (
	id serial,
	nombre text,
	direccion text,
	telefono text,
	email text,
	cuit text UNIQUE NOT NULL
);

CREATE TABLE orden_compra (
	id serial,
	id_repuesto int,
	cantidad int,
	estado text
);

CREATE TABLE usuario (
    id serial,
    nombre text,
    contrasena text,
    rol text
);

CREATE TABLE bitacora_asig_operador (
    id serial,
    id_operador int,
	id_vehiculo int,
    fecha TIMESTAMP,
	tipo text
);

CREATE TABLE cliente (
	id serial,
	cuit int UNIQUE NOT NULL,
	nombre text,
	direccion text,
	email text,
	telefono text
);

CREATE TABLE gasto (
    id SERIAL PRIMARY KEY,
    categoria VARCHAR(50) NOT NULL, -- (mantenimiento, repuestos, combustible, otros)
    fecha DATE NOT NULL,
    monto DECIMAL(10, 2) NOT NULL,
    proveedor_id VARCHAR(100), -- Puede ser NULL si no aplica
    descripcion TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE cliente ADD CONSTRAINT cliente_pk PRIMARY KEY (id);

ALTER TABLE usuario ADD CONSTRAINT usuario_pk PRIMARY KEY (id);

ALTER TABLE proveedor ADD CONSTRAINT proveedor_pk PRIMARY KEY (id);

ALTER TABLE marca_vehiculo ADD CONSTRAINT marca_vehiculo_pk PRIMARY KEY (id);

ALTER TABLE modelo_vehiculo ADD CONSTRAINT modelo_vehiculo_pk PRIMARY KEY (id);
ALTER TABLE modelo_vehiculo ADD CONSTRAINT modelo_vehiculo_id_marca_vehiculo_fk FOREIGN KEY (id_marca_vehiculo) REFERENCES marca_vehiculo(id);

ALTER TABLE vehiculo ADD CONSTRAINT vehiculo_pk PRIMARY KEY (id);
ALTER TABLE vehiculo ADD CONSTRAINT vehiculo_id_modelo_fk FOREIGN KEY (id_modelo) REFERENCES modelo_vehiculo(id);
ALTER TABLE vehiculo ADD CONSTRAINT vehiculo_id_operador_fk FOREIGN KEY (id_operador) REFERENCES usuario(id);

ALTER TABLE mantenimiento ADD CONSTRAINT mantenimiento_pk PRIMARY KEY (id);
ALTER TABLE mantenimiento ADD CONSTRAINT mantenimiento_id_vehiculo_fk FOREIGN KEY (id_vehiculo) REFERENCES vehiculo(id);

ALTER TABLE repuesto ADD CONSTRAINT repuesto_pk PRIMARY KEY (id);
ALTER TABLE repuesto ADD CONSTRAINT repuesto_id_proveedor_fk FOREIGN KEY (id_proveedor) REFERENCES proveedor(id);
ALTER TABLE repuesto ADD CONSTRAINT repuesto_id_modelo_vehiculo_fk FOREIGN KEY (id_modelo_vehiculo) REFERENCES modelo_vehiculo(id);

ALTER TABLE asignacion_repuestos ADD CONSTRAINT asignacion_repuestos_pk PRIMARY KEY (id);
ALTER TABLE asignacion_repuestos ADD CONSTRAINT asignacion_repuestos_id_mantenimiento_fk FOREIGN KEY (id_mantenimiento) REFERENCES mantenimiento(id);
ALTER TABLE asignacion_repuestos ADD CONSTRAINT asignacion_repuestos_id_repuesto_fk FOREIGN KEY (id_repuesto) REFERENCES repuesto(id);

ALTER TABLE orden_compra ADD CONSTRAINT orden_compra_pk PRIMARY KEY (id);
ALTER TABLE orden_compra ADD CONSTRAINT orden_compra_id_repuesto_fk FOREIGN KEY (id_repuesto) REFERENCES repuesto(id);

ALTER TABLE bitacora_asig_operador ADD CONSTRAINT bitacora_asig_operador_pk PRIMARY KEY (id);
ALTER TABLE bitacora_asig_operador ADD CONSTRAINT bitacora_asig_operador_id_operador_fk FOREIGN KEY (id_operador) REFERENCES usuario(id);
ALTER TABLE bitacora_asig_operador ADD CONSTRAINT bitacora_asig_operador_id_vehiculo_fk FOREIGN KEY (id_vehiculo) REFERENCES vehiculo(id);
