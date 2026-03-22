
# 📊 Arreglos Multidimensionales

## 📌 Descripción

Cinco problemas de ingeniería resueltos con matrices 2D y 3D en Python puro (sin dependencias externas).

---

## ⚙️ Problemas Resueltos

### 1. Análisis de Fuerzas
**Enfoque:** Matriz 3×3 con fuerzas. Sumatoria total y distribución equitativa en 4 apoyos.

**Eficiencia:** O(9) operaciones constantes. Al usar un tamaño fijo, el enfoque de recorrido completo no afecta el rendimiento.

---

### 2. Simulación de Fluido 3D
**Enfoque:** Volumen 3×3×3 donde cada celda almacena presión, temperatura y velocidad. Cada celda se actualiza por promedio de sus 26 vecinos, usando una copia independiente para evitar contaminación.

**Eficiencia:** O(27 × 26) por paso. El enfoque de promedios simples evita cálculos complejos (ecuaciones diferenciales), priorizando simplicidad sobre precisión física.

---

### 3. Suavizado de Imágenes
**Enfoque:** Volumen 3 capas × 5×5 píxeles. Filtro de promedio 3×3 aplicado capa por capa, recorriendo toda la matriz.

**Eficiencia:** O(75 × 9). El enfoque capa por capa permite procesamiento independiente, lo que facilita futura paralelización.

---

### 4. Análisis de Sensores
**Enfoque:** Matriz 5×5. Cálculo de promedio y desviación estándar por filas y columnas mediante recorrido completo.

**Eficiencia:** O(25). El enfoque de dos pasadas (una para promedio, otra para varianza) es aceptable para este tamaño, pero sería ineficiente para matrices grandes.

---

### 5. Transformación de Coordenadas
**Enfoque:** Puntos 2D almacenados en lista. Transformaciones mediante matrices (rotación) y operaciones directas (traslación, escalado).

**Eficiencia:** O(n) por transformación. El enfoque de aplicar la misma operación a cada punto independientemente permite escalamiento lineal.

---

## 🎯 Impacto del Enfoque en la Eficiencia

| Problema | Enfoque Elegido | Impacto en Eficiencia |
|----------|----------------|----------------------|
| **1** | Sumatoria directa | Mínimo overhead, ideal para matrices pequeñas |
| **2** | Promedio de vecinos | Evita cálculo de ecuaciones diferenciales; sacrifica precisión por velocidad |
| **3** | Procesamiento por capas | Permite paralelización potencial; independencia entre capas |
| **4** | Recorrido completo | Aceptable para 5×5; no escalable a grandes volúmenes de datos |
| **5** | Operaciones independientes | Escala lineal O(n); ideal para conjuntos de puntos grandes |

---

## 🛠️ Tecnologías

- Python 3
- Librerías estándar: `math`, `random`


## 📊 Resultados

| Problema | Estado |
|----------|--------|
| 1. Fuerzas | ✓ Equilibrio logrado |
| 2. Fluido | ✓ Propagación simulada |
| 3. Imágenes | ✓ Ruido reducido |
| 4. Sensores | ✓ Estadísticas calculadas |
| 5. Coordenadas | ✓ Transformaciones aplicadas |
