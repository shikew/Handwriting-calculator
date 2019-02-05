# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 09:36:55 2018
func：加载模型，进行模型测试
@author: kuangyongjian
"""
import tensorflow as tf
import numpy as np
from PIL import Image
# from model import Network
import cv2

CKPT_DIR = 'ckpt'


# class Predict(object):
#
#     def __init__(self):
#         # 清除默认图的堆栈，并设置全局图为默认图
#         # 若不进行清楚则在第二次加载的时候报错，因为相当于重新加载了两次
#         tf.reset_default_graph()
#         self.net = Network()
#         self.sess = tf.Session()
#         self.sess.run(tf.global_variables_initializer())
#
#         # 加载模型到sess中
#         self.restore()
#         print('load susess')
#
#     def restore(self):
#         saver = tf.train.Saver()
#         ckpt = tf.train.get_checkpoint_state(CKPT_DIR)
#         print(ckpt.model_checkpoint_path)
#         if ckpt and ckpt.model_checkpoint_path:
#             saver.restore(self.sess, ckpt.model_checkpoint_path)
#         else:
#             raise FileNotFoundError('未保存模型')
#
#     def predict(self, image_path):
#         # 读取图片并灰度化
#         img = Image.open(image_path).convert('L')
#         flatten_img = np.reshape(img, 784)
#         x = np.array([1 - flatten_img])
#         y = self.sess.run(self.net.y, feed_dict={self.net.x: x})
#
#         print(image_path)
#         print(' Predict digit', np.argmax(y[0]))


def predict(image):
    image = np.reshape(image, (28, 28, 1))
    meta_path = 'model_data/model.ckpt-12000.meta'
    model_path = 'model_data/model.ckpt-12000'
    saver = tf.train.import_meta_graph(meta_path)  # 导入图

    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    with tf.Session(config=config) as sess:
        saver.restore(sess, model_path)  # 导入变量值
        graph = tf.get_default_graph()
        input = graph.get_tensor_by_name('image_input:0')  # 这个只是获取了operation， 至于有什么用还不知道
        prediction = graph.get_tensor_by_name('predict_op:0')  # 获取之前prob那个操作的输出，即prediction
        result = sess.run(prediction,
                       feed_dict={input:[image]})  # 要想获取这个值，需要输入之前的placeholder （这里我编辑文章的时候是在with里面的，不知道为什么查看的时候就在外面了...）
    return result[0]


if __name__ == '__main__':
    # model = Predict()
    # model.predict('0.png')
    # model.predict('../test_images/1.png')
    # model.predict('../test_images/4.png')
    img = cv2.imread('1002.png', cv2.IMREAD_UNCHANGED)
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    predict(img)

