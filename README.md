[![Open in MATLAB Online](https://www.mathworks.com/images/responsive/global/open-in-matlab-online.svg)](https://matlab.mathworks.com/)

# Práctica 5.5 — Modelado y control del sistema musculoesquelético

Repositorio académico de **Modelado de Sistemas Fisiológicos (IBF-1020)**, Ingeniería Biomédica, Tecnológico Nacional de México / Instituto Tecnológico de Tijuana. Se estudia un modelo mecánico simplificado del músculo y su equivalente eléctrico, comparando un **individuo sano (control)** con un **caso simulado de atrofia muscular**. Posteriormente se aplica un controlador para reducir la diferencia entre ambas respuestas.

**Docente:** Dr. Paul Antonio Valle Trujillo  
**Asignatura:** Modelado de Sistemas Fisiológicos  
**Programa:** Ingeniería Biomédica  
**Institución:** Instituto Tecnológico de Tijuana — TecNM  
**Estudiante:** Osmar Ediel Armenta Medina  
**Número de control:** 23212178  
**Repositorio de la asignatura:** https://github.com/DrPaulValle/MSF-IBF1020

---

## Contenido

1. [Resumen](#resumen)
2. [Competencia y objetivos](#competencia-y-objetivos)
3. [Modelo mecánico](#modelo-mecánico)
4. [Analogía electromecánica](#analogía-electromecánica)
5. [Parámetros de simulación](#parámetros-de-simulación)
6. [Formulación matemática](#formulación-matemática)
7. [Análisis de estabilidad y respuesta](#análisis-de-estabilidad-y-respuesta)
8. [Implementación en MATLAB y Simulink](#implementación-en-matlab-y-simulink)
9. [Controlador PID](#controlador-pid)
10. [Implementación en Python](#implementación-en-python)
11. [Resultados y comparación](#resultados-y-comparación)
12. [Diagrama biológico](#diagrama-biológico)
13. [Estructura del repositorio](#estructura-del-repositorio)
14. [Conclusiones](#conclusiones)
15. [Referencias](#referencias)

---

## Resumen

La práctica analiza las propiedades **viscoelásticas** del sistema musculoesquelético mediante un modelo con un elemento contráctil, dos elementos elásticos y un amortiguador. A través de la analogía fuerza–voltaje se construye un circuito eléctrico equivalente, a partir del cual se estudian las ecuaciones dinámicas y la respuesta temporal. Se comparan dos condiciones: un individuo sano y un caso de atrofia muscular simulado mediante el aumento de la resistencia equivalente. Finalmente, se utiliza un controlador PID para aproximar la respuesta del caso a la referencia sana y se contrastan simulaciones en MATLAB/Simulink, Simscape Electrical y Python.

**Palabras clave:** sistema musculoesquelético; atrofia muscular; analogía electromecánica; fuerza–voltaje; viscoelasticidad; controlador PID; MATLAB; Simulink; Simscape Electrical; Python; modelado fisiológico.

## Competencia y objetivos

**Competencia:** modelar sistemas fisiológicos mediante analogías físicas, ecuaciones diferenciales y funciones de transferencia, y aplicar estrategias de control clásico para estudiar su comportamiento dinámico.

**Objetivo general:** comparar las respuestas de un modelo musculoesquelético sano y otro con atrofia muscular simulada, e implementar un controlador que reduzca la diferencia entre ambos.

**Objetivos específicos:** identificar los componentes del modelo; construir su equivalente eléctrico; obtener las ecuaciones y funciones de transferencia; analizar error, polos y estabilidad; comparar respuestas al impulso; sintonizar un controlador; y verificar los resultados mediante MATLAB y Python.

## Modelo mecánico

El modelo de la **Figura 5.3 del syllabus** representa un compartimento musculoesquelético simplificado mediante:

| Elemento | Interpretación |
|---|---|
| $F_0(t)$ | Fuerza desarrollada por el elemento contráctil activo |
| $F(t)$ | Fuerza transmitida por el sistema |
| $R$ | Amortiguación viscosa del tejido |
| $C_p$ | Compliancia del elemento elástico paralelo |
| $C_s$ | Compliancia del elemento elástico en serie |
| $x(t)$ | Desplazamiento del elemento paralelo |
| $x_1(t)$ | Desplazamiento del elemento elástico en serie |

La relación de fuerzas indicada en el instructivo es:

$$F_0(t)=\alpha F(t),\qquad 0<\alpha<1.$$

El desplazamiento del amortiguador es $x(t)-x_1(t)$, por lo que su velocidad relativa se expresa como:

$$\frac{d}{dt}[x(t)-x_1(t)].$$

La variación de las propiedades mecánicas modifica la deformación y la respuesta dinámica del sistema.

## Analogía electromecánica

Se emplea la analogía **fuerza–voltaje**, con las siguientes correspondencias:

| Magnitud mecánica | Magnitud eléctrica |
|---|---|
| Fuerza $F(t)$ | Voltaje $V(t)$ |
| Velocidad $\dot{x}(t)$ | Corriente $I(t)$ |
| Desplazamiento $x(t)$ | Carga $q(t)$ |
| Amortiguador | Resistencia $R$ |
| Compliancia mecánica | Capacitancia $C$ |
| Masa (si está presente) | Inductancia $L$ |

**Importante:** la topología no se conserva necesariamente: elementos mecánicos en paralelo pueden corresponder a elementos eléctricos en serie, y viceversa. Deben identificarse las referencias mecánicas y los nodos eléctricos antes de construir el circuito.

## Parámetros de simulación

Valores especificados en la página 89 del syllabus:

| Parámetro | Control (sano) | Caso (atrofia simulada) |
|---|---:|---:|
| $F(t)$ | $1\,\mathrm{V}$ | $1\,\mathrm{V}$ |
| $\alpha$ | $0.25$ | $0.25$ |
| $C_s$ | $10\,\mu\mathrm{F}$ | $10\,\mu\mathrm{F}$ |
| $C_p$ | $100\,\mu\mathrm{F}$ | $100\,\mu\mathrm{F}$ |
| $R$ | $100\,\Omega$ | $10\,\mathrm{k}\Omega$ |

La modificación principal es el aumento de $R$ de **100 Ω a 10 kΩ**, es decir, un factor de **100**. Este cambio se utiliza como representación académica de una alteración de la componente viscosa, no como un diagnóstico clínico.

## Formulación matemática

Se aplican las relaciones constitutivas de los elementos y las ecuaciones de equilibrio mecánico. En el equivalente eléctrico pueden utilizarse las relaciones:

$$V_R(t)=RI(t),\qquad I_C(t)=C\frac{dV_C(t)}{dt},\qquad q(t)=\int I(t)\,dt.$$

Con condiciones iniciales nulas se aplica la transformada de Laplace para obtener la relación entre fuerza y desplazamiento:

$$\boxed{G(s)=\frac{X(s)}{F(s)}}.$$

Deben calcularse por separado $G_{control}(s)$ y $G_{caso}(s)$ a partir de la **topología del circuito efectivamente construido**. El syllabus no proporciona una expresión algebraica única ya desarrollada para estas funciones; por ello, los coeficientes numéricos se deben verificar con las ecuaciones y conexiones del modelo Simulink antes de incorporarlos al reporte.

## Análisis de estabilidad y respuesta

Se calculan los polos de ambas funciones de transferencia, se representan en el plano complejo y se analiza su estabilidad. Asimismo, se evalúa el error en estado estacionario ante una entrada apropiada y se compara el efecto del aumento de resistencia sobre la respuesta transitoria.

La práctica solicita una **respuesta al impulso unitario** para:

$$\boxed{0\le t\le 10\ \mathrm{s}}.$$

Se comparan la amplitud, la velocidad de respuesta, el amortiguamiento y la diferencia temporal entre el individuo sano y el caso simulado.

## Implementación en MATLAB y Simulink

Se construyen tres representaciones del control y del caso:

1. **Modelo matemático:** ecuaciones del sistema implementadas con bloques de Simulink.
2. **Función de transferencia:** bloque `Transfer Fcn` con los coeficientes obtenidos analíticamente.
3. **Circuito eléctrico equivalente:** resistencias, capacitancias y fuentes correspondientes en Simscape Electrical.

Las tres implementaciones deben simularse bajo las mismas condiciones iniciales y parámetros para verificar la concordancia de sus respuestas.

En el cuaderno computacional de MATLAB se ejecutan los modelos y se almacenan las señales de control, caso sin controlador y caso controlado. Las gráficas deben identificar variables, unidades y leyendas y exportarse en PDF.

## Controlador PID

Se utiliza la respuesta del individuo sano como referencia para el caso de atrofia muscular. La señal de error indicada por el syllabus es:

$$\boxed{e(t)=x_{control}(t)-x_{caso}(t)}.$$

La ley de control ideal es:

$$u(t)=k_Pe(t)+k_I\int_0^t e(\tau)\,d\tau+k_D\frac{de(t)}{dt}.$$

En Simulink se implementa el bloque `PID Controller` y se utiliza **Tune** para ajustar las ganancias, buscando estabilidad y una menor diferencia entre las respuestas.

### Ganancias registradas en la simulación del estudiante

| Ganancia | Valor |
|---|---:|
| $k_P$ | $0.02149$ |
| $k_I$ | $3714.6075$ |
| $k_D$ | No especificada |

Estos valores corresponden a los datos compartidos de la simulación del estudiante. Deben verificarse en la configuración final del bloque antes de reproducir el resultado; no se presupone una ganancia derivativa igual a cero.

Se comparan tres respuestas al impulso:

- $x_{control}(t)$: individuo sano.
- $x_{caso}(t)$: caso sin controlador.
- $x_{PID}(t)$: caso con controlador.

El objetivo es reducir la diferencia respecto a la referencia sana sin perder estabilidad.

## Implementación en Python

En **Visual Studio Code** se reproducen las funciones de transferencia del control y del caso. Se utiliza el mismo intervalo temporal y las mismas condiciones de MATLAB para obtener las respuestas al impulso. Después se incorpora el controlador con las ganancias verificadas en Simulink y se genera la comparación entre las tres respuestas.

Las gráficas de Python se contrastan con las de MATLAB/Simulink para detectar diferencias debidas a parámetros, condiciones iniciales, discretización o configuración del controlador.

## Resultados y comparación

| Condición | Qué se debe mostrar | Evidencia |
|---|---|---|
| Control | Respuesta al impulso del individuo sano | Gráfica MATLAB/Python |
| Caso | Respuesta al impulso con $R=10\,\mathrm{k}\Omega$ | Gráfica MATLAB/Python |
| Caso controlado | Respuesta con el controlador sintonizado | Gráfica MATLAB/Python |
| Verificación cruzada | Coincidencia entre ecuaciones, transferencia y circuito | Capturas Simulink/Simscape |

**Interpretación:** el incremento de $R$ modifica la dinámica del modelo y genera diferencias respecto al control. La retroalimentación busca reducir dichas diferencias mediante la acción del controlador. La magnitud de la mejora y las características temporales específicas deben respaldarse con las gráficas obtenidas; no se reportan aquí resultados numéricos que no se hayan verificado.

## Diagrama biológico

El instructivo solicita elaborar en **BioRender** un diagrama que identifique el elemento contráctil muscular, estructuras elásticas musculares, tendón, desplazamiento, fuerza generada y comportamiento viscoso y elástico. Cada elemento debe relacionarse con su símbolo mecánico y su equivalente eléctrico.

Se recomienda presentar el músculo y tendón con etiquetas para $F_0(t)$, $F(t)$, $x(t)$, $C_p$, $C_s$ y $R$, distinguiendo el caso sano del caso simulado de atrofia muscular.

## Estructura del repositorio

Organización sugerida (ajustar a los nombres reales de los archivos):

```text
.
├── README.md
├── CITATION.cff
├── matlab/
│   ├── practica_5_5.mlx
│   └── sistema.slx
├── python/
│   └── musculoesqueletico.py
├── figuras/
│   ├── respuesta_matlab.pdf
│   ├── respuesta_python.pdf
│   ├── circuito_equivalente.png
│   └── diagrama_biologico.png
└── evidencias/
    ├── modelo_simulink.png
    ├── modelo_simscape.png
    └── controlador_pid.png
```

Los nombres son ejemplos; solo deben enlazarse como archivos existentes una vez incorporados al repositorio.

## Conclusiones

El modelado musculoesquelético permite relacionar las propiedades elásticas y viscosas de los tejidos con un sistema eléctrico equivalente y analizar su respuesta dinámica. La comparación entre el individuo sano y el caso simulado de atrofia muscular muestra cómo una variación de la resistencia modifica el comportamiento del modelo. El controlador PID se incorpora para intentar reducir la diferencia entre ambas respuestas, mientras que MATLAB, Simulink, Simscape Electrical y Python permiten verificar la consistencia de las representaciones. La eficacia cuantitativa del controlador deberá confirmarse con los resultados de simulación.

> **Alcance:** esta práctica es exclusivamente académica y *in silico*. El controlador simulado no constituye un tratamiento de la atrofia muscular.

## Referencias

1. M. C. Khoo, *Physiological Control Systems: Analysis, Simulation, and Estimation*, 2nd ed., IEEE Press, 2018.
2. F. C. Hoppensteadt y C. S. Peskin, *Modeling and Simulation in Medicine and the Life Sciences*, Springer.
3. J. E. Hall, *Guyton and Hall Textbook of Medical Physiology*, 14th ed., Elsevier, 2021.
4. K. Ogata, *Ingeniería de Control Moderna*, 5.ª ed., Pearson Educación, 2010.
5. N. S. Nise, *Control Systems Engineering*, 8th ed., Wiley, 2020.
6. P. A. Valle Trujillo, *Syllabus para Modelado de Sistemas Fisiológicos*, Instituto Tecnológico de Tijuana, 2026, sección 5.5, pp. 87–95.
7. Tecnológico Nacional de México, *Programa de estudio de Modelado de Sistemas Fisiológicos*, IBF-1020.
