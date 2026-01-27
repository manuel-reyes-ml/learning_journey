import httpx

with httpx.Client() as client:
    response = client.get('http://data.pr4e.org/intro-short.txt')
    # print(response.text) # get the response as one string - library performs the decoding for us

    for line in response.iter_lines(): # get the response as an iterable of lines through the web
        print(line) # decode the line to a string
    print(type(line)) # With httpx, the line is a string (library decodes for us)

# Using requests library (convenient)
"""
import requests

# One line to fetch the data
with requests.get('http://data.pr4e.org/intro-short.txt') as response: # Use 'with'(as context manager) to ensure the response is closed after use
    response.raise_for_status() # Check if the request was successful

    # print(response.text) # get the response as one string - library performs the decoding for us

    for line in response.iter_lines(): # get the response as an iterable of lines through the web  (each line is a bytes object)
        print(line.decode()) # decode the line to a string, also we can use .iter_lines(decode_unicode=True) to decode the line to a string
"""

# Old way to fetch the data (manual socket programming)
"""
import socket

mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mysock.connect(("data.pr4e.org", 80))
cmd = "GET http://data.pr4e.org/intro-short.txt HTTP/1.0\r\n\r\n".encode()
mysock.send(cmd)

while True:
    data = mysock.recv(512)
    if len(data) < 1:
        break
    print(data.decode(), end="")

mysock.close()
"""