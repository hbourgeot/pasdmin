from flask import Blueprint, jsonify, request
from models.configmodel import ConfigModel
from models.entities.students import Student
from models.studentsmodel import StudentModel
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta, datetime
import traceback

main = Blueprint('students_blueprint', __name__)


@main.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response


@main.route('/')
def get_students():
    try:

        students = StudentModel.get_students()
        return jsonify({"ok": True, "status": 200, "data": students})

    except Exception as ex:
        return jsonify({"message": str(ex)}), 500


@main.route('/<cedula>')
def get_student(cedula):
    try:
        student = StudentModel.get_student(cedula)
        if student != None:
            return jsonify({"ok": True, "status": 200, "data": student})
        else:
            return jsonify({"ok": False, "status": 404, "data": {"message": "Estudiante no encontrado"}}), 404

    except Exception as ex:
        print(ex)
        return jsonify({"message": str(ex)}), 500


@main.route('/add', methods=["POST"])
def add_student():
    try:

        cedula = request.json['cedula']
        fullname = request.json['fullname']
        correo = request.json['correo']
        telefono = request.json['telefono']
        semestre = request.json['semestre']
        estado = request.json['estado']
        carrera = request.json['carrera']
        password = generate_password_hash(request.json["password"], method="sha256")
        edad = request.json['edad']
        sexo = request.json['sexo']
        direccion = request.json['direccion']
        fecha_nac = request.json['fecha_nac']

        student = Student(str(cedula), fullname, correo, telefono, semestre, password, estado, carrera, edad, sexo,
                          0, direccion, fecha_nac)

        affected_rows = StudentModel.add_student(student)

        if affected_rows == 1:
            return jsonify({"ok": True, "status": 200, "data": None})
        else:
            return jsonify({"ok": False, "status": 500, "data": {"message": affected_rows}}), 500

    except Exception as ex:
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500


@main.route('/update/<cedula>', methods=["PUT"])
def update_student(cedula):
    try:

        fullname = request.json['fullname']
        correo = request.json['correo']
        telefono = request.json['telefono']
        semestre = request.json['semestre']
        estado = request.json['estado']
        carrera = request.json["carrera"]
        edad = request.json['edad']
        sexo = request.json['sexo']
        direccion = request.json['direccion']
        fecha_nac = request.json['fecha_nac']

        student = Student(str(cedula), fullname, correo, telefono, semestre, None, estado, carrera, edad, sexo, 0, direccion, fecha_nac)

        affected_rows = StudentModel.update_student(student)

        if affected_rows == 1:
            return jsonify({"ok": True, "status": 200, "data": None})
        else:
            return jsonify({"ok": False, "status": 500,
                            "data": {"message": "Error al actualizar, compruebe los datos e intente nuevamente"}}), 500

    except Exception as ex:
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500


@main.route('/delete/<cedula>', methods=["DELETE"])
def delete_student(cedula):
    try:

        student = Student(str(cedula))

        affected_rows = StudentModel.delete_student(student)

        if affected_rows == 1:
            return jsonify({"ok": True, "status": 200, "data": None})
        else:
            return jsonify({"ok": False, "status": 404, "data": {"message": "Estudiante no encontrado"}}), 404

    except Exception as ex:
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500


@main.route("/add-materia/<materia>", methods=["POST"])
@jwt_required()
def add_student_to_materia(materia: str):
    try:
        correo_estudiante = get_jwt_identity()  # esto obtiene la identidad del token, en este caso, un correo
        student: Student | None  # declaramos sin iniciar la variable del estudiante
        if correo_estudiante is not None:
            student_entity = Student(correo=correo_estudiante)  # creamos la entidad del estudiante
            student = StudentModel.login(student_entity)  # revisamos la bd
            if student is not None:
                affected_rows = StudentModel.add_materia(student, materia)
                if affected_rows == 1:
                    return jsonify({"ok": True, "status": 200, "data": None}), 200
    except Exception as ex:
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}})


@main.route("/materias", methods=["GET"])
@jwt_required()
def get_notas():
    try:
        correo_estudiante = get_jwt_identity()
        student: Student | None
        if correo_estudiante is not None:
            student_entity = Student(correo=correo_estudiante)
            student_entity = StudentModel.login(student_entity)
            notas_obj = StudentModel.get_notas_estudiante(student_entity.cedula)
            return jsonify({"ok": True, "status": 200, "data": notas_obj}), 200
    except Exception as ex:
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500


