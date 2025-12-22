import os
import zipfile

SRC_DIR = "/app/src"
ZIP_PATH = "/app/src.zip"


def create_src_zip():
    if not os.path.exists(SRC_DIR):
        raise FileNotFoundError(f"{SRC_DIR} n'existe pas")

    with zipfile.ZipFile(ZIP_PATH, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(SRC_DIR):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, SRC_DIR)
                zipf.write(file_path, arcname)

    print("src.zip créé avec succès")


if __name__ == "__main__":
    create_src_zip()
