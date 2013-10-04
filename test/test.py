#!/usr/bin/python
import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'libs'))
from client import MozClient
from fxui import MozUI


client = MozClient("localhost", 6000)
ui = MozUI(client)
#print ui.getStyleSheetsForApp("app://settings.gaiamobile.org/manifest.webapp")
#tab = ui.getSelectedTab()
#ss = tab.getStyleSheets()
#print ss[0].href

#res = client.send({'to':'root', 'type': 'listTabs'})
#print res
#browserActor = res["chromeDebugger"]
#styleEditorActor = res["tabs"][2]["styleEditorActor"]
#res = client.send({'to':styleEditorActor, 'type':"getStyleSheets"})
##print res["styleSheets"][0]
#styleSheetActor = res["styleSheets"][0]["actor"]
##client.send({'to':styleSheetActor, 'type':"update", 'text':"", "transition":True})
#res = client.send({'to':styleSheetActor, 'type':"fetchSource"})
#res = client.receive()
#print res["source"]
##self.view.insert(edit, 0, res["styleSheets"][0])
