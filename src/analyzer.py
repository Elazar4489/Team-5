from extractor import extract_all
from pathlib import Path
from datetime import datetime

# empty new report
def init_report():
    base = {
        'total_images': 0,
        'images_with_gps': 0,
        'images_with_datetime': 0,
        'unique_cameras': set({}),
        'data_range': {'start': "No Data", 'end': "No data"},
        "insights": []
    }
    return base

# Conversion 'datetime' from string to 'datetime' object
def convert_dt(data):
    list_with_date = filter(lambda d: d['datetime'] is not None, data)
    time_format = "%Y:%m:%d %H:%M:%S"
    # sort the dates
    date_list = [datetime.strptime(d['datetime'],time_format) for d in list_with_date]
    first_time = str(min(date_list))
    last_time = str(max(date_list))

    return [first_time,last_time]

# Checks if changed devices.
# Returns list of dicts, each one is an exchange
def detect_camera_switches(images_data):
    sorted_images = sorted(
        [img for img in images_data if img["datetime"]],
        key=lambda x: x["datetime"]
    )
    switches = []
    for i in range(1, len(sorted_images)):
        prev_cam = sorted_images[i-1].get("camera_model")
        curr_cam = sorted_images[i].get("camera_model")
        if prev_cam and curr_cam and prev_cam != curr_cam:
            switches.append({
                "date": sorted_images[i]["datetime"],
                "from": prev_cam,
                "to": curr_cam
            })
    return switches


def analyze(data: list[dict]) -> dict:
    # init new report
    report = init_report()

    # summery data to the report
    for d in data:
        report['total_images'] += 1
        if d['has_gps']:
            report['images_with_gps'] += 1
        if d['datetime']:
            report['images_with_datetime'] += 1
        if d['camera_make'] is not None and d['camera_model']:
            report['unique_cameras'].add(d['camera_make'] + " " + d['camera_model'])

    # Extract the first and last datetime by conversion to datetime object
    times =  convert_dt(data)
    report['data_range'] = { 'start': times[0] , 'end': times[1]}

    # Find patterns in the data
    # Switches devices
    all_switches = detect_camera_switches(data)
    if all_switches:
        report["insights"].append(f"נמצאו {len(all_switches)} מכשירים שונים - ייתכן שהסוכן החליף מכשירים.")
        # Which device was changed
        for d in all_switches:
            report["insights"].append(f"ב- {d['date']} הסוכן עבר ממכשיר {d['from']} ל- {d['to']}.")

    return report
