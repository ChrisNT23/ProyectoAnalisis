from faker import Faker
from datetime import datetime, timedelta
import random
import mysql.connector

# Crear una instancia de Faker
fake = Faker()

# Establecer la conexión con la base de datos MySQL
cnx = mysql.connector.connect(
    host='192.168.100.53',
    port='3306',
    user='ADMIN',
    password='',
    database='proyecto'
)

# Crea un cursor para ejecutar consultas SQL
cursor = cnx.cursor()

############################TABLA USUARIO#####################################################################################################################

# Verificar si la tabla Usuario ya existe
cursor.execute("SHOW TABLES LIKE 'Usuario'")
tabla_existe = cursor.fetchone()

if not tabla_existe:
    # Crear la tabla Usuario si no existe
    cursor.execute("""
       CREATE TABLE Usuario 
(
	usuarioID INT AUTO_INCREMENT, 
	cedula CHAR(10) NOT NULL, 
	estado BIT NOT NULL,
	CONSTRAINT PK_Usuario PRIMARY KEY (usuarioID)
)
    """)

    # Confirmar los cambios en la base de datos
    cnx.commit()
    print("La tabla Usuario se creó exitosamente.")
else:
    print("La tabla Usuario ya existe en la base de datos.")

# Generar datos ficticios y realizar inserciones
if not tabla_existe:
    # Generar 10 registros ficticios utilizando Faker
    registros = []
    for _ in range(150):
        cedula = fake.random_number(digits=10)
        estado = fake.boolean()
        registros.append((cedula, estado))

    # Insertar los registros en la tabla Usuario
    insert_query = "INSERT INTO Usuario (cedula, estado) VALUES (%s, %s)"
    cursor.executemany(insert_query, registros)

    # Confirmar los cambios en la base de datos
    cnx.commit()
    print("Los datos se insertaron exitosamente.")
else:
    print("No se insertaron nuevos datos porque la tabla Usuario ya existe.")


############################SUBSIDIARIA#####################################################################################################################

# Verificar si la tabla Subsidiaria ya existe
cursor.execute("SHOW TABLES LIKE 'Subsidiaria'")
tabla_existe = cursor.fetchone()

if not tabla_existe:
    # Crear la tabla Subsidiaria si no existe
    cursor.execute("""
        CREATE TABLE Subsidiaria (
            subsidiariaID INT AUTO_INCREMENT,
            nombre VARCHAR(50) NOT NULL,
            ciudad VARCHAR(30) NOT NULL,
            tipoSubsidiaria VARCHAR(20) NOT NULL,
            CONSTRAINT PK_Subsidiaria PRIMARY KEY (subsidiariaID)
        )
    """)

    # Confirmar los cambios en la base de datos
    cnx.commit()
    print("La tabla Subsidiaria se creó exitosamente.")
else:
    print("La tabla Subsidiaria ya existe en la base de datos.")

# Generar datos ficticios y realizar inserciones
if not tabla_existe:
    # Generar 10 registros ficticios utilizando Faker
    registros = []
    for _ in range(150):
        nombre = fake.company()
        ciudad = fake.city()
        tipo_subsidiaria = fake.random_element(['Tipo 1', 'Tipo 2', 'Tipo 3'])
        registros.append((nombre, ciudad, tipo_subsidiaria))

    # Insertar los registros en la tabla Subsidiaria
    insert_query = "INSERT INTO Subsidiaria (nombre, ciudad, tipoSubsidiaria) VALUES (%s, %s, %s)"
    cursor.executemany(insert_query, registros)

    # Confirmar los cambios en la base de datos
    cnx.commit()
    print("Los datos se insertaron exitosamente.")
else:
    print("No se insertaron nuevos datos porque la tabla Subsidiaria ya existe.")



############################CENTRO DE COSTOS#####################################################################################################################
# Áreas de trabajo posibles
areas_trabajo = ['calidad', 'operaciones', 'finanzas', 'legal', 'comercial', 'marketing', 'THC', 'administracion']
# Verificar si la tabla CentroCostos ya existe
cursor.execute("SHOW TABLES LIKE 'CentroCostos'")
tabla_existe = cursor.fetchone()

