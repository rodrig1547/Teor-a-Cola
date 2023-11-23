from conexionBD import *

#Creando una funcion para obtener la lista de carros.
def mostrarRegistros():

    conexion_MySQLdb = connectionBD() #creando mi instancia a la conexion de BD
    cursor = conexion_MySQLdb.cursor()
    cursor.execute("SELECT * FROM eecc ORDER BY id DESC")
    myresult = cursor.fetchall()
    #Convertir los datos a diccionario
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))
    cursor.close() # Cerrando Conexion a la BD
    return insertObject

def addUserbd(columns, placeholders, values):
    conexion_MySQLdb = connectionBD()
    cursor = conexion_MySQLdb.cursor()
    sql = f"INSERT INTO eecc ({columns}) VALUES ({placeholders})"
    cursor.execute(sql, values)
    conexion_MySQLdb.commit()
    cursor.close()

def deleterow(row):
    conexion_MySQLdb = connectionBD()
    cursor = conexion_MySQLdb.cursor()
    sql = "DELETE FROM eecc WHERE id=%s"
    cursor.execute(sql, row)
    conexion_MySQLdb.commit()
    cursor.close()

def editRow(values):
    conexion_MySQLdb = connectionBD()
    cursor = conexion_MySQLdb.cursor()
    sql = "UPDATE eecc SET dia = %s, viaje_ot= %s, lugar = %s, tipo_extra_costo = %s, motivo = %s,\
               hora_llegada = %s, dia2 = %s, hora_salida = %s, dia3 = %s, total_horas = %s, empresa = %s, responsable = %s, \
               monto = %s, estado = %s, responsable_evaluacion = %s  WHERE id = %s"
    cursor.execute(sql, values)
    conexion_MySQLdb.commit()
    cursor.close()