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

CREATE OR REPLACE FUNCTION actualizar_bitacora_asig_clientes() RETURNS TRIGGER AS $$
DECLARE
	id_vehic_aux int;
BEGIN
	IF NEW.id_operador IS NOT NULL THEN
		SELECT id
		INTO id_vehic_aux
		FROM vehiculo
		WHERE id_operador = NEW.id_operador;
	
		INSERT INTO bitacora_asig_clientes (id_cliente, id_operador, id_vehiculo,fecha_hora_asignacion)
		VALUES (NEW.id, NEW.id_operador, id_vehic_aux, NOW());
	ELSE
		UPDATE bitacora_asig_clientes
		SET fecha_hora_desasignacion = NOW()
		WHERE id = (SELECT id
					FROM bitacora_asig_clientes
					WHERE id_cliente = NEW.id
					ORDER BY fecha_hora_asignacion DESC
					LIMIT 1
		);
	END IF;
	RETURN NEW;
END;
$$ LANGUAGE plpgsql;
CREATE OR REPLACE TRIGGER actualizar_bitacora_asig_clientes_trg
AFTER UPDATE ON cliente
FOR EACH ROW
WHEN (OLD.id_operador IS DISTINCT FROM NEW.id_operador)
EXECUTE FUNCTION actualizar_bitacora_asig_clientes();