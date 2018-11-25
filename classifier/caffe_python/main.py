import caffe
from timer import Timer
from compute_bfd import compute_bfd
from fragment import Fragment


def main():
    # Setup Fragment
    file_types = ["exe", "html", "hwp", "jpg", "mp3", "pdf", "png"]
    file_groups = {0: "exe",
                   1: "html",
                   2: "hwp",
                   3: "jpg",
                   4: "mp3",
                   5: "pdf",
                   6: "png"}
    directories = ["/home/jonghoon/Desktop/datasets/data/fti_data/test/exe",
                   "/home/jonghoon/Desktop/datasets/data/fti_data/test/html",
                   "/home/jonghoon/Desktop/datasets/data/fti_data/test/hwp",
                   "/home/jonghoon/Desktop/datasets/data/fti_data/test/jpg",
                   "/home/jonghoon/Desktop/datasets/data/fti_data/test/mp3",
                   "/home/jonghoon/Desktop/datasets/data/fti_data/test/pdf",
                   "/home/jonghoon/Desktop/datasets/data/fti_data/test/png"]
    num_fragments = 10000
    fragment_getter = Fragment(num_fragments=num_fragments, file_types=file_types, directories=directories, fragment_size=4096)

    # Prepare caffe network
    net = caffe.Net("./deploy.prototxt", "./model.caffemodel", caffe.TEST)
    net.blobs["data"].reshape(1, 1, 256, 1)

    # Setup timer
    timer = Timer(name="Elapsed Time")

    # Result checker
    total_fragments = 0
    correct_fragments = 0
    classification_table = dict()
    for type1 in file_types:
        classification_table[type1] = dict()
        for type2 in file_types:
            classification_table[type1][type2] = 0

    # Classify
    fragment, file_type = fragment_getter.get_fragment()
    while fragment is not None:
        timer.start()
        net.blobs["data"].data[...] = compute_bfd(fragment)
        result = net.forward()
        prob = result["prob"].tolist()[0]
        classified_type = file_groups[prob.index(max(prob))]
        timer.stop()

        total_fragments += 1
        if classified_type == file_type:
            correct_fragments += 1
        classification_table[file_type][classified_type] += 1

        fragment, file_type = fragment_getter.get_fragment()
    
    print()
    print("Accuracy: {:.2f}%".format(correct_fragments / total_fragments * 100))
    print("Accuracy Table:")
    print("\t" + "\t".join(file_types))
    for type1 in file_types:
        print("{}\t".format(type1), end="")
        for type2 in file_types:
            print("{:3.2f}%".format(classification_table[type1][type2] / num_fragments * 100), end="\t")
        print()

    timer.print()


if __name__ == "__main__":
    main()