if not tabla_existe:
    # Crear la tabla CentroCostos si no existe
    cursor.execute("""
        CREATE TABLE CentroCostos (
            centroCostosID INT AUTO_INCREMENT,
            nombre VARCHAR(50) NOT NULL,
            areaTrabajo VARCHAR(50) NOT NULL,
            CONSTRAINT PK_CentroCostos PRIMARY KEY (centroCostosID)
        )
    """)

    # Confirmar los cambios en la base de datos
    cnx.commit()
    print("La tabla CentroCostos se creó exitosamente.")
else:
    print("La tabla CentroCostos ya existe en la base de datos.")

# Generar datos ficticios y realizar inserciones
if not tabla_existe:
    # Generar 10 registros ficticios utilizando Faker
    registros = []
    for _ in range(150):
        nombre = fake.company()
        area_trabajo = random.choice(areas_trabajo)
        registros.append((nombre, area_trabajo))

    # Insertar los registros en la tabla CentroCostos
    insert_query = "INSERT INTO CentroCostos (nombre, areaTrabajo) VALUES (%s, %s)"
    cursor.executemany(insert_query, registros)

    # Confirmar los cambios en la base de datos
    cnx.commit()
    print("Los datos se insertaron exitosamente.")
else:
    print("No se insertaron nuevos datos porque la tabla CentroCostos ya existe.")


############################TIPO CONTRATO#####################################################################################################################

nombres = ["indefinido", "civil", "emergente", "pasantias", "k2a", "k2a por horas"]
# Verificar si la tabla TipoContrato ya existe
cursor.execute("SHOW TABLES LIKE 'TipoContrato'")
tabla_existe = cursor.fetchone()

if not tabla_existe:
    # Crear la tabla TipoContrato si no existe
    cursor.execute("""
        CREATE TABLE TipoContrato (
            tipoContratoID INT AUTO_INCREMENT,
            nombre VARCHAR(50) NOT NULL,
            descripcion VARCHAR(250) NOT NULL,
            CONSTRAINT PK_TipoContrato PRIMARY KEY (tipoContratoID)
        )
    """)

    # Confirmar los cambios en la base de datos
    cnx.commit()
    print("La tabla TipoContrato se creó exitosamente.")
else:
    print("La tabla TipoContrato ya existe en la base de datos.")

# Generar datos ficticios y realizar inserciones
if not tabla_existe:
    # Generar 150 registros ficticios utilizando Faker
    registros = []
    for _ in range(150):
        nombre = random.choice(nombres)
        descripcion = fake.text(max_nb_chars=250)
        registros.append((nombre, descripcion))

    # Insertar los registros en la tabla TipoContrato
    insert_query = "INSERT INTO TipoContrato (nombre, descripcion) VALUES (%s, %s)"
    cursor.executemany(insert_query, registros)

    # Confirmar los cambios en la base de datos
    cnx.commit()
    print("Los datos TipoContrato se insertaron exitosamente.")
else:
    print("No se insertaron nuevos datos porque la tabla TipoContrato ya existe.")


#############################CONTRATO####################################################################################################################

# Verificar si la tabla Contrato ya existe
cursor.execute("SHOW TABLES LIKE 'Contrato'")
tabla_existe = cursor.fetchone()

if not tabla_existe:
    # Crear la tabla Contrato si no existe
    cursor.execute("""
        CREATE TABLE Contrato (
            contratoID INT AUTO_INCREMENT, 
            tipoContratoID INT,
            descripcion VARCHAR(250) NOT NULL,
            monedaPago VARCHAR(30) NOT NULL,
            fechaInicio DATE NOT NULL,
            fechaFin DATE NOT NULL,
            CONSTRAINT PK_Contrato PRIMARY KEY (contratoID),
            CONSTRAINT FK_Contrato FOREIGN KEY(tipoContratoID) REFERENCES TipoContrato(tipoContratoID)
        )
    """)
    
    # Confirmar los cambios en la base de datos
    cnx.commit()
    print("La tabla Contrato se creó exitosamente.")
else:
    print("La tabla Contrato ya existe en la base de datos.")

