import zipfile
import os


def unzip(file):
    path = os.path.dirname(file)
    print path

    with zipfile.ZipFile(file, "r") as z:
        z.extractall(path)


if __name__ == "__main__":
    unzip('C:\Users\ithaca\Documents\Magda\Tool_MIE\SENTINEL-1_TOOL\Immagini_grandi\S1A_IW_GRDH_1SDV_20151203T155609_20151203T155634_008880_00CB21_A687.zip')