
import requests
import traceback

def convertir_divisas(cantidad, moneda_origen, moneda_destino):
    api_key = '9d28c1643b914d996415fb45'    # Reemplaza 'TU_API_KEY' con tu clave de API

    url = f'https://v6.exchangerate-api.com/v6/{api_key}/pair/{moneda_origen}/{moneda_destino}/{cantidad}'

    try:
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            resultado = data['conversion_result']
            return resultado
        else:
            print('Error al realizar la conversión.')
    except requests.exceptions.RequestException as e:
        return cantidad

# # Ejemplo de uso
# cantidad_euros = 400
# moneda_origen = 'EUR'
# moneda_destino = 'USD'

# print(convertir_divisas(cantidad_euros, moneda_origen, moneda_destino))



from util.db_conn import Db_Connection

def tran_empleado():
    try:
        type = 'mysql'
        host = '127.0.0.1'
        port = '3306'
        user = 'root'
        pwd = '1234'
        # Conexión con el sor
        db_sor = 'sor_proyecto'

        # Conexión a la base de datos de destino (sor_proyecto)
        con_db_sor = Db_Connection(type, host, port, user, pwd, db_sor)
        ses_db_sor = con_db_sor.start()
        if ses_db_sor == -1:
            raise Exception("El tipo de base de datos " + type + " no es válido")
        elif ses_db_sor == -2:
            raise Exception("Error al establecer la conexión de pruebas")

# Ejecutar las consultas de actualización e inserción
        with ses_db_sor.begin() as conn:

            # Agregar una nueva columna a la tabla empleado
            alter_table_query = "ALTER TABLE empleado ADD COLUMN sueldoDolar DECIMAL(10, 2)"
            conn.execute(alter_table_query)

            # Obtener los registros de la tabla empleado
            select_query = "SELECT id, sueldo FROM empleado"
            conn.execute(select_query)
            result = conn.fetchall()

            # Actualizar los valores de la columna sueldoDolar
            update_query = "UPDATE empleado SET sueldoDolar = %s WHERE id = %s"
            for row in result:


                #Realizamos la consulta del tipo de moneda en que se le paga por contrato
                # Realizar la consulta a la tabla contrato
                select_query = "SELECT monedaPago FROM contrato WHERE contratoID = %s"
                conn.execute(select_query, (row[1],))
                result = conn.fetchone()

                # Verificar si se encontró un resultado
                moneda_pago = "USD"
                if result:
                    moneda_pago = result[0]



                #Aquí hay que mandar los datos a la api
                print("sueldo actual row[4]", row[4])
                print("moneda_pago", moneda_pago)
                nuevo_sueldo = convertir_divisas(row[4], moneda_pago, "USD")
                sueldo_dolar = nuevo_sueldo # Multiplicar el sueldo por 2
                empleado_id = row[0]
                conn.execute(update_query, (sueldo_dolar, empleado_id))

                # Confirmar los cambios en la base de datos
                conn.commit()

    except:
        traceback.print_exc()
    finally:
        con_db_sor.stop()

