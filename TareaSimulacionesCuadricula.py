import random
import math
import matplotlib.pyplot as plt
import numpy as np

# ============================================
# FUNCIONES GENERALES
# ============================================

def imprimir_matriz(matriz, titulo=""):
    """Imprime una matriz (lista de listas) fila por fila."""
    print(f"\n{titulo}")
    for fila in matriz:
        print(fila)

def obtener_vecinos(x, y, z, N, incluir_centro=False):
    """Devuelve las coordenadas vecinas de una celda (x,y,z)"""
    vecinos = [
        (x+dx, y+dy, z+dz)
        for dx in [-1, 0, 1]
        for dy in [-1, 0, 1]
        for dz in [-1, 0, 1]
        if (incluir_centro or (dx, dy, dz) != (0, 0, 0))
    ]
    return [(i, j, k) for i, j, k in vecinos if 0 <= i < N and 0 <= j < N and 0 <= k < N]


# ============================================
# PROBLEMA 1: ANÁLISIS DE FUERZAS EN UNA ESTRUCTURA
# ============================================

print("="*50)
print("Problema 1: Análisis de Fuerzas en una Estructura")
print("="*50)

# Matriz 3x3 de fuerzas aplicadas en cada nodo (en kN)
# Fuerzas en dirección vertical (positivo hacia arriba)
fuerzas_aplicadas = [
    [10, -5, 3],
    [-2, 7, -1],
    [4, -6, 8]
]

imprimir_matriz(fuerzas_aplicadas, "Fuerzas aplicadas en cada nodo (kN):")

# Calcular reacciones usando ecuaciones de estática
# Para una estructura simplemente apoyada con apoyos en las esquinas

# Coordenadas de los nodos (asumiendo espaciado de 1m)
coordenadas = {
    (0,0): (0, 0),   # (x, y)
    (0,1): (0, 1),
    (0,2): (0, 2),
    (1,0): (1, 0),
    (1,1): (1, 1),
    (1,2): (1, 2),
    (2,0): (2, 0),
    (2,1): (2, 1),
    (2,2): (2, 2)
}

# Apoyos en las cuatro esquinas
apoyos = [(0,0), (0,2), (2,0), (2,2)]

# Calcular fuerza total y momentos
fuerza_total = sum(sum(fila) for fila in fuerzas_aplicadas)

# Calcular momento respecto al eje X (suma de fuerzas * distancia en Y)
momento_x = 0
# Calcular momento respecto al eje Y (suma de fuerzas * distancia en X)
momento_y = 0

for i in range(3):
    for j in range(3):
        fuerza = fuerzas_aplicadas[i][j]
        x, y = coordenadas[(i,j)]
        momento_x += fuerza * y  # Momento alrededor del eje X
        momento_y += fuerza * x  # Momento alrededor del eje Y

print(f"\nFuerza total aplicada: {fuerza_total:.2f} kN")
print(f"Momento total alrededor de X: {momento_x:.2f} kN·m")
print(f"Momento total alrededor de Y: {momento_y:.2f} kN·m")

# Resolver sistema de ecuaciones para encontrar reacciones en los apoyos
# Ecuaciones:
# ΣF = 0: R00 + R02 + R20 + R22 = fuerza_total
# ΣMx = 0: 0*R00 + 2*R02 + 0*R20 + 2*R22 = momento_x
# ΣMy = 0: 0*R00 + 0*R02 + 2*R20 + 2*R22 = momento_y

# Resolver usando matriz de coeficientes
# [1, 1, 1, 1]   [R00]   [fuerza_total]
# [0, 2, 0, 2] * [R02] = [momento_x]
# [0, 0, 2, 2]   [R20]   [momento_y]
#                [R22]

A = np.array([
    [1, 1, 1, 1],
    [0, 2, 0, 2],
    [0, 0, 2, 2]
])

B = np.array([fuerza_total, momento_x, momento_y])

# Resolver usando mínimos cuadrados (sistema sobredeterminado)
reacciones_nodos = np.linalg.lstsq(A, B, rcond=None)[0]

# Crear matriz de reacciones
reacciones = [[0]*3 for _ in range(3)]
reacciones[0][0] = reacciones_nodos[0]
reacciones[0][2] = reacciones_nodos[1]
reacciones[2][0] = reacciones_nodos[2]
reacciones[2][2] = reacciones_nodos[3]

imprimir_matriz(reacciones, "\nReacciones en los apoyos (kN):")

# Verificar equilibrio
print("\n--- Verificación de equilibrio ---")
print(f"Suma de reacciones: {sum(reacciones_nodos):.2f} kN")
print(f"Equilibrio vertical: {'✓' if abs(sum(reacciones_nodos) - fuerza_total) < 0.01 else '✗'}")


