from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtGui import QIcon, QFont, QColor, QPainter, QLinearGradient
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QListWidget,
    QListWidgetItem, QPushButton, QMessageBox, QFrame,
    QSizePolicy, QStyle, QWidget, QSpacerItem
)

from services.notification_service import mark_as_read, get_notifications


class NotificationItem(QWidget):
    """Widget personnalisé pour afficher les notifications avec style amélioré"""

    def __init__(self, notification, parent=None):
        super().__init__(parent)
        self.notification = notification
        self.init_ui()
        self.setup_styles()

    def init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(12)

        # Indicateur de statut (lu/non lu)
        self.status_indicator = QFrame()
        self.status_indicator.setFixedSize(8, 8)
        self.status_indicator.setStyleSheet("""
            QFrame {
                background-color: #FFA500;
                border-radius: 4px;
            }
        """ if not self.notification.get("lu", False) else "")
        layout.addWidget(self.status_indicator)

        # Contenu principal
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(4)

        # Message
        self.message_label = QLabel(self.notification["message"])
        self.message_label.setWordWrap(True)
        self.message_label.setStyleSheet("""
            QLabel {
                color: #333333;
                font-size: 12px;
                font-weight: 500;
            }
        """)
        content_layout.addWidget(self.message_label)

        # Date et actions
        footer_widget = QWidget()
        footer_layout = QHBoxLayout(footer_widget)
        footer_layout.setContentsMargins(0, 0, 0, 0)

        # Date
        date_text = self.notification["date_creation"][:16]
        self.date_label = QLabel(date_text)
        self.date_label.setStyleSheet("""
            QLabel {
                color: #888888;
                font-size: 10px;
                font-style: italic;
            }
        """)
        footer_layout.addWidget(self.date_label)
        footer_layout.addStretch()

        # Bouton Marquer comme lu
        if not self.notification.get("lu", False):
            self.read_button = QPushButton("Marquer comme lu")
            self.read_button.setCursor(Qt.PointingHandCursor)
            self.read_button.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: #4285F4;
                    border: none;
                    font-size: 10px;
                    font-weight: bold;
                    padding: 2px 6px;
                }
                QPushButton:hover {
                    color: #3367D6;
                    text-decoration: underline;
                }
            """)
            footer_layout.addWidget(self.read_button)

        content_layout.addWidget(footer_widget)
        layout.addWidget(content_widget, 1)

    def setup_styles(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #FFFFFF;
                border-radius: 8px;
            }
        """)

        if not self.notification.get("lu", False):
            self.setStyleSheet("""
                QWidget {
                    background-color: #F8F9FE;
                    border: 1px solid #E0E5FF;
                    border-radius: 8px;
                }
            """)


