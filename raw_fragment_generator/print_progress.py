def print_progress(current_level, max_level, bar_length=50):
    current_percentage = current_level / max_level
    num_bars_to_print = int(current_percentage * bar_length)
    num_spaces_to_print = bar_length - num_bars_to_print
    print("|{}>{}| {:3.2f}% ({}/{})".format("=" * num_bars_to_print,
                                            " " * num_spaces_to_print,
                                            current_percentage * 100,
                                            current_level,
                                            max_level),
          end="\r")
