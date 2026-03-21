# Information Theory Lab — UDP messaging

## English

**Course:** *Teoria da Informação: Compressão e Criptografia* (Information Theory: Compression and Cryptography)  
**Instructor:** Elvandi da Silva Junior  
**Institution:** UNISINOS (Universidade do Vale do Rio dos Sinos), Brazil  

### Context

This repository is **coursework** for the class above. The subject covers both **compression** and **cryptography**; **this project focuses on the compression / source-coding side** in a small networked demo.

A **UDP client** and **UDP server** are implemented in Python using the **`socket`** API. The client selects a coding method from a text menu, types a message, and sends a **single datagram** per message. The server receives the packet, reads a small binary header (method + metadata + bit length), and **reconstructs the original text**—i.e. it **decodes** what the client **encoded**.

**Methods implemented (lossless source codes, not block ciphers):**

- **Huffman** coding (frequencies + tree)  
- **Elias γ** on symbol ranks in the sorted alphabet  
- **Fibonacci (Zeckendorf)** coding on those same ranks  

So the “encoding / decoding” here is **data compression / representation**, not AES-style encryption. In loose coursework language, people sometimes say “encrypt/decrypt” for *any* reversible transform before the wire; here that transform is **source coding** (the message is not sent as plain text bits of UTF-8, but as a compressed bitstream the server **reverses**). If the syllabus also requires classical **encryption**, that would be an additional layer on top of this pipeline.

### How to run

1. Start the server: `python3 server.py` — choose bind options from the menu.  
2. Start the client: `python3 client.py` — set host/port and method, then send messages.  

Requirements: Python 3.10+ (stdlib only).

---

## Português

**Disciplina:** Teoria da Informação: Compressão e Criptografia  
**Professor:** Elvandi da Silva Junior  
**Instituição:** UNISINOS (Universidade do Vale do Rio dos Sinos)  

### Contexto

Este repositório é um **trabalho / laboratório** da disciplina citada. A matéria trata de **compressão** e de **criptografia**; **neste projeto, o foco prático é a parte de compressão e códigos de fonte**, demonstrada em rede.

Há um **cliente** e um **servidor** que comunicam por **UDP**, em **Python**, usando **`socket`**. No cliente, um **menu em texto (TUI)** permite escolher o método, configurar host/porta e **enviar mensagens** (um **datagrama** por mensagem). No servidor, o pacote é **recebido**, o cabeçalho é interpretado (método, metadados, número de bits úteis) e o texto original é **recuperado** — ou seja, o servidor **decodifica** o que o cliente **codificou**.

**Métodos implementados (codificação sem perdas, não são cifras como AES):**

- **Huffman** (frequências e árvore)  
- **Elias γ** aplicado aos **ranks** dos símbolos no alfabeto ordenado  
- **Fibonacci (Zeckendorf)** nos mesmos ranks  

Assim, “codificar / decodificar” aqui é **compressão / códigos de fonte** (Teoria da Informação). Em linguagem informal de trabalhos, às vezes se fala em **“criptografar” e “decriptografar”** para qualquer transformação reversível antes de enviar; neste projeto, a mensagem **não segue em texto claro na carga útil** no sentido óbvio: vai **codificada em bits** (Huffman, Elias γ ou Fibonacci) e o servidor **reverte essa codificação** para recuperar o texto. **Criptografia** no sentido forte (ex.: AES, sigilo contra adversário) não está implementada aqui; se o enunciado exigir isso, seria uma **camada adicional** sobre este fluxo.

### Como executar

1. Servidor: `python3 server.py` — opções de escuta no menu.  
2. Cliente: `python3 client.py` — definir destino e método, depois enviar mensagens.  

Requisito: Python 3.10+ (apenas biblioteca padrão).
