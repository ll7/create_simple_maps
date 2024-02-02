"""
convert_osm.py
convert OpenStreetMaps in a usable file format for
"""
import xml.etree.ElementTree as ET

def label_obstacles(svg_file, color_str):
    # Parse the SVG file
    svg_tree = ET.parse(svg_file)
    svg_root = svg_tree.getroot()

    # Define the SVG and Inkscape namespaces
    namespaces = {'svg': 'http://www.w3.org/2000/svg', 'inkscape': 'http://www.inkscape.org/namespaces/inkscape'}

    # Find all 'path' elements in the SVG file
    paths = svg_root.findall('.//svg:path', namespaces)

    # Iterate over each 'path' element
    for path in paths:
        # Check if the path's fill color matches the building color
        if path.attrib.get('style') and color_str in path.attrib.get('style'):
            # Add the 'inkscape:label' attribute with the value 'obstacle'
            path.attrib['{http://www.inkscape.org/namespaces/inkscape}label'] = 'obstacle'

    # Write the changes back to the SVG file
    svg_tree.write(svg_file)

# Use the function
svg_file = 'buildings_only_svg.py'
color_str = 'BUILDING_RGB_COLOR_STR'
label_obstacles(svg_file, color_str)