# Generar datos ficticios y realizar inserciones
if not tabla_existe:
    # Generar 50 registros ficticios utilizando Faker
    registros = []
    for _ in range(150):
        tipo_contrato_id = random.randint(1, 100)  # Valor aleatorio para tipoContratoID
        descripcion = fake.text(max_nb_chars=250)
        moneda_pago = fake.currency_code()
        
        # Generar fechas aleatorias dentro del rango deseado
        fecha_inicio = fake.date_between_dates(date_start=datetime(2018, 1, 1), date_end=datetime(2025, 12, 31))
        fecha_fin = fecha_inicio + timedelta(days=random.randint(30, 365))  # Sumar días aleatorios
        
        registros.append((tipo_contrato_id, descripcion, moneda_pago, fecha_inicio, fecha_fin))

    # Insertar los registros en la tabla Contrato
    insert_query = "INSERT INTO Contrato (tipoContratoID, descripcion, monedaPago, fechaInicio, fechaFin) VALUES (%s, %s, %s, %s, %s)"
    cursor.executemany(insert_query, registros)

    # Confirmar los cambios en la base de datos
    cnx.commit()
    print("Los datos se insertaron exitosamente.")
else:
    print("No se insertaron nuevos datos porque la tabla Contrato ya existe.")


#############################PROYECTO####################################################################################################################

# Verificar si la tabla Proyecto ya existe
cursor.execute("SHOW TABLES LIKE 'Proyecto'")
tabla_existe = cursor.fetchone()

if not tabla_existe:
    # Crear la tabla Proyecto si no existe
    cursor.execute("""
        CREATE TABLE Proyecto (
            proyectoID INT AUTO_INCREMENT, 
            nombre VARCHAR(100) NOT NULL, 
            capital DECIMAL(10,2) NOT NULL, 
            gananciaNeta DECIMAL(10,2) NOT NULL,
            tamañoProyecto VARCHAR(20),
            fechaInicio DATE NOT NULL,
            fechaFinTentativa DATE NOT NULL,
            CONSTRAINT PK_Proyecto PRIMARY KEY (proyectoID)
        )
    """)
    
    # Confirmar los cambios en la base de datos
    cnx.commit()
    print("La tabla Proyecto se creó exitosamente.")
else:
    print("La tabla Proyecto ya existe en la base de datos.")

# Generar datos ficticios y realizar inserciones
if not tabla_existe:
    # Generar 50 registros ficticios utilizando Faker
    registros = []
    for _ in range(150):
        nombre = fake.catch_phrase()
        capital = round(random.uniform(10000, 1000000), 2)
        ganancia_neta = round(random.uniform(1000, 50000), 2)
        tamaño_proyecto = random.choice(["Pequeño", "Mediano", "Grande"])
        fecha_inicio = fake.date_between_dates(date_start=datetime(2018, 1, 1), date_end=datetime(2025, 12, 31))
        fecha_fin_tentativa = fecha_inicio + timedelta(days=random.randint(30, 365))

        registros.append((nombre, capital, ganancia_neta, tamaño_proyecto, fecha_inicio, fecha_fin_tentativa))

    # Insertar los registros en la tabla Proyecto
    insert_query = "INSERT INTO Proyecto (nombre, capital, gananciaNeta, tamañoProyecto, fechaInicio, fechaFinTentativa) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.executemany(insert_query, registros)

    # Confirmar los cambios en la base de datos
    cnx.commit()
    print("Los datos se insertaron exitosamente.")
else:
    print("No se insertaron nuevos datos porque la tabla Proyecto ya existe.")


#############################TIPO PERMISO####################################################################################################################

nombres_especificos = [
    "Vacaciones", "Días personales", "Licencia por enfermedad", 
    "Permiso por maternidad", "Permiso de duelo", "Permiso por estudio", 
    "Permiso sabático", "Permiso para cuidado de familiares", 
    "Permiso de adopción", "Permiso de formación"
]

# Verificar si la tabla TipoPermiso ya existe
cursor.execute("SHOW TABLES LIKE 'TipoPermiso'")
tabla_existe = cursor.fetchone()

if not tabla_existe:
    # Crear la tabla TipoPermiso si no existe
    cursor.execute("""
        CREATE TABLE TipoPermiso (
            tipoPermisoID INT AUTO_INCREMENT,
            nombre VARCHAR(300) NOT NULL, 
            descripcion VARCHAR(250) NOT NULL,
            CONSTRAINT PK_TipoPermiso PRIMARY KEY (tipoPermisoID)
        )
    """)
    
    # Confirmar los cambios en la base de datos
    cnx.commit()
    print("La tabla TipoPermiso se creó exitosamente.")
