import os
import threading
import time
import sys
import glob
import string
import random
import subprocess
import shutil

threads = []
processed = {}
_isRunned = True
sound = True
rmvid = False

if not os.path.exists('Completed'):
    os.mkdir('Completed')

if not os.path.exists('Videos'):
    os.mkdir('Videos')
    print('Created folder with video, lol')
    exit(-1)

if sound:
    if not os.path.exists('Sound'):
        os.mkdir('Sound')
        print('Created dir with sound, lol')
        exit(-1)
    s = glob.glob('Sound/*.mka')

v = glob.glob('Videos/*.mkv')

ffmpeg_command = 'ffmpeg -progress - -nostats -t 5 -c:v h264_cuvid -i \"{video}\" -i \"{sound}\" -c:v hevc_nvenc -b:v 6M -maxrate:v 8M -bufsize:v 6M -y -pix_fmt yuv420p -strict -2 -c:a copy -map 0:v -map 1:a:0 -movflags +faststart \".\Completed\{video}.mp4\"'


def ff(v: str, s: str) -> None:
    thname = "".join(random.choice(string.ascii_uppercase + string.ascii_letters + string.digits) for _ in range(16))
    processed[thname] = {
        "out": None,
        "vid": v,
        "snd": s
    }
    proc = subprocess.Popen(
        args       = ffmpeg_command.format(video=v, sound=s),
        shell      = True,
        stdout     = subprocess.PIPE,
        stderr     = subprocess.STDOUT,
    )
    for line in proc.stdout:
        ln = line.decode('utf-8').replace('\n', '')
        if "frame" in ln:
            frames = ln.split('=')[-1]
            if frames.isdigit():
                processed[thname]["CompletedFrames"] = frames

    processed.pop(thname)

def logger():
    while True:
        if not _isRunned:
            break
        sys.stdout.write(f'''\rStat | Runned: {len(threads)} Threads | Processing: | {('|').join([f"{processed[data_value]['out']} |-| {processed[data_value]['vid']} + {processed[data_value]['snd']}" for data_value in [datas for datas in processed.keys()]])}''') # chr(10) == \n | Don't try understand this :D
        sys.stdout.flush()
        time.sleep(1)

def main():
    for i in range(len(v)):
        th = threading.Thread(
            target = ff,
            args   = (v[i], s[i])
        )
        threads.append(th)
        th.start()

        if len(threads) == 3:
            for th in threads:
                th.join()
                threads.remove(th)

    for th in threads:
        th.join()

    _isRunned = False

if __name__ == '__main__':
    #threading.Thread(target=logger).start()
    main()
    if rmvid:
        try:
            [os.remove(vid) for vid in v]
        except Exception as err:
            print(f'Error while deleting folder with video: {err}')

