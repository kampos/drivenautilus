import os
import asyncio
import threading
from gi.repository import Gtk, Adw, Gio, GLib, GObject
from .config import Config
from .dependency_manager import DependencyManager
from .rclone_manager import RcloneManager
from .mount_manager import MountManager
from .systemd_manager import SystemdManager
from .nautilus_manager import NautilusManager
from .ui_state import UIState

class DriveNautilusWindow(Adw.ApplicationWindow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.set_title("KADrivesync")
        self.set_default_size(500, 600)

        self.config = Config()
        self.state = UIState()
        
        self.rclone_manager = RcloneManager(self.config.get("remote_name"))
        self.mount_manager = MountManager(
            self.config.get("remote_name"),
            self.config.get("mount_path")
        )
        self.systemd_manager = SystemdManager()
        
        self.setup_ui()
        self.refresh_state()

    def setup_ui(self):
        self.content = Adw.ToolbarView()
        self.set_content(self.content)

        # Header Bar
        self.header_bar = Adw.HeaderBar()
        self.content.add_top_bar(self.header_bar)

        # View Stack
        self.stack = Adw.ViewStack()
        self.content.set_content(self.stack)

        # Views
        self.setup_welcome_view()
        self.setup_diagnosis_view()
        self.setup_connection_view()
        self.setup_main_view()

    def setup_welcome_view(self):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=24)
        box.set_valign(Gtk.Align.CENTER)
        box.set_halign(Gtk.Align.CENTER)
        box.set_margin_top(40)
        box.set_margin_bottom(40)
        box.set_margin_start(40)
        box.set_margin_end(40)

        # Try to load custom icon, fallback to symbolic
        icon = Gtk.Image.new_from_icon_name("org.kampos.KADrivesync")
        if icon.get_storage_type() == Gtk.ImageType.EMPTY:
            icon.set_from_icon_name("cloud-upload-symbolic")
        
        icon.set_pixel_size(128)
        box.append(icon)

        title = Gtk.Label(label="KADrivesync")
        title.add_css_class("title-1")
        box.append(title)

        subtitle = Gtk.Label(label="Monta Google Drive como carpeta local en Ubuntu")
        subtitle.add_css_class("body")
        box.append(subtitle)

        btn_start = Gtk.Button(label="Comenzar")
        btn_start.add_css_class("suggested-action")
        btn_start.add_css_class("pill")
        btn_start.connect("clicked", self.on_start_clicked)
        box.append(btn_start)

        self.stack.add_titled(box, "welcome", "Bienvenida")

    def setup_diagnosis_view(self):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=24)
        box.set_margin_top(32)
        box.set_margin_bottom(32)
        box.set_margin_start(32)
        box.set_margin_end(32)

        title = Gtk.Label(label="Diagnóstico del Sistema")
        title.add_css_class("title-2")
        box.append(title)

        self.deps_list = Gtk.ListBox()
        self.deps_list.set_selection_mode(Gtk.SelectionMode.NONE)
        self.deps_list.add_css_class("boxed-list")
        box.append(self.deps_list)

        self.dep_rows = {}
        for dep in DependencyManager.REQUIRED_COMMANDS:
            row = Adw.ActionRow(title=dep)
            indicator = Gtk.Image.new_from_icon_name("view-reveal-symbolic")
            row.add_suffix(indicator)
            self.deps_list.append(row)
            self.dep_rows[dep] = (row, indicator)

        self.btn_install = Gtk.Button(label="Instalar dependencias")
        self.btn_install.add_css_class("suggested-action")
        self.btn_install.connect("clicked", self.on_install_deps_clicked)
        box.append(self.btn_install)

        self.stack.add_titled(box, "diagnosis", "Diagnóstico")

    def setup_connection_view(self):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=24)
        box.set_valign(Gtk.Align.CENTER)
        box.set_margin_top(32)
        box.set_margin_bottom(32)
        box.set_margin_start(32)
        box.set_margin_end(32)

        icon = Gtk.Image.new_from_icon_name("network-transmit-receive-symbolic")
        icon.set_pixel_size(96)
        box.append(icon)

        title = Gtk.Label(label="Configurar Google Drive")
        title.add_css_class("title-2")
        box.append(title)

        info = Gtk.Label(label="Introduce un nombre para esta conexión (se mostrará en Nautilus):")
        info.set_wrap(True)
        info.set_justify(Gtk.Justification.CENTER)
        box.append(info)

        self.entry_name = Gtk.Entry()
        self.entry_name.set_placeholder_text("Google Drive")
        self.entry_name.set_text(self.config.get("connection_label"))
        self.entry_name.set_halign(Gtk.Align.CENTER)
        self.entry_name.set_width_chars(30)
        box.append(self.entry_name)

        self.btn_connect = Gtk.Button(label="Conectar")
        self.btn_connect.add_css_class("suggested-action")
        self.btn_connect.add_css_class("pill")
        self.btn_connect.connect("clicked", self.on_connect_clicked)
        box.append(self.btn_connect)

        self.stack.add_titled(box, "connection", "Conexión")

    def setup_main_view(self):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        box.set_margin_top(24)
        box.set_margin_bottom(24)
        box.set_margin_start(24)
        box.set_margin_end(24)

        status_group = Adw.PreferencesGroup(title="Estado")
        box.append(status_group)

        self.mount_row = Adw.ActionRow(title="Montaje")
        self.mount_indicator = Gtk.Label(label="No montado")
        self.mount_indicator.add_css_class("dim-label")
        self.mount_row.add_suffix(self.mount_indicator)
        status_group.add(self.mount_row)

        actions_group = Adw.PreferencesGroup(title="Acciones")
        box.append(actions_group)

        self.btn_mount = Gtk.Button(label="Montar en Nautilus")
        self.btn_mount.add_css_class("suggested-action")
        self.btn_mount.connect("clicked", self.on_mount_clicked)
        
        mount_action_row = Adw.ActionRow(title="Control de unidad")
        mount_action_row.add_suffix(self.btn_mount)
        actions_group.add(mount_action_row)

        self.btn_open = Gtk.Button(label="Abrir en Archivos")
        self.btn_open.connect("clicked", self.on_open_clicked)
        open_action_row = Adw.ActionRow(title="Explorador de archivos")
        open_action_row.add_suffix(self.btn_open)
        actions_group.add(open_action_row)

        self.auto_mount_switch = Gtk.Switch()
        self.auto_mount_switch.set_valign(Gtk.Align.CENTER)
        self.auto_mount_switch.connect("state-set", self.on_auto_mount_toggled)
        auto_mount_row = Adw.ActionRow(title="Montar automáticamente al iniciar")
        auto_mount_row.add_suffix(self.auto_mount_switch)
        actions_group.add(auto_mount_row)

        # Dangerous Actions
        danger_group = Adw.PreferencesGroup(title="Mantenimiento")
        box.append(danger_group)

        self.btn_reset = Gtk.Button(label="Eliminar configuración")
        self.btn_reset.add_css_class("destructive-action")
        self.btn_reset.connect("clicked", self.on_reset_clicked)
        
        reset_row = Adw.ActionRow(title="Reiniciar aplicación")
        reset_row.set_subtitle("Detiene el servicio, desmonta la unidad y borra la conexión de rclone.")
        reset_row.add_suffix(self.btn_reset)
        danger_group.add(reset_row)

        # Logs
        expander = Adw.ExpanderRow(title="Detalles técnicos")
        self.log_buffer = Gtk.TextBuffer()
        log_view = Gtk.TextView(buffer=self.log_buffer)
        log_view.set_editable(False)
        log_view.set_margin_top(12)
        log_view.set_margin_bottom(12)
        log_view.set_margin_start(12)
        log_view.set_margin_end(12)
        log_view.set_size_request(-1, 200)
        
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_child(log_view)
        scrolled.set_propagate_natural_height(True)
        expander.add_row(scrolled)
        box.append(expander)

        self.stack.add_titled(box, "main", "Principal")

    def on_start_clicked(self, button):
        self.refresh_state()
        if not self.state.dependencies_installed:
            self.stack.set_visible_child_name("diagnosis")
        elif not self.state.gdrive_configured:
            self.stack.set_visible_child_name("connection")
        else:
            self.stack.set_visible_child_name("main")

    def refresh_state(self):
        deps = DependencyManager.check_dependencies()
        self.state.dependencies_installed = all(deps.values())
        self.state.missing_deps = [cmd for cmd, exists in deps.items() if not exists]
        self.state.rclone_is_snap = DependencyManager.is_rclone_snap()
        
        if self.state.dependencies_installed:
            self.state.gdrive_configured = self.rclone_manager.remote_exists()
            self.state.is_mounted = self.mount_manager.is_mounted()
            self.state.auto_mount_active = self.systemd_manager.is_service_enabled()
        
        self.update_ui()

    def update_ui(self):
        deps = DependencyManager.check_dependencies()
        for dep, exists in deps.items():
            if dep in self.dep_rows:
                row, indicator = self.dep_rows[dep]
                indicator.remove_css_class("success")
                indicator.remove_css_class("error")
                if exists:
                    indicator.set_from_icon_name("emblem-ok-symbolic")
                    indicator.add_css_class("success")
                else:
                    indicator.set_from_icon_name("window-close-symbolic")
                    indicator.add_css_class("error")

        self.btn_install.set_visible(not self.state.dependencies_installed)

        self.mount_indicator.remove_css_class("success")
        self.mount_indicator.remove_css_class("error")
        if self.state.is_mounted:
            self.mount_indicator.set_label("Listo")
            self.mount_indicator.add_css_class("success")
            self.btn_mount.set_label("Desmontar")
            self.btn_mount.remove_css_class("suggested-action")
            self.btn_mount.add_css_class("destructive-action")
        else:
            self.mount_indicator.set_label("No montado")
            self.mount_indicator.add_css_class("error")
            self.btn_mount.set_label("Montar en Nautilus")
            self.btn_mount.add_css_class("suggested-action")
            self.btn_mount.remove_css_class("destructive-action")

        self.btn_open.set_sensitive(self.state.is_mounted)
        self.auto_mount_switch.set_state(self.state.auto_mount_active)

    def on_install_deps_clicked(self, button):
        def install_async():
            DependencyManager.install_dependencies_deb()
            GLib.idle_add(self.refresh_state)
            if self.state.dependencies_installed:
                GLib.idle_add(self.on_start_clicked, None)

        threading.Thread(target=install_async).start()

    def on_connect_clicked(self, button):
        label = self.entry_name.get_text().strip() or "Google Drive"
        # Create a slug for the remote name and folder
        slug = label.replace(" ", "").lower()
        if not slug:
            slug = "gdrive"
            
        self.config.set("connection_label", label)
        self.config.set("remote_name", slug)
        self.config.set("mount_path", f"~/{label.replace(' ', '')}")
        
        # Re-initialize managers with new config
        self.rclone_manager = RcloneManager(self.config.get("remote_name"))
        self.mount_manager = MountManager(
            self.config.get("remote_name"),
            self.config.get("mount_path")
        )

        async def connect_async():
            result = await self.rclone_manager.configure_google_drive()
            GLib.idle_add(self.refresh_state)
            if result.success:
                GLib.idle_add(self.stack.set_visible_child_name, "main")

        def run_loop():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(connect_async())

        threading.Thread(target=run_loop).start()

    def on_reset_clicked(self, button):
        # Confirmation dialog
        dialog = Adw.MessageDialog(
            transient_for=self,
            heading="¿Eliminar configuración?",
            body="Se desmontará la unidad, se detendrá el inicio automático y se borrará la conexión de rclone. No se borrarán archivos de tu Google Drive.",
        )
        dialog.add_response("cancel", "Cancelar")
        dialog.add_response("delete", "Eliminar")
        dialog.set_response_appearance("delete", Adw.ResponseAppearance.DESTRUCTIVE)
        
        def on_response(d, response):
            if response == "delete":
                self.perform_reset()
        
        dialog.connect("response", on_response)
        dialog.present()

    def perform_reset(self):
        async def reset_async():
            # 1. Stop service
            self.systemd_manager.disable_service()
            # 2. Unmount
            await self.mount_manager.unmount()
            # 3. Remove Nautilus bookmark
            NautilusManager.remove_bookmark(self.config.get("mount_path"))
            # 4. Delete rclone remote
            from .command_runner import CommandRunner
            CommandRunner.run_sync(["rclone", "config", "delete", self.config.get("remote_name")])
            
            # 5. Reset config to defaults
            from .config import DEFAULT_CONFIG
            for k, v in DEFAULT_CONFIG.items():
                self.config.set(k, v)
            
            GLib.idle_add(self.refresh_state)
            GLib.idle_add(self.stack.set_visible_child_name, "welcome")

        def run_loop():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(reset_async())

        threading.Thread(target=run_loop).start()

    def on_mount_clicked(self, button):
        async def toggle_mount():
            if self.state.is_mounted:
                await self.mount_manager.unmount()
            else:
                await self.mount_manager.mount(
                    volname=self.config.get("connection_label")
                )
            GLib.idle_add(self.refresh_state)

        def run_loop():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(toggle_mount())

        threading.Thread(target=run_loop).start()

    def on_open_clicked(self, button):
        self.mount_manager.open_mount_folder()
        NautilusManager.try_add_bookmark(
            self.config.get("mount_path"), 
            self.config.get("connection_label")
        )

    def on_auto_mount_toggled(self, switch, state):
        if state:
            self.systemd_manager.write_user_service(
                self.config.get("remote_name"),
                self.config.get("mount_path"),
                self.config.get("vfs_cache_mode"),
                self.config.get("dir_cache_time"),
                self.config.get("poll_interval"),
                self.config.get("vfs_cache_max_size"),
                self.config.get("connection_label")
            )
            self.systemd_manager.enable_service()
        else:
            self.systemd_manager.disable_service()
        self.refresh_state()
        return True
