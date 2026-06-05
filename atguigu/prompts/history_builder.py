from tenacity import retry

from atguigu.domain.messages import MessageObject, BotMessage, UserMessage
from atguigu.domain.state import Turn


class HistoryBuilder:
    @staticmethod
    def build(turns:list[Turn]) -> str:
        messages:list[str] = []
        for turn in turns:
            user_message = turn.user_message
            rendered_user_message = HistoryBuilder.render_user_message(user_message)
            messages.append(f"USER:{rendered_user_message}")
            for bot_message in turn.bot_messages:
                rendered_bot_message = HistoryBuilder.render_bot_message(bot_message)
                messages.append(f"BOT:{rendered_bot_message}")
        return "\n".join(messages)
    @staticmethod
    def render_text(text:str) -> str:
        return text.strip()

    @staticmethod
    def render_object(object:MessageObject) -> str:
        label = '订单对象' if object.type == 'order' else '商品对象'
        object_id = object.id
        title = object.title
        attributes = object.attributes
        attributes_str = ", ".join([f"{key}:{value}" for key,value in attributes.items()])
        return f"[{label} id={object_id}, title={title}, {attributes_str}]"


    @staticmethod
    def render_bot_message(bot_message:BotMessage) -> str:
        if bot_message.text:
            return HistoryBuilder.render_text(bot_message.text)
        else:
            return HistoryBuilder.render_object(bot_message.object)

    @staticmethod
    def render_user_message(user_message:UserMessage) -> str:
        if user_message.text:
            return HistoryBuilder.render_text(user_message.text)
        else:
            return HistoryBuilder.render_object(user_message.object)


