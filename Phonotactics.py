from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk
import random

characters = {}

rules = []
groups = {}

root = Tk()
root.title("Phonological Rule Processor")
root.geometry("600x600")

def saveChars():
    toSave = filedialog.asksaveasfile(filetypes=[("Character files", "*.chr")], defaultextension=[("Character files", "*.chr")])
    root.update()
    toSave.write(str(characters))
    toSave.close()

def saveRules():
    print(rules)
    toSave = filedialog.asksaveasfile(filetypes=[("Rule files", "*.rlz")], defaultextension=[("Character files", "*.chr")])
    root.update()
    toSave.write(str(rules)+'RULEGROUPSPLIT'+str(groups))
    toSave.close()

def loadChars():
    toLoad = filedialog.askopenfilename(filetypes=[("Character files", "*.chr")])
    root.update()
    file = open(toLoad, 'r')
    toReturn = eval(file.read())
    file.close()
    print(toReturn)
    for i in toReturn:
        characters[i] = toReturn[i]
    dispFeatures.delete("1.0", END)
    dispFeatures.insert("1.0", formatChars())

def loadRules():
    toLoad = filedialog.askopenfilename(filetypes=[("Rule files", "*.rlz")])
    root.update()
    file = open(toLoad, 'r')
    contents=file.read().split('RULEGROUPSPLIT')
    loadedRules = eval(contents[0])
    file.close()
    for i in loadedRules:
        rules.append(i)
    print(rules)
    loadedGroups = eval(contents[1])
    for i in loadedGroups:
        groups[i] = loadedGroups[i]
    dispFeatures.delete("1.0", END)
    dispFeatures.insert("1.0", formatChars())

def formatDict(toFormat):
    toReturn = ''
    for i in toFormat.keys():
        toReturn+= i + ': '+', '.join(toFormat[i])+'\n'
    return toReturn

def formatChars():
    return formatDict(characters)

def formatGroups():
    return formatDict(groups)

def addSound():
    newChar = charInput.get("1.0", "1.1")
    newAttrs = attrInput.get("1.0", END)
    print(newChar, newAttrs)
    if len(newChar) > 0:
        if newChar in characters.keys():
            choice = messagebox.askquestion("Yes/No", "This character already exists. \nAre you sure you want to replace it?", icon='warning')
            if 'y' in choice:
                characters[newChar[0]] = []
                for i in newAttrs.split("\n"):
                    if i.isalpha():
                        characters[newChar[0]].append(i)
                charInput.delete("1.0", END)
                attrInput.delete("1.0", END)
        else:
            characters[newChar[0]] = []
            for i in newAttrs.split("\n"):
                if i.isalpha():
                    characters[newChar[0]].append(i)
            charInput.delete("1.0", END)
            attrInput.delete("1.0", END)
    dispFeatures.delete("1.0", END)
    dispFeatures.insert("1.0", formatChars())

def loadSound():
    attrInput.delete("1.0", END)
    newChar = charInput.get("1.0", "1.1")
    attrInput.insert("1.0", "\n".join(characters[newChar]))

def removeSound():
    newChar = charInput.get("1.0", "1.1")
    choice = messagebox.askquestion("Yes/No", "Are you sure you want to remove "+newChar+"? \nThis action cannot be undone", icon='warning')
    if 'y' in choice.lower():
        try:
            v=characters.pop(newChar)
            messagebox.showinfo("Success", "Removed "+newChar+" from the list")
        except KeyError:
            messagebox.showerror("Error", "Unable to remove entry from list")
        dispFeatures.delete("1.0", END)
        dispFeatures.insert("1.0", formatChars())

def plusMinusRule(start, plus, minus):
    features = characters[start].copy()
    for i in plus.split("\n"):
        features.append(i)
    for i in minus.split("\n"):
        while i in features:
            features.remove(i)
    for i in ['', ' ', '\n']:
        while i in features:
            features.remove(i)
    print(features)
    for token in characters.keys():
        found = True
        for feat in characters[token]:
            if feat not in features:
                found = False
                break
        if found:
            for feat2 in features:
                if feat2 not in characters[token]:
                    found = False
        if found:
            return token

