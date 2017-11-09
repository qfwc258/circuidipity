---
title: "Getting started with Neovim"
date: "2017-06-20"
publishDate: "2017-06-20"
tags:
  - neovim
  - linux
slug: "neovim"
aliases:
  - /neovim.html
---

Text-wrangling is a big part of unlocking the power of Linux and programming ... and with great power comes the need for a great text editor!

## Let's go!

I have used **Vim** in the past but barely scratched the surface of its features motherlode. A friend who is a [passionate vim user](http://gilesorr.com/blog/tag/vim.html) recommended I try **Neovim**, which "*strives to be a superset of Vim except for some intentionally-removed misfeatures... [and] is built for users who want the good parts of Vim, and more*". Sounds good!

## 0. Install

Neovim packages are available in Debian ...

```bash
sudo apt install neovim
sudo apt install python-dev python-pip python3-dev python3-pip
```

## 1. Launch

Launch editor ...

```bash
nvim
```

On first launch the `~/.local/share/nvim/{shada,swap}` directories are auto-generated. Manually create a new `~/.config/nvim` directory ...

```bash
mkdir ~/.config/nvim
```

... and create a `~/.config/nvim/init.vim` config file (or link to an existing `~/.vimrc`). My general settings ...

```bash
set nocompatible            " Disable compatibility to old-time vi
set showmatch               " Show matching brackets.
set ignorecase              " Do case insensitive matching
set mouse=v                 " middle-click paste with mouse
set hlsearch                " highlight search results
set tabstop=4               " number of columns occupied by a tab character
set softtabstop=4           " see multiple spaces as tabstops so <BS> does the right thing
set expandtab               " converts tabs to white space
set shiftwidth=4            " width for autoindents
set autoindent              " indent a new line the same amount as the line just typed
set number                  " add line numbers
set wildmode=longest,list   " get bash-like tab completions
set cc=80                   " set an 80 column border for good coding style
```

Check out Neovim's built-in `:help` command and the [online documentation](https://neovim.io/doc/).

Source: [nvim/init.vim](https://github.com/vonbrownie/dotfiles/blob/master/.config/nvim/init.vim)

## 2. Spelling

Toggle spell checking with the command `:set invspell`. First time the command is invoked it prompts to download the `utf-8` spell files ...

```bash
spellfile#LoadFile(): No (writable) spell directory found.
Created /home/dwa/.local/share/nvim/site/spell
No spell file for "en" in utf-8
Download it?
(Y)es, [N]o:Y

Downloading en.utf-8.spl...
"~/.local/share/nvim/site/spell/en.utf-8.spl" [New] 1121L, 609337C written
Downloading en.utf-8.sug...
"~/.local/share/nvim/site/spell/en.utf-8.sug" [New] 2512L, 596961C written
```

My own added words are saved in `~/.config/nvim/spell/{en.utf-8.add,en.utf-8.add.spl}`. Add a hot-key for the spell checker in `init.vim` ...

```bash
" toggle spelling
nnoremap <leader>s :set invspell<CR>
```

## 3. Colors

Neovim includes a few color schemes and more are available for download. Create a `colors` directory to hold extra schemes ...

```bash
mkdir -p ~/.config/nvim/colors
```

I use the [tir_black](http://www.vim.org/scripts/script.php?script_id=2777) scheme. Download and save in the new directory. Set as default color scheme in `init.vim` ...

```bash
" color scheme
colorscheme tir_black
```

I ran into the problem where the color scheme worked in the (urxvt) terminal but not inside a **tmux** session. Turns out my tmux was not seeing the 256 color palette ...

```bash
tput colors
    8
```

**[ Fix! ]** Add this setting to `~/.tmux.conf` ...

```bash
set -g default-terminal "rxvt-unicode-256color"
```

It is important to **kill all existing tmux sessions** to see the changes take effect. It is not enough to simply start [a fresh session](http://stackoverflow.com/a/25940093).

Now the colors work OK!

```bash
echo $TERM
    rxvt-unicode-256color
tput colors
    256
```

## 4. Plugins

Extend the core features of the text editor using plugins. With a fresh install of Neovim, now is a good time to setup a **plugin manager**. I install [Vundle](https://github.com/VundleVim/Vundle.vim) ...

```bash
mkdir -p ~/.config/nvim/bundle
git clone https://github.com/VundleVim/Vundle.vim.git ~/.config/nvim/bundle/Vundle.vim
```

Configure neovim to use vundle by modifying `init.vim` ...

```bash
filetype off
" set the runtime path to include Vundle and initialize
set rtp+=~/.config/nvim/bundle/Vundle.vim
call vundle#begin('~/.config/nvim/bundle')

" let Vundle manage Vundle, required
Plugin 'VundleVim/Vundle.vim'

" All of your Plugins must be added before the following line
call vundle#end()
filetype plugin indent on  " allows auto-indenting depending on file type
```

Install plugins by adding `Plugin 'plugin/name'` between `vundle#begin()` and `vundle#end()`, then launch the installer ...

```bash
nvim +PluginInstall +qall
```

A few plugins I have found very useful from the start ...

### Syntastic

[Syntax checking plugin](https://github.com/vim-syntastic/syntastic) that makes use of external syntax checkers. I install **pylint** for checking Python syntax and **shellcheck** for Bash scripting ...

```bash
sudo apt install pylint pylint3 shellcheck
```

Add the plugin to `init.vim` ...

```bash
Plugin 'vim-syntastic/syntastic'
```

... plus the [FAQ](https://github.com/vim-syntastic/syntastic#settings) recommends some defaults ...

```bash
set statusline+=%#warningmsg#
set statusline+=%{SyntasticStatuslineFlag()}
set statusline+=%*

let g:syntastic_always_populate_loc_list = 1
let g:syntastic_auto_loc_list = 1
let g:syntastic_check_on_open = 1
let g:syntastic_check_on_wq = 0
```

... plus (optional) enable [pylint checking for python3](https://github.com/vim-syntastic/syntastic/issues/1767#issuecomment-217834857) (the default falls back on python2) ...

```bash
let g:syntastic_python_pylint_exe = 'python3 -m pylint3'
```

### Vim-gitgutter

Plugin that [displays a git diff](https://github.com/airblade/vim-gitgutter) column at the side of a document marking where lines have been added, modified, or removed.

Add the plugin to `init.vim` ...

```bash
Plugin 'airblade/vim-gitgutter'
```

### Vimwiki

[Personal wiki plugin](https://github.com/vimwiki/vimwiki) that I use as a simple notebook.

Add the plugin to `init.vim` ...

```bash
Plugin 'vimwiki/vimwiki'
```

Default file location is `~/vimwiki`. To set a different location (example: `~/doc/wiki/`) ...

```bash
let g:vimwiki_list = [{'path': '~/doc/wiki/', 'path_html': '~/doc/wiki/html/'}]
```

I created a [little script](https://github.com/vonbrownie/homebin/blob/master/dlg) that runs a `git commit` before launching the wiki.

## 5. Default

I set Neovim to be my default editor (for system tasks like `visudo`) ...

```bash
sudo update-alternatives --config editor
```

Happy hacking!
