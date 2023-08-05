import io
import sys
from argparse import ArgumentParser, FileType

import toml
from PIL import Image

from dememefy import posts
from dememefy.image import Demotivator

SERVICES = {
    "reddit": (posts.RedditPosts, ["username", "password", "client_id", "token"], ["thread"]),
}


def _parse_args():
    parser = ArgumentParser(
        prog="dememefy", description="Make media fun again")
    parser.add_argument(
        "--service", "-s",
        dest="service",
        type=str,
        choices=SERVICES.keys(),
        help="Target Service.")
    parser.add_argument(
        "--save-to", "-st",
        type=str,
        default="result.png",
        dest="destination",
        help="Destination for demotivator"
    )
    parser.add_argument(
        "--open", "-o",
        action="store_true",
        help="Open output intentionally"
    )
    parser.add_argument(
        "image",
        type=FileType("rb"),
        nargs="?",
        default=sys.stdin.buffer,
        help="Image for demotivator (works only in plain mode).")
    parser.add_argument(
        "--text", "-txt",
        dest="text",
        type=str,
        default="title",
        help="Text for demotivator (works only in plain mode).")
    parser.add_argument(
        "--config", "-c",
        dest="config",
        type=str,
        help="Path to config for parse memes in target service.")
    return parser.parse_args()


def save_demotivator(picture: Image.Image, text: str, filename: str, open: bool):
    demotivator = Demotivator(
        image=picture, text=text, x_start=75, y_start=45)
    picture = demotivator.create()
    picture.save(filename)
    if open:
        try:
            picture.show()
        except OSError as error:
            print(f"Can't open generated output. Error: {error}.")


def main():
    args = _parse_args()

    if not args.service:
        if (args.text is None) or (args.image is None):
            raise ValueError(
                "In plain mode you need to set both text and image.")
        with args.image as image:
            picture = Image.open(io.BytesIO(image.read()))
        save_demotivator(picture, args.text, args.destination, args.open)
        return

    try:
        with open(args.config) as file:
            toml_string = toml.loads(file.read())
    except FileNotFoundError as error:
        raise FileNotFoundError(f"Can't find toml file. Error: {error}.")
    except:
        raise TypeError("Can't parse config file. Perhaps misconfiguration.")

    service_name, credentials, params = SERVICES[args.service]

    kwargs = {}
    for arg_name in [*credentials, *params]:
        try:
            arg_value = toml_string[args.service][arg_name]
            if arg_value:
                kwargs[arg_name] = arg_value
        except KeyError:
            if arg_name in credentials:
                raise KeyError(f"{arg_name} is missing. It's necessary param!")

    service = service_name(**kwargs)

    try:
        amount = toml_string[args.service]["amount"]
    except:
        amount = 1

    for i in range(amount):
        text, picture = service.get_post()
        save_demotivator(picture, text, f"{i+1}_{args.destination}", args.open)
