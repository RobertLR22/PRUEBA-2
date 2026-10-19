# "Adivina el Número"

> **Proyecto de diagnóstico y repaso**
> Léelo completo antes de escribir una sola línea de código.

---

## 0.1 Por qué existe esta estación

Esta estación no introduce ningún concepto nuevo. Su único propósito es **confirmar** que dominas las herramientas más básicas de Python antes de empezar a construir cosas más grandes.

Si haces este proyecto con soltura y sin ayuda, estás listo para la Estación 1. Si te cuesta, perfecto: mejor descubrirlo ahora que en la Estación 5.

**Duración esperada:** 1 a 2 días.

**Lo que NO vas a aprender aquí:** clases, `@dataclass`, excepciones personalizadas, `abc`, JSON, arquitectura por capas, Git con ramas. Nada de eso. Todo eso viene después, una estación a la vez.

**Lo que SÍ vas a repasar aquí:** variables, `while`, `input`, `if/elif/else`, validación de datos, funciones, `import` y `random`.

---

## 0.2 Requisitos previos

Antes de empezar, verifica que tengas esto:

- Python 3.10 o superior instalado (`python --version` en terminal).
- Saber ejecutar un archivo `.py` desde terminal (`python nombre_archivo.py`).
- Saber qué es una variable, una función, un `if`, un `while`, un `input`.
- Un editor de código cualquiera (VS Code, PyCharm, Sublime, incluso Notepad++).

Si algo de esta lista no lo tienes claro, avísame **antes** de empezar.

---

## 0.3 Especificación del Proyecto

### 0.3.1 Descripción general

Vas a construir un juego de consola llamado **"Adivina el número"** en **un solo archivo** de Python. El programa piensa un número secreto, y el jugador debe adivinarlo en una cantidad limitada de intentos.

### 0.3.2 Reglas del juego (contrato funcional)

1. Al iniciar, el programa genera un número entero aleatorio entre **1 y 100**.
2. El jugador tiene exactamente **7 intentos** para adivinarlo.
3. En cada turno, el programa muestra `Intento X/7:` y espera a que el jugador escriba un número.
4. Después de cada intento, el programa responde **una** de estas tres opciones:
   - `Muy bajo.` si el número del jugador es menor que el secreto.
   - `Bajo`
   - `Muy alto.` si el número del jugador es mayor que el secreto.
   - `Alto`
   - `¡Correcto!` si acertó.
5. Si el jugador acierta **antes o en el intento 7**, el programa muestra un mensaje de victoria indicando **en cuántos intentos** lo logró, y termina.
6. Si el jugador **agota los 7 intentos sin acertar**, el programa revela el número secreto y termina.
7. Si el jugador escribe algo que **no es un número** o que está **fuera del rango 1–100**, el programa muestra un mensaje de error, **no consume el intento**, y vuelve a pedir el número.

### 0.3.3 Requisitos técnicos obligatorios

- [ ] Todo el código en un único archivo llamado `adivina.py`.
- [ ] Al menos **dos funciones** definidas por ti (por ejemplo, una función que gestione el flujo principal y otra que pida/valide el intento; tú decides cómo dividirlo).
- [ ] Al menos **tres constantes** definidas al inicio del archivo.
- [ ] El número secreto se genera con `random.randint(MINIMO, MAXIMO)`.
- [ ] El flujo del juego se controla con un bucle `while`.
- [ ] La validación de entrada se hace **sin** `try/except`. Usa `.strip()` y `.isdigit()` (ver sección 0.5.5).
- [ ] La salida usa `f-strings` para interpolar variables (por ejemplo, `f"Intento {n}/7:"`).

### 0.3.4 Anti-requisitos (lo que NO debes usar)

Estos conceptos **todavía no** te toca usarlos:

- No `try/except`.
- No clases (`class`).
- No `@dataclass`.
- No `abc`, `@abstractmethod`.
- No `json`, `open`, ni persistencia en archivos.
- No múltiples archivos `.py`.
- No `import` distinto de `random`.
- No `pytest` ni pruebas automatizadas.
- No Git con ramas ni Pull Requests (ver sección 0.8).

### 0.3.5 Ejemplo de partida (formato de salida esperado)

**Caso victoria:**

