#https://www.codewars.com/kata/whats-in-a-name/train/python
import re
def name_in_str(str, substr):
    return re.compile(".*" + ".*".join(list(substr)) + ".*", re.IGNORECASE).match(str) <> None;


print name_in_str("Across the rivers", "chris")
