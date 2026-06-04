# Ficha para Ubuntu Store

## Nombre

KADrivesync

## Resumen corto

Monta Google Drive como carpeta local sin sincronizar

## Descripción larga

KADrivesync permite usar Google Drive desde Nautilus como si fuera una carpeta local. La aplicación configura un remoto de `rclone`, monta el contenido con `rclone mount` y expone el acceso desde el explorador de archivos.

No sincroniza todos los archivos al disco. El contenido se sirve bajo demanda, lo que evita duplicar datos y reduce el uso de almacenamiento local.

La aplicación incluye:

- diagnóstico de dependencias
- configuración asistida del remoto
- montaje y desmontaje
- integración con Nautilus
- arranque automático mediante `systemd --user`

## Categoría sugerida

Utility

## Licencia

GPL-3.0-only

## Confinamiento

Classic

## Motivo técnico del classic

La app necesita:

- ejecutar `rclone mount`
- manejar un punto de montaje FUSE real en el sistema del usuario
- crear y controlar una unidad `systemd --user`
- abrir el montaje en Nautilus con acceso al sistema de archivos real

## Palabras clave

google, drive, rclone, fuse, nautilus, mount, cloud, files, storage

## Contacto

kampos@kampos.info

## Enlaces

- Source code: https://github.com/kampos/drivenautilus
- Issues: https://github.com/kampos/drivenautilus/issues

## Capturas necesarias

Para aprobar mejor la ficha conviene subir:

- pantalla inicial
- pantalla de diagnóstico
- pantalla de conexión
- pantalla principal con estado montado
- Nautilus mostrando la unidad montada

## Nota operativa

Antes de publicar conviene subir el metainfo AppStream y ejecutar `snapcraft upload-metadata` sobre el `.snap` para sincronizar resumen, descripción e icono con la Store.

