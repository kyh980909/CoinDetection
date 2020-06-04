import cv2
import glob
import os

mp4_list = glob.glob('data/korea/original_data/*.MOV')

for dir_name in mp4_list:
    new_dir_name = dir_name.split('/')[3].replace('.MOV', '')

    try:
        if not os.path.exists('data/korea/original_data/' + new_dir_name):
            os.mkdir('data/korea/original_data/' + new_dir_name)

            # 영상의 이미지를 연속적으로 캡쳐할 수 있게 하는 class
            video_cap = cv2.VideoCapture(dir_name)

            count = 0

            while video_cap.isOpened():
                ret, image = video_cap.read()

                if ret:
                    if int(video_cap.get(1)) % 10 == 0:
                        print(f'Saved frame number: {str(int(video_cap.get(1)))}')
                        cv2.imwrite(f'data/korea/original_data/{new_dir_name}/{new_dir_name}_{count}.jpg', image)

                        print(f'Saved frame {new_dir_name}_{count}.jpg')
                        count += 1

                else:
                    break

            video_cap.release()

            print('다음 영상')
    except OSError:
        print('존재하는 디렉토리')