else:
    print("La tabla TipoPermiso ya existe en la base de datos.")

# Generar datos ficticios y realizar inserciones
if not tabla_existe:
    # Generar 10 registros ficticios utilizando Faker
    registros = []
    for _ in range(150):
        nombre = random.choice(nombres_especificos)
        descripcion = fake.text(max_nb_chars=250)

        registros.append((nombre, descripcion))

    # Insertar los registros en la tabla TipoPermiso
    insert_query = "INSERT INTO TipoPermiso (nombre, descripcion) VALUES (%s, %s)"
    cursor.executemany(insert_query, registros)

    # Confirmar los cambios en la base de datos
    cnx.commit()
    print("Los datos se insertaron exitosamente.")
else:
    print("No se insertaron nuevos datos porque la tabla TipoPermiso ya existe.")



#############################EMPLEADO####################################################################################################################

# Verificar si la tabla Empleado ya existe
cursor.execute("SHOW TABLES LIKE 'Empleado'")
tabla_existe = cursor.fetchone()

if not tabla_existe:
    # Crear la tabla Empleado si no existe
    cursor.execute("""
        CREATE TABLE Empleado
        (
            empleadoID INT AUTO_INCREMENT,
            usuarioID INT,
            centroCostosID INT,
            contratoID INT,
            nombre VARCHAR(50) NOT NULL,
            cargo VARCHAR(50) NOT NULL,
            sueldo DECIMAL(10,2) NOT NULL,
            nivelK VARCHAR(20),
            pais VARCHAR(60) NOT NULL,
            CONSTRAINT PK_Empleado PRIMARY KEY (empleadoID),
            CONSTRAINT FK_EmpleadoA FOREIGN KEY(usuarioID) REFERENCES Usuario(usuarioID),
            CONSTRAINT FK_EmpleadoB FOREIGN KEY(centroCostosID) REFERENCES CentroCostos(centroCostosID),
            CONSTRAINT FK_EmpleadoC FOREIGN KEY(contratoID) REFERENCES Contrato(contratoID)
        )
    """)

    # Confirmar los cambios en la base de datos
    cnx.commit()
    print("La tabla Empleado se creó exitosamente.")
else:
    print("La tabla Empleado ya existe en la base de datos.")

# Generar datos ficticios y realizar inserciones
if not tabla_existe:
    # Generar 170 registros ficticios utilizando Faker
    registros = []
    cargos = [
        "Desarrollador de software JR",
        "Analista de datos",
        "Arquitecto Software",
        "QA",
        "DevOps",
        "Desarrollador de software Senior"
    ]
    niveles = {
        (0, 500): "1",
        (501, 1200): "2",
        (1201, 1500): "3",
        (1501, 1800): "4",
        (1801, 2300): "5",
        (2301, 2800): "6",
        (2801, 4000): "7",
        (4001, float('inf')): "8"
    }
    paises = [
        "Estados Unidos",
        "Ecuador",
        "Perú",
        "Costa Rica",
        "Bolivia",
        "Mexico",
        "España",
        "Colombia"
    ]

    for _ in range(150):
        usuarioID = random.randint(1, 100)
        centroCostosID = random.randint(1, 10)
        contratoID = random.randint(1, 100)
        nombre = fake.name()
        cargo = random.choice(cargos)
        sueldo = round(random.uniform(400, 5000), 2)
        nivelK = next((nivel for (rango_inicio, rango_fin), nivel in niveles.items() if rango_inicio <= sueldo <= rango_fin), None)
        pais = random.choice(paises)
        registros.append((usuarioID, centroCostosID, contratoID, nombre, cargo, sueldo, nivelK, pais))

    # Insertar los registros en la tabla Empleado
    insert_query = "INSERT INTO Empleado (usuarioID, centroCostosID, contratoID, nombre, cargo, sueldo, nivelK, pais) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.executemany(insert_query, registros)

    # Confirmar los cambios en la base de datos
    cnx.commit()
    print("Los datos se insertaron exitosamente.")
else:
    print("No se insertaron nuevos datos porque la tabla Empleado ya existe.")


######################MARCADOR DE HORAS###########################################################################################################################

# Verificar si la tabla MarcadorHoras ya existe
cursor.execute("SHOW TABLES LIKE 'MarcadorHoras'")
tabla_existe = cursor.fetchone()

