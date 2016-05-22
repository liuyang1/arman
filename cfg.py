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
               '-show_frames']
ffprobelist = [i + ' -print_format json' for i in ffprobelist]
cmd['ffprobe'] = ffprobelist
