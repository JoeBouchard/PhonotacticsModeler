from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk
import random
import time

characters = {}

rules = []
groups = {}

root = Tk()
root.title("Phonological Rule Processor")
root.geometry("1050x720")

def saveChars():
    fName = filedialog.asksaveasfilename(filetypes=[("Character files", "*.chr")], defaultextension=[("Character files", "*.chr")])
    root.update()
    if fName != '':
        toSave = open(fName, mode='w', encoding='utf-8')
        toSave.write(str(characters))
        toSave.close()
    else:
        messagebox.showwarning(title="File not found", message="You did not select a file")

def saveRules():
    print(rules)
    fName = filedialog.asksaveasfilename(filetypes=[("Rule files", "*.rlz")], defaultextension=[("Rule files", "*.rls")])
    if fName != '':
        toSave = open(fName, mode='w', encoding='utf-8')
        root.update()
        toSave.write(str(rules))
        toSave.close()
    else:
        messagebox.showwarning(title="File not found", message="You did not select a file")


def saveGroups():
    fName = filedialog.asksaveasfilename(filetypes=[("Groups files", "*.grpz")], defaultextension=[("Groups files", "*.grpz")])
    if fName != '':
        toSave = open(fName, mode='w', encoding='utf-8')
        root.update()
        toSave.write(str(groups))
        toSave.close()
    else:
        messagebox.showwarning(title="File not found", message="You did not select a file")


def autosave():
    t=str(int(time.time()))
    yn=messagebox.askyesnocancel("Save?", message="Would you like to save your data?")
    if yn:
        saveChars()
        saveRules()
        saveGroups()
    if yn != None:
        root.destroy()
        ipaChart.destroy()

def loadChars():
    toLoad = filedialog.askopenfilename(filetypes=[("Character files", "*.chr")])
    root.update()
    if toLoad != '':
        file = open(toLoad, 'r', encoding='utf-8')
        toReturn = eval(file.read())
        file.close()
        print(toReturn)
        for i in toReturn:
            characters[i] = toReturn[i]
        dispFeatures.delete("1.0", END)
        dispFeatures.insert("1.0", formatChars())
    else:
        messagebox.showwarning(title="File not found", message="You did not select a file")


def loadRules():
    toLoad = filedialog.askopenfilename(filetypes=[("Rule files", "*.rlz")])
    root.update()
    if toLoad != '':
        file = open(toLoad, 'r')
        contents=file.read()
        loadedRules = eval(contents)
        file.close()
        for i in loadedRules:
            rules.append(i)
        updateRuleBox()
        dispGroups.delete("1.0", END)
        dispGroups.insert("1.0", formatGroups())
    else:
        messagebox.showwarning(title="File not found", message="You did not select a file")


def loadGroups():
    toLoad = filedialog.askopenfilename(filetypes=[("Groups files", "*.grpz")])
    root.update()
    if toLoad != '':
        file = open(toLoad, 'r', encoding='utf-8')
        toReturn = eval(file.read())
        file.close()
        print(toReturn)
        for i in toReturn:
            groups[i] = toReturn[i]
        dispGroups.delete("1.0", END)
        dispGroups.insert("1.0", formatGroups())
    else:
        messagebox.showwarning(title="File not found", message="You did not select a file")


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

def startIPA():
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

def hideIPA():
    ipaChart.withdraw()
    
def viewIPA(event=None):
    ipaChart.deiconify()
    ipaChart.focus_force()

