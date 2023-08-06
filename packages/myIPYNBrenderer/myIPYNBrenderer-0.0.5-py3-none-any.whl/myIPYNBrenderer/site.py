from IPython import display
from ensure import ensure_annotations
from urllib.request import urlopen
from myIPYNBrenderer.custom_exception import InvalidURLException
from myIPYNBrenderer.logger import logger


@ensure_annotations
def is_valid_URL(URL: str) -> bool:
    try:
        response_status = urlopen(URL).getcode()
        assert response_status == 200
        logger.debug(f"response_status: {response_status}")
        return True
    except Exception as e:
        logger.exception(e)
        return False


@ensure_annotations
def render_site(URL: str, width: str="90%", height: int=500) -> str:
    try:
        if is_valid_URL(URL):
            response = display.IFrame(src=URL, width=width, height=height)
            display.display(response)
            return "SUCCESS"
        else:
            raise InvalidURLException
    except Exception as e:
        raise e