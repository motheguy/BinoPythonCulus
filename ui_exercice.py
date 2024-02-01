from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget 
from PyQt5.QtWidgets import QSizePolicy, QWidget, QTabWidget
from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QHBoxLayout 
from PyQt5.QtWidgets import QDateEdit, QComboBox, QLabel, QLineEdit, QSlider, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QPixmap

from exercice import Infinite
from exercice import Saccade
from exercice import Fixation

from ui_customDialog import CustomDialog 
from recording import CSV_recorder
#from cam_video_world import CameraWorld
from ui_calibration import UI_calibration

class UI_main_excercice(QWidget):
    def __init__(self, connected_patient, selected_config):
        super().__init__()
        self.__connected_patient = connected_patient
        self.__selected_config = selected_config

        # Create a sub-tab widget
        sub_tabs = QTabWidget()
        sub_tab1 = UI_saccade(self.__connected_patient, self.__selected_config)
        sub_tab2 = UI_fixation(self.__connected_patient, self.__selected_config)
        sub_tab3 = UI_infinite(self.__connected_patient, self.__selected_config)
        sub_tabs.addTab(sub_tab1, "Saccade")
        sub_tabs.addTab(sub_tab2, "Fixation")
        sub_tabs.addTab(sub_tab3, "Infini")

        # Create a label and line edit for the common interface for Calibration
        self.ui_calibration = UI_calibration()

        layout_exo = QVBoxLayout()
        layout_exo.addWidget(sub_tabs)
        layout_exo.addWidget(self.ui_calibration.group_box_calibration)
        
        #cam_world = CameraWorld()

        layout = QHBoxLayout()
        layout.addLayout(layout_exo)
        #layout.addWidget(cam_world)
        
        self.setLayout(layout)

