import os
import sys
import xgid

class Filter:
    def __init__(self, entry, val, exists, parent):
        self.entry = entry
        self.val = val
        self.exists = exists
        self.sub_entries = dict()
        self.parent = parent
        self.xgid = ""

    def print_filter(self, depth):
        tabs = "\t" * depth
        print(tabs + "Entry =", self.entry, "Val = ", self.val, "Exists = ", self.exists, self.xgid)
        for node in self.sub_entries:
            self.sub_entries[node].print_filter(depth + 1)

def get_checkers_in_zone(board):
    checkers = 0
    for i in range(1, 13):
        checker_val = ord(board[i]) - 64
        if checker_val >= 0 and checker_val <= 15:
            checkers += checker_val
    return checkers

def create_node(node, entry, val, exists):
    new_node = Filter(entry, val, exists, node)
    node.sub_entries[entry] = new_node
    print("TYPE", type(node.sub_entries))
    return new_node

def extract_xgid(line):
    full_board = xgid.extract_xgid(line)
    print("all", full_board.board, full_board.turn)
    if full_board.turn == '-1':
        xgid.swap_board(full_board)
    print("all", full_board.board, full_board.turn)

    if full_board.dice == '00': 
        filter = Filter("Cube",  "", True, None)
        create_node(filter, "Checkers In Zone", get_checkers_in_zone(full_board.board), True)
    else: 
        filter = Filter("Checker", "", True, None)

    # print("Length", length, score_bottom, score_top)
    if full_board.length > 0: 
        score = str(full_board.length - full_board.score_bottom) + "," + str(full_board.length - full_board.score_top) + "," + full_board.cube
        create_node(filter, "Score", score, True)

    filter.xgid = xgid.board_to_line(full_board)
    return filter


def process_file(file_path):
    with open(file_path, "r", encoding="unicode_escape") as f:
        tabs = -1
        lines = f.read().split('\n')
        lines.pop()
        filter_root = None
        for index, line in enumerate(lines):
            if index == 0:
                filter = extract_xgid(line)
                filter_root = filter
                continue
            
            tab_index = 0
            while line[tab_index] == '\t':
                tab_index += 1
            entry = line[tab_index:].split('\t')
            if len(entry) > 1: val = entry[1]
            else: val = ""

            while tab_index <= tabs:
                filter = filter.parent
                tabs -= 1

            filter = create_node(filter, entry[0], val, True)
            tabs = tab_index

    filter_root.print_filter(0)
    return filter_root

def process_filter(file_path):
    with open(file_path, "r", encoding="unicode_escape") as f:
        tabs = -1
        lines = f.read().split('\n')
        lines.pop()
        filter_root = None
        for index, line in enumerate(lines):
            if index == 0:
                if line == "Cube": filter = Filter("Cube",  "", True, None)
                elif line == "Checker": filter = Filter("Checker", "", True, None)
                else: print("ERROR")
                filter_root = filter
                continue

            tab_index = 0
            while line[tab_index] == '\t':
                tab_index += 1
            entry = line[tab_index:].split('\t')
            if len(entry) > 1: 
                if entry[1] == "!":
                    exists = False
                    val = ""
                else:
                    exists = True
                    val = entry[1]
            else: 
                exists = True
                val = ""

            while tab_index <= tabs:
                filter = filter.parent
                tabs -= 1

            filter = create_node(filter, entry[0], val, exists)
            tabs = tab_index

    return filter_root

def get(file_path, isFile):
    if isFile: return process_file(file_path)
    else: return process_filter(file_path)
        
