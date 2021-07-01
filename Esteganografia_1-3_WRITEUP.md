# Steganography Challenges 1 to 3

## Description

Steganography.

## Requirements 

- Outguess
- Steghide
- Cloacked-pixel

## Sources

- JPEG.jpg
- AUDIO.wav
- PNG.png

```
The Flags have been hidden inside these files, can you find them?
```

## Exploit

Different steganography tools were used to embed the Flags inside the files.

`Outguess` was used for the `JPEG`, `Steghide` for the `AUDIO` and `Cloacked-pixel` for the `PNG`.

You need to use steganography tools that allow to pass the passphrase.

The passphrase is the content of the files.

The Flags were also encode using `Base64` for the `JPEG` and `AUDIO`, and `Rot13` for the `PNG`.


## Solution 


+ JPEG

```
Creation - outguess -k 1n_7h3_l16h7! -d secret_message.txt ORIGINAL.jpg stego.jpg

Solution - outguess -r -k 1n_7h3_l16h7! stego.jpg output.txt
```

+ WAV

```
Creation - ffmpeg -loglevel panic -i ORIGINAL.mp3 -flags bitexact ORIGINAL.wav
		   steghide embed -f -ef secret_message.txt -cf ./ORIGINAL.wav -p checkmate -sf ./steghide.wav

Solution - steghide extract -sf steghide.wav -p checkmate -xf output.txt
```

+ PNG

```
Creation - cloackedpixel hide ORIGINAL.png secret_message.txt d0n7_7ru57_m3

Solution - cloackedpixel extract ORIGINAL.png-stego.png output.txt d0n7_7ru57_m3
```