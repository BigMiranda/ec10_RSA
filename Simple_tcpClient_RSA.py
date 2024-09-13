import random
from socket import *

# Funções auxiliares de RSA e criptografia
def miller_rabin(n, k=40):
    if n == 2 or n == 3:
        return True
    if n % 2 == 0 or n < 2:
        return False
    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, s, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def gerar_primo(bits):
    while True:
        num = random.getrandbits(bits)
        if miller_rabin(num):
            return num

def verifica_primo_entre_si(phiN, e):
    while e != 0:
        phiN, e = e, phiN % e
    return phiN == 1

def define_d(phiN, e):
    return pow(e, -1, phiN)

def encrypt(plain_text, public_key):
    e, N = public_key
    return [pow(ord(char), e, N) for char in plain_text]

def decrypt(encrypted_text, private_key):
    d, N = private_key
    return ''.join([chr(pow(char, d, N)) for char in encrypted_text])

# Configuração do socket cliente
serverName = "10.1.70.5"
serverPort = 12500
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

# Geração de chaves RSA
## Gerar primos grandes para garantir um N de 4096 bits
print("Etapa 1: Gerando os números primos p e q.")

p = gerar_primo(2048)
print("p: ", p)

q = gerar_primo(2048)
print("q: ", q)

print("Etapa 2: Calculando N = p * q.")
N = p * q  # Calcula N
print("N: ", N)

print("Etapa 3: Calculando φ(N) = (p-1) * (q-1).")
phiN = (p - 1) * (q - 1)  # Calcula phi(N)
print("phiN: ", phiN)

e = 65537
print("e: ", e)

if not verifica_primo_entre_si(phiN, e):
    raise Exception("phiN e e não são primos entre si")

print(f"Etapa 4: Calculando a chave privada d.")
## Calcula d
d = define_d(phiN, e)
print("d: ", d)


# Exibir as chaves geradas
print("Chaves geradas com sucesso:")
print(f"p: {p}")
print(f"q: {q}")
print(f"N (4096 bits): {N}")
print(f"phi(N): {phiN}")
print(f"e (chave pública): {e}")
print(f"d (chave privada): {d}")


public_key = (e, N)
private_key = (d, N)

print(" ")
print(" ")
print(" ")
print(" ")

# Envia chave pública para o servidor
clientSocket.send(bytes(str(public_key), "utf-8"))

# Recebe chave pública do servidor
server_public_key = eval(clientSocket.recv(65000).decode("utf-8"))

# Teste de criptografia e envio
sentence = "Segurança de informações é essencial.".upper()
encrypted_text = encrypt(sentence, server_public_key)
clientSocket.send(bytes(str(encrypted_text), "utf-8"))

# Recebe resposta do servidor e descriptografa
encrypted_response = eval(clientSocket.recv(65000).decode("utf-8"))
decrypted_response = decrypt(encrypted_response, private_key)

print("\nTexto original:", sentence)
print("Texto criptografado enviado:", encrypted_text)
print("\nRetorno do server:", decrypted_response)

input("Pressione Enter para sair...")

clientSocket.close()
