#!/bin/bash

# Installing the all configuration files, and important brew packages

# Defining a function that checks the type of
# a shell and discards std output and std error
command_exists() {
    type "$1" > /dev/null 2>&1
}
#echo -e "\n"
echo '\\\\\ Installing dotfiles \\\\\'
echo "==============================="
source install/backup.sh

HERE="$(pwd)"
NEW_DOTFILES=$HERE/dotfiles
DOTFILES=$HOME/.dotfiles
echo "Moving new dotfiles"
cp -r $NEW_DOTFILES $DOTFILES



source install/link.sh
echo "Finished link"

exit 1
source install/git.sh


# MacOS specific Install
if [ "$(uname)" == "Darwin" ]; then
    echo -e "\\n\\nRunning on macOS"

    if test ! "$( command -v brew )"; then
        echo "Installing homebrew"
        ruby -e "$( curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install  )"
    fi

    # install brew dependancies from Brewfile
    brew bundle

    # change the default shell to zsh
    zsh_path="$( command -v zsh )"
    if ! grep "$zsh_path" /etc/shells; then
        echo "adding $zsh_path to /etc/shells"
        echo "$zsh_path" | sudo tee -a /etc/shells
    fi

    if [[ "$SHELL" != "$zsh_path" ]]; then
        chsh -s "$zsh_path"
        echo "default shell changed to $zsh_path"
    fi

    source install/osx.sh

else

    if test ! "$( command -v brew )"; then
        echo "Please try installing homebrew, and rerunning script."
        echo "ruby -e curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install  "
        exit 1
    fi
    brew bundle
fi
echo "creating vim direactories"
mkdir -p ~/.vim-tmp


# Linux specific Install
if [ "$(uname)" == "Linux" ]; then
    echo "\\n\\nRunning on Linux..."
    echo "Installing build-essential"
    sudo apt-get update
    sudo apt-get install build-essential
    sudo apt-get install texinfo

    if test ! "$( command -v brew )"; then
        echo "Installing homebrew"
        /bin/bash -e "$( curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install  )"
        echo 'eval $(/home/linuxbrew/.linuxbrew/bin/brew shellenv)' >> /home/lily/.profile
        eval $(/home/linuxbrew/.linuxbrew/bin/brew shellenv)
        brew install gcc

    fi
    brew bundle

    if ! command_exists zsh; then
        echo "zsh not found. Installing now..."
        sudo apt-get install zsh

    fi
fi




if ! command_exists zsh; then
    echo "zsh not found. Installing now..."

elif ! [[ $SHELL =~ .*zsh.* ]]; then
    echo "configuring zsh as default shell"
    chsh os :$(command -v zsh)
fi

# Change the default shell to zsh

zsh_path="$( command -v zsh )"
if ! grep "$zsh_path" /etc/shells; then
    echo "adding $zsh_path to /etc/shells"
    echo "$zsh_path" | sudo tee -a /etc/shells
fi

if [[ "$SHELL" != "$zsh_path" ]]; then
    chsh -s "$zsh_path"
    echo "default shell changed to $zsh_path"
fi

echo "Done. Reload your terminal"



