from PIL import Image
from PIL.ExifTags import TAGS
from pathlib import Path
import os


def has_gps(data: dict):
    if "GPSInfo" in data:
        return True
    return False


def latitude(data: dict):
    if "GPSInfo" in data:
        value=data["GPSInfo"]
        list_of_keys=[k for k,v in value.items()]
        if list_of_keys[0]!= "1" or list_of_keys[1]!= "2" or list_of_keys[2]!= "3" or list_of_keys[3]!= "4":
            return None
        d=float(value[2][0])
        m=float(value[2][1])
        s=float(value[2][2])
        return d + (m / 60.0) + (s / 3600.0)
    return None


def longitude(data: dict):
    if "GPSInfo" in data:
        value=data["GPSInfo"]
        list_of_keys = [k for k, v in value.items()]
        if list_of_keys[0] != "1" or list_of_keys[1] != "2" or list_of_keys[2] != "3" or list_of_keys[3] != "4":
            return None
        d=float(value[4][0])
        m=float(value[4][1])
        s=float(value[4][2])
        return d + (m / 60.0) + (s / 3600.0)
    return None

def datatime(data: dict):
    if "DateTime" in data:
        return str(data["DateTime"])
    elif  "DateTimeOriginal" in data:
        return str(data["DateTimeOriginal"])
    elif  "DateTimeDigitized" in data:
        return str(data["DateTimeDigitized"])
    return None


def camera_make(data: dict):
    if "Make" in data:
        return str(data["Make"].rstrip('\x00'))
    return None


def camera_model(data: dict):
    if "Model" in data:
        return str(data["Model"].rstrip('\x00'))
    return None


def extract_metadata(image_path):
    path = Path(image_path)

    try:
        img = Image.open(image_path)
        exif = img._getexif()
    except Exception:
        exif = None

    if exif is None:
        return {
            "filename": path.name,
            "datetime": None,
            "latitude": None,
            "longitude": None,
            "camera_make": None,
            "camera_model": None,
            "has_gps": False
        }

    data = {}
    for tag_id, value in exif.items():
        tag = TAGS.get(tag_id, tag_id)
        data[tag] = value


    exif_dict = {
        "filename": path.name,
        "datetime": datatime(data),
        "latitude": latitude(data),
        "longitude": longitude(data),
        "camera_make": camera_make(data),
        "camera_model": camera_model(data),
        "has_gps": has_gps(data)
    }
    return exif_dict


def extract_all(folder_path):
    list_of_dicts=[]
    path=Path(folder_path)
    for file in path.iterdir():
        exif_dict=extract_metadata(file)
        list_of_dicts.append(exif_dict)
    return list_of_dicts


# x=extract_all("sample_data")
# print(x)
