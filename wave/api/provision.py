from pathlib import Path
import subprocess
import time
import yaml

class Provision:
    def __init__(self, script_dir: Path):
        self.__script_dir = str(script_dir)

    # Auxiliary functions for provisioning the mininet environment
        
    def read_configyaml(self):
        config_path = Path(self.get_script_dir()) / "config.yaml"

        tipo_topologia = None
        client_ip= None
        server_ip=None

        try:
            with open(config_path, "r") as f:
                data = yaml.safe_load(f)
            
            for item in data:
                if "topology" in item:
                    tipo_topologia = item["topology"].get("type")
                if item.get("traffic") == "client":
                    client_ip= item.get("ip")
                if item.get("traffic") == "server":
                    server_ip = item.get("ip")

        except Exception as e:
            print(f"Erro: {e}")
        
        return {"topology_type": tipo_topologia, "client_ip": client_ip , "server_ip": server_ip}

        

    def start_mininet(self, topology_type):
        script = Path(self.get_script_dir()) / "mininet_up.sh"
        subprocess.Popen(["bash", str(script), topology_type])
        print("Função start_mininet acionada")

    def wait_mininet(self, timeout=60):
        switch_file = Path("/tmp/ultimo_switch.txt")
        start = time.time()

        while not switch_file.exists():
            if time.time() - start > timeout:
                raise RuntimeError("Mininet startup timeout")
            time.sleep(1)
        print("Função wait_mininet acionada")
    
    def stop_mininet(self):
        script = Path(self.get_script_dir()) / "mininet_down.sh"
        
        subprocess.Popen(["bash", str(script)])
        print("Função stop_mininet acionada")
    ## ///

    def get_script_dir(self):
        return self.__script_dir

    def set_script_dir(self, setPath):
        self.__script_dir = setPath

    def execute_command(self, command):
        try:
            result = subprocess.Popen(
                f"cd {self.get_script_dir()}; {command}",
                shell=True, stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            return
            # return result.stdout.decode()
        except subprocess.CalledProcessError as e:
            return
            # return e.stderr.decode()

    def up(self, platform):
        # Start the environment (Docker or Vagrant and Mininet)

        config = self.read_configyaml()
        
        topology_type = config["topology_type"]
        client_ip = config["client_ip"]
        server_ip = config["server_ip"]    

        if topology_type in ["tree", "linear"]:
            self.start_mininet(topology_type)
            self.wait_mininet()
        
        if platform == "docker":
            self.execute_command("docker compose up -d")
            time.sleep(10)
            script = Path(self.get_script_dir()) / "up-enviroment.sh"
            command = f"bash {script} {client_ip} {server_ip}"
            self.execute_command(command)
        else:
            self.execute_command("vagrant up")

    def down(self, platform):
        # Destroy the environment (Docker or Vagrant and Mininet)
        
        if platform == "docker":
            script = Path(self.get_script_dir()) / "down-enviroment.sh"
            self.execute_command(f"bash {script}")
            time.sleep(5)
            self.execute_command("docker compose down")

        else:
            self.execute_command("vagrant destroy -f")

        time.sleep(10)
        self.stop_mininet()

    def execute_scenario(self, *args):
        # Execute scenarios based on user input
        if args[1] == "docker":
            if args[0] == 'sin':
                command = f"""docker exec -it client ./run_wave.sh -l sinusoid {args[2]} {args[3]} {args[4]} {args[5]}"""
            elif args[0] == "step":
                command = f"""docker exec -it client ./run_wave.sh -l stair_step {args[2]} {args[3]} {args[4]}"""
            elif args[0] == "flashc":
                command = f"""docker exec -it client ./run_wave.sh -l flashcrowd {args[2]} {args[3]} {args[4]}"""
            else:
                return "Invalid scenario. Use: 'sin', 'step' or 'flashc'."
        else:
            if args[0] == 'sin':
                command = f"""vagrant ssh client -c './wave/run_wave.sh -l sinusoid {args[2]} {args[3]} {args[4]} {args[5]}'"""
            elif args[0] == "step":
                command = f"""vagrant ssh client -c './wave/run_wave.sh -l stair_step {args[2]} {args[3]} {args[4]}'"""
                print("Carga stair step executada")
            elif args[0] == "flashc":
                command = f"""vagrant ssh client -c './wave/run_wave.sh -l flashcrowd {args[2]} {args[3]} {args[4]}'"""
            else:
                return "Invalid scenario. Use: 'sin', 'step' or 'flashc'."
        return self.execute_command(command)
    
    def run_microburst(self, *args):
        if args[0] == "docker":
            command = f"""docker exec -it client 'sudo ./run_microburst.sh -l {args[1]} {args[2]}'"""
        else:
            command = f"""vagrant ssh client -c './wave/run_microburst.sh -l {args[1]} {args[2]}'"""

        return self.execute_command(command)