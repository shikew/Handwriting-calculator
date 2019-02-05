import cv2
import numpy as np
from sklearn import svm,datasets
from scipy.io import loadmat
from sklearn import neighbors

 #数据预处理
result_dict=loadmat("mnist-extend")

print(result_dict)

print('target: ',result_dict['target'].shape)

train_data = np.array(result_dict['data'], 'int16')
train_target = np.array(result_dict['target'], 'int').T
print(result_dict['target'])
print(train_target.shape)
print(train_target)
#
print('图片数据的shape：',train_data.shape)
train_data = train_data.astype('float32')
# train_data = train_data/255   #归一化
#
train_target = train_target.flatten()
print('flatten后的target：',train_target)
print('flatten后的target的shape：',train_target.shape)
print('自己数据集的data：',train_data)
print(train_data[0])

train_data1 = train_data[:60000]
train_data2 = train_data[70000:103895]
train_target1 = train_target[:60000]
train_target2 = train_target[70000:103895]
final_data = np.concatenate((train_data1, train_data2))
final_target = np.concatenate((train_target1, train_target2))  #训练数据及标签

test_data = train_data[60000:70000]
test_target = train_target[60000:70000]   #测试数据及标签

print(final_data[0])


#svm 训练模型
print('---------开始训练模型---------------')
knn = neighbors.KNeighborsClassifier(algorithm='kd_tree', n_neighbors=4)

print('-----------下一步是fit---------------')
knn.fit(final_data, final_target)

print('---------预测-------------')
res = knn.predict(test_data)  #对测试集进行预测
error_num = np.sum(res != test_target) #统计分类错误的数目
num = len(test_data)          #测试集的数目
print("Total num:",num," Wrong num:", \
      error_num,"  WrongRate:",error_num / float(num))
