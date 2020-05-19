#!/bin/zsh

#Backup all dotfiles in the .dotfiles folder


DOTFILES=$HOME/.dotfiles/
BACKUP_DIR=$HOME/dotfiles-backup

set -e # Exit immediately if a command exits with a non-zero status



for (( i = 1; i <= 101; i++  )) do
    if ! [[ -d "$BACKUP_DIR/backup_$i" ]]; then
        mkdir "$BACKUP_DIR/backup_$i"
        mv  $DOTFILES "$BACKUP_DIR/backup_$i"
        echo "!!!Backed up to Archive $i"
        break
    elif [[ i = 101 ]]; then
        echo "ARCHIVE FULL, PLEASE REMOVE OLD FILES!!!!"
        exit
    else
        echo "Archive $i full"
    fi
done



#if [ -d "$DOTFILES" ]; then
#    echo "Creating backup directory at $BACKUP_DIR and moving files"
#    mkdir -p "$BACKUP_DIR"
#    mv  $DOTFILES/ $BACKUP_DIR/
#else
#    echo "No .dotfile folder found, creating one."
#    mkdir $HOME/.dotfiles
#    mkdir -p "$BACKUP_DIR"
#fi