class UI_saccade(QWidget):
    def __init__(self, connected_patient, selected_config):
        super().__init__()
        self.__is_button_start_saccade_on = False
        self.saccade = Saccade()
        self.__connected_patient = connected_patient
        self.__selected_config = selected_config

        size_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # Create a QLabel to display the recording status
        self.recording_label = QLabel(self)
        self.recording_label.setGeometry(10, 10, 50, 50) 
        self.recording_pixmap = QPixmap('record_icon.png')  

        label_color = QLabel("Select color")
        combo_box_color = QComboBox()
        combo_box_color.setSizePolicy(size_policy)
        combo_box_color.setFixedWidth(300)
        combo_box_color.addItem("Black", QColor("black"))
        combo_box_color.addItem("Red", QColor("red"))
        combo_box_color.addItem("Blue", QColor("blue"))
        combo_box_color.setCurrentIndex(0)
        layout_color = QHBoxLayout()
        layout_color.addWidget(label_color)
        layout_color.addWidget(combo_box_color)

        label_size = QLabel("Select size")
        self.slider_size = QSlider(Qt.Horizontal, self)
        self.slider_size.setSizePolicy(size_policy)
        self.slider_size.setFixedWidth(285)
        self.slider_size.setMinimum(0)
        self.slider_size.setMaximum(100)
        self.slider_size.setSliderPosition(50)
        self.slider_size.valueChanged.connect(self.update_slider_size_value)
        self.label_slider_size_value = QLabel()
        self.label_slider_size_value.setSizePolicy(size_policy)
        self.label_slider_size_value.setFixedWidth(15)
        self.label_slider_size_value.setText(str(self.slider_size.value()))
        layout_size = QHBoxLayout()
        layout_size.addWidget(label_size)
        layout_size.addWidget(self.slider_size)
        layout_size.addWidget(self.label_slider_size_value)

        label_time_step = QLabel("Select time step (ms)")
        self.slider_time_step = QSlider(Qt.Horizontal, self)
        self.slider_time_step.setSizePolicy(size_policy)
        self.slider_time_step.setFixedWidth(285)
        self.slider_time_step.setMinimum(100)
        self.slider_time_step.setMaximum(5000)
        self.slider_time_step.setSliderPosition(1000)
        self.slider_time_step.valueChanged.connect(self.update_slider_time_step_value)
        self.label_slider_time_step_value = QLabel()
        self.label_slider_time_step_value.setSizePolicy(size_policy)
        self.label_slider_time_step_value.setFixedWidth(15)
        self.label_slider_time_step_value.setText(str(self.slider_time_step.value()))
        layout_time_step = QHBoxLayout()
        layout_time_step.addWidget(label_time_step)
        layout_time_step.addWidget(self.slider_time_step)
        layout_time_step.addWidget(self.label_slider_time_step_value)

        label_delta_horizontal = QLabel("Delta horizontal")
        self.slider_delta_horizontal = QSlider(Qt.Horizontal, self)
        self.slider_delta_horizontal.setSizePolicy(size_policy)
        self.slider_delta_horizontal.setFixedWidth(300)
        self.slider_delta_horizontal.setMinimum(0)
        self.slider_delta_horizontal.setMaximum(1000)
        self.slider_delta_horizontal.setSliderPosition(0)
        self.slider_delta_horizontal.valueChanged.connect(self.update_slider_delta_horizontal_value)
        self.label_slider_delta_horizontal_value = QLabel()
        self.label_slider_delta_horizontal_value.setSizePolicy(size_policy)
        self.label_slider_delta_horizontal_value.setFixedWidth(15)
        self.label_slider_delta_horizontal_value.setText(str(self.slider_delta_horizontal.value()))
        layout_delta_horizontal = QHBoxLayout()
        layout_delta_horizontal.addWidget(label_delta_horizontal)
        layout_delta_horizontal.addWidget(self.slider_delta_horizontal)
        layout_delta_horizontal.addWidget(self.label_slider_delta_horizontal_value)

        label_delta_vertical = QLabel("Delta vertical")
        self.slider_delta_vertical = QSlider(Qt.Horizontal, self)
        self.slider_delta_vertical.setSizePolicy(size_policy)
        self.slider_delta_vertical.setFixedWidth(300)
        self.slider_delta_vertical.setMinimum(0)
        self.slider_delta_vertical.setMaximum(1000)
        self.slider_delta_vertical.setSliderPosition(200)
        self.slider_delta_vertical.valueChanged.connect(self.update_slider_delta_vertical_value)
        self.label_slider_delta_vertical_value = QLabel()
        self.label_slider_delta_vertical_value.setSizePolicy(size_policy)
        self.label_slider_delta_vertical_value.setFixedWidth(15)
        self.label_slider_delta_vertical_value.setText(str(self.slider_delta_vertical.value()))
        layout_delta_vertical = QHBoxLayout()
        layout_delta_vertical.addWidget(label_delta_vertical)
        layout_delta_vertical.addWidget(self.slider_delta_vertical)
        layout_delta_vertical.addWidget(self.label_slider_delta_vertical_value)

        button_start_exercice_saccade = QPushButton("Start")
        button_start_exercice_saccade.clicked.connect(lambda: self.start_exercice_saccade(self.slider_size.value(), 
            QColor(combo_box_color.currentData()), 
            self.slider_time_step.value(), 
            self.slider_delta_horizontal.value(), 
            self.slider_delta_vertical.value()
            ))

        self.button_start_recording = QPushButton("Start")
        self.button_start_recording.clicked.connect(self.start_recording)

        self.button_stop_recording = QPushButton("Stop")
        self.button_stop_recording.clicked.connect(self.stop_recording)

        layout_recording = QHBoxLayout()
        layout_recording.addWidget(self.button_start_recording)
        layout_recording.addWidget(self.button_stop_recording) 
        
        layout_recording_im = QVBoxLayout()
        layout_recording_im.addLayout(layout_recording)
        layout_recording_im.addWidget(self.recording_label)

        group_box_recording = QGroupBox("Recording")
        group_box_recording.setLayout(layout_recording_im)

        self.layout = QVBoxLayout()
        self.layout.addLayout(layout_color)
        self.layout.addLayout(layout_size)
        self.layout.addLayout(layout_time_step)
        self.layout.addLayout(layout_delta_horizontal)
        self.layout.addLayout(layout_delta_vertical)
        self.layout.addWidget(button_start_exercice_saccade)
        self.layout.addWidget(group_box_recording)

        self.setLayout(self.layout)

    def update_slider_size_value(self):
        self.label_slider_size_value.setText(str(self.slider_size.value()))

    def update_slider_time_step_value(self):
        self.label_slider_time_step_value.setText(str(self.slider_time_step.value()))

    def update_slider_delta_horizontal_value(self):
        self.label_slider_delta_horizontal_value.setText(str(self.slider_delta_horizontal.value()))

    def update_slider_delta_vertical_value(self):
        self.label_slider_delta_vertical_value.setText(str(self.slider_delta_vertical.value()))

    def start_exercice_saccade(self, size, color, time_step, delta_horizontal, delta_vertical):
        self.saccade.set_is_running(True)
        self.saccade.set_size(size)
        self.saccade.set_color(color)
        self.saccade.set_time_step(time_step) 
        self.saccade.set_delta_horizontal(delta_horizontal)
        self.saccade.set_delta_vertical(delta_vertical)
        
        screen = QDesktopWidget().screenGeometry(1)
        self.saccade.setGeometry(screen)
        self.saccade.showMaximized()
        self.__is_button_start_saccade_on = True

    def start_recording(self):
        if self.__is_button_start_saccade_on:
            if self.__connected_patient.get_codePatient() != "None" or self.__selected_config.get_name_config() != "None":
                csv_recorder = CSV_recorder()
                csv_recorder.set_filename(csv_recorder.generate_filename(self.__connected_patient.get_codePatient(), "Saccade"))
                csv_recorder.set_header()

                self.saccade.set_csv_recorder(csv_recorder)

                self.recording_label.setPixmap(self.recording_pixmap.scaled(self.recording_label.width(), self.recording_label.height(), Qt.KeepAspectRatio))

                self.saccade.set_is_recording(True)
            else:
                dlg = CustomDialog(message="Connecte to a patient and a config")
                dlg.exec()
        else: 
            dlg = CustomDialog(message="Start fixation first")
            dlg.exec()

    def stop_recording(self):
        self.saccade.set_is_recording(False)
        self.recording_label.clear()

