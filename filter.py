import sys
import os
import pickle
import shutil
import convert_to_graph

def filter(filter_graph, file_graph):
    if not filter_graph: return True

    filter_graph.print_filter(0)
    file_graph.print_filter(0)
    if filter_graph.entry != file_graph.entry: 
        print("Entries don't match", filter_graph.entry, file_graph.entry)
        return False
    if filter_graph.val != "" and filter_graph.val != file_graph.val: 
        print("Values don't match", filter_graph.val, file_graph.val)
        return False

    for key in filter_graph.sub_entries:
        node = filter_graph.sub_entries[key]
        if node.exists:
            if not node.entry in file_graph.sub_entries:
                
                return False
            return filter(node, file_graph.sub_entries[node.entry])
        else:
            return node.entry not in file_graph.sub_entries

    return True

def main():
    if len(sys.argv) > 3:
        directory = sys.argv[1]
        filter_file = sys.argv[2]
        out_directory = sys.argv[3]
        full_directory = r"\Users\aadam\Documents\2025_Blunderbase\\" + directory
        full_filter_file = r"\Users\aadam\Documents\2025_Blunderbase\\" + filter_file
        full_out_directory = r"\Users\aadam\Documents\2025_Blunderbase\\" + out_directory
        
        filter_graph = convert_to_graph.get(full_filter_file, False)
        for filename in os.listdir(full_directory):
            file_path = os.path.join(full_directory, filename)
            if os.path.isfile(file_path):
                # Process the file
                with open(file_path, "rb") as f:
                    print(file_path)
                    file_graph = pickle.load(f)
                print(f"Processing file: {filename}")
                if filter(filter_graph, file_graph):
                    shutil.copy(file_path, full_out_directory)
    else:
        print("ERROR: need 3 arguments");

if __name__ == "__main__":
    main()
