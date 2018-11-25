class ResultCounter:
    def __init__(self):
        self.result_count = {0: {0: 0, 1: 0},
                             1: {0: 0, 1: 0}}

    def count(self, true_type, identified_type):
        self.result_count[true_type][identified_type] += 1

    def print_count(self):
        print("\t\tPlain\t\tEncrypted")
        print("Plain\t\t{}\t\t{}".format(self.result_count[0][0], self.result_count[0][1]))
        print("Encrypted\t\t{}\t\t{}".format(self.result_count[1][0], self.result_count[1][1]))

    def print_prob(self):
        plain_fragments_count = self.result_count[0][0] + self.result_count[0][1]
        encrypted_fragments_count = self.result_count[1][0] + self.result_count[1][1]

        print("\t\tPlain\t\tEncrypted")
        print("Plain\t\t{:3.2f}%\t\t{:3.2f}%".format(self.result_count[0][0] / plain_fragments_count * 100,
                                         self.result_count[0][1] / plain_fragments_count * 100))
        print("Encrypted\t\t{:3.2f}%\t\t{:3.2f}%".format(self.result_count[1][0] / encrypted_fragments_count * 100,
                                                         self.result_count[1][1] / encrypted_fragments_count * 100))