class UI_fixation(QWidget):
    def __init__(self, connected_patient, selected_config):
        super().__init__()
        self.__is_button_start_fixation_on = False
        self.fixation = Fixation()
        self.__connected_patient = connected_patient
        self.__selected_config = selected_config

        size_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # Create a QLabel to display the recording status
        self.recording_label = QLabel(self)
        self.recording_label.setGeometry(10, 10, 50, 50) 
        self.recording_pixmap = QPixmap('record_icon.png') 

        label_color = QLabel("Select color")
        combo_box_color = QComboBox()
        combo_box_color.setSizePolicy(size_policy)
        combo_box_color.setFixedWidth(300)
        combo_box_color.addItem("Black", QColor("black"))
        combo_box_color.addItem("Red", QColor("red"))
        combo_box_color.addItem("Blue", QColor("blue"))
        combo_box_color.setCurrentIndex(0)
        layout_color = QHBoxLayout()
        layout_color.addWidget(label_color)
        layout_color.addWidget(combo_box_color)

        label_size = QLabel("Select size")
        self.slider_size = QSlider(Qt.Horizontal, self)
        self.slider_size.setSizePolicy(size_policy)
        self.slider_size.setFixedWidth(285)
        self.slider_size.setMinimum(100)
        self.slider_size.setMaximum(1000)
        self.slider_size.valueChanged.connect(self.update_slider_size_value)
        self.label_slider_size_value = QLabel()
        self.label_slider_size_value.setSizePolicy(size_policy)
        self.label_slider_size_value.setFixedWidth(15)
        self.label_slider_size_value.setText(str(self.slider_size.value()))
        layout_size = QHBoxLayout()
        layout_size.addWidget(label_size)
        layout_size.addWidget(self.slider_size)
        layout_size.addWidget(self.label_slider_size_value)

        label_horizontal_position = QLabel("Select horizontal position")
        self.slider_horizontal_position = QSlider(Qt.Horizontal, self)
        self.slider_horizontal_position.setSizePolicy(size_policy)
        self.slider_horizontal_position.setFixedWidth(285)
        self.slider_horizontal_position.setMinimum(0)
        self.slider_horizontal_position.setMaximum(1000)
        self.slider_horizontal_position.setSliderPosition(0)
        self.slider_horizontal_position.valueChanged.connect(self.update_slider_horizontal_position_value)
        self.label_slider_horizontal_position_value = QLabel()
        self.label_slider_horizontal_position_value.setSizePolicy(size_policy)
        self.label_slider_horizontal_position_value.setFixedWidth(15)
        self.label_slider_horizontal_position_value.setText(str(self.slider_horizontal_position.value()))
        layout_horizontal_position = QHBoxLayout()
        layout_horizontal_position.addWidget(label_horizontal_position)
        layout_horizontal_position.addWidget(self.slider_horizontal_position)
        layout_horizontal_position.addWidget(self.label_slider_horizontal_position_value)

        label_vertical_position = QLabel("Select vertical position")
        self.slider_vertical_position = QSlider(Qt.Horizontal, self)
        self.slider_vertical_position.setSizePolicy(size_policy)
        self.slider_vertical_position.setFixedWidth(285)
        self.slider_vertical_position.setMinimum(0)
        self.slider_vertical_position.setMaximum(1000)
        self.slider_vertical_position.setSliderPosition(0)
        self.slider_vertical_position.valueChanged.connect(self.update_slider_vertical_position_value)
        self.label_slider_vertical_position_value = QLabel()
        self.label_slider_vertical_position_value.setSizePolicy(size_policy)
        self.label_slider_vertical_position_value.setFixedWidth(15)
        self.label_slider_vertical_position_value.setText(str(self.slider_vertical_position.value()))
        layout_vertical_position = QHBoxLayout()
        layout_vertical_position.addWidget(label_vertical_position)
        layout_vertical_position.addWidget(self.slider_vertical_position)
        layout_vertical_position.addWidget(self.label_slider_vertical_position_value)

        button_start_exercice_fixation = QPushButton("Start")
        button_start_exercice_fixation.clicked.connect(lambda: self.start_exercice_fixation(
            QColor(combo_box_color.currentData()),
            self.slider_size.value(),
            self.slider_horizontal_position.value(),
            self.slider_vertical_position.value()
            ))

        self.button_start_recording = QPushButton("Start")
        self.button_start_recording.clicked.connect(self.start_recording)

        self.button_stop_recording = QPushButton("Stop")
        self.button_stop_recording.clicked.connect(self.stop_recording)

        layout_recording = QHBoxLayout()
        layout_recording.addWidget(self.button_start_recording)
        layout_recording.addWidget(self.button_stop_recording)
        
        layout_recording_im = QVBoxLayout()
        layout_recording_im.addLayout(layout_recording)
        layout_recording_im.addWidget(self.recording_label)

        group_box_recording = QGroupBox("Recording")
        group_box_recording.setLayout(layout_recording_im)

        self.layout = QVBoxLayout()
        self.layout.addLayout(layout_color)
        self.layout.addLayout(layout_size)
        self.layout.addLayout(layout_horizontal_position)
        self.layout.addLayout(layout_vertical_position)
        self.layout.addWidget(button_start_exercice_fixation)
        self.layout.addWidget(group_box_recording)

        self.setLayout(self.layout)

    def update_slider_size_value(self):
        self.label_slider_size_value.setText(str(self.slider_size.value()))

    def update_slider_vertical_position_value(self):
        self.label_slider_vertical_position_value.setText(str(self.slider_vertical_position.value()))

    def update_slider_horizontal_position_value(self):
        self.label_slider_horizontal_position_value.setText(str(self.slider_horizontal_position.value()))

    def start_exercice_fixation(self, color, size, horizontal_position, vertical_position):
        self.fixation.set_is_running(True)
        self.fixation.set_color(color)
        self.fixation.set_size(size)
        self.fixation.set_horizontal_position(horizontal_position)
        self.fixation.set_vertical_position(vertical_position)
        screen = QDesktopWidget().screenGeometry(1)
        self.fixation.setGeometry(screen)
        self.fixation.showMaximized()
        self.__is_button_start_fixation_on = True

    def start_recording(self):
        if self.__is_button_start_fixation_on:
            if self.__connected_patient.get_codePatient() != "None" or self.__selected_config.get_name_config() != "None":
                csv_recorder = CSV_recorder()
                csv_recorder.set_filename(csv_recorder.generate_filename(self.__connected_patient.get_codePatient(), "Fixation"))
                csv_recorder.set_header()

                self.fixation.set_csv_recorder(csv_recorder)

                self.recording_label.setPixmap(self.recording_pixmap.scaled(self.recording_label.width(), self.recording_label.height(), Qt.KeepAspectRatio))

                self.fixation.set_is_recording(True)
            else:
                dlg = CustomDialog(message="Connecte to a patient and a config")
                dlg.exec()
        else: 
            dlg = CustomDialog(message="Start fixation first")
            dlg.exec()

    def stop_recording(self):
        self.fixation.set_is_recording(False)
        self.recording_label.clear()

