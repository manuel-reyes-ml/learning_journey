""" """

from __future__ import annotations

import anthropic

from learning_journey.claude.settings import Settings, get_settings

__all__ = ["get_client"]


def get_client() -> tuple[anthropic.Anthropic, Settings]:
    """ """
    settings = get_settings()
    return anthropic.Anthropic(api_key=settings.anthropic_api_key.get_secret_value()), settings


# log.info("key_accepted", api_key=settings.anthropic_api_key.get_secret_value()[-4:])
