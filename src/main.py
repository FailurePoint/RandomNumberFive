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


class RandomNumberFiveApplication(Adw.Application):
    """The main application singleton class."""

    def __init__(self):
        super().__init__(application_id='io.github.FailurePoint.RandomNumberFive',
                         flags=Gio.ApplicationFlags.DEFAULT_FLAGS)
        self.create_action('quit', lambda *_: self.quit(), ['<primary>q'])
        self.create_action('about', self.on_about_action)
        self.create_action('preferences', self.on_preferences_action)
        self.create_action('new_random', self.on_create_random, ['<primary>r'])
        self.create_action('reset', self.on_reset, ['<primary><shift>r'])


    def do_activate(self):
        """Called when the application is activated.

        We raise the application's main window, creating it if
        necessary.
        """
        self.win = self.props.active_window
        if not self.win:
            self.win = RandomNumberFiveWindow(application=self)
        self.win.present()
        self.win.generate.connect("clicked", self.on_create_random)

    def on_about_action(self, widget, _):
        """Callback for the app.about action."""
        about = Adw.AboutWindow(transient_for=self.props.active_window,
                                application_name='Random Number Five',
                                application_icon='io.github.FailurePoint.RandomNumberFive',
                                developer_name='FailurePoint',
                                version='0.1.0',
                                developers=['FailurePoint'],
                                copyright='© 2023 FailurePoint')
        about.present()

    def on_preferences_action(self, widget, _):
        """Callback for the app.preferences action."""
        print('app.preferences action activated')

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

    def on_create_random(self, widget=None, _=""):
        self.win.hint.set_text("")
        minv = self.win.min_val.get_value()
        maxv = self.win.max_val.get_value()
        print(minv, maxv)
        random_out = random.randint(minv,maxv)
        self.win.hint.get_style_context().add_class("title-1")
        self.win.output.set_text("your number is:")
        self.win.hint.set_text(f"{random_out}!")
        print(random_out)

    def on_reset(self, widget=None, _=""):
        self.win.hint.get_style_context().remove_class("title-1")
        self.win.output.set_text("No lucky numbers here yet...")
        self.win.hint.set_text('Try hitting the "generate" button to spin one up!')
        self.win.min_val.set_value(0)
        self.win.max_val.set_value(100)

def main(version):
    """The application's entry point."""
    app = RandomNumberFiveApplication()
    return app.run(sys.argv)
