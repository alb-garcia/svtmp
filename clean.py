#!/usr/bin/env python
# clean the place from emacs temp files
from nix_shell_utils import rm,cd

rm('*~')
with cd('docs'): rm('*~')
with cd('svtmp'): rm('*~')
with cd('test'): rm('*~')


    

    
