from models.entities.materias import Materias
from models.materiamodel import MateriaModel
from flask import Blueprint,jsonify,request
from werkzeug.security import generate_password_hash, check_password_hash

materia = Blueprint('materia_blueprint', __name__)

@materia.after_request 
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response

@materia.route('/')
def get_materias():

    try:

        materias = MateriaModel.get_materias()
        return jsonify({"ok": True, "status":200,"data": materias})
            
    except Exception as ex:
        return jsonify({"message": str(ex)}),500

@materia.route('/<id>')
def get_materia(id):

    try:

        materias = MateriaModel.get_materia(id)
        if materias != None:
            return jsonify({"ok": True, "status":200,"data":materias})
        else:
            return jsonify({"ok": False, "status":404,"data":{"message": "materia no encontrada"}}),404
    
    except Exception as ex:
            return jsonify({"message": str(ex)}),500

@materia.route('/add', methods = ['POST'])
def add_materia():

    try: 
        
        id = request.json['id']
        nombre = request.json['nombre']
        prelacion = request.json['prelacion']
        unidad_credito = request.json['unidad_credito']
        hp =  request.json['hp']
        ht = request.json['ht']
        semestre = request.json['semestre']
        id_carrera = request.json['id_carrera']
        id_docente = request.json['id_docente']

        materia = Materias(str(id),nombre,prelacion,unidad_credito,hp,ht,semestre,id_carrera,id_docente)

        affected_rows = MateriaModel.add_materia(materia)

        if affected_rows == 1:
             return jsonify({"ok": True, "status":200,"data":None})
        else:
            return jsonify({"ok": False, "status":500,"data":{"message": affected_rows}}), 500
        
    except Exception as ex:
        return jsonify({"ok": False, "status":500,"data":{"message":str(ex)}}), 500
             

@materia.route('/update/<id>', methods = ['PUT'])
def update_materia(id):

    try:
            
            id = request.json['id']
            nombre = request.json['nombre']
            prelacion = request.json['prelacion']
            unidad_credito = request.json['unidad_credito']
            hp =  request.json['hp']
            ht = request.json['ht']
            semestre = request.json['semestre']
            id_carrera = request.json['id_carrera']
            id_docente = request.json['id_docente']

            materia = Materias(str(id),nombre,prelacion,unidad_credito,hp,ht,semestre,id_carrera,id_docente)

            affected_rows = MateriaModel.update_materia(materia)

            if affected_rows == 1:
                return jsonify({"ok": True, "status":200,"data":None})
        
            else:
                return jsonify({"ok": False, "status":500,"data":{"message": "Error al actualizar, compruebe los datos e intente nuevamente"}}), 500
            
    except Exception as ex:
        return jsonify({"ok": False, "status":500,"data":{"message": "Error al actualizar, compruebe los datos e intente nuevamente"}}), 500

@materia.route('/delete/<id>', methods = [ 'DELETE'])
def delete_materia(id):

    try:
        
        materia  = Materias(str(id))

        affected_rows = MateriaModel.delete_materia(materia)

        if affected_rows == 1:
            return jsonify({"ok": True, "status":200,"data": None})
        else:
            return jsonify({"ok": False, "status":404,"data":{"message": "materia no encontrada"}}) ,404
    
    except Exception as ex:
        return jsonify({"ok": False, "status":500,"data":{"message": str(ex)}}), 500