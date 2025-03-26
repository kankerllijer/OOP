import streamlit as st
from datetime import datetime, time
import uuid

Paises_europa = [
    "Albania", "Alemania", "Andorra", "Austria", "Bélgica", "Bielorrusia",
    "Bosnia y Herzegovina",  "Bulgaria",  "Chequia", "Chipre",  "Croacia",
    "Dinamarca",   "Eslovaquia",     "Eslovenia",   "España",   "Estonia",
    "Finlandia",   "Francia",    "Gran Bretaña",    "Grecia",   "Holanda",
    "Hungría",     "Italia",     "Irlanda",       "Islandia",   "Letonia",
    "Liechtenstein",   "Lituania",  "Luxemburgo", "Macedonia", "Moldavia",
    "Malta",   "Mónaco",   "Noruega",  "Polonia",   "Portugal", "Rumania",
    "Rusia",   "San Marino",  "Serbia y Montenegro",   "Suecia",  "Suiza",
    "Ucrania"
]

class Aereolinia:
    class Traduccion:
        def __init__(self):
            self.meses_traduccion = {
                "January": "enero",   "February": "febrero",      "March": "marzo",
                "April": "abril", "May": "mayo", "June": "junio",  "July": "julio",
                "August": "agosto", "September": "septiembre","October": "octubre",
                "November": "noviembre", "December": "diciembre"
            }

            self.dias_traduccion = {
                "Monday": "Lunes", "Tuesday": "Martes", "Wednesday": "Miércoles",
                "Thursday": "Jueves", "Friday": "Viernes",  "Saturday": "Sábado",
                "Sunday": "Domingo"
            }

        def formatear_fecha(self, fecha):
            dia_español = fecha.strftime("%A")
            mes_español = fecha.strftime("%B")
            return f"{self.dias_traduccion[dia_español]} {fecha.day} de {self.meses_traduccion[mes_español]}"

    def __init__(self):
        self.aerofly         = "AeroFly"
        self.destinos        = []
        self.vuelos          = []
        self.dias_salida     = ["Lunes", "Miércoles", "Viernes"]
        self.horarios_salida = [f"{h}:00" for h in range(5, 21)]
        self.ingresos        = []
        self.traductor       = self.Traduccion()
        self.reservas        = []

    def registros_ingresos(self, mensaje):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.ingresos.append(f"[{timestamp}] {mensaje}")

    def verificar_destino(self, destino):
        if destino in Paises_europa and destino not in self.destinos:
            self.destinos.append(destino)
            self.registros_ingresos(f"Destino agregado: {destino}")
            return True
        return False

    def eliminar_destino(self, destino):
        if destino in self.destinos:
            self.destinos.remove(destino)
            self.registros_ingresos(f"Destino eliminado: {destino}")
            return True
        return False

    def crear_vuelos(self, destino, fecha_hora):
        for vuelo in self.vuelos:
            if vuelo.destino == destino and vuelo.fecha_hora == fecha_hora:
                return False

        num_vuelo = len(self.vuelos) + 100
        nuevo_vuelo = Vuelo(destino, fecha_hora, num_vuelo)
        self.vuelos.append(nuevo_vuelo)
        self.registros_ingresos(f"Vuelo creado: {destino} - {fecha_hora}")
        return True

    def cancelar_vuelo(self, indice):
        if 0 <= indice < len(self.vuelos):
            vuelo_cancelado = self.vuelos.pop(indice)
            self.registros_ingresos(f"Vuelo cancelado: {vuelo_cancelado.destino}")
            return True
        return False

    def buscar_vuelos(self, destino=None):
        if destino:
            return [vuelo for vuelo in self.vuelos if vuelo.destino == destino]
        return self.vuelos.copy()

    def agregar_reserva(self, reserva):
        self.reservas.append(reserva)
        self.registros_ingresos(f"Reserva creada: {reserva.codigo}")

    def buscar_reserva(self, codigo):
        for reserva in self.reservas:
            if reserva.codigo == codigo:
                return reserva
        return None

    def cancelar_reserva(self, codigo):
        reserva = self.buscar_reserva(codigo)
        if reserva:
            self.reservas.remove(reserva)
            reserva.vuelo.asientos_disponibles += 1
            return True
        return False

