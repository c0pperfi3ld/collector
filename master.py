
'''
Kali Linux web automation tools for Bug Bounty
the point of this tool is to automate the tasks that are generally done over and over again
and are always true for same websites
to catch the low hanging fruit

'''

import os, json, time
from rich import print
from collections import OrderedDict

prot_ = [] # 0 on - 1 off
dict_ = {}
dictKeys = []

vault = {
	'commands' : "../commands.json",
	'master' : "../master.txt"
}

'''dev notes
	url extraction for katana and other specific tools
	feroxbuster
		rather than doing automated have some flexibility
			like give it room for customizing the commands, using pyautogui or some other libraries

	✅ go step by step
	✅ run again
	✅ try using different command add or remove, paste all in there do what has to be done
	✅ add extra hurestics like pattern found, parameters, admin panel interesting items


'''

banner__ = '''
     ██████╗ ██████╗ ██╗     ██╗     ███████╗ ██████╗████████╗ ██████╗ ██████╗ 
    ██╔════╝██╔═══██╗██║     ██║     ██╔════╝██╔════╝╚══██╔══╝██╔═══██╗██╔══██╗
    ██║     ██║   ██║██║     ██║     █████╗  ██║        ██║   ██║   ██║██████╔╝
    ██║     ██║   ██║██║     ██║     ██╔══╝  ██║        ██║   ██║   ██║██╔══██╗
    ╚██████╗╚██████╔╝███████╗███████╗███████╗╚██████╗   ██║   ╚██████╔╝██║  ██║
     ╚═════╝ ╚═════╝ ╚══════╝╚══════╝╚══════╝ ╚═════╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝
                                by c0pprfi3ld                                               
'''

def readfile(filename:str = vault['commands']) -> list:
	if filename.endswith('.txt'):
		with open(filename,"r+") as _file:
			lines_ = _file.readlines()
			newArray_ = []
			for l_ in lines_:
				if l_.endswith('\n'):
					newArray_.append(l_[:-1])
				else:
					newArray_.append(l_)
					''' Remove the last new line '''

		return newArray_
	else:
		with open(filename) as f:
			data = json.load(f)
		return data

def protocolFix() -> None:
	print(f"Checking the domain name in the [b cyan blink]\'domain.txt\'[/] file =>",end="\n")
	array = readfile(vault['master'])
	

	prot_.append(array[0]) # with protocol

	try:
		if 'https://www.' in array[0]: noProtocol_ = array[0].split('https://www.')[1]
		else: noProtocol_ = array[0].split('http://')[1]
	except IndexError:
		pass

	prot_.append(noProtocol_) # no protocol
	global dict_, dictKeys
	dict_ = OrderedDict(readfile())
	# in order
	for k in dict_.keys(): dictKeys.append(k) 

def timer(func) -> None:
	''' should return the wrapper function '''
	def wrapper(*args):
		now_ = time.time()
		func(*args)
		then_ = time.time()
		return f"[b cyan blink2]Took {then_-now_} seconds !"
	return wrapper

@timer
def loop_(idx, item_) -> None:
	command_ = dict_[item_][0]
	filename_ = dict_[item_][1]

	# if URL present then replace
	try: fixedCommand = command_.replace('URL',prot_[dict_[item_][2]])
	except: fixedCommand = command_

	print(f"[b green]Running task => {idx}",end="\n")

	fullString = f'{fixedCommand} | tee {filename_}'
	print(f"[b magenta]{fullString}",end="\n")

	os.system(fullString) # execute the command

	return True

def deleteEv() -> None:
	os.system('rm -rf ./temp/*')
	os.chdir("./temp")

def main() -> None:
	print(f"{banner__}",end="\n")
	deleteEv()
	protocolFix()
	print(f"{dictKeys}",end="\n")

	for idx,item_ in enumerate(dictKeys, start=1):
		print(f"[b green]Continue [Any Key / No (n/N)] ==> ",end="\n")
		prompt_ = input()
		if prompt_ not in ("N",'n'):
			x = loop_(idx,item_)
			print(f"{x}",end="\n")
		else:
			print(f"Thanks for using 👍",end="\n")
			break

if __name__ == "__main__":
	main()

