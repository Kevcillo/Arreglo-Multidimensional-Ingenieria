
import random
import math

# ============================================
# FUNCIONES GENERALES
# ============================================


def imprimir_matriz(matriz, titulo=""):
    """
    Imprime una matriz (lista de listas) fila por fila.
    """
    print(f"\n{titulo}")
    for fila in matriz:
        print(fila)


def obtener_vecinos(x, y, z, N, incluir_centro=False):
    """
    Devuelve las coordenadas vecinas de una celda (x,y,z)
    
    - Recorre todas las combinaciones posibles (-1, 0, 1)
    - Filtra las que salen de los límites
    - Opcionalmente incluye la celda central
    """
    vecinos = [
        (x+dx, y+dy, z+dz)
        for dx in [-1, 0, 1]
        for dy in [-1, 0, 1]
        for dz in [-1, 0, 1]
        if (incluir_centro or (dx, dy, dz) != (0, 0, 0))
    ]

    # Filtrar solo los que están dentro del volumen
    return [(i, j, k) for i, j, k in vecinos if 0 <= i < N and 0 <= j < N and 0 <= k < N]


# ============================================
# PROBLEMA 1: ANÁLISIS DE FUERZAS
# ============================================


print("Problema 1 Análisis de fuerzas")

# Matriz 3x3 donde cada valor representa una fuerza en un nodo
fuerzas = [
    [10, -5, 3],
    [-2, 7, -1],
    [4, -6, 8]
]

imprimir_matriz(fuerzas, "Matriz de fuerzas (N):")

# Suma de cada fila → fuerza resultante por fila
suma_filas = [sum(fila) for fila in fuerzas]

# Suma de cada columna → usando zip para agrupar columnas
suma_columnas = [sum(col) for col in zip(*fuerzas)]

print("\nSuma por filas:", suma_filas)
print("Suma por columnas:", suma_columnas)

# Fuerza total del sistema (suma de todas las fuerzas)
fuerza_total = sum(suma_filas)

# Para equilibrio: la reacción debe ser igual y opuesta
reaccion_total = -fuerza_total

# Distribución uniforme en los 9 nodos
reaccion_por_nodo = reaccion_total / 9

print("\nFuerza total:", fuerza_total)
print("Reacción total:", reaccion_total)

# Crear matriz donde todos los nodos tienen la misma reacción
reacciones = [[reaccion_por_nodo]*3 for _ in range(3)]

imprimir_matriz(reacciones, "Matriz de reacciones:")


# ============================================
# PROBLEMA 2: SIMULACIÓN DE FLUIDO 3D
# ============================================

print(f"\nProblema 2 Simulación de fluido")

N = 3

# Crear una matriz 3D donde cada celda tiene presión
fluido = [[[{"presion": 0} for _ in range(N)] for _ in range(N)] for _ in range(N)]

# Generar una perturbación inicial (alta presión en el centro)
fluido[1][1][1]["presion"] = 100


def simular_paso(fluido):
    """
    Simula un paso de difusión de presión:
    - Cada celda toma el promedio de presión de sus vecinos
    - Se usa una copia para evitar sobrescribir datos en el mismo paso
    """
    nuevo = [[[celda.copy() for celda in fila] for fila in capa] for capa in fluido]

    for i in range(N):
        for j in range(N):
            for k in range(N):

                # Obtener vecinos de la celda actual
                vecinos = obtener_vecinos(i, j, k, N)

                # Promedio de presión de vecinos
                promedio = sum(fluido[x][y][z]["presion"] for x, y, z in vecinos) / len(vecinos)

                # Actualizar presión (modelo simple de difusión)
                nuevo[i][j][k]["presion"] = promedio

    return nuevo


# Ejecutar varios pasos de simulación
for paso in range(3):
    fluido = simular_paso(fluido)

    print(f"\nPaso {paso+1}")
    for i in range(N):
        imprimir_matriz(
            [[round(fluido[i][j][k]["presion"], 2) for k in range(N)] for j in range(N)],
            f"Capa {i}"
        )


# ============================================
# PROBLEMA 3: SUAVIZADO DE VOLUMEN 3D
# ============================================

print(f"\nProblema 3 Suavizado de volumen")

# Crear volumen con valores aleatorios (ruido)
volumen = [[[random.randint(0, 255) for _ in range(N)] for _ in range(N)] for _ in range(N)]

imprimir_matriz(volumen[0], "Volumen ORIGINAL (capa 0):")


def suavizar(vol):
    """
    Aplica un filtro de promedio:
    - Cada voxel se reemplaza por el promedio de sus vecinos
    - Reduce ruido (suavizado)
    """
    nuevo = [[[0]*N for _ in range(N)] for _ in range(N)]

    for i in range(N):
        for j in range(N):
            for k in range(N):

                # Incluir también la celda central en el promedio
                vecinos = obtener_vecinos(i, j, k, N, incluir_centro=True)

                # Promedio de valores vecinos
                nuevo[i][j][k] = int(sum(vol[x][y][z] for x, y, z in vecinos) / len(vecinos))

    return nuevo


volumen_suavizado = suavizar(volumen)

imprimir_matriz(volumen_suavizado[0], "Volumen SUAVIZADO (capa 0):")


# ============================================
# PROBLEMA 4: ANÁLISIS DE SENSORES
# ============================================

print(f"\nProblema 4 Analisis de sensores")

# Generar datos de temperatura aleatorios
datos = [[random.randint(20, 35) for _ in range(5)] for _ in range(5)]

# Funciones estadísticas
prom = lambda l: sum(l)/len(l)

def desv(l):
    """
    Calcula desviación estándar:
    mide qué tanto se dispersan los datos respecto al promedio
    """
    p = prom(l)
    return math.sqrt(sum((x - p)**2 for x in l)/len(l))


# Promedio por fila
prom_filas = [prom(f) for f in datos]

# Promedio por columna
prom_cols = [prom(col) for col in zip(*datos)]

print("\nPromedios filas:", prom_filas)
print("Promedios columnas:", prom_cols)


# ============================================
# PROBLEMA 5: TRANSFORMACIÓN (ROTACIÓN)
# ============================================

print(f"\nProblema 5 Transformacion/Rotacion")

def rotar_puntos(puntos, angulo):
    """
    Aplica rotación 2D usando matriz:
    
    [cos -sin]
    [sin  cos]
    """
    a = math.radians(angulo)
    cos_a, sin_a = math.cos(a), math.sin(a)

    return [
        [
            x*cos_a - y*sin_a,  # nueva coordenada X
            x*sin_a + y*cos_a   # nueva coordenada Y
        ]
        for x, y in puntos
    ]


puntos = [[1,1], [2,1], [2,2], [1,2]]

# Aplicar rotación de 45 grados
rotados = rotar_puntos(puntos, 45)

imprimir_matriz(puntos, "Original")
imprimir_matriz(rotados, "Rotados")