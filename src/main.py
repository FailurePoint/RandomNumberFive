# main.py
#
# Copyright 2023 FailurePoint
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

import sys
import gi
import random

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Gio, Adw
from .window import RandomNumberFiveWindow
from .metadata import Vstatic, debug


class RandomNumberFiveApplication(Adw.Application):
    """The main application singleton class."""

    def __init__(self):
        super().__init__(application_id='io.github.FailurePoint.RandomNumberFive',
                         flags=Gio.ApplicationFlags.DEFAULT_FLAGS)
        debug.report("*********internal action connections************", line_prompt=False)
        self.create_action('quit', lambda *_: self.quit(), ['<primary>q'])
        self.create_action('about', self.on_about_action)
        self.create_action('new_random', self.on_create_random, ['<primary>r'])
        self.create_action('reset', self.on_reset, ['<primary><shift>r'])
        debug.report("*************************************************", line_prompt=False)
        debug.newline()

        self.persistant = Gio.Settings.new("io.github.FailurePoint.RandomNumberFive")


    def do_activate(self):
        """Called when the application is activated.

        We raise the application's main window, creating it if
        necessary.
        """
        self.win = self.props.active_window
        debug.report("checking for application window...")
        if not self.win:
            debug.report("window has not been raised yet, raising now.")
            self.win = RandomNumberFiveWindow(application=self)
        else:
            debug.report("application window already running!")
        debug.report("presenting window...")
        debug.newline()
        self.win.present()
        self.win.generate.connect("clicked", self.on_create_random)

    def on_about_action(self, widget, _):
        """Callback for the app.about action."""
        debug.report("about window requested, presenting...")
        about = Adw.AboutWindow(transient_for=self.props.active_window,
                                application_name='Random Number Five',
                                application_icon='io.github.FailurePoint.RandomNumberFive',
                                developer_name='FailurePoint',
                                version=Vstatic.version(),
                                developers=['FailurePoint'],
                                copyright='© 2023 FailurePoint',
                                website='https://github.com/FailurePoint/RandomNumberFive',
                                comments='Random number generator for For the Linux desktop!\n\n Bug Report contact: FailurePoint@proton.me',
                                debug_info=debug.get_log(),
                                release_notes=Vstatic.releasenotes(),
                                license_type=Gtk.License.GPL_3_0)
        about.present()


    def create_action(self, name, callback, shortcuts=None):
        """Add an application action.

        Args:
            name: the name of the action
            callback: the function to be called when the action is
              activated
            shortcuts: an optional list of accelerators
        """
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)
        debug.report(f'registered action {name}. shortcut = {str(shortcuts)}')

    def on_create_random(self, widget=None, _=""):
        if _ is None:
            debug.report("create random called from shortcut")
        else:
            debug.report("create random called from UI")
        debug.report("creating random number...")
        self.win.hint.set_text("")
        minv = self.win.min_val.get_value()
        maxv = self.win.max_val.get_value()
        if minv == maxv:
            already_found = self.persistant.get_int("easter-egg")
            self.win.hint.get_style_context().add_class("title-1")
            self.win.hint.set_text("")
            if already_found == 1:
                self.win.output.set_text("That's not very nice...")
            elif already_found == 2:
                self.win.output.set_text("I can't do decimals ya' know...")
            elif already_found == 3:
                self.win.output.set_text("Why??")
            elif already_found == 4:
                self.win.output.set_text("I AM NOT doing that...")
            elif already_found == 5:
                self.win.output.set_text("-_-")
            elif already_found == 6:
                self.win.output.set_text("Stop pushing that button!")
            elif already_found == 7:
                self.win.output.set_text("I am warning you!")
            elif already_found == 8:
                self.win.output.set_text("Please stop?")
            elif already_found == 9:
                self.win.output.set_text("Pretty please??")
            elif already_found == 10:
                self.win.output.set_text("Uhg. Fine, your number is:")
                random_out = random.randint(minv,maxv)
                self.win.hint.set_text(f"{random_out}... Go figure! -_-")
                debug.report(f"Number created: {random_out}")
                debug.newline()
            else:
                self.persistant.set_int("easter-egg", 0)
                self.win.output.set_text("You already found this one... :)")
            if self.persistant.get_int("easter-egg") == already_found:
                self.persistant.set_int("easter-egg", already_found + 1)
        else:
            debug.report(f"randomizer range set: {minv} - {maxv} ")
            random_out = random.randint(minv,maxv)
            self.win.hint.get_style_context().add_class("title-1")
            self.win.output.set_text("your number is:")
            self.win.hint.set_text(f"{random_out}!")
            debug.report(f"Number created: {random_out}")
            debug.newline()

    def on_reset(self, widget=None, _=""):
        debug.report("UI Reset requested, resetting...")
        self.win.hint.get_style_context().remove_class("title-1")
        self.win.output.set_text("No lucky numbers here yet...")
        self.win.hint.set_text('Try hitting the "generate" button to spin one up!')
        self.win.min_val.set_value(0)
        self.win.max_val.set_value(100)

def main(version):
    """The application's entry point."""
    app = RandomNumberFiveApplication()
    return app.run(sys.argv)
