%%writefile app.py

import streamlit as st
from datetime import datetime

class ToDoList:
  def __init__(self):
    self.tareas=[]

  def crear_tarea(self,tarea,fecha):
    self.tareas.append({"tarea":tarea, "fecha": fecha})

  def borrar_tarea(self,eliminar_indice):
    if 0<= eliminar_indice<len(self.tareas):
      del self.tareas[eliminar_indice]

if 'todo' not in st.session_state:
  st.session_state.todo = ToDoList()

st.title("To-Do List")
st.divider()

nueva_tarea = st.text_input("Añadir una nueva tarea")
elegir_fecha=st.date_input("Selecciona la fecha para la tarea")

if st.button("Agregar")and nueva_tarea:
  st.session_state.todo.crear_tarea(nueva_tarea, elegir_fecha)

st.divider()

st.subheader("Tareas pendientes")
tareas_por_fechas={}

for hacer_tarea in st.session_state.todo.tareas:
  fecha_tarea = hacer_tarea ["fecha"].strftime("%d/%m/%Y")
  if fecha_tarea not in tareas_por_fechas:
    tareas_por_fechas[fecha_tarea]=[]
  tareas_por_fechas[fecha_tarea].append(hacer_tarea)


for fecha, tareas in tareas_por_fechas.items():
  with st.expander(f'{fecha} ({len(tareas)} tareas)'):
    for i,tarea in enumerate(tareas):
      col1,col2=st.columns([0.8,0.2])
      with col1:
        st.checkbox(tarea["tarea"], key=f'tarea_{fecha}_{i}')
      with col2:
        if st.button("X", key=f'eliminar_{fecha}_{i}'):
          index = st.session_state.todo.tareas.index(tarea)
          st.session_state.todo.borrar_tarea(index)
          st.rerun()
st.divider()
st.caption("Marca las tareas completadas")