if not tabla_existe:
    # Crear la tabla MarcadorHoras si no existe
    cursor.execute("""
        CREATE TABLE MarcadorHoras
        (
            marcadorHorasID INT AUTO_INCREMENT,
            empleadoID INT,
            proyectoID INT,
            fecha DATE NOT NULL,
            cantidadHoras INT NOT NULL,
            CONSTRAINT PK_MarcadorHoras PRIMARY KEY (marcadorHorasID),
            CONSTRAINT FK_MarcadorHorasA FOREIGN KEY(empleadoID) REFERENCES Empleado(empleadoID),
            CONSTRAINT FK_MarcadorHorasB FOREIGN KEY(proyectoID) REFERENCES Proyecto(proyectoID),
            CONSTRAINT CHK_CantidadHoras CHECK (cantidadHoras <= 1500)
        )
    """)

    # Confirmar los cambios en la base de datos
    cnx.commit()
    print("La tabla MarcadorHoras se creó exitosamente.")
else:
    print("La tabla MarcadorHoras ya existe en la base de datos.")

# Generar datos ficticios y realizar inserciones
if not tabla_existe:
    # Generar 150 registros ficticios utilizando Faker
    registros = []
    for _ in range(150):
        empleado_id = random.randint(1, 100)
        proyecto_id = random.randint(1, 100)  # Valor aleatorio para proyectoID
        fecha = fake.date_between_dates(date_start=datetime(2018, 1, 1), date_end=datetime(2025, 12, 31))
        cantidad_horas = random.randint(1, 1500)  # Valor aleatorio para cantidadHoras
        
        registros.append((empleado_id, proyecto_id, fecha, cantidad_horas))

    # Insertar los registros en la tabla MarcadorHoras
    insert_query = "INSERT INTO MarcadorHoras (empleadoID, proyectoID, fecha, cantidadHoras) VALUES (%s, %s, %s, %s)"
    cursor.executemany(insert_query, registros)

    # Confirmar los cambios en la base de datos
    cnx.commit()
    print("Los datos se insertaron exitosamente.")
else:
    print("No se insertaron nuevos datos porque la tabla MarcadorHoras ya existe.")



##############PERMISO################################################################################################################################

# Verificar si la tabla Permiso ya existe
cursor.execute("SHOW TABLES LIKE 'Permiso'")
tabla_existe = cursor.fetchone()

if not tabla_existe:
    # Crear la tabla Permiso si no existe
    cursor.execute("""
        CREATE TABLE Permiso
        (
            permisoID INT AUTO_INCREMENT,
            tipoPermisoID INT,
            empleadoID INT,
            motivo VARCHAR(250) NOT NULL,
            diaInicio DATE NOT NULL,
            diaFin DATE NOT NULL,
            CONSTRAINT PK_Permiso PRIMARY KEY (permisoID),
            CONSTRAINT FK_Permiso FOREIGN KEY(empleadoID) REFERENCES Empleado(empleadoID)
        )
    """)

    # Confirmar los cambios en la base de datos
    cnx.commit()
    print("La tabla Permiso se creó exitosamente.")
else:
    print("La tabla Permiso ya existe en la base de datos.")

# Generar datos ficticios y realizar inserciones
if not tabla_existe:
    motivos = ["Permiso por horas", "Otros", "Vacaciones", "Cita Médica", "Emergencia"]

    # Obtener los empleados existentes en la tabla Empleado
    cursor.execute("SELECT empleadoID FROM Empleado")
    empleados = cursor.fetchall()

    # Generar 50 registros ficticios utilizando Faker
    registros = []
    for _ in range(150):
        tipo_permiso_id = random.randint(1, 100)  # Valor aleatorio para tipoPermisoID
        empleado_id = random.choice(empleados)[0]  # Seleccionar un empleado aleatorio de los existentes
        motivo = random.choice(motivos)  # Seleccionar un motivo aleatorio de la lista
        dia_inicio = fake.date_between_dates(date_start=datetime(2018, 1, 1), date_end=datetime(2025, 12, 31))
        dia_fin = dia_inicio + timedelta(days=random.randint(1, 7))  # Sumar días aleatorios para la duración del permiso
        
        registros.append((tipo_permiso_id, empleado_id, motivo, dia_inicio, dia_fin))

    # Insertar los registros en la tabla Permiso
    insert_query = "INSERT INTO Permiso (tipoPermisoID, empleadoID, motivo, diaInicio, diaFin) VALUES (%s, %s, %s, %s, %s)"
    cursor.executemany(insert_query, registros)

    # Confirmar los cambios en la base de datos
    cnx.commit()
    print("Los datos se insertaron exitosamente.")
