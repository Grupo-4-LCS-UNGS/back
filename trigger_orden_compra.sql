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