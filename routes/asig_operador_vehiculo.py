from flask import Blueprint
from models.usuario import Usuario
from models.vehiculo import Vehiculo
from models.bitacora_asignaciones import BitacoraAsignaciones

asig_operador_vehiculo = Blueprint('asig_operador_vehiculo', __name__)

@asig_operador_vehiculo.route('/asignacion/<int:id_usuario>/vehiculos/<int:id_vehiculo>/', methods=['PUT'])
def asignar(id_vehiculo, id_usuario):
    vehiculo = Vehiculo.encontrarPorId(id_vehiculo)
    usuario = Usuario.buscarPorId(id_usuario)
   
    bitacoraAsignaciones = BitacoraAsignaciones(
        vehiculo=vehiculo,
        usuario=usuario
    )
    BitacoraAsignaciones.agregar(bitacoraAsignaciones)
    
    return bitacoraAsignaciones.serialize(), 201
   
    
    
    

@asig_operador_vehiculo.route('/desasignacion/<int:id_asignacion>', methods=['PUT'])
def desasignar(id_asignacion):
    bitacora = BitacoraAsignaciones.encontrarPorId(id_asignacion)
    BitacoraAsignaciones.agregarFechaHoraDesasignacion(id_asignacion)
    return bitacora.serialize(), 201