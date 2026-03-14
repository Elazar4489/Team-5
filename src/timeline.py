from extractor import *
import random
from datetime import datetime

def create_timeline(images_data):
    if not images_data:
        return "No data available"



    dated_images = [img for img in images_data if img.get("datetime")]
    dated_images.sort(key=lambda x: x["datetime"])
    timeline_list = [img["datetime"] for img in dated_images if img["datetime"] != None]
    if not timeline_list:
        return None

    # הוספת ה-Style לראש ה-HTML כדי להגדיר את ה-Hover
    html = f'''
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <style>
        .timeline-card {{
            transition: all 0.3s ease; /* אנימציה חלקה */
            cursor: pointer;
            position: relative;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}
        .timeline-card:hover {{
            transform: translateY(-5px); /* קפיצה קלה למעלה */
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            filter: brightness(0.95); /* שינוי קטן בגוון */
        }}
        .extra-details {{
            display: none; /* הסתרה של הפרטים */
            margin-top: 10px;
            padding-top: 10px;
            border-top: 1px solid rgba(0,0,0,0.1);
        }}
        .timeline-card:hover .extra-details {{
            display: block; /* הצגה בזמן Hover */
        }}
    </style>
    <div style="position:relative; padding:20px;">
    '''

    hex_colors_list = [
        "#F0F4F8", "#E6FFFA", "#FFF5F5", "#FFFBEB", "#F0FFF4",
        "#EBF8FF", "#FAF5FF", "#FFF5F7", "#F7FAFC", "#EDF2F7"
    ]

    icons = {
        "Apple": "fa-brands fa-apple",
        "Samsung": "fa-solid fa-mobile-button",
        "Canon": "fa-solid fa-camera"
    }

    color = random.choice(hex_colors_list)
    last_day = str(dated_images[0]["datetime"][0:10])


    for i, img in enumerate(dated_images):
        fmt = '%Y:%m:%d %H:%M:%S'
        t1 = datetime.strptime(str(dated_images[i-1]["datetime"]), fmt)
        t2 = datetime.strptime(str(img["datetime"]), fmt)
        diff = t2 - t1
        seconds_diff = diff.total_seconds()
        if seconds_diff >= 12 * 3600:
            html += f'''
                    <div style="text-align: center; font-size: 24px; padding: 15px; color: #000000; background-color: #FFFFFF; border-radius: 8px; margin-bottom: 20px;">
                        <i class="fa-solid fa-triangle-exclamation" style="font-size: 2em; display: block; margin-bottom: 5px;"></i>
                        <strong>עברו יותר מ-12 שעות</strong>
                    </div>'''

        side = "left" if i % 2 == 0 else "right"
        side_style = 'width: 40%; margin-right: auto; margin-left: 5%;' if i % 2 == 0 else 'width: 40%; margin-left: auto; margin-right: 5%;'

        # זיהוי אייקון
        make_name = img.get("camera_make", "Unknown")
        icon_class = "fa-solid fa-image"
        for brand, icon in icons.items():
            if brand.lower() in make_name.lower():
                icon_class = icon
                break

        # החלפת צבע לפי יום
        current_day = str(img["datetime"][0:10])
        if current_day != last_day:
            last_color = color
            while color == last_color:
                color = random.choice(hex_colors_list)
            last_day = current_day

        # בניית ה-HTML של הכרטיס
        html += f'''
        <div class="timeline-card" style="{side_style} text-align:{side}; background-color:{color}; padding:15px; border-radius:8px; margin-bottom: 20px;">
            <i class="{icon_class}" style="font-size: 1.2em;"></i>
            <strong>{img["datetime"]}</strong><br>
            <span>{img["filename"]}</span>

            <div class="extra-details">
                <small>
                    <i class="fa-solid fa-microchip"></i> מודל: {img.get("camera_model", "Unknown")}<br>
                    <i class="fa-solid fa-map-pin"></i> נתוני GPS זמינים
                </small>
            </div>
        </div>'''

    html += '</div>'
    return html
