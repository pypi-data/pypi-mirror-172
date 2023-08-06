import time
from functools import partial
from dfsync.char_ui import KeyController


def cmd_a():
    print("AAAAA")


def cmd_b():
    print("BBBBB")
    raise ValueError("BBBBB")


state = ["Good"]
mp = []


def cmd_c():
    print(f"State: {state.pop()}")


def cmd_t():
    mp.append("Some error")


def main():
    controller = KeyController()
    controller.on_key(
        "a",
        description="to do task a",
        action=cmd_a,
    )
    controller.on_key(
        "r",
        description="to raise an error",
        action=cmd_b,
    )
    controller.on_key(
        "t",
        description="to raise threading error",
        action=cmd_t,
    )
    controller.on_key(
        "s",
        description="to raise an error on next press",
        action=cmd_c,
    )
    controller.on_key(
        "x",
        description="to exit",
        action=partial(controller.stop, "Exiting."),
    )

    try:
        controller.help()
        controller.start()

        while controller.is_running:
            time.sleep(0.2)
            controller.raise_exceptions()
            if mp:
                raise ValueError(mp[0])
    except KeyboardInterrupt:
        controller.stop()
        print("Received [Ctrl-C], exiting.")

    except:
        controller.stop()
        raise


if __name__ == "__main__":
    main()