def textToFeatures(text):
    features = []
    for i in text:
        if i in characters.keys():
            features.append([])
            for j in characters[i]:
                features[-1].append(j)
        elif i.isalnum():
            waitVar = IntVar()
            textInput=Tk()
            textInput.title('New character found')
            textInput.geometry("150x300")
            heading = Label(textInput, text="New character found\nPlease list features for\n"+i)
            heading.pack(ipadx=2, ipady=2, padx=2, pady=2, fill='both', side='top')#lace(relx=1, width=150, x=0, y=20, anchor=NE)

            newFeats = Text(textInput, height=10)
            newFeats.pack(ipadx=2, ipady=2, padx=2, pady=2, fill='both', side='top')#lace(relx=1, width=125, height=200, x=-12.5, y=50, anchor=NE)

            def addFeatsFromPopup(i):
                characters[i] = []
                newAttrs = newFeats.get("1.0", END)
                for j in newAttrs.split("\n"):
                    if j.isalpha():
                        characters[i].append(j)
                features.append(characters.copy()[i])
                waitVar.set(1)
                
            addNewFeats = Button(textInput, text="Add features for\n"+i, command=lambda: addFeatsFromPopup(i), height=2)
            addNewFeats.pack(ipadx=2, ipady=2, padx=2, pady=2, fill='both', side='top')#lace(relx=1, width=125, height=50, x=-12.5, y=260, anchor=NE)
            
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
        for char in characters.copy().keys():
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
            heading.pack(ipadx=2, ipady=2, padx=2, pady=2, fill='both', side='top')#lace(relx=1, width=150, height=160, x=0, y=20, anchor=NE)

            newFeats = Text(textInput, height=1)
            newFeats.pack(ipadx=2, ipady=2, padx=2, pady=2, fill='both', side='top')#lace(relx=1, width=25, height=25, x=-100, y=180, anchor=NE)

            def addCharFromPopup(i):
                newAttrs = newFeats.get("1.0", END)
                newChar = newAttrs.split('\n')[0]
                characters[newChar] = i
                textList.append(newChar)
                waitVar.set(1)
                
            addNewFeats = Button(textInput, text="Add new character", command=lambda: addCharFromPopup(i))
            addNewFeats.pack(ipadx=2, ipady=2, padx=2, pady=2, fill='both', side='top')#lace(relx=1, width=125, height=50, x=-12.5, y=260, anchor=NE)
            
            textInput.focus_force()
            root.wait_variable(waitVar)
            textInput.destroy()
            dispFeatures.delete("1.0", END)
            dispFeatures.insert("1.0", formatChars())

    return ''.join(textList)

def updateRuleInput(value):
    if value == "assimilate":
        toAssimilate.pack(ipadx=2, ipady=2, padx=2, pady=2, fill='both', side='left')
        propDistance.pack_forget()
        delSelect.pack_forget()
        lblAdd.pack_forget()
        lblSubtract.pack_forget()
        toSubtract.pack_forget()

    elif value == "propagate":
        toAssimilate.pack(ipadx=2, ipady=2, padx=2, pady=2, fill='both', side='left')
        propDistance.pack(ipadx=2, ipady=2, padx=2, pady=2, fill='both', side='left')
        delSelect.pack_forget()
        lblAdd.pack_forget()
        lblSubtract.pack_forget()
        toSubtract.pack_forget()
        
    elif value == "delete":
        toAssimilate.pack_forget()
        propDistance.pack_forget()
        lblAdd.pack_forget()
        lblSubtract.pack_forget()
        toSubtract.pack_forget()
        delSelect.pack(ipadx=2, ipady=2, padx=2, pady=2, fill='both', side='left')

    elif value == "insert":
        toAssimilate.pack(ipadx=2, ipady=2, padx=2, pady=2, fill='both', side='left')
        lblAdd.pack_forget()
        lblSubtract.pack_forget()
        toSubtract.pack_forget()
        delSelect.pack_forget()
        propDistance.pack_forget()

    elif value == "add/subtract feature":
        propDistance.pack_forget()
        toAssimilate.pack_forget()
        lblAdd.pack(ipadx=2, ipady=2, padx=2, pady=2, fill=None, side='left')
        toAssimilate.pack(ipadx=2, ipady=2, padx=2, pady=2, fill='both', side='left')
        lblSubtract.pack(ipadx=2, ipady=2, padx=2, pady=2, fill=None, side='left')
        toSubtract.pack(ipadx=2, ipady=2, padx=2, pady=2, fill='both', side='left')

def createRule():
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
    val5 = None
    val6 = None
    if val4 != '':
        print(val4)
        if val4 == 'assimilate' or val4 == 'insert':
            val5 = []
            for i in toAssimilate.get("1.0", END).split('\n'):
                if i != '':
                    val5.append(i)
            print(len(val5))
            if len(val5) == 1 and val4 == 'insert':
                print(val5)
                val5 = textToFeatures(val5[0])[0]
                print(val5[0])
            
        elif val4 == 'propagate' or val4 == 'delete':
            val5 = []
            for i in toAssimilate.get("1.0", END).split('\n'):
                if i != '':
                    val5.append(i)
            val6 = propVar.get()

        elif val4 == 'add/subtract feature':
            val5 = []
            for i in toAssimilate.get("1.0", END).split('\n'):
                if i != '':
                    val5.append(i)
            val6 = []
            for i in toSubtract.get("1.0", END).split('\n'):
                if i != '':
                    val6.append(i)
        
        newRule = [val1, val2, val3, val4, val5, val6]
        return newRule
    return -1

