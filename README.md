Invisible Unicode Messages
==========================


## Usage

The program works by copying invisible text to the clipboard. You can then paste the message anywhere you want to.
​‍‍​‍​​​​‍‍​​‍​‍​‍‍​‍‍​​​‍‍​‍‍​​​‍‍​‍‍‍‍​​‍​‍‍​​​​‍​​​​​​‍‍‍​‍‍‍​‍‍​‍‍‍‍​‍‍‍​​‍​​‍‍​‍‍​​​‍‍​​‍​​​​‍​​​​‍
	python ium.py --text "hello, world!"
	104 invisible characters copied to the clipboard.

One can, for example, open a new text file (say, `test.txt`) in a text editor and paste the invisible message at some place:

	invisible message here --><-- invisible message here

The program is then able to extract the message back from the text-file:

	python ium.py --decode test.txt
	l.   1 c.  26: hello, world!

Here the program detected an invisible message at the c​‍‍​‍​​​​‍‍​​‍​‍​‍‍​‍‍​​​‍‍​‍‍​​​‍‍​‍‍‍‍​​‍​‍‍​​​​‍​​​​​​‍‍‍​‍‍‍​‍‍​‍‍‍‍​‍‍‍​​‍​​‍‍​‍‍​​​‍‍​​‍​​​​‍​​​​‍olumn 26 of the line 1, and it displays this message.

You can also encode files. But that's gonna generate a lot of invisible characters:

	python ium.py --file tiny_image.png
	19856 invisible characters copied to the clipboard.

Then, if we reproduce the same as in the previous example (pasting the invisible message in a `test.txt`), we can decode the message from this file *to* a file:

	python ium.py --decodef test.txt
	file test.txt.1.26 created

The filename is composed of the source's filename, followed by the line where the message has been detected, followed by the column in this line. If multiple messages are detected, then multiple files are created.

Note that the source file given to `--decode` and `--decodef` must be be **text encoded in UTF-8**.


## How does it work?

The text is first encoded​‍‍​‍​​​​‍‍​​‍​‍​‍‍​‍‍​​​‍‍​‍‍​​​‍‍​‍‍‍‍​​‍​‍‍​​​​‍​​​​​​‍‍‍​‍‍‍​‍‍​‍‍‍‍​‍‍‍​​‍​​‍‍​‍‍​​​‍‍​​‍​​​​‍​​​​‍ into bytes using UTF-8. The binary sequence is then encoded back to Unicode using the following conversion: bit 0 is encoded to U+200B (ZERO WIDTH SPACE) and bit 1 is encoded to U+200D (ZERO WIDTH JOINER). Those are invisible Unicode characters. The Unicode sequence is then copied to the clipboard.

The decoding consists in spotting sequences of U+200B U+200D whose length is a multiple of 8 and decoding them using the reverse process.


## Limitations

 - Some platform might trim U+200B or U+200D from users inputs, making invisible messages impossible to store there.

 - Within an editor, an invisible message can be spotted with the cursor. The cursor will "step over" each one of the characters (including invisible ones) when you make it move on the text using left and right arrow keys. Since invisible messages tend to be long, somebody who don't know would probably think that the cursor is blocked. However, there's a perfectly fine behavior when selecting text.

 - It takes a lot of space. Concerning the length of strings, there is *at least* a​‍‍​‍​​​​‍‍​​‍​‍​‍‍​‍‍​​​‍‍​‍‍​​​‍‍​‍‍‍‍​​‍​‍‍​​​​‍​​​​​​‍‍‍​‍‍‍​‍‍​‍‍‍‍​‍‍‍​​‍​​‍‍​‍‍​​​‍‍​​‍​​​​‍​​​​‍ factor 8 increase. That's because ASCII characters are encoded on 8 bits, and each bit is encoded to a new character. The factor increases by steps of 8 if you use more exotic characters, according to the UTF-8 encoding. Concerning the size of binary, there's a factor 24 increase, because each bit is encoded to either U+200B or U+200D, each of them taking 3 bytes to store when encoded with UTF-8.

 - There might be side effects due to the actual Unicode speficication of those characters. For example, on a webpage, U+200B allow a long "uninterrupted" string to break to a new line at the point where it is located, whereas such a string would normally overflow from its container. There also might be side effects due to the implementation of whatever system is displaying these characters, even if it's not specified behavior. For example, `git diff` will expressly write "U+200B" when spotting one.

 - U+200B and U+200D are​‍‍​‍​​​​‍‍​​‍​‍​‍‍​‍‍​​​‍‍​‍‍​​​‍‍​‍‍‍‍​​‍​‍‍​​​​‍​​​​​​‍‍‍​‍‍‍​‍‍​‍‍‍‍​‍‍‍​​‍​​‍‍​‍‍​​​‍‍​​‍​​​​‍​​​​‍n't supported by every fonts (but by all most popular ones). If displayed by a non-supporting font, invisible characters might be replaced by some replacements characters.

## Acknowledgments

 - [The article](http://www.drlongghost.com/wordpress/food-food/) that inspired this program.

 - The copy to the clipboard is done using the [pyperclip](https://pypi.python.org/pypi/pyperclip) module.

## License

GPLv3