def get_login_user():
    try:
        with open("log.txt", "r", encoding="utf-8") as f:
            for line in reversed(f.readlines()):
                line = line.strip()
                if line.startswith("user="):
                    username = line[len("user="):].strip()
                    if username=="None":
                        return None
                    return username
    except FileNotFoundError:
        return None
    return None
