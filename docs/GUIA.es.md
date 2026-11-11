# Guía de instalación y uso

Cómo instalar el skill `html-game-ui-design` en Claude y sacarle buenos resultados. [English version](GUIDE.md).

## Contenido

- [¿Qué instalación necesito?](#qué-instalación-necesito)
- [Apps de Claude: web, escritorio y Cowork](#apps-de-claude-web-escritorio-y-cowork)
- [Claude Code: instalar como plugin](#claude-code-instalar-como-plugin)
- [Claude Code: instalar como skill suelto](#claude-code-instalar-como-skill-suelto)
- [Otros agentes](#otros-agentes)
- [Cómo usar el skill](#cómo-usar-el-skill)
- [Ejecutar el detector por tu cuenta](#ejecutar-el-detector-por-tu-cuenta)
- [Actualizar y desinstalar](#actualizar-y-desinstalar)
- [Solución de problemas](#solución-de-problemas)

## ¿Qué instalación necesito?

| Usas | Instálalo así |
|---|---|
| Claude en el navegador, la app de escritorio o Cowork | Sube el ZIP ([apps de Claude](#apps-de-claude-web-escritorio-y-cowork)) |
| Claude Code, y quieres actualizar con un comando | Plugin ([como plugin](#claude-code-instalar-como-plugin)) |
| Claude Code, y quieres leer o editar los archivos del skill | Skill suelto ([como skill suelto](#claude-code-instalar-como-skill-suelto)) |
| Otro agente compatible con Agent Skills | Copia la carpeta ([otros agentes](#otros-agentes)) |

Los skills activados en tu cuenta de Claude también se cargan en las versiones recientes de Claude Code cuando inicias sesión con la misma cuenta, así que subir el ZIP una vez puede cubrir ambos.

## Apps de Claude: web, escritorio y Cowork

**Antes de empezar.** Los skills necesitan que la ejecución de código esté activada. En planes individuales, abre Settings > Capabilities y activa "Code execution and file creation". En planes Team y Enterprise lo controla un propietario en Organization settings > Plugins & skills; si no puedes subir un skill, pídele que revise que los skills estén habilitados ahí.

**Pasos**

1. Descarga [`dist/html-game-ui-design.zip`](../dist/html-game-ui-design.zip) de este repositorio. En su página de GitHub usa el botón de descarga; no lo descomprimas.
2. En Claude, abre **Customize > Skills** (`claude.ai/customize/skills`).
3. Haz clic en el botón **+** y luego en **Create skill**.
4. Elige **Upload a skill** y selecciona el ZIP.
5. El skill aparece en tu lista. Comprueba que su interruptor esté encendido.

Para compartirlo con tu equipo en un plan Team o Enterprise, abre el menú de tres puntos del skill y elige **Share**.

**Si armas el ZIP por tu cuenta**, el archivo debe contener la carpeta del skill en su nivel superior, y el nombre de la carpeta debe coincidir con el nombre del skill:

```
html-game-ui-design.zip
└── html-game-ui-design/
    ├── SKILL.md
    ├── references/
    └── scripts/
```

Desde la raíz del repositorio:

```bash
# macOS y Linux
cd skills && zip -r ../html-game-ui-design.zip html-game-ui-design -x "*/evals/*" "*/__pycache__/*"
```

```powershell
# Windows 10 o posterior (PowerShell o cmd)
tar -a -c -f html-game-ui-design.zip -C skills html-game-ui-design
```

## Claude Code: instalar como plugin

Este repositorio es también un marketplace de plugins con un plugin, `game-ui-anti-slop`. Desde una terminal:

```bash
claude plugin marketplace add angel-gmz/ui-anti-ai-slop
claude plugin install game-ui-anti-slop@ui-anti-ai-slop
```

Comprueba que quedó instalado:

```bash
claude plugin details game-ui-anti-slop
```

El inventario de componentes debe listar un skill, `html-game-ui-design`. Si Claude Code ya estaba abierto, ejecuta `/reload-plugins` en esa sesión o reinícialo.

También puedes hacerlo desde dentro de una sesión con el comando `/plugin`, que abre un panel para añadir marketplaces e instalar plugins.

Instalado así, el nombre completo del skill es `/game-ui-anti-slop:html-game-ui-design`.

## Claude Code: instalar como skill suelto

Úsalo cuando quieras tener los archivos a la mano para leerlos y modificarlos.

**Para todos los proyectos de tu máquina** (skill personal):

```bash
# macOS y Linux
git clone https://github.com/angel-gmz/ui-anti-ai-slop.git
mkdir -p ~/.claude/skills
cp -r ui-anti-ai-slop/skills/html-game-ui-design ~/.claude/skills/
```

```powershell
# Windows PowerShell
git clone https://github.com/angel-gmz/ui-anti-ai-slop.git
New-Item -ItemType Directory -Force "$env:USERPROFILE\.claude\skills" | Out-Null
Copy-Item -Recurse ui-anti-ai-slop\skills\html-game-ui-design "$env:USERPROFILE\.claude\skills\"
```

**Para un solo proyecto, compartido con su equipo** (skill de proyecto): copia la misma carpeta dentro de `.claude/skills/` en la raíz del repositorio del juego y haz commit.

```
tu-juego/
└── .claude/
    └── skills/
        └── html-game-ui-design/
            └── SKILL.md
```

Claude Code detecta los skills nuevos y modificados en estas carpetas durante la sesión. Si la carpeta `skills` no existía al iniciar la sesión, ejecuta `/reload-skills`.

Instalado así, el nombre del skill es `/html-game-ui-design`.

## Otros agentes

El skill sigue la [especificación abierta Agent Skills](https://agentskills.io/specification), que también leen otros agentes de programación. Copia `skills/html-game-ui-design` en el directorio de skills de tu agente; su documentación indica cuál es. El detector es Python puro y funciona en cualquier parte.

## Cómo usar el skill

### Se carga solo

No hace falta nombrar el skill. Claude lee su descripción y lo carga cuando la petición trata de interfaces de juego: un HUD, un menú, un inventario, una pantalla de título, una mano de cartas, o una queja de que la UI de un juego se ve genérica. En Claude Code también puedes invocarlo explícitamente con los nombres indicados arriba, y en cualquier app de Claude basta con decir "usa el skill html-game-ui-design".

El skill está escrito en inglés, pero Claude responde en el idioma en que le escribas.

### Qué decirle a Claude

El primer paso del skill es leer el juego, así que cuanto más le des de esto, más específico será el resultado:

| Dile | Ejemplo |
|---|---|
| La fantasía | "Eres la aprendiz de un farero en una isla azotada por tormentas, en 1890" |
| El campo de juego | "Vista desde arriba, la lancha se queda cerca del centro y la pista se desplaza" |
| Qué hace y qué mira el jugador | "Velocidad y turbo todo el tiempo; vuelta y posición de vez en cuando" |
| Plataforma y controles | "Navegador de escritorio, teclado o control" o "celular en vertical, táctil" |
| La tecnología | "Canvas de Phaser 3 a 1280x720 con HTML encima" o "HTML puro, sin compilación" |
| Arte existente, si lo hay | Adjunta una captura, sprites o una paleta |
| Qué entregar | "Un solo archivo HTML con un fondo de relleno para verlo funcionando" |

Una petición que solo nombra el componente ("hazme una barra de vida") también funciona, pero entonces Claude tiene que inventar el mundo y conviene revisar la dirección que eligió.

### Qué recibes

1. **Una dirección**, en pocas líneas: qué objeto es la interfaz dentro del mundo del juego, una referencia del mundo real, material, formas, tipografías, paleta, estilo de iconos, movimiento, un detalle firma y los defectos por omisión que rechaza.
2. **Los archivos**, construidos desde esa dirección, con iconos SVG dibujados, superficies construidas, respuesta visual cuando cambian los valores y navegación por teclado y control.
3. **Una nota breve** sobre lo que se construyó y lo que conviene que pruebes tú, como un control físico.

Antes de entregar, Claude ejecuta el detector incluido y corrige lo que encuentra.

### Cómo redirigir la dirección

La dirección es el punto más barato para cambiar de rumbo. Si no te convence, responde antes de pedir otra cosa:

```
Menos militar. La dueña del puesto es una señora mayor que pinta sus propios letreros.
```

```
Conserva la dirección, pero la tipografía de lectura es demasiado formal para niños.
```

```
Dame tres direcciones distintas para este juego, en pocas líneas cada una, y yo elijo.
```

En un proyecto grande, pide las tres opciones desde el inicio.

### Arreglar una interfaz existente

Dale el archivo a Claude y dile qué no debe romperse:

```
Este es mi HUD. Se ve como una página web genérica. Rehaz lo visual para que
pertenezca al juego (una ciudad amurallada dentro del esqueleto de una bestia
gigante). Conserva los ids y las funciones setHealth, setGold y selectTower,
porque el loop del juego las llama.
```

Claude analiza el archivo, te dice qué lo hace ver genérico y por qué, propone una dirección y reconstruye la capa visual conservando tus enlaces con el código.

### Peticiones de ejemplo

```
Construye la pantalla de ronda de un deckbuilder sobre un puesto de comida en un
mercado nocturno: mano de cinco cartas, calor disponible en el turno, mazo y
descarte, monedas, reputación, clientes en espera y Terminar turno. Un solo
archivo HTML, pensado para ratón pero que funcione con teclado.
```

```
Dos pantallas para un juego de fracciones para niñas y niños de 8 a 10 años,
celular en vertical: selección de nivel con 12 niveles en 3 mundos, y nivel
completado con estrellas y monedas. Un solo archivo HTML donde pueda pasar de
una a otra.
```

```
Revisa el menú de pausa en src/ui/pause.html con el skill y dime qué se ve
genérico. No cambies nada todavía.
```

## Ejecutar el detector por tu cuenta

El detector funciona con el código de cualquier UI de juego, con o sin Claude. Necesita Python 3.8 o posterior.

```bash
python slop_scan.py ruta/al/archivo-o-carpeta
```

| Opción | Efecto |
|---|---|
| `--json` | Salida legible por máquina |
| `--strict` | Sale con 1 también ante hallazgos P1, no solo P0 |
| `--help` | Uso |

Lee archivos `.html`, `.css`, `.scss`, `.js`, `.jsx`, `.ts`, `.tsx`, `.vue` y `.svelte`, y omite `node_modules`, `dist` y `build`. Cada hallazgo tiene un ID de regla explicado en `references/slop-tells.md`.

Los hallazgos tienen tres niveles. P0 se reconoce a simple vista como generado o como app web: emojis como iconos, paneles de vidrio difuminado, degradados morados, tipografía genérica o ausente, y foco eliminado sin reemplazo. P1 se lee como genérico cuando aparecen varios juntos. P2 es pulido faltante.

Cuando una decisión marcada es deliberada, regístrala en el código para que el detector la reporte como exenta en lugar de fallar:

```css
/* slop-ok: glass-panels  el HUD es un visor esmerilado, nombrado en la dirección */
```

Un análisis limpio significa que no se encontraron defectos obvios. No es un juicio de calidad.

## Actualizar y desinstalar

**Apps de Claude.** Descarga el ZIP nuevo y súbelo otra vez. Para quitar el skill, ábrelo en Customize > Skills, apágalo, abre el menú de tres puntos y elige Delete.

**Plugin de Claude Code.**

```bash
claude plugin marketplace update ui-anti-ai-slop            # trae el listado más reciente
claude plugin update game-ui-anti-slop@ui-anti-ai-slop      # actualiza el plugin

claude plugin uninstall game-ui-anti-slop@ui-anti-ai-slop   # quita el plugin
claude plugin marketplace remove ui-anti-ai-slop            # quita el marketplace y sus plugins
```

**Skill suelto en Claude Code.** Actualiza el repositorio con `git pull` y copia la carpeta de nuevo, o borra la carpeta `html-game-ui-design` de `~/.claude/skills/` o de `.claude/skills/`.

## Solución de problemas

**La subida se rechaza porque el nombre de la carpeta no coincide.** El ZIP debe contener una carpeta llamada exactamente `html-game-ui-design` en su nivel superior, con `SKILL.md` directamente dentro. Esto pasa al comprimir los archivos sin su carpeta o al comprimir el repositorio entero.

**La subida se rechaza por la descripción.** La descripción del skill está escrita al límite de 1,024 caracteres de Agent Skills. Si tu app de Claude pide una más corta, abre `SKILL.md`, reemplaza la línea `description:` por la siguiente y vuelve a comprimir la carpeta:

```yaml
description: Designs and builds HTML/CSS/JS video game UI (HUDs, menus, inventories, dialogue, cards) that looks like part of the game, not a generic AI-made web app. Use for any browser game interface.
```

**No aparece la opción de subir un skill.** La ejecución de código o los skills están desactivados para tu cuenta u organización. Consulta "Antes de empezar" arriba.

**Claude no usa el skill.** Revisa que su interruptor esté encendido, y luego menciona claramente la UI de juego en la petición o nombra el skill. Las peticiones muy cortas ("haz un botón") pueden no activar ningún skill.

**El detector no se ejecuta.** En las apps de Claude corre en el entorno de ejecución de código del propio Claude y no necesita nada de tu parte. En Claude Code necesita Python 3.8 o posterior en tu máquina; en Windows el comando puede ser `py` en lugar de `python`. Sin Python, Claude revisa contra el catálogo a mano.

**El resultado sigue viéndose genérico.** Mira la dirección que escribió Claude. Si nombra un cliché de género (pergamino y dorado para fantasía, hologramas cian para ciencia ficción, una fuente pixelada para todo lo retro), pide otra y dale algo concreto sobre tu mundo con qué trabajar.

**Las fuentes se ven mal al abrir el archivo sin conexión.** Los archivos cargan las tipografías desde Google Fonts y sin conexión recurren a una fuente del sistema elegida. Pídele a Claude que incruste las fuentes o que use solo tipografías del sistema si el juego debe funcionar sin internet.
