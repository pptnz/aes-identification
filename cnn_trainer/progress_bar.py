def progress_bar(current_level, max_level, num_bars=50):
    num_bar_fragments = int(current_level / max_level * num_bars)
    print("|{}>{}| ({}/{}, {:>.2f}%)".format("=" * num_bar_fragments,
                                              " " * (num_bars - num_bar_fragments),
                                              current_level,
                                              max_level,
                                              (current_level / max_level * 100)), end="\r")