class Vuelo:
    def __init__(self, destino, fecha_hora, num_vuelo, asientos=100):
        self.destino              = destino
        self.fecha_hora           = fecha_hora
        self.num_vuelo            = num_vuelo
        self.asientos_disponibles = asientos

class Pasajero:
    def __init__(self, nombre, pasaporte, contacto):
        self.nombre    = nombre
        self.pasaporte = pasaporte
        self.contacto  = contacto

    def __str__(self):
        return f"{self.nombre} | Pasaporte: {self.pasaporte} | Contacto: {self.contacto}"

class Reserva:
    def __init__(self, pasajero, vuelo):
        self.pasajero      = pasajero
        self.vuelo         = vuelo
        self.codigo        = f"RES-{uuid.uuid4().hex[:6].upper()}"
        self.fecha_reserva = datetime.now()

    def mostrar_info(self):
        return (
            f"Código: {self.codigo} | "
            f"Pasajero: {self.pasajero.nombre} | "
            f"Vuelo: {self.vuelo.num_vuelo} | "
            f"Fecha Reserva: {self.fecha_reserva.strftime('%d/%m/%Y %H:%M')}"
        )

if "Aereolinia" not in st.session_state:
    st.session_state.Aereolinia = Aereolinia()

st.set_page_config(page_title="AeroFly",layout="wide")
st.title(f"✈️ {st.session_state.Aereolinia.aerofly}")

# Gestión de destinos
st.subheader("**_Administrar Destinos_**")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Agregar destino")
    nuevo_destino = st.selectbox("Países disponibles:", sorted(Paises_europa), key="nuevo_destino")
    if st.button("➕ Agregar"):
        if st.session_state.Aereolinia.verificar_destino(nuevo_destino):
            st.success(f"Destino {nuevo_destino} agregado")
            st.rerun()

with col2:
    st.subheader("Eliminar destino")
    if st.session_state.Aereolinia.destinos:
        eliminar_destino = st.selectbox("Destinos registrados:",
                                      sorted(st.session_state.Aereolinia.destinos),
                                      key="eliminar_destino")
        if st.button("🗑️ Eliminar"):
            if st.session_state.Aereolinia.eliminar_destino(eliminar_destino):
                st.success(f"Destino {eliminar_destino} eliminado")
                st.rerun()

# Programación de vuelos
st.header("Programación de Vuelos", divider="red")
if st.session_state.Aereolinia.destinos:
    destino = st.selectbox("Seleccione destino:",
                         sorted(st.session_state.Aereolinia.destinos),
                         key="destino_vuelo")

    col1, col2 = st.columns(2)
    with col1:
        fecha = st.date_input("Fecha de salida:", min_value=datetime.today())
    with col2:
        hora = st.selectbox("Hora de salida:", st.session_state.Aereolinia.horarios_salida)

    if st.button("🛫 Programar vuelo", type="primary"):
        try:
            hora_dt = datetime.strptime(hora, "%H:%M").time()
            fecha_hora = datetime.combine(fecha, hora_dt)

            dia_en = fecha.strftime("%A")
            dia_es = st.session_state.Aereolinia.traductor.dias_traduccion[dia_en]

            if dia_es not in st.session_state.Aereolinia.dias_salida:
                raise ValueError(f"Día no permitido. Días válidos: {', '.join(st.session_state.Aereolinia.dias_salida)}")

            if st.session_state.Aereolinia.crear_vuelos(destino, fecha_hora):
                st.success("Vuelo programado exitosamente!")
                st.rerun()
            else:
                st.error("Este vuelo ya está registrado.")

        except Exception as e:
            st.error(str(e))
else:
    st.info("Primero agregue destinos disponibles")

