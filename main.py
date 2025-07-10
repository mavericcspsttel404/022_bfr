from core.BreakfastReport import run_breakfast_report
from settings import TEST_IMPORTS_INT, TEST_IMPORTS_TEXT, custom
from utils.logger import get_logger

logger = get_logger(__name__)


def k_add(x: int, y: int) -> int:
    """Adds two integers."""
    return x + y


def main() -> None:
    logger.info("🍽️ Breakfast report app started!")

    logger.debug("✨ Debug message")
    logger.info("✅ App finished successfully.")
    logger.warning("⚠️ This is a warning!")
    logger.error("💥 Oops, an error occurred")

    logger.debug(f"TEST_IMPORTS_TEXT {TEST_IMPORTS_TEXT}")
    logger.debug(f"TEST_IMPORTS_INT {TEST_IMPORTS_INT}")

    if custom:
        run_breakfast_report()
    else:
        run_breakfast_report()


if __name__ == "__main__":
    main()
