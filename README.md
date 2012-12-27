﻿はいはい (haihai)
======

Script to convert H264 Hi10P MKV to HiP MKV preserving original MKV content (except for original video track of course).

Discussion
======

[On Google+](https://plus.google.com/107252355899172817272)

Issues
======

Script assumes that video track in MKV has index of 0. Will be fixed soon.

Installation
======

1. Get Python, get mkvtoolnix, get mkvfps.exe from [here](http://konousa.ru/mkvfps.exe), get x264 8-bit version
2. Clone repo
3. Put mkvtoolnix exes to mkvtoolnix subfolder
4. Put x264.exe near haihai.py
5. Put some Hi10P files into 10bit subfolder
6. Run haihai.py

Fuck this, I want binaries!
======

No problem, get it [here](http://konousa.ru/10to8.7z).

1. Put videos into 10bit folder (create it)
2. Run haihai.exe and you're good

Linux?
======

Soon. For now you can use Wine — it works.

Advanced
======

You can put Hi10P in subfolders and script will preserve them. That's what it was created for :)

Gui?
======

No. This is batch processing script made to be as autonomous as possible (run and forget). Gui is not needed.

Options
======

You can play with x264 settings to produce different quality files

Install py2exe for python and generate haihai.exe for use w/o Python via setup.py py2exe

What's with the name?
======

Roughly Japanese “yesyes”, comes from **Hi**10P + **Hi**P.