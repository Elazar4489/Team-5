import folium


def sort_by_time(arr):
    pass

# repository of colors for devices by model
colors = ['darkgreen', 'beige', 'lightgreen', 'black', 'purple', 'darkpurple',
          'lightblue', 'orange', 'pink', 'blue', 'darkblue', 'gray', 'red', 'green']
color_devices = {}

def color_by_model(model):
    if model not in color_devices:
        c = colors.pop()
        color_devices[model] = c
    color_icon = color_devices[model]
    return color_icon

def create_map(images_data):
    images_gps = list(filter(lambda dicti: dicti["has_gps"] ,images_data))
    if not images_gps:
        return "<h2>No GPS data found</h2>"
    # base map
    m = folium.Map(location=[31.5, 34.75], zoom_start=9)

    list_coord = []

    # creates markers and adds them on the map
    for dicti in images_gps:
        folium.Marker(
            location=[dicti["latitude"], dicti["longitude"]],
            tooltip="Click here for more information",
            popup=f"{dicti['filename']}<br>{dicti['datetime']}<br>{dicti['camera_model']}",
            icon=folium.Icon(color=color_by_model(dicti["camera_model"]))
        ).add_to(m)

        # creates list with all points
        list_coord.append([dicti["latitude"], dicti["longitude"]])


    # creates line between locations
    coord_lines = [[list_coord[i],list_coord[i+1]] for i in range(len(list_coord)-1)]
    for line in coord_lines:
        folium.PolyLine(
            line,
            color= 'blue',
            weight= '4',
            opacity= '0.8'
        ).add_to(m)

    # returns 'm' as string of 'html'
    return m._repr_html_()
