#!/usr/bin/env python3
import yaml
import time
from pathlib import Path

from mininet.net import Mininet
from mininet.node import OVSSwitch
from mininet.link import TCLink
from mininet.clean import cleanup


BASE_DIR = Path(__file__).resolve().parent
CONFIG_FILE = BASE_DIR / "config.yaml"
SWITCH_FILE = Path("/tmp/last_switch.txt")


def montar_linear(net, num_switches, delay=None,loss=None, bw=None, links_cfg=None):
    link_map = {}
    if links_cfg:
        for l in links_cfg:
            if 'src' in l and 'dst' in l:
                link_map[(l['src'], l['dst'])] = l

    switches = []

    for i in range(num_switches):
        nome = f"s{i + 1}"

        sw = net.addSwitch(nome, cls=OVSSwitch, failMode='standalone')
        switches.append(sw)

        if i > 0:
            pai = switches[i - 1]
            link_parametros = {}

            src = pai.name
            dst = nome

        # modo specific
            if links_cfg and (src, dst) in link_map:
                l = link_map[(src, dst)]

                if 'delay' in l:
                    link_parametros['delay'] = l['delay']

                if 'loss' in l:
                    link_parametros['loss'] = float(l['loss'])
                
                if 'bw' in l:
                    link_parametros['bw'] = float(l['bw'])

            else:
                # modo global
                if delay:
                    link_parametros['delay'] = delay

                if loss:
                    link_parametros['loss'] = float(loss)

                if bw:
                    link_parametros['bw'] = float(bw)

            net.addLink(pai, sw, **link_parametros)


    return switches


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

    num_switches = int(topologia['num_switches'])
    delay = topologia.get('delay')
    loss= topologia.get('loss')
    bw = topologia.get('bw')
    links_cfg = topologia.get('links')

    net = Mininet(controller=None,switch=OVSSwitch,link=TCLink,build=False)

    switches = montar_linear(net,num_switches,delay=delay,loss=loss,bw=bw,links_cfg=links_cfg)

    net.build()
    net.start()
   
    SWITCH_FILE.write_text(switches[-1].name + "\n")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass

    net.stop()


main()
