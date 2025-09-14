import os, base64
import subprocess
from stegano import lsb

# ------------------- STEGANOGRAPHY --------------------

def hide_file_in_image(image_path, secret_file_path, output_path="output_stego.png"):
    try:
        filename = os.path.basename(secret_file_path)
        with open(secret_file_path, "rb") as f:
            file_bytes = f.read()

        encoded = base64.b64encode(file_bytes).decode()
        combined = f"{filename}:::{encoded}"

        stego_img = lsb.hide(image_path, combined)
        stego_img.save(output_path)

        return True, output_path
    except Exception as e:
        return False, str(e)

def extract_file_from_image(stego_image_path, output_path=None):
    try:
        hidden_data = lsb.reveal(stego_image_path)
        if not hidden_data or ":::" not in hidden_data:
            return False, "No hidden file found or wrong format."

        filename, encoded = hidden_data.split(":::", 1)
        file_bytes = base64.b64decode(encoded)

        if output_path:
            if os.path.isdir(output_path):
                output_file = os.path.join(output_path, filename)
            else:
                output_file = output_path
        else:
            output_file = filename

        with open(output_file, "wb") as f:
            f.write(file_bytes)

        return True, output_file
    except Exception as e:
        return False, str(e)

# ------------------- HIDDEN FOLDER METHOD --------------------

def hide_as_hidden_folder(path):
    try:
        if not os.path.exists(path):
            return False, "File/folder doesn't exist."
        subprocess.run(["attrib", "+s", "+h", path], shell=True)
        return True, "File hidden as a system-hidden folder successfully."
    except Exception as e:
        return False, str(e)

def unhide_hidden_folder(path):
    try:
        if not os.path.exists(path):
            return False, "File/folder doesn't exist."
        subprocess.run(["attrib", "-s", "-h", path], shell=True)
        return True, "File is now visible again."
    except Exception as e:
        return False, str(e)

# ------------------- NTFS STREAM METHOD --------------------

def hide_in_ntfs_stream(cover_file, secret_file):
    try:
        stream_path = f"{cover_file}:hiddenfile"
        with open(secret_file, "rb") as f:
            data = f.read()

        with open(stream_path, "wb") as out:
            out.write(data)

        return True, f"File hidden in NTFS stream of: {cover_file}"
    except Exception as e:
        return False, str(e)

def extract_from_ntfs_stream(cover_file, output_path=None):
    try:
        stream_path = f"{cover_file}:hiddenfile"
        with open(stream_path, "rb") as f:
            data = f.read()

        if not output_path:
            output_path = "recovered_file"

        with open(output_path, "wb") as out:
            out.write(data)

        return True, output_path
    except Exception as e:
        return False, str(e)
