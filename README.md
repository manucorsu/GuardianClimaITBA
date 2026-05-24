# ☀️ GuardianClimaITBA
Grupo 121 ("")
- Matías Barreiro
- Lautaro Cavagna
- Manuel Corsunsky Gayá
- Enzo Creatore
<!--TODO: legajos?-->

## 1. Instrucciones de instalación
Nota: para todas las instrucciones de Linux y macOS el comando de Python se muestra como `python3`, en caso de usar pyenv o similar y que el comando sea otro (ej. `python`), cambiarlo por el que corresponda.

1. (opcional pero altamente recomendado) Crear y habilitar el entorno virtual
Para evitar conflictos entre las versiones de los paquetes requeridos que usamos nosotros y las que puedan estar instaladas globalmente en el sistema, hacemos uso de los entornos virtuales de Python (venv). Para configurar el entorno ejecutar:

### En Windows:
*Esto sirve para cmd, no PowerShell.*
```batch
python -m venv .venv :: Esperar a que termine, luego...
call .venv\scripts\activate
``