```
Bienvenido a Adivina el número.
Piensa un número entre 1 y 100.
Tienes 7 intentos para adivinarlo.

Intento 1/7: 50
Muy alto.

Intento 2/7: 25
Muy bajo.

Intento 3/7: 37
¡Correcto! Lo lograste en 3 intentos.
```

**Caso derrota:**

```
Bienvenido a Adivina el número.
Piensa un número entre 1 y 100.
Tienes 7 intentos para adivinarlo.

Intento 1/7: 50
Muy alto.

Intento 2/7: 25
Muy bajo.

... (5 intentos más, todos incorrectos) ...

Intento 7/7: 80
Muy bajo.

Se agotaron los intentos. El número secreto era 42.
```

**Caso entrada inválida:**

```
Intento 3/7: abc
Error: debes escribir un número entero. Intenta de nuevo.

Intento 3/7: 0
Error: el número debe estar entre 1 y 100.

Intento 3/7: 101
Error: el número debe estar entre 1 y 100.

Intento 3/7: 42
¡Correcto! Lo lograste en 3 intentos.
```

Observa con detalle: en el último ejemplo, el intento número 3 se repitió tres veces porque las entradas inválidas **no consumen intento**. Esto es deliberado y es parte del contrato.

---

## 0.4 Criterios de Aceptación

Antes de entregar, tu proyecto debe cumplir **todos** estos puntos:

- [ ] `adivina.py` existe y se ejecuta sin errores con `python adivina.py`.
- [ ] El juego tiene las 7 reglas de la sección 0.3.2 implementadas correctamente.
- [ ] Las tres constantes (`MINIMO`, `MAXIMO`, `INTENTOS_MAXIMOS`) están definidas al inicio.
- [ ] Hay al menos dos funciones con nombres descriptivos.
- [ ] La entrada inválida no rompe el programa ni consume intentos.
- [ ] El contador de intentos en el mensaje `Intento X/7:` es siempre correcto.
- [ ] No se usa `try/except`, ni clases, ni `json`, ni nada de los anti-requisitos.
- [ ] Pasa las pruebas manuales de la sección 0.7 sin fallar.

---

## 0.5 Conceptos a Repasar

En esta sección repasamos cada concepto que necesitas. Cada ejemplo viene de un **dominio completamente distinto** al de tu juego. La idea es que entiendas **qué hace** el concepto, pero que no puedas copiar y renombrar el código para pegarlo en tu proyecto.

---

### 0.5.1 Variables

**Qué es:** una variable es una caja etiquetada donde guardas un valor para usarlo después. El nombre describe su contenido.

**Ejemplo (dominio: máquina de café):**

```python
temperatura_actual = 22          # grados centígrados
temperatura_objetivo = 90        # grados centígrados
cafe_listo = False
tiempo_inicio = 0                # segundos
```

**Lo que debes observar:**
- Los nombres son descriptivos, no `x` ni `a`.
- Los valores iniciales tienen sentido.
- Los booleanos se usan para estados de "sí/no".

---

### 0.5.2 Bucle `while`

**Qué es:** un `while` repite un bloque de código mientras una condición sea verdadera. La condición se evalúa **antes** de cada vuelta.

**Ejemplo (dominio: semáforo peatonal con botón):**

```python
boton_presionado = False
segundos_esperando = 0

while not boton_presionado:
    segundos_esperando = segundos_esperando + 1
    if segundos_esperando >= 5:
        boton_presionado = True

print("Puedes cruzar")
```

**Lo que debes observar:**
- La condición del `while` debe poder cambiar a `False` **dentro** del bucle, o será infinito.
- La variable `segundos_esperando` se incrementa dentro del bucle.
- Hay una condición de salida por tiempo, no por acierto.

**Pregunta para ti:** ¿cuál es la condición exacta para que **tu** `while` siga corriendo? ¿Y cuál es la condición para que termine? Piensa en las dos cosas: acertar y agotar intentos.

---

### 0.5.3 `input()`

**Qué es:** `input()` muestra un mensaje al usuario, espera a que escriba algo y presione Enter, y **devuelve lo escrito como texto** (tipo `str`, no `int`).

**Ejemplo (dominio: pedido de restaurante):**

```python
nombre_plato = input("¿Qué plato deseas?: ")
bebida = input("¿Qué bebida?: ")
print("Pedido confirmado:", nombre_plato, "con", bebida)
```

