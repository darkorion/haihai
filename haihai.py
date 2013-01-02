#!/usr/bin/python
#coding=utf-8

'''
This is haihai.py, a script to transcode Hi10P MKV videos to HiP suitable for hardware players.
'''
import subprocess
import os
import copy
import argparse
from decimal import *

__author__ = "Tewi Inaba"
__copyright__ = "2012"
__credits__ = ["Tewi Inaba"]
__license__ = "New BSD"
__version__ = "1.2"
__maintainer__ = "Tewi Inaba"
__email__ = "tewi@konousa.ru"
__status__ = "Development"

# subprocess commands
# list of two lists: indexes of substituted arguments, arguments itself
# extract video track from mkv, assumes that there is only one video track
extract_cmd = [[2, 3], ["mkvtoolnix/mkvextract.exe", "tracks", "%s", "%s:video.264"]]
# encodes video track using 8-bit x264.exe, you can switch it with 10-bit exe and get symmetrical script that will transcode 8-bit to 10-bit :)
encode_cmd = [[8], ['x264.exe', '--preset', '%s', '--tune', '%s', '--crf', '%i', '--fps', '%s', '-o', 'video.8bit.264', 'video.264']]
# merges transcoded video track into source mkv, removing old one
merge_cmd = [[2, 4, 5], ['mkvtoolnix/mkvmerge.exe', '-o', '%s', '-d', '!%s', '%s', 'video.8bit.264']]
# gets video track fps and video track number
getfps_cmd = [[1], ["mkvtoolnix/mkvfps.exe", "%s"]]


def run_cmd(cmd, params):
    '''
        Runs external system command with parameters and without spawning window on Windows OSes
        cmd shoud be list of two lists:
         - first list contains indexes of substituted arguments
         - second list contains list of arguments
        params is a list of parameters that will be used as substitutions
    '''
    command = copy.deepcopy(cmd)
    j = 0
    for i in command[0]:
        command[1][i] = command[1][i] % params[j]
        j += 1

    # for Windows: disable window spawning, this also makes x264.exe output into console in which python runs — very convenient
    startupinfo = None
    if os.name == 'nt':
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    print(" ".join(command[1]))
    process = subprocess.Popen(command[1], stdout=subprocess.PIPE, startupinfo=startupinfo)
    
    # we get all output from command and return it
    result = process.communicate()[0]
    return result

def job(main_dir, d = None):
    '''
        Does recursive folder search, finds all MKV files and processes them
        main_dir - a dir where to start search
        d - None on first call, or any subfolder to limit recursion there
    '''
    if d is not None:
        work_dir = os.path.join(main_dir, d)
    else:
        work_dir = main_dir

    print (work_dir)

    items = os.listdir(work_dir)

    for item in items:
        if os.path.isdir(os.path.join(work_dir, item)):
            if d is not None:
                job_dir = os.path.join(d, item)
            else:
                job_dir = item

            job(main_dir, job_dir)
        else:
            job_file(main_dir, d, item)

def job_file(main_dir, d, f):
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
    print ("Encoding", work_file, "to", output_file)

    if os.path.exists(output_file):
        print ("Output file exists, skip")
        return

    # get fps and track number
    # this is important, because x264.exe assumes 25 fps by default, and you MUST supply correct fps if you want syncronized a/v
    fps = run_cmd(getfps_cmd, [os.path.abspath(work_file)])
    # fps is [track, fps]
    fps = str(fps).strip().replace("'","").replace("b","").split(" ")
    
    # extract video track for re-encoding
    print ("Extracting")
    run_cmd(extract_cmd, [os.path.abspath(work_file), fps[0]])

    # encode video track, which is a long process, but we are patient, aren't we? :)
    print ("Encoding (please, be patient)")

    run_cmd(encode_cmd, [fps[1]])
    
    # merge video track back, wiping old one
    print ("Merging")
    run_cmd(merge_cmd, [output_file, fps[0], work_file])

def main():
    '''
        An example of transcoding using this module
        
        I put my Hi10P into 10bit folder, you can use whatever you want, even absolute path
        BUT: output ALWAYS goes into 8bit subfolder near this script
    '''

    # parse arguments
    parser = argparse.ArgumentParser(description='Transcode Hi10P to HiP.')
    parser.add_argument('--crf', metavar='crf', type=int, default=20,
                       help='basic quality parameter, lower is better, 24 considered default by x264, 20 is default in haihai')
    parser.add_argument('--tune', dest='tune', type=str, default="animation",
                       help='tune x264 for specific content, default is animation, see x264 help for more')
    parser.add_argument('--preset', dest='preset', type=str, default="fast",
                       help='x264 preset, default is fast, for low-quality source use medium or slow')

    args = parser.parse_args()

    # build encode command based on arguments
    encode_cmd[1][2] = encode_cmd[1][2] % args.preset
    encode_cmd[1][4] = encode_cmd[1][4] % args.tune
    encode_cmd[1][6] = encode_cmd[1][6] % args.crf

    job("10bit", None)

    # delete leftovers
    if os.path.exists("video.264"):
        os.remove("video.264")
    if os.path.exists("video.8bit.264"):
        os.remove("video.8bit.264")

# you can import this module and call module functions from your scripts now
if __name__ == "__main__":
    main()
