import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
import PyQt5.QtTextToSpeech as QTTs


class Speaker:
    def __init__(self,parent,other_controls_widget:qtw.QWidget,text_box:qtw.QTextEdit) -> None:
        # some variables
        self.parent = parent
        self.other_controls_widget = other_controls_widget
        self.editor = text_box
        self.voices_box = None
        self.voices = []
        self.selected_voice = None
        self.speak_btn = None
        self.defaultVoiceRate = 0.0
        self.defaultVoicePitch = 0.0
        self.defaultVoiceVolume = 1.0
        self.voiceRate = None
        self.voicePitch = None
        self.voiceVolume = None

        # set voices in the voices combo box
        self.set_voices_in_box()


        # speak button clicking
        self.speak_btn = self.other_controls_widget.findChild(qtw.QPushButton,"speakButton")
        self.speak_btn.clicked.connect(self.speak)

        # set the rate , pitch , volume
        self.set_rate_voice_pitch()



    def set_voices_in_box(self):
        self.voices_box = self.other_controls_widget.findChild(qtw.QComboBox,"voicesBox")
        self.get_voices()
        self.voices_box.addItems([voice.name() for voice in self.voices])
        self.selected_voice = self.voices[0]
        self.voices_box.currentIndexChanged.connect(lambda index:self.choose_voice(index))


    def get_voices(self):
        self.engine = None
        voiceEngines = QTTs.QTextToSpeech.availableEngines()
        if len(voiceEngines) > 0:
            engineName = voiceEngines[0]
            self.engine = QTTs.QTextToSpeech(engineName,self.parent)
            for voice in self.engine.availableVoices():
                self.voices.append(voice)
                
        else:
            self.voices_box.setDisabled(True)
            self.speak_btn.setDisabled(True)

        

    def choose_voice(self,voice_index:int):
        self.selected_voice =  self.voices[voice_index]


    def set_rate_voice_pitch(self):
        def set_rate():
            self.engine.setRate(self.defaultVoiceRate)
            self.voiceRateSlider.setValue(int(self.defaultVoiceRate))
            
        def set_pitch():
            self.engine.setPitch(self.defaultVoicePitch)
            self.voicePitchSlider.setValue(int(self.defaultVoicePitch))

        def set_volume():
            self.engine.setVolume(self.defaultVoiceVolume)
            self.voiceVolumeSlider.setValue(int(self.defaultVoiceVolume))

        # setting  rate 
        self.voiceRateSlider = self.other_controls_widget.findChild(qtw.QSlider,"voiceRate")
        reset_voice_rate = qtw.QAction("Reset Voice Rate",self.voiceRateSlider)
        self.voiceRateSlider.addAction(reset_voice_rate)
        reset_voice_rate.triggered.connect(set_rate)
        self.voiceRateSlider.valueChanged.connect(lambda n:self.engine.setRate(float(-n)))

        # setting pitch
        self.voicePitchSlider = self.other_controls_widget.findChild(qtw.QSlider,"voicePitch")
        reset_voice_pitch = qtw.QAction("Reset Voice Pitch",self.voicePitchSlider)
        self.voicePitchSlider.addAction(reset_voice_pitch)
        reset_voice_pitch.triggered.connect(set_pitch)
        self.voicePitchSlider.valueChanged.connect(lambda n:self.engine.setPitch(float(-n)))

        # setting volume
        self.voiceVolumeSlider = self.other_controls_widget.findChild(qtw.QSlider,"voiceVolume")
        reset_voice_volume = qtw.QAction("Reset Voice Volume",self.voiceVolumeSlider)
        self.voiceVolumeSlider.addAction(reset_voice_volume)
        reset_voice_volume.triggered.connect(set_volume)
        self.voiceVolumeSlider.valueChanged.connect(lambda n:self.engine.setVolume(float(n)))


    def speak(self):
        cursor = self.editor.textCursor()
        text = cursor.selectedText()
        self.engine.setVoice(self.selected_voice)
        self.engine.say(text)
        
            