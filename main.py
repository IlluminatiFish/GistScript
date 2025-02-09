import requests, re, time, base64

DISCORD_WEBHOOK_REGEX = re.compile(
    r"(https?:\/\/(ptb\.|canary\.)?discord(app)?\.com\/api\/webhooks\/(\d{18})\/([\w\-]{68}))"
)

BASE64_REGEX = re.compile("^([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{2}==)?")

with open("gists.txt") as f:
    PASTEBINS = f.read().splitlines()


def delete_webhook(webhook: str) -> None:
    with open("404.txt", "r+") as f:
        if webhook in f.read().splitlines():
            return
        f.write(webhook + "\n")
    resp = requests.post(
        webhook,
        json={
            "content": "We are Anonymous. We are Legion. We do not forgive. We do not forget. Expect us.",
            "tts": True,
            "username": "Anonymous via vive la revolution and The Fight Against Malware",
            "avatar_url": "https://cdn.discordapp.com/icons/910733698452815912/8dd25417b5c2a2cf49e1b98a74a15aa8.webp?size=96",
        },
        headers={
            "User-Agent": "AntiMalwareBot/gistscript (+https://discord.gg/TWhrmZFXqb)"
        },
    )
    print(resp)
    print(requests.delete(webhook))


while True:
    for pastebin in PASTEBINS:
        resp = requests.get(
            pastebin,
            headers={
                "User-Agent": "AntiMalwareBot/gistscript (+https://discord.gg/TWhrmZFXqb)"
            },
        )
        if resp.status_code != 200:
            print(f"Error: {resp.status_code} on {pastebin}")
            continue

        oldtext = resp.text
        text = resp.text
        icanhasbase64 = BASE64_REGEX.match(text)
        while (
            icanhasbase64 is not None
            and icanhasbase64.start() == 0
            and icanhasbase64.end() == len(text)
        ):  # screw you, massileQOL
            print(f"Base64 detected on url ({pastebin}), decoding...")
            try:
                text = base64.b64decode(text).decode("utf-8")
            except UnicodeDecodeError as e:
                print("not base64")
                text = oldtext
                break
            print("Decoded: " + text)
            icanhasbase64 = BASE64_REGEX.match(text)

        for webhook in DISCORD_WEBHOOK_REGEX.findall(text):
            delete_webhook(webhook[0])
    time.sleep(5)
