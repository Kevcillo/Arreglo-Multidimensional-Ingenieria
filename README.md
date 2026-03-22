# 📊 Proyecto: Análisis y Simulación de Sistemas Computacionales

## 📌 Descripción

Este proyecto implementa diferentes problemas computacionales relacionados con:

* Análisis de fuerzas en estructuras
* Simulación de difusión en fluidos 3D
* Procesamiento de imágenes (suavizado)
* Análisis estadístico de sensores
* Transformaciones geométricas

Cada problema fue resuelto utilizando estructuras de datos como listas, matrices 2D y 3D, junto con algoritmos de recorrido y cálculo numérico.

---

## 🧠 Enfoque de solución

El enfoque principal utilizado en todos los problemas es:

* Uso de **estructuras matriciales (listas anidadas)** para representar sistemas físicos
* Aplicación de **algoritmos iterativos** (bucles) para recorrer datos
* Uso de **promedios y operaciones matemáticas** para simular comportamientos físicos
* Separación en funciones para mejorar la **modularidad y reutilización**

---

## ⚙️ Problemas implementados

### 🔹 Problema 1: Análisis de fuerzas

Se calcula:

* Suma de fuerzas por fila y columna
* Fuerza total del sistema
* Reacción necesaria para equilibrio

📌 Enfoque:
Uso de sumatorias y distribución uniforme.

---

### 🔹 Problema 2: Simulación de fluido 3D

Se simula la propagación de presión en una matriz 3D.

📌 Enfoque:

* Cada celda toma el promedio de sus vecinos
* Se usa copia de la matriz para evitar sobreescritura

📌 Impacto en eficiencia:
Complejidad O(N³), ya que se recorren todas las celdas del volumen.

---

### 🔹 Problema 3: Suavizado de imágenes 3D

Se reduce el ruido aplicando un filtro de promedio.

📌 Enfoque:

* Promedio de vecinos (incluyendo la celda central)
* Técnica similar a filtros en procesamiento de imágenes

📌 Impacto:
Reduce variaciones bruscas → mejora calidad de datos.

---

### 🔹 Problema 4: Análisis de sensores

Se calculan:

* Promedios
* Desviación estándar

📌 Enfoque:
Uso de fórmulas estadísticas básicas.

📌 Impacto:
Permite analizar estabilidad y variabilidad de los datos.

---

### 🔹 Problema 5: Transformación de coordenadas

Se aplica rotación a puntos en 2D.

📌 Enfoque:
Uso de matrices de rotación:

```
[cos -sin]
[sin  cos]
```

📌 Impacto:
Transformaciones eficientes con complejidad O(n).

---

## 🚀 Eficiencia de la solución

* Uso de listas y comprensión de listas mejora legibilidad
* Evita estructuras innecesarias
* Se minimiza duplicación de código
* Complejidad dominante:

  * Problemas 2 y 3: O(N³)
  * Problemas 1, 4 y 5: O(N²) o menor

---

## 🛠️ Tecnologías usadas

* Python 3
* Librerías estándar:

  * `math`
  * `random`

---

## ▶️ Cómo ejecutar

1. Clonar el repositorio:

```bash
git clone <URL_DEL_REPOSITORIO>
```

2. Ejecutar el archivo:

```bash
python archivo.py
```