# ============================================
# PROBLEMA 2: SIMULACIÓN DE FLUIDO EN UNA CUADRÍCULA 3D
# ============================================

print("\n" + "="*50)
print("Problema 2: Simulación de Fluido en una Cuadrícula 3D")
print("="*50)

N = 3

# Cada celda contiene presión, temperatura y velocidad
fluido = [[[{
    "presion": 0,
    "temperatura": 20.0,  # Temperatura inicial en °C
    "velocidad": [0.0, 0.0, 0.0]  # Velocidad en x, y, z
} for _ in range(N)] for _ in range(N)] for _ in range(N)]

# Perturbación inicial: alta presión en el centro
fluido[1][1][1]["presion"] = 100
fluido[1][1][1]["temperatura"] = 80  # Punto caliente
fluido[1][1][1]["velocidad"] = [10, 10, 10]  # Velocidad inicial

# Parámetros de simulación
c = 343  # Velocidad del sonido en el fluido (m/s)
dt = 0.01  # Paso de tiempo (s)
dx = 1.0  # Espaciado entre celdas (m)

def simular_onda_presion(fluido, c, dt, dx):
    """Simula propagación de ondas de presión usando ecuación de onda"""
    nuevo = [[[celda.copy() for celda in fila] for fila in capa] for capa in fluido]
    
    for i in range(N):
        for j in range(N):
            for k in range(N):
                vecinos = obtener_vecinos(i, j, k, N)
                
                # Calcular laplaciano de presión (∇²p)
                laplaciano = 0
                for x, y, z in vecinos:
                    laplaciano += fluido[x][y][z]["presion"] - fluido[i][j][k]["presion"]
                
                # Ecuación de onda: ∂²p/∂t² = c²∇²p
                # Método simplificado: p_new = p + (c² * ∇²p * dt²) / (2*dx²)
                aceleracion_presion = (c**2 * laplaciano) / (dx**2)
                nuevo[i][j][k]["presion"] = fluido[i][j][k]["presion"] + aceleracion_presion * dt**2
                
                # Difusión de temperatura (ley de Fourier simplificada)
                diff_temp = sum(fluido[x][y][z]["temperatura"] for x,y,z in vecinos) / len(vecinos)
                nuevo[i][j][k]["temperatura"] = fluido[i][j][k]["temperatura"] + 0.1 * (diff_temp - fluido[i][j][k]["temperatura"])
                
                # Propagación de velocidad (simplificada)
                if i == 1 and j == 1 and k == 1:
                    nuevo[i][j][k]["velocidad"] = fluido[i][j][k]["velocidad"]
                else:
                    nuevo[i][j][k]["velocidad"] = [
                        sum(fluido[x][y][z]["velocidad"][0] for x,y,z in vecinos) / len(vecinos),
                        sum(fluido[x][y][z]["velocidad"][1] for x,y,z in vecinos) / len(vecinos),
                        sum(fluido[x][y][z]["velocidad"][2] for x,y,z in vecinos) / len(vecinos)
                    ]
    
    return nuevo

# Simular varios pasos
print("\nSimulando propagación de onda de presión...")
for paso in range(5):
    fluido = simular_onda_presion(fluido, c, dt, dx)
    if paso % 2 == 0:
        print(f"\nPaso {paso+1} - Presión en centro: {fluido[1][1][1]['presion']:.2f}")
        print(f"Temperatura en centro: {fluido[1][1][1]['temperatura']:.1f}°C")
        print(f"Velocidad en centro: {fluido[1][1][1]['velocidad']}")


# ============================================
# PROBLEMA 3: ANÁLISIS DE IMÁGENES MÉDICAS EN 3D
# ============================================

print("\n" + "="*50)
print("Problema 3: Análisis de Imágenes Médicas en 3D")
print("="*50)

# Crear volumen 3D con ruido (simulando imágenes médicas)
volumen = [[[random.randint(0, 255) for _ in range(8)] for _ in range(8)] for _ in range(5)]  # 5 capas de 8x8

def suavizar_capa(capa):
    """Aplica filtro de promedio a una capa 2D"""
    nueva_capa = [[0]*len(capa[0]) for _ in range(len(capa))]
    for i in range(len(capa)):
        for j in range(len(capa[0])):
            # Obtener vecinos en 2D (incluyendo la celda actual)
            vecinos = []
            for di in [-1, 0, 1]:
                for dj in [-1, 0, 1]:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < len(capa) and 0 <= nj < len(capa[0]):
                        vecinos.append(capa[ni][nj])
            nueva_capa[i][j] = int(sum(vecinos) / len(vecinos))
    return nueva_capa

