import traceback

import requests

from utils.logger import get_logger

# from utils.spikeAlert import create_spike_incident

logger = get_logger(__name__)


def handle_exception(e):
    logger.error(f"error_type: {str(type(e).__name__)}")
    logger.error(f"error_message: {str(e)}")
    logger.error(f"error_stacktrace: {str(traceback.format_exc())}")

    # TODO: any complex logic to decide on severity and priority etc
    try:
        # response = create_spike_incident(
        #     message=str(e),
        #     name=type(e).__name__,
        #     step_id="",
        #     stack=traceback.format_exc(),
        #     severity="sev2",
        #     priority="p2",
        # )
        # logger.debug(f"response = {str(response)}")
        logger.info("Spike Alert sent successfully")
    except requests.exceptions.RequestException as e:
        logger.error(f"Error creating spike incident: {str(e)}")
    except Exception as e:
        logger.error(f"Error creating spike incident: {str(e)}")

    # TODO: send email to developers
