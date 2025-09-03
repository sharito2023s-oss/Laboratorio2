## 📚 Librerías de Datos

###  <img src="https://pandas.pydata.org/static/img/pandas.svg" width="150">

Biblioteca fundamental para manipulación y análisis de datos en Python

- Estructuras de datos DataFrame y Series

- Herramientas para lectura/escritura de múltiples formatos

- Operaciones de limpieza, transformación y agregación de datos

- Integración con otras bibliotecas científicas


### <img src="https://geopandas.org/en/stable/_images/geopandas_icon.png" width="100"> GeoPandas

Extensión de pandas para datos geoespaciales

- Operaciones geométricas espaciales

- Integración con shapely y Fiona

- Visualización de mapas

### <img src="https://networkx.org/_static/networkx_logo.svg" width="150">

Biblioteca para creación, manipulación y estudio de grafos

- Algoritmos de grafos

- Estructuras de datos para redes

- Visualización básica

### 🦉 Ibis

Framework de expresiones para big data

- Sintaxis tipo pandas para backends distribuidos

- Soporte para múltiples motores (BigQuery, Spark, etc.)

- Ejecución perezosa (lazy evaluation)

### 🦆 DuckDB

Base de datos analytical in-process

- SQL para análisis de datos

- Alta performance en consultas analíticas

- Integración directa con pandas

---


## 🎨 Librerías de Visualización

### 📊 matplotlib

Biblioteca de visualización fundamental en Python

- Gráficos 2D de alta calidad

- Altamente personalizable

- Base para muchas otras bibliotecas

### 🌐 Bokeh

Visualizaciones interactivas para navegadores web

- Gráficos interactivos

- Aplicaciones web dashboard

- Streaming de datos

### <img src="https://holoviews.org/_static/logo.png" width="40"> HoloViews

Visualización declarativa de datos

- Sintaxis declarativa

- Anotaciones de datos ricas

- Backends múltiples (Bokeh, matplotlib)


### <img src="https://streamlit.io/images/brand/streamlit-logo-primary-colormark-darktext.png" width="150">

Framework para aplicaciones web de data science

- Creación rápida de dashboards

- Scripts Python puros

- Interactividad nativa

## 🧠 Modelo BDI para Toma de Decisiones en Planificación de Trayectorias

## 🤖 Agente Inteligente

Un agente inteligente es un sistema autónomo capaz de percibir su entorno a través de sensores, procesar esta información, y actuar sobre el medio ambiente mediante actuadores para lograr objetivos específicos.

Características principales:

- Autonomía: Opera sin intervención humana directa

- Reactividad: Responde a cambios en su entorno

- Proactividad: Toma iniciativas para alcanzar metas

- Racionalidad: Selecciona acciones que maximizan su medida de desempeño

Ejemplos de aplicaciones:

- Agentes de software para búsqueda de información

- Robots autónomos

- Sistemas de recomendación

- Asistentes virtuales inteligentes

## ⚡ Campo de Potencial Artificial

Un campo de potencial artificial es una técnica de planificación de caminos que utiliza conceptos de campos electromagnéticos para guiar un agente hacia su objetivo mientras evita obstáculos.

Componentes principales:

##### 🧲 Campo de Atracción


Python
# Ejemplo conceptual de campo atractivo
F_attractive = -k * (q - q_goal)


- Atrae el agente hacia el objetivo (q_goal)

- La fuerza aumenta con la distancia al objetivo

- Parámetro k controla la intensidad de atracción

##### 🚫 Campo de Repulsión

Python
# Ejemplo conceptual de campo repulsivo
if distancia(q, obstáculo) < d0:
    F_repulsive = η * (1/distancia(q, obstáculo) - 1/d0) * (1/distancia(q, obstáculo)^2)
else:
    F_repulsive = 0


- Aleja el agente de obstáculos

- Solo actúa dentro de una distancia umbral (d0)

- Parámetro η controla la intensidad de repulsión

#### 🎯 Campo Resultante

Python
F_total = F_atractivo + Σ F_repulsivo

- Superposición de todos los campos

- El agente sigue la dirección del gradiente negativo

Ventajas:

- Cálculos computacionalmente eficientes

- Trayectorias suaves y naturales

- Adaptabilidad a entornos dinámicos

Desventajas:

- Riesgo de mínimos locales (atrapamiento)

- Dificultad para elegir parámetros óptimos

- Limitaciones en entornos muy complejos

## 🎯 Algoritmo BDI (Belief-Desire-Intention)

El modelo BDI (Creencias-Deseos-Intenciones) es una arquitectura de agentes inteligentes basada en actitudes proposicionales que simula procesos de razonamiento humano.

Componentes fundamentales:

##### 💭 Creencias (Beliefs)

Python
class Belief:
    def __init__(self, knowledge, perception_data):
        self.world_state = self.process_perception(perception_data)
        self.self_state = self.update_self_knowledge(knowledge)


- Representan el conocimiento del agente sobre su entorno

- Se actualizan constantemente mediante percepción

- Incluyen información sobre obstáculos, objetivos y estado propio

#### ❤️ Deseos (Desires)

Python
class Desire:
    def __init__(self, goals, preferences):
        self.goal_set = self.prioritize_goals(goals, preferences)
        self.active_desires = self.select_feasible_desires()


- Estados objetivos que el agente quiere alcanzar

- Pueden ser conflictivos (requieren mecanismos de resolución)

- Se priorizan según preferencias y restricciones

##### 🎯 Intenciones (Intentions)

Python
class Intention:
    def __init__(self, selected_desire, beliefs):
        self.current_goal = selected_desire
        self.plan = self.generate_plan(beliefs, selected_desire)
        self.commitment_level = self.calculate_commitment()


- Deseos seleccionados a los que el agente se compromete

- Guían la planificación y ejecución de acciones

- Implican compromiso temporal y recursos

Ciclo de razonamiento BDI:

1. Percepción: Actualizar creencias con nueva información sensorial

2. Opciones: Generar deseos basados en creencias actuales

3. Filtro: Seleccionar intenciones de entre los deseos posibles

4. Ejecución: Realizar acciones para cumplir las intenciones

5. Retroalimentación: Evaluar resultados y ajustar comportamientos

#### Aplicación en planificación de trayectorias:

Python
# Pseudocódigo simplificado de agente BDI para navegación
def bdi_navigation_agent():
    beliefs = initialize_beliefs()
    desires = generate_desires(beliefs)
    intentions = filter_intentions(desires, beliefs)
    
    while not goal_achieved():
        plan = generate_path(intentions, beliefs)
        execute_movement(plan)
        
        # Actualización continua
        beliefs.update(perceive_environment())
        desires = reconsider_desires(beliefs)
        
        if should_reconsider_intentions(beliefs, intentions):
            intentions = filter_intentions(desires, beliefs)


Ventajas del enfoque BDI:

- Flexibilidad: Adaptación a cambios en el entorno

- Modularidad: Separación clara de componentes cognitivos

- Explicabilidad: Comportamiento comprensible y predecible

- Eficiencia: Razonamiento dirigido por metas

Retos de implementación:

- Representación formal de creencias, deseos e intenciones

- Mecanismos de conflicto entre metas

- Niveles adecuados de compromiso/reconsideración

- Integración con sistemas de planificación tradicionales

## 🔄 Integración en Planificación de Trayectorias

La tesis propone combinar campos potenciales con arquitectura BDI para crear un sistema de navegación más robusto y inteligente:

- Creencias: Modelan el campo potencial y estado del entorno

- Deseos: Incluyen llegar al objetivo y mantener seguridad

- Intenciones: Deciden entre comportamientos reactivos y deliberativos
