import web
import json
import numpy as np
from PIL import Image
import cv2
from split_test import split
from tensorflow_test import predict
from cal import cal

classes = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', "+", "-", "X", "/", "(", ")"]

class Result:
    def POST(self):

        parameters = web.input(_method="POST")
        if "img_data" in parameters:

            img_str = parameters['img_data']

            img_arr = img_str.split(',')

            new_list = []
            for i in range(len(img_arr)):
                if img_arr[i] == "255":
                    new_list.append(255)
                else:
                    new_list.append(0)
            print(len(img_arr))
            # TODO
            img_arr = np.array(img_arr).reshape(202,602,4).astype(np.uint8)
            binary_img_arr = img_arr[:, :, 3]

            print(binary_img_arr)

            # cv2.imshow('img', img_arr)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()

            result = split(img_arr)
            print('要养成良好的编程习惯！', result)

            str = []
            ready_to_compute = ''
            for img in result:
                print('-----下一步为predict------------')
                one = predict(img)
                # str.append(one)
                # print(one)
                ready_to_compute += classes[one]

            print(ready_to_compute)
            print('计算前')
            output_result = cal(ready_to_compute)
            print('返回算式结果：',output_result)


            # save_img(binary_img_arr, "./target.png")
            return output_result
        else:
            return 'No parameters'
    '''
    def get_result(request):
        img_str = request.POST["img_data"]
        global cnn_model
        img_arr = np.array(img_str.split(',')).reshape(200, 1000, 4).astype(np.uint8)
        binary_img_arr = img_arr[:, :, 3]
        print(img_str)
        
        save_img(binary_img_arr, "./target.png")
        data = cv2.imread('./target.png', 2)
        data = 255 - data
        images = get_image_cuts(data, is_data=True, n_lines=1, data_needed=True)
        equation = ""
        cnn_model = model()
        cnn_model.load_model(meta, path)
        digits = list(cnn_model.predict(images))
        for d in digits:
            equation += SYMBOL[d]
        print("数据驱动分析结果：" + equation)
        equation = screen(equation)
        print("知识驱动分析结果：" + equation)
        result = calculate(equation)
        return JsonResponse({"status": "{} = {}".format(equation, result)}, safe=False)

'''
urls = ('/result', Result)

app = web.application(urls)
app.run()
