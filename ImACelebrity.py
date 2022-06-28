import streamlit as st
import time
import matplotlib.pyplot as plt
import numpy as np
import cv2
from bing_image_downloader import downloader
import json
from PIL import Image
import os
import glob


def saveimg(UserPhoto, ListOfExtensions):
    path = 'data/'

    UserPhoto_filename = UserPhoto.name
    extension = os.path.splitext(UserPhoto_filename)[1]

    if extension in ListOfExtensions:
        img = Image.open(UserPhoto)
        if not extension.endswith('.jpg'):
            img = img.convert("RGB")

        img.save(path+'userphoto.jpg')


def Image_Similarity(path_celebrityphoto, celebrity1, celebrity2):
    ProgressBar = st.progress(5)
    image = cv2.imread(path_userphoto)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    histogram = cv2.calcHist([gray_image], [0],
                             None, [256], [0, 256])
    image = cv2.imread(f'{path_celebrityphoto}/{celebrity1}/Image_1.jpg')
    gray_image1 = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    histogram1 = cv2.calcHist([gray_image1], [0],
                              None, [256], [0, 256])
    image = cv2.imread(f'{path_celebrityphoto}/{celebrity2}/Image_1.jpg')
    gray_image2 = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    histogram2 = cv2.calcHist([gray_image2], [0],
                              None, [256], [0, 256])
    c1, c2 = 0, 0
    i = 0
    while i < len(histogram) and i < len(histogram1):
        c1 += (histogram[i] - histogram1[i]) ** 2
        i += 1
    c1 = c1 ** (1 / 2)
    i = 0
    time.sleep(0.5)
    ProgressBar.empty()
    ProgressBar = st.progress(50)
    while i < len(histogram) and i < len(histogram2):
        c2 += (histogram[i] - histogram2[i]) ** 2
        i += 1
    c2 = c2 ** (1 / 2)
    time.sleep(0.5)
    ProgressBar.empty()


    return c1, c2



def ConvertImgFormat(path_celebrityphoto, NewCelebrity):
    for file in glob.glob(f'{path_celebrityphoto}/{NewCelebrity}' + "/*.*"):
        extension = os.path.splitext(file)[1]
        name = os.path.basename(os.path.splitext(file)[0])

        img = Image.open(file)
        if not extension.endswith('.jpg'):
            img = img.convert("RGB")
            os.remove(file)

        img.save(f'{path_celebrityphoto}/{NewCelebrity}/{name}.jpg')

def DownloadNewCelebrity(filename, NewCelebrity):
    with open(filename, 'r', encoding = 'utf8') as readfile:
        ListOfCelebrities = json.load(readfile)

    if NewCelebrity not in ListOfCelebrities:
        downloader.download(NewCelebrity, limit=1, output_dir='dataset', adult_filter_off=True, force_replace=False,
                            timeout=60, verbose=True)
        ConvertImgFormat(path_celebrityphoto, NewCelebrity)

        ListOfCelebrities.append(NewCelebrity)

        with open(filename, 'w', encoding = 'utf8') as outfile:
            json.dump(ListOfCelebrities, outfile, ensure_ascii=False, indent=4)

ListOfExtensions = ['.jpeg', '.png', '.jpg']
path_userphoto = 'data/userphoto.jpg'
path_celebrityphoto = 'dataset'



#Read ListOfCelebrities json file
filename = 'data/ListOfCelebrities.json'
with open (filename, 'r', encoding= "utf8") as readfile:
    ListOfCelebrities = json.load(readfile)


st.image('data/ImACelebrity!!.jpg', width = 800)
title = st.title("I'm a Celebrity!!")

Selection = st.selectbox('Selecione:', ['Selecione uma das opções','Who am I most like?', 'Add a new Celebrity!', 'Algorithm Evaluation'])

if Selection == 'Who am I most like?':
    PersonalPhoto = st.file_uploader('Selecione a sua fotografia.', type=ListOfExtensions)
    if PersonalPhoto is not None:
        saveimg(PersonalPhoto, ListOfExtensions)

    celebrity1 = st.selectbox('Selecione a Celebridade 1:', sorted(ListOfCelebrities))
    col1, col2, col3 = st.columns(3)
    with col2:

        st.image(f'{path_celebrityphoto}/{celebrity1}/Image_1.jpg', width=150)


    celebrity2 = st.selectbox('Selecione a Celebridade 2:', ListOfCelebrities)
    col1, col2, col3 = st.columns(3)
    with col2:

        st.image(f'{path_celebrityphoto}/{celebrity2}/Image_1.jpg', width=150)

    WhoAmIMostLike = st.button('Who am I most like?')

    if WhoAmIMostLike:
        if celebrity1==celebrity2:
            st.warning('Atenção!! Mude uma das celebridades!')

        elif PersonalPhoto is None:
            st.warning('Atenção!! Adicione uma fotografia')

        else:
            c1, c2 = Image_Similarity(path_celebrityphoto, celebrity1, celebrity2)

            ProgressBar = st.progress(75)
            if (c1 < c2):
                st.subheader(f"Es mais parecido com {celebrity1} do que com {celebrity2}")

                col1, col2 = st.columns([0.5, 0.5])
                with col1:

                    st.image(f'{path_celebrityphoto}/{celebrity1}/Image_1.jpg', width=300)

                with col2:

                    st.image(f'{path_userphoto}', width=300)

            else:
                st.subheader(f"Es mais parecido com {celebrity2} do que com {celebrity1}")

                col1, col2 = st.columns([0.5, 0.5])
                with col1:

                    st.image(f'{path_celebrityphoto}/{celebrity2}/Image_1.jpg', width=300)

                with col2:

                    st.image(f'{path_userphoto}', width=300)



            time.sleep(0.5)
            ProgressBar.empty()
            ProgressBar = st.progress(100)
            time.sleep(1.5)
            ProgressBar.empty()

if Selection == 'Add a new Celebrity!':
    NewCelebrity = st.text_input('Escreva o nome de uma nova Celebridade: ', key=str)
    NewCeleButton = st.button('Add a new Celebrity')
    if NewCeleButton:
        DownloadNewCelebrity(filename, NewCelebrity)

if Selection == 'Algorithm Evaluation':
    PercentagemCerto = 56.6
    PercentagemErrado = 100 - PercentagemCerto

    labels = 'Certos', 'Errados'
    sizes = [PercentagemCerto, PercentagemErrado]

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    st.pyplot(fig1)
