import sys

from utils.logger import get_logger

logger = get_logger(__name__)

is_uat = True
update_dw = False

if len(sys.argv) > 2:
    if sys.argv[1] == "uat":
        is_uat = True
    if sys.argv[1] == "prod":
        is_uat = False
    if sys.argv[2] == "update":
        update_dw = True


def say_hello(name: str) -> str:
    return f"👋 Hello, {name}!"


def main() -> None:
    logger.info("🍽️ Breakfast report app started!")
    message = say_hello("Functional Programmer")
    print(message)
    logger.info("✅ App finished successfully.")
    logger.debug("Debug message ✨")
    logger.warning("This is a warning! ⚠️")
    logger.error("Oops, an error occurred 💥")
    logger.debug(f"Debug info: {message}")


if __name__ == "__main__":
    main()