def suavizar_volumen(volumen):
    """Suaviza cada capa del volumen independientemente"""
    return [suavizar_capa(capa) for capa in volumen]

# Visualizar mejora
def visualizar_capa(capa_original, capa_suavizada, titulo="Capa"):
    """Visualiza una capa antes y después del suavizado"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
    
    im1 = ax1.imshow(capa_original, cmap='gray', vmin=0, vmax=255)
    ax1.set_title(f'{titulo} - Original')
    ax1.axis('off')
    
    im2 = ax2.imshow(capa_suavizada, cmap='gray', vmin=0, vmax=255)
    ax2.set_title(f'{titulo} - Suavizada')
    ax2.axis('off')
    
    plt.colorbar(im1, ax=ax1, fraction=0.046)
    plt.colorbar(im2, ax=ax2, fraction=0.046)
    plt.tight_layout()
    plt.show()

print("\nMostrando visualización de la mejora en las imágenes...")
volumen_suavizado = suavizar_volumen(volumen)

# Visualizar capa 0 (la primera)
visualizar_capa(volumen[0], volumen_suavizado[0], "Capa 0")

# Calcular métricas de mejora
ruido_original = np.std(volumen[0])
ruido_suavizado = np.std(volumen_suavizado[0])
print(f"\nRuido (desviación estándar) en capa 0:")
print(f"Original: {ruido_original:.2f}")
print(f"Suavizado: {ruido_suavizado:.2f}")
print(f"Reducción de ruido: {(1 - ruido_suavizado/ruido_original)*100:.1f}%")


# ============================================
# PROBLEMA 4: MANEJO DE DATOS EN UNA TABLA DE SENSORES
# ============================================

print("\n" + "="*50)
print("Problema 4: Manejo de Datos en una Tabla de Sensores")
print("="*50)

# Datos de temperatura de 5 sensores en 5 momentos (en °C)
datos_sensores = [[random.randint(20, 35) for _ in range(5)] for _ in range(5)]

print("\nDatos de temperatura (°C):")
imprimir_matriz(datos_sensores, "Matriz de sensores (filas=momentos, columnas=sensores):")

# Funciones estadísticas
def promedio(lista):
    return sum(lista) / len(lista)

def desviacion_std(lista):
    prom = promedio(lista)
    return math.sqrt(sum((x - prom)**2 for x in lista) / len(lista))

# Análisis por fila (momentos en el tiempo)
prom_filas = [promedio(fila) for fila in datos_sensores]
std_filas = [desviacion_std(fila) for fila in datos_sensores]

# Análisis por columna (sensores)
prom_columnas = [promedio([fila[i] for fila in datos_sensores]) for i in range(5)]
std_columnas = [desviacion_std([fila[i] for fila in datos_sensores]) for i in range(5)]

print("\n--- Análisis por momento en el tiempo (filas) ---")
for i, (prom, std) in enumerate(zip(prom_filas, std_filas)):
    print(f"Momento {i+1}: Media = {prom:.2f}°C, σ = {std:.2f}°C")

print("\n--- Análisis por sensor (columnas) ---")
for i, (prom, std) in enumerate(zip(prom_columnas, std_columnas)):
    print(f"Sensor {i+1}: Media = {prom:.2f}°C, σ = {std:.2f}°C")

# Visualización de resultados
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))

# Gráfico 1: Temperatura por sensor (boxplot)
datos_sensores_plot = [datos_sensores[i] for i in range(5)]
ax1.boxplot(datos_sensores_plot, labels=[f'S{i+1}' for i in range(5)])
ax1.set_title('Distribución de Temperatura por Sensor')
ax1.set_ylabel('Temperatura (°C)')
ax1.grid(True, alpha=0.3)

# Gráfico 2: Promedios por sensor
ax2.bar(range(5), prom_columnas, yerr=std_columnas, capsize=5, alpha=0.7)
ax2.set_title('Promedio de Temperatura por Sensor')
ax2.set_xlabel('Sensor')
ax2.set_ylabel('Temperatura (°C)')
ax2.set_xticks(range(5))
ax2.set_xticklabels([f'S{i+1}' for i in range(5)])
ax2.grid(True, alpha=0.3)

# Gráfico 3: Evolución temporal (todas las series)
for i in range(5):
    ax3.plot(range(5), [fila[i] for fila in datos_sensores], marker='o', label=f'Sensor {i+1}')
ax3.set_title('Evolución Temporal de Temperatura')
ax3.set_xlabel('Momento en el tiempo')
ax3.set_ylabel('Temperatura (°C)')
ax3.legend()
ax3.grid(True, alpha=0.3)

# Gráfico 4: Mapa de calor
im = ax4.imshow(datos_sensores, cmap='hot', aspect='auto', interpolation='nearest')
ax4.set_title('Mapa de Calor de Temperaturas')
ax4.set_xlabel('Sensor')
ax4.set_ylabel('Momento')
ax4.set_xticks(range(5))
ax4.set_xticklabels([f'S{i+1}' for i in range(5)])
ax4.set_yticks(range(5))
ax4.set_yticklabels([f'M{i+1}' for i in range(5)])
plt.colorbar(im, ax=ax4, label='Temperatura (°C)')

plt.tight_layout()
plt.show()

print("\n✓ Visualización completa generada")


# ============================================
# PROBLEMA 5: TRANSFORMACIÓN DE COORDENADAS
# ============================================

print("\n" + "="*50)
print("Problema 5: Transformación de Coordenadas en Sistema Cartesiano")
print("="*50)

# Puntos originales (cuadrado)
puntos = np.array([
    [1, 1],
    [2, 1],
    [2, 2],
    [1, 2],
    [1, 1]  # Cerramos el polígono
])

def rotar_puntos(puntos, angulo_grados):
    """Rota puntos alrededor del origen"""
    angulo_rad = math.radians(angulo_grados)
    cos_a, sin_a = math.cos(angulo_rad), math.sin(angulo_rad)
    matriz_rotacion = np.array([[cos_a, -sin_a], [sin_a, cos_a]])
    return puntos @ matriz_rotacion.T

def trasladar_puntos(puntos, dx, dy):
    """Traslada puntos"""
    return puntos + np.array([dx, dy])

def escalar_puntos(puntos, sx, sy):
    """Escala puntos"""
    return puntos * np.array([sx, sy])

# Aplicar transformaciones
puntos_rotados = rotar_puntos(puntos, 45)
puntos_trasladados = trasladar_puntos(puntos, 3, 2)
puntos_escalados = escalar_puntos(puntos, 1.5, 0.8)
puntos_complejos = escalar_puntos(rotar_puntos(trasladar_puntos(puntos, 1, 1), 30), 0.8, 1.2)

# Visualización
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))

# Gráfico 1: Rotación
ax1.plot(puntos[:, 0], puntos[:, 1], 'bo-', label='Original', linewidth=2, markersize=6)
ax1.plot(puntos_rotados[:, 0], puntos_rotados[:, 1], 'ro-', label='Rotado 45°', linewidth=2, markersize=6)
ax1.set_title('Rotación de 45°')
ax1.set_xlabel('X')
ax1.set_ylabel('Y')
ax1.grid(True, alpha=0.3)
ax1.legend()
ax1.axis('equal')

# Gráfico 2: Traslación
ax2.plot(puntos[:, 0], puntos[:, 1], 'bo-', label='Original', linewidth=2, markersize=6)
ax2.plot(puntos_trasladados[:, 0], puntos_trasladados[:, 1], 'go-', label='Trasladado (3,2)', linewidth=2, markersize=6)
ax2.set_title('Traslación')
ax2.set_xlabel('X')
ax2.set_ylabel('Y')
ax2.grid(True, alpha=0.3)
ax2.legend()
ax2.axis('equal')

# Gráfico 3: Escalamiento
ax3.plot(puntos[:, 0], puntos[:, 1], 'bo-', label='Original', linewidth=2, markersize=6)
ax3.plot(puntos_escalados[:, 0], puntos_escalados[:, 1], 'mo-', label='Escalado (1.5, 0.8)', linewidth=2, markersize=6)
ax3.set_title('Escalamiento')
ax3.set_xlabel('X')
ax3.set_ylabel('Y')
ax3.grid(True, alpha=0.3)
ax3.legend()
ax3.axis('equal')

# Gráfico 4: Transformación compuesta
ax4.plot(puntos[:, 0], puntos[:, 1], 'bo-', label='Original', linewidth=2, markersize=6)
ax4.plot(puntos_complejos[:, 0], puntos_complejos[:, 1], 'co-', label='Transformación compuesta', linewidth=2, markersize=6)
ax4.set_title('Transformación Compuesta\n(Traslación + Rotación + Escalamiento)')
ax4.set_xlabel('X')
ax4.set_ylabel('Y')
ax4.grid(True, alpha=0.3)
ax4.legend()
ax4.axis('equal')

plt.tight_layout()
plt.show()

print("\n✓ Visualización de todas las transformaciones completada")
print("\n" + "="*50)
print("RESUMEN FINAL: Todos los problemas han sido resueltos completamente")
print("="*50)
