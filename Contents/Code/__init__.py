####################################################################################################

HOMESTAR_PREFIX = "/video/homestarrunner"
ART             = 'art-default.png'
ICON            = 'icon-default.png'

####################################################################################################

#class HRMenuContainer(MediaContainer):
#  def __init__(self, art = "art-default.png", viewGroup = "Menu", title1 = None, title2 = None, noHistory = False, replaceParent = False):
#    if title1 is None:
#      title1 = "Homestar Runner"
#    MediaContainer.__init__(self, art = R(art), viewGroup = viewGroup, title1 = title1, title2 = title2, noHistory = noHistory, replaceParent = replaceParent)
    
####################################################################################################

def Start():

  HTTP.CacheTime = 7200
  Plugin.AddPrefixHandler(HOMESTAR_PREFIX, MainMenu, "Homestar Runner", "icon-default.png", "art-default.png")
  Plugin.AddViewGroup("Menu", viewMode = "List", mediaType = "items")

  MediaContainer.art = R(ART)

####################################################################################################

def MainMenu():
  
  dir = MediaContainer(title1 = "Homestar Runner", viewGroup='InfoList')
  
  dir.Append(Function(DirectoryItem(AddSeries, title = "Strong Bad Emails", thumb = R("icon-strongbademails.png")), series_id = "sb", thumb = R("icon-strongbademails.png")))
  dir.Append(Function(DirectoryItem(AddSeries, title = "Teen Girl Squad", thumb = R("icon-teengirlsquad.png")), series_id = "tgs", thumb = R("icon-teengirlsquad.png")))
  dir.Append(Function(DirectoryItem(AddSeries, title = "Answering Machines", thumb = R("icon-answeringmachine.png")), series_id = "am", thumb = R("icon-answeringmachine.png")))
  dir.Append(Function(DirectoryItem(AddSeries, title = "Shorts", thumb = R("icon-shorts.png")), series_id = "sh", thumb = R("icon-shorts.png")))
  dir.Append(Function(DirectoryItem(AddSeries, title = "Toons", thumb = R("icon-toons.png")), series_id = "t", thumb = R("icon-toons.png")))
  dir.Append(Function(DirectoryItem(AddSeries, title = "Holiday", thumb = R("icon-holiday.png")), series_id = "ho", thumb = R("icon-holiday.png")))
  dir.Append(Function(DirectoryItem(AddSeries, title = "Puppet Stuff", thumb = R("icon-puppetstuff.png")), series_id = "p", thumb = R("icon-puppetstuff.png")))
  dir.Append(Function(DirectoryItem(AddSeries, title = "Powered by The Cheat", thumb = R("icon-poweredbythecheat.png")), series_id = "teh", thumb = R("icon-poweredbythecheat.png")))
  
  return dir

####################################################################################################

def AddSeries(sender, query = None, series_id = None, thumb = None):

  dir = MediaContainer(title1 = sender.itemTitle, viewGroup='InfoList')

  thisXML = XML.ElementFromURL("http://www.homestarrunner.com/rando.xml", isHTML = True)

  emailCount = 0

  for child in thisXML:
    if child.tag == series_id:
      emailCount = emailCount + 1
      if child.get("u"):
        thisURL = "http://www.homestarrunner.com/" + child.get("u")
      else:
        thisURL = "http://www.homestarrunner.com/sbemail" + str(emailCount) + ".html"
      dir.Append(WebVideoItem(url = thisURL, title = str(emailCount) + ": " + child.get("n"), duration = 0, thumb = thumb))
      
  # reverse the order to put the most recent items first
  dir.Reverse()
      
  return dir
  
####################################################################################################