def addRule():
    newRule = createRule()
    if newRule != -1:
        rules.append(newRule)
        messagebox.showinfo("Success!", "Added new rule:\n"+str(rules[-1]))
    else:
        messagebox.showerror("Error", "Invalid rule. \nBlank combobox")
    updateRuleBox()

def addRuleSel():
    newRule = createRule()
    if newRule != -1:
        rules.insert(ruleBox.curselection()[0], newRule)
        messagebox.showinfo("Success!", "Added new rule:\n"+str(rules[-1]))
    else:
        messagebox.showerror("Error", "Invalid rule. \nBlank combobox")
    updateRuleBox()

def moveRuleUp():
    i = ruleBox.curselection()[0]
    if i > 0:
        k = rules[i-1]
        rules[i-1] = rules[i]
        rules[i] = k
        updateRuleBox()
    ruleBox.select_set(i-1)

def moveRuleDown():
    i = ruleBox.curselection()[0]
    if i < len(rules)-1:
        k = rules[i+1]
        rules[i+1] = rules[i]
        rules[i] = k
        updateRuleBox()
    ruleBox.select_set(i+1)

    
def loadSelectedRule():
    rule = rules[ruleBox.curselection()[0]]
    changeStart.delete("1.0", END)
    changeStart.insert("1.0", '\n'.join(rule[0]))

    beforeAfterVar.set(rule[1])

    triggerAttr.delete("1.0", END)
    triggerAttr.insert("1.0", '\n'.join(rule[2]))

    actionVar.set(rule[3])

    updateRuleInput(rule[3])

    if rule[3] != 'delete':
        toAssimilate.delete("1.0", END)
        toAssimilate.insert("1.0", '\n'.join(rule[4]))

        if 'subtract' in rule[3]:
            toSubtract.delete("1.0", END)
            toSubtract.insert("1.0", '\n'.join(rule[5]))

        if 'propagate' in rule[3]:
            propVar.set(rule[5])

    else:
        propVar.set(rule[4])

def delSelectedRule():
    rules.pop(ruleBox.curselection()[0])
    updateRuleBox()
            
    
def addGroup():
    gName = groupName.get("1.0", END).split('\n')[0]
    if gName in groups.keys():
        ans=messagebox.askokcancel(title="Already exists", message="A group already exists with this name.\nDo you want to overwrite it?")
        if not ans:
            return -1
        else:
            groups[gName] = []
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

