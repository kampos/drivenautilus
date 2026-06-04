import os

import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw, Gio, Gdk

from .window import DriveNautilusWindow

class DriveNautilusApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(application_id='org.kampos.KADrivesync',
                         flags=Gio.ApplicationFlags.FLAGS_NONE,
                         **kwargs)
        self.window = None

    def do_activate(self):
        if not self.window:
            self.window = DriveNautilusWindow(application=self)
            
            # Set window icon
            base_dir = os.path.dirname(__file__)
            icon_path = os.path.join(os.path.dirname(os.path.dirname(base_dir)), "data", "icons", "org.kampos.KADrivesync.svg")
            if os.path.exists(icon_path):
                self.window.set_icon_name("org.kampos.KADrivesync")
                # For development, we might need to load it directly
                try:
                    display = Gdk.Display.get_default()
                    theme = Gtk.IconTheme.get_for_display(display)
                    if not theme.has_icon("org.kampos.KADrivesync"):
                        theme.add_search_path(os.path.dirname(icon_path))
                except:
                    pass
                    
        self.window.present()

    def do_startup(self):
        Adw.Application.do_startup(self)
        self.load_css()

    def load_css(self):
        provider = Gtk.CssProvider()
        
        # Get path to style.css
        base_dir = os.path.dirname(__file__)
        css_path = os.path.join(base_dir, "resources", "style.css")
        
        if os.path.exists(css_path):
            provider.load_from_path(css_path)
            Gtk.StyleContext.add_provider_for_display(
                Gdk.Display.get_default(),
                provider,
                Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
            )
