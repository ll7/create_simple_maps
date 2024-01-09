import xml.etree.ElementTree as ET
import time
import re

print("Converting map now: " + time.strftime("%Y-%m-%d_%H:%M:%S"))

# The color to filter by (already in percentage format)
building_rgb_color_str = 'rgb(85.098039%,81.568627%,78.823529%)'

# The scale factor applied during the export
scale_factor = 1 # TODO: Replace this with the actual scale factor
print("Scale factor: " + str(scale_factor))

# Parse the SVG file
map_folder = 'svg_maps'
map_name = 'map3_1350'
map_full_name = map_folder + '/' + map_name + '.svg'
print("Map name: " + map_full_name)
tree = ET.parse(map_full_name)
root = tree.getroot()

# Identify all elements with the specified color
# Initialize an empty list to store the elements
elements = []
# Iterate over all elements in the root object
for elem in root.iter():
    # Check if the element has a 'style' attribute and if the 'style' attribute contains the building_rgb_color_str
    if 'style' in elem.attrib and building_rgb_color_str in elem.attrib['style']:
        # If the condition is met, add the element to the list
        elements.append(elem)


# Create a new SVG file with just the elements
new_root = ET.Element('svg', xmlns="http://www.w3.org/2000/svg")

# Copy viewBox attribute from the original root to the new root
print("Create a new viewBox attribute")
if 'viewBox' in root.attrib:
    viewbox = list(map(float, root.attrib['viewBox'].split()))
    print("old viewbox: " + str(viewbox))
    viewbox[2] *= scale_factor  # Scale the width
    viewbox[3] *= scale_factor  # Scale the height
    print("new viewbox: " + str(viewbox))
    new_root.attrib['viewBox'] = ' '.join(map(str, viewbox))

for elem in elements:
    # Check if the element is a path
    if elem.tag.endswith('path'):
        # Parse the d attribute
        d = elem.attrib['d']
        commands = re.findall(r'([A-Za-z])|(-?\d+(?:\.\d+)?)', d)

        # Scale the coordinates
        scaled_commands = []
        for command in commands:
            if command[0]:  # If it's a command
                scaled_commands.append(command[0])
            else:  # If it's a coordinate
                scaled_commands.append(str(float(command[1]) * scale_factor))

        # Reassemble the d attribute
        elem.attrib['d'] = ' '.join(scaled_commands)

    new_root.append(elem)

# Get the width of the image
viewbox = list(map(float, root.attrib['viewBox'].split()))
image_width = viewbox[2]

# Add an alternating black and white line over the whole image width
line_length = 100  # Length of each line segment in meters
for i in range(0, int(image_width), line_length):
    color = "rgb(0,0,0)" if (i // line_length) % 2 == 0 else "rgb(100%,100%,100%)"
    ET.SubElement(
        new_root, 
        'line', 
        x1=str(i), 
        y1="10", 
        x2=str(i + line_length), 
        y2="10", 
        style=f"stroke:{color};stroke-width:2"
        )
scale_text = ET.SubElement(new_root, 'text', x="10", y="30", style="font-size:12px")
scale_text.text = str(line_length) + " m"  # Replace this with the actual distance the scale bar represents

# raise an error if elements is empty
if len(elements) == 0:
    raise ValueError('No elements found with color {}'.format(building_rgb_color_str))

# Save the new SVG file
new_tree = ET.ElementTree(new_root)
now = time.strftime("%Y%m%d-%H%M%S")
filtered_map_name = 'filtered_' + map_name + '_' + now + '.svg'
new_tree.write(filtered_map_name)