from geojsonio import display

with open(r'C:\Users\ithaca\Documents\Magda\Tool_MIE\SENTINEL-1_TOOL\AOI\AOI.geojson') as f:
    contents = f.read()
    display(contents)
    f.close()