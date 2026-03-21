"""Huffman, Elias γ e Fibonacci (Zeckendorf + terminador 11). Stdlib apenas."""
from __future__ import annotations

from collections import Counter
from heapq import heappush, heappop
from typing import Dict, Tuple

# --- Huffman -----------------------------------------------------------------

Tree = Tuple[int, int, object]  # (freq, id, filho...) — folha ou nó interno


def huffman_frequencias(texto: str) -> Dict[str, int]:
    return dict(Counter(texto))


def huffman_montar_arvore(freq: Dict[str, int]) -> Tree | None:
    if not freq:
        return None
    heap: list[Tree] = []
    for i, (ch, c) in enumerate(sorted(freq.items())):
        heappush(heap, (c, i, ch))
    prox_id = len(freq)
    while len(heap) > 1:
        a = heappop(heap)
        b = heappop(heap)
        heappush(heap, (a[0] + b[0], prox_id, a, b))
        prox_id += 1
    return heap[0]


def huffman_gerar_codigos(no: Tree | None, prefixo: str = "", t: Dict[str, str] | None = None) -> Dict[str, str]:
    if t is None:
        t = {}
    if no is None:
        return t
    if len(no) == 3 and isinstance(no[2], str):
        t[no[2]] = prefixo if prefixo else "0"
        return t
    _, _, esq, dir_ = no  # type: ignore[misc]
    huffman_gerar_codigos(esq, prefixo + "0", t)
    huffman_gerar_codigos(dir_, prefixo + "1", t)
    return t


def bits_para_bytes(bits: str) -> Tuple[bytes, int]:
    n = len(bits)
    pad = (8 - n % 8) % 8
    bits = bits + "0" * pad
    out = bytearray()
    for i in range(0, len(bits), 8):
        out.append(int(bits[i : i + 8], 2))
    return bytes(out), n


def bytes_para_bits(dados: bytes, n_bits: int) -> str:
    s = "".join(f"{b:08b}" for b in dados)
    return s[:n_bits]


def huffman_decodificar(bits: str, raiz: Tree | None) -> str:
    if raiz is None:
        return ""
    if len(raiz) == 3 and isinstance(raiz[2], str):
        return raiz[2] * len(bits) if bits else ""
    saida: list[str] = []
    no: Tree | None = raiz
    for b in bits:
        if no is None or len(no) != 4:
            break
        _, _, esq, dir_ = no  # type: ignore[misc]
        no = esq if b == "0" else dir_
        if len(no) == 3 and isinstance(no[2], str):
            saida.append(no[2])
            no = raiz
    return "".join(saida)


# --- Fibonacci: sequência em cache -------------------------------------------

# Sequência Zeckendorf 1, 2, 3, 5, … — cresce uma vez e reutiliza-se (sob demanda).
_FIB: list[int] = [1, 2]


def _ensure_fib_length(tamanho: int) -> None:
    """Garante len(_FIB) >= tamanho (adiciona termos só quando falta)."""
    while len(_FIB) < tamanho:
        _FIB.append(_FIB[-1] + _FIB[-2])


def _fib_linha_para_codificar(n: int) -> list[int]:
    """Prefixo mínimo [1,2,…] com último termo >= n (igual ao algoritmo antigo)."""
    _ensure_fib_length(2)
    i = 1
    while _FIB[i] < n:
        i += 1
        _ensure_fib_length(i + 1)
    return _FIB[: i + 1]


def elias_gamma_codificar(n: int) -> str:
    if n < 1:
        raise ValueError("Elias γ exige n >= 1")
    b = bin(n)[2:]
    return "0" * (len(b) - 1) + b


def elias_gamma_extrair(bits: str) -> tuple[int, str]:
    i = 0
    while i < len(bits) and bits[i] == "0":
        i += 1
    if i >= len(bits):
        raise ValueError("fluxo Elias truncado")
    k = i
    fim = i + k + 1
    if fim > len(bits):
        raise ValueError("fluxo Elias truncado")
    n = int(bits[i:fim], 2)
    return n, bits[fim:]


def elias_gamma_codificar_sequencia(numeros: list[int]) -> str:
    return "".join(elias_gamma_codificar(n) for n in numeros)


def elias_gamma_decodificar_sequencia(bits: str) -> list[int]:
    out: list[int] = []
    resto = bits
    while resto:
        n, resto = elias_gamma_extrair(resto)
        out.append(n)
    return out


def fibonacci_codificar(n: int) -> str:
    if n < 1:
        raise ValueError("Fibonacci exige n >= 1")
    fib = _fib_linha_para_codificar(n)
    c = [0] * len(fib)
    r = n
    i = len(fib) - 1
    while i >= 0:
        if fib[i] <= r:
            c[i] = 1
            r -= fib[i]
            i -= 2
        else:
            i -= 1
    while c and c[-1] == 0:
        c.pop()
    if not c:
        c = [1]
    return "".join(str(x) for x in c) + "11"


def _zeckendorf_corpo_para_int(corpo: str) -> int:
    if not corpo:
        return 0
    L = len(corpo)
    _ensure_fib_length(L)
    return sum(int(b) * _FIB[k] for k, b in enumerate(corpo))


def fibonacci_extrair_um(bits: str) -> tuple[int, str]:
    """Um código termina em 11; o corpo (antes do 11) não contém 11 (Zeckendorf)."""
    n = len(bits)
    j = 3
    while j <= n:
        if bits[j - 2 : j] != "11":
            j += 1
            continue
        corpo = bits[: j - 2]
        if "11" in corpo:
            j += 1
            continue
        val = _zeckendorf_corpo_para_int(corpo)
        if val < 1:
            j += 1
            continue
        if fibonacci_codificar(val) != bits[:j]:
            j += 1
            continue
        return val, bits[j:]
    raise ValueError("terminador Fibonacci ausente ou fluxo truncado")


def fibonacci_codificar_sequencia(numeros: list[int]) -> str:
    return "".join(fibonacci_codificar(n) for n in numeros)


def fibonacci_decodificar_sequencia(bits: str) -> list[int]:
    out: list[int] = []
    resto = bits
    while resto:
        n, resto = fibonacci_extrair_um(resto)
        out.append(n)
    return out
