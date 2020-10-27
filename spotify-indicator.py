#!/usr/bin/env python3
import os
import re
import signal
import subprocess

import gi

gi.require_version('AppIndicator3', '0.1')
from gi.repository import AppIndicator3

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GLib

gi.require_version('GdkPixbuf', '2.0')
from gi.repository.GdkPixbuf import Pixbuf


HOME_DIR = '/usr/share/spotify-indicator'
APPINDICATOR_ID = "spotify-indicator"
VERSION = '1.0.0'
COPYRIGHT = 'Copyright ' + '\u00a9' + '2020 Pavel Makhov'
LICENSE = """
Licensed under the MIT license:

    http://www.opensource.org/licenses/mit-license.php

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE."""


class SpotifyIndicator:
    def __init__(self):
        self.current_dict = {}
        self.spotify_indicator = AppIndicator3.Indicator.new(
            "spotify-indicator",
            os.path.abspath(HOME_DIR + "/Spotify_Icon_RGB_Green.png"),
            AppIndicator3.IndicatorCategory.SYSTEM_SERVICES)

        self.spotify_indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.spotify_indicator.connect('scroll-event', self.scroll)
        self.spotify_indicator.set_menu(self.menu_build())

        GLib.timeout_add(1000, self.refresh_label)

    def refresh_label(self):
        result = subprocess.run(['sp', 'metadata'], stdout=subprocess.PIPE)
        current = result.stdout.decode('utf-8')
        parts = re.split("\n", current)
        parts.remove('')
        for line in parts:
            a = re.split("\|", line)
            self.current_dict[a[0]] = a[1]
        self.spotify_indicator.set_label(self.ellipsize(self.current_dict['artist']) + " | " +
                                         self.ellipsize(self.current_dict['title']), '')

        status_output = subprocess.run(['sp', 'status'], stdout=subprocess.PIPE)
        status = status_output.stdout.decode('utf-8').strip()
        if status == 'Playing':
            self.spotify_indicator.set_icon_full(
                os.path.abspath(HOME_DIR + "/Spotify_Icon_RGB_Green.png"), '')
        elif status == 'Paused':
            self.spotify_indicator.set_icon_full(
                os.path.abspath(HOME_DIR + "/Spotify_Icon_RGB_White.png"), '')

        return True

    def ellipsize(self, str):
        return (str[:20] + '..') if len(str) > 20 else str

    def scroll(self, ind, steps, direction):
        if direction == Gdk.ScrollDirection.UP:
            subprocess.run(["sp", "prev"])
        elif direction == Gdk.ScrollDirection.DOWN:
            subprocess.run(["sp", "next"])

    def toggle_playback(self, widget):
        subprocess.run(['sp', 'play'])

    def menu_build(self):
        menu = Gtk.Menu()

        item_pokemon = Gtk.MenuItem(label="Play / Pause")
        item_pokemon.connect('activate', self.toggle_playback)
        menu.append(item_pokemon)

        separator = Gtk.SeparatorMenuItem.new()
        separator.show()
        menu.append(separator)

        about_item = Gtk.MenuItem(label='About');
        about_item.connect("activate", self.openAbout)
        menu.append(about_item)

        item_quit = Gtk.MenuItem(label="Quit")
        item_quit.connect('activate', self.quit)
        menu.append(item_quit)

        menu.show_all()

        return menu

    def openAbout(self, widget):
        aboutWindow = Gtk.AboutDialog()
        aboutWindow.set_logo(APPLOGO)
        aboutWindow.set_icon(APPLOGO)
        aboutWindow.set_program_name('Spotify indicator')
        aboutWindow.set_version('Version ' + VERSION)
        aboutWindow.set_copyright(COPYRIGHT)
        aboutWindow.set_license(LICENSE)
        aboutWindow.set_authors(['Pavel Makhov <streetturtle@gmail.com>'])
        aboutWindow.set_resizable(False)
        aboutWindow.run()
        aboutWindow.destroy()

    def quit(self):
        Gtk.main_quit()


if __name__ == "__main__":
    APPLOGO = Pixbuf.new_from_file_at_size(HOME_DIR + "/Spotify_Icon_RGB_Green.png", 100, 100)

    signal.signal(signal.SIGINT, signal.SIG_DFL)

    SpotifyIndicator()

    Gtk.main()
