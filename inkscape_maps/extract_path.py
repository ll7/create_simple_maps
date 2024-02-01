import xml.etree.ElementTree as ET

def extract_path_info(svg_file):
    # Parse the SVG file
    svg_tree = ET.parse(svg_file)
    svg_root = svg_tree.getroot()

    # Define the SVG and Inkscape namespaces
    namespaces = {'svg': 'http://www.w3.org/2000/svg', 'inkscape': 'http://www.inkscape.org/namespaces/inkscape'}

    # Find all 'path' elements in the SVG file
    paths = svg_root.findall('.//svg:path', namespaces)

    # Initialize an empty list to store the path information
    path_info = []

    # Iterate over each 'path' element
    for path in paths:
        # Extract the 'd' attribute (coordinates), 'inkscape:label' and 'id'
        coordinates = path.attrib.get('d')
        label = path.attrib.get('{http://www.inkscape.org/namespaces/inkscape}label')
        id_ = path.attrib.get('id')

        # Append the information to the list
        path_info.append({'coordinates': coordinates, 'label': label, 'id': id_})

    return path_info

# Use the function
svg_file = 'inkscape_maps/route_draft.svg'
path_info = extract_path_info(svg_file)
for info in path_info:
    print(info)