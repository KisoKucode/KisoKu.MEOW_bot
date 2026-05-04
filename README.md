# 🐾 KisoKu.MEOW_bot

!Discord
!Python
!PostgreSQL

¡Bienvenido a **KisoKu.MEOW_bot**! Un bot multifuncional diseñado para transformar tu servidor de Discord en un centro de entretenimiento interactivo.  

🎯 **Enfoque principal:** Aunque ofrece herramientas de utilidad, el alma del bot es su **sistema de economía y apuestas**, junto con un robusto sistema de niveles y roles. ¡Prepárate para la diversión y la competencia!

---

## 🚀 Características Principales

- Aquí un vistazo a lo que KisoKu.MEOW_bot puede ofrecer, organizado por módulos:

### 🎉 General
- **Eventos de Bienvenida y Despedida:** Saluda automáticamente a nuevos miembros y despide a los que se van en el canal configurado.
- **Comandos Básicos:** `/saludo`, `/despedida`, `/hora`, `/chiste`.
- **Ayuda Interactiva:** El comando `/ayuda` muestra una lista organizada de todos los comandos disponibles.

### 🛠️ Utilidades
- **Información del Servidor:** Obtén detalles del servidor con `/server`.
- **Información de Usuario:** Consulta tu perfil con `/usuario` y tu avatar con `/avatar`.
- **Gestión de Miembros y Roles:** Muestra el número de miembros (`/miembros`), información de roles (`/rolinfo <rol>`) y lista de canales (`/canales`).
- **Comunicación:** Envía mensajes privados a otros usuarios (`/mensajeprivado <usuario> <mensaje>`).
- **Interacción:** Crea encuestas rápidas (`/encuesta <pregunta>`) y envía sugerencias (`/sugerencia <texto>`).

### 💰 Economía y Casino
- **Sistema de Monedas:** Gana, gasta y gestiona tu saldo.
- **Recompensas Diarias:** Recoge monedas gratis una vez al día con `/diario`.
- **Consulta de Saldo:** Revisa tus fondos con `/saldo`.
- **Clasificación Global:** Compite por ser el más rico en el servidor con `/clasificacion`.
- **Juegos de Casino:**
    - **Tragamonedas:** Prueba tu suerte con `/tragamonedas <apuesta>`.
    - **Cara o Cruz:** Apuesta en un clásico con `/moneda <apuesta> <cara|cruz>`.
    - **Blackjack:** Juega contra el crupier con `/blackjack <apuesta>`.
    - **Video Poker:** Forma la mejor mano de póker con `/poker <apuesta>`.
    - **Apuesta de Dados:** Predice la suma de dos dados con `/dados_apuesta <apuesta> <bajo|siete|alto>`.
    - **Ruleta:** Apuesta a números, colores o paridad con `/ruleta numero|color|paridad`.
    - **Carreras de Animales:** Apuesta por tu corredor favorito con `/carrera <apuesta> <corredor>`.
    - **Ahorcado:** Un clásico juego de adivinar palabras.

### 📈 Sistema de Niveles
- **Experiencia por Actividad:** Gana puntos de experiencia (XP) simplemente chateando en el servidor.
- **Subida de Nivel:** Desbloquea nuevos niveles y demuestra tu dedicación a la comunidad.

### 🛒 Tienda de Roles
- **Roles Exclusivos:** Canjea tus monedas por roles únicos y distintivos en el servidor.
- **Comandos:** Explora los roles disponibles con `/tienda` y compra con `/comprar <rol>`.

### 💖 Módulos de Romance
- **Poemas Automáticos:** El bot envía poemas románticos periódicamente al canal general, acompañados de arte ASCII.
- **Comandos de Poesía:** Dedica versos con `/poema` y añade tus propias creaciones a la base de datos con `/agregar_poema <texto>`.

### 🖥️ Panel de Monitoreo (Status)
- **Estado del Bot:** Monitorea la latencia del bot y el estado general del servidor en tiempo real.

---

## 🛠️ Instalación y Configuración (Linux)
Sigue estos pasos para desplegar el bot:

### 1. Prerrequisitos
- Python 3.8 o superior.
- PostgreSQL instalado y en ejecución.

### 2. Clonar el Repositorio
```bash
git clone <URL_DEL_REPOSITORIO>
cd KisoKu.MEOW_bot
```

