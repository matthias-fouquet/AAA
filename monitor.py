import os
import platform
import re
import socket
import subprocess
import time
from datetime import datetime
from pathlib import Path
from string import Template

import psutil


# timestamp = heure de boot formatée
timestamp = datetime.fromtimestamp(psutil.boot_time()).strftime("%A %d %B %Y, %H:%M:%S")


def get_serial_number():
    system = platform.system()
    try:
        if system == "Windows":
            serial = subprocess.getoutput("wmic bios get serialnumber").split("\n")[-1].strip()
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
    except Exception:
        return "Unknown"


def get_gpu_name():
    system = platform.system()
    try:
        if system == "Windows":
            lines = subprocess.getoutput("wmic path win32_VideoController get name").splitlines()
            gpu = next((l.strip() for l in lines if l.strip() and "Name" not in l), "")
        elif system == "Linux":
            gpu = subprocess.getoutput("lspci | grep -i 'vga'").strip()
        elif system == "Darwin":
            gpu = subprocess.getoutput("system_profiler SPDisplaysDataType | grep 'Chipset Model'").strip()
        else:
            gpu = "Unsupported system"
        return gpu if gpu else "Unknown GPU"
    except Exception:
        return "Unknown GPU"


def get_cpu_name():
    # platform.uname().processor est souvent vide sur Linux
    cpu = (platform.uname().processor or "").strip()
    if cpu:
        return cpu

    system = platform.system()
    try:
        if system == "Linux":
            out = subprocess.getoutput("cat /proc/cpuinfo | grep -m1 'model name' | cut -d: -f2").strip()
            return out if out else "Unknown CPU"
        elif system == "Darwin":
            out = subprocess.getoutput("sysctl -n machdep.cpu.brand_string").strip()
            return out if out else "Unknown CPU"
        elif system == "Windows":
            out = subprocess.getoutput("wmic cpu get name").splitlines()
            name = next((l.strip() for l in out if l.strip() and "Name" not in l), "")
            return name if name else "Unknown CPU"
    except Exception:
        pass

    return "Unknown CPU"


def machine_section():
    return {
        "hostname": platform.node(),
        "model": platform.uname().machine,
        "serial_number": get_serial_number(),
        "cpu_name": get_cpu_name(),
        "gpu_name": get_gpu_name(),
    }


def os_details():
    boot_time_dt = datetime.fromtimestamp(psutil.boot_time())
    uptime_seconds = time.time() - psutil.boot_time()

    return {
        "operating_system": platform.uname().system,
        "system_version": platform.release(),  # plus lisible que uname().version
        "boot_time": boot_time_dt.strftime("%Y-%m-%d %H:%M:%S"),
        "uptime": time.strftime("%H:%M:%S", time.gmtime(uptime_seconds)),
        "number_of_users": len(psutil.users()),
    }


def cpu_details():
    cpu_freq = psutil.cpu_freq()
    usage_per_core = psutil.cpu_percent(interval=1, percpu=True)

    usage_per_core_str = ", ".join(f"core {i}: {percent:.1f}%" for i, percent in enumerate(usage_per_core))

    return {
        "number_of_cores": psutil.cpu_count() or 0,
        "usage_per_core": usage_per_core_str,
        "cpu_maximal_frequency": round(cpu_freq.max, 0) if cpu_freq else 0,
    }


def cpu_usage():
    return {
        "cpu_usage_percentage": round(psutil.cpu_percent(interval=0.6), 1),
    }


def memory_details():
    vm = psutil.virtual_memory()
    swap = psutil.swap_memory()

    def gb(x):
        return round(x / (1024**3), 2)

    total_ram = gb(vm.total)
    available_ram = gb(vm.available)

    cpu_cores = psutil.cpu_count() or 1

    return {
        "total_ram": total_ram,
        "available_ram": available_ram,
        "memory_architecture": platform.architecture()[0],
        "ram_per_core": f"{round(total_ram / cpu_cores, 2)} GB / core",
        "swap_total": gb(swap.total),
    }


def memory_usage():
    vm = psutil.virtual_memory()

    def gb(x):
        return round(x / (1024**3), 2)

    total_ram = gb(vm.total)
    used_ram = gb(vm.used)

    ram_usage_percentage = round((used_ram / total_ram) * 100, 1) if total_ram > 0 else 0

    return {
        "ram_usage_percentage": ram_usage_percentage,
    }


