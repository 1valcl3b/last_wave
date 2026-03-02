import time
import subprocess
from pathlib import Path
import yaml



BASE_DIR = Path("provision")
LOG_FILE = BASE_DIR / "logs" / "ms.txt"
CONFIG_FILE = BASE_DIR / "config.yaml"
MININET_SCRIPT = BASE_DIR / "mininet_up.sh"


def read_topology():
    if not CONFIG_FILE.exists():
        raise RuntimeError("config.yaml não encontrado")

    with open(CONFIG_FILE, "r") as f:
        data = yaml.safe_load(f)

    for item in data:
        if "topology" in item:
            return item["topology"].get("type")

    raise RuntimeError("Topologia não definida no config.yaml")


def start_mininet(topology):
    print(f"[MONITOR] Subindo Mininet com topologia: {topology}")

    subprocess.call(
        ["bash", str(MININET_SCRIPT), topology]
    )


while True:

    if LOG_FILE.exists():
        status = LOG_FILE.read_text().strip()

        if status == "up":

            try:
                topology = read_topology()

                start_mininet(topology)

                LOG_FILE.write_text("on")
                print("[MONITOR] Mininet ON")

            except Exception as e:
                print("[MONITOR] Erro:", e)

    time.sleep(2)