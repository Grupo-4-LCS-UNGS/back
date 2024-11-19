CREATE OR REPLACE FUNCTION generarOrdenCompra() RETURNS TRIGGER AS $$
DECLARE
	cant_compra int;
BEGIN
	IF NEW.stock < NEW.umbral_minimo THEN
		cant_compra := NEW.umbral_maximo - NEW.stock;
		INSERT INTO orden_compra (id_repuesto, cantidad, estado)
		VALUES(NEW.id, cant_compra, 'pendiente');
		NEW.stock := NEW.umbral_maximo;
	END IF;
	RETURN NEW;
END;
$$ LANGUAGE plpgsql;
CREATE OR REPLACE TRIGGER generarOrdenCompra_trg
BEFORE UPDATE ON repuesto
FOR EACH ROW
EXECUTE FUNCTION generarOrdenCompra();

CREATE OR REPLACE FUNCTION actualizar_bitacora_operador() RETURNS TRIGGER AS $$
DECLARE
	tipo text;
	id_op_aux int;
BEGIN
	IF NEW.id_operador = OLD.id_operador THEN
		RETURN NEW;
	END IF;
	IF NEW.id_operador IS NULL THEN
		tipo := 'DESASIGNACION';
		id_op_aux := OLD.id_operador;
	ELSE
		tipo := 'ASIGNACION';
		id_op_aux := NEW.id_operador;
	END IF;
	INSERT INTO bitacora_asig_operador (id_operador, id_vehiculo, fecha, tipo)
	VALUES (id_op_aux, OLD.id, NOW(), tipo);
	RETURN NEW;
END;
$$ LANGUAGE plpgsql;
CREATE OR REPLACE TRIGGER actualizar_bitacora_operador_trg
AFTER UPDATE ON vehiculo
FOR EACH ROW
EXECUTE FUNCTION actualizar_bitacora_operador();