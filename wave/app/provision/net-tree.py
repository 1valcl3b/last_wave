#!/usr/bin/env python3
import yaml
from mininet.net import Mininet
from mininet.node import OVSSwitch
from mininet.link import TCLink, Intf
from mininet.cli import CLI
from mininet.clean import cleanup
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
CONFIG_FILE = BASE_DIR / "config.yaml"
SWITCH_FILE = Path("/tmp/last_switch.txt")

def montar_arvore(net, depth, branching, max_switches, delay=None, loss=None,bw=None ,links_cfg=None):
    link_map = {}
    if links_cfg:
        for l in links_cfg:
            key = (l['src'], l['dst'])
            link_map[key] = l
    contador = 0
    switches = []

    def adicionar(pai=None, nivel=0):
        nonlocal contador
        if contador >= max_switches:
            return

        nome = f"s{contador + 1}"

        sw = net.addSwitch(nome,cls=OVSSwitch,failMode='standalone')

        switches.append(sw)
        contador += 1

        if pai:
            link_parametros = {}

            src = pai.name
            dst = nome

            # Mode specific
            if links_cfg and (src, dst) in link_map:
                l = link_map[(src, dst)]

                if 'delay' in l:
                    link_parametros['delay'] = l['delay']

                if 'loss' in l:
                    link_parametros['loss'] = float(l['loss'])

                if 'bw' in l:
                    link_parametros['bw'] = float(l['bw'])

            else:
                # Mode global
                if delay:
                    link_parametros['delay'] = delay

                if loss:
                    link_parametros['loss'] = float(loss)
                
                if bw:
                    link_parametros['bw']= float(bw)

            net.addLink(pai, sw, **link_parametros)

        if nivel < depth - 1:
            for _ in range(branching):
                if contador < max_switches:
                    adicionar(sw, nivel + 1)

    adicionar()
    return switches

    # if switches:
    #     Intf('br0', node=switches[0])    
    #     Intf('br1', node=switches[-1])   

   


def main():
    cleanup()

    if not CONFIG_FILE.exists():
        raise Exception(f"Config file not found: {CONFIG_FILE}")

    with open(CONFIG_FILE) as f:
        cfg = yaml.safe_load(f)

    topologia = None
    for i in cfg:
        if 'topology' in i:
            topologia = i['topology']
            break

    if topologia is None:
        raise Exception("Topologia nao foi encontrada")

    depth = int(topologia['depth'])
    branching = int(topologia['branching'])
    max_switches = int(topologia['max_switches'])
    delay = topologia.get('delay')
    loss= topologia.get('loss')
    bw = topologia.get('bw')
    links_cfg = topologia.get('links')

    net = Mininet(controller=None,switch=OVSSwitch,link=TCLink,build=False)

    switches = montar_arvore(net,depth=depth,branching=branching,max_switches=max_switches,delay=delay,loss=loss,bw=bw,links_cfg=links_cfg)



    # switches = montar_arvore(net,depth=depth,branching=branching,max_switches=max_switches,delay=delay, loss=loss)
    



    net.build()
    net.start()    

    SWITCH_FILE.write_text(switches[-1].name + "\n")
    
    
    # Path("/tmp/ultimo_switch").write_text(switches[-1].name + "\n")
    
    # with open("/tmp/ultimo_switch.txt", "w") as f:
    #      f.write(switches[-1].name + "\n")
    
    #CLI(net)
    

    import time
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    net.stop()


if __name__ == "__main__":
    main()