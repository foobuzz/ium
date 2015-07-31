import argparse, os.path
from pyperclip import pyperclip


ENC = {
	'0': chr(0x200B),
	'1': chr(0x200D)
}

DEC = {
	chr(0x200B): '0',
	chr(0x200D): '1'
}


def get_hidden_string(byts):
	hidden = ''
	for B in byts:
		bits = '{:0>8b}'.format(B)
		for b in bits:
			hidden += ENC[b]
	return hidden


def get_bytes(hstring):
	bits = ''
	for c in hstring:
		bits += DEC[c]
	byts = []
	for i in range(0, len(bits), 8):
		byts.append(int(bits[i:i+8], 2))
	return bytearray(byts)


def find_sequences(line):
	length = len(line)
	i = 0
	while i < length:
		if line[i] in DEC:
			j = i
			while j < length and line[j] in DEC:
				j += 1
			yield (i, j)
			i = j
		else:
			i += 1


def main():
	parser = argparse.ArgumentParser(description="""Invisible Unicode Messages""")
	parser.add_argument('--text')
	parser.add_argument('--file')
	parser.add_argument('--decode')
	parser.add_argument('--decodef')
	args = parser.parse_args()

	from_text = args.text is not None
	from_file = args.file is not None
	to_text = args.decode is not None
	to_file = args.decodef is not None

	if from_text or from_file:
		if from_text:
			encoded = args.text.encode('utf8')
		elif from_file:
			with open(args.file, 'rb') as the_file:
				encoded = the_file.read()
		hidden = get_hidden_string(encoded)
		pyperclip.copy(hidden)
		print('{} invisible characters copied to the clipboard.'.format(len(hidden)))

	elif to_text or to_file:
		sourcef = args.decode if to_text else args.decodef
		with open(sourcef, encoding='utf8') as source:
			for i, line in enumerate(source):
				for start, end in find_sequences(line):
					chunk = line[start:end]
					if len(chunk)%8 == 0:
						clear = get_bytes(chunk)
						if to_text:
							text = clear.decode('utf8', 'replace')
							print('l. {:>3} c. {:>3}: {}'.format(i+1, start, text))
						elif to_file:
							basename = os.path.basename(sourcef)
							filename = '{}.{}.{}'.format(basename, i+1, start)
							with open(filename, 'wb') as output:
								output.write(clear)
							print('file {} created'.format(filename))


if __name__ == '__main__':
	main()