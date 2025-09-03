import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st
from PIL import Image

employee_data_path = 'Employee_data.csv'
employee_data = pd.read_csv(employee_data_path)

# 1.- Desplegar de un título y una breve descripción

st.title('Desempeño de los colaboradores del Área de Marketing')
st.text('Este dashboard web contiene indicadores y filtros del desemenpeño, ' \
'promedio de horas trabajadas, edad, genero y salario de los colabaoradores ' \
'del Área de Marketing')

# 2.- Desplegar el logotipo de la empresa.

logo = Image.open('Logo.png')
st.sidebar.image(logo)

# 3.- Desplegar un control para seleccionar el género.

selected_gender = st.sidebar.multiselect("Selecciona el género del empleado", 
                                    employee_data['gender'].unique(), default=employee_data['gender'].unique())
st.sidebar.write(f"Opcion Seleccionada: {selected_gender!r}")
employee_data_aux = employee_data.loc[employee_data['gender'].isin(selected_gender)]

# 4.- Desplegar un control para seleccionar un rango del puntaje de desempeño.

selected_performance = st.sidebar.slider('Selecciona la calificació de desempeño del empleado',
                                         min_value=float(employee_data['performance_score'].min()),
                                         max_value=float(employee_data['performance_score'].max()), 
                                         value= (1.0 ,4.0))
st.sidebar.write(f"Valores seleccionados: {selected_performance!r}")
employee_data_aux = employee_data_aux.loc[(employee_data_aux['performance_score']>=selected_performance[0]) & 
                                          (employee_data_aux['performance_score']<=selected_performance[1])]

# 5.- Desplegar un control para seleccionar el estado civil.

selected_marital_status = st.sidebar.multiselect("Selecciona el estado civil del empleado", 
                                                employee_data['marital_status'].unique(), 
                                                default=employee_data['marital_status'].unique())
st.sidebar.write(f"Opcion Seleccionada: {selected_marital_status!r}")
employee_data_aux = employee_data_aux.loc[employee_data['marital_status'].isin(selected_marital_status)]

# 6.- Gráfico en donde se visualice la distribución de los puntajes de desempeño.

fig = px.histogram(employee_data_aux, x='performance_score', hover_data='performance_score', 
                   title="Histograma de puntaje de desempeño")
st.write(fig)

# 7.- Gráfico en donde se visualice el promedio de horas trabajadas por el género

hours_by_gender = employee_data_aux[['gender', 'average_work_hours']].groupby('gender', 
                                                                          as_index=False).mean()
fig2 = px.bar(hours_by_gender, x='gender', y='average_work_hours', 
              title='Horas trabajadas promedio por genero')
st.write(fig2)

# 8.- Gráfico en donde se visualice la edad de los empleados con respecto al salario

salary_by_age = employee_data_aux[['salary', 'age']].groupby('age', 
                                                         as_index=False).mean()
fig3 = px.bar(salary_by_age, x='age', y='salary', 
              title='Salario por edad')
st.write(fig3)

# 9.- Gráfico en donde se visualice la relación del promedio de horas trabajadas versus el puntaje de desempeño

fig4 = px.scatter(employee_data_aux, x='average_work_hours', y='performance_score', 
                  color='gender', title='Horas promedio trabajadas vs puntaje de desempeño')
st.write(fig4)

# 10.- Conclusión sobre el análisis mostrado

st.markdown(f'En este analisis se estan considerando **{employee_data_aux['id_employee'].count()}** empleados, ' \
        f'cuyo promedio de la calificación de su desempeño es: **{employee_data_aux['performance_score'].mean():,.1f}**, ' \
        f'en promedio trabajan: **{employee_data_aux['average_work_hours'].mean():,.0f}** horas, ' \
        f'su salario promedio es: **${employee_data_aux['salary'].mean():,.0f}** y ' \
        f'la edad promedio es : **{employee_data_aux['age'].mean():,.0f}**')
