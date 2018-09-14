def print_progress(current_step, max_step, bar_length=50):
    progress_percentage = current_step / max_step
    num_bar_to_print = int(progress_percentage * bar_length)
    num_space_to_print = bar_length - num_bar_to_print

    print("|{}>{}| {:>5.1f}% ({}/{})".format("=" * num_bar_to_print,
                                             " " * num_space_to_print,
                                             progress_percentage * 100,
                                             current_step,
                                             max_step), end="\r")
