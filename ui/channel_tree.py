from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QLabel,
    QLineEdit,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)

class ChannelTree(QWidget):
    channel_selected = Signal(str, str)

    def __init__(self) -> None:
        super().__init__()

        self.filter_edit = QLineEdit()
        self.filter_edit.setPlaceholderText("Фильтр по имени группы или канала...")

        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["Группы / каналы"])
        self.tree.setAlternatingRowColors(True)
        self.tree.setUniformRowHeights(True)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Каналы"))
        layout.addWidget(self.filter_edit)
        layout.addWidget(self.tree)

        self.filter_edit.textChanged.connect(self._apply_filter)
        self.tree.currentItemChanged.connect(self._on_current_item_changed)

    def set_structure(self, structure: dict[str, list[str]]) -> None:
        self.tree.clear()

        for group_name, channel_names in structure.items():
            group_item = QTreeWidgetItem([group_name])

            for channel_name in channel_names:
                channel_item = QTreeWidgetItem([channel_name])
                channel_item.setData(0, Qt.UserRole, (group_name, channel_name))
                group_item.addChild(channel_item)

            self.tree.addTopLevelItem(group_item)
            group_item.setExpanded(True)

        self._apply_filter(self.filter_edit.text())

    def _on_current_item_changed(
        self,
        current: QTreeWidgetItem | None,
        previous: QTreeWidgetItem | None,
    ) -> None:
        del previous

        if current is None:
            return

        payload = current.data(0, Qt.UserRole)
        if payload is None:
            return

        group_name, channel_name = payload
        self.channel_selected.emit(group_name, channel_name)

    def _apply_filter(self, text: str) -> None:
        query = text.strip().lower()

        for i in range(self.tree.topLevelItemCount()):
            group_item = self.tree.topLevelItem(i)
            group_name = group_item.text(0).lower()

            group_matches = query in group_name if query else True
            any_child_visible = False

            for j in range(group_item.childCount()):
                child_item = group_item.child(j)
                child_name = child_item.text(0).lower()

                child_matches = query in child_name if query else True
                visible = (not query) or group_matches or child_matches

                child_item.setHidden(not visible)
                any_child_visible = any_child_visible or visible

            group_visible = (not query) or group_matches or any_child_visible
            group_item.setHidden(not group_visible)

            if query and group_visible:
                group_item.setExpanded(True)