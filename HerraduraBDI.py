import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from pathlib import Path
import math

# Configurar la ruta de guardado
ruta_graficas = Path.home() / "Documentos"
ruta_graficas.mkdir(exist_ok=True)

# Parámetros del campo de potencial
K_ATRACTIVO = 0.5
K_REPULSIVO = 3.0
RADIO_REPULSION = 2.5
PASO = 0.1
UMBRAL_CONVERGENCIA = 0.1

# Implementación del modelo BDI
class AgenteBDI:
    def _init_(self, posicion_inicial, objetivo, obstaculos):
        # Creencias (Beliefs)
        self.posicion = np.array(posicion_inicial, dtype=float)
        self.objetivo = np.array(objetivo, dtype=float)
        self.obstaculos = np.array(obstaculos, dtype=float)
        self.historial_posiciones = [self.posicion.copy()]
        self.historial_energia = []
        
        # Deseos (Desires)
        self.deseo_principal = "alcanzar_objetivo"
        self.deseos_secundarios = ["evitar_obstaculos", "optimizar_trayectoria"]
        
        # Intenciones (Intentions)
        self.intencion_actual = "seguir_campo_potencial"
        self.camino_previo = []
        self.estancado = False
        self.contador_estancamiento = 0
        
    def actualizar_creencias(self):
        # Calcular distancia al objetivo
        self.distancia_objetivo = np.linalg.norm(self.objetivo - self.posicion)
        
        # Calcular distancia mínima a obstáculos
        self.distancia_min_obstaculo = min([np.linalg.norm(obs - self.posicion) for obs in self.obstaculos])
        
        # Verificar si está estancado
        if len(self.historial_posiciones) > 10:
            ultimas_posiciones = self.historial_posiciones[-10:]
            desplazamiento = np.linalg.norm(ultimas_posiciones[-1] - ultimas_posiciones[0])
            if desplazamiento < 0.5:
                self.contador_estancamiento += 1
                if self.contador_estancamiento > 5:
                    self.estancado = True
            else:
                self.contador_estancamiento = 0
                self.estancado = False
    
    def deliberar(self):
        # Si está cerca del objetivo, terminar
        if self.distancia_objetivo < UMBRAL_CONVERGENCIA:
            self.intencion_actual = "terminar"
            return
        
        # Si está estancado, cambiar de estrategia
        if self.estancado:
            self.intencion_actual = "buscar_alternativa"
            return
        
        # Por defecto, seguir el campo potencial
        self.intencion_actual = "seguir_campo_potencial"
    
    def ejecutar(self):
        if self.intencion_actual == "terminar":
            return False  # Terminar ejecución
        
        elif self.intencion_actual == "seguir_campo_potencial":
            gradiente = self.calcular_gradiente()
            self.posicion -= gradiente * PASO
        
        elif self.intencion_actual == "buscar_alternativa":
            # Cuando está estancado, intentar moverse perpendicularmente al gradiente
            gradiente = self.calcular_gradiente()
            # Crear un vector perpendicular
            perpendicular = np.array([-gradiente[1], gradiente[0]])
            # Elegir dirección que aleje de obstáculos cercanos
            self.posicion += perpendicular * PASO * 2
            self.estancado = False
        
        # Guardar historial
        self.historial_posiciones.append(self.posicion.copy())
        energia = self.calcular_potencial()
        self.historial_energia.append(energia)
        
        return True
    
    def calcular_potencial(self):
        # Potencial de atracción (cuadrático cerca del objetivo)
        distancia = np.linalg.norm(self.objetivo - self.posicion)
        potencial_atractivo = 0.5 * K_ATRACTIVO * distancia**2
        
        # Potencial de repulsión de los obstáculos
        potencial_repulsivo = 0
        for obstaculo in self.obstaculos:
            distancia_obs = np.linalg.norm(self.posicion - obstaculo)
            if distancia_obs < RADIO_REPULSION:
                potencial_repulsivo += 0.5 * K_REPULSIVO * (1/distancia_obs - 1/RADIO_REPULSION)**2
        
        return potencial_atractivo + potencial_repulsivo
    
    def calcular_gradiente(self, epsilon=0.1):
        gradiente = np.zeros(2)
        for i in range(2):
            delta = np.zeros(2)
            delta[i] = epsilon
            potencial_pos = self.calcular_potencial_pos(self.posicion + delta)
            potencial_neg = self.calcular_potencial_pos(self.posicion - delta)
            gradiente[i] = (potencial_pos - potencial_neg) / (2 * epsilon)
        
        # Normalizar el gradiente
        norma = np.linalg.norm(gradiente)
        if norma > 0:
            gradiente /= norma
            
        return gradiente
    
    def calcular_potencial_pos(self, posicion):
        # Potencial de atracción
        distancia = np.linalg.norm(self.objetivo - posicion)
        potencial_atractivo = 0.5 * K_ATRACTIVO * distancia**2
        
        # Potencial de repulsión
        potencial_repulsivo = 0
        for obstaculo in self.obstaculos:
            distancia_obs = np.linalg.norm(posicion - obstaculo)
            if distancia_obs < RADIO_REPULSION:
                potencial_repulsivo += 0.5 * K_REPULSIVO * (1/distancia_obs - 1/RADIO_REPULSION)**2
        
        return potencial_atractivo + potencial_repulsivo

