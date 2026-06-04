# Análisis técnico

## Resumen

KADrivesync es una aplicación de escritorio en Python con GTK4 y libadwaita que automatiza el montaje de Google Drive en una carpeta local mediante `rclone mount`.

El flujo principal es:

1. diagnosticar dependencias del sistema
2. crear o validar el remoto de `rclone`
3. montar Google Drive en una ruta del usuario
4. abrir esa ruta en Nautilus
5. opcionalmente crear un servicio `systemd --user` para el arranque automático

## Componentes principales

- `src/drivenautilus/app.py`: instancia la aplicación GTK.
- `src/drivenautilus/window.py`: define la UI y los flujos de interacción.
- `src/drivenautilus/config.py`: persiste la configuración del usuario.
- `src/drivenautilus/rclone_manager.py`: crea, valida y consulta remotos.
- `src/drivenautilus/mount_manager.py`: controla el montaje y desmontaje.
- `src/drivenautilus/systemd_manager.py`: escribe y gestiona la unidad de usuario.
- `src/drivenautilus/nautilus_manager.py`: integra bookmarks y apertura en Nautilus.
- `src/drivenautilus/dependency_manager.py`: comprueba comandos externos.

## Dependencias reales

La app depende de:

- `pygobject`
- `Gtk 4`
- `libadwaita`
- `rclone`
- `fuse3`
- `systemctl --user`
- `nautilus`
- `xdg-open`

## Hallazgos

### 1. Identidad de la app

El proyecto mezclaba varios identificadores:

- `DriveNautilus`
- `KADrivesync`
- `org.fonteboa.*`
- `org.kampos.*`

Eso complica AppStream, Snap y Debian. La base de documentación y empaquetado se ha normalizado a `KADrivesync` con `org.kampos.KADrivesync`.

### 2. Tests

`pytest` estaba recorriendo copias generadas del proyecto en `prime/`, `stage/` y `parts/`, lo que provocaba errores de importación por falta de `src` en `sys.path`.

Se ha añadido:

- `pytest.ini` para limitar la búsqueda de tests
- `conftest.py` para añadir `src` al path de importación

### 3. Metadatos de paquete

`debian/install` apuntaba a archivos que ya no existían con esos nombres.

Se ha corregido para usar:

- `data/org.kampos.KADrivesync.desktop`
- `data/org.kampos.KADrivesync.metainfo.xml`
- `data/icons/org.kampos.KADrivesync.svg`

## Riesgos pendientes

- El árbol contiene artefactos de build grandes en `prime/`, `stage/` y `parts/`.
- El Snap actual usa `confinement: classic`; eso exige revisión manual en la Snap Store.
- No hay una batería de integración para validar el montaje real contra Google Drive.