**Lo que debes observar:**
- `input("mensaje")` devuelve **siempre** un string. Aunque el usuario escriba `5`, `input()` devuelve `"5"` (texto), no `5` (número).
- La comparación `input() == 42` **siempre da `False`**, porque `"42"` no es igual a `42`.
- Por eso necesitarás convertir a entero después de validar (con `int()`).

---

### 0.5.4 Condicionales `if` / `elif` / `else`

**Qué es:** un condicional evalúa una condición booleana y ejecuta un bloque u otro según el resultado. `elif` solo se evalúa si el `if` anterior fue falso. `else` se ejecuta si nada fue verdadero.

**Ejemplo (dominio: termostato de aire acondicionado):**

```python
temperatura = 18

if temperatura < 15:
    print("Encender calefacción")
elif temperatura < 22:
    print("Temperatura agradable")
else:
    print("Encender aire acondicionado")
```

**Lo que debes observar:**
- Solo **una** rama se ejecuta por cada evaluación.
- Si usas `if` en lugar de `elif`, podrías ejecutar varias ramas por error.
- El orden de las condiciones importa: si `temperatura = 10`, entra al primer `if` y no llega al `elif`.

---

### 0.5.5 Validación de entrada

**Qué es:** validar es revisar que los datos que llegan sean los esperados **antes** de usarlos. Si no son válidos, se le pide al usuario que corrija.

**Ejemplo (dominio: formulario de teléfono):**

```python
telefono = input("Teléfono (10 dígitos): ").strip()

if not telefono.isdigit():
    print("Error: solo se permiten números.")
elif len(telefono) != 10:
    print("Error: deben ser exactamente 10 dígitos.")
else:
    print("Teléfono válido:", telefono)
```

**Lo que debes observar y reutilizar como técnica:**
- `.strip()` elimina espacios al inicio y al final. Úsalo siempre sobre el resultado de `input()`.
- `.isdigit()` devuelve `True` si el string contiene **solo dígitos** y al menos un carácter. Devuelve `False` para strings vacíos, con letras, con puntos o con signos.
- `len()` cuenta caracteres.
- Si usas `.isdigit()` para validar, no necesitas `try/except`. Esa es la razón por la que tu proyecto **no** debe usar `try/except`: la validación con `.isdigit()` es suficiente para un rango de 1 a 100.
- Después de validar que es dígito, sí conviertes a entero con `int()`.

**Nota importante:** `.isdigit()` **no acepta** números negativos (`"-5".isdigit()` es `False`). Para tu juego eso está bien, porque los negativos están fuera del rango 1–100 de todos modos. Pero tenlo presente para el futuro.

---

### 0.5.6 Funciones

**Qué es:** una función es un bloque de código con nombre que puedes llamar varias veces. Recibe parámetros (opcionalmente) y puede devolver un valor (opcionalmente).

**Ejemplo (dominio: cajero de tienda):**

```python
def calcular_cambio(precio, pago):
    return pago - precio


def mostrar_ticket(producto, precio, pago):
    cambio = calcular_cambio(precio, pago)
    print(f"Producto: {producto}")
    print(f"Precio: ${precio}")
    print(f"Pagaste: ${pago}")
    print(f"Cambio: ${cambio}")


mostrar_ticket("Café americano", 35, 50)
```

**Lo que debes observar:**
- `return` devuelve un valor que puedes guardar en una variable.
- Una función puede llamar a otra función (composición).
- Una función puede no devolver nada (como `mostrar_ticket`) y aun así ser útil: hace una acción.
- Los parámetros son la forma de pasar datos **hacia adentro** de la función.

**Pregunta para ti:** ¿cuáles son las dos (o más) funciones que **tu** proyecto necesita? Una suele ser el flujo principal. ¿Qué otra cosa repetitiva podrías aislar en una función?.

---

### 0.5.7 `random` (la única importación permitida)

**Qué es:** el módulo `random` genera valores pseudoaleatorios. Para este proyecto solo necesitas una función: `random.randint(a, b)`, que devuelve un entero aleatorio entre `a` y `b`, ambos inclusive.

**Ejemplo (dominio: tirar un dado de 6 caras):**

```python
import random

resultado = random.randint(1, 6)
print(f"Tiraste un {resultado}")
```

