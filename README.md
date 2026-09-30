# Guia de Refactorizacion: Sistema de Auditoria de Inventario

> **Arquitectura Hexagonal (Ports & Adapters) con Python**
> Documento de trabajo y guia de aprendizaje paso a paso para el equipo de desarrollo.

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![Arquitectura](https://img.shields.io/badge/Arquitectura-Hexagonal-purple)]()
[![Estado](https://img.shields.io/badge/Estado-En%20Progreso-yellow)]()

---

## Tabla de Contenidos

- [0. Bienvenida y Contexto](#0-bienvenida-y-contexto)
- [1. Conceptos Transversales](#1-conceptos-transversales-leelos-antes-de-empezar)
- [2. Flujo de Trabajo Profesional con Git](#2-flujo-de-trabajo-profesional-con-git)
- [3. Configuracion Inicial del Repositorio](#3-configuracion-inicial-del-repositorio)
- [4. Fase 1 - `feature/domain-core`](#-fase-1---featuredomain-core)
- [5. Fase 2 - `feature/ports-interfaces`](#-fase-2---featureports-interfaces)
- [6. Fase 3 - `feature/infrastructure-adapter`](#-fase-3---featureinfrastructure-adapter)
- [7. Fase 4 - `feature/application-usecases`](#-fase-4---featureapplication-usecases)
- [8. Fase 5 - `feature/cli-menu`](#-fase-5---featurecli-menu)
- [9. Checklist Final](#9-checklist-final-de-arquitectura)
- [10. Glosario](#10-glosario-rapido-chuleta-de-consulta)
- [11. Mensaje Final del Mentor](#11-mensaje-final-del-mentor)

---

## 0. Bienvenida y Contexto

Hoy vas a construir, paso a paso, un **Sistema de Auditoria de Inventario** aplicando **Arquitectura Hexagonal**. Empezaras desde lo mas simple (clases y datos) y terminarias con un sistema profesional, testeable y desacoplado.

### Regla de oro del aprendiz

> Cada `# TODO:` que veas en este documento es tuyo. Nadie lo va a resolver por ti. Si te atascas, investiga, prueba, rompe el codigo y vuelve a intentarlo. Eso es ser ingeniero.

### Perfil de entrada / salida

| | Nivel |
|---|---|
| **Actual** | Sintaxis basica de Python: variables, `if/else`, listas, diccionarios, funciones e importacion de modulos. |
| **Objetivo** | Arquitectura Hexagonal, Inyeccion de Dependencias, Tipado Estricto (`typing`), Clases Abstractas (`abc.ABC`), Excepciones Personalizadas, Persistencia JSON aislada, y flujo profesional de Git con ramas, PRs y revisiones. |

---

## 1. Conceptos Transversales (Leelos antes de empezar)

Antes de entrar en las fases, necesitas entender **que es la Arquitectura Hexagonal** y **por que** la usamos.

### Analogia: El enchufe de pared

Imagina que tu casa es el **Dominio** (la logica de negocio: como se audita un inventario). Las paredes tienen **enchufes** (los **Puertos**), que son un estandar: "cualquier cosa que se enchufe aqui debe entregar 110V y 2 patas". No importa si enchufas una licuadora, un cargador o una TV; el enchufe no cambia. Los **Adaptadores** son los cables y clavijas especificas de cada dispositivo: uno para licuadora, otro para laptop, otro para la TV.

En software:

| Termino | Significado | En tu proyecto |
|---|---|---|
| **Dominio** | Reglas de negocio puras, sin saber de archivos ni consolas. | `Producto`, `Inventario`, `Auditoria` |
| **Puerto** | Contrato/interfaz que dice *que* se necesita, no *como*. | `RepositorioInventario` (interfaz) |
| **Adaptador** | Implementacion concreta de un puerto. | `RepositorioJSON`, `MenuCLI` |
| **Caso de Uso / Servicio** | Orquesta el dominio para cumplir una tarea. | `ServicioAuditoria` |
| **Inyeccion de Dependencias** | Pasarle a un objeto sus colaboradores desde fuera, no crearlos dentro. | `ServicioAuditoria(repositorio)` |

> **Regla hexagonal:** El dominio **nunca** debe importar `json`, `os`, `print`, ni nada de infraestructura. Solo conoce sus puertos.

---

## 2. Flujo de Trabajo Profesional con Git

Antes de tocar una sola linea de codigo, necesitas aprender a trabajar como se hace en un equipo profesional. El codigo no se escribe directamente sobre `main`.

### 2.1 Modelo de ramas: Trunk-Based simplificado

Usaremos una variante sencilla del flujo **GitHub Flow**:

```
main
 |
 |-- feature/domain-core
 |-- feature/ports-interfaces
 |-- feature/infrastructure-adapter
 |-- feature/application-usecases
 |-- feature/cli-menu
```

Reglas estrictas:

1. `main` es **intocable directamente**. Solo se actualiza via Pull Request aprobado.
2. Cada fase se desarrolla en su propia rama `feature/*`.
3. Una rama = una responsabilidad = un Pull Request.
4. Los commits son **atomicos** y siguen **Conventional Commits**.
5. Antes de pedir revision, debes correr tus pruebas manuales y verificar el checklist.

### 2.2 Convencion de nombres de ramas

| Tipo | Prefijo | Ejemplo |
|---|---|---|
| Nueva funcionalidad | `feature/` | `feature/domain-core` |
| Correccion de bug | `fix/` | `fix/json-corrupto` |
| Refactor | `refactor/` | `refactor/servicio-auditoria` |
| Documentacion | `docs/` | `docs/readme-inicial` |
| Tareas de mantenimiento | `chore/` | `chore/gitignore` |

### 2.3 Conventional Commits

El formato es:

```
<tipo>(<alcance>): <descripcion corta en imperativo>

[cuerpo opcional]

[footer opcional]
```

Tipos permitidos:

| Tipo | Uso |
|---|---|
| `feat` | Nueva funcionalidad |
| `fix` | Correccion de bug |
| `refactor` | Cambio de codigo que no agrega funcionalidad ni corrige bug |
| `docs` | Solo documentacion |
| `test` | Agregar o modificar pruebas |
| `chore` | Tareas de build, dependencias, configuracion |
| `style` | Formato (espacios, comas), sin cambios de logica |

Ejemplos correctos:

```
feat(domain): agregar entidad Producto con validaciones
fix(adapters): manejar JSONDecodeError en RepositorioJSON
refactor(application): inyectar repositorio por constructor
docs(readme): agregar guia de flujo Git
```

Ejemplos incorrectos:

```
cambios              <- vago, sin tipo ni alcance
Update models.py     <- sin tipo, mayuscula, sin contexto
arregle el bug       <- sin tipo, sin alcance, sin contexto
```

### 2.4 Ciclo de trabajo por fase (lo repetiras 5 veces)

```bash
# 1. Asegurarte de estar en main actualizado
git checkout main
git pull origin main

# 2. Crear la rama de la fase
git checkout -b feature/nombre-de-la-fase

# 3. Trabajar, haciendo commits atomicos conforme avanzas
git add <archivo-especifico>       # NUNCA uses 'git add .' a ciegas
git commit -m "feat(scope): descripcion clara"

# 4. Empujar la rama al remoto
git push -u origin feature/nombre-de-la-fase

# 5. Abrir el Pull Request desde GitHub/GitLab
#    - Titulo en formato Conventional Commit
#    - Descripcion con: que hiciste, como probarlo, checklist marcado
#    - Asignar revisor (tu mentor)
#    - NO hacer merge tu mismo

# 6. Esperar revision, aplicar cambios solicitados, empujar de nuevo
git add <archivo>
git commit -m "refactor(scope): aplicar feedback de revision"
git push

# 7. Una vez aprobado, el revisor hace merge (Squash & Merge)
# 8. Volver a main y actualizar
git checkout main
git pull origin main

# 9. Borrar la rama local
git branch -d feature/nombre-de-la-fase
```

### 2.5 Plantilla de Pull Request

Guarda este archivo como `.github/pull_request_template.md` en el repo:

```markdown
## Descripcion
<!-- Que hace este PR y por que -->

## Fase
<!-- Fase 1, 2, 3, 4 o 5 -->

## Tipo de cambio
- [ ] Nueva funcionalidad (feat)
- [ ] Correccion de bug (fix)
- [ ] Refactor (refactor)
- [ ] Documentacion (docs)

## Como probarlo
<!-- Comandos exactos que el revisor debe ejecutar -->

## Checklist
- [ ] Los commits siguen Conventional Commits
- [ ] El codigo no rompe la arquitectura hexagonal
- [ ] `grep -R "print(\|import json\|open(" domain/ ports/` devuelve vacio
- [ ] Las pruebas manuales de la fase pasan
- [ ] No hay archivos basura (`__pycache__`, `.env`, JSON de prueba) en el PR

## Capturas / Evidencia
<!-- Opcional: pega output de terminal -->
```

### 2.6 Reglas de convivencia en el repositorio

- **No hagas force push** sobre ramas de otros.
- **No mezcles dos fases en un mismo PR.**
- **No commitees** archivos de `data/*.json` (ya estan en `.gitignore`).
- **Revisa tu propio diff** antes de pedir revision: `git diff main...HEAD`.
- **Escribe commits en ingles o en espanol, pero se consistente** en todo el repo. Recomendacion: ingles para el codigo, espanol para el dominio del negocio si el equipo lo prefiere.

### 2.7 Ejercicio de verificacion del flujo

Antes de empezar la Fase 1, crea un PR de prueba:

```bash
git checkout -b docs/readme-inicial
# Edita este README (agrega tu nombre como autor)
git add README.md
git commit -m "docs(readme): agregar autor del proyecto"
git push -u origin docs/readme-inicial
# Abre el PR en GitHub, asignalo a tu mentor
```

**Criterio de aceptacion:**
- El PR se ve profesional, con titulo en Conventional Commits.
- El checklist esta marcado.
- El mentor puede hacer el merge sin pedir cambios.

---

## 3. Configuracion Inicial del Repositorio

Antes de la Fase 1, prepara el terreno.

```bash
# 1. Clona el repositorio o inicializalo
git clone <url-del-repo>
cd inventory_audit

# 2. Crea la estructura base de carpetas
mkdir -p domain ports adapters application data

# 3. Crea los __init__.py vacios para que Python trate las carpetas como paquetes
touch domain/__init__.py ports/__init__.py adapters/__init__.py application/__init__.py

# 4. Crea un .gitignore minimo
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
# Pega aqui el contenido de la seccion 2.5 en .github/pull_request_template.md

# 6. Primer commit en una rama (no en main directamente)
git checkout -b chore/estructura-inicial
git add .
git commit -m "chore: estructura inicial del proyecto hexagonal"
git push -u origin chore/estructura-inicial
# Abre PR, espera revision, merge
```

### Estructura final esperada

```
inventory_audit/
├── .github/
│   └── pull_request_template.md
├── domain/          # Reglas de negocio puras
├── ports/           # Contratos (interfaces)
├── adapters/        # Implementaciones concretas
├── application/     # Casos de uso / servicios
├── data/            # Archivos JSON de persistencia
├── main.py          # Punto de entrada
├── README.md        # Este documento
└── .gitignore
```

---

# FASE 1 - `feature/domain-core`

## 1.1 Concepto clave: Programacion Orientada a Objetos (POO) y `@dataclass`

### Analogia: El plano vs. la casa

Una **clase** es un **plano arquitectonico**. Define que tendra una casa (puertas, ventanas, color). Una **instancia** es una **casa real construida** a partir de ese plano. Puedes construir 100 casas (instancias) del mismo plano (clase), y cada una tendra sus propios valores.

Una **`@dataclass`** es como un **formulario pre-impreso**: Python te genera automaticamente el `__init__`, el `__repr__` y la comparacion entre objetos. Tu solo declaras los campos.

### Analogia: Las excepciones

Una **excepcion** es como una **alarma de incendios**. Cuando algo va mal (hay fuego), no sigues cocinando: suena la alarma y todo el mundo sabe que hay que atender una emergencia. En software, cuando un `Producto` tiene precio negativo, **lanzas** una excepcion en lugar de dejar pasar datos corruptos.

## 1.2 Objetivos de la Fase

- Crear la carpeta `domain/` con dos archivos: `models.py` y `exceptions.py`.
- Definir la entidad `Producto` como `@dataclass`.
- Definir excepciones personalizadas del dominio.
- **Regla estricta:** ningun `print`, ningun `import json`, ningun `open()` dentro de `domain/`.

## 1.3 Requisitos Tecnicos

### `domain/exceptions.py`

Define una excepcion base y al menos dos hijas.

```python
# domain/exceptions.py

class ErrorDeDominio(Exception):
    """Excepcion base para errores del dominio de inventario."""
    # TODO: Tu codigo aqui (pista: solo pasa, o define un __init__ si quieres mensaje)
    ...


class ProductoInvalidoError(ErrorDeDominio):
    # TODO: Tu codigo aqui
    ...


class ProductoNoEncontradoError(ErrorDeDominio):
    # TODO: Tu codigo aqui
    ...
```

### `domain/models.py`

```python
# domain/models.py
from dataclasses import dataclass
from domain.exceptions import ProductoInvalidoError


@dataclass
class Producto:
    id: str
    nombre: str
    cantidad: int
    precio_unitario: float

    def __post_init__(self) -> None:
        """
        Se ejecuta automaticamente al construir el objeto.
        Aqui debes VALIDAR las reglas de negocio.
        """
        # TODO: Si cantidad < 0 -> lanza ProductoInvalidoError
        # TODO: Si precio_unitario < 0 -> lanza ProductoInvalidoError
        # TODO: Si nombre esta vacio -> lanza ProductoInvalidoError
        ...
```

## 1.4 Ejercicios de Verificacion (ejecuta en terminal)

```bash
git checkout main
git pull origin main
git checkout -b feature/domain-core

# Prueba manual 1: producto valido
python -c "from domain.models import Producto; p = Producto('A1','Laptop',5,1500.0); print(p)"

# Prueba manual 2: producto invalido (debe lanzar tu excepcion)
python -c "from domain.models import Producto; Producto('A2','Mouse',-3,25.0)"

# Prueba manual 3: verifica que NO existe acoplamiento a infraestructura
grep -R "import json\|open(\|print(" domain/
# Debe devolver vacio. Si devuelve algo, estas violando la arquitectura!
```

### Criterio de aceptacion

- `Producto` se construye sin errores con datos validos.
- Se lanza `ProductoInvalidoError` con datos invalidos.
- `grep` de la prueba 3 no devuelve nada.

### Cierre de la fase (Pull Request)

```bash
git add domain/exceptions.py domain/models.py
git commit -m "feat(domain): agregar entidad Producto y excepciones de dominio"
git push -u origin feature/domain-core

# Abre Pull Request en GitHub:
# - Titulo: feat(domain): entidad Producto y excepciones de dominio
# - Descripcion: usa la plantilla del PR
# - Asigna a tu mentor
# - NO hagas merge tu mismo
```

---

# FASE 2 - `feature/ports-interfaces`

## 2.1 Concepto clave: Clases Abstractas (`abc.ABC`) y Contratos

### Analogia: La oferta de trabajo

Cuando una empresa publica una vacante, describe **que** debe hacer el empleado ("gestionar inventario, reportar faltantes"), pero **no dice como**. Cualquier persona que cumpla esos requisitos puede ser contratada. Eso es un **contrato** (puerto).

En Python, una **clase abstracta** es ese contrato: define **metodos sin cuerpo** (marcados con `@abstractmethod`). Nadie puede instanciar la clase abstracta directamente; solo sus **hijas** (adaptadores) pueden implementarla.

### Analogia: El estandar USB

El puerto USB define la forma, no el dispositivo. Tu `RepositorioInventario` (puerto) dice: "quien me implemente debe saber `guardar`, `listar`, `buscar_por_id` y `eliminar`". No importa si es JSON, SQL o memoria.

## 2.2 Objetivos de la Fase

- Crear `ports/repository.py` con una clase abstracta `RepositorioInventario`.
- Definir metodos abstractos con **tipado estricto** (`typing`).
- **No** implementar logica: solo firmas.

## 2.3 Requisitos Tecnicos

```python
# ports/repository.py
from abc import ABC, abstractmethod
from typing import List, Optional
from domain.models import Producto


class RepositorioInventario(ABC):
    """Puerto: contrato de persistencia para productos de inventario."""

    @abstractmethod
    def guardar(self, producto: Producto) -> None:
        """Persiste un producto (crea o actualiza)."""
        # TODO: solo pass
        ...

    @abstractmethod
    def listar(self) -> List[Producto]:
        """Devuelve todos los productos almacenados."""
        # TODO: solo pass
        ...

    @abstractmethod
    def buscar_por_id(self, producto_id: str) -> Optional[Producto]:
        """Devuelve el producto o None si no existe."""
        # TODO: solo pass
        ...

    @abstractmethod
    def eliminar(self, producto_id: str) -> None:
        """Elimina un producto por su id."""
        # TODO: solo pass
        ...
```

> **Reto extra (opcional):** Crea tambien `ports/notificador.py` como puerto abstracto, con un metodo `notificar(mensaje: str) -> None`. Lo usaras en la Fase 4.

## 2.4 Ejercicios de Verificacion

```bash
git checkout main
git pull origin main
git checkout -b feature/ports-interfaces

# Prueba 1: NO se puede instanciar una clase abstracta
python -c "from ports.repository import RepositorioInventario; RepositorioInventario()"
# Debe lanzar TypeError: Can't instantiate abstract class...

# Prueba 2: verifica que el puerto NO importa infraestructura
grep -R "import json\|open(" ports/
# Debe estar vacio.
```

### Criterio de aceptacion

- `TypeError` al intentar instanciar `RepositorioInventario`.
- El puerto solo importa `abc`, `typing` y `domain.models`.

### Cierre de la fase

```bash
git add ports/repository.py
git commit -m "feat(ports): contrato RepositorioInventario con metodos abstractos"
git push -u origin feature/ports-interfaces
# Abre PR siguiendo la plantilla
```

---

# FASE 3 - `feature/infrastructure-adapter`

## 3.1 Concepto clave: Adaptadores de Persistencia + Manejo de JSON + `try/except`

### Analogia: El archivador fisico

Tu puerto dijo: "necesito guardar productos". El adaptador JSON es como un **archivero metalico**: los productos se guardan en carpetas (el archivo `.json`). Cada vez que quieres agregar uno, abres el cajon (`open`), lo lees (`json.load`), metes el nuevo (append), y cierras (`json.dump`).

### Analogia: `try/except` como cinturon de seguridad

Cuando conduces, no asumes que nunca habra un choque: llevas cinturon. En codigo, **no asumas** que el archivo JSON siempre existira o que siempre sera valido. Envuelve las operaciones riesgosas en `try/except` y traduce el error tecnico (`FileNotFoundError`, `json.JSONDecodeError`) a un error de dominio.

## 3.2 Objetivos de la Fase

- Crear `adapters/json_repository.py`.
- Implementar la clase `RepositorioJSON(RepositorioInventario)`.
- Manejar: archivo inexistente, JSON corrupto, permisos denegados.
- **No** romper el contrato: debe heredar y sobrescribir **todos** los metodos abstractos.

## 3.3 Requisitos Tecnicos

```python
# adapters/json_repository.py
import json
import os
from typing import List, Optional
from domain.models import Producto
from domain.exceptions import ErrorDeDominio
from ports.repository import RepositorioInventario


class RepositorioJSON(RepositorioInventario):

    def __init__(self, ruta_archivo: str) -> None:
        self.ruta = ruta_archivo
        # TODO: si el archivo no existe, crealo con una lista vacia []
        ...

    def _leer_todos(self) -> List[dict]:
        """
        Metodo privado (con _) que devuelve la lista cruda del JSON.
        Envuelvelo en try/except.
        """
        # TODO: abrir archivo, json.load, retornar lista
        # TODO: capturar FileNotFoundError -> retornar []
        # TODO: capturar json.JSONDecodeError -> lanzar ErrorDeDominio("JSON corrupto")
        ...

    def _escribir_todos(self, datos: List[dict]) -> None:
        # TODO: abrir archivo en modo 'w', json.dump con indent=4
        # TODO: capturar PermissionError -> lanzar ErrorDeDominio("Sin permisos")
        ...

    def guardar(self, producto: Producto) -> None:
        # TODO: leer, buscar por id; si existe -> actualizar; si no -> append; escribir
        ...

    def listar(self) -> List[Producto]:
        # TODO: leer, convertir cada dict a Producto, retornar lista
        ...

    def buscar_por_id(self, producto_id: str) -> Optional[Producto]:
        # TODO: iterar y retornar el Producto o None
        ...

    def eliminar(self, producto_id: str) -> None:
        # TODO: filtrar la lista, escribir de nuevo
        # TODO: si no existe -> lanzar ProductoNoEncontradoError
        ...
```

## 3.4 Ejercicios de Verificacion

```bash
git checkout main
git pull origin main
git checkout -b feature/infrastructure-adapter

# Prueba 1: guardar y listar
python -c "
from adapters.json_repository import RepositorioJSON
from domain.models import Producto
r = RepositorioJSON('data/test.json')
r.guardar(Producto('P1','Teclado',10,25.0))
r.guardar(Producto('P2','Monitor',3,300.0))
print(r.listar())
"

# Prueba 2: buscar por id
python -c "
from adapters.json_repository import RepositorioJSON
r = RepositorioJSON('data/test.json')
print(r.buscar_por_id('P1'))
print(r.buscar_por_id('NOEXISTE'))  # Debe imprimir None
"

# Prueba 3: eliminar
python -c "
from adapters.json_repository import RepositorioJSON
r = RepositorioJSON('data/test.json')
r.eliminar('P2')
print(r.listar())
"

# Prueba 4: JSON corrupto
echo "esto no es json" > data/test.json
python -c "
from adapters.json_repository import RepositorioJSON
r = RepositorioJSON('data/test.json')
r.listar()  # Debe lanzar tu ErrorDeDominio
"
```

### Criterio de aceptacion

- Todas las operaciones CRUD funcionan.
- JSON corrupto lanza `ErrorDeDominio`, no `JSONDecodeError` crudo.
- El adaptador **hereda** de `RepositorioInventario` (verificalo con `isinstance`).

### Cierre de la fase

```bash
git add adapters/json_repository.py
git commit -m "feat(adapters): repositorio JSON con manejo de errores de E/S"
git push -u origin feature/infrastructure-adapter
# Abre PR siguiendo la plantilla
```

---

# FASE 4 - `feature/application-usecases`

## 4.1 Concepto clave: Servicios de Aplicacion + Inyeccion de Dependencias (DI)

### Analogia: El chef y su proveedor

Un **chef** (Servicio) sabe cocinar, pero **no cultiva sus propios vegetales**. Alguien se los entrega: el **proveedor** (Repositorio). El chef no sabe si el proveedor trae del campo, de un invernadero o de otro pais; solo sabe que le entregara los ingredientes segun un contrato.

Eso es **Inyeccion de Dependencias**: el `ServicioAuditoria` **no crea** su repositorio con `RepositorioJSON()`. Alguien se lo pasa por el constructor:

```python
servicio = ServicioAuditoria(repositorio=RepositorioJSON("data/inv.json"))
```

**Ventaja:** en pruebas, puedes inyectar un `RepositorioEnMemoria` falso sin tocar disco. **El dominio no se contamina.**

## 4.2 Objetivos de la Fase

- Crear `application/services.py` con la clase `ServicioAuditoria`.
- Inyectar el repositorio (tipo `RepositorioInventario`) por constructor.
- Implementar operaciones de negocio: `registrar_producto`, `auditar`, `reportar_faltantes`, `eliminar_producto`.

## 4.3 Requisitos Tecnicos

```python
# application/services.py
from typing import List, Dict
from domain.models import Producto
from domain.exceptions import ProductoNoEncontradoError
from ports.repository import RepositorioInventario


class ServicioAuditoria:

    def __init__(self, repositorio: RepositorioInventario) -> None:
        # TODO: guarda el repositorio en self (inyeccion de dependencias!)
        ...

    def registrar_producto(self, producto: Producto) -> None:
        # TODO: delegar al repositorio
        ...

    def listar_inventario(self) -> List[Producto]:
        # TODO: delegar al repositorio
        ...

    def calcular_valor_total(self) -> float:
        # TODO: sumar cantidad * precio_unitario de cada producto
        ...

    def reportar_faltantes(self, minimo: int = 5) -> List[Producto]:
        """
        Devuelve los productos cuya cantidad sea menor al minimo.
        """
        # TODO: filtrar la lista
        ...

    def auditar(self, id_producto: str, cantidad_contada: int) -> Dict[str, int]:
        """
        Compara la cantidad contada en bodega contra la registrada.
        Devuelve un dict: {'esperado': X, 'contado': Y, 'diferencia': X-Y}.
        """
        # TODO: buscar producto, si no existe -> ProductoNoEncontradoError
        # TODO: construir y retornar el dict
        ...
```

## 4.4 Ejercicios de Verificacion

```bash
git checkout main
git pull origin main
git checkout -b feature/application-usecases

# Prueba 1: crear un repositorio EN MEMORIA falso (sin tocar JSON)
# para demostrar que la DI funciona.
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

# Prueba 2: usar el servicio con el repo falso
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

### Criterio de aceptacion

- El servicio funciona con `RepositorioJSON` **y** con `RepoMemoria` sin cambiar una sola linea.
- `auditar` retorna un dict con las 3 llaves.
- `ProductoNoEncontradoError` se lanza cuando aplica.

### Cierre de la fase

```bash
git add application/services.py
git commit -m "feat(application): servicio de auditoria con DI del repositorio"
git push -u origin feature/application-usecases
# Abre PR siguiendo la plantilla
```

---

# FASE 5 - `feature/cli-menu`

## 5.1 Concepto clave: Adaptador de Entrada (CLI) + Orquestacion en `main.py`

### Analogia: El recepcionista del hotel

El **dominio** es el hotel (habitaciones, servicios, reglas). El **recepcionista** es el adaptador CLI: traduce lo que pide el cliente ("quiero una habitacion") al lenguaje del hotel ("reserva la habitacion 302"). El cliente no habla con el gerente; habla con el recepcionista.

`main.py` es el **director de orquesta**: no toca instrumentos, pero decide **quien toca y cuando**. Su unica mision es **ensamblar** las piezas: crear el repositorio, inyectarlo al servicio y entregarle el servicio al menu.

## 5.2 Objetivos de la Fase

- Crear `adapters/cli.py` con la clase `MenuCLI`.
- Crear `main.py` que ensamble todo.
- El CLI **no debe** contener logica de negocio: solo llama al servicio.

## 5.3 Requisitos Tecnicos

```python
# adapters/cli.py
from application.services import ServicioAuditoria
from domain.models import Producto
from domain.exceptions import ErrorDeDominio


class MenuCLI:

    def __init__(self, servicio: ServicioAuditoria) -> None:
        # TODO: guarda el servicio en self
        ...

    def ejecutar(self) -> None:
        """Bucle principal del menu."""
        while True:
            self._mostrar_menu()
            opcion = input("Elige una opcion: ").strip()
            # TODO: if/elif para cada opcion
            # TODO: opcion "6" -> break
            ...

    def _mostrar_menu(self) -> None:
        # TODO: imprimir las opciones (1. Registrar, 2. Listar, ...)
        ...

    def _opcion_registrar(self) -> None:
        # TODO: pedir datos con input(), construir Producto, llamar servicio
        # TODO: envolver en try/except ErrorDeDominio para mostrar mensajes amigables
        ...

    def _opcion_listar(self) -> None:
        # TODO: servicio.listar_inventario(), formatear tabla
        ...

    def _opcion_auditar(self) -> None:
        # TODO: pedir id y cantidad contada, llamar servicio.auditar()
        ...

    def _opcion_faltantes(self) -> None:
        # TODO: servicio.reportar_faltantes()
        ...

    def _opcion_eliminar(self) -> None:
        # TODO: pedir id, llamar servicio
        ...
```

```python
# main.py
from adapters.json_repository import RepositorioJSON
from adapters.cli import MenuCLI
from application.services import ServicioAuditoria


def main() -> None:
    # TODO: 1) Crear el repositorio apuntando a 'data/inventario.json'
    # TODO: 2) Inyectarlo al servicio
    # TODO: 3) Inyectar el servicio al menu
    # TODO: 4) menu.ejecutar()
    ...


if __name__ == "__main__":
    main()
```

## 5.4 Ejercicios de Verificacion

```bash
git checkout main
git pull origin main
git checkout -b feature/cli-menu

# Prueba 1: flujo completo interactivo
python main.py
# -> Registrar producto: A1, Laptop, 3, 1500
# -> Listar -> debe aparecer
# -> Auditar A1 con cantidad 1 -> debe mostrar diferencia 2
# -> Faltantes (minimo 5) -> debe aparecer A1
# -> Eliminar A1 -> Listar -> vacio
# -> Salir

# Prueba 2: verificar el JSON generado
cat data/inventario.json
# Debe ser JSON valido con indentacion.

# Prueba 3: error controlado
python main.py
# -> Registrar producto con cantidad negativa
# -> Debe imprimir un mensaje amigable, NO un traceback.

# Prueba 4: arquitectura intacta
grep -R "print(" domain/ ports/ application/
# Debe estar vacio. La impresion en consola SOLO vive en adapters/cli.py y main.py.
```

### Criterio de aceptacion

- El menu ejecuta las 6 opciones sin errores.
- Los errores de dominio se muestran como mensajes amigables.
- El dominio y los puertos **no** tienen `print` ni `input`.

### Cierre de la fase

```bash
git add adapters/cli.py main.py
git commit -m "feat(cli): menu interactivo y orquestacion en main"
git push -u origin feature/cli-menu
# Abre PR siguiendo la plantilla
```

---

## 9. Checklist Final de Arquitectura

Antes de hacer el PR final a `main`, verifica:

| | Criterio | Comando de verificacion |
|---|---|---|
| [ ] | `domain/` no importa infraestructura | `grep -R "import json\|open(" domain/` |
| [ ] | `ports/` no importa adaptadores | `grep -R "adapters" ports/` |
| [ ] | `application/` no instancia repositorios concretos | `grep -R "RepositorioJSON(" application/` |
| [ ] | El servicio funciona con dos repos distintos | Prueba con `RepoMemoria` |
| [ ] | Todos los metodos abstractos estan implementados | `python -c "from adapters.json_repository import RepositorioJSON; RepositorioJSON('x.json')"` |
| [ ] | Errores de E/S se traducen a `ErrorDeDominio` | Prueba con JSON corrupto |
| [ ] | `main.py` solo ensambla, no tiene logica de negocio | Revision manual |
| [ ] | Los 5 PRs fueron aprobados y mergeados | Revision en GitHub |

### Entrega final

```bash
git checkout main
git pull origin main
git log --oneline --graph
# Debe mostrar los 5 merges de las fases
```

---

## 10. Glosario Rapido (Chuleta de Consulta)

| Termino | Significado en 1 linea |
|---|---|
| **Entidad** | Objeto con identidad propia (`Producto`). |
| **DTO** | Objeto para transportar datos entre capas. |
| **Puerto** | Interfaz abstracta que define un contrato. |
| **Adaptador** | Implementacion concreta de un puerto. |
| **Caso de Uso** | Accion de negocio (`registrar`, `auditar`). |
| **DI** | Pasar dependencias desde fuera (Dependency Injection). |
| **Acoplamiento** | Grado en que un modulo depende de otro. Objetivo: **bajo**. |
| **Cohesion** | Grado en que un modulo tiene un proposito unico. Objetivo: **alto**. |
| **`@dataclass`** | Decorador que autogenera `__init__`, `__repr__`, `__eq__`. |
| **`@abstractmethod`** | Obliga a las subclases a implementar el metodo. |
| **`__post_init__`** | Hook de `@dataclass` que corre tras el `__init__`. |
| **Conventional Commits** | Estandar de mensajes de commit: `tipo(alcance): descripcion`. |
| **Pull Request (PR)** | Solicitud de fusion de una rama hacia `main` con revision previa. |
| **Squash & Merge** | Estrategia de merge que combina todos los commits del PR en uno. |

---

## 11. Mensaje Final

No te frustres si en la Fase 3 el JSON te da problemas, ni si en la Fase 4 no entiendes por que inyectar en vez de crear dentro. **Esa incomodidad es el aprendizaje**.

Cuando termines, quiero que me expliques con tus palabras:

1. Por que `domain/` no debe saber que existe un archivo `.json`?
2. Que ganaste al inyectar el repositorio al servicio en lugar de crearlo adentro?
3. Que pasaria si manana el jefe pide migrar de JSON a PostgreSQL? Cuantos archivos tendrias que tocar?
4. Por que no commiteamos directamente a `main`?
5. Que diferencia hay entre un commit atomico y un commit que mezcla varias cosas?

> Si puedes responder esas cinco preguntas sin mirar el documento, habras entendido la Arquitectura Hexagonal **y** el flujo profesional de trabajo.

---


## Autors
- Roberto Luna

