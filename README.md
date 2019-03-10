## CounterTrace

Counts the number of contours in an image with various pixel intensities. The image is supposed to be grayscale

## Prerequisites

1. Python 3
2. Matplotlib
3. pillow
4. numpy

## Usage
```bash
pip install -r reqirements.txt
```

```bash
python3 CounterTracer.py file_path --shape width, height
usage: Count the number of contours in a binary image [-h] [--shape SHAPE]
                                                      file_path

positional arguments:
  file_path             Input Image Path

optional arguments:
  -h, --help            show this help message and exit
  --shape SHAPE, -s SHAPE
                        Shape of the original image width, height
```