def plusMinusRuleButton():
    newChar = plusMinusRule(changeStart.get("1.0", "1.1"), changePlus.get("1.0", END), changeMinus.get("1.0", END))
    changeEnd.delete("1.0", END)
    changeEnd.insert("1.0", newChar)

def viewIPA():
    ipaChart = Tk()
    ipaChart.title("IPA Chart")
    ipaChart.geometry("350x200")
    cons = '''pb			td		ʈɖ	cɟ	kɡ	qɢ	 	ʔ 
m	ɱ		n		ɳ	ɲ	ŋ	ɴ		
ʙ			r					ʀ		
    	ⱱ		ɾ		ɽ					
ɸβ	fv	θð	sz	ʃʒ	ʂʐ	çʝ	xɣ	χʁ	ħʕ	hɦ
				ɬɮ							
	ʋ		ɹ		ɻ	j	ɰ			
			l		ɭ	ʎ	ʟ			'''
    consListBase = cons.split('\n')

    vowels = '''iy\tɨʉ\tɯu
ɪʏ\tʊ
eø\tɘɵ\tɤo
\tə
ɛœ\tɜɞ\tʌɔ
æ\tɐ
aɶ\t\tɑɒ'''

    vowelsListBase = vowels.split('\n')

    symbolsC = []
    row = 0
    for j in consListBase:
        consList = j.split('\t')
        for i in consList:
            symbolsC.append(Text(ipaChart))
            symbolsC[-1].insert("1.0", i)
            
            xcor = (consList.index(i))*(20)-350
            ycor = row*20+20
            
            symbolsC[-1].place(height=20, width=20, relx=1, x=xcor, y=ycor)
        row += 1

    symbolsV = []
    row = 0
    for j in vowelsListBase:
        vowelsList = j.split('\t')
        for i in vowelsList:
            symbolsV.append(Text(ipaChart))
            symbolsV[-1].insert("1.0", i)
            
            xcor = (vowelsList.index(i))*(25)-100
            ycor = row*20+20
            
            symbolsV[-1].place(height=20, width=20, relx=1, x=xcor, y=ycor)
        row += 1
    
    ipaChart.focus_force()

def textToFeatures(text):
    features = []
    for i in text:
        if i in characters.keys():
            features.append(characters[i])
        elif i.isalnum():
            waitVar = IntVar()
            textInput=Tk()
            textInput.title('New character found')
            textInput.geometry("150x300")
            heading = Label(textInput, text="New character found\nPlease list features for\n"+i)
            heading.place(relx=1, width=150, x=0, y=20, anchor=NE)

            newFeats = Text(textInput)
            newFeats.place(relx=1, width=125, height=200, x=-12.5, y=50, anchor=NE)

            def addFeatsFromPopup(i):
                characters[i] = []
                newAttrs = newFeats.get("1.0", END)
                for j in newAttrs.split("\n"):
                    if j.isalpha():
                        characters[i].append(j)
                features.append(characters[i])
                waitVar.set(1)
                
            addNewFeats = Button(textInput, text="Add features for\n"+i, command=lambda: addFeatsFromPopup(i))
            addNewFeats.place(relx=1, width=125, height=50, x=-12.5, y=260, anchor=NE)
            
            textInput.focus_force()
            root.wait_variable(waitVar)
            textInput.destroy()
            dispFeatures.delete("1.0", END)
            dispFeatures.insert("1.0", formatChars())
    return features

def featuresToText(features):
    textList = []
    for i in features:
        found = False
        for char in characters.keys():
            found = True
            for j in i:
                if j not in characters[char]:
                    found=False
                    break
            if found:
                for j in characters[char]:
                    if j not in i:
                        found = False
            if found:
                textList.append(char)
                break
        if not found:
            waitVar = IntVar()
            textInput=Tk()
            textInput.title('New feature set found')
            textInput.geometry("150x300")
            heading = Label(textInput, text="New feature set found\nPlease input the character for\n"+'\n'.join(i))
            heading.place(relx=1, width=150, height=160, x=0, y=20, anchor=NE)

            newFeats = Text(textInput)
            newFeats.place(relx=1, width=25, height=25, x=-100, y=180, anchor=NE)

            def addCharFromPopup(i):
                newAttrs = newFeats.get("1.0", END)
                newChar = newAttrs.split('\n')[0]
                characters[newChar] = i
                textList.append(newChar)
                waitVar.set(1)
                
            addNewFeats = Button(textInput, text="Add new character", command=lambda: addCharFromPopup(i))
            addNewFeats.place(relx=1, width=125, height=50, x=-12.5, y=260, anchor=NE)
            
            textInput.focus_force()
            root.wait_variable(waitVar)
            textInput.destroy()
            dispFeatures.delete("1.0", END)
            dispFeatures.insert("1.0", formatChars())

    return ''.join(textList)
            
