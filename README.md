Ichor - Inflexible CD Ripper
=====

Ichor is a Linux commandline Python script that encodes CDs to high quality MP3s.

It fetches album and track details from [MusicBrainz](https://musicbrainz.org), rips the CD with [cdparanoia](https://www.xiph.org/paranoia/), and encodes the result to MP3 with [LAME](http://lame.sf.net). If available it downloads cover art from [Cover Art Archive](https://coverartarchive.org/) and adds it to files as well as the directory.

It is inflexible and single minded in it's task. It takes no parameters, it has no options.

*Just run it, when the CD ejects it is done.*

## Ichor is not for you if ...
* Want to rip homemade compilation CDs (Ichor requires the album details to be on MusicBrainz).
* You like tweaking settings.

## Requirements
* Internet connection (fetches data from MusicBrainz and Cover Art Archive).
* Linux (tested on Linux Mint 16 Petra).
* Harddrive space ~900MBs (depends on the size of the CD to be ripped - wav files will be ripped first, then deleted as they are encoded).
* Python 2.7 (tested on Python 2.7.5).
* MusicBrainz Python modules: [musicbrainzngs](http://python-musicbrainzngs.readthedocs.org/en/latest/), [discid](http://python-discid.readthedocs.org/en/latest/).
* cdparanoia.
* LAME.

## Installation on Linux Mint / Ubuntu
Assuming Python 2.7+ is installed

1. Install pip http://pip.readthedocs.org/en/latest/installing.html
2. Install Python modules (run as root):

    ````bash
    pip install discid
    pip install musicbrainzngs
    ````
    
3. Install cdparanoia and lame (run as root):

    ````bash
    aptitude install cdparanoia lame
    ````
4. Download and save [ichor.py](https://raw.githubusercontent.com/rvavruch/ichor/master/ichor.py)
5. Make _ichor.py_ executable:

    ````bash
    chmod a+x ichor.py
    ````

## Usage
1. Insert CD.
2. Open a terminal and navigate to the directory where the MP3s should be saved to (see [File naming conventions](https://github.com/rvavruch/ichor/blob/master/README.md#file-naming-conventions--directory-structure)).
    ````bash
    cd path/to/mp3/directory
    ````

3. Run Ichor:

    ````bash
    path/to/ichor.py
    ````
    or
    
    ````bash
    python path/to/ichor.py
    ````
    
    1. If the CD is not recognised by MusicBrainz, Ichor will quit and print a URL you can use to add it to MusicBrainz. Once the CD has been added to MusicBrainz, run Ichor again.
    2. If there are multiple releases for the CD found, you will be asked to choose one. Recommedation is to choose one with cover art if everything else is the same.
4. Once Ichor is finished it will eject the CD.

## File naming conventions & directory structure
Ichor will create the following directory structure and filenames:

````bash
%artist name%/[%album year%] %album title%/%artist name% - %track number% - %track title%.mp3
````
For example:
````
The Beatles/[1964] A Hard Day's Night/The Beatles - 07 - Can't Buy Me Love.mp3
````

If there are multiple artists the track filenames will change to have the track number first:
````bash
%track number% - %artist name% - %track title%.mp3
````

If there is a [pregap track](https://en.wikipedia.org/wiki/Pregap) which is not mentioned in the track list it will be ripped as `%artist name% - 00 - Pregap.mp3` or as appropiate for multiple artists.

## LAME options
Ichor uses the LAME present _standard_ (equivalent to the old V2 preset) which encodes at VBR of ~190kps. The LAME man page says:

> This preset should generally be transparent to most people on most music and is already quite high in quality.

More information on presets from [Hydrogen Wiki](http://wiki.hydrogenaud.io/index.php?title=LAME#Recommended_settings_details).

## Rationale behind forcing the user to enter CD into MusicBrainz

When ripping a CD the track titles are either fetched from a database or entered manually.

If CD is not present in the database, the user has to enter the track titles manually, in which case they may as well add it to a communal database while they are at it.

