import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from PyQt6.QtGui import QPainter, QPen, QBrush, QColor, QFont, QFontMetrics
from PyQt6.QtCore import Qt, QRectF, QSize, QTimer

class ConcentricCircleButton(QPushButton):
    def __init__(self, text="GO", parent=None):
        super().__init__(text, parent)

        self.ring_initial_opacity = 130

        # Factors relative to button diameter
        self.ring_initial_radius_factor = 0.41 # Start just outside the button face
        self.ring_max_radius_factor = 0.49     # Expand to just before the widget edge
        self.ring_expansion_range_factor = self.ring_max_radius_factor - self.ring_initial_radius_factor

        self.num_animated_rings = 3
        self.animated_rings_data = [] # Stores {'factor': float, 'opacity': float}

        self.setFixedSize(250, 250) # Default size
        self.setFont(QFont("Arial", 40, QFont.Weight.Bold))

        # Define colors
        self.buttonFaceColor = QColor("#2B2E3B")
        self.innerCircleColor = QColor("#348899")
        self.outerGlowHintColor = QColor(0, 255, 255, 40) # Very subtle static glow base
        self.animatedRingColor = QColor(0, 220, 220)    # Base color for animated rings
        self.textColor = QColor("white")

        self._hover = False
        self._pressed = False

        # --- Animation Attributes ---
        self.animation_timer = QTimer(self)
        self.animation_timer.timeout.connect(self._update_animation)
        # Timer interval (milliseconds), e.g., 50ms for ~20 FPS
        self.timer_interval = 50 
        # How much the radius_factor increases per timer tick
        self.ring_speed_factor_per_update = 0.004 

        self._initialize_animated_rings_state() # Set up initial state of rings

    def _initialize_animated_rings_state(self):
        """Initializes or resets the state of the animated rings."""
        self.animated_rings_data.clear()
        for i in range(self.num_animated_rings):
            # Stagger the initial position of each ring
            stagger_offset_factor = (i / self.num_animated_rings) * self.ring_expansion_range_factor
            current_factor = self.ring_initial_radius_factor + stagger_offset_factor
            
            # Calculate opacity based on how far it's already "expanded" due to stagger
            progress = max(0.0, min(stagger_offset_factor / self.ring_expansion_range_factor, 1.0))
            opacity = self.ring_initial_opacity * (1 - progress**1.5) # Fade if starting further out

            self.animated_rings_data.append({
                "current_radius_factor": current_factor,
                "opacity": opacity
            })

    def setFixedSize(self, width, height):
        super().setFixedSize(width, height)
        # If size changes, re-initialize ring states relative to new size perception
        # This is simplified; for dynamic resizing during animation, more robust handling might be needed
        self._initialize_animated_rings_state() 
        self.update()

    def showEvent(self, event):
        """Start animation when the widget is shown."""
        if not self.animation_timer.isActive():
            self._initialize_animated_rings_state() # Ensure rings are set up
            self.animation_timer.start(self.timer_interval)
        super().showEvent(event)

    def hideEvent(self, event):
        """Stop animation when the widget is hidden."""
        if self.animation_timer.isActive():
            self.animation_timer.stop()
        super().hideEvent(event)

    def _update_animation(self):
        """Updates the state of each animated ring."""
        if not self.isVisible(): # Defensive check
            return

        for ring in self.animated_rings_data:
            ring["current_radius_factor"] += self.ring_speed_factor_per_update

            # Calculate progress for opacity fade
            # progress = (current - initial) / range
            progress = (ring["current_radius_factor"] - self.ring_initial_radius_factor) / \
                       self.ring_expansion_range_factor
            progress = max(0.0, min(progress, 1.0)) # Clamp to [0,1]
            
            # Rings fade as they expand (e.g., opacity decreases with square of progress)
            ring["opacity"] = self.ring_initial_opacity * (1 - progress**1.5)

            # Reset ring if it expands beyond max radius or fades too much
            if ring["current_radius_factor"] >= self.ring_max_radius_factor or ring["opacity"] < 5:
                ring["current_radius_factor"] = self.ring_initial_radius_factor
                ring["opacity"] = self.ring_initial_opacity
        
        self.update() # Trigger a repaint

    def enterEvent(self, event):
        self._hover = True
        self.update()
        super().enterEvent(event)

    def updateColor(self, color: str, glowColor: str | None = None):
        if not glowColor:
            glowColor = color
        self.innerCircleColor = QColor(color)
        self.animatedRingColor = QColor(color)    # Base color for animated rings
        self.outerGlowHintColor = QColor(glowColor) # Very subtle static glow base
        print(self.animation_timer.isActive())
        self.animation_timer.stop()

    def leaveEvent(self, event):
        self._hover = False
        self.update()
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        self._pressed = True
        self.update()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self._pressed = False
        self.update()
        super().mouseReleaseEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = self.rect()
        width = rect.width()
        height = rect.height()
        center_x = width / 2
        center_y = height / 2
        diameter = min(width, height)

        if diameter <= 0: # Nothing to draw if no size
            return

        currentButtonFaceColor = QColor(self.buttonFaceColor)
        if self._pressed:
            currentButtonFaceColor = currentButtonFaceColor.darker(130)
        elif self._hover:
            currentButtonFaceColor = currentButtonFaceColor.lighter(110)
        
        # 1. Subtle static background glow (optional, can be removed if too busy)
        static_glow_radius = diameter * self.ring_max_radius_factor * 1.05 # Slightly larger than max animated
        painter.setPen(QPen(self.outerGlowHintColor, diameter * 0.04, Qt.PenStyle.SolidLine))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawEllipse(QRectF(center_x - static_glow_radius, center_y - static_glow_radius,
                                   2 * static_glow_radius, 2 * static_glow_radius))

        # 2. Draw the ANIMATED rings
        for ring_data in self.animated_rings_data:
            radius = ring_data["current_radius_factor"] * diameter
            opacity = ring_data["opacity"]

            if opacity > 0 and radius > 0:
                animated_color = QColor(self.animatedRingColor)
                animated_color.setAlpha(int(opacity))
                
                # Pen width for animated rings, e.g., making it thinner as it expands
                pen_width = diameter * 0.018 * (1 - (radius / (self.ring_max_radius_factor * diameter)) * 0.7)
                pen_width = max(1.0, pen_width) # ensure minimum pen width

                painter.setPen(QPen(animated_color, pen_width, Qt.PenStyle.SolidLine))
                painter.setBrush(Qt.BrushStyle.NoBrush)
                painter.drawEllipse(QRectF(center_x - radius, center_y - radius,
                                           2 * radius, 2 * radius))

        # 3. Draw the main darker cyan/blue inner solid ring (static)
        inner_ring_radius = diameter * (self.ring_initial_radius_factor - 0.02) # Just inside the animated rings start
        painter.setPen(QPen(self.innerCircleColor, diameter * 0.02, Qt.PenStyle.SolidLine))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawEllipse(QRectF(center_x - inner_ring_radius, center_y - inner_ring_radius,
                                   2 * inner_ring_radius, 2 * inner_ring_radius))

        # 4. Draw the button face
        button_face_radius = diameter * (self.ring_initial_radius_factor - 0.04) # Smaller than the inner ring
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(currentButtonFaceColor))
        painter.drawEllipse(QRectF(center_x - button_face_radius, center_y - button_face_radius,
                                   2 * button_face_radius, 2 * button_face_radius))

        # 5. Draw the text
        painter.setPen(QPen(self.textColor))
        painter.setFont(self.font())
        font_metrics = QFontMetrics(self.font())
        text_width = font_metrics.horizontalAdvance(self.text())
        
        text_x = center_x - text_width / 2
        text_y = center_y - (font_metrics.ascent() + font_metrics.descent()) / 2 + font_metrics.ascent()
        
        painter.drawText(int(text_x), int(text_y), self.text())


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Animated Round Button")
        self.setGeometry(100, 100, 400, 400)
        self.setStyleSheet("background-color: #1E1F26;")

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.go_button = ConcentricCircleButton("GO")
        # self.go_button.setFixedSize(300,300) # You can change size here

        layout.addWidget(self.go_button)
        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
