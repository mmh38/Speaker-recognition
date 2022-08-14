# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main-simple.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


import time
import librosa
# import required libraries
import sounddevice as sd
import pandas as pd
from PyQt5.QtCore import pyqtSlot
from scipy.io.wavfile import write
import wavio as wv
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog, QLabel, QProgressBar
from playsound import playsound
from keras.models import model_from_json
# from tensorflow.keras.models import Sequential, model_from_json
import noisereduce as nr
import librosa
import numpy as np
class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(900, 445)
        self.layoutWidget = QtWidgets.QWidget(Dialog)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 10, 581, 81))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btnLoadAudioFile = QtWidgets.QPushButton(self.layoutWidget)
        self.btnLoadAudioFile.setObjectName("btnLoadAudioFile")
        self.horizontalLayout.addWidget(self.btnLoadAudioFile)
        self.btnPlayAudioFile = QtWidgets.QPushButton(self.layoutWidget)
        self.btnPlayAudioFile.setObjectName("btnPlayAudioFile")
        self.horizontalLayout.addWidget(self.btnPlayAudioFile)
        self.horizontalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(220, 200, 321, 151))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.labelRes = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.labelRes.setObjectName("labelRes")
        self.horizontalLayout_2.addWidget(self.labelRes)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.resultLabel = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.resultLabel.setText("")
        self.resultLabel.setObjectName("resultLabel")
        self.horizontalLayout_2.addWidget(self.resultLabel)
        self.layoutWidget_2 = QtWidgets.QWidget(Dialog)
        self.layoutWidget_2.setGeometry(QtCore.QRect(610, 10, 161, 81))
        self.layoutWidget_2.setObjectName("layoutWidget_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.layoutWidget_2)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.btnPredict = QtWidgets.QPushButton(self.layoutWidget_2)
        self.btnPredict.setObjectName("btnPredict")
        self.horizontalLayout_3.addWidget(self.btnPredict)

        self.n = 100
        self.loadedFile = 0
        # Connect to function
        self.btnLoadAudioFile.clicked.connect(self.loadAudio)
        self.btnPlayAudioFile.clicked.connect(self.playAudio)
        self.btnPredict.clicked.connect(self.predict)





        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Python GUI"))
        self.btnLoadAudioFile.setText(_translate("Dialog", "Load Audio File"))
        self.btnPlayAudioFile.setText(_translate("Dialog", "Play Voice"))
        self.labelRes.setText(_translate("Dialog", "       RESULT"))
        self.btnPredict.setText(_translate("Dialog", "Predict"))

    def recordAudio(self):
        # Sampling frequency
        # Sampling frequency
        freq = 44100

        # Recording duration
        duration = 5

        # Start recorder with the given values
        # of duration and sample frequency 5 -- 100
        recording = sd.rec(int(duration * freq),
                           samplerate=freq, channels=2)

        # Record audio for the given number of seconds
        sd.wait()

        # This will convert the NumPy array to an audio
        # file with the given sampling frequency
        write("sss0.wav", freq, recording)
        speed = duration / self.n
        for i in range(self.n):
            time.sleep(speed)
            self.progressBar.setValue(i + 1)
        # while(total > 0):
        #     time.sleep(1)
        #     total -= percent
        #     inc += percent
        #     # self.progressBar.setValue(int(inc))
        #     self.progressBar.setValue(int(inc))

    def loadAudio(self):
        fname, filter = QFileDialog.getOpenFileName()
        if fname:
            self.loadedFile = str(fname)
            print(self.loadedFile)
        else:
            print('Ivalid Image')
        # model = load_model('model.h5')
        # model.compile(loss='categorical_crossentropy',
        #               optimizer='adam',
        #               metrics=['acc'])
        # print(self.loadedFile)
        # for i in range(self.n):
        #     time.sleep(1)
        #     self.progressBar.setValue(i + 1)

    def playAudio(self):
        # playsound()
        # playsound(self.loadedFile)
        if(self.loadedFile):
            # samplerate, data = wavfile.read(self.loadedFile)
            playsound(self.loadedFile)
        # self.loadedFile = data
    #
    def predict(self):
        json_path = 'model.json'
        model_path = 'model.h5'

        # load json and create model
        json_file = open(json_path, 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)
        # load weights into new model
        loaded_model.load_weights(model_path)

        # Data preprocessing

        # filenames = next(walk("/content"), (None, None, []))[2]
        X_test = []
        sig_test, sr_test = librosa.load(self.loadedFile)
        n_test = np.random.randint(0, len(sig_test) - (sr_test * 2))
        sig_test_ = sig_test[n_test: int(n_test + (sr_test * 2))]
        mfcc_test_ = librosa.feature.mfcc(sig_test_, sr=sr_test, n_mfcc=13)
        reduced_noise_test = nr.reduce_noise(mfcc_test_, sr_test)
        X_test.append(reduced_noise_test)

        # Data reshaping
        X_test = np.array(X_test)
        a = pd.DataFrame(X_test[0])
        a = a.sample(n=87, axis='columns')
        b = a.to_numpy()
        c = b.reshape(1, 13, 87, 1)

        # Model prediction
        prediction = loaded_model.predict(c)
        speaker_ids = prediction.argmax(axis=1)

        # Speaker name
        if speaker_ids == 0:
            self.labelRes.setStyleSheet("color : green")
            self.labelRes.setStyleSheet("color : green")
            self.resultLabel.setText("Jannatul, Your Voice Recognized \nSuccessfully, Access Granted")
            # return 'Jannatul, you can pass'
        elif speaker_ids == 1:
            self.labelRes.setStyleSheet("color : green")
            self.labelRes.setStyleSheet("color : green")
            self.resultLabel.setText("Mahabuba, Your Voice Recognized \nSuccessfully, Access Granted")
            # return 'Mahabuba, you can pass'
        elif speaker_ids == 2:
            self.labelRes.setStyleSheet("color : green")
            self.labelRes.setStyleSheet("color : green")
            self.resultLabel.setText("Shezan, Your Voice Recognized \nSuccessfully, Access Granted")
            # return 'Shezan, you can pass'
        elif speaker_ids == 3:
            self.labelRes.setStyleSheet("color : red")
            self.labelRes.setStyleSheet("color : red")
            self.resultLabel.setText("Unknown, Your Access Has Been Denied")
            # return 'Unknown identity detected'



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())