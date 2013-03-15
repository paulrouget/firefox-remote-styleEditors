#FIXME
# What about inline styles?

######### DEBUG
import sys
sys.dont_write_bytecode = True
######### /DEBUG

import os, sys, threading
sys.path.append(os.path.join(os.path.dirname(__file__), 'libs'))

import sublime, sublime_plugin
from client import MozClient
from fxui import MozUI
from urlparse import urlparse
from os.path import splitext, basename

threads = {}
stylesheets = {}

class FirefoxCssCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    if hasattr(self, 'ss'):
      # Already synced
      print "Can't resync"
      return

    self.edit = edit

    client = MozClient("localhost", 6000)
    ui = MozUI(client)
    tab = ui.getSelectedTab()
    self.ss = tab.getStyleSheets()

    self.view.set_status("firefox-sync", "fx:connected")
    #FIXME: when do we hide that? No disconnected event yet.

    urls = [basename(urlparse(s.href).path) for s in self.ss]
    sublime.active_window().show_quick_panel(urls, self.on_chosen)

  def on_chosen(self, idx):
    global threads, stylesheets

    s = self.ss[idx]
    self.view.set_syntax_file('Packages/CSS/CSS.tmLanguage')
    self.view.insert(self.edit, 0, s.getSource())

    self.edit = None

    id = self.view.buffer_id()

    stylesheets[id] = s

    return

class ModificationListener(sublime_plugin.EventListener):
  def on_modified(self, view):
    global pushers

    if view.is_loading():
      print "not pushing: style loading"
      return

    id = view.buffer_id()

    if not id in stylesheets:
      print "not pushing: not tracking this view"
      return

    if id in threads and threads[id].isAlive():
      print "not pushing: a thread is pending"
      return

    text = view.substr(sublime.Region(0, view.size()))

    threads[id] = FirefoxCssPusher(stylesheets[id], text)
    print "pushing"
    return

class FirefoxCssPusher(threading.Thread):
  def __init__(self, stylesheet, text):
    self.stylesheet = stylesheet
    self.text = text
    threading.Thread.__init__(self)
    self.start()
  def run(self):
    self.stylesheet.pushSource(self.text, True)