else:
    print("No se insertaron nuevos datos porque la tabla Permiso ya existe.")


##############PERMISO PROCESADO ################################################################################################################################

# Verificar si la tabla PermisoProcesado ya existe
cursor.execute("SHOW TABLES LIKE 'PermisoProcesado'")
tabla_existe = cursor.fetchone()

if not tabla_existe:
    # Crear la tabla PermisoProcesado si no existe
    cursor.execute("""
        CREATE TABLE PermisoProcesado
        (
            permisoProcesadoID INT AUTO_INCREMENT,
            permisoID INT,
            horasProcesadas INT NOT NULL,
            tipoProceso VARCHAR(30) NOT NULL,
            CONSTRAINT PK_PermisoProcesado PRIMARY KEY (permisoProcesadoID),
            CONSTRAINT FK_PermisoProcesado FOREIGN KEY(permisoID) REFERENCES Permiso(permisoID)
        )
    """)

    # Confirmar los cambios en la base de datos
    cnx.commit()
    print("La tabla PermisoProcesado se creó exitosamente.")
else:
    print("La tabla PermisoProcesado ya existe en la base de datos.")

# Generar datos ficticios y realizar inserciones
if not tabla_existe:
    # Obtener los permisos existentes en la tabla Permiso
    cursor.execute("SELECT permisoID FROM Permiso")
    permisos = cursor.fetchall()

    # Generar 100 registros ficticios utilizando Faker
    registros = []
    tipos_proceso = ["Aprobado", "Rechazado", "Pendiente"]

    for _ in range(150):
        permiso_id = random.choice(permisos)[0]  # Seleccionar un permiso aleatorio de los existentes
        horas_procesadas = random.randint(1, 8)  # Generar horas procesadas aleatorias
        tipo_proceso = random.choice(tipos_proceso)  # Seleccionar un tipo de proceso aleatorio
        
        registros.append((permiso_id, horas_procesadas, tipo_proceso))

    # Insertar los registros en la tabla PermisoProcesado
    insert_query = "INSERT INTO PermisoProcesado (permisoID, horasProcesadas, tipoProceso) VALUES (%s, %s, %s)"
    cursor.executemany(insert_query, registros)

    # Confirmar los cambios en la base de datos
    cnx.commit()
    print("Los datos se insertaron exitosamente.")
else:
    print("No se insertaron nuevos datos porque la tabla PermisoProcesado ya existe.")

################APROBADOR PERMISO############################################################################################################################


# Verificar si la tabla AprobadorPermiso ya existe
cursor.execute("SHOW TABLES LIKE 'AprobadorPermiso'")
tabla_existe = cursor.fetchone()

if not tabla_existe:
    # Crear la tabla AprobadorPermiso si no existe
    cursor.execute("""
        CREATE TABLE AprobadorPermiso
        (
            aprobadorPermisoID INT AUTO_INCREMENT,
            permisoID INT,
            fechaAprobacion DATE NOT NULL,
            comentario VARCHAR(250),
            CONSTRAINT PK_AprobadorPermiso PRIMARY KEY (aprobadorPermisoID),
            CONSTRAINT FK_AprobadorPermiso FOREIGN KEY(permisoID) REFERENCES Permiso(permisoID)
        )
    """)

    # Confirmar los cambios en la base de datos
    cnx.commit()
    print("La tabla AprobadorPermiso se creó exitosamente.")
else:
    print("La tabla AprobadorPermiso ya existe en la base de datos.")

