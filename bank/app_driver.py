from server import HTTPServer


def main():
    server = HTTPServer('127.0.0.1', 8080)
    server.run_server()


if __name__ == '__main__':
    main()
