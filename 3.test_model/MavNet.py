import tflearn
from tflearn.layers.conv import conv_2d, max_pool_2d,avg_pool_2d, conv_3d, max_pool_3d, avg_pool_3d
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression
from tflearn.layers.normalization import local_response_normalization
from tflearn.layers.merge_ops import merge


def mavnet(width, height, frame_count, lr, output=5, model_name = 'mavNet.model'):
    network = input_data(shape=[None, width, height,1], name='input')
    conv1_7_7 = conv_2d(network, 64, 7, strides=2, activation='relu', name = 'conv1_7_7_s2')
    pool1_3_3 = max_pool_2d(conv1_7_7, 3,strides=2)
    pool1_3_3 = local_response_normalization(pool1_3_3)
    conv2_3_3_reduce = conv_2d(pool1_3_3, 64,1, activation='relu',name = 'conv2_3_3_reduce')
    conv2_3_3 = conv_2d(conv2_3_3_reduce, 192,3, activation='relu', name='conv2_3_3')
    conv2_3_3 = local_response_normalization(conv2_3_3)
    pool2_3_3 = max_pool_2d(conv2_3_3, kernel_size=3, strides=2, name='pool2_3_3_s2')
    mavnet_3a_1_1 = conv_2d(pool2_3_3, 64, 1, activation='relu', name='mavnet_3a_1_1')
    mavnet_3a_3_3_reduce = conv_2d(pool2_3_3, 96,1, activation='relu', name='mavnet_3a_3_3_reduce')
    mavnet_3a_3_3 = conv_2d(mavnet_3a_3_3_reduce, 128,filter_size=3,  activation='relu', name = 'mavnet_3a_3_3')
    mavnet_3a_pool = max_pool_2d(pool2_3_3, kernel_size=3, strides=1, )
    mavnet_3a_pool_1_1 = conv_2d(mavnet_3a_pool, 32, filter_size=1, activation='relu', name='mavnet_3a_pool_1_1')

    # merge the mavnet_3a__
    mavnet_3a_output = merge([mavnet_3a_1_1, mavnet_3a_3_3, mavnet_3a_pool_1_1], mode='concat', axis=3)
    mavnet_3b_1_1 = conv_2d(mavnet_3a_output, 128,filter_size=1,activation='relu', name= 'mavnet_3b_1_1' )
    mavnet_3b_3_3_reduce = conv_2d(mavnet_3a_output, 128, filter_size=1, activation='relu', name='mavnet_3b_3_3_reduce')
    mavnet_3b_3_3 = conv_2d(mavnet_3b_3_3_reduce, 192, filter_size=3,  activation='relu',name='mavnet_3b_3_3')
    mavnet_3b_pool = max_pool_2d(mavnet_3a_output, kernel_size=3, strides=1,  name='mavnet_3b_pool')
    mavnet_3b_pool_1_1 = conv_2d(mavnet_3b_pool, 64, filter_size=1,activation='relu', name='mavnet_3b_pool_1_1')

    #merge the mavnet_3b_*
    mavnet_3b_output = merge([mavnet_3b_1_1, mavnet_3b_3_3, mavnet_3b_pool_1_1], mode='concat',axis=3,name='mavnet_3b_output')

    pool3_3_3 = max_pool_2d(mavnet_3b_output, kernel_size=3, strides=2, name='pool3_3_3')
    mavnet_4a_1_1 = conv_2d(pool3_3_3, 192, filter_size=1, activation='relu', name='mavnet_4a_1_1')
    mavnet_4a_3_3_reduce = conv_2d(pool3_3_3, 96, filter_size=1, activation='relu', name='mavnet_4a_3_3_reduce')
    mavnet_4a_3_3 = conv_2d(mavnet_4a_3_3_reduce, 208, filter_size=3,  activation='relu', name='mavnet_4a_3_3')
    mavnet_4a_pool = max_pool_2d(pool3_3_3, kernel_size=3, strides=1,  name='mavnet_4a_pool')
    mavnet_4a_pool_1_1 = conv_2d(mavnet_4a_pool, 64, filter_size=1, activation='relu', name='mavnet_4a_pool_1_1')

    mavnet_4a_output = merge([mavnet_4a_1_1, mavnet_4a_3_3, mavnet_4a_pool_1_1], mode='concat', axis=3, name='mavnet_4a_output')


    mavnet_4b_1_1 = conv_2d(mavnet_4a_output, 160, filter_size=1, activation='relu', name='mavnet_4a_1_1')
    mavnet_4b_3_3_reduce = conv_2d(mavnet_4a_output, 112, filter_size=1, activation='relu', name='mavnet_4b_3_3_reduce')
    mavnet_4b_3_3 = conv_2d(mavnet_4b_3_3_reduce, 224, filter_size=3, activation='relu', name='mavnet_4b_3_3')
    mavnet_4b_pool = max_pool_2d(mavnet_4a_output, kernel_size=3, strides=1,  name='mavnet_4b_pool')
    mavnet_4b_pool_1_1 = conv_2d(mavnet_4b_pool, 64, filter_size=1, activation='relu', name='mavnet_4b_pool_1_1')

    mavnet_4b_output = merge([mavnet_4b_1_1, mavnet_4b_3_3, mavnet_4b_pool_1_1], mode='concat', axis=3, name='mavnet_4b_output')


    mavnet_4c_1_1 = conv_2d(mavnet_4b_output, 128, filter_size=1, activation='relu',name='mavnet_4c_1_1')
    mavnet_4c_3_3_reduce = conv_2d(mavnet_4b_output, 128, filter_size=1, activation='relu', name='mavnet_4c_3_3_reduce')
    mavnet_4c_3_3 = conv_2d(mavnet_4c_3_3_reduce, 256,  filter_size=3, activation='relu', name='mavnet_4c_3_3')

    mavnet_4c_pool = max_pool_2d(mavnet_4b_output, kernel_size=3, strides=1)
    mavnet_4c_pool_1_1 = conv_2d(mavnet_4c_pool, 64, filter_size=1, activation='relu', name='mavnet_4c_pool_1_1')

    mavnet_4c_output = merge([mavnet_4c_1_1, mavnet_4c_3_3, mavnet_4c_pool_1_1], mode='concat', axis=3,name='mavnet_4c_output')

    mavnet_4d_1_1 = conv_2d(mavnet_4c_output, 112, filter_size=1, activation='relu', name='mavnet_4d_1_1')
    mavnet_4d_3_3_reduce = conv_2d(mavnet_4c_output, 144, filter_size=1, activation='relu', name='mavnet_4d_3_3_reduce')
    mavnet_4d_3_3 = conv_2d(mavnet_4d_3_3_reduce, 288, filter_size=3, activation='relu', name='mavnet_4d_3_3')
    mavnet_4d_pool = max_pool_2d(mavnet_4c_output, kernel_size=3, strides=1,  name='mavnet_4d_pool')
    mavnet_4d_pool_1_1 = conv_2d(mavnet_4d_pool, 64, filter_size=1, activation='relu', name='mavnet_4d_pool_1_1')

    mavnet_4d_output = merge([mavnet_4d_1_1, mavnet_4d_3_3, mavnet_4d_pool_1_1], mode='concat', axis=3, name='mavnet_4d_output')

    mavnet_4e_1_1 = conv_2d(mavnet_4d_output, 256, filter_size=1, activation='relu', name='mavnet_4e_1_1')
    mavnet_4e_3_3_reduce = conv_2d(mavnet_4d_output, 160, filter_size=1, activation='relu', name='mavnet_4e_3_3_reduce')
    mavnet_4e_3_3 = conv_2d(mavnet_4e_3_3_reduce, 320, filter_size=3, activation='relu', name='mavnet_4e_3_3')

    mavnet_4e_pool = max_pool_2d(mavnet_4d_output, kernel_size=3, strides=1,  name='mavnet_4e_pool')
    mavnet_4e_pool_1_1 = conv_2d(mavnet_4e_pool, 128, filter_size=1, activation='relu', name='mavnet_4e_pool_1_1')


    mavnet_4e_output = merge([mavnet_4e_1_1, mavnet_4e_3_3,mavnet_4e_pool_1_1],axis=3, mode='concat')

    pool4_3_3 = max_pool_2d(mavnet_4e_output, kernel_size=3, strides=2, name='pool_3_3')


    mavnet_5a_1_1 = conv_2d(pool4_3_3, 256, filter_size=1, activation='relu', name='mavnet_5a_1_1')
    mavnet_5a_3_3_reduce = conv_2d(pool4_3_3, 160, filter_size=1, activation='relu', name='mavnet_5a_3_3_reduce')
    mavnet_5a_3_3 = conv_2d(mavnet_5a_3_3_reduce, 320, filter_size=3, activation='relu', name='mavnet_5a_3_3')
    mavnet_5a_pool = max_pool_2d(pool4_3_3, kernel_size=3, strides=1,  name='mavnet_5a_pool')
    mavnet_5a_pool_1_1 = conv_2d(mavnet_5a_pool, 128, filter_size=1,activation='relu', name='mavnet_5a_pool_1_1')

    mavnet_5a_output = merge([mavnet_5a_1_1, mavnet_5a_3_3, mavnet_5a_pool_1_1], axis=3,mode='concat')


    mavnet_5b_1_1 = conv_2d(mavnet_5a_output, 384, filter_size=1,activation='relu', name='mavnet_5b_1_1')
    mavnet_5b_3_3_reduce = conv_2d(mavnet_5a_output, 192, filter_size=1, activation='relu', name='mavnet_5b_3_3_reduce')
    mavnet_5b_3_3 = conv_2d(mavnet_5b_3_3_reduce, 384,  filter_size=3,activation='relu', name='mavnet_5b_3_3')
    mavnet_5b_pool = max_pool_2d(mavnet_5a_output, kernel_size=3, strides=1,  name='mavnet_5b_pool')
    mavnet_5b_pool_1_1 = conv_2d(mavnet_5b_pool, 128, filter_size=1, activation='relu', name='mavnet_5b_pool_1_1')
    mavnet_5b_output = merge([mavnet_5b_1_1, mavnet_5b_3_3, mavnet_5b_pool_1_1], axis=3, mode='concat')

    pool5_7_7 = avg_pool_2d(mavnet_5b_output, kernel_size=7, strides=1)
    pool5_7_7 = dropout(pool5_7_7, 0.4)


    loss = fully_connected(pool5_7_7, output,activation='softmax')



    network = regression(loss, optimizer='momentum',
                         loss='categorical_crossentropy',
                         learning_rate=lr, name='targets')

    model = tflearn.DNN(network,
                        max_checkpoints=0, tensorboard_verbose=0,tensorboard_dir='log')


    return model
