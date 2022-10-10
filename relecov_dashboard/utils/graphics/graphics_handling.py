import subprocess


def screen_size():
    size = (None, None)
    args = ["xrandr", "-q", "-d", ":0"]
    proc = subprocess.Popen(args,stdout=subprocess.PIPE)
    for line in proc.stdout:
        if isinstance(line, bytes):
            line = line.decode("utf-8")
            if "Screen" in line:
                size = (int(line.split()[7]),  int(line.split()[9][:-1]))
    return size

def set_screen_size(size):
    adjust_percentaje = 20 # 20%
    return [size[0] - (size[0] * adjust_percentaje) / 100, size[1] - (size[1] * adjust_percentaje) / 100 ]