import imgaug as ia
import imgaug.augmenters as iaa
from imgaug.augmentables.bbs import BoundingBox, BoundingBoxesOnImage
import os
import time
import cv2


def image_augmentation(img_path, save_path):
    try:
        ia.seed(1)

        w = 1920
        h = 1080

        label = ''

        image = cv2.imread(img_path, 1)
        print(img_path.split('/')[4])
        for index in range(10):
            box_pos = []
            with open(img_path.replace('png', 'txt'), 'r') as f:
                line = f.readline()
                label = line.split(" ")[0]
                box_pos = line.split(" ")[1:]

            box_pos = list(map(lambda x: int(x), box_pos))

            bbs = BoundingBoxesOnImage([
                BoundingBox(x1=box_pos[0], y1=box_pos[1], x2=box_pos[2], y2=box_pos[3]),
            ], shape=image.shape)

            # Augmentation parameter
            seq = iaa.Sequential([
                iaa.Crop(percent=(0, 0.1)),  # random crops, 이미지 랜덤하게 크롭
                # Small gaussian blur with random sigma between 0 and 0.5.
                # But we only blur about 50% of all images.
                # 50%로 확률로 블러 넣기
                iaa.Sometimes(
                    0.5,
                    iaa.GaussianBlur(sigma=(0, 0.5))
                ),
                # Strengthen or weaken the contrast in each image.
                # 선형 대비
                iaa.LinearContrast((0.75, 1.5)),
                # Add gaussian noise.
                # For 50% of all images, we sample the noise once per pixel.
                # For the other 50% of all images, we sample the noise per pixel AND
                # channel. This can change the color (not only brightness) of the
                # pixels.
                # 노이즈 추가
                iaa.AdditiveGaussianNoise(loc=0, scale=(0.0, 0.05 * 255), per_channel=0.5),
                # Make some images brighter and some darker.
                # In 20% of all cases, we sample the multiplier once per channel,
                # which can end up changing the color of the images.카
                # 명암 추가
                iaa.Multiply((0.8, 1.2), per_channel=0.2),
                # Apply affine transformations to each image.
                # Scale/zoom them, translate/move them, rotate them and shear them.
                # 아핀 변환
                iaa.Affine(
                    scale={"x": (0.8, 1.2), "y": (0.8, 1.2)},
                    translate_percent={"x": (-0.2, 0.2), "y": (-0.2, 0.2)},
                    rotate=(-25, 25),
                    shear=(-8, 8)
                )
            ], random_order=True)  # apply augmenters in random order

            images_aug, bbs_aug = seq(image=image, bounding_boxes=bbs)

            cv2.imwrite(f'{save_path}_aug{index}.jpg', images_aug)
            after = bbs_aug.bounding_boxes[0]
            yolo_format = convert((w, h), (after.x1, after.x2, after.y1, after.y2))
            with open(f'{save_path}_aug{index}.txt', 'w') as f:
                f.write(f'{label} {yolo_format[0]} {yolo_format[1]} {yolo_format[2]} {yolo_format[3]}')

    except Exception as e:
        print(e)
        print(img_path)


def convert(size, box):
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return x, y, w, h


if __name__ == '__main__':
    blend_path = 'data/korea/blend_data/'

    blend_list = list(filter(lambda x: os.path.isdir(blend_path + x), os.listdir(blend_path)))

    for img_dir in blend_list:
        try:
            if not os.path.exists(f'data/korea/augmentation_data/{img_dir}'):
                # blend_data 폴더에 같은 폴더명 생성
                os.mkdir(f'data/korea/augmentation_data/{img_dir}')
                start = time.time()

                print(img_dir)
                for blend_img in list(filter(lambda x: x.endswith('png'), os.listdir(f'{blend_path}{img_dir}'))):
                    image_augmentation(f'{blend_path}{img_dir}/{blend_img}',
                                       f'data/korea/augmentation_data/{img_dir}/{blend_img.replace(".png", "")}')

                print(time.time() - start)
                print('=' * 20)

        except OSError:
            print('존재하는 디렉토리')
