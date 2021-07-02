# Web Hacking Challenge 2

## Description

Web Hacking.

## Sources

```
My nephew is a fussy eater and is only willing to eat lime cookies. Any other flavor and he throws a tantrum.
```

## Exploit

You just need to change the cookie value to the base64 value of "lima".

## Solution 

Run the following command on the console.

```
document.cookie = 'flavour=bGltYQ==';
```

Then refresh the website.