Bmenu 
=====
_15th January, 2010_

Bmenu is a simple python script that uses the [pygtk](http://www.pygtk.org) library bindings to provide a freestanding menu generated from a simple text file. It allows nested menus to an arbitrary depth, as well as pipe menus in the same way as openbox does. In fact, I wrote it because I missed the Openbox root menu in other window managers (namely [wmii](http://wmii.suckless.org)). It can be bound to a hotkey (using xbindkeys, for example) and called up anywhere. 

Download
--------
You can clone it from github: 
    
    > git clone git://github.com/bricef/bmenu.git bmenu

Or download it using the download button above.

Install/Use
-----------
To install Bmenu, extract the archive and place the bmenu script somewhere appropriate. Then, using your method of choice, bind the script to a mouse or keyboard shortcut. For example to bind Bmenu to [ctrl]+[x] using xbindkeys[^1] add the following to your <code>~/.xbindkeysrc</code>.

	"python /path/to/bmenu.py /path/to/menu.txt"
		Alt + x

To use Bmenu, you'll need a properly formatted menu.txt file.

The menu.txt file
-----------------
The menu file takes its format from the openbox2 menu description format. In it can be described actions, submenus, separators, labels and pipemenus. Only lines that have a valid menu item description are taken into account. The pound '#' sign can also be used to denote a comment, or to comment out a well formed entry. The parser is rather forgiving, and freetext, empty lines, and unknown items will simply be ignored.

In general, each entry takes the form <code>\[action\]\(label\){command.to.execute}</code>. The label will be displayed in the menu, and cannot contain any parenthesis, (I cannot be bothered with adding the neccessary code). If you feel that this would be neccessary, feel free to add it yourself and [let me know](http://bricefernandes.com/contact.html), as I would be happy to add your changes. The command to execute may contain any charater between the curly braces (including curly braces), since the regular expression used is greedy.
 
###Labels and separators.

	[label](Bmenu)
	[separator]

For the label item, a label is required (Duh!) the label will be shown as bold. The separator is a simple horizontal rule, and does not need a label. Neither need commands since they cannot be selected/activated.

###Straightforward action

	[exec]{firefox}
	[exec]{geany}
	[exec](Gmail){chromium --app=http://mail.google.com}
	[exec](term){sakura -f terminal}

The straighforward action begins by <code>[exec]</code> and has both a label and a command field. The label field is optional, and if missing, the text will default to the command itself. Such as 'firefox' and 'geany' in the above example.

###Regular submenus

	[submenu](Net)
		[exec](firefox){firefox}
		[exec](emesene){emesene}
		[submenu](info)	
			[exec](iftop){sakura -f terminal -e "sudo iftop -i wlan0" -h}
		[/submenu]
	[/submenu]

Submenus are delimited by <code>\[submenu\](label)</code> and <code>\[/submenu\]</code> entries. The label is non-optional. Between the beginning and end of a submenu, any correctly formatted entry is acceptable, including other submenus. Submenus can be nested to an arbitrary depth. If some submenus are not appropriately closed the behaviour is undefined (ie: I haven't bothered to test it properly), so check your menu file!

###Pipe Menus

	[pipe-menu](label){/path/to/script}

Piped menus must have both label and command. Omission of either will cause a fatal error. Piped menus are what makes bmenu marginally more useful than [dzen2](http://sites.google.com/site/gotmor/dzen) (with the latest update allowing clickable areas), [9menu](http://pwet.fr/man/linux/commandes/9menu), or [dmenu](http://tools.suckless.org/dmenu/). They allow submenus to be dynamically generated from an external script on mouseover. Whenever the pipe-menu is selected, the command is run in the background, and the output of the command on stdout is parsed for bmenu instructions to create the submenu. Any correctly formated bmenu entry is allowed, even other pipe menus. This for example allows you to have your emails accessible from bmenu, or to use bmenu as a filebrowser. 

<span style="color:#ff0000;font-weight:bold">Warning:</span> If the pipe-menu script takes a long time to execute, bmenu will hang until the script has finished. There is no timeout delay. This would make a great feature to add for version 0.2!

<span style="color:#ff0000;font-weight:bold">Warning:</span> Bmenu does not check stderr when running a script, and anything written to it is discarded permanently.

Ie: It is strongly recommanded that you test your commands before hand, both for the correctness of output statement, as well as for delay problems.

Todo
----
+ Add the ability to pipe menus straight into the root of bmenu (to have a generic popup menu solution)
+ thoroughly document the code and refactor to allow import as module
+ write a man page
+ add it to some source revision
+ package it for Arch and shove it on AUR
+ write a converter to convert to-and-from openbox3 menu files
+ add a pipe menu timeout
+ add a log to keep errors


[^1]: To use xbindkeys, see [here](http://wiki.archlinux.org/index.php/Xbindkeys).
