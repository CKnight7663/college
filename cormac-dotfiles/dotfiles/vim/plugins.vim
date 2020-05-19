set nocompatible           " Be improved, required
filetype off                " Required

" set runtime path to include Vundle and initialise
set rtp+=~/.dotfiles/vim/bundle/Vundle.vim
call vundle#begin('~/.dotfiles/vim/bundle/')


"""""""" Required Plugins
" let Vundle manage Vundle
Plugin 'VundleVim/Vundle.vim'
""""""""" User Plugins

Plugin 'ycm-core/YouCompleteMe' 
Plugin 'preservim/nerdtree'
Plugin 'ctrlpvim/ctrlp.vim'
Plugin 'tpope/vim-fugitive'
Plugin 'vim-syntastic/syntastic'
Plugin 'ajh17/VimCompletesMe'
Plugin 'neoclide/coc.nvim'

""""""""" End of Plugins
call vundle#end()
filetype plugin indent on