**Nota honesta sobre este concepto:** este es el **único** caso de todo el documento donde la sintaxis exacta que necesitas es igual a la del ejemplo. No hay otra forma de generar un número aleatorio en un rango en Python. Pero tú decides **qué rango** usar y **dónde** guardar el resultado. El ejemplo usa 1–6 (dado); tu juego usará otros valores definidos por tus constantes.

---

## 0.6 Errores Comunes (Anti-patrones a Evitar)

Estos son los tropiezos más frecuentes. Si alguno te pasa, no es fracaso: es parte del aprendizaje. Pero detéctalos **antes** de entregar.

1. **Olvidar `.strip()`** antes de `.isdigit()`. Si el usuario escribe `" 5 "` (con espacios), `.isdigit()` devuelve `False` y el programa rechaza un número válido.
2. **Comparar el string de `input()` con un entero.** `input("...") == 42` siempre es `False`, porque `"42" != 42`. Debes convertir a entero **después** de validar.
3. **Contar intentos fuera del `while`.** Si el contador se incrementa una sola vez, nunca llegará a 7. Debe incrementarse dentro del bucle (o donde corresponda según tu diseño).
4. **No incrementar intentos en entradas inválidas... pero tampoco dejarlo mal.** Regla del contrato: **entrada inválida NO consume intento**. Verifica esto con cuidado: no basta con "no incrementar", tienes que asegurarte de que el flujo vuelve a pedir el número **sin** haber consumido uno.
5. **Usar `if` en lugar de `elif`** cuando solo debe ejecutarse una rama. Si el jugador acierta, no debe imprimir también "muy alto" o "muy bajo".
6. **Olvidar `break` o una bandera de salida** después de acertar. Si solo imprimes `¡Correcto!` pero no rompes el bucle, el juego sigue corriendo.
7. **Hardcodear el número secreto.** Debes usar `random.randint(MINIMO, MAXIMO)`, no `42` escrito a mano.
8. **Meter todo el código en el nivel superior del archivo sin funciones.** El contrato exige al menos dos funciones.
9. **No manejar el caso de agotar intentos.** Si el jugador nunca acierta, el programa debe revelar el número y terminar, no quedarse colgado.
10. **Usar `try/except`.** Eso viene en la Estación 4. Aquí no.

---

## 0.7 Pruebas Manuales Obligatorias

Antes de entregar, ejecuta estas pruebas a mano. Si alguna falla, corrige y vuelve a empezar.

### Prueba A - Camino feliz (victoria)

1. Ejecuta `python adivina.py`.
2. Juega hasta acertar en algún intento menor a 7.
3. Verifica:
   - [ ] El mensaje de bienvenida aparece.
   - [ ] Los intentos se numeran correctamente del 1 al que aciertes.
   - [ ] Cada intento incorrecto muestra "Muy bajo" o "Muy alto" (según corresponda).
   - [ ] Al acertar, se imprime `¡Correcto!` con el número de intentos usados.
   - [ ] El programa termina.

### Prueba B - Camino de derrota

1. Ejecuta `python adivina.py`.
2. Juega 7 veces con números incorrectos.
3. Verifica:
   - [ ] Se muestran los 7 intentos numerados del 1 al 7.
   - [ ] Al llegar al intento 7 sin acertar, se revela el número secreto.
   - [ ] El programa termina sin colgarse.

### Prueba C - Validación de entradas inválidas

En una partida, en algún intento escribe **en este orden**:

1. `abc` → debe mostrar error, **no** consumir intento, y volver a pedir el mismo número de intento.
2. `5.5` → debe mostrar error, **no** consumir intento.
3. `-5` → debe mostrar error, **no** consumir intento.
4. `0` → debe mostrar error, **no** consumir intento (fuera de rango).
5. `101` → debe mostrar error, **no** consumir intento (fuera de rango).
6. `  50  ` (con espacios) → debe **aceptar** como número válido.
7. Presionar Enter sin escribir nada → debe mostrar error, no consumir intento.

### Prueba D - Contador correcto

1. Ejecuta y juega.
2. En cada `Intento X/7`, verifica que `X` refleje el número real de intentos consumidos (las entradas inválidas no deben aumentar `X`).
3. Al final, el número de intentos reportado en el mensaje de victoria debe coincidir con el último `X` que se mostró antes de acertar.

