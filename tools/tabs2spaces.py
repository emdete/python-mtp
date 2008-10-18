#!/usr/bin/python
#-------------------------------------------------------------------------------
# Name:        tabs2spaces.py
# Purpose:     Takes one filename as the first argument and converts each tab
#              into the number of spaces specified with the second argument.
#
# Usage:       tabs2spaces.py <filename> <number-of-spaces-per-tab>
#
# Author:      Wayne Koorts
# Website:     http://www.wkoorts.com
# Created:     21/09/2008
# Copyright:   Copyright 2008 Wayne Koorts
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import sys

if len(sys.argv) < 3:
    print "Usage: tabs2spaces.py <filename> <number-of-spaces-per-tab>"
    sys.exit(1)
    
tabs_filename = sys.argv[1]
num_spaces = sys.argv[2]

tabsfree_filename = "notabs_" + tabs_filename
spaces_str = ""
for x in range(0, int(num_spaces)):
    spaces_str = spaces_str + " "

try:
    tabs_file = open(tabs_filename, "r")
except:
    print "Error opening file \"" + tabs_filename + "\""
    print "Chances are you accidentally mis-spelt the name"
    sys.exit(1)

try:
    tabsfree_file = open(tabsfree_filename, "w")
except:
    print "Can't create new file \"" + tabsfree_filename + "\""

sys.stdout.write("Creating tabs-free file... ")
while tabs_file.read(1) != "":
    tabs_file.seek(tabs_file.tell() - 1) # Loop condition already incremented file position
    char = tabs_file.read(1)
    if char == "\t":
        tabsfree_file.write(spaces_str)
    else:
        tabsfree_file.write(char)
sys.stdout.write("done!\n")
        
tabs_file.close()
tabsfree_file.close()

print "Tabs removed successfully!  The new tabs-free file is:"
print tabsfree_filename
