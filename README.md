# BearCart
BearCart an autonomous driving project. The goal is to upgrade an off-the-shelf
RC car into an AI powered self-driving platform. The software is running on a
Raspberry Pi 5 SBC in its native operating system: Raspberry Pi OS.
![portrait](/_DOCS/assemble/mechanical/images/bc_portrait.jpg)

This project is strongly inspired by the 
[DonkeyCar](https://github.com/autorope/donkeycar) project.


## Software Installation
Fire up the terminal on your Raspberry Pi, and run following commands in it.

### Install Dependencies 
```bash
sudo apt install python3-pip
pip install pip --upgrade --break-system-packages
```

### Clone The Repository
```bash
cd ~
git clone https://github.com/UCAEngineeringPhysics/BearCart.git
```

### Install Python Packages
```bash
cd ~/BearCart
pip install -r requirements.txt --break-system-packages
```

## Assembly Guides
- Components [layout](/_DOCS/assemble/mechanical/README.md)
- Wiring [diagrams](/_DOCS/assemble/electric/README.md) 

## Bill of Materials
Please use our [shopping list](/_DOCS/BOM.md) for a reference

## Demo video
- [BearCart stumbles](https://youtube.com/shorts/Kcm6qQqev3s)
