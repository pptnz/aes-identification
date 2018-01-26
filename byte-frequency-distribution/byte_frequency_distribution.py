from print_progress import print_progress
import os
import random


def main():
    directory0 = input("Directory0: ")
    directory1 = input("Directory1: ")
    output_directory = input("Directory to save csv: ")
    csv_filename = input("csv filename: ")
    size = int(input("Size in bytes: "))
    do_shuffle = int(input("0-shuffle, 1-no_shuffle: "))

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    files0 = list(filter(lambda filename: (not filename.startswith(".")) and ("." in filename),
                        os.listdir(directory0)))
    files1 = list(filter(lambda filename: (not filename.startswith(".")) and ("." in filename),
                         os.listdir(directory1)))
    num_files = len(files0) + len(files1)
    num_files_processed = 0
    num_csv = 1
    csv_row = 0

    file0 = open(os.path.join(directory0, files0.pop()), "rb")
    file1 = open(os.path.join(directory1, files1.pop()), "rb")
    csv = open(os.path.join(output_directory, csv_filename.format(num_csv)), "w")

    if do_shuffle == 0:
        while len(files0) != 0 and len(files1) != 0:
            data0 = file0.read(size)
            while len(data0) != size:
                file0.close()
                file0 = open(os.path.join(directory0, files0.pop()), "rb")
                num_files_processed += 1
                data0 = file0.read(size)
                if len(files0) == 0:
                    data0 = ""
                    break

            data1 = file1.read(size)
            while len(data1) != size:
                file1.close()
                file1 = open(os.path.join(directory1, files1.pop()), "rb")
                num_files_processed += 1
                data1 = file1.read(size)
                if len(files1) == 1:
                    data1 = ""
                    break

            group = random.randint(0, 1)
            data = [data0, data1][group]
            if len(data) == 0:
                break

            # compute data
            bfd1 = [0 for _ in range(256)]
            # bfd2 = [[0 for _ in range(256)] for _ in range(256)]
            for i in range(size - 1):
                bfd1[data[i]] += 1
                # bfd2[data[i]][data[i + 1]] += 1
            bfd1[data[-1]] += 1

            res = ','.join(str(i) for i in bfd1)
            # for row in bfd2:
            #     res += ','
            #     res += ','.join(str(i) for i in row)
            if group == 0:
                res += ',1,0'
            else:
                res += ',0,1'
            csv.write(res)
            csv_row += 1
            if csv_row >= 100:
                csv_row = 0
                num_csv += 1
                csv.close()
                csv = open(os.path.join(output_directory, csv_filename.format(num_csv)), "w")
            else:
                csv.write('\n')

            print_progress(num_files_processed, num_files)

        while len(files0) != 0:
            data = file0.read(size)
            while len(data) != size:
                file0.close()
                file0 = open(os.path.join(directory0, files0.pop()), "rb")
                num_files_processed += 1
                data = file0.read(size)
                if len(files0) == 0:
                    data = ""
                    break
            if len(data) == 0:
                break

            # compute dataz
            bfd1 = [0 for _ in range(256)]
            # bfd2 = [[0 for _ in range(256)] for _ in range(256)]
            for i in range(size - 1):
                bfd1[data[i]] += 1
                # bfd2[data[i]][data[i + 1]] += 1
            bfd1[data[-1]] += 1

            res = ','.join(str(i) for i in bfd1)
            # for row in bfd2:
            #     res += ','
            #     res += ','.join(str(i) for i in row)
            res += ',1,0'
            csv.write(res)
            csv_row += 1
            if csv_row >= 100:
                csv_row = 0
                num_csv += 1
                csv.close()
                csv = open(os.path.join(output_directory, csv_filename.format(num_csv)), "w")
            else:
                csv.write('\n')

            print_progress(num_files_processed, num_files)
        
        while len(files1) != 0:
            data = file1.read(size)
            while len(data) != size:
                file1.close()
                file1 = open(os.path.join(directory1, files1.pop()), "rb")
                num_files_processed += 1
                data = file1.read(size)
                if len(files1) == 0:
                    data = ""
                    break
            if len(data) == 0:
                break

            # compute dataz
            bfd1 = [0 for _ in range(256)]
            # bfd2 = [[0 for _ in range(256)] for _ in range(256)]
            for i in range(size - 1):
                bfd1[data[i]] += 1
                # bfd2[data[i]][data[i + 1]] += 1
            bfd1[data[-1]] += 1

            res = ','.join(str(i) for i in bfd1)
            # for row in bfd2:
            #     res += ','
            #     res += ','.join(str(i) for i in row)
            res += ',0,1'
            csv.write(res)
            csv_row += 1
            if csv_row >= 100:
                csv_row = 0
                num_csv += 1
                csv.close()
                csv = open(os.path.join(output_directory, csv_filename.format(num_csv)), "w")
            else:
                csv.write('\n')

            print_progress(num_files_processed, num_files)

    elif do_shuffle == 1:
        while len(files0) != 0:
            data = file0.read(size)
            while len(data) != size:
                file0.close()
                file0 = open(os.path.join(directory0, files0.pop()), "rb")
                num_files_processed += 1
                data = file0.read(size)
                if len(files0) == 0:
                    data = ""
                    break
            if len(data) == 0:
                break

            # compute data
            bfd1 = [0 for _ in range(256)]
            # bfd2 = [[0 for _ in range(256)] for _ in range(256)]
            for i in range(size - 1):
                bfd1[data[i]] += 1
                # bfd2[data[i]][data[i + 1]] += 1
            bfd1[data[-1]] += 1

            res = ','.join(str(i) for i in bfd1)
            # for row in bfd2:
            #     res += ','
            #     res += ','.join(str(i) for i in row)
            res += ',1,0'
            csv.write(res)
            csv_row += 1
            if csv_row >= 100:
                csv_row = 0
                num_csv += 1
                csv.close()
                csv = open(os.path.join(output_directory, csv_filename.format(num_csv)), "w")
            else:
                csv.write('\n')

            print_progress(num_files_processed, num_files)

        while len(files1) != 0:
            data = file1.read(size)
            while len(data) != size:
                file1.close()
                file1 = open(os.path.join(directory1, files1.pop()), "rb")
                num_files_processed += 1
                data = file1.read(size)
                if len(files1) == 0:
                    data = ""
                    break
            if len(data) == 0:
                break

            # compute dataz
            bfd1 = [0 for _ in range(256)]
            # bfd2 = [[0 for _ in range(256)] for _ in range(256)]
            for i in range(size - 1):
                bfd1[data[i]] += 1
                # bfd2[data[i]][data[i + 1]] += 1
            bfd1[data[-1]] += 1

            res = ','.join(str(i) for i in bfd1)
            # for row in bfd2:
            #     res += ','
            #     res += ','.join(str(i) for i in row)
            res += ',0,1'
            csv.write(res)
            csv_row += 1
            if csv_row >= 100:
                csv_row = 0
                num_csv += 1
                csv.close()
                csv = open(os.path.join(output_directory, csv_filename.format(num_csv)), "w")
            else:
                csv.write('\n')

            print_progress(num_files_processed, num_files)


if __name__ == '__main__':
    main()