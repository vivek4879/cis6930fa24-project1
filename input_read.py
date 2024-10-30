import glob
import sys
# print(sys.argv)

def input_read():
    arguments_received = sys.argv
    flags = []
    concepts = []
    stats_ = []
    output_path_list = []
    

    for i in range (len(arguments_received)):
        if arguments_received[i] == '--input':
            glob_received = arguments_received[i + 1]
        elif arguments_received[i] == '--concept':
            concepts.append(arguments_received[i+1])
        elif arguments_received[i] == '--output':
            output_path_list.append(arguments_received[i+1])
        elif arguments_received[i] == '--stats':
            stats_.append(arguments_received[i+1])
        elif arguments_received[i].startswith('--'):
            flags.append(arguments_received[i][2:])
        

    input_files = glob.glob(glob_received)
    return (input_files, flags,concepts,stats_,output_path_list)