def addRuleWindow():
    global ruleScreen
    ruleScreen = Tk()
    ruleScreen.title("Add rule")
    ruleScreen.geometry("600x150")
    
    ruleLbl = Label(ruleScreen, text="if")
    ruleLbl.pack(fill='both', side='left')

    changeStart = Text(ruleScreen, height=10, width=10)
    changeStart.pack(fill='x', side='left')#lace(height=100, width=75, relx = 1, x = -570, y=20, anchor=NW)

    beforeAfterVar = StringVar(ruleScreen)
    beforeAfter = OptionMenu(ruleScreen, beforeAfterVar, "precedes", "follows")
    beforeAfter.pack(fill='x', side='left')#lace(height=25, width=85, relx=1, x=-490, y=20)

    triggerAttr = Text(ruleScreen, height=10, width=10)
    triggerAttr.pack(fill='x', side='left')#lace(height=100, width=75, relx = 1, x = -400, y=20, anchor=NW)

    lblPlus = Label(ruleScreen, text=":")
    lblPlus.pack(fill='x', side='left')#lace(height=25, width=25, relx = 1, x = -325, y=20, anchor=NW)

    toAssimilate = Text(ruleScreen, height=10, width=10)
    propVar = StringVar(ruleScreen)
    propDistance = OptionMenu(ruleScreen, propVar, "to next consonant", "to next vowel", "to next sound", "to all consonants", "to all vowels", "to all sounds")

    def update(value):
        if value == "assimilate":
            toAssimilate.pack(fill='both', side='left')#lace(height=100, width=75, relx = 1, x = -215, y=20, anchor=NW)
            propDistance.pack_forget()
            propDistance.update()
            ruleScreen.update()

        elif value == "propagate":
            toAssimilate.pack(fill='both', side='left')#lace(height=100, width=75, relx = 1, x = -215, y=20, anchor=NW)
            propDistance.pack(fill='both', side='left')#lace(height=25, width=125, relx = 1, x = -140, y=20, anchor=NW)

    actionVar = StringVar(ruleScreen)
    actionChoice=OptionMenu(ruleScreen, actionVar, "assimilate", "propagate", "delete", "insert", command=update)
    actionChoice.pack(fill='both', side='left')#lace(height=25, width=85, relx=1, x=-305, y=20)
    ruleScreen.focus_force()

    def addRule():
        newRule = []
        
        val1 = []
        val3 = []
        
        for i in changeStart.get("1.0", END).split('\n'):
            if i != '':
                val1.append(i)
                
        val2 = beforeAfterVar.get()
        
        for i in triggerAttr.get("1.0", END).split("\n"):
            if i != '':
                val3.append(i)
                
        val4 = actionVar.get()
        
        if val4 == 'assimilate':
            val5 = []
            for i in toAssimilate.get("1.0", END).split('\n'):
                if i != '':
                    val5.append(i)
            newRule=[val1, val2, val3, val4, val5]
            
        elif val4 == 'propagate':
            val5 = []
            for i in toAssimilate.get("1.0", END).split('\n'):
                if i != '':
                    val5.append(i)
            val6 = propVar.get()
            newRule = [val1, val2, val3, val4, val5, val6]

        if val4 != '':
            rules.append(newRule)
            messagebox.showinfo("Success!", "Added new rule:\n"+str(rules[-1]))
            print(rules)
            viewRules()
        else:
            messagebox.showerror("Error", "Invalid rule. \nBlank combobox")
        
        
        
    ruleButton = Button(ruleScreen, text="Add Rule", command=addRule)
    ruleButton.pack(fill='both', side='right')#lace(height=50, width=50, relx=1, x=-305, y=50)

