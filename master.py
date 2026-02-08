
'''
Kali Linux web automation tools for Bug Bounty
the point of this tool is to automate the tasks that are generally done over and over again
and are always true for same websites
to catch the low hanging fruit

'''

import os, json, time
from rich import print
from collections import OrderedDict, defaultdict


'''dev notes
	url extraction for katana and other specific tools
	feroxbuster
		rather than doing automated have some flexibility
			like give it room for customizing the commands, using pyautogui or some other libraries

	⭐ have to combine results
	🟠 make it class based rather than function
	✅ go step by step
	✅ run again
	✅ try using different command add or remove, paste all in there do what has to be done
	✅ add extra hurestics like pattern found, parameters, admin panel interesting items


'''


class COLLECTOR:
	def __init__(self) -> None:
		#self.domain = domain
		self.prot_ = [] # 0 on - 1 off
		self.dict_ = {}
		self.dictKeys = []
		self.folderName = 'temp'
		self.group = defaultdict(list)
		self.vault = {
			'commands' : "../commands.json",
			'master' : "../master.txt"
		}
		self.keys__ = set() # all the urls

		self.banner = f'''[b cyan]
	     ██████╗ ██████╗ ██╗     ██╗     ███████╗ ██████╗████████╗ ██████╗ ██████╗ 
	    ██╔════╝██╔═══██╗██║     ██║     ██╔════╝██╔════╝╚══██╔══╝██╔═══██╗██╔══██╗
	    ██║     ██║   ██║██║     ██║     █████╗  ██║        ██║   ██║   ██║██████╔╝
	    ██║     ██║   ██║██║     ██║     ██╔══╝  ██║        ██║   ██║   ██║██╔══██╗
	    ╚██████╗╚██████╔╝███████╗███████╗███████╗╚██████╗   ██║   ╚██████╔╝██║  ██║
	     ╚═════╝ ╚═════╝ ╚══════╝╚══════╝╚══════╝ ╚═════╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝
	                                by [b blue blink2]c0pperfi3ld[/]                                               
		'''

		

	def readfile(self, filename:str) -> list:
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

	

	def protocolFix(self) -> None:
		print(f"Checking the domain name in the [b cyan blink]\'domain.txt\'[/] file =>",end="\n")
		array = self.readfile(self.vault['master'])
		
		self.prot_.append(array[0]) # with protocol

		try:
			if 'https://www.' in array[0]: noProtocol_ = array[0].split('https://www.')[1]
			else: noProtocol_ = array[0].split('http://')[1]
		except IndexError:
			pass

		self.prot_.append(noProtocol_) # no protocol
		
		self.dict_ = OrderedDict(self.readfile(self.vault['commands']))
		# in order
		for k,v in self.dict_.items():
			self.dictKeys.append(k)
			self.group[v[3]].append(v[1])

	"""
	
	@staticmethod
	def timer(self, func) :
		''' should return the wrapper function '''
		def wrapper(*args):
			now_ = time.time()
			func(*args)
			then_ = time.time()
			return f"[b cyan blink2]Took {then_-now_} seconds !"
		return wrapper
	"""

	
	def loop_(self, idx, item_) -> None:
		command_ = self.dict_[item_][0]
		filename_ = self.dict_[item_][1]

		# if URL present then replace
		print(f"{self.prot_}",end="\n")
		try: fixedCommand = command_.replace('URL',self.prot_[self.dict_[item_][2]])
		except Exception as ex_:
			fixedCommand = command_

		print(f"[b green]Running task => {idx}",end="\n")

		fullString = f'{fixedCommand} | tee {filename_}'
		print(f"[b magenta]{fullString}",end="\n")

		os.system(fullString) # execute the command

	def writeFile(self, data, filename:str) -> None:
		with open(filename, 'w+') as file__:
			for d in data:
				file__.write(d)
				file__.write('\n')


	def deleteEv(self) -> None:
		os.system('rm -rf ./temp/*')
		os.chdir("./temp")

	def duplicateFinder(self) -> None:
		dups__ = defaultdict(int) # just number the urls
		num__ = 0
		for k,v in self.group.items():
			if k != 0:
				num__ = k
				for vv in v:
					textFile = vv
					file__ = self.readfile(vv)
					for f__ in file__:
						self.keys__.add(f__)
						if f__ in dups__:
							dups__[f__]+=1
						else:
							dups__[f__] = 1

				self.keys__ = list(self.keys__)
				for kk_ in self.keys__:
					print(f"{kk_}",end="\n")

				newFileName = "".join("".join(v).split('.txt')) + '.txt'

				self.writeFile(self.keys__, newFileName)
				print(f"{dups__}",end="\n")
				print(f"{len(dups__)}",end="\n")

				self.keys__.clear()
				self.keys__ = set()
	
	def checkFolder(self, name:str) -> bool:
		_allFolders = os.listdir(os.getcwd())
		__flag = False
		for __a in _allFolders:
			if __a == self.folderName:
				print(f"[b red]Folder found ! Skipping folder creation ...",end="\n")
				__flag = True
				break
		if not __flag:
			os.system(f'mkdir {self.folderName}')
			print(f"Folder created named [b cyan]{self.folderName}[/]",end="\n")
		time.sleep(1)



	def main(self) -> None:
		print(f"{self.banner}",end="\n")
		self.deleteEv() # clear the folder
		self.protocolFix()
		print(f"{self.dictKeys}",end="\n")

		for idx,item_ in enumerate(self.dictKeys, start=1):
			print(f"Should start [b magenta]{item_}[/]",end="\n")
			print(f"[b green]Continue [Any Key / No (n/N)] / Skip (s) ==> ",end=" ")
			prompt_ = input()
			if prompt_.lower() == 's':
				continue # skip the item
			elif prompt_ not in ("N",'n'):

				# main code goes here
				self.loop_(idx,item_)

				
			else:
				print(f"Thanks for using 👍",end="\n")
				break

		self.duplicateFinder()

if __name__ == "__main__":
	c = COLLECTOR()
	c.checkFolder('temp')
	c.main()
	

