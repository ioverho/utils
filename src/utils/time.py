import datetime
import typing


def get_timestamp() -> str:
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    return timestamp


class Timer:
    def __init__(self) -> None:
        self.start = datetime.datetime.now()

    def time(
        self, format: typing.Literal["seconds", "microseconds", "str"] = "seconds"
    ) -> float | int | str:
        end = datetime.datetime.now()

        delta = end - self.start

        if format == "str":
            total_seconds = delta.total_seconds()

            if total_seconds > 1:
                days, remainder = divmod(total_seconds, 60 * 60 * 24)
                hours, remainder = divmod(remainder, 60 * 60)
                minutes, seconds = divmod(remainder, 60)

                output = ""
                if days > 0:
                    output += f"{days} days, "

                if hours > 0 or (days > 0):
                    output += f"{hours} hours, "

                if minutes > 0 or (days > 0) or (hours > 0):
                    output += f"{minutes} minutes, "

                output += f"{seconds:.3f} seconds"
            else:
                output = f"{delta.microseconds} microseconds"

            return output

        elif format == "seconds":
            return delta.total_seconds()

        elif format == "microseconds":
            return delta.microseconds

        else:
            raise ValueError(
                f"Format must be one of 'seconds', 'microseconds', or 'str'. Currently: {format}"
            )