### 3. Configurar el Entorno Virtual
Es una buena práctica usar un entorno virtual para aislar las dependencias del proyecto.
```bash
# Crear el entorno virtual
python3 -m venv venv

# Activar el entorno
source venv/bin/activate

> **Nota:** El comando anterior es para shells como `bash` o `zsh`. Si usas una shell diferente como `fish`, el comando correcto es `source venv/bin/activate.fish`.
```

### 4. Instalar Dependencias
Instala todas las librerías de Python necesarias con el archivo `requirements.txt`.
```bash
pip install -r requirements.txt
```

### 5. Configurar la Base de Datos
El bot usa PostgreSQL. Necesitas crear una base de datos y un usuario para él.
```sql
-- Conéctate a psql como superusuario
sudo -u postgres psql

-- Ejecuta los siguientes comandos
CREATE DATABASE meow_bot_db;
CREATE USER meow_bot_user WITH PASSWORD 'tu_contraseña_segura';
GRANT ALL PRIVILEGES ON DATABASE meow_bot_db TO meow_bot_user;
\q
```

### 6. Crear el archivo `.env`
Este archivo contendrá todas tus claves secretas. Crea un archivo llamado `.env` en la raíz del proyecto y añade lo siguiente, reemplazando los valores:

```env
# --- Discord ---
DISCORD_TOKEN=AQUI_VA_EL_TOKEN_DE_TU_BOT
BOT_NAME="MEOW Bot"

# --- Canales (Opcional, usará los defaults si no se especifica) ---
GENERAL_CHANNEL="general"
SUGGESTIONS_CHANNEL="sugerencias"

# --- Base de Datos ---
DB_HOST=localhost
DB_NAME=meow_bot_db
DB_USER=meow_bot_user
DB_PASSWORD=tu_contraseña_segura
DB_PORT=5432 # Puerto de PostgreSQL, por defecto 5432

# --- Casino (Opcional) ---
DAILY_AMOUNT=150
```

### 7. Iniciar el Bot
Una vez que todo esté configurado, puedes iniciar el bot.
```bash
python3 index.py
```

---

## Progreso de desarrollo

- **Evento de bienvenida:**  
  Cuando un usuario entra al servidor, el bot lo saluda automáticamente en el canal general.

- **Evento de despedida:**  
  Cuando un usuario sale del servidor, el bot envía una despedida automática.

- **Lista de comandos /ayuda:**  
  El comando `/ayuda` muestra todos los comandos disponibles para facilitar el uso del bot.

---

## Comandos implementados

```
/saludo - Saluda al usuario
/despedida - Se despide del usuario
/hora - Muestra la hora actual
/chiste - Cuenta un chiste
/usuario - Muestra tu información
/dado - Lanza un dado
/server - Información del servidor       
/repetir <mensaje> - Repite tu mensaje
/encuesta <pregunta> - Encuesta rápida
/avatar - Muestra tu avatar
/miembros - Muestra el número de miembros y cuántos están en línea
/rolinfo <rol> - Muestra información sobre un rol
/canales - Lista todos los canales del servidor
/invitar - Envía el enlace de invitación del servidor
/mensajeprivado <usuario> <mensaje> - Envía un mensaje privado a un usuario
/sugerencia <texto> - Envía una sugerencia
```

---

## Eventos automáticos

- **Bienvenida:**  
  El bot saluda automáticamente a los nuevos miembros y les desea diversión en el servidor.

- **Despedida:**  
  El bot despide automáticamente a los usuarios que salen del servidor.

---

## Ideas para comandos y mini juegos

### Comandos sociales
- `/kiss <usuario>`: Envía un mensaje de beso entre usuarios con frases divertidas y estilo anime.

### Mini juegos
- **Horcado:**  
  Juego de adivinar palabras correctas.

- **Rol de vida y trabajo:**  
  Sistema de trabajos, coches y banco virtual.

- **Dados:**  
  Apuesta, saca el número mayor y gana.

- **Cartas 21:**  
  Saca el número más alto y gana.

---

---

## Contribuciones

¡Todas las ideas y sugerencias son bienvenidas!  
Puedes comentar tus ideas en este archivo para seguir mejorando el bot.

---

## Autor

Desarrollado por Daniel (KisoKu.MEOW)

## Mensaje de inicio

Cuando el bot se conecta, muestra en consola:  
`Bot conectado como {bot.user}`

---

## Contribuciones

¡Todas las ideas y sugerencias son bienvenidas!  
Puedes comentar tus ideas en este archivo para seguir mejorando el bot.

---

## Autor

Desarrollado por Daniel (KisoKu.MEOW)
