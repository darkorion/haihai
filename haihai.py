'''
This is haihai.py, a script to transcode Hi10P MKV videos to HiP suitable for hardware players.
'''
import subprocess
import os
import copy

__author__ = "Tewi Inaba"
__copyright__ = "2012"
__credits__ = ["Tewi Inaba"]
__license__ = "New BSD"
__version__ = "1.0"
__maintainer__ = "Tewi Inaba"
__email__ = "tewi@konousa.ru"
__status__ = "Development"

# subprocess commands
# list of two lists: indexes of substituted arguments, arguments itself
# extract video track from mkv, assumes that there is only one track and it has index of 0
extract_cmd = [[2], ["mkvtoolnix/mkvextract.exe", "tracks", "%s", "0:video.264"]]
# encodes video track using 8-bit x264.exe, you can switch it with 10-bit exe and get symmetrical script that will re-encode 8-bit to 10-bit :)
encode_cmd = [[8], ['x264.exe', '--preset', 'fast', '--tune', 'animation', '--crf', '20', '--fps', '%s', '-o', 'video.8bit.264', 'video.264']]
# merges re-encoded video track into source mkv, removing old one
merge_cmd = [[2, 5], ['mkvtoolnix/mkvmerge.exe', '-o', '%s', '-d', '!0', '%s', 'video.8bit.264']]
# gets video track fps, assumptions are the same as in extract_cmd
getfps_cmd = [[1], ["mkvtoolnix/mkvfps.exe", "%s"]]


# runs external system command with parameters and without spawning window on Windows OSes
def run_cmd(cmd, params):
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
    process = subprocess.Popen(command[1], stdout=subprocess.PIPE, startupinfo=startupinfo)
    
    # we get all output from command and return it
    result = process.communicate()[0]
    return result

# main function that does recursive folder search
def job(main_dir, d):
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

            job(main_dir, job_dir)
        else:
            job_file(main_dir, d, item)

# function that re-encodes single file
# args: high-level folder, current-level folder, base file name
# example args: 10bit, chuunibyou, chuunibyou-01.mkv
def job_file(main_dir, d, f):
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

    # get fps
    # this is important, because x264.exe assumes 25 fps by default, and you MUST supply correct fps if you want syncronized a/v
    fps = run_cmd(getfps_cmd, [os.path.abspath(work_file)])
    fps = fps.strip()
    
    # extract video track for re-encoding
    print "Extracting"
    run_cmd(extract_cmd, [os.path.abspath(work_file)])
    
    # encode video track, which is a long process, but we are patient, aren't we? :)
    print "Encoding (please, be patient)"
    run_cmd(encode_cmd, [fps])
    
    # merge video track back, wiping old one
    print "Merging"
    run_cmd(merge_cmd, [output_file, work_file])

# I put my Hi10P into 10bit folder, you can use whatever you want, even absolute path
# BUT: output ALWAYS goes into 8bit subfolder near this script
job("10bit", None)

# delete leftovers
os.remove("video.264")
os.remove("video.8bit.264")