# Gestión de pasajeros
st.header("Gestión de Pasajeros", divider="red")
st.subheader("**_Reservar Asiento_**")
if st.session_state.Aereolinia.vuelos:
    vuelos_disponibles = [f"{v.num_vuelo} - {v.destino} ({v.fecha_hora.strftime('%d/%m/%Y %H:%M')})"
                        for v in st.session_state.Aereolinia.vuelos]
    vuelo_seleccionado = st.selectbox("Vuelos disponibles:", vuelos_disponibles)
    idx_vuelo = vuelos_disponibles.index(vuelo_seleccionado)
    vuelo = st.session_state.Aereolinia.vuelos[idx_vuelo]

    nombre    = st.text_input("Nombre completo:")
    pasaporte = st.text_input("Número de pasaporte:")
    contacto  = st.text_input("Contacto (email/teléfono):")

    if st.button("✅ Confirmar reserva"):
        if all([nombre, pasaporte, contacto]):
            pasajero = Pasajero(nombre, pasaporte, contacto)
            if vuelo.asientos_disponibles > 0:
                # Verificar pasaporte único en el vuelo
                reservas_existentes = [r for r in st.session_state.Aereolinia.reservas
                                      if r.vuelo == vuelo and r.pasajero.pasaporte == pasaporte]
                if reservas_existentes:
                    st.error("Este pasaporte ya tiene reserva en este vuelo")
                else:
                    reserva = Reserva(pasajero, vuelo)
                    st.session_state.Aereolinia.agregar_reserva(reserva)
                    vuelo.asientos_disponibles -= 1
                    st.success(f"Reserva exitosa! Código: {reserva.codigo}")
                    st.rerun()
            else:
                st.error("Error: No hay asientos disponibles")
        else:
            st.warning("Complete todos los campos")
else:
    st.info("No hay vuelos programados")

# Listado de vuelos
st.header("Vuelos Programados", divider="red")
buscar_por = st.radio("Filtrar por:", ["Todos", "Destino"], horizontal=True)
destino_busqueda = None

if buscar_por == "Destino" and st.session_state.Aereolinia.destinos:
    destino_busqueda = st.selectbox("Seleccione destino:",
                                  sorted(st.session_state.Aereolinia.destinos),
                                  key="buscar_destino")

vuelos = st.session_state.Aereolinia.buscar_vuelos(destino_busqueda)

if vuelos:
    for i, vuelo in enumerate(vuelos):
        fecha_formateada = st.session_state.Aereolinia.traductor.formatear_fecha(vuelo.fecha_hora)
        reservas_vuelo = [r for r in st.session_state.Aereolinia.reservas if r.vuelo == vuelo]
        with st.expander(f"Vuelo {vuelo.num_vuelo} - {vuelo.destino}"):
            st.markdown(f"""
            **Fecha:** {fecha_formateada}
            **Hora:** {vuelo.fecha_hora.strftime('%H:%M')}
            **Asientos disponibles:** {vuelo.asientos_disponibles}
            **Pasajeros registrados:** {len(reservas_vuelo)}
            """)
            if reservas_vuelo:
                st.write("**Detalle de pasajeros:**")
                for reserva in reservas_vuelo:
                    st.write(f"- {reserva.pasajero} | Código Reserva: {reserva.codigo}")
            # Botón para cancelar vuelo
            if st.button(f"Cancelar Vuelo {vuelo.num_vuelo}", key=f"cancel_vuelo_{i}"):
                if st.session_state.Aereolinia.cancelar_vuelo(i):
                    st.success("Vuelo cancelado exitosamente")
                    st.rerun()
                else:
                    st.error("Error al cancelar el vuelo")
else:
    st.info("No se encontraron vuelos")

# Cancelar reservas
st.subheader("Cancelar Reserva")
codigo_reserva = st.text_input("Ingrese código de reserva:")
if st.button("❌ Cancelar reserva"):
    if st.session_state.Aereolinia.cancelar_reserva(codigo_reserva):
        st.success("Reserva cancelada")
        st.rerun()
    else:
        st.error("Código inválido")
