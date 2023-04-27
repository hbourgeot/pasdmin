from flask import Blueprint,jsonify,request
from models.entities.monto import Monto
from models.mountmodel import MountModel
from flask_cors import CORS

montos = Blueprint('monto_blueprint',__name__)
CORS(montos)

@montos.route('/')
def get_montos():
    try:

        monto = MountModel.get_montos()
        return jsonify(monto)
    
    except Exception as ex:
        return jsonify({"message": str(ex)}),500

@montos.route('/<id>')
def get_monto(id):
    try:
        monto = MountModel.get_monto(id)
        if monto != None:
            return jsonify(monto)
        else:
            return jsonify({}),404
    
    except Exception as ex:
        return jsonify({"message": str(ex)}),500

@montos.route('/add', methods = ["POST"])
def add_monto():
    try:

        id_monto = request.json['id']
        pre_inscripcion = request.json['pre_inscripcion']
        inscripcion = request.json['inscripcion']
        id_pago = request.json['pago']
        cuota1 =request.json['cuota1']
        cuota2=request.json['cuota2']
        cuota3 =request.json['cuota3']
        cuota4 =request.json['cuota4']
        cuota5 =request.json['cuota5']

        
        monto = Monto(str(id_monto),str(id_pago),pre_inscripcion,inscripcion,cuota1,cuota2,cuota3,cuota4,cuota5)

        affected_rows = MountModel.add_monto(monto)

        if affected_rows == 1:
            return jsonify(monto.id)
        else:
            return jsonify({'message': "Error on insert"}), 500
    
    except Exception as ex:
        return jsonify({"message": str(ex)}),500
    
@montos.route('/update/<id>', methods = ["PUT"])
def update_admin(id):
    try:

       
        pre_inscripcion = request.json['pre_inscripcion']
        inscripcion = request.json['inscripcion']
        id_pago = request.json['pago']
        cuota1 =request.json['cuota1']
        cuota2=request.json['cuota2']
        cuota3 =request.json['cuota3']
        cuota4 =request.json['cuota4']
        cuota5 =request.json['cuota5']
        
        monto = Monto(str(id),str(id_pago),pre_inscripcion,inscripcion,cuota1,cuota2,cuota3,cuota4,cuota5)

        affected_rows = MountModel.update_monto(monto)

        if affected_rows == 1:
            return jsonify(monto.id_pago)
        else:
            return jsonify({'message': "Error on insert"}), 500
    
    except Exception as ex:
        return jsonify({"message": str(ex)}),500