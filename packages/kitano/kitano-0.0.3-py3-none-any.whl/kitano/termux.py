'''
lib for working on the shellTermux
date: 17 oct 2022 seg 09:36 am
ReinanBr
'''

import os
import sys
import subprocess as subp



#get response from terminal
def shellRun(command,inLine=True):
	resShell = subp.check_output(command.split(' '))
#	sys.stdout.write(resShell) 
	resShell = ''.join(str(resShell).split("b'"))
	resShell = resShell[0:(len(resShell)-1)]
	resShell = ''.join(resShell.split("\n"))
	brokenLine = ' ' if inLine else '\n'
	resOutput = resShell.replace('\\n',brokenLine)
	return resOutput
