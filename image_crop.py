import cv2, sys
import glob
import numpy as np
import time
import os


def crop_coin(img_path, img_dir, img_name):
    try:
        # 이미지 불러오기
        origin = cv2.imread(img_path)
        img = cv2.imread(img_path, 0)

        k = 5

        img = cv2.GaussianBlur(img, (k, k), 0)
        cimg = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 100, param1=20, param2=100, minRadius=150, maxRadius=500)
        circles = np.uint16(np.around(circles))

        for i in circles[0, :]:
            cv2.circle(cimg, (i[0], i[1]), i[2], (0, 255, 0), 10)

        # 원이 한개일 때
        if len(circles) == 1:
            x, y, r = circles[0][0]

            # image trim 하기, 시작점을 동전의 왼쪽 위로
            x = x - r
            y = y - r
            w = h = 2 * r

            img_trim = origin[y:y + h, x:x + w]
            # 이미지 저장
            cv2.imwrite(f'data/korea/crop_data/{img_dir}/{img_name}', img_trim)
    except Exception as e:
        print(f'Error: {e}')
        print(f'{img_name}')
        print('원이 검출되지 않음')


if __name__ == '__main__':
    path = 'data/korea/original_data/'
    dir_list = list(filter(lambda x: os.path.isdir(path + x), os.listdir(path)))

    for img_dir in dir_list:
        print(f'Dir name : {img_dir}')

        try:
            if not os.path.exists(f'data/korea/crop_data/{img_dir}'):
                # crop_data 폴더에 같은 폴더명 생성
                os.mkdir(f'data/korea/crop_data/{img_dir}')
                start = time.time()
                for img_file in os.listdir(path + img_dir):
                    img_path = f'{path}{img_dir}/{img_file}'
                    crop_coin(img_path, img_dir, img_file)

                print(time.time() - start)
                print('=' * 20)

        except OSError:
            print('존재하는 디렉토리')

