#!/bin/bash

#Backup all dotfiles in the .dotfiles folder


DOTFILES=$HOME/.dotfiles
BACKUP_DIR=$HOME/dotfiles-backup

set -e # Exit immediately if a command exits with a non-zero status


if [ -d "$BACKUP_DIR" ]; then
    echo "Deleting $BACKUP_DIR"
    rm -r "$BACKUP_DIR"
fi

if [ -d "$DOTFILES" ]; then
    echo "Creating backup directory at $BACKUP_DIR and moving files"
    mkdir -p "$BACKUP_DIR"
    mv  $DOTFILES/ $BACKUP_DIR/
else
    echo "No .dotfile folder found, creating one."
    mkdir $HOME/.dotfiles
    mkdir -p "$BACKUP_DIR"
fi
