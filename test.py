from client import MarionetteClient


client = MarionetteClient("localhost", 6000)
res = client.send({'to':'root', 'type': 'listTabs'})
browserActor = res["chromeDebugger"]
#styleEditorActor = res["tabs"][2]["styleEditorActor"]
#res = client.send({'to':styleEditorActor, 'type':"getStyleSheets"})
##print res["styleSheets"][0]
#styleSheetActor = res["styleSheets"][0]["actor"]
##client.send({'to':styleSheetActor, 'type':"update", 'text':"", "transition":True})
#res = client.send({'to':styleSheetActor, 'type':"fetchSource"})
#res = client.receive()
#print res["source"]
##self.view.insert(edit, 0, res["styleSheets"][0])
