Ichor - Inflexible CD Ripper
=====

Ichor is a Python script that encodes CDs to high quality MP3s.

It uses the [MusicBrainz](https://musicbrainz.org) database get album and track details for the CD, [cdparanoia](https://www.xiph.org/paranoia/) to rip the CD tracks to wav files, and finally [Lame](http://lame.sf.net) to encode the wav files to MP3.

It is inflexible in that it takes no parameters, it has no options. You just run it and it does it's thing. This simplifies the experience but some users may find it limiting.


## Requirements
* Linux (tested in Linux Mint 16 Petra)
* Python 2.7
* MusicBrainz Python modules: musicbrainzngs, discid
* cdparanoia
* lame

## Installation




