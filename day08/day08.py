from collections import defaultdict
import sys

WIDTH = 25
HEIGHT = 6
LAYER_PIXELS = WIDTH * HEIGHT

def day08(filename):
    with open(filename) as f:
        data = [int(token) for token in f.read().rstrip()]

    num_layers = len(data) // LAYER_PIXELS
    assert num_layers * LAYER_PIXELS == len(data)

    layers = [data[i * LAYER_PIXELS:(i + 1) * LAYER_PIXELS] for i in range(num_layers)]
    layer_counts = []
    for layer in layers:
        layer_count = defaultdict(int)
        layer_counts.append(layer_count)
        for c in layer:
            layer_count[c] += 1

    layer_count = min(layer_counts, key = lambda x: x[0])
    print(layer_count[1] * layer_count[2])

    image = []

    for i in range(LAYER_PIXELS):
        for j in range(num_layers):
            if layers[j][i] != 2:
                image.append(layers[j][i])
                break

    for i in range(HEIGHT):
        for j in range(WIDTH):
            pixel = image[i * WIDTH + j]
            assert pixel == 0 or pixel == 1
            print(" " if pixel == 0 else "*", end = "")
        print()

if __name__ == "__main__":
    day08(sys.argv[1])
