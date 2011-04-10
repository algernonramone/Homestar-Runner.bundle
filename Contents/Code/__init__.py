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

  dir = MediaContainer(title2=sender.itemTitle)

  data = HTTP.Request('http://www.homestarrunner.com/rando.xml').content
  #Rebuild the crappy XML as JSON
  data = data.strip('<?xml version="1.0" encoding="iso-8859-1"?>')
  data = data.replace('<!-- teen girl squad tgs-->', '').replace('<!-- answering machines am-->','').replace('<!-- shorts sh-->','').replace('<!-- big toons t-->','').replace('<!--holiday ho-->','').replace('<!--puppet stuff p-->','').replace('<!--- cheat stuff teh-->','').replace('<!-- sbemail sb-->','')
  data = data.replace('<','{').replace('{!', '<!').replace('/>', '},').replace(' n=', ' "n":').replace(' u=', ', "u":').replace(' s=', ', "s":').replace(' new=',', "new":')
  data = data.replace('{tgs ', '{"id":"tgs", ').replace('{am ', '{"id":"am", ').replace('{sh ', '{"id":"sh", ').replace('{t ', '{"id":"t", ').replace('{ho ', '{"id":"ho", ')
  data = data.replace('{p ', '{"id":"p", ').replace('{teh ', '{"id":"teh", ').replace('{sb ', '{"id":"sb", ')
  data = '[%s\n]' % data[:-3]
  #parse the brand new JSON
  thisJSON = JSON.ObjectFromString(data)
  

  emailCount = 0
  
  for vid in thisJSON:
    if vid['id'] == series_id:
      emailCount = emailCount + 1
      try:
        if vid['u']:
          thisURL = 'http://www.homestarrunner.com/%s' % vid['u']
      except:
        thisURL = 'http://www.homestarrunner.com/sbemail%d.html' % emailCount
      dir.Append(WebVideoItem(url = thisURL, title = str(emailCount) + ': ' + vid['n'], thumb = thumb))

  if len(dir) == 0:
    return MessageContainer("Empty", "There aren't any items")
  else:
    # reverse the order to put the most recent items first
    dir.Reverse()
    return dir

####################################################################################################
