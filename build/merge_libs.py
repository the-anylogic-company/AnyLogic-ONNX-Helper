# AL exports libraries separate from their dependencies (placed in a lib folder).
# Running this script will merge the dependencies into a single jar, deleting the originals.

import os
import shutil
import tempfile
import re
from zipfile import ZipFile


def merge(lib_folder, target_jar, verbose=False):
    assert os.path.isdir(lib_folder), f"Cannot find lib folder '{lib_folder}'"
    assert os.path.isfile(target_jar), f"Cannot find target jar '{target_jar}'"

    # Create temporary directory to dump all jar contents into
    temp_dir = tempfile.mkdtemp(prefix = "onnxwrapper-build-")

    if verbose: print("Created temporary directory:", temp_dir)

    archives = [os.path.join(lib_folder, file) for file in os.listdir(lib_folder) if file.endswith(".jar")] + \
               [target_jar]

    # Extract all dependencies
    for file in archives:
        if verbose: print("Extracting:", file)
        
        with ZipFile(file, 'r') as archive:
            archive.extractall(temp_dir)

    # Edit the 'library.xml' to no longer reference the external jars
    xml_file = os.path.join(temp_dir, "library.xml")
    with open(xml_file, "r") as f:
        content = re.sub("<ClassPathEntry>.+?</ClassPathEntry>", "", f.read(), flags=re.DOTALL)
    with open(xml_file, "w") as f:
        _ = f.write(content)

    # Clean up used assets (lib folder and target jar)
    shutil.rmtree(lib_folder)
    os.remove(target_jar)

    # Repackage into a zip and rename as a jar
    archive = shutil.make_archive("OnnxHelperLibrary", "zip", temp_dir)
    os.rename(archive, archive.replace("OnnxHelperLibrary.zip", "OnnxHelperLibrary.jar"))

if __name__ == "__main__":
    if os.path.isdir("lib"):
        merge("lib", "OnnxHelperLibrary.jar")
    else:
        print("Libraries already merged. Terminating.")


    
