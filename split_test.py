import cv2
import numpy as np
from tensorflow_test import predict
from matplotlib import pyplot as plt
import cal

def split(img):
    # 载入图片
    # img = cv2.imread('split-img.png')

    lowerb = (0, 0, 116)
    upperb = (255, 255, 255)
    # 根据hsv阈值 进行二值化
    back_mask = cv2.inRange(cv2.cvtColor(img, cv2.COLOR_BGR2HSV), lowerb, upperb)

    cv2.imwrite('number_back_mask_by_hsv_threshold.png', back_mask)

    # 形态学操作， 圆形核腐蚀
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    back_mask = cv2.erode(back_mask, kernel, iterations=1)
    # 反色 变为数字的掩模
    num_mask = cv2.bitwise_not(back_mask)
    # 中值滤波
    num_mask = cv2.medianBlur(num_mask, 3)
    cv2.imwrite('number_mask_filter_by_median.png', num_mask)

    # 寻找轮廓
    bimg, contours, hier = cv2.findContours(num_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 声明画布 拷贝自img
    canvas = cv2.cvtColor(num_mask, cv2.COLOR_GRAY2BGR)


    def getStandardDigit(img):
        '''
            返回标准的数字矩阵
        '''
        STD_WIDTH = 28  # 标准宽度
        STD_HEIGHT = 28

        height, width = img.shape

        # 判断是否存在长条的1
        new_width = int(width * STD_HEIGHT / height)
        if new_width > STD_WIDTH:
            new_width = STD_WIDTH
        # 以高度为准进行缩放
        resized_num = cv2.resize(img, (new_width, STD_HEIGHT), interpolation=cv2.INTER_NEAREST)
        # 新建画布
        canvas = np.zeros((STD_HEIGHT, STD_WIDTH))
        x = int((STD_WIDTH - new_width) / 2)
        canvas[:, x:x + new_width] = resized_num

        return canvas


    minWidth = 5  # 最小宽度
    minHeight = 20  # 最小高度

    base = 1000  # 计数编号
    imgIdx = base  # 当前图片的编号

    result = []

    #对识别出的轮廓按从左到右排序
    counter_list = []
    for cidx, cnt in enumerate(contours):
        counter_list.append(cv2.boundingRect(cnt))
    counter_list = sorted(counter_list)
    print('排序后的轮廓:',counter_list)

    # 检索满足条件的区域
    for counters in counter_list:
        (x, y, w, h) = counters
        if w < minWidth or h < minHeight:
            # 如果不满足条件就过滤掉
            continue
        # 获取ROI图片
        digit = num_mask[y:y + h, x:x + w]
        digit = getStandardDigit(digit)
        cv2.imwrite('./digits_bin/{}.png'.format(imgIdx), digit)
        result.append(digit)
        # cv2.imshow('img', digit)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        imgIdx += 1

        # 原图绘制圆形
        cv2.rectangle(canvas, pt1=(x, y), pt2=(x + w, y + h), color=(0, 255, 255), thickness=2)

    cv2.imwrite('number_mask_mark_rect.png', canvas)

    return result


if __name__ == '__main__':
    classes = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', "+", "-", "X", "/", "(", ")"]
    ready_to_compute = ''
    img = cv2.imread('long.png', cv2.IMREAD_UNCHANGED)
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    print(img.shape)
    result = split(img)
    str = []
    for img in result:
        one = predict(img)
        # str.append(one)
        # print(one)
        ready_to_compute += classes[one]
    print(ready_to_compute)
    output_result = cal.cal(ready_to_compute)
    print(output_result)

    # for image in result:
    #     cv2.imshow('img', image)
    #     cv2.waitKey(0)
    #     cv2.destroyAllWindows()