@main.route("/historico", methods=["GET"])
@jwt_required()
def get_historico():
    try:
        correo_estudiante = get_jwt_identity()
        student: Student | None
        if correo_estudiante is not None:
            student_entity = Student(correo=correo_estudiante)
            student_entity = StudentModel.login(student_entity)
            notas_obj = StudentModel.get_historico(student_entity.cedula)
            return jsonify({"ok": True, "status": 200, "data": notas_obj}), 200
    except Exception as ex:
        print(ex.with_traceback(None))
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500


@main.route("/horario", methods=["GET"])
@jwt_required()
def get_horario():
    try:
        correo_estudiante = get_jwt_identity()
        student: Student | None
        if correo_estudiante is not None:
            student_entity = Student(correo=correo_estudiante)
            student_entity = StudentModel.login(student_entity)
            materias = StudentModel.get_inscritas(student_entity.cedula)
            return jsonify({"ok": True, "status": 200, "data": {"materias": materias}}), 200
    except Exception as ex:
        print(ex.with_traceback(None))
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500


@main.route('/login', methods=["POST"])
def login():
    try:
        fecha_actual = datetime.now()
        usuario = request.json.get('usuario', None)
        clave = request.json.get('clave', None)
        estudiante = Student(correo=usuario)
        estudiante = StudentModel.login(estudiante)
        if estudiante is not None:
            if check_password_hash(estudiante.password,
                                   clave):  # comprobamos que el hash sea igual a la clave ingrasada
                # antes de crear el access token debe realizar la comprobación nombrada, guiate del codigo comentado 
                pagos = StudentModel.get_pago_by_student(estudiante.cedula)
                config = ConfigModel.get_configuracion("1")

                # Validar pagos de pre-inscripción e inscripción
                for concepto in ["pre_inscripcion", "inscripcion"]:
                    pago_realizado = any(pago.monto_id.concepto == concepto and pago.ciclo == config.ciclo for pago in pagos)
                    if not pago_realizado:
                        return jsonify({"ok": False, "status": 401, "data": {"message": f"No has realizado el pago de la {concepto.replace('_', ' ').capitalize()}"}}), 401
                
                # Validar pagos de cuotas por fechas
                for i in range(1, 6):
                    fecha_cuota = getattr(config, f'cuota{i}')
                    if fecha_actual >= datetime.strptime(fecha_cuota, "%Y-%m-%d"):
                        pago_realizado = any(pago.monto_id.concepto == f'cuota{i}' and pago.ciclo == config.ciclo for pago in pagos)
                        if not pago_realizado:
                            return jsonify({"ok": False, "status": 401, "data": {"message": f"No has realizado el pago de la cuota {i}"}}), 401

                access_token = create_access_token(identity=estudiante.correo, expires_delta=timedelta(hours=2),
                                                   additional_claims={'rol': 'E'})  # creamos el token que vive una hora
                return jsonify({"ok": True, "status": 200,
                                "data": {"estudiante": estudiante.to_JSON(), "access_token": f"Bearer {access_token}"}})

            else:
                return jsonify({"ok": False, "status": 401, "data": {"message": "Correo y/o clave incorrectos"}}), 401
        else:
            return jsonify({"ok": False, "status": 401, "data": {"message": "Correo y/o clave incorrectos"}}), 401


    except Exception as ex:
        traceback.print_exc()
        return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500


@main.route('/refresh')
@jwt_required()
def jwt_student():
    try:
        correo_estudiante = get_jwt_identity()  # esto obtiene la identidad del token, en este caso, un correo
        student: Student | None  # declaramos sin iniciar la variable del estudiante
        if correo_estudiante is not None:
            student_entity = Student(correo=correo_estudiante)  # creamos la entidad del estudiante
            student = StudentModel.login(student_entity)  # revisamos la bd
            if student != None:
                return jsonify({"ok": True, "status": 200, "data": student.to_JSON()})  # retornamos si es correcto

        else:
            return jsonify({"ok": False, "status": 401, "data": {"message": "no autorizado"}}), 401

    except Exception as ex:
        return jsonify({"message": str(ex)}), 500