# Generar datos ficticios y realizar inserciones
if not tabla_existe:
    # Obtener los permisos existentes en la tabla Permiso
    cursor.execute("SELECT permisoID FROM Permiso")
    permisos = cursor.fetchall()

    # Generar 100 registros ficticios utilizando Faker
    registros = []

    for _ in range(150):
        permiso_id = random.choice(permisos)[0]  # Seleccionar un permiso aleatorio de los existentes
        fecha_aprobacion = fake.date_between_dates(date_start=datetime(2018, 1, 1), date_end=datetime(2023, 12, 31))  # Generar fecha aleatoria
        comentario = fake.text(max_nb_chars=250)  # Generar comentario aleatorio
        
        registros.append((permiso_id, fecha_aprobacion, comentario))

    # Insertar los registros en la tabla AprobadorPermiso
    insert_query = "INSERT INTO AprobadorPermiso (permisoID, fechaAprobacion, comentario) VALUES (%s, %s, %s)"
    cursor.executemany(insert_query, registros)

    # Confirmar los cambios en la base de datos
    cnx.commit()
    print("Los datos se insertaron exitosamente.")
else:
    print("No se insertaron nuevos datos porque la tabla AprobadorPermiso ya existe.")


############################################AprobadorCentroCostos############################################################################################################################

# Verificar si la tabla AprobadorCentroCostos ya existe
cursor.execute("SHOW TABLES LIKE 'AprobadorCentroCostos'")
tabla_existe = cursor.fetchone()

if not tabla_existe:
    # Crear la tabla AprobadorCentroCostos si no existe
    cursor.execute("""
        CREATE TABLE AprobadorCentroCostos
        (
            aprobadorCentroCostosID INT AUTO_INCREMENT,
            empleadoID INT,
            centroCostosID INT,
            subsidiariaID INT,
            fechaInicio DATE NOT NULL,
            fechaFin DATE NOT NULL,
            CONSTRAINT PK_AprobadorCentro PRIMARY KEY (aprobadorCentroCostosID),
            CONSTRAINT FK_AprobadorCentroA FOREIGN KEY(empleadoID) REFERENCES Empleado(empleadoID),
            CONSTRAINT FK_AprobadorCentroB FOREIGN KEY(centroCostosID) REFERENCES CentroCostos(centroCostosID),
            CONSTRAINT FK_AprobadorCentroC FOREIGN KEY(subsidiariaID) REFERENCES Subsidiaria(subsidiariaID)
        )
    """)

    # Confirmar los cambios en la base de datos
    cnx.commit()
    print("La tabla AprobadorCentroCostos se creó exitosamente.")
else:
    print("La tabla AprobadorCentroCostos ya existe en la base de datos.")

# Generar datos ficticios y realizar inserciones
if not tabla_existe:
    # Obtener los IDs de empleados, centros de costos y subsidiarias existentes
    cursor.execute("SELECT empleadoID FROM Empleado")
    empleados = cursor.fetchall()

    cursor.execute("SELECT centroCostosID FROM CentroCostos")
    centros_costos = cursor.fetchall()

    cursor.execute("SELECT subsidiariaID FROM Subsidiaria")
    subsidiarias = cursor.fetchall()

    # Generar 100 registros ficticios utilizando Faker
    registros = []

    for _ in range(150):
        empleado_id = random.choice(empleados)[0]  # Seleccionar un empleado aleatorio de los existentes
        centro_costos_id = random.choice(centros_costos)[0]  # Seleccionar un centro de costos aleatorio de los existentes
        subsidiaria_id = random.choice(subsidiarias)[0]  # Seleccionar una subsidiaria aleatoria de las existentes
        fecha_inicio = fake.date_between_dates(date_start=datetime(2018, 1, 1), date_end=datetime(2023, 12, 31))  # Generar fecha aleatoria
        fecha_fin = fake.date_between_dates(date_start=fecha_inicio, date_end=datetime(2023, 12, 31))  # Generar fecha aleatoria posterior a la fecha de inicio

        registros.append((empleado_id, centro_costos_id, subsidiaria_id, fecha_inicio, fecha_fin))

    # Insertar los registros en la tabla AprobadorCentroCostos
    insert_query = "INSERT INTO AprobadorCentroCostos (empleadoID, centroCostosID, subsidiariaID, fechaInicio, fechaFin) VALUES (%s, %s, %s, %s, %s)"
    cursor.executemany(insert_query, registros)

    # Confirmar los cambios en la base de datos
    cnx.commit()
    print("Los datos se insertaron exitosamente.")
else:
    print("No se insertaron nuevos datos porque la tabla AprobadorCentroCostos ya existe.")

##########################################################################################################################################


# Cerrar el cursor y la conexión
cursor.close()
cnx.close()
