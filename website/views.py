from django.shortcuts import render, redirect
from django.contrib import messages
import requests
import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from .models import Code

# Create your views here.



def home(request):
	# api = 'sk-proj-ehKEqjLKj4dKkoL68GBkT3BlbkFJYM3CyPbtMPmImIIJlb1C'
	lang_list = ['abap', 'abnf', 'actionscript', 'ada', 'agda', 'al', 'antlr4', 'apacheconf', 'apex', 'apl', 'applescript', 'aql', 'arduino', 'arff', 'armasm', 'arturo', 'asciidoc', 'asm6502', 'asmatmel', 'aspnet', 'autohotkey', 'autoit', 'avisynth', 'avro-idl', 'awk', 'bash', 'basic', 'batch', 'bbcode', 'bbj', 'bicep', 'birb', 'bison', 'bnf', 'bqn', 'brainfuck', 'brightscript', 'bro', 'bsl', 'c', 'cfscript', 'chaiscript', 'cil', 'cilkc', 'cilkcpp', 'clike', 'clojure', 'cmake', 'cobol', 'coffeescript', 'concurnas', 'cooklang', 'coq', 'cpp', 'crystal', 'csharp', 'cshtml', 'csp', 'css', 'css-extras', 'csv', 'cue', 'cypher', 'd', 'dart', 'dataweave', 'dax', 'dhall', 'diff', 'django', 'dns-zone-file', 'docker', 'dot', 'ebnf', 'editorconfig', 'eiffel', 'ejs', 'elixir', 'elm', 'erb', 'erlang', 'etlua', 'excel-formula', 'factor', 'false', 'flow', 'fortran', 'fsharp', 'ftl', 'gap', 'gcode', 'gdscript', 'gedcom', 'gettext', 'gherkin', 'git', 'glsl', 'gml', 'gn', 'go', 'go-module', 'gradle', 'graphql', 'groovy', 'haml', 'handlebars', 'haskell', 'haxe', 'hcl', 'hlsl', 'hoon', 'hpkp', 'hsts', 'html', 'http', 'ichigojam', 'icon', 'icu-message-format', 'idris', 'iecst', 'ignore', 'inform7', 'ini', 'io', 'irestore-security-rules', 'j', 'java', 'javadoc', 'javadoclike', 'javascript', 'javastacktrace', 'jexl', 'jolie', 'jq', 'js-extras', 'js-templates', 'jsdoc', 'json', 'json5', 'jsonp', 'jsstacktrace', 'jsx', 'julia', 'keepalived', 'keyman', 'kotlin', 'kumir', 'kusto', 'latex', 'latte', 'less', 'lilypond', 'linker-script', 'liquid', 'lisp', 'livescript', 'llvm', 'log', 'lolcode', 'lua', 'magma', 'makefile', 'markdown', 'markup', 'markup-templating', 'mata', 'matlab', 'maxscript', 'mel', 'mermaid', 'metafont', 'mizar', 'mongodb', 'monkey', 'moonscript', 'n1ql', 'n4js', 'nand2tetris-hdl', 'naniscript', 'nasm', 'neon', 'nevod', 'nginx', 'nim', 'nix', 'nsis', 'objectivec', 'ocaml', 'odin', 'opencl', 'openqasm', 'oz', 'parigp', 'parser', 'pascal', 'pascaligo', 'pcaxis', 'peoplecode', 'perl', 'php', 'php-extras', 'phpdoc', 'plant-uml', 'plsql', 'powerquery', 'powershell', 'processing', 'prolog', 'promql', 'properties', 'protobuf', 'psl', 'pug', 'puppet', 'pure', 'purebasic', 'purescript', 'python', 'q', 'qml', 'qore', 'qsharp', 'r', 'racket', 'reason', 'regex', 'rego', 'renpy', 'rescript', 'rest', 'rip', 'roboconf', 'robotframework', 'ruby', 'rust', 'sas', 'sass', 'scala', 'scheme', 'scss', 'shell-session', 'smali', 'smalltalk', 'smarty', 'sml', 'solidity', 'solution-file', 'soy', 'sparql', 'splunk-spl', 'sqf', 'sql', 'squirrel', 'stan', 'stata', 'stylus', 'supercollider', 'swift', 'systemd', 't4-cs', 't4-templating', 't4-vb', 'tap', 'tcl', 'textile', 'toml', 'tremor', 'tsx', 'tt2', 'turtle', 'twig', 'typescript', 'typoscript', 'unrealscript', 'uorazor', 'uri', 'v', 'vala', 'vbnet', 'velocity', 'verilog', 'vhdl', 'vim', 'visual-basic', 'warpscript', 'wasm', 'web-idl', 'wgsl', 'wiki', 'wolfram', 'wren', 'xeora', 'xml-doc', 'xojo', 'xquery', 'yaml', 'yang', 'zig']
	url = "https://api.chatanywhere.tech/v1/chat/completions"
	if request.method == "POST":
		code = request.POST['code']
		lang = request.POST['lang']

		if lang == "Select Your Programming Language":
			messages.success(request, "Wuh Oh! You forgot to pick a language!")
			return render(request, 'home.html', {'lang_list':lang_list, 'code':code, 'lang':lang})
		else:
			# OPENAI!!
			apikey = "sk-NnUgiMNXLXuCaDnsEkaozlySJ46F2cxelUvrjvWzjzNCaQx4"
			try:
				payload = json.dumps({
				   "model": "gpt-3.5-turbo",
				   "messages": [
				      {
				         "role": "system",
				         "content": "You are a helpful assistant that fixes and generates code."
				      },
				      {
				         "role": "user",
				         "content": f"Hello. Respond ONLY with code. I need you to fix this {lang} code: {code}. Dont account for whitespace or special characters unless it is new lines and tabs. Dont use any '```' or specify the programming language. JUST THE CODE"
				      }
				   ]
				})
				headers = {
				   'Authorization': 'Bearer sk-NnUgiMNXLXuCaDnsEkaozlySJ46F2cxelUvrjvWzjzNCaQx4',
				   'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
				   'Content-Type': 'application/json'
				}
				response_asjson = requests.request("POST", url, headers=headers, data=payload)
				response_data = response_asjson.json()
				print(response_data)
				response = response_data['choices'][0]['message']['content'].strip()
				record = Code(question=code, code_answer=response, language=lang, user=request.user)
				record.save()
				return render(request, 'home.html', {'lang_list':lang_list, 'response':response, 'lang':lang})
			except Exception as e:
				return render(request, 'home.html', {'lang_list':lang_list, 'response':e, 'lang':lang})
	return render(request, 'home.html', {'lang_list':lang_list})





