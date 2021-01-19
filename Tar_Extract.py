import xtarfile as tarfile
import os
import tarfile
import shutil
from os import listdir
from os.path import isfile, join

# user parameters
tar_dir = ""  # enter path to write out TAR files
extract_dir = os.path.join(tar_dir, "0_Extracts")
# imagery_dir = ""

# get files in the tar directory
onlyfiles = [f for f in listdir(tar_dir) if isfile(join(tar_dir, f))]

for f in onlyfiles:
    fname = os.path.join(tar_dir, f)
    print(fname)

    if fname.endswith("tar.gz"):
        print("Extracting .gz ...")
        tar = tarfile.open(fname, "r:gz")
        tar.extractall(path=extract_dir)
        tar.close()
    elif fname.endswith("tar"):
        print("Extracting tar ...")
        tar = tarfile.open(fname, "r:")
        tar.extractall(path=extract_dir)
        tar.close()