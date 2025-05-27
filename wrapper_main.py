import os
import sys
import subprocess
from PyQt5.QtWidgets import QApplication
from main import MainApp


def start_backend():
    """
    Démarre le serveur Django avec l'environnement virtuel correct.
    """
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        backend_path = os.path.abspath(
            os.path.join(base_dir, '..', 'GESTION_BUDGET_UFR_SET', 'gestion_budgetaire_backend'))
        manage_py = os.path.join(backend_path, 'manage.py')
        venv_python = os.path.abspath(
            os.path.join(base_dir, '..', 'GESTION_BUDGET_UFR_SET', 'env_pfc', 'Scripts', 'python.exe'))

        if not os.path.isfile(manage_py):
            raise FileNotFoundError(f"Le fichier manage.py est introuvable à : {manage_py}")
        if not os.path.isfile(venv_python):
            raise FileNotFoundError(f"Le Python de l'environnement virtuel est introuvable à : {venv_python}")

        subprocess.Popen([venv_python, manage_py, 'runserver'], cwd=backend_path)
        print("[OK] Serveur Django lancé.")
    except Exception as e:
        print(f"[ERREUR] Impossible de démarrer le serveur Django : {e}")


if __name__ == '__main__':
    start_backend()

    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())
