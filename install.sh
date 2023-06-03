#!/bin/bash

function setup() {
    printf "\n%s\n%s\n" "# HET" "export PATH=\$PATH:$PWD" >>"$1"
}

if [ -f "$HOME/.zshrc" ]; then
    setup "$HOME/.zshrc"
elif [ -f "$HOME/.bashrc" ]; then
    setup "$HOME/.bashrc"
else
    printf "%s\n" "Could not find any shell startup files : .bashrc .zshrc "
fi
