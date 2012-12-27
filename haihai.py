#!/usr/bin/python
#coding=utf-8

'''
This is haihai.py, a script to transcode Hi10P MKV videos to HiP suitable for hardware players.
FFMpeg branch, multiplatform
'''
import subprocess
import os
import copy
import argparse
import shlex

__author__ = "Tewi Inaba"
__copyright__ = "2012"
__credits__ = ["Tewi Inaba"]
__license__ = "New BSD"
__version__ = "1.2-ffmpeg"
__maintainer__ = "Tewi Inaba"
__email__ = "tewi@konousa.ru"
__status__ = "Development"

# subprocess commands
# encodes video track using ffmpeg
encode_cmd = ""
if os.name == "nt":
    encode_cmd = 'ffmpeg.exe -i "%s" -map 0 -c copy -c:v libx264 -preset %s -crf %d -tune %s "%s" -threads 0 -loglevel error'
else:
    encode_cmd = 'ffmpeg -i %s -map 0 -c copy -c:v libx264 -preset %s -crf %d -tune %s %s -threads 0 -loglevel error'

def run_cmd(cmd, params):
    '''
        Runs external system command with parameters and without spawning window on Windows OSes
        cmd shoud be string
        params is a list/tuple of parameters that will be used as substitutions
    '''
    command = cmd % tuple(params)
    print command

    # for Windows: disable window spawning, this also makes x264.exe output into console in which python runs — very convenient
    startupinfo = None
    if os.name == 'nt':
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, startupinfo=startupinfo)
    
    # we get all output from command and return it
    result = process.communicate()[0]
    return result

def job(main_dir, d = None, args = ()):
    '''
        Does recursive folder search, finds all MKV files and processes them
        main_dir - a dir where to start search
        args - settings for encoder
        d - None on first call, or any subfolder to limit recursion there
    '''
    if d is not None:
        work_dir = os.path.join(main_dir, d)
    else:
        work_dir = main_dir

    print work_dir

    items = os.listdir(work_dir)

    for item in items:
        if os.path.isdir(os.path.join(work_dir, item)):
            if d is not None:
                job_dir = os.path.join(d, item)
            else:
                job_dir = item

            job(main_dir, job_dir, args)
        else:
            job_file(main_dir, d, item, args)

def job_file(main_dir, d, f, args):
    '''
        Transcodes a single file
        main_dir - see job
        d - see job
        f - base file name
    '''
    if d is None:
        work_file = os.path.join(main_dir, f)
        output_file = os.path.join("8bit", f)
    else:
        work_file = os.path.join(main_dir, d, f)
        output_file = os.path.join("8bit", d, f)

    output_file = output_file.replace("_", " ")
    print "Encoding", work_file, "to", output_file

    if os.path.exists(output_file):
        print "Output file exists, skip"
        return

    # encode video track, which is a long process, but we are patient, aren't we? :)
    print "Encoding (please, be patient)"
    run_cmd(encode_cmd, (os.path.abspath(work_file), args.preset, args.crf, args.tune, os.path.abspath(output_file)))

def main():
    '''
        An example of transcoding using this module
        
        I put my Hi10P into 10bit folder, you can use whatever you want, even absolute path
        BUT: output ALWAYS goes into 8bit subfolder near this script
    '''

    # parse arguments
    parser = argparse.ArgumentParser(description='Transcode Hi10P to HiP.')
    parser.add_argument('--crf', metavar='crf', type=int, default=20,
                       help='basic quality parameter, lower is better, 24 considered default by libx264, 20 is default in haihai')
    parser.add_argument('--tune', dest='tune', type=str, default="animation",
                       help='tune libx264 for specific content, default is animation, see libx264 help for more')
    parser.add_argument('--preset', dest='preset', type=str, default="fast",
                       help='libx264 preset, default is fast, for low-quality source use medium or slow')

    args = parser.parse_args()

    job("10bit", args=args)

# you can import this module and call module functions from your scripts now
if __name__ == "__main__":
    main()