# KADrivesync

KADrivesync es una app de escritorio para Ubuntu que monta Google Drive como una carpeta local visible en Nautilus sin sincronizar todos los archivos al disco.

La idea es simple: usas `rclone mount`, ves tu unidad en el explorador de archivos y accedes al contenido bajo demanda.

## Qué hace

- Configura un remoto de Google Drive con `rclone`.
- Monta el remoto en una carpeta local del usuario.
- Crea o elimina un servicio `systemd --user` para el arranque automático.
- Añade el acceso a Nautilus para abrir el montaje directamente.
- Muestra un diagnóstico básico de dependencias del sistema.

## Qué no hace

- No sincroniza una copia completa del Drive al disco.
- No pretende sustituir a un cliente de sincronización bidireccional.
- No soporta todavía otros proveedores de nube.

## Requisitos

- Ubuntu con GNOME y Nautilus.
- `rclone`.
- `fuse3`.
- `systemd --user`.

## Estado del proyecto

La aplicación ya tiene:

- interfaz GTK4/libadwaita
- empaquetado Snap
- empaquetado Debian
- metadatos AppStream
- pruebas unitarias para gestores internos

También hay una tarea pendiente de limpieza: el árbol contiene copias generadas en `prime/`, `stage/` y `parts/` que no deberían formar parte del control de versiones final.

## Instalación

### Snap

```bash
sudo snap install kadrivesync --classic
```

> Esta app usa `classic confinement` porque necesita montar FUSE y gestionar un servicio de usuario con acceso real al sistema.

### Debian

```bash
sudo dpkg -i drivenautilus.deb
sudo apt-get install -f
```

## Uso

1. Abre `KADrivesync`.
2. Pasa por el diagnóstico si faltan dependencias.
3. Configura el remoto de Google Drive.
4. Monta la unidad.
5. Abre la carpeta desde Nautilus.

## Desarrollo

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
pip install pytest
pytest -q
```

## Empaquetado

### Snap

```bash
snapcraft
```

### Debian

```bash
debuild -us -uc
```

## Publicación

La documentación de soporte para publicación está en `docs/`:

- `docs/ANALISIS.md`
- `docs/UBUNTU_STORE.md`
- `docs/FORO_APROBACION.md`

## Licencia

GPL-3.0-only
