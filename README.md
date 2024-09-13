# ec10_RSA

---

Gabriel Mendes Rodrigues Oliveira        081200037

Gabriel Nunes Alves Santos               081200038

Matheus Vinicius Miranda Brito           081200024

Matheus Vital dos Santos de Oliveira     081210042

---

Comunicação Segura com RSA e Sockets
Este projeto demonstra uma comunicação segura entre um cliente e um servidor usando criptografia RSA, implementada em Python com sockets TCP.

Descrição
O sistema funciona da seguinte maneira:

Geração de Chaves RSA: Tanto o cliente quanto o servidor geram suas próprias chaves RSA (pública e privada).
Troca de Chaves: O cliente e o servidor trocam suas chaves públicas para criptografia de mensagens.
Criptografia e Decriptação: O cliente envia uma mensagem criptografada para o servidor usando a chave pública do servidor. O servidor decripta a mensagem usando sua chave privada e envia uma resposta criptografada de volta ao cliente.
Como Funciona
Cliente: Gera um par de chaves RSA, envia sua chave pública ao servidor e criptografa uma mensagem para o servidor.
Servidor: Gera seu próprio par de chaves RSA, recebe a chave pública do cliente, decripta a mensagem recebida e envia uma resposta criptografada.
Instruções de Execução
Servidor: Execute o server.py. O servidor ficará aguardando uma conexão e gerará suas chaves.
Cliente: Execute o client.py. O cliente se conecta ao servidor, realiza a troca de chaves e envia uma mensagem criptografada.
Requisitos
Python 3
Observações
Este projeto é para fins educacionais e não utiliza bibliotecas de criptografia de alto nível.
A comunicação e criptografia foram implementadas usando RSA com chaves de 4096 bits.
