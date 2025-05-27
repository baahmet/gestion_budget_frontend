from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLabel, QLineEdit,
    QComboBox, QPushButton, QMessageBox
)
from PyQt5.QtCore import Qt
from services.utilisateur_service import register_utilisateur, update_utilisateur


class UtilisateurFormDialog(QDialog):
    """Boîte de dialogue pour la création ou modification d'utilisateurs."""

    def __init__(self, parent=None, utilisateur_data=None):
        super().__init__(parent)
        self.utilisateur_data = utilisateur_data
        self.setWindowTitle("Modifier un utilisateur" if utilisateur_data else "Créer un utilisateur")
        self.setMinimumWidth(400)
        self.setStyleSheet("""
            QDialog {
                background-color: #f5f7fa;
                font-family: 'Segoe UI';
            }
            QLabel {
                font-size: 14px;
                color: #2c3e50;
            }
            QLineEdit, QComboBox {
                padding: 8px;
                font-size: 13px;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                background-color: white;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 10px;
                font-size: 14px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignRight)

        # Champ Nom
        self.nom_input = QLineEdit()
        self.nom_input.setPlaceholderText("Nom complet")
        form_layout.addRow("👤 Nom :", self.nom_input)

        # Champ Email
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("exemple@domaine.com")
        form_layout.addRow("📧 Email :", self.email_input)

        # Champ Rôle
        self.role_combo = QComboBox()
        self.role_combo.addItem("Comptable", "comptable")
        self.role_combo.addItem("Directeur", "directeur")
        self.role_combo.addItem("CSA", "csa")
        form_layout.addRow("🛡 Rôle :", self.role_combo)

        # Mot de passe (uniquement en création)
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Mot de passe")
        if not self.utilisateur_data:
            form_layout.addRow("🔒 Mot de passe :", self.password_input)

        # Pré-remplissage en modification
        if self.utilisateur_data:
            self.nom_input.setText(self.utilisateur_data["nom"])
            self.email_input.setText(self.utilisateur_data["email"])
            self.role_combo.setCurrentText(self.utilisateur_data["role"].capitalize())

        # Bouton Soumettre
        self.submit_btn = QPushButton("💾 Modifier" if self.utilisateur_data else "➕ Créer")
        self.submit_btn.clicked.connect(self.submit)

        layout.addLayout(form_layout)
        layout.addWidget(self.submit_btn, alignment=Qt.AlignCenter)

    def submit(self):
        nom = self.nom_input.text().strip()
        email = self.email_input.text().strip()
        role = self.role_combo.currentData()
        password = self.password_input.text()

        if not nom or not email:
            QMessageBox.warning(self, "Champs requis", "Veuillez remplir tous les champs obligatoires.")
            return

        data = {
            "nom": nom,
            "email": email,
            "role": role
        }

        if not self.utilisateur_data and password:
            data["mot_de_passe"] = password

        if self.utilisateur_data:
            result = update_utilisateur(self.utilisateur_data["id"], data)
        else:
            result = register_utilisateur(data)

        if result["success"]:
            QMessageBox.information(self, "Succès", "Opération réalisée avec succès.")
            self.accept()
        else:
            QMessageBox.critical(self, "Erreur", result["message"])
