# Capture The Flag Challenge 3

## Description

Capture The Flag.

## Sources

```
Explore and discover possible vulnerabilities of the machine to gain access and capture the Flags.
```

## Exploit

Begin by enumerating the IP. 

```
sudo nmap -sC -sV -A -p- <IP> -T5 -oA Alfa
```

Using `nmap` we discover that port 21 is opened and 139–445 too, so let’s enumerate this ports.

```
ftp <IP>
```

Using the `anonymous` user and `blank` password we gain access to the ftp server. Inside it we discover a directory name thomas, wich contains a file named milo.jpg.

Download the file to your machine, and we find it's a photo of a Dog, maybe of Thomas.

```
get milo.jpg
```

Now let’s enumerate `samba`.

```
enum4linux -a -r <IP>
```

That confirms that user “thomas” is the local user. So now lets access the webpage and see if we can get anything else.

First thing to do is check if a robots.txt exists.
We find a listing of directories and at the bottom of the page, we find a brainfuck.

Using a brainfuck decoder we discover a directory /alfa-support.

When we access it, we can see a conversation beaten Thomas and Alfa IT Support.

Thomas says that he lost the password, and the password contain the name of his pet followed by 3 numerical digits.

With the information we gather before, we know it's pet is named milo, now we need to create the wordlists to brute-force port ssh 65111.

Using `cruch` we generate the wordlists.

```
crunch 7 7 1234567890 -t milo@@@ -o wordlists
```

Now that we have the worldists, let’s bruteforce port ssh using `hydra`.

```
hydra -l thomas -P wordlists ssh://<IP>:65111 -t 64
```

Bruteforce done, and now we can access the machine using the credentials we discovered.

```
[65111][ssh] host: <IP>   login: thomas   password: milo666
```

Inside the machine we discover a `.remote_secret` file which needs root privileges to run. The file is certainly editable, but it is not convenient because there is something inside, such as an encrypted password.

We check the services running, and we can see that the localhost is running as root and has a port 5901.

```
ss -tlpn
```

Now let’s try tunneling to that door with the following command.

```
ssh -L 5901:127.0.0.1:5901 thomas@<IP> -p 65111
```

Now in our terminal we can try to see if this port 5901 is really opened.

```
sudo nmap 127.0.0.1
```

It’s is!!! The command `lsof` confirms that the tunnel is established.

```
lsof -i:5901
```

Now we can try with `VNC` to log as a root with the file `.remote_secret` that contain the encrypted password.

```
vncviewer -passwd .remote_secret localhost:5901
```

AND WE ARE ROOT!!