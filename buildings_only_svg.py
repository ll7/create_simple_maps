import xml.etree.ElementTree as ET

# The color to filter by (already in percentage format)
# rgb_color_percent = (85.098039, 81.568627, 78.823529)
# rgb_color_str = 'rgb({:.6f}%, {:.6f}%, {:.6f}%)'.format(*rgb_color_percent)
rgb_color_str = 'rgb(85.098039%,81.568627%,78.823529%)'

# Parse the SVG file
tree = ET.parse('svg_maps/map (2).svg')
root = tree.getroot()

# Identify all elements with the specified color
elements = [elem for elem in root.iter() if 'style' in elem.attrib and rgb_color_str in elem.attrib['style']]

# Create a new SVG file with just the elements
new_root = ET.Element('svg', xmlns="http://www.w3.org/2000/svg")
for elem in elements:
    new_root.append(elem)

# raise an error if elements is empty
if len(elements) == 0:
    raise ValueError('No elements found with color {}'.format(rgb_color_str))

# Save the new SVG file
new_tree = ET.ElementTree(new_root)
new_tree.write('filtered_map.svg')