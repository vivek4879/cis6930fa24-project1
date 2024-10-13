import glob
import sys
print(sys.argv)
arguments_received = sys.argv
flags = []
concepts = []
stats_ = []

for i in range (len(arguments_received)):
    if arguments_received[i] == '--input':
        glob_received = arguments_received[i + 1]
    elif arguments_received[i] == '--concept':
        concepts.append(arguments_received[i+1])
    elif arguments_received[i] == '--output':
        output_path = arguments_received[i+1]
    elif arguments_received[i] == '--stats':
        stats_.append(arguments_received[i+1])
    elif arguments_received[i].startswith('--'):
        flags.append(arguments_received[i][2:])
    

input_files = glob.glob(glob_received)

print(input_files)
print(flags)
print(concepts)
print(stats_)
