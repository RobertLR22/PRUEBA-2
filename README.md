# Guía: Sistema de Auditoría de Inventario

## Arquitectura Hexagonal (Ports & Adapters) con Python

### Filosofía de esta guía

> **Esta guía NO te da las respuestas. Te da las herramientas para que TÚ las construyas.**
>
> Cada concepto viene con **ejemplos genéricos** (de otros dominios, como animales, vehículos o figuras geométricas) para que entiendas la mecánica. Luego, en tu proyecto real, encontrarás **TODOs con pistas y explicaciones** de qué debe hacer cada pieza, pero **el código lo escribes tú**.
>
> Si copias y pegas los ejemplos, no aprenderás. Si adaptas los ejemplos a tu problema, sí.

---

## Índice General

1. [Introducción y Filosofía](#1-introducción-y-filosofía)
2. [Conceptos Fundamentales de Python](#2-conceptos-fundamentales-de-python)
3. [¿Qué es la Arquitectura Hexagonal?](#3-qué-es-la-arquitectura-hexagonal)
4. [Flujo de Trabajo Profesional con Git](#4-flujo-de-trabajo-profesional-con-git)
5. [Configuración Inicial del Repositorio](#5-configuración-inicial-del-repositorio)
6. [FASE 1: El Dominio](#6-fase-1-el-dominio)
7. [FASE 2: Los Puertos](#7-fase-2-los-puertos)
8. [FASE 3: Los Adaptadores](#8-fase-3-los-adaptadores)
9. [FASE 4: La Aplicación](#9-fase-4-la-aplicación)
10. [FASE 5: El CLI](#10-fase-5-el-cli)
11. [Checklist Final](#11-checklist-final-de-arquitectura)
12. [Glosario Completo](#12-glosario-completo)
13. [Preguntas de Autoevaluación](#13-preguntas-de-autoevaluación)

---

## 1. Introducción y Filosofía

### 1.1 ¿Qué especifica esta guia?

Esta guía está diseñada para alguien que **apenas comienza** en programación. No asumo que sabes qué es una clase, un objeto, una interfaz o una inyección de dependencias. Vamos a construir todo desde cero, con analogías del mundo real y **ejemplos genéricos** que te enseñen la mecánica.

**Pero hay una regla inquebrantable:**

> **Cada `# TODO:` que veas en tu proyecto es tuyo. Nadie lo va a resolver por ti.**
>
> Los ejemplos que verás usan dominios distintos (animales, vehículos, figuras). Tú deberás **traducir** esos ejemplos a tu dominio de inventario. Si te atascas, investiga, prueba, rompe el código y vuelve a intentarlo. Eso es ser ingeniero.

### 1.2 Perfil de Entrada y Salida

| Aspecto | Antes (Entrada) | Después (Salida) |
|---|---|---|
| **Python** | Variables, `if/else`, listas, diccionarios, funciones | Clases, objetos, herencia, clases abstractas, dataclasses, tipado |
| **Arquitectura** | Ninguno | Hexagonal, Puertos y Adaptadores, Inyección de Dependencias |
| **Git** | `add`, `commit`, `push` básico | Ramas, Pull Requests, Conventional Commits |
| **Errores** | `try/except` básico | Excepciones personalizadas, traducción de errores |
| **Persistencia** | Ninguna o archivos de texto | JSON estructurado, repositorios, abstracción |

### 1.3 ¿Qué vas a construir?

Un **Sistema de Auditoría de Inventario** que permita:

1. **Registrar productos** con ID, nombre, cantidad y precio unitario.
2. **Listar todos los productos** del inventario.
3. **Buscar productos** por su ID.
4. **Auditar un producto**: comparar la cantidad registrada contra la contada físicamente.
5. **Reportar faltantes**: productos cuya cantidad está por debajo de un mínimo.
6. **Calcular el valor total** del inventario.
7. **Eliminar productos** del inventario.

---

## 2. Conceptos Fundamentales de Python

Antes de entrar en materia, vamos a repasar los conceptos de Python que usarás. **Cada concepto viene con ejemplos genéricos** (no de inventario) para que entiendas la mecánica. Tú luego los adaptarás a tu problema.

### 2.1 ¿Qué es una Clase?

#### Analogía: El Plano vs. La Casa

Una **clase** es un **plano arquitectónico**: define qué tendrá una casa (puertas, ventanas, color). Una **instancia** es una **casa real construida** a partir de ese plano. Puedes construir 100 casas del mismo plano, y cada una tendrá sus propios valores.

#### Ejemplo genérico: Clase `Vehiculo`

```python
class Vehiculo:
    def __init__(self, marca, modelo, anio):
        self.marca = marca
        self.modelo = modelo
        self.anio = anio

    def descripcion(self):
        return f"{self.marca} {self.modelo} ({self.anio})"

# Crear instancias
auto = Vehiculo("Toyota", "Corolla", 2020)
moto = Vehiculo("Yamaha", "FZ", 2022)

print(auto.descripcion())   # Toyota Corolla (2020)
print(moto.descripcion())   # Yamaha FZ (2022)
```

**Explicación línea por línea:**

- `class Vehiculo:` → Define una clase. `class` es palabra reservada.
- `def __init__(self, marca, modelo, anio):` → Constructor. Se ejecuta al crear la instancia. `self` es la referencia al objeto mismo.
- `self.marca = marca` → Crea un **atributo** llamado `marca` en el objeto y le asigna el valor del parámetro.
- `def descripcion(self):` → Define un **método** (función que pertenece a la clase).
- `Vehiculo("Toyota", "Corolla", 2020)` → Llama al constructor. Python crea el objeto, ejecuta `__init__`, y devuelve el objeto.
- `auto.descripcion()` → Llama al método sobre el objeto. Python pasa automáticamente `auto` como `self`.

#### Ejemplo genérico: Clase con validación

```python
class Circulo:
    def __init__(self, radio):
        if radio <= 0:
            raise ValueError("El radio debe ser positivo")
        self.radio = radio

    def area(self):
        return 3.1416 * (self.radio ** 2)

# Válido
c1 = Circulo(5)
print(c1.area())  # 78.54

# Inválido
try:
    c2 = Circulo(-3)
except ValueError as e:
    print(f"Error: {e}")  # Error: El radio debe ser positivo
```

**Explicación:**

- `if radio <= 0:` → Validación antes de asignar el atributo.
- `raise ValueError("...")` → Lanza una excepción. Detiene la ejecución del constructor.
- `try/except` → Captura la excepción para manejarla sin que el programa se caiga.
- `self.radio ** 2` → Eleva al cuadrado.

### 2.2 ¿Qué es una `@dataclass`?

#### Analogía: El Formulario Pre-impreso

Una **`@dataclass`** es como un **formulario pre-impreso**: Python te genera automáticamente el `__init__`, el `__repr__` y la comparación entre objetos. Tú solo declaras los campos.

#### Ejemplo genérico: `@dataclass` para `Libro`

**Sin `@dataclass` (mucho código):**

```python
class Libro:
    def __init__(self, titulo, autor, paginas):
        self.titulo = titulo
        self.autor = autor
        self.paginas = paginas

    def __repr__(self):
        return f"Libro(titulo={self.titulo}, autor={self.autor}, paginas={self.paginas})"

    def __eq__(self, other):
        if not isinstance(other, Libro):
            return False
        return (self.titulo == other.titulo and
                self.autor == other.autor and
                self.paginas == other.paginas)
```

**Con `@dataclass` (mucho menos código):**

```python
from dataclasses import dataclass

@dataclass
class Libro:
    titulo: str
    autor: str
    paginas: int

libro = Libro("Cien años de soledad", "García Márquez", 471)
print(libro)  # Libro(titulo='Cien años de soledad', autor='García Márquez', paginas=471)
```

**Explicación:**

- `@dataclass` → Decorador que autogenera `__init__`, `__repr__` y `__eq__`.
- `titulo: str` → Campo con anotación de tipo.
- `libro = Libro(...)` → Construye la instancia usando el `__init__` autogenerado.
- `print(libro)` → Usa el `__repr__` autogenerado.

#### Ejemplo genérico: `@dataclass` con validación (`__post_init__`)

```python
from dataclasses import dataclass

@dataclass
class Rectangulo:
    base: float
    altura: float

    def __post_init__(self):
        if self.base <= 0:
            raise ValueError("La base debe ser positiva")
        if self.altura <= 0:
            raise ValueError("La altura debe ser positiva")

    def area(self):
        return self.base * self.altura

# Válido
r1 = Rectangulo(5, 3)
print(r1.area())  # 15

# Inválido
try:
    r2 = Rectangulo(-2, 4)
except ValueError as e:
    print(f"Error: {e}")  # Error: La base debe ser positiva
```

**Explicación:**

- `def __post_init__(self):` → Se ejecuta **después** del `__init__` autogenerado.
- `self.base` → Accede al valor ya asignado por el `__init__`.
- `raise ValueError(...)` → Lanza excepción si la validación falla.

### 2.3 ¿Qué es una Excepción?

#### Analogía: La Alarma de Incendios

Una **excepción** es como una **alarma de incendios**. Cuando algo va mal, no sigues cocinando: suena la alarma, todos evacúan, y se atiende la emergencia. En software, cuando un dato es inválido, **lanzas** una excepción en lugar de dejar pasar datos corruptos.

#### Ejemplo genérico: Excepciones para un sistema de biblioteca

```python
# Definir excepciones personalizadas
class ErrorDeBiblioteca(Exception):
    """Base para errores de la biblioteca."""
    pass

class LibroNoDisponibleError(ErrorDeBiblioteca):
    """El libro ya está prestado."""
    pass

class SocioNoRegistradoError(ErrorDeBiblioteca):
    """El socio no existe."""
    pass

# Usarlas
def prestar_libro(libro, socio):
    if not socio.registrado:
        raise SocioNoRegistradoError(f"El socio {socio.nombre} no está registrado")
    if libro.prestado:
        raise LibroNoDisponibleError(f"El libro '{libro.titulo}' ya está prestado")
    libro.prestado = True
    return f"Libro '{libro.titulo}' prestado a {socio.nombre}"
```

**Explicación:**

- `class ErrorDeBiblioteca(Exception):` → Excepción base. Hereda de `Exception`.
- `class LibroNoDisponibleError(ErrorDeBiblioteca):` → Hereda de la base. Si capturas `ErrorDeBiblioteca`, también capturas esta.
- `raise SocioNoRegistradoError(...)` → Lanza la excepción con un mensaje.
- **Ventaja:** Si quieres capturar **todos** los errores de biblioteca, haces `except ErrorDeBiblioteca`. Si quieres capturar solo uno, `except LibroNoDisponibleError`.

**¿Por qué no usar `ValueError` directamente?**

Porque `ValueError` es genérico. Si mañana quieres capturar **solo** los errores de tu dominio, usas `except ErrorDeBiblioteca`, y no capturarás otros `ValueError` que no tengan que ver.

### 2.4 ¿Qué es una Clase Abstracta?

#### Analogía: La Oferta de Trabajo

Una **clase abstracta** es como una **oferta de trabajo**: describe **qué** debe hacer el empleado, pero no dice **cómo**. Cualquier persona que cumpla los requisitos puede ser contratada.

#### Ejemplo genérico: Clase abstracta `FiguraGeometrica`

```python
from abc import ABC, abstractmethod

class FiguraGeometrica(ABC):
    """Contrato: toda figura debe saber calcular su área y perímetro."""

    @abstractmethod
    def area(self) -> float:
        """Calcula el área de la figura."""
        pass

    @abstractmethod
    def perimetro(self) -> float:
        """Calcula el perímetro de la figura."""
        pass

# Esto falla:
# f = FiguraGeometrica()  # TypeError: Can't instantiate abstract class

# Esto funciona:
class Cuadrado(FiguraGeometrica):
    def __init__(self, lado):
        self.lado = lado

    def area(self) -> float:
        return self.lado ** 2

    def perimetro(self) -> float:
        return self.lado * 4

class Circulo(FiguraGeometrica):
    def __init__(self, radio):
        self.radio = radio

    def area(self) -> float:
        return 3.1416 * self.radio ** 2

    def perimetro(self) -> float:
        return 2 * 3.1416 * self.radio

# Uso polimórfico
figuras = [Cuadrado(4), Circulo(3)]
for f in figuras:
    print(f"Área: {f.area()}, Perímetro: {f.perimetro()}")
```

**Explicación:**

- `from abc import ABC, abstractmethod` → Importa `ABC` y `abstractmethod`.
- `class FiguraGeometrica(ABC):` → Clase abstracta que hereda de `ABC`.
- `@abstractmethod` → Marca un método como abstracto. Las subclases **deben** implementarlo.
- `FiguraGeometrica()` → Falla con `TypeError` porque es abstracta.
- `class Cuadrado(FiguraGeometrica):` → Hereda e implementa **todos** los métodos abstractos.
- `figuras = [Cuadrado(4), Circulo(3)]` → Polimorfismo: ambas son `FiguraGeometrica`, pero cada una calcula a su manera.

### 2.5 ¿Qué es la Inyección de Dependencias?

#### Analogía: El Chef y su Proveedor

Un **chef** sabe cocinar, pero **no cultiva sus propios vegetales**. Alguien se los entrega: el **proveedor**. El chef no sabe si el proveedor trae del campo, de un invernadero o de otro país; solo sabe que le entregará los ingredientes según un contrato.

#### Ejemplo genérico: Notificador

**Sin inyección (malo):**

```python
class NotificadorEmail:
    def enviar(self, mensaje):
        print(f"Enviando email: {mensaje}")

class ServicioPedidos:
    def __init__(self):
        # El servicio CREA su propio notificador
        self.notificador = NotificadorEmail()

    def procesar(self, pedido):
        self.notificador.enviar(f"Pedido {pedido} procesado")
```

**Problema:** Si mañana quieres notificar por SMS, tienes que **modificar** `ServicioPedidos`. Además, no puedes probar sin enviar emails reales.

**Con inyección (bueno):**

```python
class NotificadorEmail:
    def enviar(self, mensaje):
        print(f"Email: {mensaje}")

class NotificadorSMS:
    def enviar(self, mensaje):
        print(f"SMS: {mensaje}")

class NotificadorFalso:
    def __init__(self):
        self.mensajes = []
    def enviar(self, mensaje):
        self.mensajes.append(mensaje)

class ServicioPedidos:
    def __init__(self, notificador):
        # El servicio RECIBE su notificador desde fuera
        self.notificador = notificador

    def procesar(self, pedido):
        self.notificador.enviar(f"Pedido {pedido} procesado")

# Uso con email
srv1 = ServicioPedidos(NotificadorEmail())
srv1.procesar(123)

# Uso con SMS
srv2 = ServicioPedidos(NotificadorSMS())
srv2.procesar(456)

# Uso con falso (para pruebas)
notif_falso = NotificadorFalso()
srv3 = ServicioPedidos(notif_falso)
srv3.procesar(789)
print(notif_falso.mensajes)  # ['Pedido 789 procesado']
```

**Ventajas:**

1. **Flexibilidad**: Cambias la implementación sin tocar el servicio.
2. **Testeabilidad**: Inyectas un notificador falso en las pruebas.
3. **Desacoplamiento**: El servicio no depende de una implementación concreta.

### 2.6 ¿Qué es el Tipado Estricto (`typing`)?

#### Ejemplo genérico: Funciones con anotaciones de tipo

```python
from typing import List, Optional, Dict

# Sin anotaciones
def promedio(numeros):
    return sum(numeros) / len(numeros)

# Con anotaciones
def promedio_tipado(numeros: List[float]) -> float:
    return sum(numeros) / len(numeros)

# Opcional (puede ser None)
def buscar_estudiante(nombre: str) -> Optional[str]:
    if nombre == "Ana":
        return "A001"
    return None

# Diccionario
def contar_palabras(texto: str) -> Dict[str, int]:
    resultado = {}
    for palabra in texto.split():
        resultado[palabra] = resultado.get(palabra, 0) + 1
    return resultado

# Uso
print(promedio_tipado([10.0, 20.0, 30.0]))  # 20.0
print(buscar_estudiante("Ana"))              # A001
print(buscar_estudiante("Luis"))             # None
print(contar_palabras("hola mundo hola"))    # {'hola': 2, 'mundo': 1}
```

**Explicación:**

- `numeros: List[float]` → Anota que `numeros` es una lista de flotantes.
- `-> float` → Anota que la función devuelve un flotante.
- `Optional[str]` → Puede ser `str` o `None`.
- `Dict[str, int]` → Diccionario con claves string y valores enteros.

**¿Por qué usar tipado?**

1. **Documentación**: Queda claro qué espera y qué devuelve cada función.
2. **Herramientas**: VS Code te avisa si pasas un tipo incorrecto.
3. **Verificación**: `mypy` puede verificar los tipos antes de ejecutar.
4. **Refactorización**: Cambiar un tipo es más seguro porque sabes dónde se usa.

### 2.7 ¿Qué es JSON?

#### Analogía: El Formulario Estandarizado

JSON es un **formato de texto** para guardar datos estructurados. Es como un formulario que cualquier lenguaje de programación puede leer y escribir.

#### Ejemplo genérico: Guardar estudiantes en JSON

```python
import json

# Diccionario
estudiante = {"id": "A001", "nombre": "Ana", "nota": 9.5}

# Convertir a JSON (string)
print(json.dumps(estudiante, indent=4))

# Guardar en archivo
with open("estudiante.json", "w") as f:
    json.dump(estudiante, f, indent=4)

# Leer de archivo
with open("estudiante.json", "r") as f:
    leido = json.load(f)
    print(leido["nombre"])  # Ana

# Lista de estudiantes
estudiantes = [
    {"id": "A001", "nombre": "Ana", "nota": 9.5},
    {"id": "A002", "nombre": "Luis", "nota": 7.0}
]
with open("estudiantes.json", "w") as f:
    json.dump(estudiantes, f, indent=4)
```

**Explicación:**

- `json.dumps(obj)` → Convierte un objeto Python a un string JSON.
- `json.dump(obj, archivo)` → Escribe el objeto Python directamente en un archivo.
- `json.load(archivo)` → Lee un archivo JSON y lo convierte a un objeto Python.
- `indent=4` → Formatea con 4 espacios de indentación.

---

## 3. ¿Qué es la Arquitectura Hexagonal?

### 3.1 Analogía: El Enchufe de Pared

Imagina que tu casa es el **Dominio** (la lógica de negocio). Las paredes tienen **enchufes** (los **Puertos**), que son un estándar: "cualquier cosa que se enchufe aquí debe entregar 110V y 2 patas". No importa si enchufas una licuadora, un cargador o una TV; el enchufe no cambia. Los **Adaptadores** son los cables específicos de cada dispositivo.

### 3.2 Los Componentes

| Término | Significado | En tu proyecto |
|---|---|---|
| **Dominio** | Reglas de negocio puras. | `Producto` |
| **Puerto** | Contrato/interfaz. | `RepositorioInventario` |
| **Adaptador** | Implementación concreta. | `RepositorioJSON`, `MenuCLI` |
| **Caso de Uso** | Orquesta el dominio. | `ServicioAuditoria` |
| **DI** | Pasar colaboradores desde fuera. | `ServicioAuditoria(repositorio)` |

### 3.3 La Regla Hexagonal

> **El dominio nunca debe importar `json`, `os`, `print`, ni nada de infraestructura. Solo conoce sus puertos.**

- `domain/` no puede tener `import json`, `open()`, `print()`, `input()`.
- `ports/` solo puede importar `abc`, `typing` y `domain`.
- `application/` solo puede importar `domain` y `ports`.
- `adapters/` puede importar todo lo que necesite.
- `main.py` ensambla todo.

### 3.4 Diagrama

```
                    ┌─────────────────────────────────────┐
                    │           main.py                   │
                    │  (Ensambla todo: DI)                │
                    └─────────────────────────────────────┘
                                      │
              ┌───────────────────────┼───────────────────────┐
              │                       │                       │
              ▼                       ▼                       ▼
    ┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐
    │   adapters/     │   │  application/   │   │    ports/       │
    │  - cli.py       │   │ - services.py   │   │ - repository.py │
    │  - json_repo.py │   │                 │   │                 │
    └─────────────────┘   └─────────────────┘   └─────────────────┘
              │                       │                       │
              └───────────────────────┼───────────────────────┘
                                      │
                                      ▼
                            ┌─────────────────┐
                            │    domain/      │
                            │ - models.py     │
                            │ - exceptions.py │
                            └─────────────────┘
```

---

## 4. Flujo de Trabajo Profesional con Git

### 4.1 ¿Por qué no trabajar directamente en `main`?

`main` es la rama **estable** y **protegida**. Cada cambio se hace en una rama separada, se revisa mediante un **Pull Request (PR)**, y solo después de la aprobación se fusiona.

**Ventajas:**

1. **Calidad**: Otro desarrollador revisa tu código.
2. **Historial limpio**: Cada funcionalidad tiene su rama.
3. **Seguridad**: Si algo sale mal, reviertes el PR sin afectar a los demás.
4. **Colaboración**: Varias personas trabajan en paralelo sin pisarse.

### 4.2 Modelo de Ramas

```
main
 |
 |-- feature/domain-core
 |-- feature/ports-interfaces
 |-- feature/infrastructure-adapter
 |-- feature/application-usecases
 |-- feature/cli-menu
```

**Reglas:**

1. `main` es **intocable directamente**.
2. Cada fase en su propia rama `feature/*`.
3. Una rama = una responsabilidad = un PR.
4. Commits **atómicos** con **Conventional Commits**.
5. Antes de pedir revisión, corre tus pruebas y verifica el checklist.

### 4.3 Convención de Ramas

| Tipo | Prefijo | Ejemplo |
|---|---|---|
| Nueva funcionalidad | `feature/` | `feature/domain-core` |
| Corrección de bug | `fix/` | `fix/json-corrupto` |
| Refactor | `refactor/` | `refactor/servicio-auditoria` |
| Documentación | `docs/` | `docs/readme-inicial` |
| Mantenimiento | `chore/` | `chore/gitignore` |

### 4.4 Conventional Commits

**Formato:**

```
<tipo>(<alcance>): <descripción corta en imperativo>
```

| Tipo | Uso |
|---|---|
| `feat` | Nueva funcionalidad |
| `fix` | Corrección de bug |
| `refactor` | Cambio sin nueva funcionalidad ni fix |
| `docs` | Solo documentación |
| `test` | Pruebas |
| `chore` | Build, dependencias, configuración |
| `style` | Formato, sin cambios de lógica |

**Ejemplos correctos:**

```
feat(domain): agregar entidad Producto con validaciones
fix(adapters): manejar JSONDecodeError en RepositorioJSON
refactor(application): inyectar repositorio por constructor
docs(readme): agregar guía de flujo Git
```

**Ejemplos incorrectos:**

```
cambios              <- vago
Update models.py     <- sin tipo, mayúscula
arregle el bug       <- sin tipo, sin alcance
```

### 4.5 Ciclo de Trabajo por Fase

```bash
# 1. Asegurarte de estar en main actualizado
git checkout main
git pull origin main

# 2. Crear la rama de la fase
git checkout -b feature/nombre-de-la-fase

# 3. Trabajar, haciendo commits atómicos
git add <archivo-especifico>       # NUNCA 'git add .' a ciegas
git commit -m "feat(scope): descripción clara"

# 4. Empujar la rama
git push -u origin feature/nombre-de-la-fase

# 5. Abrir PR en GitHub:
#    - Título en Conventional Commit
#    - Descripción con checklist
#    - Asignar revisor
#    - NO hacer merge tú mismo

# 6. Esperar revisión, aplicar cambios, empujar de nuevo
git add <archivo>
git commit -m "refactor(scope): aplicar feedback"
git push

# 7. Una vez aprobado, el revisor hace merge (Squash & Merge)
# 8. Volver a main y actualizar
git checkout main
git pull origin main

# 9. Borrar la rama local
git branch -d feature/nombre-de-la-fase
```

### 4.6 Plantilla de Pull Request

Guarda este archivo como `.github/pull_request_template.md`:

```markdown
## Descripción
<!-- Qué hace este PR y por qué -->

## Fase
<!-- Fase 1, 2, 3, 4 o 5 -->

## Tipo de cambio
- [ ] Nueva funcionalidad (feat)
- [ ] Corrección de bug (fix)
- [ ] Refactor (refactor)
- [ ] Documentación (docs)

## Cómo probarlo
<!-- Comandos exactos que el revisor debe ejecutar -->

## Checklist
- [ ] Los commits siguen Conventional Commits
- [ ] El código no rompe la arquitectura hexagonal
- [ ] `grep -R "print(\|import json\|open(" domain/ ports/` devuelve vacío
- [ ] Las pruebas manuales de la fase pasan
- [ ] No hay archivos basura en el PR

## Capturas / Evidencia
<!-- Opcional -->
```

### 4.7 Reglas de Convivencia

- **No hagas force push** sobre ramas de otros.
- **No mezcles dos fases en un mismo PR.**
- **No commitees** archivos de `data/*.json`.
- **Revisa tu propio diff** antes de pedir revisión: `git diff main...HEAD`.
- **Sé consistente** con el idioma de los commits.

### 4.8 Ejercicio de Verificación del Flujo

Antes de empezar la Fase 1, crea un PR de prueba:

```bash
git checkout -b docs/readme-inicial
# Edita este README (agrega tu nombre como autor)
git add README.md
git commit -m "docs(readme): agregar autor del proyecto"
git push -u origin docs/readme-inicial
# Abre el PR en GitHub, asígnalo a tu mentor
```

**Criterio de aceptación:**
- El PR se ve profesional.
- El checklist está marcado.
- El mentor puede hacer merge sin pedir cambios.

---

## 5. Configuración Inicial del Repositorio

```bash
# 1. Clona el repositorio o inicialízalo
git clone <url-del-repo>
cd inventory_audit

# 2. Crea la estructura base
mkdir -p domain ports adapters application data

# 3. Crea los __init__.py vacíos
touch domain/__init__.py ports/__init__.py adapters/__init__.py application/__init__.py

# 4. Crea un .gitignore mínimo
cat > .gitignore << 'EOF'
__pycache__/
*.pyc
*.pyo
.env
.venv/
venv/
data/*.json
.pytest_cache/
.mypy_cache/
EOF

# 5. Crea la plantilla de PR
mkdir -p .github
# Pega aquí el contenido de la sección 4.6

# 6. Primer commit en una rama
git checkout -b chore/estructura-inicial
git add .
git commit -m "chore: estructura inicial del proyecto hexagonal"
git push -u origin chore/estructura-inicial
# Abre PR, espera revisión, merge
```

### Estructura final esperada

```
inventory_audit/
├── .github/
│   └── pull_request_template.md
├── domain/          # Reglas de negocio puras
│   └── __init__.py
├── ports/           # Contratos (interfaces)
│   └── __init__.py
├── adapters/        # Implementaciones concretas
│   └── __init__.py
├── application/     # Casos de uso / servicios
│   └── __init__.py
├── data/            # Archivos JSON de persistencia
├── main.py          # Punto de entrada (se crea en Fase 5)
├── README.md        # Este documento
└── .gitignore
```

---

## 6. FASE 1: El Dominio

**Rama:** `feature/domain-core`

### 6.1 Objetivos

- Crear `domain/exceptions.py` con excepciones personalizadas.
- Crear `domain/models.py` con la entidad `Producto` como `@dataclass`.
- **Regla estricta:** ningún `print`, `import json`, `open()` dentro de `domain/`.

### 6.2 ¿Qué es una Entidad?

Una **entidad** es un objeto con **identidad propia**. En tu caso, un `Producto` tiene un `id` único que lo distingue. Aunque dos productos tengan el mismo nombre y precio, si tienen `id` diferente, son productos distintos.

**Características:**
- Tiene un identificador único.
- Tiene datos que la describen.
- Tiene reglas de negocio.
- **No sabe** cómo se guarda ni cómo se muestra.

### 6.3 ¿Qué son las Excepciones de Dominio?

Las **excepciones de dominio** representan errores específicos de las reglas de negocio. No son errores técnicos ("archivo no encontrado"), sino errores de negocio ("producto inválido").

**Ventajas:**
1. **Claridad**: `ProductoInvalidoError` es más descriptivo que `ValueError`.
2. **Jerarquía**: Puedes capturar todas con `except ErrorDeDominio`.
3. **Separación**: El dominio no depende de excepciones genéricas.

### 6.4 Crear `domain/exceptions.py`

**Lo que debes construir:**

Necesitas **tres** excepciones:

1. `ErrorDeDominio` → Base para todas. Hereda de `Exception`.
2. `ProductoInvalidoError` → Hereda de `ErrorDeDominio`. Se lanza cuando un producto viola las reglas.
3. `ProductoNoEncontradoError` → Hereda de `ErrorDeDominio`. Se lanza cuando buscas un producto que no existe.

**Pista basada en el ejemplo genérico:**

En el ejemplo de la biblioteca viste cómo se define una jerarquía de excepciones:

```python
class ErrorDeBiblioteca(Exception):
    pass

class LibroNoDisponibleError(ErrorDeBiblioteca):
    pass
```

**Tu tarea:** Adapta ese patrón a tu dominio. Escribe `domain/exceptions.py` con las tres clases. Agrega docstrings que expliquen cuándo se lanza cada una.

**Criterio de verificación:**

```bash
python -c "from domain.exceptions import ErrorDeDominio, ProductoInvalidoError, ProductoNoEncontradoError; print('OK')"
# Debe imprimir: OK
```

### 6.5 Crear `domain/models.py`

**Lo que debes construir:**

Una `@dataclass` llamada `Producto` con **cuatro campos**:

- `id: str`
- `nombre: str`
- `cantidad: int`
- `precio_unitario: float`

Y un método `__post_init__` que valide:

- `id` no vacío.
- `nombre` no vacío.
- `cantidad >= 0`.
- `precio_unitario >= 0`.

Si alguna validación falla, lanza `ProductoInvalidoError`.

**Pista basada en el ejemplo genérico:**

En el ejemplo del `Rectangulo` viste cómo se valida en `__post_init__`:

```python
@dataclass
class Rectangulo:
    base: float
    altura: float

    def __post_init__(self):
        if self.base <= 0:
            raise ValueError("La base debe ser positiva")
        # ...
```

**Tu tarea:** Adapta ese patrón. En lugar de `ValueError`, lanza `ProductoInvalidoError`. Agrega las cuatro validaciones. Piensa: ¿cómo verificas que un string no está vacío? (Pista: `if not self.nombre or self.nombre.strip() == "":`).

**Criterio de verificación:**

```bash
# Producto válido
python -c "from domain.models import Producto; p = Producto('A1','Laptop',5,1500.0); print(p)"
# Debe imprimir: Producto(id='A1', nombre='Laptop', cantidad=5, precio_unitario=1500.0)

# Producto inválido (cantidad negativa)
python -c "from domain.models import Producto; Producto('A2','Mouse',-3,25.0)"
# Debe lanzar ProductoInvalidoError

# Verificar que NO hay acoplamiento a infraestructura
grep -R "import json\|open(\|print(" domain/
# Debe estar vacío
```

### 6.6 Cierre de la Fase

```bash
git add domain/exceptions.py domain/models.py
git commit -m "feat(domain): agregar entidad Producto y excepciones de dominio"
git push -u origin feature/domain-core
# Abre PR siguiendo la plantilla
```

### 6.7 Preguntas de Autoevaluación

1. ¿Qué diferencia hay entre una clase y una instancia?
2. ¿Qué hace el decorador `@dataclass`?
3. ¿Para qué sirve `__post_init__`?
4. ¿Por qué creamos excepciones personalizadas en lugar de usar `ValueError`?
5. ¿Por qué `domain/` no debe importar `json`?

---

## 7. FASE 2: Los Puertos

**Rama:** `feature/ports-interfaces`

### 7.1 Objetivos

- Crear `ports/repository.py` con una clase abstracta `RepositorioInventario`.
- Definir métodos abstractos con tipado estricto.
- **No** implementar lógica: solo firmas.

### 7.2 ¿Qué es un Puerto?

Un **puerto** es un **contrato**. Define **qué** se necesita, pero no **cómo** se hace. En tu caso, `RepositorioInventario` dice: "quien me implemente debe saber guardar, listar, buscar por ID y eliminar productos".

**Analogía:** Un puerto USB define la forma del conector, no el dispositivo.

### 7.3 Crear `ports/repository.py`

**Lo que debes construir:**

Una clase abstracta `RepositorioInventario(ABC)` con **cuatro métodos abstractos**:

1. `guardar(self, producto: Producto) -> None`
2. `listar(self) -> List[Producto]`
3. `buscar_por_id(self, producto_id: str) -> Optional[Producto]`
4. `eliminar(self, producto_id: str) -> None`

Cada método debe:
- Tener `@abstractmethod`.
- Tener un docstring que explique qué hace.
- Tener `pass` como cuerpo (no implementación).

**Pista basada en el ejemplo genérico:**

En el ejemplo de `FiguraGeometrica` viste cómo se define una clase abstracta:

```python
from abc import ABC, abstractmethod

class FiguraGeometrica(ABC):
    @abstractmethod
    def area(self) -> float:
        pass
```

**Tu tarea:** Adapta ese patrón. Importa `Producto` desde `domain.models`. Usa `List` y `Optional` desde `typing`.

**Criterio de verificación:**

```bash
# NO se puede instanciar
python -c "from ports.repository import RepositorioInventario; RepositorioInventario()"
# Debe lanzar TypeError: Can't instantiate abstract class

# El puerto NO importa infraestructura
grep -R "import json\|open(" ports/
# Debe estar vacío
```

### 7.4 Reto Extra (Opcional): Puerto Notificador

Si quieres practicar, crea `ports/notificador.py` con una clase abstracta `Notificador` que tenga un método `notificar(mensaje: str) -> None`. Lo usarás en la Fase 4 si decides implementarlo.

### 7.5 Cierre de la Fase

```bash
git add ports/repository.py
git commit -m "feat(ports): contrato RepositorioInventario con métodos abstractos"
git push -u origin feature/ports-interfaces
# Abre PR siguiendo la plantilla
```

### 7.6 Preguntas de Autoevaluación

1. ¿Qué diferencia hay entre una clase normal y una abstracta?
2. ¿Para qué sirve `@abstractmethod`?
3. ¿Por qué no se puede instanciar `RepositorioInventario`?
4. ¿Qué significa que un puerto sea un "contrato"?
5. ¿Por qué el puerto no debe saber si los datos se guardan en JSON o SQL?

---

## 8. FASE 3: Los Adaptadores

**Rama:** `feature/infrastructure-adapter`

### 8.1 Objetivos

- Crear `adapters/json_repository.py`.
- Implementar `RepositorioJSON(RepositorioInventario)`.
- Manejar: archivo inexistente, JSON corrupto, permisos denegados.
- **No** romper el contrato: implementar **todos** los métodos abstractos.

### 8.2 ¿Qué es un Adaptador?

Un **adaptador** es una **implementación concreta** de un puerto. Mientras el puerto dice "necesito guardar productos", el adaptador dice "yo los guardo en JSON".

### 8.3 ¿Qué es `try/except`?

`try/except` maneja errores sin que el programa se caiga. Pones el código riesgoso en `try`, y el manejo en `except`.

**Analogía:** Cuando conduces, no asumes que nunca habrá un choque: llevas cinturón. En código, no asumes que el archivo JSON siempre existirá o será válido.

### 8.4 Crear `adapters/json_repository.py`

**Lo que debes construir:**

Una clase `RepositorioJSON` que herede de `RepositorioInventario`. Debe tener:

**Constructor `__init__(self, ruta_archivo: str)`:**
- Guardar `ruta_archivo` en `self.ruta`.
- Si el archivo no existe, crearlo con una lista vacía `[]`.
- Capturar `PermissionError` y lanzar `ErrorDeDominio`.

**Método privado `_leer_todos(self) -> List[dict]`:**
- Abrir el archivo, `json.load`, retornar la lista.
- Capturar `FileNotFoundError` → retornar `[]`.
- Capturar `json.JSONDecodeError` → lanzar `ErrorDeDominio("JSON corrupto")`.
- Capturar `PermissionError` → lanzar `ErrorDeDominio("Sin permisos")`.

**Método privado `_escribir_todos(self, datos: List[dict]) -> None`:**
- Abrir en modo `'w'`, `json.dump` con `indent=4`.
- Capturar `PermissionError` → lanzar `ErrorDeDominio`.

**Método `guardar(self, producto: Producto) -> None`:**
- Leer todos.
- Convertir `producto` a diccionario.
- Buscar por `id`: si existe, actualizar; si no, `append`.
- Escribir de nuevo.

**Método `listar(self) -> List[Producto]`:**
- Leer todos.
- Convertir cada dict a `Producto` con una list comprehension.

**Método `buscar_por_id(self, producto_id: str) -> Optional[Producto]`:**
- Leer todos.
- Iterar y retornar el `Producto` o `None`.

**Método `eliminar(self, producto_id: str) -> None`:**
- Leer todos.
- Filtrar la lista.
- Si no cambió el tamaño, lanzar `ProductoNoEncontradoError`.
- Escribir de nuevo.

**Pista basada en el ejemplo genérico:**

En el ejemplo de JSON viste cómo leer y escribir:

```python
with open("archivo.json", "w") as f:
    json.dump(datos, f, indent=4)

with open("archivo.json", "r") as f:
    datos = json.load(f)
```

**Tu tarea:** Adapta ese patrón. Envuelve las operaciones riesgosas en `try/except`. Traduce los errores técnicos a `ErrorDeDominio`.

**Criterio de verificación:**

```bash
# Guardar y listar
python -c "
from adapters.json_repository import RepositorioJSON
from domain.models import Producto
r = RepositorioJSON('data/test.json')
r.guardar(Producto('P1','Teclado',10,25.0))
r.guardar(Producto('P2','Monitor',3,300.0))
for p in r.listar(): print(p)
"

# Buscar por id
python -c "
from adapters.json_repository import RepositorioJSON
r = RepositorioJSON('data/test.json')
print(r.buscar_por_id('P1'))
print(r.buscar_por_id('NOEXISTE'))  # None
"

# Eliminar
python -c "
from adapters.json_repository import RepositorioJSON
r = RepositorioJSON('data/test.json')
r.eliminar('P2')
for p in r.listar(): print(p)
"

# JSON corrupto
echo "esto no es json" > data/test.json
python -c "
from adapters.json_repository import RepositorioJSON
r = RepositorioJSON('data/test.json')
r.listar()  # Debe lanzar ErrorDeDominio
"
```

### 8.5 Cierre de la Fase

```bash
git add adapters/json_repository.py
git commit -m "feat(adapters): repositorio JSON con manejo de errores de E/S"
git push -u origin feature/infrastructure-adapter
# Abre PR siguiendo la plantilla
```

### 8.6 Preguntas de Autoevaluación

1. ¿Qué diferencia hay entre un puerto y un adaptador?
2. ¿Por qué `RepositorioJSON` hereda de `RepositorioInventario`?
3. ¿Qué pasa si el archivo JSON está corrupto?
4. ¿Por qué traducimos `JSONDecodeError` a `ErrorDeDominio`?
5. ¿Qué significa `isinstance(r, RepositorioInventario)`?

---

## 9. FASE 4: La Aplicación

**Rama:** `feature/application-usecases`

### 9.1 Objetivos

- Crear `application/services.py` con `ServicioAuditoria`.
- Inyectar el repositorio por constructor.
- Implementar: `registrar_producto`, `listar_inventario`, `calcular_valor_total`, `reportar_faltantes`, `auditar`, `eliminar_producto`.

### 9.2 ¿Qué es un Servicio de Aplicación?

Un **servicio** **orquesta** el dominio para cumplir una tarea. No contiene reglas de negocio (esas están en el dominio), ni detalles de infraestructura (esos están en los adaptadores). Solo coordina.

**Analogía:** Un chef sabe cocinar, pero no cultiva sus vegetales. Alguien se los entrega: el proveedor (repositorio).

### 9.3 Crear `application/services.py`

**Lo que debes construir:**

Una clase `ServicioAuditoria` con:

**Constructor `__init__(self, repositorio: RepositorioInventario)`:**
- Guardar `repositorio` en `self.repositorio`.
- **No** crear el repositorio dentro. Recibirlo desde fuera (DI).

**Método `registrar_producto(self, producto: Producto) -> None`:**
- Delegar al repositorio: `self.repositorio.guardar(producto)`.

**Método `listar_inventario(self) -> List[Producto]`:**
- Delegar al repositorio: `return self.repositorio.listar()`.

**Método `calcular_valor_total(self) -> float`:**
- Listar productos.
- Sumar `cantidad * precio_unitario` de cada uno.
- Retornar el total.

**Método `reportar_faltantes(self, minimo: int = 5) -> List[Producto]`:**
- Listar productos.
- Filtrar los que tengan `cantidad < minimo`.
- Retornar la lista filtrada.

**Método `auditar(self, id_producto: str, cantidad_contada: int) -> Dict[str, int]`:**
- Buscar el producto con `self.repositorio.buscar_por_id(id_producto)`.
- Si es `None`, lanzar `ProductoNoEncontradoError`.
- Retornar un dict con:
  - `'esperado'`: `producto.cantidad`
  - `'contado'`: `cantidad_contada`
  - `'diferencia'`: `producto.cantidad - cantidad_contada`

**Método `eliminar_producto(self, id_producto: str) -> None`:**
- Delegar al repositorio: `self.repositorio.eliminar(id_producto)`.

**Pista basada en el ejemplo genérico:**

En el ejemplo del chef viste cómo se inyecta un colaborador:

```python
class ServicioPedidos:
    def __init__(self, notificador):
        self.notificador = notificador
```

**Tu tarea:** Adapta ese patrón. En lugar de un notificador, inyecta un `RepositorioInventario`. Implementa los seis métodos. Piensa: ¿qué método del repositorio necesitas en cada caso?

**Criterio de verificación:**

```bash
# Crear un repositorio EN MEMORIA falso para probar la DI
cat > /tmp/fake_repo.py << 'EOF'
from typing import List, Optional
from ports.repository import RepositorioInventario
from domain.models import Producto
from domain.exceptions import ProductoNoEncontradoError

class RepoMemoria(RepositorioInventario):
    def __init__(self): self._data = {}
    def guardar(self, p: Producto) -> None: self._data[p.id] = p
    def listar(self) -> List[Producto]: return list(self._data.values())
    def buscar_por_id(self, i: str) -> Optional[Producto]: return self._data.get(i)
    def eliminar(self, i: str) -> None:
        if i not in self._data: raise ProductoNoEncontradoError(i)
        del self._data[i]
EOF

# Usar el servicio con el repo falso
PYTHONPATH=/tmp python -c "
from fake_repo import RepoMemoria
from application.services import ServicioAuditoria
from domain.models import Producto

srv = ServicioAuditoria(RepoMemoria())
srv.registrar_producto(Producto('A1','Laptop',2,1500.0))
srv.registrar_producto(Producto('A2','Mouse',20,25.0))
print('Total:', srv.calcular_valor_total())
print('Faltantes:', srv.reportar_faltantes(minimo=5))
print('Auditoria:', srv.auditar('A1', 1))
"
```

### 9.4 Cierre de la Fase

```bash
git add application/services.py
git commit -m "feat(application): servicio de auditoría con DI del repositorio"
git push -u origin feature/application-usecases
# Abre PR siguiendo la plantilla
```

### 9.5 Preguntas de Autoevaluación

1. ¿Qué es la Inyección de Dependencias?
2. ¿Por qué el servicio no crea su propio repositorio?
3. ¿Qué ventaja tiene poder inyectar `RepoMemoria` en lugar de `RepositorioJSON`?
4. ¿Qué hace el método `auditar`?
5. ¿Por qué `calcular_valor_total` no está en el repositorio?

---

## 10. FASE 5: El CLI

**Rama:** `feature/cli-menu`

### 10.1 Objetivos

- Crear `adapters/cli.py` con `MenuCLI`.
- Crear `main.py` que ensamble todo.
- El CLI **no debe** contener lógica de negocio: solo llama al servicio.

### 10.2 ¿Qué es un Adaptador de Entrada?

Un **adaptador de entrada** es la interfaz por donde el usuario interactúa. Puede ser CLI, API REST, GUI, etc.

**Analogía:** El dominio es el hotel. El recepcionista es el adaptador CLI: traduce lo que pide el cliente al lenguaje del hotel.

### 10.3 Crear `adapters/cli.py`

**Lo que debes construir:**

Una clase `MenuCLI` con:

**Constructor `__init__(self, servicio: ServicioAuditoria)`:**
- Guardar `servicio` en `self.servicio`.

**Método `ejecutar(self) -> None`:**
- Bucle `while True`.
- Mostrar menú con `_mostrar_menu()`.
- Pedir opción con `input()`.
- `if/elif` para cada opción.
- Opción `"6"` → `break`.

**Método `_mostrar_menu(self) -> None`:**
- Imprimir las opciones: 1. Registrar, 2. Listar, 3. Auditar, 4. Faltantes, 5. Eliminar, 6. Salir.

**Método `_opcion_registrar(self) -> None`:**
- Pedir `id`, `nombre`, `cantidad`, `precio` con `input()`.
- Convertir `cantidad` a `int` y `precio` a `float`.
- Construir `Producto(...)`.
- Llamar `self.servicio.registrar_producto(producto)`.
- Envolver en `try/except`:
  - `ValueError` → mensaje amigable sobre números.
  - `ErrorDeDominio` → mostrar `e`.

**Método `_opcion_listar(self) -> None`:**
- Llamar `self.servicio.listar_inventario()`.
- Si está vacío, mostrar mensaje.
- Si no, formatear como tabla.
- Mostrar `self.servicio.calcular_valor_total()`.

**Método `_opcion_auditar(self) -> None`:**
- Pedir `id` y `cantidad_contada`.
- Llamar `self.servicio.auditar(id, cantidad)`.
- Mostrar `esperado`, `contado`, `diferencia`.
- `try/except` para `ValueError` y `ErrorDeDominio`.

**Método `_opcion_faltantes(self) -> None`:**
- Pedir `minimo`.
- Llamar `self.servicio.reportar_faltantes(minimo)`.
- Mostrar la lista o mensaje de "no hay faltantes".

**Método `_opcion_eliminar(self) -> None`:**
- Pedir `id`.
- Llamar `self.servicio.eliminar_producto(id)`.
- `try/except ErrorDeDominio`.

**Pista basada en el ejemplo genérico:**

En el ejemplo del notificador viste cómo se usa un servicio:

```python
srv = ServicioPedidos(NotificadorEmail())
srv.procesar(123)
```

**Tu tarea:** Adapta ese patrón. En lugar de `ServicioPedidos`, usa `ServicioAuditoria`. En lugar de `procesar`, llama a los métodos del servicio. **El CLI no sabe de JSON ni de reglas de negocio; solo llama al servicio.**

### 10.4 Crear `main.py`

**Lo que debes construir:**

Una función `main()` que:

1. Cree `RepositorioJSON("data/inventario.json")`.
2. Lo inyecte a `ServicioAuditoria(repositorio)`.
3. Inyecte el servicio a `MenuCLI(servicio)`.
4. Llame `menu.ejecutar()`.

Y un `if __name__ == "__main__": main()`.

**Pista basada en el ejemplo genérico:**

```python
def main():
    notificador = NotificadorEmail()
    servicio = ServicioPedidos(notificador)
    # ...
```

**Tu tarea:** Adapta ese patrón. Ensambla las piezas: repositorio → servicio → menú.

### 10.5 Ejercicios de Verificación

```bash
# Flujo completo interactivo
python main.py
# -> Registrar producto: A1, Laptop, 3, 1500
# -> Listar -> debe aparecer
# -> Auditar A1 con cantidad 1 -> diferencia 2
# -> Faltantes (mínimo 5) -> debe aparecer A1
# -> Eliminar A1 -> Listar -> vacío
# -> Salir

# Verificar el JSON generado
cat data/inventario.json
# Debe ser JSON válido con indentación

# Error controlado
python main.py
# -> Registrar producto con cantidad negativa
# -> Debe imprimir mensaje amigable, NO un traceback

# Arquitectura intacta
grep -R "print(" domain/ ports/ application/
# Debe estar vacío
```

### 10.6 Cierre de la Fase

```bash
git add adapters/cli.py main.py
git commit -m "feat(cli): menú interactivo y orquestación en main"
git push -u origin feature/cli-menu
# Abre PR siguiendo la plantilla
```

### 10.7 Preguntas de Autoevaluación

1. ¿Por qué el CLI no debe contener lógica de negocio?
2. ¿Qué hace `main.py`?
3. ¿Por qué `main.py` es el único que conoce todas las piezas?
4. ¿Qué pasaría si mañana quieres cambiar el CLI por una API REST?
5. ¿Por qué `domain/` no tiene `print`?

---

## 11. Checklist Final de Arquitectura

Antes de hacer el PR final a `main`, verifica:

| | Criterio | Comando |
|---|---|---|
| [ ] | `domain/` no importa infraestructura | `grep -R "import json\|open(" domain/` |
| [ ] | `ports/` no importa adaptadores | `grep -R "adapters" ports/` |
| [ ] | `application/` no instancia repositorios | `grep -R "RepositorioJSON(" application/` |
| [ ] | El servicio funciona con dos repos distintos | Prueba con `RepoMemoria` |
| [ ] | Todos los métodos abstractos implementados | `python -c "from adapters.json_repository import RepositorioJSON; RepositorioJSON('x.json')"` |
| [ ] | Errores de E/S traducidos a `ErrorDeDominio` | Prueba con JSON corrupto |
| [ ] | `main.py` solo ensambla | Revisión manual |
| [ ] | Los 5 PRs fueron aprobados | Revisión en GitHub |

### Entrega final

```bash
git checkout main
git pull origin main
git log --oneline --graph
# Debe mostrar los 5 merges de las fases
```

---

## 12. Glosario Completo

| Término | Significado | Ejemplo |
|---|---|---|
| **Entidad** | Objeto con identidad propia. | `Producto` |
| **Puerto** | Interfaz abstracta. | `RepositorioInventario` |
| **Adaptador** | Implementación concreta. | `RepositorioJSON` |
| **Caso de Uso** | Acción de negocio. | `registrar_producto` |
| **DI** | Pasar dependencias desde fuera. | `ServicioAuditoria(repositorio)` |
| **Acoplamiento** | Grado de dependencia. Objetivo: bajo. | — |
| **Cohesión** | Propósito único. Objetivo: alto. | — |
| **`@dataclass`** | Autogenera `__init__`, `__repr__`, `__eq__`. | `Producto` |
| **`@abstractmethod`** | Obliga a implementar. | `guardar`, `listar` |
| **`__post_init__`** | Hook tras `__init__`. | Validaciones en `Producto` |
| **Conventional Commits** | Estándar de commits. | `feat(domain): ...` |
| **Pull Request** | Solicitud de fusión. | PR de cada fase |
| **Squash & Merge** | Combina commits en uno. | Al aprobar PR |
| **Excepción** | Error que interrumpe. | `ProductoInvalidoError` |
| **Try/Except** | Manejo de errores. | En `RepositorioJSON` |
| **JSON** | Formato de texto. | `data/inventario.json` |
| **Herencia** | Una clase deriva de otra. | `RepositorioJSON(RepositorioInventario)` |
| **Polimorfismo** | Tratar objetos distintos igual. | `RepoMemoria` y `RepositorioJSON` |
| **Tipado** | Anotaciones de tipo. | `List[Producto]` |

---

## 13. Preguntas de Autoevaluación

Cuando termines, quiero que me expliques con tus palabras:

1. **¿Por qué `domain/` no debe saber que existe un archivo `.json`?**

2. **¿Qué ganaste al inyectar el repositorio al servicio en lugar de crearlo adentro?**

3. **¿Qué pasaría si mañana el jefe pide migrar de JSON a PostgreSQL? ¿Cuántos archivos tendrías que tocar?**

4. **¿Por qué no commiteamos directamente a `main`?**

5. **¿Qué diferencia hay entre un commit atómico y uno que mezcla varias cosas?**

### Ejercicio Final: Explica la Arquitectura

Escribe un documento de una página explicando:

1. Qué es la Arquitectura Hexagonal.
2. Cuáles son sus componentes.
3. Por qué el dominio no debe depender de la infraestructura.
4. Cómo la Inyección de Dependencias ayuda a testear.
5. Qué ventajas tiene este diseño sobre uno tradicional (todo en un solo archivo).

### Ejercicio Extra: Migrar a SQLite

Si quieres practicar más:

1. Crea `adapters/sqlite_repository.py`.
2. Implementa `RepositorioSQLite(RepositorioInventario)`.
3. Usa `sqlite3` en lugar de `json`.
4. Cambia `main.py` para que use `RepositorioSQLite`.
5. Verifica que **no tuviste que tocar** `domain/`, `ports/` ni `application/`.

**Esto demuestra el poder de la Arquitectura Hexagonal.**

---

## 14. Mensaje Final

No te frustres si en la Fase 3 el JSON te da problemas, ni si en la Fase 4 no entiendes por qué inyectar en vez de crear dentro. **Esa incomodidad es el aprendizaje.**

Cuando termines, quiero que me expliques con tus palabras:

1. ¿Por qué `domain/` no debe saber que existe un archivo `.json`?
2. ¿Qué ganaste al inyectar el repositorio al servicio en lugar de crearlo adentro?
3. ¿Qué pasaría si mañana el jefe pide migrar de JSON a PostgreSQL? ¿Cuántos archivos tendrías que tocar?
4. ¿Por qué no commiteamos directamente a `main`?
5. ¿Qué diferencia hay entre un commit atómico y uno que mezcla varias cosas?

> Si puedes responder esas cinco preguntas sin mirar este documento, habrás entendido la Arquitectura Hexagonal **y** el flujo profesional de trabajo.

---

## Autores

- **Rasiel Espinal** - Documento original
- **Roberto Luna** - Estudiante 
---

*Última actualización: 30 de sep del 2026*
