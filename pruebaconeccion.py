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

def getEscolaridad(data):
    if data == "Preescolar":
        return "2"
    elif data == "Básica Primaria":
        return "3"
    elif data == "Básica Secundaria":
        return "4"
    elif data == "Media Académica o Clásica":
        return "5"
    elif data == "Media Técnica":
        return "6"
    elif data == "Normalista":
        return "7"
    elif data == "Técnico Profesional":
        return "8"
    elif data == "Tecnológica":
        return "9"
    elif data == "Profesional":
        return "10"
    elif data == "Especialización":
        return "11"
    elif data == "Maestría":
        return "12"
    elif data == "Doctorado":
        return "13"
    else:
        return "1"

def getZoneResidencial(data):
    if data == "Urbano":
        return "U"
    else:
        return "R"

def getPais(data):
    diccionario = {"Canadá": "0001", "Estados Unidos":"001","Jerusalén": "002","Islas Chatham": "0064","Rusia": "007","Egipto": "020","Comoros": "0269","Sudáfrica": "027","Grecia": "030","Holanda": "031","Bélgica": "032","Francia": "033","España": "034","Hungría": "036","Italia": "039","Rumania": "040","Suiza": "041","Austria": "043","Reino Unido": "044","Dinamarca": "045","Suecia": "046","Noruega": "047","Polonia": "048","Alemania": "049","Perú": "051","México": "052","Cuba": "053","Argentina": "054","Brasil": "055","Chile": "056","Colombia": "057","Venezuela": "058","Antillas francesas": "0596","Malasia": "060","Australia": "061","Indonesia": "062", "Filipinas": "063","Nueva Zelanda": "064","Singapur": "065","Tailandia": "066","Islas marianas": "0670","Japón": "081","Corea del sur": "082","Vietnam": "084","China": "086","Turquía": "090","India": "091","Pakistán": "091","Afganistán": "093","Sri Lanka": "094","Myanmar": "095","Irán": "098","Bahamas": "1242","Barbados": "1246","Antigua y Barbuda": "1268","Puerto Rico": "1787","Marruecos": "212","Argelia": "213","Túnez": "216","Libia": "218","Gambia": "220","Senegal": "221","Mauritania": "222","Mali": "223","Guinea": "224","Costa Ivory": "225","Burkina faso": "226","Níger": "227","Togo": "228","Benín": "229","Mauricio": "230","Liberia": "231","Sierra leona": "232","Ghana": "233","Nigeria": "234","Chad": "235","Republica Centroafricana": "236","Camerún": "237","Cabo verde": "238","Santo tomé y Príncipe": "239","Guinea ecuatorial": "240","Gabón": "241","Congo": "242","Zaire": "243","Angola": "244","Guinea Bissau": "245","Seychelles": "248","Sudan": "249","Ruanda": "250","Etiopia": "251","Somalia": "252","Yibuti": "253","Kenia": "254","Tanzania": "255","Uganda": "256","Burundi": "257","Mozambique": "258","Zanzíbar": "259","Zambia": "260","Madagascar": "261","Zimbabwe": "263","Namibia": "264","Malawi": "265","Lesoto": "266","Botswana": "267","Suazilandia": "268","Mahoré": "269","Islas vírgenes": "284","Santa helena": "290","Eritrea": "291","Aruba": "297","Islas faroe": "298","Groenlandia": "299","Islas vírgenes": "340","Islas Caiman": "345","Gibraltar": "350","Portugal": "351","Luxemburgo": "352","Irlanda": "353","Islandia": "354","Albania": "355","Malta": "356","Chipre": "357","Finlandia": "358","Bulgaria": "359","Lituania": "370","Letonia": "371","Estinia": "372","Moldavia": "373","Armenia": "374","Bielorrusia": "375","Andorra": "376","Mónaco": "377","San Marino": "378","Ucrania": "380","Serbia": "381","Montenegro": "382","Croacia": "385","Eslovenia": "386","Bosnia y Herzegovina": "387","Macedonia": "389","Liechtenstein": "4175","Republica checa": "420","Eslovaquia": "421","Granada": "473","Islas Malvinas": "500","Belice": "501","Guatemala": "502","El salvador": "503","Honduras": "504","Nicaragua": "505","Costa rica": "506","Panamá": "507","San Pedro y Miquelón": "508","Haití": "509","Bahía de Guantánamo": "5399","Guadalupe": "590","Bolivia": "591","Guyana": "592","Ecuador": "593","Guayana francesa": "594","Paraguay": "595","Martinica": "596","Surinam": "597","Uruguay": "598","Antillas holandesas": "599","Montserrat": "664", "Saipán":"670", "Guam":"671", "Antártida":"672", "Brunei":"673", "Nauru":"674", "Papua nueva guinea":"675", "Tonga":"676", "Islas Salomón":"677", "Islas Fiji":"679", "Palaos":"680", "Islas Cook":"682", "Niue":"683", "Samoa americana":"684", "Samoa":"685", "Kiribati":"686", "Nueva caledonia":"687", "Polinesia francesa":"689", "Tokelau":"690", "Micronesia":"691","Islas Marshall": "692","Santa lucia": "758","Dominica": "767","San VIcente y las granadinas": "784","Bermuda": "8009","Islas Midway": "808","Republica dominicana": "809","Core del norte": "850","Hong Kong": "852","Macau": "853","Cambodia": "855","Laos": "856","Trinidad y Tobago": "868","Isla nieves": "869","Jamaica": "876","Bangladesh": "880","Taiwán": "886","Maldivas": "960","Líbano": "961","Jordania": "962","Siria": "963","Iraq": "964","Kuwait": "965","Arabia saudita": "966","Yemen": "967","Omán": "968","Emiratos árabes unidos": "971","Israel": "972","Bahrain": "973","Qatar": "974","Bután": "975","Mongolia": "976","Nepal": "977","Turkmenistán": "993","Azerbaiyán": "994","Georgia": "995","Kirguistán": "996"}
    return diccionario[data]

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
    dicc["lugar_nacimiento"] = data[11]
    dicc["escolaridad"] = getEscolaridad(data[10])
    dicc["pais"] = getPais(data[11])
    dicc["telefono_uno"] = data[17]
    dicc["celular"] = str(data[18])
    dicc["email"] = data[19]
    dicc["dirección"] = data[15]
    dicc["zona_residencial"] = getZoneResidencial(data[16])
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