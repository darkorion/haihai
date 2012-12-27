﻿はいはい (haihai)
======

Script to convert H264 Hi10P MKV to HiP MKV preserving original MKV content (except for original video track of course).

Nice page [here](http://fuwaneko.github.com/haihai/).

Discussion
======

[On Google+](https://plus.google.com/107252355899172817272)

FFMpeg branch
======

Now FFMpeg branch is available for Windows/Linux/MacOSX users.

0. Clone FFMpeg branch or download archive and extract it.
1. Get FFMpeg. Linux users already have it or can use package manager. Windows users can download **static** build [here](http://ffmpeg.zeranoe.com/builds/), extract ffmpeg.exe near haihai.py.
2. Get Python. Linux users already have it or can use package manager. Windows users can download [here](http://www.python.org).
3. Put videos into 10bit folder near haihai.py with any folder structure you want.
4. Open command-line prompt.
5. Run haihai.py --help to see available options.
6. Run haihai.py if you're okay with defaults or provide your options.

FFMpeg branch does not show encoding progress, but you can remove “-loglevel error” and turn it on.

FFMpeg branch will not become main, as I prefer x264 and stuff. But it will be updated with new features, probably ones I don't need, but you requested.

Main branch will remain Windows-only from now on and probably will not be updated, as I am fully satisfied with it.

Mac OS X users can also download ffmpeg binaries for Mac and use FFMpeg branch script. Python is installed by default in Mac OS X.

In theory it's possible to use FFMpeg branch even on smartphones/tablets with ARM processors. But encoding will bee sllloooooooowwwwww.

Installation
======

For main branch only (Windows).

1. Get [Python](http://www.python.org), get [mkvtoolnix](http://www.bunkus.org/videotools/mkvtoolnix/), get mkvfps.exe from [here](http://konousa.ru/mkvfps.exe), get [x264 8-bit version](http://www.x264.nl).
2. Clone main branch.
3. Put mkvtoolnix exes to mkvtoolnix subfolder.
4. Put x264.exe near haihai.py.
5. Put some Hi10P files into 10bit subfolder.
6. Run haihai.py.

Fuck this, I want binaries!
======

[For Windows only](http://konousa.ru/10to8.7z), other OSes don't need binaries.

Whaaa, I can't unpack!
------

Use [7-zip](http://www.7-zip.org) and stop pirating WinRAR.

Linux/MacOSX?
======

Yes, see FFMpeg branch.

Advanced
======

You can put Hi10P in subfolders and script will preserve them. That's what it was created for :)

You can select different encoding options for x264:

* --preset (ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow, placebo), defines overall quality. Slower means better. Default is fast.
* --crf (0-50), defines constant quality. Lower is better, 0 is lossless (not recommended). Default is 20.
* --tune (film, animation, grain, stillimage, psnr, ssim, fastdecode, zerolatency), source optimizations. Default is animation.

On Windows install py2exe for python and generate haihai.exe for use w/o Python via setup.py py2exe.

Gui?
======

No. This is batch processing script made to be as autonomous as possible (run and forget). Gui is not needed.

What's with the name?
======

Roughly Japanese “yesyes” (but actually means nothing :), comes from **Hi**10P + **Hi**P.