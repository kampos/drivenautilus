import sys
import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw
from .app import DriveNautilusApp

def main():
    app = DriveNautilusApp()
    return app.run(sys.argv)

if __name__ == "__main__":
    main()
