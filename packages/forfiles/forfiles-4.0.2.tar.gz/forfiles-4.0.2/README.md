# forfiles

forfiles has useful tools for files and images.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install forfiles.

```bash
pip install --upgrade forfiles
```

Also install dependencies.
```bash
pip install -r requirements.txt
```

## Usage
```python
from forfiles import file, image

# file tools
file.filter("C:/Users/example/Downloads/directory-to-filter/", [".png", ".txt", "md"])

# image tools
image.scale("C:/Users/example/Downloads/boat.png", 1, 1.5)
image.resize("C:/Users/example/Downloads/car.jpg", 1000, 1000)

# image tools for directories
image.dir_scale("C:/Users/example/Downloads/cats", 2, 2)
image.dir_resize("C:/Users/example/Downloads/giraffes", 1000, 1000)
```