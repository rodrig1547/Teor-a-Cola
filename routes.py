from flask import Flask, render_template, redirect, url_for, session, request
from funciones import *  #Importando mis Funciones
from Consultas_sql import *


#Declarando nombre de la aplicación e inicializando, crear la aplicación Flask
app = Flask(__name__)
application = app


app.secret_key = '97110c78ae51a45af397be6534caef90ebb9b1dcb3380af008f90b23a5d1616bf19bc29098105da20fe'


#Redireccionando cuando la página no existe
@app.errorhandler(404)
def not_found(error):
    if 'conectado' in session:
        return redirect(url_for('inicio'))
    else:
        return render_template('public/modulo_login/index.html')
    
    
#Creando mi Decorador para el Home
@app.route('/')
def inicio():
    if 'conectado' in session:
        return render_template('public/dashboard/home.html', dataLogin = dataLoginSesion())
    else:
        return render_template('public/modulo_login/index.html')
    
    
@app.route('/login')
def login():
    if 'conectado' in session:
        return render_template('public/dashboard/home.html', dataLogin = dataLoginSesion())
    else:
        return render_template('public/modulo_login/index.html')


#Ruta para agregar/guardar registros a EECC
@app.route('/user', methods=['POST'])
def addUser():
    # Si el Perfil Corresponde a CAT
    if dataLoginSesion()["tipoLogin"] == 100:
        data = {}
        for field in ['dia', 'viaje_ot', 'cliente', 'lugar', 'tipo_extra_costo', 'motivo',
                    'hora_llegada', 'dia2', 'hora_salida', 'dia3', 'total_horas', 'empresa', 
                    'responsable','monto','estado']:
            data[field] = request.form.get(field)
            data['usuario'] = dataLoginSesion()['nombre'] +' ' + dataLoginSesion()['apellido'] 

        
    
        columns = ', '.join([f'`{column}`' for column in data.keys()])
        placeholders = ', '.join(['%s'] * len(data))
        values = list(data.values())
        addUserbd(columns, placeholders, values)

        return redirect(url_for('EECC'))
    #Si el Perfil Corresponde a un administrador de contratos o Desarrollador
    else: 
        data = {}
        for field in ['dia', 'viaje_ot', 'cliente', 'lugar', 'tipo_extra_costo', 'motivo',
                    'hora_llegada', 'dia2', 'hora_salida', 'dia3', 'total_horas', 'empresa', 
                    'responsable','monto','estado']:
            data[field] = request.form.get(field)
            data['usuario'] = dataLoginSesion()['nombre'] +' ' + dataLoginSesion()['apellido']
            data['cliente'] = dataLoginSesion()['perfil_usuario'][13:]
        if  data['estado'] == 'Aprobado' or data['estado'] == 'Rechazado':
            data['responsable_evaluacion'] = dataLoginSesion()['nombre'] +' ' + dataLoginSesion()['apellido']
        else: 
            data['responsable_evaluacion'] = ''
                    
             
    
        columns = ', '.join([f'`{column}`' for column in data.keys()])
        placeholders = ', '.join(['%s'] * len(data))
        values = list(data.values())
        addUserbd(columns, placeholders, values)

        return redirect(url_for('EECC'))
    
#Ruta para ELIMINAR Registros
@app.route('/delete/<string:id>/<string:estado>')
def delete(id, estado):
    if estado == 'Ingreso CAT' and dataLoginSesion()['tipoLogin'] ==100:
        data = (id,)
        deleterow(data)
        return redirect(url_for('EECC'))
    else: 
        data = (id,)
        deleterow(data)
        return redirect(url_for('EECC'))
    
    
#Ruta para EDITAR Registros de EECC
@app.route('/edit/<string:id>', methods=['POST'])
def edit(id):
    data = {}
    for field in ['dia', 'viaje_ot', 'lugar', 'tipo_extra_costo', 'motivo',
               'hora_llegada', 'dia2', 'hora_salida', 'dia3', 'total_horas', 'empresa', 'responsable', 
               'monto', 'estado', 'responsable_evaluacion']:
        data[field] = request.form.get(field)    
    data['id'] = id
    
    print ()
    if  request.form.get('estado') == 'Aprobado' or request.form.get('estado') == 'Rechazado':
        data['responsable_evaluacion'] = dataLoginSesion()['nombre'] +' ' + dataLoginSesion()['apellido']
    else: 
        data['responsable_evaluacion'] = ''
    values = list(data.values())
    editRow(values)
    return redirect(url_for('EECC'))    



# Cerrar session del usuario
@app.route('/logout')
def logout():
    msgClose = ''
    # Eliminar datos de sesión, esto cerrará la sesión del usuario
    session.pop('conectado', None)
    session.pop('id', None)
    session.pop('email', None)
    msgClose ="La sesión fue cerrada correctamente"
    return render_template('public/modulo_login/index.html', msjAlert = msgClose, typeAlert=1)