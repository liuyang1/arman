# cfg
alias = {}
alias['ts'] = ['mpeg', 'mpg', 'trp']
alias['mp4'] = ['m4v']
alias['mkv'] = ['webm']

# config based on ext
checker = {}
checker['ts'] = ['ffprobe', 'mediainfo']
checker['mp4'] = ['ffprobe']

# command table
cmd = {}
ffprobelist = ['-show_format',
               '-show_programs',
               '-show_streams',
               '-show_chapters',
               # '-show_frames'
               ]
ffprobelist = [i + ' -print_format json' for i in ffprobelist]
cmd['ffprobe'] = ffprobelist

ignoreExtLst = ['.log', '.xxd', '.info', '.nfo']
# cfg done


import os
import json
import subprocess
import os.path


def is_folder_to_ignore(d):
    lastdir = os.path.basename(d)
    return lastdir[0] == '.' and len(lastdir) > 1


def loadfilelst(d):
    lst = []
    for root, dirs, files in os.walk(d):
        dirs[:] = [i for i in dirs if not is_folder_to_ignore(i)]
        lst += [os.path.abspath("%s/%s" % (root, f)) for f in files]
    lst = [f for f in lst if os.path.splitext(f)[1] not in ignoreExtLst]
    return lst


def loadHistory(f):
    try:
        with open(f) as fp:
            data = json.load(fp)
        return data
    except IOError:
        print("No history file: %s" % (f))
        return None


def md5sum(f):
    cmd = ['md5sum', f]
    try:
        out = subprocess.check_output(cmd)
    except subprocess.CalledProcessError:
        print("failed md5sum on file: %s" % (f))
        return ""
    out = out.decode('UTF-8')
    line = out.split("\n")[0]
    ret = line.split()[0]
    return ret


def crc32(f):
    cmd = ['crc32', f]
    out = subprocess.check_output(cmd)
    out = out.decode('UTF-8')
    line = out.split("\n")[0]
    return line


def ffprobe_unit(f, opt="-show_format -print_format json"):
    cmd = ['ffprobe'] + opt.split() + [f]
    fp = open("/dev/null", "w")
    out = subprocess.check_output(cmd, stderr=fp)
    fp.close()
    out = out.decode('UTF-8')
    ret = json.loads(out)
    return ret


def ffprobe(f):
    ret = {opt: ffprobe_unit(f, opt) for opt in cmd['ffprobe']}
    return ret



d = "test"
lst = loadfilelst(d)
print(lst)
hist = loadHistory(".arman.history")
print(hist)
hashTbl = {}
for f in lst:
    crc = crc32(f)
    if crc == "":
        continue
    dct = {}
    dct['filename'] = f
    dct['ffprobe'] = ffprobe(f)
    hashTbl[crc] = dct
print(hashTbl)
for hsh, f in hashTbl.items():
    print(hsh)
    print(json.dumps(f, indent=4))
