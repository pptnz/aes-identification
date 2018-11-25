from data_reader import DataReader
from encryption_checker import EncryptionChecker
from result_writer import ResultWriter
from helper_functions import read_settings, compute_bfd, get_file_size, print_progress


def main():
    # Read Settings value.
    # Non-media input and output path settings
    input_path = read_settings("./settings.json", "input")

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
    fragments_count = int(get_file_size(file_path=input_path) / fragment_size)

    # Create DataReader
    data_reader = DataReader(path=input_path, read_size=fragment_size)

    # Create and Setup EncryptionChecker
    encryption_checker = EncryptionChecker()
    encryption_checker.setup_entropy_checker(frequency_threshold=frequency_threshold,
                                             entropy_threshold=entropy_threshold)
    encryption_checker.setup_cnn_checker(model_path=model_path,
                                         weight_path=weight_path,
                                         encryption_threshold=encryption_threshold)
    
    # Process Non-media data
    print("\nProcessing...")
    processed_count = 0
    fragment = data_reader.read()
    while fragment is not None:
        # Compute bfd
        bfd = compute_bfd(fragment=fragment)
        
        # Check the encryption by entropy
        entropy_result = encryption_checker.check_by_entropy(bfd=bfd)
        
        # Check the encryption by cnn
        cnn_result = encryption_checker.check_by_cnn(bfd=bfd)

        # TODO: Count result

        # Print progress
        processed_count += 1
        print_progress(processed_count, fragments_count)
        
        # Fetch next file fragment
        fragment = data_reader.read()

    # TODO: Print Result


if __name__ == '__main__':
    main()
