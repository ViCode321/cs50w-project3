# Project 3
La app cumple con los requisitos del project3, hay 2 usuarios creados el admin con contraseña admin, y victor123 con contraseña 1234, implemente el envío de mensaje de confirmación al cliente, es decir cuando un cliente hace una orden de pizzas (las cuales están clasificadas por orden de tamaño) estas se agregan al carrito y el admin puede ver dichas ordenes luego este puede presionar el botón para confirmar los pedidos, y esto envía un mensaje al correo electrónico del cliente.
El resto cumple con los requisitos del project3.

# Configuración del Entorno Virtual

Este proyecto utiliza un entorno virtual para gestionar las dependencias. A continuación, se describen los pasos para configurar un entorno virtual en diferentes sistemas operativos.

## Windows

1. Abre la línea de comandos (Command Prompt) o PowerShell.

2. Navega al directorio raíz de tu proyecto utilizando el comando `cd`:
```bash
cd ruta/a/tu/proyecto
```
3. Crea el entorno virtual en Windows
```bash
python -m venv myenv
```

4. Activa el entorno virtual en powershell
```bash
.\myenv\Scripts\Activate.ps1
```

## macOS y Linux

1. Crea el entorno virtual en macOS y Linux
```bash
python3 -m venv myenv
```
2. Activa el entorno virtual en macOS y Linux
```bash
source myenv/bin/activate
```

## Instalar los paquetes del proyecto

Puedes instalar todos los paquetes necesarios para el proyecto utilizando el siguiente comando:

```bash
pip install -r requirements.txt
```
