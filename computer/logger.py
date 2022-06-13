class Logger:
    def error(self, msg: str) -> None:
        print(f"[Error] {msg}")

    def info(self, msg: str) -> None:
        print(f"[Info] {msg}")

    def success(self, msg: str) -> None:
        print(f"[Success] {msg}")
