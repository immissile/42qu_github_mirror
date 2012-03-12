# /etc/skel/.bash_profile

# This file is sourced by bash for login shells.  The following line
# runs your .bashrc and is recommended by the bash info pages.
[[ -f ~/.bashrc ]] && . ~/.bashrc

LOCAL=$HOME/.env
export PATH=$LOCAL/bin:$PATH
export C_INCLUDE_PATH=$C_INCLUDE_PATH:$LOCAL/include/:$LOCAL/include/python2.6/
export CPLUS_INCLUDE_PATH=$CPLUS_INCLUDE_PATH:$LOCAL/include/:$LOCAL/include/python2.6/
export LC_CTYPE=en_US.UTF-8
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$LOCAL/lib
export LD_RUN_PATH=$LD_RUN_PATH:$LOCAL/lib
export LIBRARY_PATH=$LOCAL/lib
export LDPATH=$LDPATH:$LOCAL/lib

HISTFILE=$HISTFILE/.bash_history
HISTFILESIZE=99999
HISTSIZE=99999

