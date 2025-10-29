from flask import Blueprint, request, jsonify
from models import db, Empresa
from app import ma
import os
from werkzeug.utils import secure_filename

empresas_bp = Blueprint('empresas', __name__, url_prefix='/empresas')

# Schema
class EmpresaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Empresa
        load_instance = True

empresa_schema = EmpresaSchema()
empresas_schema = EmpresaSchema(many=True)

# CREATE
@empresas_bp.route('/', methods=['POST'])
def add_empresa():
    nome = request.form.get('nome')
    cnpj = request.form.get('cnpj')
    setor = request.form.get('setor')
    email = request.form.get('email')
    file = request.files.get('certificado_esg')

    certificado_path = None
    if file:
        filename = secure_filename(file.filename)
        certificado_path = os.path.join('data/uploads', filename)
        file.save(certificado_path)

    nova = Empresa(nome=nome, cnpj=cnpj, setor=setor, email=email, certificado_esg=certificado_path)
    db.session.add(nova)
    db.session.commit()
    return empresa_schema.jsonify(nova), 201

# READ (todos)
@empresas_bp.route('/', methods=['GET'])
def get_empresas():
    empresas = Empresa.query.all()
    return empresas_schema.jsonify(empresas)

# READ (um)
@empresas_bp.route('/<int:id>', methods=['GET'])
def get_empresa(id):
    empresa = Empresa.query.get_or_404(id)
    return empresa_schema.jsonify(empresa)

# UPDATE
@empresas_bp.route('/<int:id>', methods=['PUT'])
def update_empresa(id):
    empresa = Empresa.query.get_or_404(id)
    empresa.nome = request.form.get('nome', empresa.nome)
    empresa.cnpj = request.form.get('cnpj', empresa.cnpj)
    empresa.email = request.form.get('email', empresa.email)
    db.session.commit()
    return empresa_schema.jsonify(empresa)

# DELETE
@empresas_bp.route('/<int:id>', methods=['DELETE'])
def delete_empresa(id):
    empresa = Empresa.query.get_or_404(id)
    db.session.delete(empresa)
    db.session.commit()
    return jsonify({'message': 'Empresa deletada com sucesso'})
# Arquivo para CRUD de empresas
