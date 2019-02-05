import numpy as np
from PIL import Image
from keras.models import load_model

img_gray = Image.open('1002.png')
number = np.array(img_gray)
print(number.shape)
print('准备的图片的shape：',number.flatten().shape)
print('原number:',number)
number = number.astype('float32')
number = number/255   #归一化
number = number.flatten()
print('处理过后的number.shape:',number.shape)

model = load_model('mnist-dnn.h5')
# model.load_weights('mnist.model.best.hdf5')
# def recognize(photo_data):
#     return clf.predict(photo_data)

print(model.predict_classes(np.array([number])))
#print('测试标签为：',test_target[8000])