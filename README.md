# ☕ Estimador de Puntaje SCA para Café

Aplicación web de **Machine Learning** desarrollada en Python para estimar el puntaje de taza de un café a partir de características del grano verde y atributos de evaluación sensorial.

El proyecto integra procesamiento de datos, entrenamiento de un modelo de Machine Learning y despliegue de una aplicación interactiva mediante **Streamlit**.

## 🚀 Demo

**Aplicación web:**  
https://sca-coffee-predictor.streamlit.app/

**Código fuente:**  
https://github.com/YoferML/sca-coffee-predictor

---

## 🎯 Objetivo

El objetivo del proyecto es desarrollar una herramienta que permita obtener una **estimación del puntaje SCA** a partir de información relacionada con un lote de café.

La aplicación combina:

- Características del café verde.
- Información de origen y procesamiento.
- Atributos de evaluación sensorial.
- Evaluación taza por taza.
- Un modelo de Machine Learning para generar una estimación.

El sistema busca servir como herramienta de apoyo para la evaluación y análisis de muestras de café.

---

## 🧠 Flujo del proyecto

```text
Dataset de café
       │
       ▼
Limpieza y preparación de datos
       │
       ▼
Entrenamiento del modelo
       │
       ▼
Exportación del modelo (.pkl)
       │
       ▼
Integración con Streamlit
       │
       ▼
Aplicación web
       │
       ▼
Estimación del puntaje SCA
```

---

## 📊 Datos

El dataset utilizado fue obtenido desde **Kaggle** y posteriormente procesado en Python mediante **Google Colab**.

El proceso de preparación incluyó tareas de limpieza y transformación de los datos para poder utilizarlos durante el entrenamiento del modelo.

El proyecto también contempla información relacionada con cafés de distintos países y características del café verde.

> **Nota:** el modelo actual tiene una representación limitada de algunas categorías de origen. En particular, la cantidad de datos disponibles para cafés peruanos es reducida, por lo que las estimaciones asociadas a Perú deben interpretarse con cautela.

---

## 🤖 Machine Learning

El modelo fue desarrollado y entrenado en **Google Colab** utilizando Python y posteriormente exportado en formato `.pkl`.

El archivo:

```text
modelo_sca_v3.pkl
```

contiene el modelo entrenado utilizado por la aplicación web.

La aplicación carga este modelo y utiliza las características ingresadas por el usuario para generar una estimación.

### Proceso general

```python
Datos de entrada
       ↓
Preprocesamiento
       ↓
Modelo entrenado
       ↓
Predicción
       ↓
Estimación del puntaje
```

---

## 🌐 Aplicación web

La interfaz fue desarrollada utilizando **Streamlit**, permitiendo ejecutar el modelo de Machine Learning desde una aplicación web interactiva.

La aplicación permite ingresar información del café organizada en diferentes secciones.

### 1. Origen y características del café verde

Se ingresan datos como:

- Altitud.
- Humedad.
- Proceso.
- Variedad.
- País.
- Defectos de categoría 1.
- Defectos de categoría 2.

### 2. Evaluación sensorial

La aplicación permite registrar los atributos sensoriales utilizados en la evaluación del café.

Los atributos se introducen utilizando una escala de puntuación.

### 3. Evaluación taza por taza

También se registra información correspondiente a las tazas evaluadas, incluyendo aspectos como:

- Uniformidad.
- Limpieza.
- Dulzor.
- Defectos de taza.

### 4. Resultado

Finalmente, el sistema presenta:

- Puntaje calculado.
- Estimación realizada por Machine Learning.
- Desglose del resultado.
- Alertas cuando existe una diferencia importante entre el cálculo y la estimación del modelo.

---

## 🧮 Cálculo del puntaje

La aplicación considera la evaluación de los diferentes atributos y componentes de la ficha de catación para obtener el puntaje correspondiente.

Además del cálculo del puntaje, el sistema muestra una estimación generada por el modelo de Machine Learning.

Esto permite comparar:

```text
Puntaje de evaluación
        ↕
Estimación del modelo ML
```

