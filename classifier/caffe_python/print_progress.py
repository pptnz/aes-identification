def print_progress(current_level, max_level, type, num_types):
    num_bars = int(current_level / max_level * 50)
    num_spaces = 50 - num_bars
    print("|{}>{}| (type {}/{}, file {}/{}, {:.2f}%)".format("=" * num_bars,
                                                             " " * num_spaces,
                                                             type,
                                                             num_types,
                                                             current_level,
                                                             max_level,
                                                             current_level / max_level * 100),
          end="\r")