def applyRules():
    word = startingWord.get("1.0", END)
    wordFeats = textToFeatures(word)

    for r in rules:
        for i in range(0, max(1, len(wordFeats)-1)):
            valid=True
            for f in r[0]:
                valid = True
                if f not in wordFeats[i]:
                    valid = False
                    break
            if valid:
                j=i
                if 'p' in r[1]:
                    j+=1
                elif 'f' in r[1]:
                    j-=1
                if j < len(wordFeats)and j >= 0:
                    for f in r[2]:
                        if f not in wordFeats[j]:
                            valid = False
                            break
                else:
                    valid=False
            if valid:
                if r[3] == 'assimilate':
                    featToAssim = []
                    for g in r[4]:
                        if g in list(groups.keys()):
                            featToAssim.append(groups[g])
                        else:
                            messagebox.showwarning(title="Not a group",
                                                   message="No group titled:\t"+g+"\nAssimilating "+g+"as a feature.")
                            groups[g] = [g]
                            featToAssim.append([g])
                    for grup in featToAssim:
                        for feat in grup:
                            while feat in wordFeats[i]:
                                wordFeats[i].remove(feat)
                            if feat in wordFeats[j]:
                                wordFeats[i].append(feat)
                                
                elif r[3] == 'propagate':
                    featToProp = []
                    for g in r[4]:
                        if g in list(groups.keys()):
                            featToProp.append(groups[g])
                        else:
                            messagebox.showwarning(title="Not a group",
                                                   message="No group titled:\t"+g+"\nAssimilating "+g+"as a feature.")
                            groups[g] = [g]
                            featToProp.append([g])


                    allOrNext = 'next' in r[5]
                    allSounds = 'sound' in r[5]
                    for k in range(i+1, len(wordFeats)):
                        vowelComp = 'vowel' in wordFeats[k] and 'vowel' in r[5]
                        consComp = 'consonant' in wordFeats[k] and 'consonant' in r[5]
                        if (vowelComp or consComp or allSounds) and allOrNext:
                            for grup in featToProp:
                                for feat in grup:
                                    while feat in wordFeats[k]:
                                        wordFeats[k].remove(feat)
                                    if feat in wordFeats[i]:
                                        wordFeats[k].append(feat)

                            if allOrNext:
                                allOrNext = 'all' in r[5]

                elif r[3] == 'delete':
                    k=i
                    if 'previous' in r[5]:
                        k-=1
                    elif 'next' in r[5]:
                        k+=1
                    wordFeats.pop(k)

                elif r[3] == 'insert':
                    wordFeats.insert(max(i, j), r[4])

                else:
                    for f in r[5]:
                        for g in groups.keys():
                            if f == g:
                                for k in groups[g]:
                                    while k in wordFeats[i]:
                                        wordFeats[i].remove(k)
                        while f in wordFeats[i]:
                            wordFeats[i].remove(k)
                    for f in r[4]:
                        for g in groups.keys():
                            if f in groups[g]:
                                for k in groups[g]:
                                    while k in wordFeats[i]:
                                        wordFeats[i].remove(k)
                        if f not in wordFeats[i]:
                            print(f)
                            wordFeats[i].append(f)
    print(wordFeats)

    endingWord.delete("1.0", END)
    endingWord.insert("1.0", featuresToText(wordFeats))
    dispGroups.delete("1.0", END)
    dispGroups.insert("1.0", formatGroups())
    dispFeatures.delete("1.0", END)
    dispFeatures.insert("1.0", formatChars())
        
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

    makeNewline = False
    toReturn = 'i'
    lastSpace=0
    for i in range(0, len(ruleStr)):
        if i%20 == 19:
            makeNewline = True
        if makeNewline and ruleStr[i] == ' ':
            toReturn+=ruleStr[lastSpace+1:i]+'\n'
            lastSpace = i
            makeNewline = False
    toReturn+=ruleStr[lastSpace:len(ruleStr)]
    return toReturn

def updateRuleBox():
    for j in range(0, len(rules)+5):
        ruleBox.delete(j)
    for i in range(0, len(rules)):
        ruleText = str(i+1)+". "+formatRule(rules[i])
        while '\n' in ruleText:
            ruleText=ruleText.replace('\n', ' ')
        ruleBox.delete(i)
        ruleBox.insert(i, ruleText)
    
            
menuBar = Menu(root)

root.bind("<F1>", viewIPA)
root.protocol('WM_DELETE_WINDOW', autosave)

root['bg'] = '#a3ccf4'
baseBg = "#6389df"

fileBar = Menu(menuBar)
fileBar.add_command(label="Save Characters", command=saveChars)
fileBar.add_command(label="Save Rules", command=saveRules)
fileBar.add_command(label="Save Groups", command=saveGroups)
fileBar.add_command(label="Load Characters", command=loadChars)
fileBar.add_command(label="Load Rules", command=loadRules)
fileBar.add_command(label="Load Groups", command=loadGroups)
menuBar.add_cascade(label="File", menu=fileBar)
root.config(menu=menuBar)

viewBar = Menu(menuBar)
viewBar.add_command(label="View IPA Chart \t <F1>", command=viewIPA)
menuBar.add_cascade(label='View', menu=viewBar)

##Frame that everything but rule inputs is in
topFrame = Frame(root, width=1000, height=420, bg=baseBg)
labelBg = '#bebcc1'

##Make frame for adding tokens
charFrame = Frame(topFrame, width=400, height=400, bg=baseBg, bd=2)
charInputFrame = Frame(charFrame, width=100, height=400, bg=baseBg)

charLbl = Label(charInputFrame, text = "Character")
charLbl.pack(ipadx=2, ipady=2, padx=2, pady=2, fill='both', side='top')

charInput = Text(charInputFrame, width=15, height=1)
charInput.tag_configure("center", justify='center')
charInput.tag_add("center", "1.0", END)
charInput.pack(ipadx=2, ipady=2, padx=2, pady=2, fill='both', side='top')#lace(height=25, width=100, relx=1, x=-125, y=50, anchor = NE)

attrLbl = Label(charInputFrame, text="Features")
attrLbl.pack(ipadx=2, ipady=2, padx=2, pady=2, fill='both', side='top')#lace(relx = 1, x = -33, y=255, anchor=NE)

