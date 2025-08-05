from PIL import Image
import math
from collections import defaultdict
from use_camera import capture_photo


def get_dominant_color(filepath):
    # Define basic RGB color categories
    color_categories = {
        'red': (255, 0, 0),
        'green': (0, 255, 0),
        'blue': (0, 0, 255),
    }

    def euclidean_distance(c1, c2):
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(c1, c2)))

    def closest_color(pixel):
        closest = None
        min_distance = float('inf')
        for name, color in color_categories.items():
            dist = euclidean_distance(pixel, color)
            if dist < min_distance:
                min_distance = dist
                closest = name
        return closest

    # Load and resize the image
    img = Image.open(filepath).convert('RGB')
    img = img.resize((100, 100))  # smaller size = faster

    # Tally up closest color matches
    color_count = defaultdict(int)
    for pixel in img.getdata():
        name = closest_color(pixel)
        color_count[name] += 1

    # Get the most common color category
    dominant_color = max(color_count, key=color_count.get)
    return dominant_color




def detect_color():
    capture_photo("color_detect")
    return get_dominant_color('images/color_detect.jpg')


if __name__ == "__main__":
    color = detect_color()
    print(color)



















