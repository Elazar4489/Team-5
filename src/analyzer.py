from extractor import extract_all
from pathlib import Path

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

# Sort images by time. Return list of only dicts with 'datetime'.
def sort_images_by_time(data):
    sorted_images = sorted(
        [img for img in data if img["datetime"]],
        key=lambda x: x["datetime"]
    )
    return sorted_images

# Checks if changed devices.
# Returns list of dicts, each one is an exchange
def detect_camera_switches(images_data):
    sorted_images = sort_images_by_time(images_data)
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
    times =  sort_images_by_time(data)
    report['data_range'] = { 'start': times[0]['datetime'] , 'end': times[-1]['datetime']}

    # Find patterns in the data
    # Switches devices
    all_switches = detect_camera_switches(data)
    if all_switches:
        report["insights"].append(f"נמצאו {len(report['unique_cameras'])} מכשירים שונים - ייתכן שהסוכן החליף מכשירים.")
        # Which device was changed
        for d in all_switches:
            report["insights"].append(f"ב- {d['date']} הסוכן עבר ממכשיר {d['from']} ל- {d['to']}.")

    return report
