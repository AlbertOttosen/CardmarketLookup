Overview
--------

This is a tool for quickly assessing an estimated price on a list of cards. 


User guide
----------

Add a file "buylist.txt" to the same directory as the "cardLookup.py" script. 
Write a list of cardnames and quantities on the format:

<amount> [cardname]

Examples:
---------

4x Snapcaster Mage
2 tarmogoyf

See example buylist file for additional reference.


Technical details
-----------------
The tool uses webscrabing on cardmarket.com to fetch price trends. 
It makes use of a thread pool to reduce the big delay when querying one card at a time.