def addGroupWindow():
    groupScreen = Tk()
    groupScreen.title("Make new group")
    groupScreen.geometry("150x600")

    def addGroup():
        gName = groupName.get("1.0", END).split('\n')[0]
        if gName in groups.keys():
            ans=messagebox.askokcancel(title="Already exists", message="A group already exists with this name.\nDo you want to overwrite it?")
            if not ans:
                return -1
        else:
            groups[gName] = []
            
        gMemsText = groupFeatures.get("1.0", END)
        for i in gMemsText.split('\n'):
            if i.isalnum():
                groups[gName].append(i)

        dispGroups.delete("1.0", END)
        dispGroups.insert("1.0", formatGroups())
        
    def loadGroup():
        gName = groupName.get("1.0", END).split('\n')[0]
        if gName in groups.keys():
            groupFeatures.delete("1.0", END)
            groupFeatures.insert("1.0", '\n'.join(groups[gName]))
        else:
            messagebox.showerror(title="Error", message="Group not found")

    def deleteGroup():
        gName = groupName.get("1.0", END).split('\n')[0]
        if gName in groups.keys():
            ans=messagebox.askokcancel(title='Confirm', message="Are you sure you want to delete the group\n"+gName)
            if ans:
                groups.pop(gName)
                groupFeatures.delete("1.0", END)
            messagebox.showinfo(title="Success", message="Successfully removed group\n"+gName)
        else:
            messagebox.showerror(title="Error", message="Group not found")
        dispGroups.delete("1.0", END)
        dispGroups.insert("1.0", formatGroups())
    
    topDescriptor = Label(groupScreen, text="Name for group of features")
    topDescriptor.pack(fill='both', side='top')

    groupName = Text(groupScreen, height=1)
    groupName.pack(fill='x', side='top')

    splitter=ttk.Separator(groupScreen, orient='horizontal')
    splitter.pack(side='top', fill='x')

    featDescriptor = Label(groupScreen, text="Features in group")
    featDescriptor.pack(fill='both', side='top')

    groupFeatures = Text(groupScreen, height=20)
    groupFeatures.pack(fill='x', side='top')

    bAddGroup = Button(groupScreen, text="Add new group", height=3, command=addGroup)
    bAddGroup.pack(fill='x', side='top')

    bLoadGroup = Button(groupScreen, text="Load group", height=3, command=loadGroup)
    bLoadGroup.pack(fill='x', side='top')

    bRemoveGroup = Button(groupScreen, text="Disband group", height=3, command=deleteGroup)
    bRemoveGroup.pack(fill='x', side='top')

    
def viewRules():
    ruleScreen = Tk()
    ruleScreen.title('Rules')
    ruleScreen.geometry("150x600")

    def applyRules():
        word = startingWord.get("1.0", END)
        wordFeats = textToFeatures(word)

        endingWord.delete("1.0", END)
        endingWord.insert("1.0", featuresToText(wordFeats))
        

    startingWord = Text(ruleScreen, height=1)
    startingWord.pack(fill='x', side='top')

    goButton = Button(ruleScreen, text="GO!", command=applyRules, height=2)
    goButton.pack(fill='x', side='top')

    ruleFrames = []
    for i in range(0, len(rules)):
        ruleFrames.append([])
        ruleFrames[i].append(Frame(ruleScreen, height=2, width=10))
        ruleFrames[i][0].pack(fill='x', side='top')
        ruleFrames[i].append(Label(ruleFrames[i][0], text=formatRule(rules[i])))
        ruleFrames[i][1].pack(fill='both', side='left')
        print(i,rules[i])
        

    endingWord = Text(ruleScreen, height=2)
    endingWord.pack(fill='x', side='top')

