import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# Cargar los datos
@st.cache_data
def load_data():
    df = pd.read_csv("data.csv")
    df['Date'] = pd.to_datetime(df['Date'])
    df['Month'] = df['Date'].dt.to_period('M').astype(str)
    return df

df = load_data()

# Título del dashboard
st.title("Dashboard de Ventas - Tiendas de Conveniencia")

st.markdown("""
### Objetivo
Este dashboard tiene como propósito analizar y visualizar datos de ventas de una cadena de tiendas de conveniencia, con foco en patrones de comportamiento por género, ciudad, tipo de cliente y línea de productos.

---

### a. Examen del Conjunto de Datos
El conjunto de datos contiene información detallada sobre transacciones realizadas en una cadena de tiendas de conveniencia. Entre las columnas se incluyen datos como el producto vendido, género del cliente, método de pago, fecha, hora, monto total, entre otros.

**Vista previa del dataset:**
""")

# Mostrar el dataframe completo o una muestra filtrada
st.dataframe(df.head(20))

st.markdown("""
---

### b. Variables Seleccionadas y Justificación
| Variable             | Justificación                                                                                                                            |
| -------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| `Product line`       | Permite identificar qué categorías de productos son más vendidas. Es esencial para segmentar el análisis por tipo de producto.           |
| `Month`              | Derivada de `Date`, esta variable permite observar tendencias mensuales y detectar patrones de comportamiento en el tiempo.              |
| `Gender`             | Permite analizar diferencias de comportamiento entre hombres y mujeres, útil para estrategias de marketing diferenciadas.                |
| `Payment`            | Permite conocer las preferencias de método de pago de los clientes. Es útil para adaptar sistemas de cobro y promociones.                |
| `Quantity` y `Total` | Representan el volumen de ventas y el ingreso total por transacción. Son variables cuantitativas centrales en el análisis financiero.    |
| `Unit price`         | Relacionada con el valor individual de los productos, permite analizar si productos más caros tienen menor o mayor frecuencia de compra. |

---

### Variables Clave
- **Product line**: Categorías de productos vendidos.
- **Gender**: Género de los compradores.
- **City**: Ubicación de la tienda.
- **Total**: Monto total de la compra.
- **Unit price** y **Quantity**: Variables que permiten analizar precios y volúmenes.
- **Payment**: Método de pago.
- **Rating**: Evaluación del cliente.

---
""")

# Sidebar para filtros
st.sidebar.header("Filtros")
producto = st.sidebar.selectbox("Línea de Producto", options=['Todos'] + sorted(df['Product line'].unique().tolist()))
ciudad = st.sidebar.selectbox("Ciudad", options=['Todas'] + sorted(df['City'].unique().tolist()))
genero = st.sidebar.radio("Género", options=['Todos', 'Male', 'Female'])

# Aplicar filtros
filtro_df = df.copy()
if producto != 'Todos':
    filtro_df = filtro_df[filtro_df['Product line'] == producto]
if ciudad != 'Todas':
    filtro_df = filtro_df[filtro_df['City'] == ciudad]
if genero != 'Todos':
    filtro_df = filtro_df[filtro_df['Gender'] == genero]

# KPIs
st.subheader("Indicadores Clave")
st.metric("Total Ventas ($)", f"{filtro_df['Total'].sum():,.2f}")
st.metric("Promedio de Calificaciones", f"{filtro_df['Rating'].mean():.2f}")
st.metric("Ingresos Brutos Promedio ($)", f"{filtro_df['gross income'].mean():,.2f}")

# Gráfico de líneas: Total mensual
st.subheader("Ventas Totales por Mes")
ventas_mensuales = filtro_df.groupby("Month")['Total'].sum().reset_index()
fig1 = px.line(ventas_mensuales, x='Month', y='Total', markers=True, title="Ventas Mensuales")
st.plotly_chart(fig1)

# Boxplot: Precio por producto
st.subheader("Distribución de Precios por Línea de Producto")
fig2, ax = plt.subplots()
sns.boxplot(data=filtro_df, x='Product line', y='Unit price', ax=ax)
plt.xticks(rotation=45)
st.pyplot(fig2)

# Histograma de calificaciones
st.subheader("Distribución de Calificaciones")
fig3 = px.histogram(filtro_df, x='Rating', nbins=20)
st.plotly_chart(fig3)

# Gráfico 3D: Precio vs Total vs Rating
st.subheader("Relación 3D: Precio, Total y Calificación")
fig4 = px.scatter_3d(filtro_df, x='Unit price', y='Total', z='Rating', color='Product line')
st.plotly_chart(fig4)

st.markdown("""
---
### Conclusiones
1. **Preferencias por género**: Algunas líneas de productos tienen diferencias claras en preferencia entre hombres y mujeres.
2. **Distribución geográfica**: La ciudad influye en los patrones de consumo y métodos de pago.
3. **Satisfacción del cliente**: Las evaluaciones promedio (Rating) permiten inferir la percepción de calidad.
4. **Relación entre variables**: Hay correlaciones interesantes entre precio unitario, total y satisfacción.

---
### Créditos
Elaborado por el equipo de análisis de datos para la asignatura de Visualización.
""")
