# Cryptography Challenge 2

## Description

Cryptography and bruteforce.

## Requirements 

- rockyou.txt
- john (the ripper)

## Sources

- flag.zip


```
I wanted to send this file to a friend, but I didn't want anyone else to see what's inside it, so I protected it with a pin.
For an extra layer of protection, I also encoded the message in base64.
```


## Exploit

You need to bruteforce 5 lettered pin `(11111)` using a tool like `john (the ripper)`  and the wordlist `rockyou.txt` to access the zipped file. Then, unzip the file and decode the text to see the Flag.

## Solution 

```
sudo zip2john ./flag.zip > hash 
sudo john hash --fork=4 -w=/path/to/rockyou.txt
```