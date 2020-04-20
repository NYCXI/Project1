import cv2
from retinaface import RetinaFace
import sys
import numpy as np
import os
import datetime
import glob
import face_model
import argparse
import random



def detect_face(img):
    thresh = 0.8
    scales = [1024, 1980]
    count = 1
    gpuid = 0
    detector = RetinaFace('./model/R50', 0, gpuid, 'net3')
    im_shape = img.shape
    target_size = scales[0]
    max_size = scales[1]
    im_size_min = np.min(im_shape[0:2])
    im_size_max = np.max(im_shape[0:2])

    im_scale = float(target_size) / float(im_size_min)

    if np.round(im_scale * im_size_max) > max_size:
        im_scale = float(max_size) / float(im_size_max)

    scales = [im_scale]
    flip = False
    
    for c in range(count):
        faces, landmarks = detector.detect(img, thresh, scales = scales, do_flip = flip)
        print(c, faces.shape, landmarks.shape)

    face = []
    box = []
    boxx = []
    '''
    if faces is not None:
        for i in range(faces):    
            box2 = faces[i].astype(np.int)
            box.append(box2)
            #color = (0, 0, 255)

            face.append(img[box2[0]:box2[1], box2[2]:box2[3]])
            cv2.imshow('face', img[box2[0]:box2[1], box2[2]:box2[3]])
    '''
    
    if faces is not None:
        for i in range(faces.shape[0]):
            
            box_temp = faces[i].astype(np.int)
            x1 = box_temp[1] - 10
            if x1 < 0:
                x1 = 0
            y1 = box_temp[3] + 10
            if y1 > img.shape[1]:
                y1 = img.shape[1]
            x2 = box_temp[0] - 10
            if x2 < 0:
                x2 = 0
            y2 = box_temp[2] + 10
            if y2 > img.shape[1]:
                y2 = img.shape[1]
            face_temp = img[x1 : y1, x2 : y2]
            face.append(face_temp)
            box.append(box_temp)
            print(face_temp.shape)
            #cv2.imshow(str(i), face_temp)
            cv2.waitKey(1)
            box1 = []
            box1.append(x1)
            box1.append(y1)
            box1.append(x2)
            box1.append(y2)
            boxx.append(box1)
            

    return face, box, boxx

def identify_gender_age(face_img, args):
    model = face_model.FaceModel(args)
    face_list = []
    face = face_img
    print('facee', face.shape)
    #cv2.imshow('faceee', face)
    facedb = model.get_input(face)
    if facedb is not None:
        gender, age = model.get_ga(facedb)
    else:
        gender = -1
        age = -1
    return gender, age

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--image-size', default = '122,122')
    parser.add_argument('--image', default = '')
    parser.add_argument('--model', default = 'model/model,0', help = 'model path')
    parser.add_argument('--gpu', default = 0, type = int, help = 'gpu id')
    parser.add_argument('--det', default = 0, type = int, help = 'mtcnn option')
    parser.add_argument('--video', default = 'test2.mp4', help = 'input video')
    args = parser.parse_args()
    return args

def main():
    args = get_args()
    cap = cv2.VideoCapture(args.video)
    fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    out = cv2.VideoWriter('out.mp4',fourcc, int(cap.get(cv2.CAP_PROP_FPS)), (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))
    if cap is not None:
        print('successfully load video')
    num = 0
    while(cap.isOpened()):
        retval, frame = cap.read()
        if retval == True:
            args.image_size = frame.shape
            args.image = frame
            face, box, boxx= detect_face(frame)
            print(len(face))
            if face is not None:
                print('face_num', len(face))
                for i in range(len(face)):
                    print(face[i].shape[0: 2])
                    print(face[i].shape)
                    args.image_size = face[i].shape[0:2]
                    gender, age = identify_gender_age(face[i], args)
                    box1 = box[i]
                    boxx1 = boxx[i]
                    cv2.rectangle(frame, (box1[0], box1[1]), (box1[2], box1[3]), (0, 0, 255), 2)
                    #cv2.rectangle(frame, (boxx1[2], boxx1[0]), (boxx1[3], boxx1[1]), (0, 255, 0), 2)
                    cv2.rectangle(frame, (boxx1[3], boxx1[1]), (boxx1[2], boxx1[0]), (0, 255, 0), 2)
                    cv2.putText(frame, 'gender:' + str(gender) +' age:' + str(age), (box1[2], box1[3]), cv2.FONT_HERSHEY_PLAIN, 2.0, (0, 0, 255), 1)
            out.write(frame)
            print(num)
            num += 1
        else:
            break
        ch = cv2.waitKey(0)
    cap.release()
    out.release()

def main2():
    args = get_args()
    filepath_picname = "F:/megaage_asian/megaage_asian/list/test_name.txt"
    filepath_picage = "F:/megaage_asian/megaage_asian/list/test_age.txt"
    f1 = open(filepath_picname, "r")
    f2 = open(filepath_picage, "r")

    picname = []
    picage = []
    #读取test_name
    for line in f1.readlines():
        picname.append(line)
    f1.close()
    #读取test_age
    for line in f2.readlines():
        picage.append(line)
    f2.close()
    fr = open("TestRes.txt", "w")
    c = 0
    count1 = 0
    count2 = 0
    count3 = 0
    os.makedirs(".\\images")
    while c < 200:
        c = c + 1
        t = random.randint(0,len(picname))
        picpath = "F:\\megaage_asian\\megaage_asian\\test\\" + picname[t][0:-1]
        storepath = ".\\images\\" + picname[t][0:-1]
        pic_info = (picpath, picage[t])
        print(pic_info[0],pic_info[1])
        img = cv2.imread(pic_info[0])
        cv2.imwrite(storepath, img)
        if img is None:
            print("load img failed")
            break
        args.image_size = img.shape
        args.image = img
        face, box, boxx = detect_face(img)
        if face is not None:
            for i in range(len(face)):
                args.image_size = face[i].shape[0:2]
                gender, age = identify_gender_age(face[i], args)
                fr.write("num: " + str(c) + "    pic: " + picname[t][0:-1] + "   gender: " + str(gender) + "/ " + "   age: " + str(age) + "/" + pic_info[1][0:-1] + "\n")
                if int(pic_info[1][0:-1]) == age:
                    count1 += 1
                if abs(int(pic_info[1][0:-1]) - age) < 3:
                    count2 += 1
                if abs(int(pic_info[1][0:-1]) - age) < 5:
                    count3 += 1
                print("num: " + str(c) + "    pic: " + picname[t][0:-1] + "   gender: " + str(gender) + "/ " + "   age: " + str(age) + "/" + pic_info[1][0:-1] + "\n")
    fr.write("res:  a: " + str(count1) + "/200   b: " + str(count2) + "/200   c: " + str(count3) + "/200")
    fr.close()



if __name__ == '__main__':
    main2()