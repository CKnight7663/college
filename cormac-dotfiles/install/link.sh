#!/bin/bash


DOTFILES=$HOME/.dotfiles
BACKUP_DIR=$HOME/dotfiles-backup


echo -e "\n"
echo '\\\\\\Creating symlinks\\\\\\'
echo "============================="


linkables=$( find -H "$DOTFILES" -maxdepth 3 -name '*symlink' )
for file in $linkables ; do
    target="$HOME/.$( basename "$file" '.symlink' )"      #Creates file to link to
    echo "$target"
	if [ -e "$target" ]; then
        echo "~${target#$HOME} already exists... moving to backup"
        mv $target $BACKUP_DIR
    fi
    ln -s "$file" "$target"
done

echo -e "\n"
echo '\\\\\\ Installing Config Files\\\\\\'
echo "===================================="


if ! [ -d "$DOTFILES/config" ]; then
	mkdir "$DOTFILES/config"
fi
config_files=$( find "$DOTFILES/config" -maxdepth 1) #2>/dev/null )
for config in $config_files; do
    target="$HOME/.config$( basename "$config" )"
    if [ -e "$target" ]; then
        echo "~${target#$HOME} already exists... moving to backup"
        mv $target $BACKUP_DIR
    fi
    ln -s "$config" "$target"
done



echo "Done creating symlinks!!"






