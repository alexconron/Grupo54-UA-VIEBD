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
Este proyecto presenta un análisis visual e interactivo de un conjunto de datos, bajo este contexto:

> Una cadena de tiendas de conveniencia quiere analizar sus ventas y el comportamiento de los clientes para mejorar su estrategia de marketing. Para ello, han recopilado un conjunto de datos que incluye información sobre las ventas, los productos y los clientes.
---
""")

st.markdown("### a. Examen del Conjunto de Datos")
st.dataframe(df.head(20))

st.markdown("""
---

### b. Variables Seleccionadas y Justificación
| Variable             | Justificación                                                                                                                            |
| -------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| `Product line`       | Permite identificar qué categorías de productos son más vendidas. Es esencial para segmentar el análisis por tipo de producto.           |
| `Month`              | Derivada de `Date`, esta variable permite observar tendencias mensuales y detectar patrones de comportamiento.                           |
| `Gender`             | Permite analizar diferencias entre hombres y mujeres, útil para estrategias de marketing diferenciadas.                                  |
| `Payment`            | Permite conocer las preferencias de método de pago de los clientes.                                                                      |
| `Quantity` y `Total` | Representan el volumen de ventas y el ingreso total por transacción.                                                                     |
| `Unit price`         | Analiza si productos más caros tienen menor o mayor frecuencia de compra.                                                                |
| `Rating`             | Refleja la percepción del cliente sobre su experiencia de compra, útil para evaluar satisfacción y fidelidad.                            |

---
""")

# Sidebar para filtros
st.sidebar.header("Filtros")
producto = st.sidebar.selectbox("Línea de Producto", options=['Todos'] + sorted(df['Product line'].unique()))
ciudad = st.sidebar.selectbox("Ciudad", options=['Todas'] + sorted(df['City'].unique()))
genero = st.sidebar.radio("Género", options=['Todos', 'Male', 'Female'])

filtro_df = df.copy()
if producto != 'Todos':
    filtro_df = filtro_df[filtro_df['Product line'] == producto]
if ciudad != 'Todas':
    filtro_df = filtro_df[filtro_df['City'] == ciudad]
if genero != 'Todos':
    filtro_df = filtro_df[filtro_df['Gender'] == genero]

# KPIs
st.subheader("📌 Indicadores Clave")
st.metric("Total Ventas ($)", f"{filtro_df['Total'].sum():,.2f}")
st.metric("Promedio de Calificaciones", f"{filtro_df['Rating'].mean():.2f}")
st.metric("Ingresos Brutos Promedio ($)", f"{filtro_df['gross income'].mean():,.2f}")

# Gráfico de líneas: Total mensual por línea de producto
st.subheader("📅 Ventas Totales Mensuales por Línea de Producto")

st.markdown("""
**¿Para qué sirve este gráfico?**  
Permite observar la evolución mensual de las ventas para cada línea de producto. Es clave para detectar estacionalidades o tendencias específicas por categoría.

**¿Qué muestra?**  
- Muestra el total vendido por cada línea de producto en cada mes.
- Al seleccionar "Todos", compara múltiples líneas de productos en el tiempo.
- Si se filtra una línea específica, se enfoca en su evolución individual.

**Conclusión**  
La visualización ayuda a identificar productos con ventas estacionales, comportamiento constante o eventos que afectaron su rendimiento. Es útil para planificar marketing segmentado y gestión de stock.
""")

if producto == "Todos":
    ventas_mensuales = (
        filtro_df.groupby(["Month", "Product line"])["Total"].sum().reset_index()
    )
    fig1 = px.line(
        ventas_mensuales,
        x="Month",
        y="Total",
        color="Product line",
        markers=True,
        title="Ventas Mensuales por Línea de Producto"
    )
else:
    ventas_mensuales = filtro_df.groupby("Month")["Total"].sum().reset_index()
    fig1 = px.line(
        ventas_mensuales,
        x="Month",
        y="Total",
        markers=True,
        title=f"Ventas Mensuales - {producto}"
    )

st.plotly_chart(fig1)

# Boxplot
st.subheader("📦 Distribución de Precios por Línea de Producto")
st.markdown("""
**¿Para qué sirve este gráfico?**  
Comparar la dispersión de precios entre productos. Útil para identificar productos premium o outliers.

**¿Qué muestra?**  
- *Sports and travel* tiene mayor variabilidad.
- *Health and beauty* es más homogénea.

**Conclusión**  
Las categorías con mayor variación podrían tener oportunidades para promociones segmentadas o estrategias de precios diferenciados.
""")
fig2, ax = plt.subplots()
sns.boxplot(data=filtro_df, x='Product line', y='Unit price', ax=ax)
plt.xticks(rotation=45)
st.pyplot(fig2)

# Histograma
st.subheader("⭐ Distribución de Calificaciones")
st.markdown("""
**¿Para qué sirve este gráfico?**  
Evaluar la percepción general del cliente sobre la experiencia de compra.

**¿Qué muestra?**  
- La mayoría de las calificaciones están por sobre 6.
- Hay pocos casos extremos de baja calificación.

**Conclusión**  
La percepción del cliente es mayoritariamente positiva, aunque hay margen para investigar los casos bajos.
""")
fig3 = px.histogram(filtro_df, x='Rating', nbins=20)
st.plotly_chart(fig3)

# Gráfico 3D
st.subheader("📊 Relación 3D: Precio, Total y Calificación")
st.markdown("""
**¿Para qué sirve este gráfico?**  
Explorar la relación entre precio del producto, total gastado y satisfacción del cliente.

**¿Qué muestra?**  
- Algunas categorías agrupan puntos con altas ventas y calificaciones.  
- Se observan relaciones interesantes entre el valor y la percepción.

**Conclusión**  
Se pueden detectar productos de alto rendimiento tanto en ventas como en satisfacción, ideales para destacar en campañas.
""")
fig4 = px.scatter_3d(filtro_df, x='Unit price', y='Total', z='Rating', color='Product line')
st.plotly_chart(fig4)

# Conclusión final
st.markdown("""
---
### ✅ Conclusiones Generales
1. **Preferencias por género**: Algunas líneas de productos tienen diferencias claras.
2. **Estrategia regional**: La ciudad impacta en comportamiento y métodos de pago.
3. **Satisfacción del cliente**: Buena en general, pero hay áreas para investigar.
4. **Relaciones clave**: Precio, monto gastado y rating muestran correlaciones interesantes.

---
### Créditos
Elaborado por el grupo 54, integrantes:
- Tamara Aragón Estay
- German Cigna Gutierrez
- Nicolas Lampe Huenul
- Manuel Riquelme Mardones
- Andrés Vera Moraga
""")
