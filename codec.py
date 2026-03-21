"""União Huffman / Elias γ / Fibonacci + formato de pacote UDP."""
from __future__ import annotations

import json
import struct
from typing import Any, Dict, Tuple

from inteiro_codigos import (
    bits_para_bytes,
    bytes_para_bits,
    elias_gamma_codificar_sequencia,
    elias_gamma_decodificar_sequencia,
    fibonacci_codificar_sequencia,
    fibonacci_decodificar_sequencia,
    huffman_decodificar,
    huffman_frequencias,
    huffman_gerar_codigos,
    huffman_montar_arvore,
)

MODE_HUFFMAN = 0
MODE_ELIAS_GAMMA = 1
MODE_FIBONACCI = 2

NOME_DO_MODO = {
    MODE_HUFFMAN: "huffman",
    MODE_ELIAS_GAMMA: "elias_gamma",
    MODE_FIBONACCI: "fibonacci",
}

_MODOS_NOME = {
    "huffman": MODE_HUFFMAN,
    "elias": MODE_ELIAS_GAMMA,
    "gamma": MODE_ELIAS_GAMMA,
    "elias_gamma": MODE_ELIAS_GAMMA,
    "fibonacci": MODE_FIBONACCI,
    "fib": MODE_FIBONACCI,
}


def resolver_modo(nome: str) -> int:
    k = nome.strip().lower().replace("-", "_")
    if k not in _MODOS_NOME:
        raise ValueError(f"método desconhecido: {nome!r} (use huffman, elias, fibonacci)")
    return _MODOS_NOME[k]


def _alfabeto_ranks(texto: str) -> Tuple[list[str], Dict[str, int]]:
    chars = sorted(set(texto))
    rank = {ch: i + 1 for i, ch in enumerate(chars)}
    return chars, rank


def codificar(texto: str, modo: int) -> Tuple[Dict[str, Any], bytes, int]:
    if not texto:
        meta: Dict[str, Any] = {"alphabet": []} if modo != MODE_HUFFMAN else {}
        return meta, b"", 0

    if modo == MODE_HUFFMAN:
        freq = huffman_frequencias(texto)
        raiz = huffman_montar_arvore(freq)
        codigos = huffman_gerar_codigos(raiz)
        fluxo = "".join(codigos[ch] for ch in texto)
        payload, n_bits = bits_para_bytes(fluxo)
        return freq, payload, n_bits

    _, rank = _alfabeto_ranks(texto)
    nums = [rank[ch] for ch in texto]
    if modo == MODE_ELIAS_GAMMA:
        fluxo = elias_gamma_codificar_sequencia(nums)
    else:
        fluxo = fibonacci_codificar_sequencia(nums)
    payload, n_bits = bits_para_bytes(fluxo)
    chars, _ = _alfabeto_ranks(texto)
    return {"alphabet": chars}, payload, n_bits


def decodificar(modo: int, meta: Dict[str, Any], payload: bytes, n_bits: int) -> str:
    if not payload and n_bits == 0:
        return ""
    bits = bytes_para_bits(payload, n_bits)

    if modo == MODE_HUFFMAN:
        raiz = huffman_montar_arvore(meta)  # meta é o mapa de frequências
        return huffman_decodificar(bits, raiz)

    alfabeto: list[str] = meta.get("alphabet", [])
    if not alfabeto:
        return ""
    inv = {i + 1: ch for i, ch in enumerate(alfabeto)}

    if modo == MODE_ELIAS_GAMMA:
        nums = elias_gamma_decodificar_sequencia(bits)
    else:
        nums = fibonacci_decodificar_sequencia(bits)

    return "".join(inv[r] for r in nums)


def empacotar(modo: int, meta: Dict[str, Any], payload: bytes, n_bits: int) -> bytes:
    j = json.dumps(meta, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    return struct.pack("!BII", modo, len(j), n_bits) + j + payload


def desempacotar(pacote: bytes) -> Tuple[int, Dict[str, Any], bytes, int]:
    modo, lj, n_bits = struct.unpack("!BII", pacote[:9])
    j = pacote[9 : 9 + lj]
    payload = pacote[9 + lj :]
    meta = json.loads(j.decode("utf-8"))
    return modo, meta, payload, n_bits
