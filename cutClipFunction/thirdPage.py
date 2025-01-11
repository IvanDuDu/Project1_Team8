from PySide6.QtWidgets import (
    QApplication, QWidget, QPushButton, QMessageBox, QLabel, QGridLayout,QScrollArea, QVBoxLayout
)
from PySide6.QtGui import QPixmap, QPalette, QBrush
from PySide6.QtCore import Qt, QUrl
from PySide6.QtMultimedia import QMediaPlayer
from PySide6.QtMultimediaWidgets import QVideoWidget
import sys

class ThirdWindow(QWidget):
    def __init__(self, video_path, clipDetail,segmented_objects,segmented_actions):
        """
        ThirdWindow Constructor.
        :param video_path: Đường dẫn video cần hiển thị (mặc định là None)
        """
        super().__init__()
        self.video_path = video_path
        self.data_list = clipDetail
        self.segmented_objects = segmented_objects
        self.segmented_actions = segmented_actions
        self.initUI()

    def initUI(self):
        # Cài đặt hình nền
        background_image_path = 'D:\\CODIng\\CV\\Project1_Team8\\thirdPage.png'

        pixmap = QPixmap(background_image_path)
        if pixmap.isNull():
            QMessageBox.critical(self, "Error", f"Failed to load background image: {background_image_path}")
            sys.exit(1)

        self.setFixedSize(pixmap.width(), pixmap.height())
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(pixmap))
        self.setPalette(palette)

        self.setWindowTitle("Third Window")

        # Khu vực xem video
        self.video_widget = QVideoWidget(self)
        self.video_widget.setGeometry(310, 45, 721, 405)  # x, y, width, height
        self.video_widget.setStyleSheet("background-color: #000; border: 1px solid #999;")


        #Image showcase
        self.image_overlay = QLabel(self)
        # self.image_overlay.setGeometry(310, 45, 405, 405)
        self.image_overlay.setStyleSheet("background-color: transparent;")
        self.image_overlay.setAlignment(Qt.AlignCenter)
        self.image_overlay.hide()  # Initially hidden

        # Nút HOME
        self.finishButton = QPushButton("RETURN HOME", self)
        self.finishButton.setGeometry(740, 485, 270, 60)  # x, y, width, height
        self.finishButton.setStyleSheet("""
            QPushButton {
                font-family: Muli;  
                font-size: 30px;
                font-weight: bold;
                color: white;
                background-color:  #00a181;
                padding: 10px;
            }
            QPushButton {border-radius: 30px;}
            QPushButton:hover {
                background-color: #7ed957;
                color: #004651;
            }
        """)
        self.finishButton.clicked.connect(self.confirm)

        # Image selection
        self.image_preview = QLabel(self)  # Change from QWidget to QLabel
        self.image_preview.setGeometry(0, 230, 200, 200)  # Size and position
        self.image_preview.setStyleSheet("background-color: #eeeeee; border: 1px solid #ccc; border-radius: 10px;")
        # self.image_preview.setAlignment(Qt.AlignCenter)  # Center alignment for the image

        # Tạo lưới hiển thị bên trong widget con
        self.grid_layout = QGridLayout(self.image_preview)
        self.grid_layout.setContentsMargins(5, 5, 5, 5)  # Lề xung quanh
        self.grid_layout.setSpacing(5)  # Khoảng cách giữa các ô

        # Thêm các nút vào lưới
        # self.add_buttons_to_grid(self.data_list)
        self.extra_layout_container_below = QWidget(self)  # A new container widget
        self.extra_layout_container_below.setStyleSheet(
            "background-color: #00a181; border: none;")  # Set green background color and remove border
        self.extra_layout_container_below.setFixedSize(500, 100)  # Adjust width and height
        self.extra_layout_container_below.move(self.image_preview.x() + 15,
                                               self.image_preview.y() + self.image_preview.height() + 40)

        self.extra_grid_layout = QGridLayout(self.extra_layout_container_below)
        self.extra_grid_layout.setContentsMargins(5, 5, 5, 5)  # Set small margins
        self.extra_grid_layout.setSpacing(5)  # Spacing between buttons
        self.extra_grid_layout.setAlignment(Qt.AlignTop)  # Align buttons to the top

        self.add_buttons_to_grid()

        # Khởi tạo MediaPlayer
        self.media_player = QMediaPlayer(self)
        self.media_player.setVideoOutput(self.video_widget)

        # Nếu có đường dẫn video, hiển thị ngay
        if self.video_path:
            self.play_video(self.video_path)

    def confirm(self):
        self.close()

    def play_video(self, video_path):
        self.media_player.setSource(QUrl.fromLocalFile(video_path))
        self.media_player.play()
        self.video_widget.show()

    def set_video_path(self, video_path):
        self.video_path = video_path
        self.play_video(video_path)

    def add_buttons_to_grid(self):
        """
        Tao ra list cac output de track duoc
        """
        row = 0  # Track the current row in the grid layout
        self.object_buttons = {}  # Dictionary to store buttons for each class
        self.action_buttons = []
        self.faces_buttons = []

        # Phan tracking khuon mat
        faces_button = QPushButton("Faces", self)
        faces_button.setStyleSheet(self.button_style())
        faces_button.setFixedSize(200, 20)
        self.grid_layout.addWidget(faces_button, row, 0, 1, 2)
        row += 1

        for index, clip in enumerate(self.data_list):
            button_text = f"Faces: (Frames {clip['start_time']} - {clip['end_time']})"
            face_button = QPushButton(button_text, self.extra_layout_container_below)  # Add to green area
            face_button.setStyleSheet(self.object_style())
            face_button.setFixedSize(200, 30)  # Adjust button size for the green area
            face_button.setVisible(False)  # Initially hidden

            face_button.clicked.connect(lambda _, idx=index, clp=clip: self.handle_button_click(idx, clp))
            self.faces_buttons.append(face_button)

        faces_button.clicked.connect(self.toggle_faces_buttons)

        #phan cac object da track được
        for class_name, objects in self.segmented_objects.items():
            # Create a button for the class name
            class_button = QPushButton(class_name, self)
            class_button.setStyleSheet(self.button_style())
            class_button.setFixedSize(200, 20)
            self.grid_layout.addWidget(class_button, row, 0, 1, 2)
            row += 1

            self.object_buttons[class_name] = []  # Store buttons for each class
            for obj in objects:
                button_text = f"(Frames {obj['appear_frame']} - {obj['disappear_frame']})"
                object_button = QPushButton(button_text, self.extra_layout_container_below)  # Add to green area
                object_button.setStyleSheet(self.object_style())
                object_button.setFixedSize(200, 30)  # Adjust button size for green layout
                object_button.clicked.connect(lambda _, ob=obj: self.show_object_image(ob))
                object_button.setVisible(False)  # Initially hidden
                self.object_buttons[class_name].append(object_button)

            # Connect the class button to toggle the object buttons
            class_button.clicked.connect(
                lambda _, buttons=self.object_buttons[class_name]: self.toggle_object_buttons(buttons))

        #Phan tuong tac giua cac vat the
        main_action_button = QPushButton("Actions", self)
        main_action_button.setStyleSheet(self.button_style())
        main_action_button.setFixedSize(200, 20)
        self.grid_layout.addWidget(main_action_button, row, 0, 1, 2)  # Add the main "Actions" button
        row += 1

        # Create buttons for each action and store them
        for action_name, action_clips in self.segmented_actions.items():
            for clip in action_clips:
                button_text = f"{clip['object1']} with {clip['object2']} (Frames {clip['appear_time']} - {clip['disappear_time']})"
                action_button = QPushButton(button_text, self.extra_layout_container_below)  # Add to green area
                action_button.setStyleSheet(self.object_style())
                action_button.setFixedSize(200, 30)  # Adjust button size for the green area
                action_button.setVisible(False)  # Initially hidden

                # Correctly bind the `clip` variable to the lambda
                action_button.clicked.connect(lambda _, clp=clip: self.play_video(clp["video_path"]))
                self.action_buttons.append(action_button)

        # Connect "Actions" button to toggle visibility in the green layout
        main_action_button.clicked.connect(self.toggle_action_buttons)

    def toggle_faces_buttons(self):
        """
        Toggles the visibility of the 'Faces' buttons and displays them in the green layout.
        """
        # Clear the existing layout content
        for i in reversed(range(self.extra_grid_layout.count())):
            widget = self.extra_grid_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        # Add the buttons dynamically to the grid layout
        if not any(button.isVisible() for button in self.faces_buttons):  # If hidden, make visible
            for row, button in enumerate(self.faces_buttons):
                button.setVisible(True)
                self.extra_grid_layout.addWidget(button, row, 0)  # Add to green layout
        else:  # If visible, hide them
            for button in self.faces_buttons:
                button.setVisible(False)

    def toggle_action_buttons(self):
        """
        Toggles the visibility of the 'Actions' buttons and displays them in the green layout.
        """
        # Clear the existing layout content
        for i in reversed(range(self.extra_grid_layout.count())):
            widget = self.extra_grid_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        # Add the buttons dynamically to the grid layout
        if not any(button.isVisible() for button in self.action_buttons):  # If hidden, make visible
            for row, button in enumerate(self.action_buttons):
                button.setVisible(True)
                self.extra_grid_layout.addWidget(button, row, 0)  # Add to green layout
        else:  # If visible, hide them
            for button in self.action_buttons:
                button.setVisible(False)

    def toggle_object_buttons(self, buttons):
        """
        Toggles the visibility of object buttons and displays them in the green layout.
        :param buttons: List of buttons to toggle.
        """
        # Clear the existing layout content
        for i in reversed(range(self.extra_grid_layout.count())):
            widget = self.extra_grid_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        # Add the buttons dynamically to the grid layout
        if not any(button.isVisible() for button in buttons):  # If hidden, make visible
            for row, button in enumerate(buttons):
                button.setVisible(True)
                self.extra_grid_layout.addWidget(button, row, 0)  # Add to green layout
        else:  # If visible, hide them
            for button in buttons:
                button.setVisible(False)

    #hien thi phan tu trong Clip Detail
    def handle_button_click(self, index, clip):
        """
        Xử lý sự kiện khi nút được nhấn.
        Phát video từ thời điểm start_time đến end_time.
        :param index: Chỉ số của clip.
        :param clip: Thông tin chi tiết của clip (start_time, end_time, detected_objects).
        """
        start_time = (clip["start_time"])
        end_time = (clip["end_time"])

        # Đặt video bắt đầu tại start_time
        self.media_player.setPosition(start_time * 1000)  # Đơn vị của setPosition là milliseconds
        self.media_player.play()

        # Theo dõi thời điểm hiện tại và dừng khi đạt end_time
        def stop_at_end_time(position):
            if position >= end_time * 1000:  # end_time cũng chuyển sang milliseconds
                self.media_player.pause()
                self.media_player.positionChanged.disconnect()  # Ngắt kết nối sau khi dừng

        # Kết nối tín hiệu positionChanged để kiểm tra thời gian
        self.media_player.positionChanged.connect(stop_at_end_time)

        # Hiển thị thông báo xác nhận
        QMessageBox.information(self, "Playing Clip", f"Playing clip {index + 1} from {start_time}s to {end_time}s.")

    #Hien thi anh
    def show_object_image(self, obj):
        """Display the image of the selected object in the video preview area."""
        image_path = obj["image_path"]  # Path to the image
        pixmap = QPixmap(image_path)  # Load the image into a QPixmap
        if pixmap.isNull():
            QMessageBox.warning(self, "Error", f"Failed to load image: {image_path}")
        else:
            self.video_widget.hide()
            self.image_overlay.show()  # Show the overlay
            self.media_player.pause()  # Pause the video
            preview_width = self.video_widget.width()
            preview_height = self.video_widget.height()

            # Scale the pixmap while maintaining aspect ratio
            scaled_pixmap = pixmap.scaled(preview_width, preview_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)

            # Center the image overlay within the video widget area
            image_width = scaled_pixmap.width()
            image_height = scaled_pixmap.height()
            x_offset = (preview_width - image_width) // 2
            y_offset = (preview_height - image_height) // 2

            # Adjust the geometry of the image overlay
            self.image_overlay.setGeometry(
                self.video_widget.x() + x_offset,
                self.video_widget.y() + y_offset,
                image_width,
                image_height
            )
            self.image_overlay.setPixmap(scaled_pixmap)

    def button_style(self):
        return """
            QPushButton {
                font-family: Muli;  
                font-size: 14px; 
                font-weight: bold;
                color: white;
                background-color: #007acc;
                padding: 2px; 
                min-width: 100px;  
                max-width: 120px;  
                min-height: 20px; 
                max-height: 30px;  
            }
            QPushButton {border-radius: 4px;}
            QPushButton:hover {
                background-color: #5dade2;
                color: #ffffff;
            }
        """

    def object_style(self):
        return """
            QPushButton {
                font-family: Muli;  
                font-size: 8px;  
                font-weight: bold;
                color: white;
                background-color: #2ef2a4;
                padding: 3px;  
                min-width: 100px;  
                max-width: 200px;  
                min-height: 20px;  
                max-height: 30px;  
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #7ed957;
                color: #004651;
            }
            QPushButton:pressed {
                background-color: #005f41;
            }
        """


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Dữ liệu mẫu cho clipsDetail
    clipsDetail = [
        {
            "start_time": "00:00:05",
            "end_time": "00:00:15",
            "detected_objects": ["Car", "Tree", "Dog"]
        },
        {
            "start_time": "00:01:00",
            "end_time": "00:01:30",
            "detected_objects": ["Person", "Bicycle"]
        },
        {
            "start_time": "00:02:00",
            "end_time": "00:02:30",
            "detected_objects": ["Cat", "Bus"]
        },
    ]

    segmented_objects = {
        "Car": [
            {"track_id": 1, "image_path": "D:\\CODIng\\CV\\YOLO Image Detection\\segmented objects\\billie on the chair\\person\\person-1_from_4_to_94.jpg","appear_frame": 20, "disappear_frame": 30},
            {"track_id": 2, "image_path": "car2.jpg", "appear_frame": 20, "disappear_frame": 30}
        ],
        "Person": [
            {"track_id": 3, "image_path": "D:\CODIng\CV\Project1_Team8\BillieEilish2.jpg", "appear_frame": 5, "disappear_frame": 15}
        ]
    }

    # Example segmented_actions
    segmented_actions = {
        "A person with a chair": [
            {
                "object1": "Person",
                "object2": "Chair",
                "appear_time": 4,  # Start time in seconds
                "disappear_time": 64,  # End time in seconds
                "video_path": "D:\\CODIng\\CV\\YOLO Image Detection\\segmented clips\\billie on the chair\\person and chair-('1', '3')_from_4_to_64.mp4",
                "description": "A person holding a cup"
            }
        ],
        "A person with a car": [
            {
                "object1": "Person",
                "object2": "Couch",
                "appear_time": 10,
                "disappear_time": 50,
                "video_path": "D:\\CODIng\\CV\\YOLO Image Detection\\billie on the chair.mp4",
                "description": "A car interacting with a person"
            }
        ]
    }

    video_path = "D:\\CODIng\\CV\\YOLO Image Detection\\billie on the chair.mp4" # Thay bằng đường dẫn thực tế
    window = ThirdWindow(video_path=video_path, clipDetail=clipsDetail,segmented_objects=segmented_objects, segmented_actions=segmented_actions)
    window.show()

    sys.exit(app.exec())