#!/usr/bin/env python3
"""Cliente UDP: menu TUI — Huffman, Elias γ ou Fibonacci."""
import socket

from codec import codificar, empacotar, resolver_modo


def _ler_int(prompt: str, default: int) -> int:
    s = input(f"{prompt} [{default}]: ").strip()
    if not s:
        return default
    try:
        return int(s)
    except ValueError:
        print("  (inválido, mantém o valor anterior)")
        return default


def _normalizar_host(h: str) -> str:
    """`local` não resolve no DNS; tratar como localhost."""
    k = h.strip().lower()
    if k == "local":
        return "localhost"
    return h.strip()


def main() -> None:
    host = "localhost"
    port = 5000
    metodo_str = "huffman"
    modo = resolver_modo(metodo_str)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        while True:
            print()
            print("  ═══ Cliente UDP (teoria da informação) ═══")
            print(f"  Destino: {host}:{port}")
            print(f"  Método:  {metodo_str}")
            print("  ─────────────────────────────────────────")
            print("  1  Usar Huffman")
            print("  2  Usar Elias γ")
            print("  3  Usar Fibonacci")
            print("  4  Definir host")
            print("  5  Definir porta")
            print("  6  Enviar mensagem…")
            print("  0  Sair")
            op = input("\n  Escolha: ").strip()

            if op == "0":
                print("  Até logo.")
                break
            if op == "1":
                metodo_str = "huffman"
                modo = resolver_modo(metodo_str)
                print("  → Huffman")
            elif op == "2":
                metodo_str = "elias"
                modo = resolver_modo(metodo_str)
                print("  → Elias γ")
            elif op == "3":
                metodo_str = "fibonacci"
                modo = resolver_modo(metodo_str)
                print("  → Fibonacci")
            elif op == "4":
                h = input(f"  Host [{host}]: ").strip()
                if h:
                    if h.strip().lower() == "local":
                        print("  (nota: `local` → localhost)")
                    host = _normalizar_host(h)
            elif op == "5":
                port = _ler_int("  Porta", port)
            elif op == "6":
                try:
                    msg = input("  Mensagem: ")
                except EOFError:
                    break
                if not msg.strip():
                    print("  (vazio, ignorado)")
                    continue
                meta, payload, n_bits = codificar(msg, modo)
                pacote = empacotar(modo, meta, payload, n_bits)
                alvo = _normalizar_host(host)
                try:
                    sock.sendto(pacote, (alvo, port))
                except socket.gaierror as e:
                    print(f"  ✗ Não consegui resolver o host {host!r} — use 127.0.0.1 ou localhost. ({e})")
                    continue
                except OSError as e:
                    print(f"  ✗ Erro de rede ao enviar: {e}")
                    continue
                print(f"  ✓ Enviado ({metodo_str}), {len(pacote)} bytes → {alvo}:{port}")
            else:
                print("  Opção desconhecida.")
    finally:
        sock.close()


if __name__ == "__main__":
    main()
