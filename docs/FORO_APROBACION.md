# Solicitud para el foro de Snap Store

Usa este texto como base para pedir revisión de classic confinement.

```text
name: KADrivesync
description: Aplicación de escritorio para montar Google Drive como carpeta local en Nautilus usando rclone mount y FUSE, sin sincronizar todo el contenido al disco.
snapcraft: https://github.com/kampos/drivenautilus/blob/main/snap/snapcraft.yaml
upstream: https://github.com/kampos/drivenautilus
upstream-relation: Soy el autor y mantenedor del proyecto.
supported-category: storage and backup
reasoning: La aplicación necesita montar un sistema de archivos FUSE real para que Google Drive aparezca como carpeta local dentro de Nautilus. También crea y gestiona una unidad systemd --user para el montaje automático. He probado los flujos de montaje, desmontaje y arranque automático, y el comportamiento requerido no encaja bien con una estricta sandbox porque el objetivo del producto es exponer un montaje real del sistema de archivos al usuario.

I understand that strict confinement is generally preferred over classic.

I’ve tried the existing interfaces to make the snap work under strict confinement.
```

## Qué conviene adjuntar en el post

- URL pública del `snapcraft.yaml`
- URL del repositorio upstream
- explicación breve de por qué `home` y `removable-media` no cubren el caso
- captura o salida de `snappy-debug` si la tienes
- aclaración de que no sincroniza todo el Drive, solo lo monta

## Observación

La categoría `supported-category` es la parte más sensible del request. Si el equipo de revisión no acepta `storage and backup`, habrá que ajustar el argumento y explicar con más detalle el caso de uso exacto.

