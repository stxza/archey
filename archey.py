#!/usr/bin/env python

# Import libraries.
from subprocess import Popen, PIPE

# Define colors.
# Uncomment whatever color scheme you prefer.
clear = "\x1b[0m" # clear [Do NOT comment out]

# color = "\x1b[1;30m" # black
# color2 = "\x1b[0;30m" # black

# color = "\x1b[1;31m" # red 
# color2 = "\x1b[0;30m" # red

# color = "\x1b[1;32m" # green
# color2 = "\x1b[0;32m" # green

# color = "\x1b[1;33m" # yellow
# color2 = "\x1b[0;33m" # yellow

color = "\x1b[1;34m" # blue [Default]
color2 = "\x1b[0;34m" # blue [Default]

# color = "\x1b[1;35m" # magenta
# color2 = "\x1b[0;35m" # magenta

# color = "\x1b[1;36m" # cyan
# color2 = "\x1b[0;36m" # cyan

# color = "\x1b[1;37m" # white
# color2 = "\x1b[0;37m" # white

# Define arrays containing values.
list = []
blank = ['']*10

# Find running processes.
p1 = Popen(['ps', '-A'], stdout=PIPE)
p2 = Popen(["awk", '{print $4}'], stdin=p1.stdout, stdout=PIPE)
processes = p2.communicate()[0].split("\n")

# Print coloured key with normal value.
def output(key, value):
	output = "%s%s:%s %s" % (color, key, clear, value)
	list.append(output)

# Define operating system.
def os_display(): 
	os = "Arch Linux"	
	output('OS', os)

# Define kernel.
def kernel_display():
	kernel = Popen(['uname', '-r'], stdout=PIPE).communicate()[0].rstrip("\n")
	output ('Kernel', kernel)

# Define uptime.
def uptime_display():
	p1 = Popen(['uptime'], stdout=PIPE)
	p2 = Popen(['sed', '-e', 's/^.*up //', "-e", 's/, *[0-9]*.users.*//'], stdin=p1.stdout, stdout=PIPE)
	uptime = p2.communicate()[0].rstrip("\n")
	output ('Uptime', uptime)
	p1 = p2 = None

# Define battery. [Requires: acpi]
def battery_display(): 
	p1 = Popen(['acpi'], stdout=PIPE)
	p2 = Popen(['sed', 's/.*, //'], stdin=p1.stdout, stdout=PIPE)
	battery = p2.communicate()[0].rstrip("\n")
	output ('Battery', battery)

# Define desktop environment. 
def de_display():
	dict = {'gnome-session': 'GNOME',
		'ksmserver': 'KDE',
		'xfce-mcs-manager': 'Xfce'}
	de = 'None found'
	for key in dict.keys():
		if key in processes: de = dict[key]
	output ('DE', de)

# Define window manager.
def wm_display():
        dict = {'awesome': 'Awesome',
		'beryl': 'Beryl',
		'blackbox': 'Blackbox',
		'dwm': 'DWM',
		'enlightenment': 'Enlightenment',
                'fluxbox': 'Fluxbox',
		'fvwm': 'FVWM',
		'icewm': 'icewm',
		'kwin': 'kwin',
		'metacity': 'Metacity',
                'openbox': 'Openbox',
		'wmaker': 'Window Maker',
		'xfwm4': 'Xfwm',
		'xmonad': 'Xmonad'}  
        wm = 'None found'
        for key in dict.keys():
		if key in processes: wm = dict[key]
        output ('WM', wm)

# Define number of packages installed.
def packages_display():
	p1 = Popen(['pacman', '-Q'], stdout=PIPE)
	p2 = Popen(['wc', '-l'], stdin=p1.stdout, stdout=PIPE)
	packages = p2.communicate()[0].rstrip("\n")
	output ('Packages', packages)

# Define root partition information. 
def fs_display():
	# Display root filesystem information. 
	p1 = Popen(['df', '-Th'], stdout=PIPE)
	p2 = Popen(['grep', "/$"], stdin=p1.stdout, stdout=PIPE)
	p3 = Popen(['awk', '{print $4" / "$3}'], stdin=p2.stdout, stdout=PIPE)
	root = p3.communicate()[0].rstrip("\n")
	output ('Root', root)

# Define home partition information.
def home_display():
	# Display home filesystem information.
	p1 = Popen(['df', '-Th'], stdout=PIPE)
	p2 = Popen(['grep', "/home$"], stdin=p1.stdout, stdout=PIPE)
	p3 = Popen(['awk', '{print $4" / "$3}'], stdin=p2.stdout, stdout=PIPE)
	home = p3.communicate()[0].rstrip("\n")
	output ('Home', home)


# Values to display.
# Possible Options [Enabled by default]: os, kernel, uptime, de, wm, packages, fs
# Possible Options [Disabled by default]: battery, home
display = [ 'os', 'kernel', 'uptime', 'de', 'wm', 'packages', 'fs' ]

# Run functions found in 'display' array.
for x in display:
	funcname=x+"_display"
	func=locals()[funcname]
	func()

# Fill 'list' array with with blank keys. [Do NOT remove]
list.extend(blank)

# Result.
print """%s
%s               +                
%s               #                
%s              ###               %s
%s             #####              %s
%s             ######             %s
%s            ; #####;            %s
%s           +##.#####            %s
%s          +##########           %s
%s         ######%s#####%s##;         %s
%s        ###%s############%s+        %s
%s       #%s######   #######        %s
%s     .######;     ;###;`\".      %s
%s    .#######;     ;#####.       %s
%s    #########.   .########`     %s
%s   ######'           '######    %s
%s  ;####                 ####;   
%s  ##'                     '##   
%s #'                         `#  %s                          
""" % (color, color, color, color, list[0], color, list[1], color, list[2], color, list[3], color, list[4], color, list[5], color, color2, color, list[6], color, color2, color, list[7], color, color2, list[8], color2, list[9], color2, list[10], color2, list[11], color2, list[12], color2, color2, color2, clear)

