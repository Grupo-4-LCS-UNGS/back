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

CREATE OR REPLACE FUNCTION actualizar_bitacora_asignaciones() RETURNS TRIGGER AS $$
DECLARE
	id_vehic_aux int;
BEGIN
	IF NEW.id_operador IS NOT NULL THEN
		INSERT INTO bitacora_asignaciones (id_vehiculo, id_usuario, fecha_hora_asignacion)
		VALUES (NEW.id, NEW.id_operador, NOW());
	ELSE
		UPDATE bitacora_asignaciones
		SET fecha_hora_desasignacion = NOW()
		WHERE id = (SELECT id
					FROM bitacora_asignaciones
					WHERE id_vehiculo = NEW.id
					ORDER BY fecha_hora_desasignacion DESC
					LIMIT 1
		);
	END IF;
	RETURN NEW;
END;
$$ LANGUAGE plpgsql;
CREATE OR REPLACE TRIGGER actualizar_bitacora_asignaciones_trg
AFTER UPDATE ON vehiculo
FOR EACH ROW
WHEN (OLD.id_operador IS DISTINCT FROM NEW.id_operador)
EXECUTE FUNCTION actualizar_bitacora_asignaciones();