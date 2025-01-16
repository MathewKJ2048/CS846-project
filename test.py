from langchain_ollama import OllamaLLM
import os
import sys

# llm = OllamaLLM(model="tinyllama")
# response = llm.invoke("The first man on the moon was ...")
# print(response)

TEST = True

if len(sys.argv)!=1:
	TEST=False

print(TEST)

corpus_folder = "./corpus"
file_names = []
for root, dirs, files in os.walk(corpus_folder):
	for f in files:
		if not f.endswith(".als"):
			continue
		file_names.append(os.path.join(root,f))

flist = [file_names[3]] if TEST else file_names

print(len(flist))



model_list_test = ["tinyllama","tinyllama","tinyllama"]
actual_list_model = ["llama3.2","tinyllama"]#,"mixtral","codellama","llama2"]
mlist = model_list_test if TEST else actual_list_model

data = {}

file_output = 0
def write_file(data):
	global file_output
	name = "./out/"+str(file_output)+".stream"
	with open(name,"w+") as file:
		file.write(str(data))
	file_output+=1

for i in range(len(flist)):
	f = flist[i]
	data[f] = {}
	for m in mlist:
		llm = OllamaLLM(model=m)
		with open(f) as inpf:
			contents = inpf.read()
		prompt = "This is sample Alloy code. How many signatures exist? Answer in a single sentence, use symbols for numbers, do not use "," to separate the numbers\n"+contents
		response = llm.invoke(prompt)
		data[f][m] = response
		print(str(i+1)+"/"+str(len(flist))+"\t|\t"+m)
	write_file(data)
	data = {}


	
	
