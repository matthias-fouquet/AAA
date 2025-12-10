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
from datetime import datetime

# commandes avancées, infos systeme
import subprocess

# permet anayse de fichiers (reccurcivité propre)
from pathlib import Path

# permet la manipulation d'html manuellement
from string import Template

# sert au pourcentage et calculs de statistiques pour les gauges
import math

def sytem_section():
    machine_name = platform.node()
    operating_system =
    uptime =
    number_of_users =
    boot_time = 
    primary_ip_adress = 

def cpu_details(): 
    number_of_cores = 
    frequency_of_cores =
    usage_percentage = 

def memory_usage():
    total_ram =
    used_ram =
    ram_usage_percentage =
    progress_bars = 

def network_information():
    main_ip_adress =
    interface_details =

def process_monitoring():
    running_processes_cpu =
    running_processes_ram =
    ressource_consuming_3 =

def file_statistics():
    analyze_directory =
    number_of_files =
    files_per_extension = 
    files_percentage_compared = 

def main():
    