def network_information():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        main_ip_address = s.getsockname()[0]
        s.close()
    except Exception:
        main_ip_address = "Unknown"

    interfaces = psutil.net_if_addrs()
    rows = []

    for name, addrs in interfaces.items():
        ipv4 = [a.address for a in addrs if getattr(a, "family", None) == socket.AF_INET]
        if ipv4:
            rows.append(f"<li>{name}: {', '.join(ipv4)}</li>")

    return {
        "main_ip_address": main_ip_address,
        "interfaces_rows": "\n".join(rows) if rows else "<li>No IPv4 interfaces found</li>",
    }


def file_statistics():
    analyze_directory = str(Path.home() / "Documents")
    extensions = [".txt", ".py", ".pdf", ".jpg"]

    counts = {ext: 0 for ext in extensions}
    total_files = 0

    for _, _, files in os.walk(analyze_directory):
        for f in files:
            total_files += 1
            ext = Path(f).suffix.lower()
            if ext in counts:
                counts[ext] += 1

    def pct(count: int) -> float:
        return (count / total_files * 100) if total_files else 0.0

    rows = []
    for ext in extensions:
        rows.append(
            "<tr>"
            f"<td>{ext}</td>"
            f"<td>{counts[ext]}</td>"
            f"<td>{pct(counts[ext]):.2f}</td>"
            "</tr>"
        )

    return {
        "analyze_directory": analyze_directory,
        "number_of_files": total_files,
        "files_table_rows": "\n".join(rows),
    }


def top_processes(limit=5):
    procs = []
    for p in psutil.process_iter(["pid", "name"]):
        try:
            procs.append(p)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    # Amorcer CPU par process
    for p in procs:
        try:
            p.cpu_percent(None)
        except Exception:
            pass

    time.sleep(0.6)

    cpu_list = []
    ram_list = []

    vm = psutil.virtual_memory()
    total_gb = vm.total / (1024**3)

    for p in procs:
        try:
            cpu = p.cpu_percent(None)
            mem_gb = p.memory_info().rss / (1024**3)
            name = p.info.get("name") or "?"
            cpu_list.append((cpu, p.pid, name))
            ram_list.append((mem_gb, p.pid, name))
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    cpu_list.sort(reverse=True, key=lambda x: x[0])
    ram_list.sort(reverse=True, key=lambda x: x[0])

    cpu_rows = []
    for cpu, pid, name in cpu_list[:limit]:
        cpu_rows.append(f"<tr><td>{pid}</td><td>{name}</td><td>{cpu:.1f}</td></tr>")

    ram_rows = []
    for mem_gb, pid, name in ram_list[:limit]:
        ram_rows.append(
            f"<tr><td>{pid}</td><td>{name}</td><td>{mem_gb:.2f} GB / {total_gb:.2f} GB</td></tr>"
        )

    return {
        "cpu_process_rows": "\n".join(cpu_rows) if cpu_rows else "<tr><td colspan='3'>No data</td></tr>",
        "ram_process_rows": "\n".join(ram_rows) if ram_rows else "<tr><td colspan='3'>No data</td></tr>",
    }


def build_context():
    context = {"timestamp": timestamp}
    context.update(machine_section())
    context.update(os_details())
    context.update(cpu_details())
    context.update(cpu_usage())
    context.update(memory_details())
    context.update(memory_usage())
    context.update(network_information())
    context.update(file_statistics())
    context.update(top_processes(limit=5))
    return context


def convert_double_braces_to_template_syntax(html: str) -> str:
    pattern = re.compile(r"\{\{\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*\}\}")
    return pattern.sub(r"${\1}", html)


def html_generator():
    base_dir = Path(__file__).resolve().parent
    template_path = base_dir / "template.html"
    output_path = base_dir / "index.html"

    raw_template = template_path.read_text(encoding="utf-8")
    converted_template = convert_double_braces_to_template_syntax(raw_template)

    template = Template(converted_template)
    html_output = template.safe_substitute(build_context())

    output_path.write_text(html_output, encoding="utf-8")


if __name__ == "__main__":
    html_generator()