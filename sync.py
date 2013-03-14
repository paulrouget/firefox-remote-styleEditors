import sublime, sublime_plugin
from client import MarionetteClient

mozClient = None
mozStyleSheetActor = None
mozLastChange = 0;

class FirefoxCssCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    global mozClient, mozStyleSheetActor

    mozClient = MarionetteClient("localhost", 6000)

    res = mozClient.send({'to':'root', 'type': 'listTabs'})
    styleEditorActor = res["tabs"][2]["styleEditorActor"]
    res = mozClient.send({'to':styleEditorActor, 'type':"getStyleSheets"})

    mozStyleSheetActor = res["styleSheets"][0]["actor"]

    res = mozClient.send({'to':mozStyleSheetActor, 'type':"fetchSource"})
    res = mozClient.receive()
    self.view.insert(edit, 0, res["source"])
    self.view.set_syntax_file('Packages/CSS/CSS.tmLanguage')

class TrailingSpacesListener(sublime_plugin.EventListener):
  def on_modified(self, view):
    global mozClient, mozStyleSheetActor
    text = view.substr(sublime.Region(0, view.size()))
    mozClient.send({'to':mozStyleSheetActor,'type':"update",'text': text,"transition":True})



