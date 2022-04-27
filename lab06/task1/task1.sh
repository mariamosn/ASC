#!/bin/bash
wget -O tachyon_vtune_amp_xe.tgz http://ocw.cs.pub.ro/courses/_media/asc/lab6/tachyon_vtune_amp_xe.tgz 
gunzip tachyon_vtune_amp_xe.tgz
tar -xvf tachyon_vtune_amp_xe.tar
cd tachyon && make