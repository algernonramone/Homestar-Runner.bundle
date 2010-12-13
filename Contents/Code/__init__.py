####################################################################################################

PREFIX = '/video/homestarrunner'
TITLE  = 'Homestar Runner'
ART    = 'art-default.jpg'
ICON   = 'icon-default.png'

####################################################################################################

def Start():

  Plugin.AddPrefixHandler(PREFIX, MainMenu, TITLE, ICON, ART)
  Plugin.AddViewGroup('List', viewMode='List', mediaType='items')

  # Set the default MediaContainer attributes
  MediaContainer.title1 = TITLE
  MediaContainer.viewGroup = 'List'
  MediaContainer.art = R(ART)
  DirectoryItem.thumb = R(ICON)
  WebVideoItem.thumb = R(ICON)

  HTTP.CacheTime = 7200

####################################################################################################

def MainMenu():

  dir = MediaContainer()

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

def AddSeries(sender, series_id=None, thumb=None):

  dir = MediaContainer()

  thisXML = HTML.ElementFromURL('http://www.homestarrunner.com/rando.xml')

  emailCount = 0

  for child in thisXML:
    if child.tag == series_id:
      emailCount = emailCount + 1
      if child.get('u'):
        thisURL = 'http://www.homestarrunner.com/' + child.get('u')
      else:
        thisURL = 'http://www.homestarrunner.com/sbemail' + str(emailCount) + '.html'
      dir.Append(WebVideoItem(url = thisURL, title = str(emailCount) + ': ' + child.get('n'), thumb = thumb))

  # reverse the order to put the most recent items first
  dir.Reverse()

  return dir

####################################################################################################
