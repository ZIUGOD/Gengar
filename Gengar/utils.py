import os
from datetime import datetime, timedelta
from mastodon import Mastodon
from dotenv import load_dotenv
from time import sleep

load_dotenv()


class System:
    def clear(self) -> None:
        """Clears the terminal"""
        os.system("cls" if os.name == "nt" else "clear")

    def write_log(self, *values: object) -> None:
        """
        Writes a log message to a file named with the current date.
        Args:
            *values (object): Variable length argument list of values to be logged.
        """

        log_message = " ".join(str(value) for value in values)
        if not os.path.exists("logs/"):
            os.mkdir("logs/")

        new_folder_name = f"{datetime.today().strftime('%Y-%m')}/"

        if not os.path.exists(f"logs/{new_folder_name}"):
            os.mkdir(f"logs/{new_folder_name}")

        log_file_path = f"logs/{new_folder_name}{datetime.today().strftime('%d')}.log"

        with open(log_file_path, "a") as file:
            file.write(f"{datetime.now().strftime('%H:%M:%S')} - {log_message}\n")


class Bot:
    def __init__(self):
        self.system = System()
        self.mastodon = Mastodon(
            os.getenv("CLIENT_KEY"),
            os.getenv("CLIENT_SECRET"),
            os.getenv("ACCESS_TOKEN"),
            api_base_url="https://mastodon.social",
        )

    def get_seconds_until_next_interval(self) -> int:
        current_time = datetime.now()

        if current_time.minute != 0:
            next_time = current_time.replace(
                hour=current_time.hour + 1, minute=0, second=0, microsecond=0
            )

        else:
            next_time = (current_time + timedelta(hours=1)).replace(
                minute=0, second=0, microsecond=0
            )
        seconds_until_next_interval = (next_time - current_time).total_seconds()
        return int(seconds_until_next_interval)

    def create_toot(self, _content: str | None = None) -> None:
        if _content is None:
            self.system.write_log("The bot received an empty toot content. Aborting.")
            return

        if len(_content) > 500:
            self.system.write_log(
                "The bot received a toot content that is too long (> 500). Aborting."
            )
            return

        try:
            self.mastodon.status_post(_content)
            self.system.write_log(f"A new toot was sent: {_content}.")

        except Exception as error:
            self.system.write_log(f"Error: {error}")

    def start(self):
        self.system.write_log("Starting bot in Mastodon.")
        while True:
            current_time = datetime.now()
            if current_time.minute == 0 or current_time.minute == 30:
                self.create_toot("This is a scheduled toot.")

                wait_time = self.get_seconds_until_next_interval()

                self.system.write_log(f"Bot slept for {wait_time} seconds.")

                sleep(wait_time)

                self.system.write_log(f"Bot woke up at {datetime.now()}")

            else:
                wait_time = self.get_seconds_until_next_interval()

                self.system.write_log(f"Bot slept for {wait_time} seconds.")

                sleep(wait_time)

                self.system.write_log(f"Bot woke up at {datetime.now()}")
