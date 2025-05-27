from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLabel, QLineEdit,
    QComboBox, QPushButton, QMessageBox
)
from PyQt5.QtCore import Qt
from services.rapport_service import generer_rapport, update_rapport
from services.budget_service import get_budgets


class RapportFormDialog(QDialog):
    def __init__(self, parent=None, rapport=None):
        super().__init__(parent)
        self.rapport = rapport
        self.setWindowTitle("Modifier le Rapport" if self.rapport else "Générer un Rapport")
        self.setMinimumWidth(450)
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

        # Récupération des budgets
        budgets_result = get_budgets()
        if not budgets_result["success"]:
            QMessageBox.critical(self, "Erreur", budgets_result["message"])
            self.reject()
            return

        budgets = budgets_result["data"]
        self.budget_combo = QComboBox()
        self.budget_map = {b["exercice"]: b["id"] for b in budgets}
        self.budget_combo.addItems(self.budget_map.keys())
        form_layout.addRow("🔢 Budget :", self.budget_combo)

        self.periode_input = QLineEdit()
        self.periode_input.setPlaceholderText("Ex: Janvier - Mars 2024")
        form_layout.addRow("📅 Période :", self.periode_input)

        self.type_combo = QComboBox()
        self.type_combo.addItem("PDF", "pdf")
        self.type_combo.addItem("Excel", "excel")
        form_layout.addRow("🗂 Format :", self.type_combo)

        # Préremplir en cas de modification
        if self.rapport:
            budget_exercice = next((k for k, v in self.budget_map.items() if v == self.rapport["budget"]), None)
            if budget_exercice:
                self.budget_combo.setCurrentText(budget_exercice)
            self.periode_input.setText(self.rapport["periode"])
            self.type_combo.setCurrentText(self.rapport["type"].upper())
            self.type_combo.setDisabled(True)  # Désactiver la modification du format

        self.submit_btn = QPushButton("✅ Modifier" if self.rapport else "📊 Générer le rapport")
        self.submit_btn.clicked.connect(self.submit)

        layout.addLayout(form_layout)
        layout.addSpacing(10)
        layout.addWidget(self.submit_btn, alignment=Qt.AlignCenter)

    def submit(self):
        budget_id = self.budget_map[self.budget_combo.currentText()]
        periode = self.periode_input.text().strip()
        type_rapport = self.type_combo.currentData()

        if not periode:
            QMessageBox.warning(self, "Champs requis", "Veuillez indiquer la période.")
            return

        data = {
            "budget": budget_id,
            "periode": periode,
            "type": type_rapport
        }

        if self.rapport:
            result = update_rapport(self.rapport["id"], data)
        else:
            result = generer_rapport(data)

        if result["success"]:
            QMessageBox.information(self, "Succès", "Opération réalisée avec succès.")
            self.accept()
        else:
            QMessageBox.critical(self, "Erreur", result["message"])
