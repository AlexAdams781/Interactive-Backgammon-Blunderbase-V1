import subprocess
import xgid

def get_cube_stats(line):
    print("running process ", line)
    process = subprocess.Popen(['gnubg/gnubg-cli.exe', '-q'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    inp = "set xgid " + line + "\nhint\nexit"
    stdout, stderr = process.communicate(input=inp.encode('utf-8'))
    print("Stdout:", stdout.decode().splitlines()[26:])
    return stdout.decode().splitlines()[26:]

def get_checker_stats(line, max_moves):
    process = subprocess.Popen(['gnubg/gnubg-cli.exe', '-q'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    inp = "set xgid " + line + "\nhint\nexit"
    stdout, stderr = process.communicate(input=inp.encode('utf-8'))
    if not max_moves: max_moves = 3
    lines = stdout.decode().splitlines()
    last_line = min(len(lines), 24 + max_moves * 3)
    print("Stdout:", lines[24 : last_line])
    return lines[24 : last_line]

def get_stats(line, max_moves=None):
    print("getting stats")
    full_board = xgid.extract_xgid(line)
    if full_board.dice == '00':
        return get_cube_stats(line)

    return get_checker_stats(line, max_moves)

get_stats("XGID=----a-E-D---fD---B-b-bb-b-:0:0:1:54:3:1:0:5:6", max_moves=5)
