# Phonology Rule Modeler

Welcome to the Phonology Rule Modeler, hosted at https://github.com/JoeBouchard/PhonotacticsModeler!
This will guide you through the installation process and give you the rundown on how to use this program.

# Installation

### Option 1: .exe
When you download this repository, you should be able to just unzip it and run Phonotactics.exe. Double click on it to run it. It will ask you if you want to trust it. Click "More Information", then "Run Anyway". The Phonotactics.exe will be kept up-to-date with the Python code, so there is no reason to prefer one over the other as far as updates go. Use Option 2 only if Option 1 does not work.

### Option 2: The Python Code
If Option 1 does not work, you can run it by double clicking the Phonotactics.py. However, this requires having Python 3.6 or higher installed on your machine. You can find the links to install Python [here](https://www.python.org/downloads/release/python-385/). 

Windows users will need the Windows x86 executable installer, found [here](https://www.python.org/ftp/python/3.8.5/python-3.8.5-amd64.exe). 

Mac users will need the macOS installer, found [here](https://www.python.org/ftp/python/3.8.5/python-3.8.5-macosx10.9.pkg). 

Linux users, you're using Linux. You're tech savvy enough to figure it out.
After installing Python, double click Phonotactics.py. The window should pop up and be ready for use.

### Updating
To update to the newest version, download [this repository](https://github.com/JoeBouchard/PhonotacticsModeler) again.

# Usage
This project is intended to model the underlying phonological rules and processes behind languages and apply them to given inputs. It achieves this using 3 different user-defined variables: *Characters*, *Groups*, and *Rules*. Further explanation of these topics is given below.

## Characters
*Characters* are IPA symbols with Features attached. Features may include anything the user wants to input, from place and manner of articulataion to tense/lax vowels. Characters are currently always one symbol long but may include diacritical marks. You can bring up a basic IPA chart at any point by pressing **F1**

#### Character Input
All widgets related to Character input are on the left side of the window. On the far left is a box that displays all Characters the user has input. To the right, there is a small text entry labeled "Character" and a large one beneath it labeled "Features". 

Write the Character you wish to define in the Character input box, and list its Features in the box below, one on each line with no punctuation. Click "Add character and features to logs" to save the Character into the database of Characters. The box that displays all Characters will update accordingly. 

To edit a character, input it into the "Character" box and click "Load character from logs" to load its features. Add or subtract whatever features you want, then click "Add character and features to logs"

To remove a Character, input it into the "Character" box and click "Remove character from logs". 

## Groups
*Groups* are user-defined collections of mutually exclusive features. For example, a group "Place" might contain the features "bilabial", "labiodental", "alveolar", "velar", etc. Groups are useful in the process of creating Rules, which will be explained more in the Rules section.

#### Defining Groups
All widgets related to Groups are on the right side of the window. On the far right is a box that displays all Groups the user has input. To the left, there is a text entry box that mimics the Character input box. The process for creating Groups mimics the process for creating Characters.

## Rules
*Rules* represent the Phonological processes that underlie a language. Rule related widgets are colored a light blue.

### Rule Entry
Rules are entered using the Rule Entering widget on the bottom of the window. Using the drop down menus and text entries, you are able to define a variety of Rules. The entry is laid out in sentence format following the format "if Target precedes/follows/is Trigger, then perform an operation".

#### Target
The *Target* is the first text entry box in the Rule Entry widget. Here the user provides a list of Features to look for that will be acted on. Like with Character and Groups, the Features here must be entered with one per line and no punctuation. The Target is the character that receives the change in the actions of *assimilate*, *delete*, and *add/subtract feature* and gives its features in the *propagate* action, all of which are explained more in depth under the "Rule Types" heading.

#### Trigger
The *Trigger* is the second text entry box in the Rule Entry widget. Here the user provides a list of Features that will trigger the rule to apply to the Target. Feature entry follows the standard Feature entry format. The Trigger gives its attributes to the Target in the *assimilate* rule, explained in the "Rule Types" heading. The Trigger may be left blank to apply every time the Target occurs.

#### Proximity
The *Proximity* drop down bar indicates the position of the Trigger relative to the Target. 

#### Rule Types
There are currently 5 basic rule types: *assimilate*, *propagate*, *insert*, *delete*, and *add/subtract feature*
1. Assimilate: Copies a value from the Trigger to the Target. The text entry box can be a single Feature or a Group. If the text entry is a Group, it will replace the Features from that Group that the Target has with those of the Trigger. 
2. Propagate: Spreads a value from the Target as far as indicated. The text entry box selects Groups or Features to be spread, and the drop down menu defines how far to spread those features.
3. Insert: Inserts a Character or set of Features between Target and Trigger. Input a Character or list of Features into the text entry box. Note: This rule does NOT allow for the use of Groups.
4. Delete: Deletes the Character selected by the drop down menu. Previous/this/following Characters are defined by the position of the Target.
5. Add/Subtract feature: Adds and/or subtracts Features or Groups from Target. The first entry box can only take in Features and adds those features to the Target. If the Feature is in a Group, it replaces any Features from the Group with itself. The second entry box takes Groups or Features and removes them from the Target.

#### Adding Rules
To add the Rule defined in the Rule creator to the end of the list of Rules, click the "Add Rule" button. 
To add the Rule before the selected Rule, click "Add Rule Before Selection".

#### Modifying Rules
Select a Rule in the Rule Viewer and click "Load Rule" to load the Rule into the Rule Entering widget. 
Select a Rule in the Rule Viewer and click "Delete Rule" to delete the Rule. This action cannot be undone.
Note: Unlike with Characters and Groups, loading then adding a group will duplicate it, not replace it. The only way to replace a rule is to copy it then manually deleting the original.

### Rule Viewing
The Rule Viewer is located in the center of the window. This is where you input words, view and order Rules, and get the output of the Rules.

#### Input
To input a word, enter it into the small text entry box labeled "Input Word". Click "GO!" to apply the Rules to the word and display the result in the text box labeled "Output Word"

#### List of Rules
Below the "GO!" button is a list of Rules. Click one to select it, and it will turn blue to mark the selection. If the Rules are too long, use the scrollbar beneath the list to scroll side to side. Use the scroll wheel on your mouse to scroll up and down along the list of Rules.

#### Ordering Rules
Once you have selected a Rule, use the "Move rule up" and "Move rule down" buttons to move the selected Rule up or down.

## Loading and Saving Files

To load or save Groups, Characters, and/or Rules, click "File" in the top left corner and select the option you want. They are saved in different files, with Characters in '.chr' files, Groups in '.grpz' files, and Rules in '.rlz' files. It will also give you the option to save your current data when you attempt to close the window.

# Limitations and Future Expansions
- Currently Characters can only be of length 1. Planning to implement to allow for longer characters, allowing for vowel length and simplified affricates.
- Planning to add more possible Rules to allow for more complex processes such as Metathesis.
- Currently cannot recognize word or morpheme boundaries and can only process one word at a time. Intend to expand functionality in that sense.
- All words must be typed manually. Planning to implement a feature to read from a CSV and output to a CSV.
