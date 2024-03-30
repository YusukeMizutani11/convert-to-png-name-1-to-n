import os
from PIL import Image
import sys


def convert_images_and_sort_by_creation_date(source_folder, target_folder):
    # ターゲットフォルダが存在しない場合は作成
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    # ソースフォルダ内の画像ファイルを作成日時順に並べ替える
    files = [os.path.join(source_folder, f) for f in os.listdir(source_folder)]
    files.sort(key=os.path.getctime)

    # 連番を初期化
    num = 1

    # 並べ替えたファイルリストを処理
    for filepath in files:
        # ファイルの拡張子を確認（画像ファイルのみを対象とする）
        if filepath.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            try:
                with Image.open(filepath) as img:
                    # RGBAをRGBに変換（JPEG保存の場合）
                    if img.mode == 'RGBA':
                        img = img.convert('RGB')
                    # 新しいファイル名を生成（連番 + ".png"）
                    new_name = f"{num}.png"
                    img.save(os.path.join(target_folder, new_name))
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
        convert_images_and_sort_by_creation_date(source_folder, target_folder)
