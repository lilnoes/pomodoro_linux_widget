import sys
from pathlib import Path
import gi
gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GLib

#working directory
parentDir = Path(__file__).absolute().parent


#default pomodoro duration
mins = 25

#call from command line python pomodoro.py mins
if len(sys.argv) > 1:
    try:
        mins = int(sys.argv[1])
    except:
        print("invalid input, must be a number greater than 0, reset to 25 mins")
        mins = 25


class Pomodoro:
    def __init__(self, mins):
        builder = Gtk.Builder()
        builder.add_from_file(str(parentDir.joinpath("glade.glade")))

        self.window = builder.get_object("window1")
        self.button = builder.get_object("button1")
        self.restartButton = builder.get_object("restartButton")
        self.label = builder.get_object("label1")

        builder.connect_signals(self)

        #run every second
        secs = 1
        GLib.timeout_add_seconds(secs, self.onTimer, {})

        self.mins = mins
        self.count = mins*60 #25 minutes
        self.open = False
        self.button.set_label("START")
        self.label.set_label("")

        self.hideRestartButton()

    def onDestroy(self, *args):
        Gtk.main_quit(*args)

    def onButtonPressed(self, button):
        self.open = not self.open
        self.showRestartButton()
        if self.open and self.count > 0:
            self.label.set_label("running")
        if not self.open and self.count > 0:
            self.label.set_label("paused")

    def hideRestartButton(self):
        self.restartButton.hide()

    def showRestartButton(self):
        self.restartButton.show()
    
    #return true so that it will get called again
    def onTimer(self, data):
        if not self.open:
            return True
        if self.count == 0:
            self.label.set_label("FINISHED")
            self.button.set_label("START")
            self.count = self.mins*60
            self.open = False
            self.hideRestartButton()
        else:
            self.count -= 1
            mins = self.count // 60
            secs = self.count - (mins*60)
            self.button.set_label(f"{mins}:{secs}")
        return True

    def onRestart(self, button):
        self.open = True
        self.count = self.mins * 60
        self.label.set_label("running")


#connect css to application
css = Gtk.CssProvider.new()
css.load_from_path(str(parentDir.joinpath("index.css")))
Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), css, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)


pomodoro = Pomodoro(mins)
pomodoro.window.show()
Gtk.main()