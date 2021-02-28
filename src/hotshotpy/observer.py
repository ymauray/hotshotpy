import hotshotpy
import numpy as np
import os
import time

from PIL import Image, ImageOps, ImageDraw
from tesserocr import PyTessBaseAPI
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer

ai = ["ALEXA", "TOSHIRO", "MARCUS", "VIKTOR", "MIKE", "XING", "ASTON", "KEIKO"]


def find_coeffs(pa, pb):
    matrix = []
    for p1, p2 in zip(pa, pb):
        matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0]*p1[0], -p2[0]*p1[1]])
        matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1]*p1[0], -p2[1]*p1[1]])

    A = np.matrix(matrix, dtype=float)
    B = np.array(pb).reshape(8)

    res = np.dot(np.linalg.inv(A.T * A) * A.T, B)
    return np.array(res).reshape(8)


def on_modified(event):
    global time
    print(f"{event.src_path} has been modified.")
    time.sleep(1)
    im = Image.open(event.src_path)
    im = im.crop((690, 153, 690 + 1209, 33 + 801))
    im = ImageOps.invert(im)
    im = im.convert('LA')
    im = im.convert('RGBA')

    xshift = -100
    coeffs = find_coeffs(
        [(0, 0), (1209, 0), (1209, 719), (0, 719)],
        [(0, 0), (1209, 0), (1209+xshift, 719), (xshift, 719)])
    im = im.transform((1209, 719), Image.PERSPECTIVE, coeffs, Image.BICUBIC)

    data = np.array(im)
    red, blue, green, alpha = data.T

    source_color = (red >= 46)
    data[..., :-1][source_color.T] = (255, 255, 255)

    im2 = Image.fromarray(data)

    pos = 1
    results = []
    for y in [85, 167, 249, 331, 413, 495, 577, 659]:
        im3 = im2.crop((225, y - 82, 1209, y))
        im3.save(hotshotpy.common("tmp.png"))
        with PyTessBaseAPI(path=hotshotpy.common("tessdata/")) as api:
            api.SetImageFile(hotshotpy.common("tmp.png"))
            text = api.GetUTF8Text()
            for line in text.split('\n'):
                if line:
                    chunks = line.split(' ')
                    name = chunks[0].strip()
                    if not name in ai:
                        race_time = chunks[1].strip()
                        result = dict()
                        result['pos'] = pos
                        result['driver'] = name
                        result['race_time'] = race_time
                        results.append(result)
                        print(
                            f"{line} => pos = {pos}, name = {name}, race_time = {race_time}")
        pos += 1

    os.remove(hotshotpy.common("tmp.png"))


def start_observer(path):
    patterns = ["[0-9]*_[0-9]*_[0-9]*.png"]
    ignore_patterns = []
    ignore_directories = True
    case_sensitive = True
    event_handler = PatternMatchingEventHandler(
        patterns, ignore_patterns, ignore_directories, case_sensitive)
    event_handler.on_modified = on_modified

    observer = Observer()
    observer.schedule(event_handler, path)
    observer.start()
    return observer
