#!/bin/bash
$INSTALL_DIR=/var/gtfobins
mkdir $INSTALL_DIR
$tag = $(curl https://github.com/nathrema/gtfobins/releases/latest -i -I | grep -E 'location:' | cut -d' ' -f 1 | cut -d'/' -f 8)
curl https://github.com/nathrema/gtfobins/releases/download/$tag/gtfobins.py > $INSTALL_DIR/gtfobins
chmod +x $INSTALL_DIR/gtfobins
ln -s $INSTALL_DIR/gtfobins /usr/bin/gtfobins
