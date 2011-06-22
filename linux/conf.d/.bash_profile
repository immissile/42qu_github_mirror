# /etc/skel/.bash_profile

# This file is sourced by bash for login shells.  The following line
# runs your .bashrc and is recommended by the bash info pages.
export PATH=$HOME/bin:$HOME/sbin:$PATH:/usr/sbin:/sbin
[[ -f ~/.bashrc ]] && . ~/.bashrc



HISTFILE=$HISTFILE/.bash_history
HISTFILESIZE=99999
HISTSIZE=99999