class UI_infinite(QWidget):
    def __init__(self, connected_patient, selected_config):
        super().__init__()
        self.__is_button_start_infinite_on = False
        self.__connected_patient = connected_patient
        self.__selected_config = selected_config
        self.infinite = Infinite()

        size_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # Create a QLabel to display the recording status
        self.recording_label = QLabel(self)
        self.recording_label.setGeometry(10, 10, 50, 50) 
        self.recording_pixmap = QPixmap('record_icon.png') 

        label_direction = QLabel("Select direction")
        self.combo_box_direction = QComboBox()
        self.combo_box_direction.setSizePolicy(size_policy)
        self.combo_box_direction.setFixedWidth(300)
        self.combo_box_direction.addItem("Vertical")
        self.combo_box_direction.addItem("Horizontal")
        self.combo_box_direction.setCurrentIndex(0)
        layout_direction = QHBoxLayout()
        layout_direction.addWidget(label_direction)
        layout_direction.addWidget(self.combo_box_direction)

        label_color = QLabel("Select color")
        combo_box_color = QComboBox()
        combo_box_color.setSizePolicy(size_policy)
        combo_box_color.setFixedWidth(300)
        combo_box_color.addItem("Black", QColor("black"))
        combo_box_color.addItem("Red", QColor("red"))
        combo_box_color.addItem("Blue", QColor("blue"))
        combo_box_color.setCurrentIndex(0)
        layout_color = QHBoxLayout()
        layout_color.addWidget(label_color)
        layout_color.addWidget(combo_box_color)

        label_size = QLabel("Select size")
        self.slider_size = QSlider(Qt.Horizontal, self)
        self.slider_size.setSizePolicy(size_policy)
        self.slider_size.setFixedWidth(285)
        self.slider_size.setMinimum(1)
        self.slider_size.setMaximum(100)
        self.slider_size.setSliderPosition(50)
        self.slider_size.valueChanged.connect(self.update_slider_size_value)
        self.label_slider_size_value = QLabel()
        self.label_slider_size_value.setSizePolicy(size_policy)
        self.label_slider_size_value.setFixedWidth(15)
        self.label_slider_size_value.setText(str(self.slider_size.value()))
        layout_size = QHBoxLayout()
        layout_size.addWidget(label_size)
        layout_size.addWidget(self.slider_size)
        layout_size.addWidget(self.label_slider_size_value)

        label_speed = QLabel("Select speed")
        self.slider_speed = QSlider(Qt.Horizontal, self)
        self.slider_speed.setSizePolicy(size_policy)
        self.slider_speed.setFixedWidth(285)
        self.slider_speed.setMinimum(10)
        self.slider_speed.setMaximum(200)
        self.slider_speed.valueChanged.connect(self.update_slider_speed_value)
        self.label_slider_speed_value = QLabel()
        self.label_slider_speed_value.setSizePolicy(size_policy)
        self.label_slider_speed_value.setFixedWidth(15)
        self.label_slider_speed_value.setText(str(self.slider_speed.value()))
        layout_speed = QHBoxLayout()
        layout_speed.addWidget(label_speed)
        layout_speed.addWidget(self.slider_speed)
        layout_speed.addWidget(self.label_slider_speed_value)

        label_width_infini_cm = QLabel("Select width infini object (cm)")
        self.slider_width_infini_cm = QSlider(Qt.Horizontal, self)
        self.slider_width_infini_cm.setSizePolicy(size_policy)
        self.slider_width_infini_cm.setFixedWidth(285)
        self.slider_width_infini_cm.setMinimum(5)
        self.slider_width_infini_cm.setMaximum(40)
        self.slider_width_infini_cm.setSliderPosition(10)
        self.slider_width_infini_cm.valueChanged.connect(self.update_slider_width_infini_cm_value)
        self.label_slider_width_infini_cm_value = QLabel()
        self.label_slider_width_infini_cm_value.setSizePolicy(size_policy)
        self.label_slider_width_infini_cm_value.setFixedWidth(15)
        self.label_slider_width_infini_cm_value.setText(str(self.slider_width_infini_cm.value()))
        layout_width_infini_cm = QHBoxLayout()
        layout_width_infini_cm.addWidget(label_width_infini_cm)
        layout_width_infini_cm.addWidget(self.slider_width_infini_cm)
        layout_width_infini_cm.addWidget(self.label_slider_width_infini_cm_value)

        label_height_infini_cm = QLabel("Select height infini object (cm)")
        self.slider_height_infini_cm = QSlider(Qt.Horizontal, self)
        self.slider_height_infini_cm.setSizePolicy(size_policy)
        self.slider_height_infini_cm.setFixedWidth(285)
        self.slider_height_infini_cm.setMinimum(5)
        self.slider_height_infini_cm.setMaximum(30)
        self.slider_height_infini_cm.setSliderPosition(20)
        self.slider_height_infini_cm.valueChanged.connect(self.update_slider_height_infini_cm_value)
        self.label_slider_height_infini_cm_value = QLabel()
        self.label_slider_height_infini_cm_value.setSizePolicy(size_policy)
        self.label_slider_height_infini_cm_value.setFixedWidth(15)
        self.label_slider_height_infini_cm_value.setText(str(self.slider_height_infini_cm.value()))
        layout_height_infini_cm = QHBoxLayout()
        layout_height_infini_cm.addWidget(label_height_infini_cm)
        layout_height_infini_cm.addWidget(self.slider_height_infini_cm)
        layout_height_infini_cm.addWidget(self.label_slider_height_infini_cm_value)

        button_start_exercice_infini = QPushButton("Start")
        button_start_exercice_infini.clicked.connect(lambda: self.start_exercice_infini(
            self.slider_speed.value(), 
            self.slider_size.value(), 
            QColor(combo_box_color.currentData()),
            (self.combo_box_direction.currentIndex() == 0),#index==0 -> is_vertical=True
            self.slider_width_infini_cm.value(),
            self.slider_height_infini_cm.value(),
            self.__selected_config,
                ))

        self.button_start_recording = QPushButton("Start")
        self.button_start_recording.clicked.connect(self.start_recording)

        self.button_stop_recording = QPushButton("Stop")
        self.button_stop_recording.clicked.connect(self.stop_recording)

        layout_recording = QHBoxLayout()
        layout_recording.addWidget(self.button_start_recording)
        layout_recording.addWidget(self.button_stop_recording)
        
        layout_recording_im = QVBoxLayout()
        layout_recording_im.addLayout(layout_recording)
        layout_recording_im.addWidget(self.recording_label)

        group_box_recording = QGroupBox("Recording")
        group_box_recording.setLayout(layout_recording_im)

        self.layout = QVBoxLayout()
        self.layout.addLayout(layout_direction)
        self.layout.addLayout(layout_color) 
        self.layout.addLayout(layout_size)
        self.layout.addLayout(layout_speed)
        self.layout.addLayout(layout_width_infini_cm)
        self.layout.addLayout(layout_height_infini_cm)
        self.layout.addWidget(button_start_exercice_infini)
        self.layout.addWidget(group_box_recording)

        self.setLayout(self.layout)

    def update_slider_size_value(self):
        self.label_slider_size_value.setText(str(self.slider_size.value()))

    def update_slider_speed_value(self):
        self.label_slider_speed_value.setText(str(self.slider_speed.value()))

    def update_slider_width_infini_cm_value(self):
        self.label_slider_width_infini_cm_value.setText(str(self.slider_width_infini_cm.value()))

    def update_slider_height_infini_cm_value(self):
        self.label_slider_height_infini_cm_value.setText(str(self.slider_height_infini_cm.value()))

    def start_exercice_infini(self, speed, size, color, is_vertical, 
        width_target_infini_object_cm, height_target_infini_object_cm, selected_config):
        self.infinite.set_is_running(True)
        self.infinite.set_speed(speed/1000) #the slider only return integer value
        self.infinite.set_size(size)
        self.infinite.set_color(color)
        self.infinite.set_is_object_vertical(is_vertical)
        self.infinite.set_width_target_infini_object_cm(width_target_infini_object_cm)
        self.infinite.set_height_target_infini_object_cm(height_target_infini_object_cm)
        self.infinite.set_selected_config(selected_config)

        self.infinite.update_size_object()
        self.infinite.update_x_scaling()
        self.infinite.update_y_scaling()

        screen = QDesktopWidget().screenGeometry(1)
        self.infinite.setGeometry(screen)
        self.infinite.showMaximized()
        self.__is_button_start_infinite_on = True

    def start_recording(self):
        if self.__is_button_start_infinite_on:
            if self.__connected_patient.get_codePatient() != "None" or self.__selected_config.get_name_config() != "None":
                if (self.combo_box_direction.currentIndex() == 0):#index==0 -> is_vertical=True
                    exercice_name = "InfiniteV"
                else:
                    exercice_name = "InfiniteH"

                csv_recorder = CSV_recorder()
                csv_recorder.set_filename(csv_recorder.generate_filename(self.__connected_patient.get_codePatient(), exercice_name))
                csv_recorder.set_header()

                self.infinite.set_csv_recorder(csv_recorder)

                self.recording_label.setPixmap(self.recording_pixmap.scaled(self.recording_label.width(), self.recording_label.height(), Qt.KeepAspectRatio))
                
                self.infinite.set_is_recording(True)
            else:
                dlg = CustomDialog(message="Connecte to a patient and a config")
                dlg.exec()    
        else: 
            dlg = CustomDialog(message="Start infini first")
            dlg.exec()

    def stop_recording(self):
        self.infinite.set_is_recording(False)
        self.recording_label.clear()

