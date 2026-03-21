#!/usr/bin/env python3
"""Servidor UDP: menu TUI para bind; decodifica Huffman / Elias γ / Fibonacci."""
import socket

from codec import NOME_DO_MODO, decodificar, desempacotar


def _ler_int(prompt: str, default: int) -> int:
    s = input(f"{prompt} [{default}]: ").strip()
    if not s:
        return default
    try:
        return int(s)
    except ValueError:
        print("  (inválido, uso o padrão)")
        return default


def main() -> None:
    print()
    print("  ═══ Servidor UDP (teoria da informação) ═══")
    print("  1  Escutar em localhost:5000 (todas as interfaces)")
    print("  2  Definir interface e porta à mão")
    print("  0  Sair")
    op = input("\n  Escolha: ").strip()

    if op == "0":
        return
    if op == "1":
        host, port = "localhost", 5000
    elif op == "2":
        host = input("  Host/interface [localhost]: ").strip() or "localhost"
        port = _ler_int("  Porta", 5000)
    else:
        print("  Opção desconhecida.")
        return

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, port))
    print(f"\n  À escuta em udp {host}:{port} (Ctrl+C para terminar)\n")

    try:
        while True:
            data, addr = sock.recvfrom(65535)
            try:
                modo, meta, payload, n_bits = desempacotar(data)
                texto = decodificar(modo, meta, payload, n_bits)
                nome = NOME_DO_MODO.get(modo, str(modo))
                print(f"  de {addr} ({nome}): {texto!r}")
            except Exception as e:
                print(f"  de {addr}: erro — {e}")
    except KeyboardInterrupt:
        print("\n  Servidor terminado.")
    finally:
        sock.close()


if __name__ == "__main__":
    main()
