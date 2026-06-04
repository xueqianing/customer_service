

class FlowStepLink:
    target:str

class StaticLink(FlowStepLink):
    pass


class ConditionalLink(FlowStepLink):
    condition:str

class FallbackLink(FlowStepLink):
    pass