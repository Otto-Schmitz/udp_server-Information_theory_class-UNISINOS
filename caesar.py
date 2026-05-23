"""Cifra de César (implementação manual) e formato de pacote UDP."""
from __future__ import annotations

_PREFIXO = "CAESAR"


def _deslocar_letra(caractere: str, deslocamento: int, cifrar: bool) -> str:
    """Desloca uma letra A–Z ou a–z; devolve o caractere inalterado se não for letra."""
    if "a" <= caractere <= "z":
        base = ord("a")
    elif "A" <= caractere <= "Z":
        base = ord("A")
    else:
        return caractere

    delta = deslocamento % 26
    if not cifrar:
        delta = -delta

    pos = (ord(caractere) - base + delta) % 26
    return chr(base + pos)


def cifrar(texto: str, deslocamento: int) -> str:
    """Aplica a Cifra de César: preserva espaços e caracteres não alfabéticos."""
    return "".join(_deslocar_letra(c, deslocamento, True) for c in texto)


def decifrar(texto: str, deslocamento: int) -> str:
    """Reverte a Cifra de César com a mesma chave usada na cifragem."""
    return "".join(_deslocar_letra(c, deslocamento, False) for c in texto)


def empacotar_caesar(chave: int, mensagem_cifrada: str) -> bytes:
    """Monta o datagrama: CAESAR|<chave>|<texto cifrado> (UTF-8)."""
    corpo = f"{_PREFIXO}|{chave}|{mensagem_cifrada}"
    return corpo.encode("utf-8")


def desempacotar_caesar(pacote: bytes) -> tuple[int, str]:
    """Extrai chave e mensagem cifrada de um pacote CAESAR."""
    texto = pacote.decode("utf-8")
    partes = texto.split("|", 2)
    if len(partes) != 3 or partes[0] != _PREFIXO:
        raise ValueError("pacote CAESAR inválido")
    try:
        chave = int(partes[1])
    except ValueError as e:
        raise ValueError("chave de cifra inválida") from e
    return chave, partes[2]


def eh_pacote_caesar(pacote: bytes) -> bool:
    """Indica se o datagrama usa o protocolo da Cifra de César."""
    return pacote.startswith(f"{_PREFIXO}|".encode("utf-8"))
