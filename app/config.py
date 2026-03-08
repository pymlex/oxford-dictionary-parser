from os import getenv

MAX_PAGES = int(getenv("MAX_PAGES", "4"))
USER_AGENT_POOL = getenv("USER_AGENT_POOL", "auto")