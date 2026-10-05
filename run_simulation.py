import sys
import os
import builtins
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QLineEdit, QHBoxLayout
from PyQt5.QtCore import QTimer, Qt
from snake import load_snake
from snake_app import SnakeWidget, SQUARE_SIZE

# Configuration, change your folder (here)
SAVED_SNAKE_FOLDER = "C:/Code/SnakeAI-master/saved_snakes2"
INDIVIDUAL_NAME = "best_snake_gen100"
SETTINGS_PATH = os.path.join(SAVED_SNAKE_FOLDER, 'settings.json')


class SnakeGameApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Play Best Snake")
        self.settings = self.load_settings()
        self.snake = self.load_snake()
 
        # Layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Score label
        self.score_label = QLabel("Score: 0")
        self.score_label.setAlignment(Qt.AlignCenter)
        self.score_label.setStyleSheet("font-size: 24px; color: black;")
        self.layout.addWidget(self.score_label)

        # Game over label
        self.game_over_label = QLabel("")
        self.game_over_label.setAlignment(Qt.AlignCenter)
        self.game_over_label.setStyleSheet("font-size: 24px; color: red;")
        self.layout.addWidget(self.game_over_label)

        # SnakeWidget (visual board)
        self.snake_widget = SnakeWidget(self, self.settings["board_size"], self.snake)
        self.snake_widget.draw_vision = False
        board_width = self.settings["board_size"][0] * SQUARE_SIZE[0]
        board_height = self.settings["board_size"][1] * SQUARE_SIZE[1]
        self.snake_widget.setFixedSize(board_width, board_height)
        self.layout.addWidget(self.snake_widget, alignment=Qt.AlignCenter)

        # Play Again button
        self.play_again_btn = QPushButton("Play Again")
        self.play_again_btn.clicked.connect(self.restart_game)
        self.layout.addWidget(self.play_again_btn, alignment=Qt.AlignCenter)

        # Game loop timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.game_loop)
        self.timer.start(100)

        # Set window size
        self.setFixedSize(board_width + 100, board_height + 150)

        # FPS controls
        fps_layout = QHBoxLayout()

        self.fps_input = QLineEdit()
        self.fps_input.setPlaceholderText("Enter FPS (e.g. 10)")
        self.fps_input.setFixedWidth(150)

        fps_button = QPushButton("Set FPS")
        fps_button.clicked.connect(self.set_fps)

        fps_layout.addWidget(self.fps_input)
        fps_layout.addWidget(fps_button)
        self.layout.addLayout(fps_layout)

    def load_settings(self):
        import json
        with open(SETTINGS_PATH, 'r') as f:
            return json.load(f)

    def load_snake(self):
        return load_snake(SAVED_SNAKE_FOLDER, INDIVIDUAL_NAME, self.settings)

    def restart_game(self):
        self.snake = self.load_snake()
        self.snake_widget.snake = self.snake
        self.score_label.setText("Score: 0")
        self.score_label.setStyleSheet("font-size: 24px; color: black;")

        # Reset the game over label
        self.game_over_label.setText("") # Clear game over message
        self.game_over_label.setStyleSheet("") # Reset any style applied

        self.snake_widget.repaint() # Redraw the widget to reflect changes
        self.timer.start(100)

    def game_loop(self):
        if self.snake.is_alive:
            self.snake.update()  # Make the snake "think"
            self.snake.move()    # Move based on its decision
            self.snake_widget.repaint()
            self.score_label.setText(f"Score: {self.snake.score}")
        else:
            self.score_label.setText(f"Game Over - Score: {self.snake.score}")
            self.score_label.setStyleSheet("font-size: 20px; color: red;")
            self.game_over_label.setText("The snake has died.")
            self.game_over_label.setStyleSheet("font-size: 16px; color: red;")
            self.timer.stop()

    def set_fps(self):
        try:
            fps = float(self.fps_input.text())
            if fps <= 0:
                raise ValueError
            interval = int(1000 / fps)
            self.timer.setInterval(interval)
            print(f"Updated FPS to {fps} ({interval} ms/frame)")
        except ValueError:
            print("Invalid FPS. Enter a number > 0.")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SnakeGameApp()
    window.show()
    sys.exit(app.exec_())
