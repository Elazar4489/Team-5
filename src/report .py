from datetime import datetime
from extractor import extract_all
from map_view import create_map
from analyzer import analyze

def create_report(images_data, map_html, timeline_html, analysis):
    now = datetime.now().strftime("%d/%m/%Y %H:%M")

    insights_html = ""

    for insight in analysis.get("insights", []):
        insights_html += f"<li>{insight}</li>\n"

    cameras_html = ""
    for cam in analysis.get("unique_cameras", []):
        cameras_html += f"<span class='badge'>{cam}</span>\n"
    total_imgs = analysis.get('total_images', 0)
    gps_imgs = analysis.get('images_with_gps', 0)

    unique_cams_count = len(analysis.get('unique_cameras', []))
    html = f"""
    <!DOCTYPE html>
    <html lang="he" dir="rtl"> <head>
        <meta charset="UTF-8"> <title>דו"ח מודיעין ויזואלי</title>
        <style>
            /* אזור העיצוב (CSS). */
            /* שימו לב: בגלל שאנחנו בתוך f-string של פייתון, חייבים לכתוב סוגריים מסולסלים כפולים {{ }} עבור ה-CSS. */
            /* אם נכתוב רק סוגריים בודדים, פייתון יחשוב שזה משתנה ויקרוס. */
            body {{ font-family: Arial, sans-serif; max-width: 1000px; margin: 0 auto; padding: 20px; background: #f4f7f6; }}
            .header {{ background: #1e3c72; color: white; padding: 20px; border-radius: 8px; text-align: center; }}
            .section {{ background: white; padding: 20px; margin: 20px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
            .stats {{ display: flex; gap: 20px; justify-content: center; }}
            .stat-box {{ background: #e8eff5; padding: 20px; border-radius: 8px; text-align: center; min-width: 120px; }}
            .stat-num {{ font-size: 2.5em; font-weight: bold; color: #1e3c72; }}
            .badge {{ background: #1e3c72; color: white; padding: 5px 15px; border-radius: 20px; margin: 3px; display: inline-block; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>דו"ח מודיעין ויזואלי</h1>
            <p>הופק בתאריך: {now}</p> 
        </div>

        <div class="section">
            <h2>סיכום נתונים</h2>
            <div class="stats">
                <div class="stat-box">
                    <div class="stat-num">{total_imgs}</div>
                    <div>תמונות</div>
                </div>
                <div class="stat-box">
                    <div class="stat-num">{gps_imgs}</div>
                    <div>מיקומי GPS</div>
                </div>
                <div class="stat-box">
                    <div class="stat-num">{unique_cams_count}</div>
                    <div>מכשירים שונים</div>
                </div>
            </div>
        </div>

        <div class="section">
            <h2>תובנות ודפוסים (Insights)</h2>
            <ul>
                {insights_html if insights_html else "<li>לא נמצאו תובנות מיוחדות.</li>"}
            </ul>
        </div>

        <div class="section">
            <h2>מכשירים שזוהו</h2>
            <div>
                {cameras_html if cameras_html else "לא זוהו מכשירים."}
            </div>
        </div>

        <div class="section">
            <h2>מפת מיקומים</h2>
            {map_html if map_html else "<p>אין נתוני מפה להצגה.</p>"}
        </div>

        <div class="section">
            <h2>ציר זמן (Timeline)</h2>
            {timeline_html if timeline_html else "<p>אין נתוני ציר זמן להצגה.</p>"}
        </div>
    </body>
    </html>
    """

    return html


# מפה נועד בשביל הבדיקה שאני עשיתי
if __name__ == "__main__":

    import map_view,extractor,analyzer,timeline
    folder_path = r"C:\Users\EHRE14\PycharmProjects\Team-5\images\ready"
    real_images_data = extractor.extract_all(folder_path)
    real_map_html = map_view.create_map(real_images_data)
    analysis = analyzer.analyze(extractor.extract_all(folder_path))
    real_timeline = timeline.create_timeline(extractor.extract_all(folder_path))

    html_output = create_report(real_images_data, real_map_html, real_timeline, analysis)

    with open("report.html", "w", encoding="utf-8") as f:
        f.write(html_output)

    print("קובץ הבדיקה נוצר! פתח את report.html בדפדפן שלך.")