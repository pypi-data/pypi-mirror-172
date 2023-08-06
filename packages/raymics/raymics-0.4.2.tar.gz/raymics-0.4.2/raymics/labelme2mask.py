"""Convert labelme json file to mask"""
import os
import math
import json
import numpy as np
import PIL
import PIL.Image
import PIL.ImageDraw

from typing import Tuple, List


def shape_to_mask(img_shape: Tuple[int, int], points: List[Tuple[float, float]],
                  shape_type: str = None, line_width: int = 10,
                  point_size: int = 5) -> np.ndarray:

    mask = np.zeros(img_shape[:2], dtype=np.uint8)
    mask = PIL.Image.fromarray(mask)
    draw = PIL.ImageDraw.Draw(mask)
    xy = [tuple(point) for point in points]

    if shape_type == "circle":
        assert len(xy) == 2, "Shape of shape_type=circle must have 2 points"
        (cx, cy), (px, py) = xy
        d = math.sqrt((cx - px) ** 2 + (cy - py) ** 2)
        draw.ellipse([cx - d, cy - d, cx + d, cy + d], outline=1, fill=1)

    elif shape_type == "rectangle":
        assert len(xy) == 2, "Shape of shape_type=rectangle must have 2 points"
        draw.rectangle(xy, outline=1, fill=1)

    elif shape_type == "line":
        assert len(xy) == 2, "Shape of shape_type=line must have 2 points"
        draw.line(xy=xy, fill=1, width=line_width)

    elif shape_type == "linestrip":
        draw.line(xy=xy, fill=1, width=line_width)

    elif shape_type == "point":
        assert len(xy) == 1, "Shape of shape_type=point must have 1 points"
        cx, cy = xy[0]
        r = point_size
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=1, fill=1)

    else:
        assert len(xy) > 2, "Polygon must have points more than 2"
        draw.polygon(xy=xy, outline=1, fill=1)

    mask = np.array(mask)

    return mask


def labelme2mask(json_path: str, mask_path: str):
    """

    Parameters
    ----------
    json_path : str
        Path of the labelme json file.

    mask_path : str
        Destination path of the mask file.

    """
    with open(json_path) as f:
        json_data = json.load(f)

    points = json_data["shapes"][0]["points"]
    shape = json_data["shapes"][0]["shape_type"]
    h, w = json_data["imageHeight"], json_data["imageWidth"]
    mask = shape_to_mask(img_shape=(h, w), points=points, shape_type=shape)

    mask_dir = os.path.dirname(mask_path)
    if not os.path.exists(mask_dir):
        os.makedirs(mask_dir)

    with open(mask_path, "wb") as f:
        np.save(f, mask)


def batch_labelme2mask(src_dir: str, dst_dir: str):

    def get_all_json_files(data_dir: str) -> List[str]:
        paths = []
        for name in os.listdir(data_dir):
            path = os.path.join(data_dir, name)
            if os.path.isdir(path):
                paths += get_all_json_files(path)
            else:
                if name.endswith(".json"):
                    paths.append(path)
        return paths

    src_json_paths = get_all_json_files(src_dir)
    dst_json_paths = []
    for path in src_json_paths:
        rel_path = os.path.relpath(path, src_dir)
        dst_path = os.path.join(dst_dir, rel_path)[:-4] + "npy"
        dst_json_paths.append(dst_path)

    for src_path, dst_path in zip(src_json_paths, dst_json_paths):
        labelme2mask(src_path, dst_path)


if __name__ == "__main__":
    batch_labelme2mask(
        src_dir="/Users/john/Datasets/breast_and_thyroid/json/polygon/breast",
        dst_dir="/Users/john/Datasets/breast_and_thyroid/npy-tmp"
    )
