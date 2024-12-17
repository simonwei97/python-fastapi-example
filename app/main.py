import argparse

import uvicorn
from uvicorn.config import LOGGING_CONFIG

from app.conf import settings


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--workers", type=int, default=1)
    args = parser.parse_args()

    # refer: https://github.com/tiangolo/fastapi/issues/1508
    log_config = LOGGING_CONFIG
    log_config["formatters"]["default"][
        "fmt"
    ] = "%(asctime)s | %(levelname)s | %(message)s"
    log_config["formatters"]["access"][
        "fmt"
    ] = "%(asctime)s | %(levelname)s | %(message)s"

    uvicorn.run(
        "app.server:app",
        host=args.host,
        port=args.port,
        workers=args.workers,
        log_level=settings.log_level,
        log_config=log_config,
        use_colors=True,
    )


if __name__ == "__main__":
    main()
