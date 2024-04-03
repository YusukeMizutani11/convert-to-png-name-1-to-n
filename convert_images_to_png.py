from datetime import datetime
import os
import sys
from PIL import Image
import win32com.client


def get_time_taken(path):
    shell = win32com.client.Dispatch("Shell.Application")
    folder = shell.NameSpace(os.path.dirname(path))
    item = folder.ParseName(os.path.basename(path))
    date_taken = item.ExtendedProperty("System.Photo.DateTaken")
    if date_taken:
        # EXIFから得られた日時がoffset-awareな場合、offset-naiveに変換
        if date_taken.tzinfo is not None and date_taken.tzinfo.utcoffset(date_taken) is not None:
            date_taken = date_taken.replace(tzinfo=None)
    else:
        # 撮影日時が取得できない場合は、ファイルの作成日時を使用
        try:
            ctime = os.path.getctime(path)
            date_taken = datetime.fromtimestamp(ctime)
        except Exception as e:
            print(f"Error getting creation time for {path}: {e}")
            date_taken = datetime.min
    return date_taken


def convert_images_and_sort_by_time_taken(source_folder, target_folder):
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    files = [os.path.join(source_folder, f) for f in os.listdir(
        source_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    files.sort(key=get_time_taken)

    num = 1
    for filepath in files:
        try:
            with Image.open(filepath) as img:
                if img.mode == 'RGBA':
                    img = img.convert('RGB')
                new_name = f"{num}.png"
                target_path = os.path.join(target_folder, new_name)
                img.save(target_path)
                print(f"Saved {os.path.basename(filepath)} as {new_name}")
                num += 1
        except Exception as e:
            print(f"Error processing {filepath}: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python script.py source_folder target_folder")
    else:
        source_folder = sys.argv[1]
        target_folder = sys.argv[2]
        convert_images_and_sort_by_time_taken(source_folder, target_folder)
