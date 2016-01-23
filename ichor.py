#!/usr/bin/python
import sys, subprocess, shlex, os

import discid
import musicbrainzngs


# Script details
scriptName = "Ichor" # The inflexible CD ripper
scriptVersion = '2.3.0' # see changelog.md for details
scriptURL = 'https://github.com/rvavruch/ichor'
print "%s %s (%s) thinks you're neat!" % (scriptName, scriptVersion, scriptURL)



# get Audio CD details
try:
    disc = discid.read()        # reads from default device
except discid.DiscError, e:
    if str(e) == u'cannot read table of contents':
        print 'Could not read CD.'
    sys.exit(1)



# try to find Audio CD match on MusicBrainz
musicbrainzngs.set_useragent(scriptName, scriptVersion, scriptURL)

try:
    discReleases = musicbrainzngs.get_releases_by_discid(disc.id, ['artist-credits', 'recordings'], disc.toc_string, False)
except:
    print sys.exc_info()
    sys.exit(2)

try:
    discReleases['disc']
    releaseList = discReleases['disc']['release-list']
except:
    try:
        discReleases['release-list']
        releaseList = discReleases['release-list']
    except:
        print releaseList
        print sys.exc_info()
        sys.exit(2)

numberOfReleases = len(releaseList)

if numberOfReleases == 0:
    print "This CD is not yet in the MusicBrainz database."
    print "To continue please add it using the following link:", disc.submission_url
    sys.exit(0)
elif numberOfReleases > 1:
    # if there are multiple releases allow the user to choose one
    print
    print "Multiple releases, choose one:\n"

    releaseIdx = 1
    for release in releaseList:
        print '#' + str(releaseIdx)
        print "Artist:", release['artist-credit-phrase']
        print "Title:", release['title']
        print "Country:", release['country']
        print "Date:", release['date']
        if release['cover-art-archive']['front'] != 'false':
            print "Cover art: Yes"
        else:
            print "Cover art: No"
        print "Barcode:", release['barcode']
        try:
            release['disambiguation']
        except KeyError:
            release['disambiguation'] = 'None'
        
        if release['disambiguation'] != 'None':
            print "Disambiguation:", release['disambiguation']
        
        releaseIdx += 1
        print
    
    releaseChoice = 0
    releaseOptions = range(1, numberOfReleases+1)
    
    while releaseChoice not in releaseOptions:
        userInput = raw_input('Enter release number [1-' + str(numberOfReleases) + ']: ')
        try:
            releaseChoice = int(userInput)
        except:
            releaseChoice = 0
    
    releaseChoice -= 1
    selectedRelease = releaseList[releaseChoice]
else:
    selectedRelease = releaseList[0]



# determine the number of artists credited
numberOfArtists = len(selectedRelease['artist-credit'])
isSingleArtist = not(numberOfArtists > 1 or selectedRelease['artist-credit'][0]['artist']['id'] == '89ad4ac3-39f7-470e-963a-56509c546377') # more than one artist credited or 'Various Artists'



# create mp3 directory and change into it
artist = selectedRelease['artist-credit'][0]['artist']['sort-name']
fsSafeArtist = artist.replace("/", "_")
albumTitle = selectedRelease['title']
fsSafeAlbumTitle = albumTitle.replace("/", "_")

print "Ripping: %s - %s\n" % (artist, albumTitle) # just for interests sake

try:
    date = selectedRelease['release-event-list'][0]['date']
except:
    date = '0000'

year = int(date[0:4]) # only need first 4 characters, ie. the year


mp3dirname = "%s/[%d] %s" % (fsSafeArtist, year, fsSafeAlbumTitle)

try:
    os.makedirs(mp3dirname)
except OSError, e:
    # if not that the directory already exists
    if sys.exc_info()[1][0] != 17:
        print e
        sys.exit(1)
    
os.chdir(mp3dirname)



# rip CD to wav
command = 'cdparanoia -B'
status = subprocess.call(shlex.split(command))

if status != 0:
    print "Ripping failed!"
    print command
    sys.exit(1)



# Convert all wavs to mp3, and if successful delete wav file
ll = sorted(os.listdir("."))

comment = "Ripped with %s v%s (%s)" % (scriptName, scriptVersion, scriptURL)
tracks = selectedRelease['medium-list'][0]['track-list']
i = 0
for wav in ll:
    if wav.endswith('cdda.wav') and os.path.isfile(wav):
    	
        trackData = tracks[i]
        trackNum = int(trackData['number'])
        artist = trackData['recording']['artist-credit-phrase'].replace('"', "\\\"").replace("'", "\'")
        title = trackData['recording']['title'].replace('"', "\\\"").replace("'", "\'")

        # if unknown pregap, compress it but don't use track names
        if wav != 'track00.cdda.wav' or (wav == 'track00.cdda.wav' and trackNum == 0):
            i+=1
        else:
            trackNum = 0
            title = 'Pregap'
        
        fsSafeTitle = title.replace("/", "_")

        # if not single artist put track number in front
        if isSingleArtist:
            trackName = "%s - %02d - %s.mp3" % (fsSafeArtist, trackNum, fsSafeTitle)
        else:
            trackName = "%02d - %s - %s.mp3" % (trackNum, fsSafeArtist, fsSafeTitle)
            
        lamecmd = 'lame --preset standard --ta "%s" --tn %d --tt "%s" --tl "%s" --ty "%d" --tc "%s" "%s" "%s"' % (artist, trackNum, title, albumTitle, year, comment, wav, trackName)

        lamecmd = lamecmd.encode('utf8')

        status = subprocess.call(shlex.split(lamecmd))
        
        # if success delete wav file
        if status == 0:
            os.remove(wav)
        else:
            print "Encoding failed!"
            print lamecmd
            sys.exit(1)



# Download cover art if available
if selectedRelease['cover-art-archive']['front'] != 'false':
    frontURL = "http://coverartarchive.org/release/%s/front" % (selectedRelease['id'])
    wgetcmd = "wget --progress=bar --output-document=Folder.jpg %s" % (frontURL)
    status = subprocess.call(shlex.split(wgetcmd))
    
    # if not success
    if status != 0:
        print "Cover art download failed"
        print wgetcmd
        sys.exit(1)



# Done - eject CD to indicate process finished
status = subprocess.call(shlex.split("eject"))

if status != 0:
    print "Failed to eject!"
    sys.exit(1)