class NotificationsWidget(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Centre de Notifications")
        self.setMinimumSize(450, 600)
        self.setup_ui()
        self.setup_styles()

        # Configuration du timer de rafraîchissement
        self.refresh_timer = QTimer(self)
        self.refresh_timer.timeout.connect(self.load_notifications)
        self.refresh_timer.start(60000)  # 60 secondes

        self.load_notifications()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # En-tête avec gradient
        self.header = QFrame()
        self.header.setFixedHeight(80)
        header_layout = QVBoxLayout(self.header)
        header_layout.setContentsMargins(20, 20, 20, 20)

        title_layout = QHBoxLayout()
        self.title_label = QLabel("Centre de Notifications")
        self.title_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 18px;
                font-weight: bold;
            }
        """)
        title_layout.addWidget(self.title_label)

        self.notif_count = QLabel()
        self.notif_count.setStyleSheet("""
            QLabel {
                background-color: rgba(255, 255, 255, 0.2);
                color: white;
                font-size: 12px;
                font-weight: bold;
                padding: 2px 8px;
                border-radius: 10px;
            }
        """)
        title_layout.addWidget(self.notif_count)
        title_layout.addStretch()

        header_layout.addLayout(title_layout)
        main_layout.addWidget(self.header)

        # Contenu principal
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(15, 15, 15, 15)
        content_layout.setSpacing(15)

        self.status_label = QLabel("Chargement des notifications...")
        self.status_label.setStyleSheet("""
            QLabel {
                color: #666666;
                font-size: 12px;
            }
        """)
        content_layout.addWidget(self.status_label)

        self.list_widget = QListWidget()
        self.list_widget.setStyleSheet("""
            QListWidget {
                background-color: transparent;
                border: none;
                outline: none;
            }
        """)
        self.list_widget.setAlternatingRowColors(False)
        self.list_widget.setFrameShape(QListWidget.NoFrame)
        self.list_widget.setSelectionMode(QListWidget.NoSelection)
        self.list_widget.setVerticalScrollMode(QListWidget.ScrollPerPixel)
        self.list_widget.setSpacing(8)
        content_layout.addWidget(self.list_widget)

        main_layout.addWidget(content_widget, 1)

        # Pied de page
        footer = QFrame()
        footer.setFixedHeight(60)
        footer_layout = QHBoxLayout(footer)
        footer_layout.setContentsMargins(20, 0, 20, 0)

        self.mark_all_read_btn = QPushButton("Tout marquer comme lu")
        self.mark_all_read_btn.setCursor(Qt.PointingHandCursor)
        footer_layout.addWidget(self.mark_all_read_btn)

        footer_layout.addStretch()

        self.refresh_btn = QPushButton("Rafraîchir")
        self.refresh_btn.setCursor(Qt.PointingHandCursor)
        self.refresh_btn.setIcon(QIcon.fromTheme("view-refresh"))
        footer_layout.addWidget(self.refresh_btn)

        main_layout.addWidget(footer)

    def setup_styles(self):
        self.setStyleSheet("""
            QDialog {
                background-color: #F5F7FA;
                border-radius: 12px;
            }
            QPushButton {
                background-color: #4285F4;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #3367D6;
            }
            QPushButton:pressed {
                background-color: #2A56C6;
            }
        """)

    def paintEvent(self, event):
        """Pour le gradient de l'en-tête"""
        painter = QPainter(self)
        gradient = QLinearGradient(0, 0, 0, self.header.height())
        gradient.setColorAt(0, QColor("#4285F4"))
        gradient.setColorAt(1, QColor("#34A853"))
        painter.fillRect(self.header.rect(), gradient)
        super().paintEvent(event)

    def load_notifications(self):
        """Charger et afficher les notifications"""
        self.list_widget.clear()
        self.status_label.setText("Chargement des notifications...")

        # Remplacer le timer simulé par un appel direct
        self._finish_loading()

    def _finish_loading(self):
        result = get_notifications()
        if result["success"]:
            notifications = result["data"]

            if not notifications:
                self.status_label.setText("Aucune notification pour le moment.")
                self.notif_count.setText("0 nouveau")
                return

            unread_count = sum(1 for n in notifications if not n.get("lu", False))
            self.notif_count.setText(f"{unread_count} nouveau" + ("x" if unread_count > 1 else ""))
            self.status_label.setText(f"{len(notifications)} notification(s)")

            for notif in notifications:
                item = QListWidgetItem()
                item.setFlags(item.flags() & ~Qt.ItemIsSelectable)
                widget = NotificationItem(notif)
                item.setSizeHint(widget.sizeHint())

                self.list_widget.addItem(item)
                self.list_widget.setItemWidget(item, widget)

                if not notif.get("lu", False) and hasattr(widget, "read_button"):
                    # Correction du problème de lambda
                    widget.read_button.clicked.connect(
                        lambda checked, n=notif: self._handle_mark_as_read(n)
                    )

            # Connecter le bouton "Tout marquer comme lu" une seule fois
            if not hasattr(self, '_mark_all_connected'):
                self.mark_all_read_btn.clicked.connect(self.mark_all_as_read)
                self.refresh_btn.clicked.connect(self.load_notifications)
                self._mark_all_connected = True

        else:
            self.status_label.setText("Erreur de chargement")
            QMessageBox.critical(self, "Erreur", result["message"])

    def _handle_mark_as_read(self, notification):
        """Wrapper pour gérer le marquage comme lu"""
        self.mark_notification_as_read(notification)

    def mark_notification_as_read(self, notification):
        """Marquer une notification spécifique comme lue"""
        if notification.get("id"):
            print(f"Tentative de marquage de la notification {notification['id']}")  # Debug
            result = mark_as_read(notification["id"])
            print("Résultat:", result)  # Debug

            if result.get("success"):
                self.load_notifications()
            else:
                QMessageBox.warning(
                    self,
                    "Avertissement",
                    result.get("message", "Impossible de marquer cette notification comme lue")
                )
        else:
            QMessageBox.warning(
                self,
                "Avertissement",
                "Notification invalide: ID manquant"
            )

    def mark_all_as_read(self):
        """Marquer toutes les notifications comme lues"""
        confirm = QMessageBox.question(
            self,
            "Confirmation",
            "Êtes-vous sûr de vouloir marquer toutes les notifications comme lues ?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            print("Tentative de marquage global")  # Debug
            result = mark_as_read("all")
            print("Résultat global:", result)  # Debug

            if result.get("success"):
                self.load_notifications()
                QMessageBox.information(
                    self,
                    "Succès",
                    result.get("message", "Toutes les notifications ont été marquées comme lues")
                )
            else:
                QMessageBox.warning(
                    self,
                    "Avertissement",
                    result.get("message", "Impossible de marquer les notifications comme lues")
                )