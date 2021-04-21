import os


def maxof(tuples):
    mxval = tuples[0][1] - tuples[0][0]
    mx = tuples[0]
    for t in tuples:
        val = t[1] - t[0]
        if mxval < val:
            mx = t
            mxval = val
    return [mx, mxval]


def compare2str(a, b):
    commons = []
    i = 0
    while i < (len(a)):
        j = 0
        chk = False
        while j < (len(b) - 1):
            start_i = i
            start_j = j
            try:
                while a[i] == b[j]:
                    i += 1
                    j += 1
                    chk = True
                    if j >= len(b) or i >= len(a):
                        break
            except Exception as e:
                print("barrier broke - index out of range: ", e)
            end_i = i - 1
            end_j = j - 1
            if start_i >= end_i and start_j >= end_j:
                j += 1
            else:
                commons.append((start_i, end_i, start_j, end_j))
            if i >= len(a):
                break
        if not chk:
            i += 1

    return maxof(commons)


def key_of_max(dictionary):
    mx = 0
    mxkey = None
    for key in dictionary:
        if mx < dictionary[key][1]:
            mx = dictionary[key][1]
            mxkey = key
    fil_indices = list(map(int, mxkey.split('-')))
    return mxkey, fil_indices


def find_longest_byte_strand(path="./sample_bin_files"):
    filenames = os.listdir(path)
    f = [open(path + '/' + str(i), 'rb').read() for i in filenames]

    identical_strands = {}

    for i in range(len(f) - 1):
        for j in range(i + 1, len(f)):
            identical_strands[str(i) + '-' + str(j)] = compare2str(f[i], f[j])

    mxkey, fil_indices = key_of_max(identical_strands)
    longest_string = f[fil_indices[0]][identical_strands[mxkey][0][0]:identical_strands[mxkey][0][1]]

    files_offset = [(filenames[fil_indices[0]], identical_strands[mxkey][0][:2]),
                    (filenames[fil_indices[1]], identical_strands[mxkey][0][2:])]
    for i in range(len(f)):
        if i in fil_indices:
            continue
        occuring_index = f[i].find(longest_string)
        if occuring_index != -1:
            files_offset.append((filenames[i], (occuring_index, occuring_index + len(longest_string))))

    return files_offset


parent_folder = "./sample_bin_files"
files_with_common = find_longest_byte_strand(path=parent_folder)  # find the longest strand in 2 or more files
strand_length = files_with_common[0][1][1] - files_with_common[0][1][0]
print("length of the strand: ", strand_length)
print("Filenames where longest strand appears with starting and ending index: ")
for file in files_with_common:
    print(file[0], file[1])
