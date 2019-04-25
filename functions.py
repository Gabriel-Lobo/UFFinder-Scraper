def print_progress(index, max_size):
    progress = 100 / (max_size - 1) * (index + 1)
    progress_bar_size = [' '] * 40  # TODO - fix hardcoded value 40
    progress_bar_curr = progress // 2.5  # TODO - fix hardcoded value 2.5

    for i in range(0, int(progress_bar_curr)):
        if i <= int(progress_bar_curr):
            progress_bar_size[i] = '|'

    print("\r" + str("{:.2f}".format(progress)) + '% - [' + ''.join(progress_bar_size) + ']', end='')
