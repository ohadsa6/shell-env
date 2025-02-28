 Features {{{1
                                                                              " These options and commands enable some very useful features in Vim, that    " no user should have to live without.
" These options and commands enable some very useful features in Vim, that    " no user should have to live without.
" no user should have to live without.
                                                                              " Set 'nocompatible' to ward off unexpected things that your distro might     " have made, as well as sanely reset options when re-sourcing .vimrc          set nocompatible
" Set 'nocompatible' to ward off unexpected things that your distro might     " have made, as well as sanely reset options when re-sourcing .vimrc          set nocompatible
" have made, as well as sanely reset options when re-sourcing .vimrc          set nocompatible
set nocompatible

 " Attempt to determine the type of a file based on its name and possibly its  " contents. Use this to allow intelligent auto-indenting for each filetype, 
 " contents. Use this to allow intelligent auto-indenting for each filetype, 
 " and for plugins that are filetype specific.
 filetype indent plugin on

 " Enable syntax highlighting 
 syntax on


 " Must have options {{{1

 " Highlight searches (use <C-L> to temporarily turn off highlighting; see the " mapping of <C-L> below)
 " mapping of <C-L> below)
 set hlsearch
 set incsearch



 " Usability options {{{1

 " When opening a new line and no filetype-specific indenting is enabled, keep " the same indent as the line you're currently on. Useful for READMEs, etc. 
 " the same indent as the line you're currently on. Useful for READMEs, etc. 
 set autoindent
 set backspace.indent,eol,start " more powerful backspacing

 " Display line numbers on the left
  set number

 " Display right ruler
 set colorcolumn=100
 highlight ColorColumn ctermbg=0 guibg=lightgrey


 " Spell check {{{1 
 set spelllang=en_us


 " key mappping
 rmap <C-p> :tabnext<CR>

  Specify a directory for plugins
 " - For Neovim: stdpath('data') . '/plugged'
 " - Avoid using standard Vim directory names like 'plugin' 
 "call plug#begin('-/.vim/plugged')

 "Plug 'Valloric/YouCompleteMe'

 " Initialize plugin system 
     plug#end()