# Configuración del entorno
agente_posicion = np.array([1.0, 1.0])
objetivo = np.array([12.0, 12.0])

# Definición de la herradura
obstaculos = np.array([
    [2, 2], [2, 3], [2, 4], [2, 5], [2, 6], [2, 7], [2, 8], [2, 9], [2, 10], [10, 10],
    [10, 9], [10, 8], [10, 7], [10, 6], [10, 5], [10, 4], [10, 3], [10, 2],
    [9, 2], [9, 3], [9, 4], [9, 5], [9, 6], [9, 7], [9, 8], [9, 9],
    [3, 9], [3, 8], [3, 7], [3, 6], [3, 5], [3, 4], [3, 3], [3, 2],
    [4, 9], [5, 9], [6, 9], [7, 9], [8, 9], [3, 10], [4, 10], [5, 10], [6, 10],
    [7, 10], [8, 10], [9, 10]
])

# Crear agente BDI
agente = AgenteBDI(agente_posicion, objetivo, obstaculos)

# Configuración de la visualización
fig, (ax, ax2) = plt.subplots(1, 2, figsize=(14, 6))

def inicializar_visualizacion():
    ax.clear()
    ax.scatter(objetivo[0], objetivo[1], color='green', marker='x', s=200, label='Objetivo')
    ax.scatter(obstaculos[:, 0], obstaculos[:, 1], color='black', marker='s', s=50, label='Obstáculos')
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 13)
    ax.set_title('Trayectoria del Agente BDI')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.legend()
    ax.grid(True)
    
    ax2.clear()
    ax2.set_title('Evolución de la Energía Potencial')
    ax2.set_xlabel('Iteración')
    ax2.set_ylabel('Energía Potencial')
    ax2.grid(True)
    
    return ax, ax2

# Función de actualización para la animación
def update(frame):
    ax, ax2 = inicializar_visualizacion()
    
    # Ejecutar un paso del agente BDI
    continuar = agente.ejecutar()
    
    # Actualizar creencias y deliberar
    agente.actualizar_creencias()
    agente.deliberar()
    
    # Visualizar trayectoria
    historial = np.array(agente.historial_posiciones)
    ax.plot(historial[:, 0], historial[:, 1], 'b-', alpha=0.3)
    ax.scatter(agente.posicion[0], agente.posicion[1], color='red', s=100, label='Agente')
    
    # Visualizar energía potencial
    ax2.plot(agente.historial_energia, 'r-')
    ax2.set_xlim(0, max(100, len(agente.historial_energia)))
    
    if not continuar or frame >= 200:
        ani.event_source.stop()
        print("✅ El agente ha llegado al objetivo o alcanzado el máximo de iteraciones")
    
    return ax, ax2

# Crear animación
ani = FuncAnimation(fig, update, frames=200, interval=200, repeat=False)

# Guardar la animación
try:
    ruta_guardado = ruta_graficas / "animacion_bdi_herradura.gif"
    ani.save(ruta_guardado, writer='pillow', fps=5)
    print(f"✅ Animación guardada en: {ruta_guardado}")
except Exception as e:
    print(f"❌ Error al guardar la animación: {e}")

plt.tight_layout()
plt.show()

# Guardar imagen estática final
try:
    fig_final, ax_final = plt.subplots(figsize=(8, 8))
    ax_final.scatter(objetivo[0], objetivo[1], color='green', marker='x', s=200, label='Objetivo')
    ax_final.scatter(obstaculos[:, 0], obstaculos[:, 1], color='black', marker='s', s=50, label='Obstáculos')
    
    historial = np.array(agente.historial_posiciones)
    ax_final.plot(historial[:, 0], historial[:, 1], 'b-', alpha=0.7)
    ax_final.scatter(agente.posicion[0], agente.posicion[1], color='red', s=100, label='Agente')
    
    ax_final.set_xlim(0, 13)
    ax_final.set_ylim(0, 13)
    ax_final.set_title('Trayectoria Final del Agente BDI')
    ax_final.set_xlabel('X')
    ax_final.set_ylabel('Y')
    ax_final.legend()
    ax_final.grid(True)
    
    ruta_imagen = ruta_graficas / "trayectoria_final_bdi.png"
    plt.savefig(ruta_imagen, dpi=300, bbox_inches='tight')
    print(f"✅ Imagen final guardada en: {ruta_imagen}")
    plt.close(fig_final)
except Exception as e:
    print(f"❌ Error al guardar la imagen: {e}")