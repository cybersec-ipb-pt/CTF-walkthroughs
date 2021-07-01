import base64

encode = list()
decode = list()
store = str()

message = input(": ")
message_bytes = message.encode('ascii')
base64_bytes = base64.b64decode(message_bytes)
base64_message = base64_bytes.decode('ascii')
print(base64_message)

val = base64_message.split(', ')

for a in val:
    num = int(int(a) - 3)
    encode.append(num)

for b in encode:
    decode.append(chr(b))

for i in range(0, len(decode)):
    store = store + str(decode[i])

print(store)