from pathlib import Path

import yaml

from atguigu.task.flow.models import FlowsList, FlowSlot


class FlowLoader:
    def load(self, path: Path) -> FlowsList:
        with open(path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        slots = self._load_slots(data.get('slots', {}))
        print(slots)

    def _load_slots(self, slots_data: dict[str, dict]) -> dict[str, FlowSlot]:
        slots = {}
        for slot_name, slot_data in slots_data.items():
            slots[slot_name] = FlowSlot(**slot_data, name=slot_name)
        return slots


if __name__ == '__main__':
    flow_path = Path(__file__).parents[3] / 'flow_config' / 'user_flows.yml'
    loader = FlowLoader()
    flows_list = loader.load(flow_path)
