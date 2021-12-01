from numpy.core.fromnumeric import shape
import pygsheets
import pandas as pd
import time
import json
import requests
import smtplib
from smtplib import SMTPException

def getTipoDocumento(data):
    if data == "Cédula ciudadanía":
        return "CC"
    elif data == "Cédula de extranjería":
        return "CE"
    elif data == "Carné diplomático":
        return "CD"
    elif data == "Pasaporte":
        return "PA"
    elif data == "Salvoconducto":
        return "SC"
    elif data == "Permiso especial de permanencia":
        return "PE"
    elif data == "Residente especial para la paz":
        return "RE"
    elif data == "Registro civil":
        return "RC"
    elif data == "Tarjeta de identidad":
        return "TI"
    elif data == "Certificado de nacido vivo":
        return "CN"
    elif data == "Número único de identificación personal":
        return "UN"
    elif data == "Adulto sin identificar":
        return "AS"
    elif data == "Menor sin identificar":
        return "MS"
    elif data == "Pasaporte de la ONU":
        return "PR"
    elif data == " Nit":
        return "NI"
    elif data == "Sin indentificación":
        return "SI"
    elif data == "Documento de extranjero":
        return "DE"
        
def sendTheEmail(data):
    server = smtplib.SMTP('smtp.gmail.com: 587')
    server.starttls()
 
    # Login Credentials for sending the mail
    server.login("connecion.medicas@gmail.com", "coneccionmedicas123")
    
    message = """\
        Subject: Respuesta al insertar un nuevo paciente

        La respuesta del servidor es : \n
        
        estado:{} \n
        mensaje: {}
    """.format(data['estado'],data['mensaje'])

    # send the message via the server.
    server.sendmail("connecion.medicas@gmail.com", "asistencia@juanestebansierra.com", message )
    
    server.quit()
    
    print ("successfully sent email to %s:" % ("asistencia@juanestebansierra.com"))

def getEstadoCivil(data):
    if data == "Soltero(a)":
        return "1"
    elif data == "Casado(a)":
        return "2"
    elif data == "Unión Libre":
        return "3"
    elif data == "Separado(a)":
        return "4"
    else:
        return "5"

def getIdentidadGenero(data):
    if data == "Masculino":
        return "01"
    elif data == "Femenino":
        return "02"
    elif data == "Transgénero":
        return "03"
    elif data == "Neutro":
        return "04"
    else:
        return "05"


def generateJSON(data):
    dicc = {}
    dicc["tipo_documento"] = getTipoDocumento(data[8])
    dicc["id_paciente" ] = str(data[9])
    dicc["tipo_identidad_genero"] = getIdentidadGenero(data[3])
    # Generando los nombres y apellidos
    nombres = data[6].split(" ")
    apellidos = data[7].split(" ")
    dicc["primer_nombre"] = nombres[0]
    dicc["segundo_nombre"] = "" if len(nombres) == 1 else nombres[1]
    dicc["primer_apellido"] = apellidos[0]
    dicc["segundo_apellido"] = "" if len(apellidos) == 1 else apellidos[1]
    dicc["estado_civil"] = getEstadoCivil(data[2])
    dicc["sexo"] = "M" if data[4] == "Masculino" else "F"
    dicc["fecha_nacimiento"] = data[5]
    dicc["celular"] = str(data[18])
    dicc["email"] = data[19]
    dicc["entidad"] = "000000"
    dicc["tipo_aseguramiento"] = "4"
    dicc["tipo_sangre"] = data[21]
    dicc['api_key'] = 'himed'
    print("El diccionario es")
    print(dicc)
    return json.dumps(dicc)


#authorization
gc = pygsheets.authorize(service_file='pruebaconeccion.json')

# Create empty dataframe
df = pd.DataFrame()

sh = gc.open('Coneccion con himed')

#select the first sheet 
wks = sh.sheet1

# Tomando los datos de los primero pacientes
last_update = sh.updated
df = wks.get_as_df(encoding="utf-8")
last_row = df.shape[0]

# Enviando la nueva informacion de los primeros usuarios
for i in range(df.shape[0]):
    data = df.iloc[i,:].to_list()
    json_data = generateJSON(data)
    print("Enviando informacion")
    print(json_data)
    r = requests.post(url = 'https://user.medsas.co/interoperabilidad/Api/Controllers/Demograficos/crearPaciente.php', data=json_data)
    print(f"Status Code: {r.status_code}, Response: {r.json()}")
    sendTheEmail(r.json())

while(True):
    if last_update != sh.updated:
        df_new = wks.get_as_df()
        diff = df_new.shape[0] - last_row
        print('se actualizo')
        print("la diferencia columna es: "+ str(diff))
        for i in range(last_row, last_row + diff):
            data = df_new.iloc[i,:].to_list()
            json_data = generateJSON(data)
            print("Enviando informacion")
            r = requests.post(url = 'https://user.medsas.co/interoperabilidad/Api/Controllers/Demograficos/crearPaciente.php', data=json_data)
            print(f"Status Code: {r.status_code}, Response: {r.json()}")
            sendTheEmail(r.json())
        last_update = sh.updated
        last_rows = df_new.shape[0]
    else:
        print('no se actualizo')
    time.sleep(60)