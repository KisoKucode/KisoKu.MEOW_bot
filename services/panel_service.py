from typing import Optional

from models.panel import Panel
from services.dao_protocols import PanelDAOProtocol


class PanelService:
    """Servicio para gestionar el panel de estado con abstracción de persistencia."""

    def __init__(self, panel_dao: PanelDAOProtocol) -> None:
        self._panel_dao = panel_dao

    def save_panel(self, guild_id: int, channel_id: int, message_id: int) -> None:
        self._panel_dao.save_panel(guild_id, channel_id, message_id)

    def get_panel(self) -> Optional[Panel]:
        return self._panel_dao.get_panel()

    def clear_panel(self) -> None:
        self._panel_dao.clear_panel()
