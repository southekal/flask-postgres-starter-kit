from markdown2 import Markdown

from log_config.custom_logger import logger


def to_markdown(document):
	m = Markdown(extras=["footnotes", "tables"])
	mk = m.convert(document)
	return mk