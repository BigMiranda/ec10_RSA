import random
from socket import *

# Funções auxiliares de RSA e criptografia
def miller_rabin(n, k=40):
    """Teste de primalidade de Miller-Rabin para verificar se o número é primo."""
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
    """Gera um número primo de 'bits' bits de forma aleatória."""
    while True:
        num = random.getrandbits(bits)
        if miller_rabin(num):
            return num

def verifica_primo_entre_si(phiN, e):
    """Verifica se 'phiN' e 'e' são primos entre si (máximo divisor comum == 1)."""
    while e != 0:
        phiN, e = e, phiN % e
    return phiN == 1

def define_d(phiN, e):
    """Calcula o inverso multiplicativo de 'e' mod 'phiN', que será a chave privada 'd'."""
    return pow(e, -1, phiN)

def encrypt(plain_text, public_key):
    """Criptografa o texto plano usando a chave pública (e, N)."""
    e, N = public_key
    return [pow(ord(char), e, N) for char in plain_text]

def decrypt(encrypted_text, private_key):
    """Decripta o texto criptografado usando a chave privada (d, N)."""
    d, N = private_key
    return ''.join([chr(pow(char, d, N)) for char in encrypted_text])

# Configuração do socket servidor
serverPort = 12500
serverSocket = socket(AF_INET, SOCK_STREAM)  # Define o tipo de socket (TCP)
serverSocket.bind(("", serverPort))  # Associa o socket à porta definida
serverSocket.listen(1)  # Aguarda conexões, permitindo até 1 cliente na fila
print("Servidor TCP aguardando conexão...")

connectionSocket, addr = serverSocket.accept()  # Aceita conexão de um cliente
print(f"Conexão estabelecida com: {addr}")

# Geração de chaves RSA do servidor
## Gerar primos grandes para garantir um N de 4096 bits
print("Etapa 1: Gerando os números primos p e q.")
p = gerar_primo(2048)  # Gera o primo p de 2048 bits
print("p: ", p)

q = gerar_primo(2048)  # Gera o primo q de 2048 bits
print("q: ", q)

print("Etapa 2: Calculando N = p * q.")
N = p * q  # Calcula N (parte da chave pública e privada)
print(f"N: {N}")

print("Etapa 3: Calculando φ(N) = (p-1) * (q-1).")
phiN = (p - 1) * (q - 1)  # Calcula phi(N)
print(f"phi(N): {phiN}")

# Define o valor de 'e' (comum: 65537) e verifica se 'e' e 'phiN' são primos entre si
e = 65537
if not verifica_primo_entre_si(phiN, e):
    raise Exception("phiN e e não são primos entre si")

print("Etapa 4: Calculando a chave privada d.")
d = define_d(phiN, e)  # Calcula o valor de d, chave privada
print(f"d: {d}")


# Exibir as chaves geradas
print("Chaves geradas com sucesso:")
print(f"p: {p}")
print(f"q: {q}")
print(f"N (4096 bits): {N}")
print(f"phi(N): {phiN}")
print(f"e (chave pública): {e}")
print(f"d (chave privada): {d}")

print(" ")

# Exibe as chaves geradas
print("Chaves RSA geradas:")
print(f"Chave pública (e, N): ({e}, {N})")
print(f"Chave privada (d, N): ({d}, {N})")

# Define as chaves pública e privada
public_key = (e, N)
private_key = (d, N)

print(" ")
print(" ")
print(" ")
print(" ")

# Recebe chave pública do cliente
client_public_key = eval(connectionSocket.recv(650000000).decode("utf-8"))
print(f"Chave pública recebida do cliente: {client_public_key}")

# Envia a chave pública do servidor ao cliente
connectionSocket.send(bytes(str(public_key), "utf-8"))

# Recebe mensagem criptografada do cliente
encrypted_message = eval(connectionSocket.recv(650000000).decode("utf-8"))
print(f"Mensagem criptografada recebida: {encrypted_message}")

# Decripta a mensagem usando a chave privada do servidor
decrypted_message = decrypt(encrypted_message, private_key)
print(f"Mensagem decriptografada: {decrypted_message}")

# Resposta ao cliente (criptografa uma resposta com a chave pública do cliente)
response = "Mensagem recebida com sucesso.".upper()
encrypted_response = encrypt(response, client_public_key)

# Envia a resposta criptografada ao cliente
connectionSocket.send(bytes(str(encrypted_response), "utf-8"))

# Fecha a conexão
input("Pressione Enter para sair...")

connectionSocket.close()
