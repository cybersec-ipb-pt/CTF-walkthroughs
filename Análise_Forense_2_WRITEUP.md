# Forensic Analysis Challenge 2

## Description

Forensic analysis.

## Requirements 

- Teler

## Sources

- analise_forense_2.txt

```
A system maintained by IPB, was the target of multiple attacks. Analyze the log and discover the timestamp in which the "Command Injection" attack occurred.
```

## Exploit

By analyzing the given file, the Flag can be found on the following log entry:

```
"192.168.4.25 - - [22/Dec/2016:16:31:51 +0300] "GET /index.php?arg=8.8.8.8;system('id') HTTP/1.1" 500 1983 "-" "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.21 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.21""
```
