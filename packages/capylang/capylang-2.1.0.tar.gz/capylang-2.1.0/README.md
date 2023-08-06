# Capylang
### Capylang is a pretty simple language.
### Regular Examples
```python
from capylang import capy
mycapy = capy(id="MyCapy",printinst=True) # ID is for identification of Capylang Instances, and printinst prints the ID
print(mycapy.__doc__) # Returns help
a = 4
b = 3
print(str(mycapy.add(a,b))) # Prints 7 (also uses the add function)
print(str(mycapy.minus(a,b))) # Prints 1 (also uses the subtract function)
print(str(mycapy.multi(a,b))) # Prints 12 (also uses the multiply function)
print(str(mycapy.div(a,b))) # Prints 2.3 (average, also uses the divide function)
print(str(mycapy.hyp(a,b))) # It returns the hypotenuse of opp, and adj
print(str(mycapy.opp(a,b))) # Try this yourself for more info, check mycapy.__doc__
print(str(mycapy.adj(a,b))) # Try this yourself for more info, check mycapy.__doc__
```
### Decorators (Make your own Capylang if you feel lazy or want to!)
```python
import capylang
@capylang.decorators.add # Equivalent to mycapy.add
def myadd(a,b,c):
  return a,b,c # The decorator does it all for ya.

print(myadd(1,2,3))
# Basicallly everything above. Add, minus, multi, div, hyp, opp, and adj. Fibonacci is here.
```
### DateTime alternative
```python
import capylang
date = "1/16/1921" # MM/DD/YYYY (January 16th 1921)
mydate = capylang.date.new(date)
print(mydate)
print(mydate.text())
#
```
### Clearing on Terminals
```python
import capylang
capylang.terminal.os_clear() # Clear with the os module
capylang.terminal.replit_clear() # Clear with the replit module
```
### Fibonacci Sequence
```python
from capylang import capy
# The fibonacci sequence function returns numbers in the fibonacci sequence, it contains 2 args:
# num_of_nums: the number of sequence numbers you'd like to generate (required)
# index: to return a specific number in the sequence (optional)
fibo = capy(printinst=True,id="Fibonacci Sequence")
print(fibo.nacci(num_of_nums=10,index=6))
```
### Math string evaluation
```python
# Coming in decorators soon.
from capylang import capy
eval = capy(printinst=True,id="Evaluation")
print(eval.calc("6/2*(1+2)")) # 9
```
### Old, used to be deprecated, but revived capy.log
```python
# Coming in decorators soon.
from capylang import capy
eval = capy(printinst=True,id="Evaluation")
eval.log("The prophecy is true!!!")
```
### Did you know you could use "deprecated" syntax?
```python
from capylang import capy
capy.log("You don't even need to initialize the module!")
```
### String occurrences
```python
import capylang

mystr = "I am an Apple."
mystr = capylang.string.init(mystr)
print(mystr.freq()["Apple."])
```
### String occurrences to lower
```python
import capylang

mystr = "I am an Apple."
mystr = capylang.string.init(mystr)
print(mystr.lowfreq()["apple."])
```
### Binary searching in an array
```python
import capylang
hi = [1,3,5,7,9]
print(capylang.capi.binary_search(hi,3)) # Returns the index of 3 in hi. Otherwise, returns None.
print(capylang.capi.binary_search(hi,-1)) # Returns None because -1 is not in the array.
```
### Color sets
```python
import capylang
print(capylang.color.set["classic"]) # ROYGBP
print(capylang.color.set["full"]) # ROYGBIV
print(capylang.color.set["full_bip"]) # ROYGBIP
# Useful for color sorting.
```
### That's pretty much it for a basic tutorial of Capylang.