La diferencia entre ambos valores puede utilizarse como una señal para revisar los datos ingresados.

---

## 🇵🇪 Consideración para cafés peruanos

La aplicación permite seleccionar **Perú** como país de origen.

Sin embargo, el modelo actual fue entrenado con una cantidad limitada de registros peruanos. Por esta razón, la predicción para cafés peruanos debe considerarse como una estimación general y no como un modelo especializado para café peruano.

Una futura versión podría incorporar un conjunto de datos más amplio de cafés provenientes de:

- Cajamarca.
- San Martín.
- Junín.
- Cusco.
- Puno.
- Otras regiones cafetaleras del Perú.

Esto permitiría desarrollar posteriormente modelos con mayor especialización para el contexto peruano.

---

## 🛠️ Tecnologías utilizadas

- **Python**
- **Pandas**
- **Scikit-Learn**
- **Google Colab**
- **Streamlit**
- **Pickle**
- **Git**
- **GitHub**

---

## 📁 Estructura del proyecto

```text
sca-coffee-predictor/
│
├── app.py
│   └── Aplicación web desarrollada con Streamlit
│
├── modelo_sca_v3.pkl
│   └── Modelo de Machine Learning entrenado
│
├── requirements.txt
│   └── Dependencias del proyecto
│
├── README.md
│   └── Documentación técnica
│
└── docs/
    └── manual-usuario.md
        └── Guía para utilizar la aplicación
```

---

## ▶️ Ejecución local

Clonar el repositorio:

```bash
git clone https://github.com/YoferML/sca-coffee-predictor.git
cd sca-coffee-predictor
```

Instalar las dependencias:

```bash
pip install -r requirements.txt
```

Ejecutar la aplicación:

```bash
streamlit run app.py
```

La aplicación se abrirá localmente en el navegador.

---

## 📖 Guía de uso

Para aprender qué información ingresar en cada campo de la aplicación, consultar:

**[Ficha de uso: Estimador de puntaje SCA](docs/manual-usuario.md)**

La guía explica:

- Qué significa cada campo.
- Qué valores se deben ingresar.
- Qué opciones seleccionar.
- Ejemplos de llenado.
- Cómo realizar la evaluación taza por taza.
- Cómo interpretar el resultado.
- Alertas del sistema.
- Errores comunes.

---

## ☁️ Despliegue

La aplicación se encuentra desplegada mediante **Streamlit** y conectada al repositorio de GitHub.

Cada actualización del código puede desplegarse nuevamente desde el repositorio.

**Demo:**  
https://sca-coffee-predictor.streamlit.app/

---

## ⚠️ Limitaciones

El resultado proporcionado por la aplicación debe considerarse una **estimación** y no sustituye una evaluación profesional de café.

Entre las principales limitaciones se encuentran:

- Cantidad limitada de datos para algunas categorías.
- Representación limitada de cafés peruanos.
- Dependencia de la calidad de los datos ingresados.
- El modelo no sustituye la evaluación sensorial realizada por un catador capacitado.

Además, las definiciones y criterios utilizados en la ficha de uso deben contrastarse con la documentación oficial de la **Specialty Coffee Association (SCA)** antes de utilizar el sistema como herramienta formal de capacitación o certificación.

---

## 🔮 Mejoras futuras

Algunas posibles líneas de desarrollo son:

- Incorporar una base de datos más amplia de cafés peruanos.
- Registrar nuevas catas realizadas mediante la aplicación.
- Incorporar regiones productoras del Perú.
- Mejorar la representación de variedades y procesos.
- Comparar diferentes modelos de Machine Learning.
- Incorporar métricas de evaluación del modelo.
- Implementar un historial de predicciones.
- Desarrollar visualizaciones para analizar las características del café.
- Mejorar la trazabilidad de las muestras utilizadas.

---

## 👨‍💻 Autor

**Yofer ML**

Matemático orientado a la Ingeniería de Machine Learning.

📍 Piura, Perú

GitHub:  
https://github.com/YoferML