attrInput = Text(charInputFrame, width=15, height=20)
attrInput.pack(ipadx=2, ipady=2, padx=2, pady=2, fill='both', side='top', expand=1)#lace(height=200, width = 100, relx=1, x=-10, y=50, anchor = NE)

bAdd = Button(charInputFrame, height=2, text = "Add character and\nfeatures to logs", command = addSound) 
bAdd.pack(fill='both', side='top')#lace(relx = 1, height = 75, width = 100, x =-125, y = 125, anchor = NE)

bLoad = Button(charInputFrame, height=2, text = "Load character\nfrom logs", command=loadSound)
bLoad.pack( fill='both', side='top')#lace(relx=1, height=75, width=100, x=-125, y=200, anchor=NE)

bRemove = Button(charInputFrame,height=2, text="Remove character\n from logs", command=removeSound)
bRemove.pack(fill='both', side='top')#lace(relx=1, height=75, width=100, x=-125, y=275, anchor=NE)


dispFeatures = Text(charFrame, height=20, width=30)
scrollb = Scrollbar(charFrame, command=dispFeatures.yview)
scrollb.pack(ipady=2, pady=2, fill='y', side='left')

dispFeatures['yscrollcommand']=scrollb.set
dispFeatures.pack(ipady=2, pady=2, fill='both', side='left', expand=1)
dispFeatures.insert("1.0", "No characters listed yet!")

charInputFrame.pack(ipadx=2, ipady=2, padx=2, pady=2, fill='both', side='right')#, expand=1)
charFrame.pack(ipadx=2, ipady=2, padx=2, pady=2, fill='both', side='left', anchor='nw', expand=1)

##Make frame for adding groups
groupFrame = Frame(topFrame, width=400, height=400, bg=baseBg)
groupScreen = Frame(groupFrame, width=100, height=400, bg=baseBg)

topDescriptor = Label(groupScreen, text="Feature group name")
topDescriptor.pack(ipadx=2, ipady=2, padx=2, pady=2, fill='both', side='top')

groupName = Text(groupScreen, height=1, width=10)
groupName.pack(ipadx=2, ipady=2, padx=2, pady=2, fill='x', side='top')

featDescriptor = Label(groupScreen, text="Features in group")
featDescriptor.pack(ipadx=2, ipady=2, padx=2, pady=2, fill='both', side='top')

groupFeatures = Text(groupScreen, height=20, width=20)
groupFeatures.pack(ipadx=2, ipady=2, padx=2, pady=2, fill='both', side='top', expand=1)

bAddGroup = Button(groupScreen, text="Add new group", height=2, command=addGroup)
bAddGroup.pack(ipadx=0, ipady=0, padx=0, pady=0, fill='x', side='top')

bLoadGroup = Button(groupScreen, text="Load group", height=2, command=loadGroup)
bLoadGroup.pack(ipadx=0, ipady=0, padx=0, pady=0, fill='x', side='top')

bRemoveGroup = Button(groupScreen, text="Disband group", height=2, command=deleteGroup)
bRemoveGroup.pack(ipadx=0, ipady=0, padx=0, pady=0, fill='x', side='top')

dispGroups = Text(groupFrame, width=30)

groupScrollB = Scrollbar(groupFrame, command=dispGroups.yview)
groupScrollB.pack(ipady=2, pady=2, fill='y', side='right')
dispGroups.pack(ipady=2, pady=2, fill='both', side='right', expand=1)
dispGroups.insert("1.0", "No feature groups yet!")
dispGroups['yscrollcommand']=groupScrollB.set

groupScreen.pack(ipadx=2, ipady=2, padx=2, pady=2, fill='both', side='right')
groupFrame.pack(ipadx=2, ipady=2, padx=2, pady=2, fill='both', side='right', expand=1)

##Make frame for showing rules

ruleDisp = Frame(topFrame, width=300, height=400, bg='#a3ccf4')

startWordLbl = Label(ruleDisp, width=10, height=1, text="Input Word")
startWordLbl.pack(ipadx=2, ipady=2, padx=2, pady=2, fill=None, side='top')

startingWord = Text(ruleDisp, height=1, width=20)
startingWord.pack(ipadx=2, ipady=2, padx=2, pady=2, fill='x', side='top')

goButton = Button(ruleDisp, text="GO!", command=applyRules, height=2)
goButton.pack(ipadx=2, ipady=2, padx=2, pady=2, fill='x', side='top')

ruleFrames = []