def formatRule(ruleArray):
    ruleStr = 'if '
    ruleStr+=' +'.join(ruleArray[0])
    ruleStr+=' '+ruleArray[1]+' '
    ruleStr+=' +'.join(ruleArray[2])
    ruleStr+=': '+ruleArray[3]+' '
    if ruleArray[3] == 'assimilate':
        ruleStr += ' +'.join(ruleArray[4])
    elif ruleArray[3] == 'propagate':
        ruleStr += ' +'.join(ruleArray[4])+' '
        ruleStr+=ruleArray[5]

    print(ruleStr)
    makeNewline = False
    toReturn = ''
    lastSpace=0
    for i in range(0, len(ruleStr)):
        if i%20 == 19:
            makeNewline = True
        if makeNewline and ruleStr[i] == ' ':
            toReturn+=ruleStr[lastSpace+1:i]+'\n'
            print(ruleStr[lastSpace+1:i])
            lastSpace = i
            makeNewline = False
    toReturn+=ruleStr[lastSpace:len(ruleStr)]
    print(ruleStr[lastSpace:len(ruleStr)])
    return toReturn
            
menuBar = Menu(root)

fileBar = Menu(menuBar)
fileBar.add_command(label="Save Characters", command=saveChars)
fileBar.add_command(label="Save Rules", command=saveRules)
fileBar.add_command(label="Load Characters", command=loadChars)
fileBar.add_command(label="Load Rules", command=loadRules)
menuBar.add_cascade(label="File", menu=fileBar)
root.config(menu=menuBar)

viewBar = Menu(menuBar)
viewBar.add_command(label="View IPA Chart", command=viewIPA)
viewBar.add_command(label="View Rules", command=viewRules)
menuBar.add_cascade(label='View', menu=viewBar)

bAdd = Button(root, text = "Add character\nand features\nto logs", command = addSound) 
bAdd.place(relx = 1, height = 75, width = 100, x =-125, y = 125, anchor = NE)

bLoad = Button(root, text = "Load character\nfrom logs", command=loadSound)
bLoad.place(relx=1, height=75, width=100, x=-125, y=200, anchor=NE)

bRemove = Button(root, text="Remove character\n from logs", command=removeSound)
bRemove.place(relx=1, height=75, width=100, x=-125, y=275, anchor=NE)

charInput = Text(root)
charInput.place(height=25, width=100, relx=1, x=-125, y=50, anchor = NE)

charLbl = Label(root, text = "Character")
charLbl.place(relx = 1, x = -144, y=80, anchor=NE)

attrInput = Text(root)
attrInput.place(height=200, width = 100, relx=1, x=-10, y=50, anchor = NE)

attrLbl = Label(root, text="Features")
attrLbl.place(relx = 1, x = -33, y=255, anchor=NE)

dispFeatures = Text(root)
dispFeatures.place(height=300, width=350, relx = 1, x=-600, y=50, anchor=NW)

scrollb = Scrollbar(command=dispFeatures.yview)
scrollb.place(height=300, width=10, relx = 1, x=-250, y=50, anchor=NW)
dispFeatures['yscrollcommand']=scrollb.set

dispGroups = Text(root)
dispGroups.place(height=150, width=300, relx=1, x=-10, y=425, anchor=NE)
dispGroups.insert("1.0", "No feature groups yet!")
groupScrollB = Scrollbar(command=dispGroups.yview)
groupScrollB.place(height=150, width=10, relx=1, x=-10, y=425, anchor=NE)
dispGroups['yscrollcommand']=groupScrollB.set
    
bAddRule = Button(root, text="Create new rule", command=addRuleWindow)
bAddRule.place(height=50, width=150, relx = 1, x = -300, y=400, anchor=CENTER)

bAddGrouping = Button(root, text='Add new feature grouping', command=addGroupWindow)
bAddGrouping.place(height=50, width=150, relx=1, x=-150, y=400, anchor=CENTER)

viewRules()
viewIPA()

root.mainloop()
##changePlus = Text(root)
##changePlus.place(height=200, width=100, relx = 1, x = -500, y=400, anchor=NW)

##lblMinus = Label(root, text="-")
##lblMinus.place(height=25, width=25, relx = 1, x = -400, y=400, anchor=NW)
##
##changeMinus = Text(root)
##changeMinus.place(height=200, width=100, relx = 1, x = -375, y=400, anchor=NW)
##
##bGo = Button(root, text="=", command=plusMinusRuleButton)
##bGo.place(height=50, width=50, relx = 1, x = -250, y=400, anchor=NW)
##
##changeEnd = Text(root)
##changeEnd.place(height=50, width=50, relx = 1, x = -150, y=400, anchor=NW)
##
