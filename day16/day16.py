import sys

# 16 digit FFT
#
# 1  0 -1  0  1  0 -1  0  1  0 -1  0  1  0 -1  0  1  0 -1  0  1  0 -1  0  1  0 -1  0  1  0 -1  0  first digit
# 0  1  1  0  0 -1 -1  0  0  1  1  0  0 -1 -1  0  0  1  1  0  0 -1 -1  0  0  1  1  0  0 -1 -1  0  0  second digit
# 0  0  1  1  1  0  0  0 -1 -1 -1  0  0  0  1  1  1  0  0  0 -1 -1 -1  0  0  0  1  1  1  0  0  0 -1 -1  third digit
# 0  0  0  1  1  1  1  0  0  0  0 -1 -1 -1 -1  0  0  0  0  1  1  1  1  0  0  0  0 -1 -1 -1 -1  0  0  0  0  fourth digit
# 0  0  0  0  1  1  1  1  1  0  0  0  0  0 -1 -1 -1 -1 -1  0  0  0  0  0  1  1  1  1  1  0  0  0  0  0 -1 -1  fifth digit
# 0  0  0  0  0  1  1  1  1  1  1  0  0  0  0  0  0 -1 -1 -1 -1 -1 -1  0  0  0  0  0  0  1  1  1  1  1  1  0  0  sixth digit
# 0  0  0  0  0  0  1  1  1  1  1  1  1  0  0  0  0  0  0  0 -1 -1 -1 -1 -1 -1 -1  0  0  0  0  0  0  0  1  1  1  1  seventh digit
# 0  0  0  0  0  0  0  1  1  1  1  1  1  1  1  0  0  0  0  0  0  0  0 -1 -1 -1 -1 -1 -1 -1 -1  0  0  0  0  0  0  0  0  eighth digit


def fft(signal):
    output = []
    for i in range(1, len(signal) + 1):
        output_elem = 0
        j = i - 1
        while j < len(signal):
            output_elem += sum(signal[j:j + i])
            j += i * 2
            output_elem += -sum(signal[j:j + i])
            j += i  * 2
        output_digit = output_elem % 10
        output.append(output_digit if output_elem >= 0 or output_digit == 0 else 10 - output_digit)
    return output

def day16(filename):
    with open(filename) as f:
        signal = [int(token) for token in f.read().rstrip()]

    # Part 1

    new_signal = signal
    for _ in range(100):
        new_signal = fft(new_signal)

    print(''.join(map(str, new_signal[0:8])))

    # Part 2
    offset = int(''.join(map(str, signal[0:7])))
    new_signal = [0 for i in range(offset, len(signal) * 10000)]

    for i in range(len(new_signal)):
        new_signal[i] = signal[(i + offset) % len(signal)]
    signal = new_signal

    for _ in range(100):
        for i in reversed(range(len(signal) - 1)):
            new_signal[i] = (new_signal[i + 1] + signal[i]) % 10
        signal = new_signal
        new_signal = signal.copy()

    print(''.join(map(str, signal[0:8])))


if __name__ == "__main__":
    day16(sys.argv[1])
