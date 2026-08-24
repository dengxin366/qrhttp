import argparse
from http.server import HTTPServer, SimpleHTTPRequestHandler
import socket
import sys
import qrcode


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip


def print_qr_code(url):
    qr = qrcode.QRCode()
    qr.add_data(url)
    qr.make(fit=True)
    qr.print_ascii(invert=True)


def main():
    parser = argparse.ArgumentParser(
        description="qrhttp, http.server like server with an QR code in terminal"
    )
    parser.add_argument(
        "port",
        type=int,
        nargs="?",
        default=8000,
        help="Port number (default: 8000)",
    )
    args = parser.parse_args()

    port = args.port
    local_ip = get_local_ip()
    url = f"http://{local_ip}:{port}"

    print("\n" + "=" * 50)
    print(f" Http server running ...")
    print(f" Url: {url}")
    print(f" Please scan after the phone connects the same Wi-Fi：")
    print("=" * 50 + "\n")

    print_qr_code(url)

    print("\nPress Ctrl+C to stop server...\n")

    server_address = ("", port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        sys.exit(0)


if __name__ == "__main__":
    main()