class MozUI(object):
    def __init__(self, client):
        self.client = client

    def getTabList(self):
        res = self.client.send({'to':'root', 'type': 'listTabs'})
        l = [MozTab(self.client, t["url"], t["title"], t["styleEditorActor"], False) for t in res["tabs"]] 
        l[res["selected"]].selected = True
        return l

    def getSelectedTab(self):
        tabs = self.getTabList()
        return [t for t in tabs if t.selected == True][0]

class MozTab(object):
    def __init__(self, client, url, title, actor, selected):
      self.client = client
      self.url = url
      self.title = title
      self.actor = actor
      self.selected = selected
    def __str__(self):
      s = "MozTab:"
      s += "\n  url:     " + self.url
      s += "\n  title:   " + self.title
      if self.selected:
        s += "\n  selected"
      return s
    __repr__ = __str__
    def getStyleSheets(self):
      res = self.client.send({'to':self.actor, 'type': 'getStyleSheets'})
      d = [{"actor":s["actor"], "href":s["href"], "disabled":s["disabled"]} for s in res["styleSheets"]]
      d = [s for s in d if not s["disabled"]] #Filter our disabled styleSeets
      return [MozStyleSheet(self.client, s["actor"], s["href"]) for s in d]

class MozStyleSheet(object):
    def __init__(self, client, actor, href):
      self.client = client
      self.actor = actor
      self.href = href
    def __str__(self):
      return "MozStyleSheet: " + self.href
    __repr__ = __str__
    def getSource(self):
      self.client.send({'to':self.actor, 'type':"getText"})
      res = self.client.receive()
      return res["source"]
    def pushSource(self, text, transition):
      self.client.send({'to':self.actor,'type':"update",'text': text,"transition":transition})

