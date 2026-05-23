from pathlib import Path

import yaml

from atguigu.flow.links import FlowStepLink, StaticLink, ConditionalLink, FallbackLink
from atguigu.flow.models import FlowsList, FlowSlot, Flow
from atguigu.flow.step import FlowStep


class FlowLoader:
    def load(self,path:Path)-> FlowsList:
        with open(path,'r',encoding='utf-8') as f:
            data =  yaml.safe_load( f)
            slots = self._load_slot(data.get('slots',{}))
            flows = self._load_flows(data.get('flows',{}),slots)
            return FlowsList(flows=flows,slots=slots)

    def _load_slot(self, slots_data:dict[str,dict]) -> dict[str,FlowSlot]:
        slots = {}
        for slot_name , slot_data in slots_data.items():
            slots[slot_name] = FlowSlot(
                **slot_data,
                name=slot_name
            )
        return slots

    def _load_flows(self, flow_data:dict[str,dict], slots)-> list[Flow]:
        flows:list[Flow] = []
        for flow_id,flow_data in flow_data.items():
            flows.append(Flow(
                id=flow_id,
                name=flow_data.get('name'),
                description=flow_data.get('description'),
                steps=self._load_steps(flow_data.get('steps', [])),
                slots=slots
            ))
        return  flows

    def _load_steps(self, flow_step_data:list[dict]):
        flow_step:list[FlowStep]= []
        for step_data in flow_step_data:
            flow_step.append(FlowStep(
                id=step_data['id'],
                type=step_data['type'],
                description=step_data.get('description'),
                next=self._load_step_links(step_data.get('next', []))
            ))
        return flow_step

    @staticmethod
    def _load_step_links(next_data: str | list) -> list[FlowStepLink]:
        if isinstance(next_data, str):
            return [StaticLink(target=next_data)]
        else:
            links = []
            for link_data in next_data:
                if 'if' in link_data:
                    links.append(ConditionalLink(target=link_data['then'], condition=link_data['if']))
                else:
                    links.append(FallbackLink(target=link_data['else']))
            return links

    def load_many(self, paths: list[Path]) -> FlowsList:
        flows: list[Flow] = []
        slots: dict[str, FlowSlot] = {}
        for path in paths:
            flows_list: FlowsList = self.load(path)
            flows.extend(flows_list.flows)
            slots.update(flows_list.slots)
        return FlowsList(flows=flows, slots=slots)

if __name__ == '__main__':
    user_flow_path = Path(__file__).parents[2] / 'flow_config' / 'user_flows.yml'
    system_flow_path = Path(__file__).parents[2] / 'flow_config' / 'system_flows.yml'
    loader = FlowLoader()
    result = loader.load_many([ user_flow_path,system_flow_path])
    for flow in result.flows:
        print(flow)
    for slot in result.slots:
        print(slot)