ruleBox = Listbox(ruleDisp, height=15, width=20)

ruleBox.insert(1, "Rules go here!")
    
ruleScrollX = Scrollbar(ruleDisp, command=ruleBox.xview, orient='horizontal')
ruleBox['xscrollcommand'] = ruleScrollX.set

ruleBox.pack(ipadx=2, ipady=2, padx=2, pady=2, side='top', fill='both', expand=1)
ruleScrollX.pack(ipadx=2, ipady=2, padx=2, pady=2, side="top", fill='x')

endingWord = Text(ruleDisp, height=2, width=20)
endingWord.pack(ipadx=2, ipady=2, padx=2, pady=2, fill='x', side='bottom')

endWordLbl = Label(ruleDisp, width=11, height=1, text="Output Word")
endWordLbl.pack(ipadx=2, ipady=2, padx=2, pady=2, fill=None, side='bottom')

moveDownButton = Button(ruleDisp, command=moveRuleDown, height=1, text="v Move rule down v")
moveDownButton.pack(fill='x', side='bottom')

moveUpButton = Button(ruleDisp, command=moveRuleUp, height=1, text="^ Move rule up ^")
moveUpButton.pack(fill='x', side='bottom')

ruleDisp.pack(ipadx=2, padx=2, fill='both', side='left', expand=1)

##Make frame for adding rules
ruleScreen = Frame(root, width=1000, height=150, bg='#a3ccf4')

delRuleButton = Button(ruleScreen, text="Delete\nselected\nrule", command=delSelectedRule)
delRuleButton.pack(ipadx=2, ipady=2, padx=2, pady=2, fill='y', side='left')

loadRuleButton = Button(ruleScreen, text="Load\nselected\nrule", command=loadSelectedRule)
loadRuleButton.pack(ipadx=2, ipady=2, padx=2, pady=2, fill='y', side='left')

ruleLbl = Label(ruleScreen, text="if")
ruleLbl.pack(ipadx=2, ipady=2, padx=2, pady=2, fill=None, side='left')

changeStart = Text(ruleScreen, height=10, width=11)
changeStart.pack(ipadx=2, ipady=2, padx=2, pady=2, fill='x', side='left')

beforeAfterVar = StringVar(ruleScreen)
beforeAfter = OptionMenu(ruleScreen, beforeAfterVar, "precedes", "follows", "is")
beforeAfter.pack(ipadx=2, ipady=2, padx=2, pady=2, fill='x', side='left')

triggerAttr = Text(ruleScreen, height=10, width=11)
triggerAttr.pack(ipadx=2, ipady=2, padx=2, pady=2, fill='x', side='left')

lblPlus = Label(ruleScreen, text=", then :")
lblPlus.pack(ipadx=2, ipady=2, padx=2, pady=2, fill=None, side='left')

actionVar = StringVar(ruleScreen)
actionChoice=OptionMenu(ruleScreen, actionVar, "assimilate", "propagate", "delete", "insert", "add/subtract feature", command=updateRuleInput)
actionChoice.pack(ipadx=2, ipady=2, padx=2, pady=2, fill=None, side='left')

toAssimilate = Text(ruleScreen, height=10, width=11)
propVar = StringVar(ruleScreen)
propDistance = OptionMenu(ruleScreen, propVar, "to next consonant", "to next vowel", "to next sound", "to all consonants", "to all vowels", "to all sounds")
delSelect = OptionMenu(ruleScreen, propVar, "previous character", "this character", "following character")

lblAdd = Label(ruleScreen, text="Add")
lblSubtract = Label(ruleScreen, text="and subtract")
toSubtract=Text(ruleScreen, height=10, width=11)

ruleButtonSelection = Button(ruleScreen, text="Add\nRule\nAbove\nSelection", command=addRuleSel)
ruleButtonSelection.pack(ipadx=2, ipady=2, padx=2, pady=2, fill='both', side='right')

ruleButton = Button(ruleScreen, text="Add Rule", command=addRule)
ruleButton.pack(ipadx=2, ipady=2, padx=2, pady=2, fill='both', expand=1, side='right')

ruleScreen.pack(fill='both', side='bottom', expand=1)

topFrame.pack(side='top', fill='both', expand=1)

ipaChart = Tk()
ipaChart.title("IPA Chart")
ipaChart.geometry("350x200")
ipaChart.protocol('WM_DELETE_WINDOW', hideIPA)

startIPA()
viewIPA()

root.mainloop()