def suggest(request):
	lang_list = ['abap', 'abnf', 'actionscript', 'ada', 'agda', 'al', 'antlr4', 'apacheconf', 'apex', 'apl', 'applescript', 'aql', 'arduino', 'arff', 'armasm', 'arturo', 'asciidoc', 'asm6502', 'asmatmel', 'aspnet', 'autohotkey', 'autoit', 'avisynth', 'avro-idl', 'awk', 'bash', 'basic', 'batch', 'bbcode', 'bbj', 'bicep', 'birb', 'bison', 'bnf', 'bqn', 'brainfuck', 'brightscript', 'bro', 'bsl', 'c', 'cfscript', 'chaiscript', 'cil', 'cilkc', 'cilkcpp', 'clike', 'clojure', 'cmake', 'cobol', 'coffeescript', 'concurnas', 'cooklang', 'coq', 'cpp', 'crystal', 'csharp', 'cshtml', 'csp', 'css', 'css-extras', 'csv', 'cue', 'cypher', 'd', 'dart', 'dataweave', 'dax', 'dhall', 'diff', 'django', 'dns-zone-file', 'docker', 'dot', 'ebnf', 'editorconfig', 'eiffel', 'ejs', 'elixir', 'elm', 'erb', 'erlang', 'etlua', 'excel-formula', 'factor', 'false', 'flow', 'fortran', 'fsharp', 'ftl', 'gap', 'gcode', 'gdscript', 'gedcom', 'gettext', 'gherkin', 'git', 'glsl', 'gml', 'gn', 'go', 'go-module', 'gradle', 'graphql', 'groovy', 'haml', 'handlebars', 'haskell', 'haxe', 'hcl', 'hlsl', 'hoon', 'hpkp', 'hsts', 'html', 'http', 'ichigojam', 'icon', 'icu-message-format', 'idris', 'iecst', 'ignore', 'inform7', 'ini', 'io', 'irestore-security-rules', 'j', 'java', 'javadoc', 'javadoclike', 'javascript', 'javastacktrace', 'jexl', 'jolie', 'jq', 'js-extras', 'js-templates', 'jsdoc', 'json', 'json5', 'jsonp', 'jsstacktrace', 'jsx', 'julia', 'keepalived', 'keyman', 'kotlin', 'kumir', 'kusto', 'latex', 'latte', 'less', 'lilypond', 'linker-script', 'liquid', 'lisp', 'livescript', 'llvm', 'log', 'lolcode', 'lua', 'magma', 'makefile', 'markdown', 'markup', 'markup-templating', 'mata', 'matlab', 'maxscript', 'mel', 'mermaid', 'metafont', 'mizar', 'mongodb', 'monkey', 'moonscript', 'n1ql', 'n4js', 'nand2tetris-hdl', 'naniscript', 'nasm', 'neon', 'nevod', 'nginx', 'nim', 'nix', 'nsis', 'objectivec', 'ocaml', 'odin', 'opencl', 'openqasm', 'oz', 'parigp', 'parser', 'pascal', 'pascaligo', 'pcaxis', 'peoplecode', 'perl', 'php', 'php-extras', 'phpdoc', 'plant-uml', 'plsql', 'powerquery', 'powershell', 'processing', 'prolog', 'promql', 'properties', 'protobuf', 'psl', 'pug', 'puppet', 'pure', 'purebasic', 'purescript', 'python', 'q', 'qml', 'qore', 'qsharp', 'r', 'racket', 'reason', 'regex', 'rego', 'renpy', 'rescript', 'rest', 'rip', 'roboconf', 'robotframework', 'ruby', 'rust', 'sas', 'sass', 'scala', 'scheme', 'scss', 'shell-session', 'smali', 'smalltalk', 'smarty', 'sml', 'solidity', 'solution-file', 'soy', 'sparql', 'splunk-spl', 'sqf', 'sql', 'squirrel', 'stan', 'stata', 'stylus', 'supercollider', 'swift', 'systemd', 't4-cs', 't4-templating', 't4-vb', 'tap', 'tcl', 'textile', 'toml', 'tremor', 'tsx', 'tt2', 'turtle', 'twig', 'typescript', 'typoscript', 'unrealscript', 'uorazor', 'uri', 'v', 'vala', 'vbnet', 'velocity', 'verilog', 'vhdl', 'vim', 'visual-basic', 'warpscript', 'wasm', 'web-idl', 'wgsl', 'wiki', 'wolfram', 'wren', 'xeora', 'xml-doc', 'xojo', 'xquery', 'yaml', 'yang', 'zig']
	url = "https://api.chatanywhere.tech/v1/chat/completions"
	if request.method == "POST":
		code = request.POST['code']
		lang = request.POST['lang']

		if lang == "Select Your Programming Language":
			messages.success(request, "Wuh Oh! You forgot to pick a language!")
			return render(request, 'suggest.html', {'lang_list':lang_list, 'code':code, 'lang':lang})
		else:
			# OPENAI!!
			apikey = "sk-NnUgiMNXLXuCaDnsEkaozlySJ46F2cxelUvrjvWzjzNCaQx4"
			try:
				payload = json.dumps({
				   "model": "gpt-3.5-turbo",
				   "messages": [
				      {
				         "role": "system",
				         "content": "You are a helpful assistant that fixes and generates code."
				      },
				      {
				         "role": "user",
				         "content": f"Hello. Respond ONLY with code. Dont use any '```' or specify the programming language. JUST THE CODE. I need you to generate {lang} code following what I want. I want {lang} code that does as follows: {code}. Dont account for whitespace or special characters unless it is new lines and tabs. Dont use any '```' or specify the programming language. JUST THE CODE"
				      }
				   ]
				})
				headers = {
				   'Authorization': 'Bearer sk-NnUgiMNXLXuCaDnsEkaozlySJ46F2cxelUvrjvWzjzNCaQx4',
				   'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
				   'Content-Type': 'application/json'
				}
				response_asjson = requests.request("POST", url, headers=headers, data=payload)
				response_data = response_asjson.json()
				print(response_data)
				response = response_data['choices'][0]['message']['content'].strip()
				record = Code(question=code, code_answer=response, language=lang, user=request.user)
				record.save()
				return render(request, 'suggest.html', {'lang_list':lang_list, 'response':response, 'lang':lang})
			except Exception as e:
				return render(request, 'suggest.html', {'lang_list':lang_list, 'response':e, 'lang':lang})
	return render(request, 'suggest.html', {'lang_list':lang_list})




def login_user(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			messages.success(request, "Hooray! You have been logged in!")
			return redirect('home')
		else:
			messages.success(request, "Uh Oh. Error logging in. Please try again.")
			return redirect('home')
	else:
		return render(request, 'home.html', {})


def logout_user(request):
	logout(request)
	messages.success(request, "Bye Bye! You have been logged out!")
	return redirect('home')



def register_user(request):
	if request.method == "POST":
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			login(request, user)
			messages.success(request, "You have been registered and automaticlly logged in! Woohoo!")
			return redirect('home')
	else:
		form = SignUpForm()

	return render(request, 'register.html', {'form':form})



def past(request):
	if request.user.is_authenticated:
		code = Code.objects.filter(user_id=request.user.id)
		return render(request, 'past.html', {'code':code})
	else:
		messages.success(request, "You must be logged in to access the past code database :(")
		return redirect('home')



def delete_past(request, Past_id):
	past = Code.objects.get(pk=Past_id)
	past.delete()
	messages.success(request, "This snippet of code has officially been banished to the shadow realm!")
	return redirect('past')