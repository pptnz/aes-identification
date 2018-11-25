from data_reader import DataReader
from encryption_checker import EncryptionChecker
from helper_functions import read_settings, compute_bfd, get_file_size, print_progress
from result_counter import ResultCounter

def main():
    # Read Settings value.
    # Non-media input and output path settings
    plain_input_path = read_settings("./settings.json", "input")
    encrypted_input_path = read_settings("./settings.json", "input")

    # Entropy-Checker settings
    frequency_threshold = read_settings("./settings.json", "entropy_checker", "frequency_threshold")
    entropy_threshold = read_settings("./settings.json", "entropy_checker", "entropy_threshold")

    # CNN-Checker settings
    model_path = read_settings("./settings.json", "cnn_checker", "model_path")
    weight_path = read_settings("./settings.json", "cnn_checker", "weight_path")
    encryption_threshold = read_settings("./settings.json", "cnn_checker", "encryption_threshold")

    # Fragment size settings
    fragment_size = read_settings("./settings.json", "fragment_size")

    # Compute the number of fragments to process
    plain_fragments_count = int(get_file_size(file_path=plain_input_path) / fragment_size)
    encrypted_fragments_count = int(get_file_size(file_path=encrypted_input_path) / fragment_size)

    # Create DataReader
    plain_data_reader = DataReader(path=plain_input_path, read_size=fragment_size)
    encrypted_data_reader = DataReader(path=encrypted_input_path, read_size=fragment_size)

    # Create and Setup EncryptionChecker
    encryption_checker = EncryptionChecker()
    encryption_checker.setup_entropy_checker(frequency_threshold=frequency_threshold,
                                             entropy_threshold=entropy_threshold)
    encryption_checker.setup_cnn_checker(model_path=model_path,
                                         weight_path=weight_path,
                                         encryption_threshold=encryption_threshold)
    
    # Create ResultCounter
    entropy_result_counter = ResultCounter()
    cnn_result_counter = ResultCounter()
    
    # Process Non-media data
    print("\nProcessing Plain Fragments...")
    processed_count = 0
    fragment = plain_data_reader.read()
    while fragment is not None:
        # Compute bfd
        bfd = compute_bfd(fragment=fragment)
        
        # Check the encryption by entropy
        entropy_result = encryption_checker.check_by_entropy(bfd=bfd)
        entropy_result_counter.count(true_type=0, identified_type=entropy_result)
        
        # Check the encryption by cnn
        cnn_result = encryption_checker.check_by_cnn(bfd=bfd)
        cnn_result_counter.count(true_type=0, identified_type=cnn_result)

        # Print progress
        processed_count += 1
        print_progress(processed_count, plain_fragments_count)
        
        # Fetch next file fragment
        fragment = plain_data_reader.read()
    print("Done.\n")

    print("\nProcessing Encrypted Fragments...")
    processed_count = 0
    fragment = encrypted_data_reader.read()
    while fragment is not None:
        # Compute bfd
        bfd = compute_bfd(fragment=fragment)

        # Check the encryption by entropy
        entropy_result = encryption_checker.check_by_entropy(bfd=bfd)
        entropy_result_counter.count(true_type=0, identified_type=entropy_result)

        # Check the encryption by cnn
        cnn_result = encryption_checker.check_by_cnn(bfd=bfd)
        cnn_result_counter.count(true_type=0, identified_type=cnn_result)

        # Print progress
        processed_count += 1
        print_progress(processed_count, encrypted_fragments_count)

        # Fetch next file fragment
        fragment = encrypted_data_reader.read()
    print("Done.\n")

    # Print result
    print("Entropy Result:")
    entropy_result_counter.print_count()
    entropy_result_counter.print_prob()

    print("\nCNN Result:")
    cnn_result_counter.print_count()
    cnn_result_counter.print_prob()


if __name__ == '__main__':
    main()