### Prueba E - Sin concepto prohibido

Ejecuta en la terminal, dentro de la carpeta del proyecto:

```bash
grep -n "try\|except\|class \|import json\|open(" adivina.py
```

Debe devolver **vacío**. Si devuelve algo, estás violando un anti-requisito.

---

## 0.8 Git (Versión Mínima para Esta Estación)

En esta estación **no usamos ramas ni Pull Requests**. Eso empieza en la Estación 1. Aquí solo practicamos los comandos más básicos.

```bash
# 1. Si no tienes repositorio, inicialízalo
git init

# 2. Primer commit: cuando ya tengas un archivo adivina.py, aunque esté incompleto
git add adivina.py
git commit -m "feat: esqueleto inicial del juego"

# 3. Cuando el juego esté completo y pase todas las pruebas manuales
git add adivina.py
git commit -m "feat: juego adivina el numero completo"

# 4. Revisar el historial
git log --oneline
```

**Reglas de commit para esta estación:**

- Empieza el mensaje con `feat:` cuando el commit agrega funcionalidad.
- Sé específico y breve. "cambios" no es un buen mensaje.
- Haz al menos **dos commits** (uno con el esqueleto, uno con la versión final). Así practicas la idea de commits atómicos.

---

## 0.9 Qué Hacer Si Te Atascas

Sigue este protocolo en orden. No saltes al final.

1. **Relee la sección 0.5** del concepto que no entiendes.
2. **Abre una terminal de Python** (`python` sin argumentos) y copia el ejemplo de esa sección línea por línea. Ejecuta cada línea para ver qué pasa.
3. **Imprime variables** dentro de tu código para ver qué valores tienen en cada paso. Por ejemplo: `print("DEBUG numero_secreto =", numero_secreto)` o `print("DEBUG intento =", intento)`. Luego borra esas líneas cuando termines.
4. **Aíslate en un archivo aparte.** Si tu `while` no funciona, crea un archivo `prueba.py` con solo ese `while` y un `print()` de prueba, hasta que funcione. Luego lo llevas al proyecto.
5. **Hazte dos preguntas clave:**
   - ¿Cuál es la condición exacta para que el `while` siga corriendo?
   - ¿Cuál es la condición exacta para que termine? (Pista: hay **dos** formas de que termine).
6. Si tras 30 minutos seguidos sigues atascado en lo mismo dime lo siguiente:
   - Qué intentaste.
   - Qué esperabas que pasara.
   - Qué pasó en realidad (pega el error o el output).
   - El fragmento mínimo de código que reproduce el problema.

---

## 0.10 Checklist Final de Aceptación

Marca cada casilla **solo** cuando lo hayas verificado tú mismo.

- [ ] `adivina.py` existe y corre con `python adivina.py`.
- [ ] Las 7 reglas de la sección 0.3.2 están implementadas.
- [ ] Hay al menos dos funciones definidas.
- [ ] Las tres constantes (`MINIMO`, `MAXIMO`, `INTENTOS_MAXIMOS`) están al inicio.
- [ ] Se usa `random.randint`.
- [ ] La validación con `.strip()` + `.isdigit()` + rango funciona.
- [ ] Las entradas inválidas no consumen intento.
- [ ] El contador `Intento X/7` es correcto en todo momento.
- [ ] El camino de victoria y el de derrota funcionan.
- [ ] `grep -n "try\|except\|class \|import json\|open(" adivina.py` devuelve vacío.
- [ ] Hay al menos dos commits en Git con mensajes descriptivos.
- [ ] Pasaste las pruebas manuales A, B, C, D y E.

---

## 0.11 Qué Viene Después

Si esta estación te resultó cómoda, estás listo para la **Estación 1: Agenda de contactos en memoria**.

En la Estación 1 seguimos sin clases ni archivos, pero introduciremos:

- Listas de diccionarios (una estructura de datos nueva).
- Menús con varias opciones (un `while` con `if/elif` más elaborado).
- **Git con ramas**, aunque todavía sin Pull Requests.

Si esta estación te costó, no te preocupes: repítela una vez más con variaciones (por ejemplo, sube el rango a 1–1000, o baja los intentos a 5). La repetición con variaciones es una de las formas más efectivas de consolidar el aprendizaje.
