import os
import urllib.request
from pathlib import Path


README_PATH = Path("README.md")
START = "<!--START_SECTION:waka-->"
END = "<!--END_SECTION:waka-->"
LANGUAGE_LIMIT = 5


def format_duration(total_seconds: float) -> str:
    minutes = round(total_seconds / 60)
    hours, minutes = divmod(minutes, 60)
    if hours and minutes:
        return f"{hours} hr{'s' if hours != 1 else ''} {minutes} mins"
    if hours:
        return f"{hours} hr{'s' if hours != 1 else ''}"
    return f"{minutes} min{'s' if minutes != 1 else ''}"


def progress_bar(percent: float) -> str:
    filled = round(percent / 4)
    return "█" * filled + "░" * (25 - filled)


def main() -> None:
    token = os.environ.get("WAKATIME_API_KEY", "").strip()
    if not token:
        raise RuntimeError("WAKATIME_API_KEY is not configured")

    request = urllib.request.Request(
        "https://wakatime.com/api/v1/users/current/stats/last_7_days",
        headers={
            "Authorization": f"Bearer {token}",
            "User-Agent": "Similarityoung-readme-updater",
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        data = __import__("json").load(response)["data"]

    lines = []
    for language in data["languages"][:LANGUAGE_LIMIT]:
        name = language["name"][:16]
        duration = language["text"][:15]
        percent = language["percent"]
        lines.append(f"{name:<17}{duration:<22}{progress_bar(percent)}   {percent:05.2f} %")

    section = f"{START}\n\n```txt\n" + "\n".join(lines) + f"\n```\n\n{END}"
    readme = README_PATH.read_text(encoding="utf-8")
    start_index = readme.index(START)
    end_index = readme.index(END, start_index) + len(END)
    updated = readme[:start_index] + section + readme[end_index:]
    README_PATH.write_text(updated, encoding="utf-8")


if __name__ == "__main__":
    main()
