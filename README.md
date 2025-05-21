# 🛍️ Análisis de Ventas - Tiendas de Conveniencia

Este proyecto presenta un análisis visual e interactivo de un conjunto de datos, bajo este contexto:
> Una cadena de tiendas de conveniencia quiere analizar sus ventas y el comportamiento de
> los clientes para mejorar su estrategia de marketing. Para ello, han recopilado un conjunto
> de datos que incluye información sobre las ventas, los productos y los clientes. Su misión
> será usar estas técnicas de visualización de datos para analizar y presentar
> los resultados de este conjunto de datos

---

## 📁 Archivos incluidos

- `data.csv`: Dataset original incluyendo fecha, producto, método de pago, género del cliente, precio, total y más.
- `analisis.ipynb`: Notebook exploratorio con análisis en Python (Pandas, Seaborn, Plotly).
- `dashboard.py`: Aplicación interactiva construida con Streamlit que integra visualizaciones y conclusiones.

---

## ▶️ Cómo ejecutar el dashboard

1. **Clona este repositorio**:

```bash
git clone https://github.com/tu_usuario/tu_repositorio.git
cd tu_repositorio
```
Instala las dependencias:

Se recomienda usar un entorno virtual:
```bash
python -m venv env
source env/bin/activate  # o env\\Scripts\\activate en Windows
pip install -r requirements.txt
```
O instalar directamente:
```bash
pip install streamlit pandas matplotlib seaborn plotly nbformat numpy
```
Ejecuta el dashboard:
```bash
streamlit run dashboard.py
```
Esto abrirá la app en tu navegador en http://localhost:8501

# 📊 Funcionalidades del Dashboard
Filtros interactivos por producto, ciudad y género.

Indicadores clave (ventas totales, calificaciones, ingresos brutos).

Gráficos:

- Líneas (ventas mensuales)

- Boxplots (distribución de precios)

- Histogramas (calificaciones)

- Gráficos 3D (precio, total, satisfacción)

- Visualización del dataset (head(20))

# 👨‍🏫 Autoría y contexto
Trabajo realizado para la asignatura Visualización de Información en la Era del Big Data. Incluye análisis descriptivo, selección de variables clave y conclusiones basadas en los datos.

Grupo:
- Tamara Aragón Estay
- German Cigna Gutierrez
- Nicolas Lampe Huenul
- Manuel Riquelme Mardones
- Andrés Vera Moraga
