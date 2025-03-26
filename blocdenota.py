import streamlit as st
import uuid
#_________________CLASES BASES_______________

 class Nota:
   def __init__(self, titulo, contenido):
     self.titulo    = titulo
     self.contenido = contenido
     self.id        = str(uuid.uuid4())
 
   def mostrar_contenido(self):
     raise NotImplementedError("")
 
   def editar (self, nuevo_titulo, nuevo_contenido):
     self.titulo    = nuevo_titulo
     self.contenido = nuevo_contenido
 
 class NotaTexto(Nota):
   def mostrar_contenido(self):
         return f"{self.contenido}"
 
 class NotaLista(Nota):
   def mostrar_contenido(self):
         items = self.contenido.split(',')
         return "\n".join([f"\n• {item.strip()}" for item in items])
 
 class NotaImagen(Nota):
   def mostrar_contenido(self):
         return self.contenido
 
# ________________GESTIÓN DE NOTAS_______________
 
 class BlocDeNotas:
   def __init__(self):
     self.notas = []
 
   def agregar_nota(self, nota):
     self.notas.append(nota)
 
   def eliminar_nota(self, nota_id):
     self.notas = [n for n in self.notas if n.id != nota_id]
 
   def obtener_por_tipo(self, tipo):
     return [n for n in self.notas if isinstance(n, tipo)]
 
   def buscar_por_titulo(self, texto_busqueda):
     return [n for n in self.notas if texto_busqueda.lower() in n.titulo.lower()]
 
   def obtener_todas(self):
     return self.notas
 
#_____________________INTERFAZ_________________
 
 def inicializar_sesion():
   if 'bloc' not in st.session_state:
       st.session_state.bloc = BlocDeNotas()
   if 'busqueda' not in st.session_state:
       st.session_state.busqueda = ''
 
 def mostrar_editor_nota():
   st.header("➕ Crear Nueva Nota")
 
   col1, col2 = st.columns([1, 2])
   with col1:
       tipo_nota = st.selectbox("Tipo de nota:", ["Texto", "Lista", "Imagen"])
       titulo = st.text_input("Título:")
 
   with col2:
     if tipo_nota == "Lista":
           contenido = st.text_input("Elementos (separados por comas):")
           st.caption("Ej: manzanas, pan, leche")
     elif tipo_nota == "Imagen":
           contenido = st.text_input("URL de imagen:")
           st.caption("Ej:https://fotito.com/imagen.jpg")
     else:
       contenido = st.text_area("Contenido:")
 
   if st.button("Crear Nota"):
       if titulo and contenido:
         if tipo_nota == "Texto":
           nueva = NotaTexto(titulo, contenido)
         elif tipo_nota == "Lista":
           nueva = NotaLista(titulo, contenido)
         else:
           nueva = NotaImagen(titulo, contenido)
 
         st.session_state.bloc.agregar_nota(nueva)
         st.success("¡Nota creada exitosamente!")
       else:
         st.error("Debes completar todos los campos")
 
 def mostrar_tarjeta_nota(nota, prefijo =""):
   with st.container():
     st.subheader(nota.titulo)
 
     if isinstance(nota, NotaImagen):
       try:
         st.image(nota.contenido, width=300)
       except:
         st.error("Error al cargar la imagen")
     else:
         st.markdown(nota.mostrar_contenido())
 
     with st.expander("✏️ Editar Nota"):
         nuevo_titulo = st.text_input("Título", value=nota.titulo,
                                      key=f"{prefijo}_titulo_{nota.id}")
         nuevo_contenido = st.text_area("Contenido", value=nota.contenido,
                                      key=f"{prefijo}_contenido_{nota.id}")
 
         if st.button("💾 Guardar Cambios", key= f"{prefijo}_guardar_{nota.id}"):
           nota.editar(nuevo_titulo,nuevo_contenido)
           st.rerun()
 
     if st.button("🗑️ Eliminar", key = f"{prefijo}_eliminar_{nota.id}"):
           st.session_state.bloc.eliminar_nota(nota.id)
           st.rerun()
 
     st.markdown("---")
 
 def mostrar_buscador():
   st.header("🔍 Buscar Notas")
   st.session_state.busqueda = st.text_input("Buscar por título:")
 
   if st.session_state.busqueda:
     resultados = st.session_state.bloc.buscar_por_titulo(st.session_state.busqueda)
 
     if resultados:
       st.subheader(f"_Resultados encontrados:_ {len(resultados)}")
       for nota in resultados:
         mostrar_tarjeta_nota(nota, "busqueda")
     else:
       st.warning("No se encontraron notas con ese título")
 
 def mostrar_vista_tabla(notas):
   datos = []
   for nota in notas:
       datos.append({
           "Título"   : nota.titulo,
           "Contenido": nota.mostrar_contenido() [:50] + "..."
       })
 
   st.dataframe(
       data = datos,
       column_config = {
           "Título": "Título",
           "Contenido": "Vista Previa"
       },
       use_container_width = True,
       hide_index = True
   )
 
 def mostrar_pestanas():
   tab1,tab2,tab3 = st.tabs(["📄 Texto", "📍 Listas", "🖼️ Imágenes"])
   with tab1:
     vista = st.selectbox("Modo de visualización", ["Tarjetas", "Tabla"],
                          key = "vista_texto")
     st.header("Notas de Texto")
     notas = st.session_state.bloc.obtener_por_tipo(NotaTexto)
     if notas:
       if vista == "Tarjetas":
         for nota in notas:
           mostrar_tarjeta_nota(nota, "pestana_texto")
       else:
         mostrar_vista_tabla(notas)
     else:
       st.info("No hay notas de texto creadas")
 
   with tab2:
     vista = st.selectbox("Modo de visualización:", ["Tarjetas", "Tabla"],
                          key = "vista_listas")
     st.header("Listas de Tareas")
     notas = st.session_state.bloc.obtener_por_tipo(NotaLista)
     if notas:
       if vista == "Tarjetas":
         for nota in notas:
           mostrar_tarjeta_nota(nota, "persona_lista")
       else:
         mostrar_vista_tabla(notas)
     else:
       st.info("No hay listas creadas")
 
   with tab3:
     vista = st.selectbox("Modo de visualización:", ["Tarjetas", "Tabla"],
                          key = "vista_imagenes")
     st.header("Notas con Imágenes")
     notas = st.session_state.bloc.obtener_por_tipo(NotaImagen)
     if notas:
       if vista == "Tarjetas":
         for nota in notas:
           mostrar_tarjeta_nota(nota, "persona_imagenes")
       else:
         mostrar_vista_tabla(notas)
     else:
       st.info("No hay imágenes guardadas")
 
 
#______________________MAIN_______________________
 
 def main():
   st.set_page_config(page_title="Bloc de Notas",layout="wide")
   st.title("📚 Bloc de :blue[Notas]")
 
   inicializar_sesion()
   mostrar_editor_nota()
   st.markdown("---")
 
   mostrar_buscador()
   st.markdown("---")
 
   mostrar_pestanas()
   st.markdown("---")
 
   st.header("📋 Vista General de Notas")
   todas_notas = st.session_state.bloc.obtener_todas()
   if todas_notas:
     mostrar_vista_tabla(todas_notas)
   else:
     st.info("No hay Notas creadas aún")
 
 if __name__ == "__main__":
   main()

