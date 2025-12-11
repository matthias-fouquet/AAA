# collecte données CPU, RAM, ect.
import psutil 

# collecte version systeme, machine, ect.
import platform

# collecte adresse ip principale 
import socket

# permet l'analyse de reppertoires et d'extensions
import os 

# collecte de l'heure de demarrage, temps depuis logging, ect.
import time
from time import gmtime, strftime
from datetime import datetime

# commandes avancées, infos systeme
import subprocess

# permet anayse de fichiers (reccurcivité propre)
from pathlib import Path

# permet la manipulation d'html manuellement
from string import Template

# sert au pourcentage et calculs de statistiques pour les gauges
import math

timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_serial_number():
    system = platform.system()
    try:
        # Windows
        if system == "Windows":
            serial = subprocess.getoutput(
                'wmic bios get serialnumber'
            ).split("\n")[-1].strip()
        # Linux
        elif system == "Linux":
            serial = subprocess.getoutput(
                "cat /sys/class/dmi/id/product_serial"
            ).strip()
            # Si pas trouvé → méthode alternative
            if not serial:
                serial = subprocess.getoutput(
                    "sudo dmidecode -s system-serial-number"
                ).strip()
        # macOS
        elif system == "Darwin":
            serial = subprocess.getoutput(
                "system_profiler SPHardwareDataType | grep 'Serial Number' | awk '{print $4}'"
            ).strip()
        else:
            serial = "Unsupported OS"
        return serial if serial else "Unknown"
    except:
        return "Unknown"
    
def get_gpu_name():
    system = platform.system()
    try:
        # Windows (WMIC)
        if system == "Windows":
            gpu = subprocess.getoutput(
                "wmic path win32_VideoController get name"
            ).split("\n")[1].strip()
            return gpu if gpu else "Unknown GPU"
        # Linux
        elif system == "Linux":
            gpu = subprocess.getoutput("lspci | grep -i 'vga'").strip()
            return gpu if gpu else "Unknown GPU"
        # macOS
        elif system == "Darwin":
            gpu = subprocess.getoutput(
                "system_profiler SPDisplaysDataType | grep 'Chipset Model'"
            ).strip()
            return gpu if gpu else "Unknown GPU"
        else:
            return "Unsupported system"
    except:
        return "Unknown GPU"

def machine_section():
    hostname = platform.node() # nom de la machine 
    model = platform.uname().machine   # modele de la machine 
    serial_number = get_serial_number() # numero de serie 
    cpu_name = platform.uname().processor # nom du CPU
    gpu_name = get_gpu_name() # nom du processeur graphique 

def os_details():
    operating_system = platform.uname().system #systeme d'exploitation
    system_version = platform.uname().version # version du systeme d'éxploitation
    boot_time = datetime.fromtimestamp(psutil.boot_time()) # heure du demarrage de la machine
    uptime_seconds = time.time() - psutil.boot_time() # temps écoulé depuis le démarrage en seconde 
    uptime = time.strftime("%H:%M:%S", time.gmtime(uptime_seconds)) # temps écoulé depuis le démarrage 
    number_of_users = len(psutil.users()) 

def cpu_details(): 
    number_of_cores = psutil.cpu_count() # nombre de coeur 
    frequency_of_cores = psutil.cpu_percent(interval=1, percpu=True) # utilisation par coeur 
    cpu_maximal_frequency = psutil.cpu_freq().max # frequence max du CPU

def cpu_usage():
    cpu_usage_percentage = psutil.cpu_percent(interval=1)  # Moyenne sur 1 seconde du pourcentage d'utilisation du CPU
    cpu_actual_usage = psutil.cpu_freq().current #fréquence mx du CPU
    running_processes_cpu = psutil.Process().cpu_percent # utilisation du CPU par des processus en % 

def memory_usage():
    total_ram = psutil.virtual_memory().total/(1024 ** 3) # capacité total de la RAM
    used_ram = psutil.virtual_memory().available/(1024 ** 3) # RAM utilisé en Go
    running_processes_ram = psutil.Process().memory_info().rss / (1024 ** 2) #utilisation de la RAM par des processus en Go
    ram_usage_percentage = psutil.virtual_memory().percent/(1024 ** 3) # pourcentage utilisé de la RAM
    progress_bars =  

def network_information():
    for conn in psutil.net_connections(kind='inet'):
        main_ip_adress = conn.laddr #adresse IP local
    interface_details = psutil.net_if_addrs()

def file_statistics():
    analyze_directory = str(Path.home() / "Documents")
    # Les extensions à analyser
    extensions = [".txt", ".py", ".pdf", ".jpg"]
    files_per_extension =  {ext: 0 for ext in extensions}  # compteur initialisé à 0
    number_of_files = 0
     # Parcours du dossier et de tous les sous-dossiers
    for root, dirs, files in os.walk(analyze_directory):
        for file in files:
            number_of_files += 1
            ext = Path(file).suffix.lower()  # récupérer l'extension en minuscule
            if ext in files_per_extension:
                files_per_extension[ext] += 1
    files_percentage_compared = {
        ext: (count / number_of_files) * 100 if number_of_files > 0 else 0
        for ext, count in files_per_extension.items()
    }

def main():
    