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
        if system == "Windows":
            serial = subprocess.getoutput('wmic bios get serialnumber').split("\n")[-1].strip()
        elif system == "Linux":
            serial = subprocess.getoutput("cat /sys/class/dmi/id/product_serial").strip()
            if not serial:
                serial = subprocess.getoutput("sudo dmidecode -s system-serial-number").strip()
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
        if system == "Windows":
            gpu = subprocess.getoutput("wmic path win32_VideoController get name").split("\n")[1].strip()
        elif system == "Linux":
            gpu = subprocess.getoutput("lspci | grep -i 'vga'").strip()
        elif system == "Darwin":
            gpu = subprocess.getoutput("system_profiler SPDisplaysDataType | grep 'Chipset Model'").strip()
        else:
            return "Unsupported system"
        return gpu if gpu else "Unknown GPU"
    except:
        return "Unknown GPU"

def machine_section():
    hostname = platform.node()
    model = platform.uname().machine
    serial_number = get_serial_number()
    cpu_name = platform.uname().processor
    gpu_name = get_gpu_name()
    return hostname, model, serial_number, cpu_name, gpu_name

def os_details():
    operating_system = platform.uname().system
    system_version = platform.uname().version
    boot_time = datetime.fromtimestamp(psutil.boot_time())
    uptime_seconds = time.time() - psutil.boot_time()
    uptime = time.strftime("%H:%M:%S", time.gmtime(uptime_seconds))
    number_of_users = len(psutil.users())
    return operating_system, system_version, boot_time, uptime, number_of_users

def cpu_details():
    number_of_cores = psutil.cpu_count()
    usage_per_core = psutil.cpu_percent(interval=1, percpu=True)
    frequency_of_cores = "".join(f"core {i}: {percent:.1f}%" for i, percent in enumerate(usage_per_core))
    cpu_maximal_frequency = psutil.cpu_freq().max
    return number_of_cores, frequency_of_cores, cpu_maximal_frequency

def cpu_usage():
    cpu_usage_percentage = psutil.cpu_percent(interval=1)
    cpu_actual_usage = psutil.cpu_freq().current
    running_processes_cpu = psutil.Process().cpu_percent(interval=1)
    return cpu_usage_percentage, cpu_actual_usage, running_processes_cpu

def memory_usage():
    total_ram = psutil.virtual_memory().total/(1024 ** 3)
    used_ram = psutil.virtual_memory().used/(1024 ** 3)
    running_processes_ram = psutil.Process().memory_info().rss / (1024 ** 2)
    
    # FIX ✔️ plus de division par 1Go !
    ram_usage_percentage = psutil.virtual_memory().percent
    
    return total_ram, used_ram, running_processes_ram, ram_usage_percentage

def network_information():
    hostname = socket.gethostname()
    main_ip_address = socket.gethostbyname(hostname)
    interfaces = psutil.net_if_addrs()
    stats = psutil.net_if_stats()

    simple_interfaces = {}

    for name, addrs in interfaces.items():
        iface_info = {"IPv4": None, "MAC": None, "Status": "Down", "Speed_Mbps": 0}
        for addr in addrs:
            if addr.family == socket.AF_INET:
                iface_info["IPv4"] = addr.address
            elif addr.family == psutil.AF_LINK:
                iface_info["MAC"] = addr.address
        if name in stats:
            iface_info["Status"] = "Up" if stats[name].isup else "Down"
            iface_info["Speed_Mbps"] = stats[name].speed
        simple_interfaces[name] = iface_info

    return main_ip_address, simple_interfaces

def file_statistics():
    analyze_directory = str(Path.home() / "Documents")
    extensions = [".txt", ".py", ".pdf", ".jpg"]
    files_per_extension = {ext: 0 for ext in extensions}
    number_of_files = 0

    for root, dirs, files in os.walk(analyze_directory):
        for file in files:
            number_of_files += 1
            ext = Path(file).suffix.lower()
            if ext in files_per_extension:
                files_per_extension[ext] += 1

    files_percentage_compared = {
        ext: (count / number_of_files) * 100 if number_of_files else 0
        for ext, count in files_per_extension.items()
    }
    return analyze_directory, files_per_extension, number_of_files, files_percentage_compared

from jinja2 import Template

def main():

    html_raw = Path("template.html").read_text(encoding="utf-8")

    hostname, model, serial_number, cpu_name, gpu_name = machine_section()
    operating_system, system_version, boot_time, uptime, number_of_users = os_details()
    number_of_cores, frequency_of_cores, cpu_maximal_frequency = cpu_details()
    cpu_usage_percentage, cpu_actual_usage, running_processes_cpu = cpu_usage()
    total_ram, used_ram, running_processes_ram, ram_usage_percentage = memory_usage()
    main_ip_address, interface_details = network_information()
    analyze_directory, files_per_extension, number_of_files, files_percentage_compared = file_statistics()

    data = {
        "timestamp": timestamp,
        "hostname": hostname,
        "model": model,
        "serial_number": serial_number,
        "cpu_name": cpu_name,
        "gpu_name": gpu_name,

        "operating_system": operating_system,
        "system_version": system_version,
        "boot_time": boot_time,
        "uptime": uptime,
        "number_of_users": number_of_users,

        "number_of_cores": number_of_cores,
        "frequency_of_cores": frequency_of_cores,
        "cpu_maximal_frequency": cpu_maximal_frequency,

        "cpu_usage_percentage": cpu_usage_percentage,
        "cpu_actual_usage": cpu_actual_usage,
        "running_processes_cpu": running_processes_cpu,

        "total_ram": total_ram,
        "used_ram": used_ram,
        "running_processes_ram": running_processes_ram,
        "ram_usage_percentage": ram_usage_percentage,

        "main_ip_address": main_ip_address,
        "interface_details": interface_details,

        "analyze_directory": analyze_directory,
        "files_per_extension": files_per_extension,
        "number_of_files": number_of_files,
        "files_percentage_compared": files_percentage_compared,

        "progress_bars": ""
    }

    # --- rendu JINJA2 ---
    template = Template(html_raw)
    html = template.render(data)

    Path("index.html").write_text(html, encoding="utf-8")
    print("✔️ Rapport généré : index.html")


# --- IMPORTANT : on lance main() ---
if __name__ == "__main__":
    main()
