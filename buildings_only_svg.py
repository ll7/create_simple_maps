import xml.etree.ElementTree as ET

# The color to filter by (already in percentage format)
rgb_color_str = 'rgb(85.098039%,81.568627%,78.823529%)'

# The scale factor applied during the export
scale_factor = 1/1_500 # TODO: Replace this with the actual scale factor

# Parse the SVG file
tree = ET.parse('svg_maps/map1.svg')
root = tree.getroot()

# Identify all elements with the specified color
elements = [elem for elem in root.iter() if 'style' in elem.attrib and rgb_color_str in elem.attrib['style']]

# Create a new SVG file with just the elements
new_root = ET.Element('svg', xmlns="http://www.w3.org/2000/svg")

# Copy viewBox attribute from the original root to the new root
if 'viewBox' in root.attrib:
    new_root.attrib['viewBox'] = root.attrib['viewBox']

for elem in elements:
    # Reverse the scaling for each element
    for attr in ['width', 'height', 'x', 'y']:
        if attr in elem.attrib:
            elem.attrib[attr] = str(float(elem.attrib[attr]) / scale_factor)
    new_root.append(elem)

# raise an error if elements is empty
if len(elements) == 0:
    raise ValueError('No elements found with color {}'.format(rgb_color_str))

# Save the new SVG file
new_tree = ET.ElementTree(new_root)
new_tree.write('filtered_map.svg')