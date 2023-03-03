from typing import List

import manager.bot
from adapter.botservice import BotAdapter
from adapter.chatgpt.web import ChatGPTWebAdapter
from renderer.renderer import Renderer, FullTextRenderer

handlers = dict()


class ConversationContext:
    type: str
    adapter: BotAdapter
    renderer: Renderer

    def __init__(self, _type):
        self.renderer = FullTextRenderer()
        if _type == 'chatgpt-web':
            self.adapter = ChatGPTWebAdapter()
        else:
            raise Exception("Unsupported adapter")
        self.type = _type

    async def reset(self):
        pass

    async def ask(self, prompt: str, name: str = None):
        async with self.renderer:
            async for item in self.adapter.ask(prompt):
                yield await self.renderer.render(item)
            yield await self.renderer.result()

    def rollback(self):
        pass


class ConversationHandler:
    """
    每个聊天窗口拥有一个 ConversationHandler，
    负责管理多个不同的 ConversationContext
    """
    conversations = []
    """当前聊天窗口下所有的会话"""

    current_conversation: ConversationContext = None

    def __int__(self, ):
        ...

    def list(self) -> List[ConversationContext]:
        ...

    """创建新的上下文"""

    async def create(self, _type: str):
        if len(self.conversations) < 1:
            conversation = ConversationContext(_type)
            self.conversations.append(conversation)
            print("Duck")
            return conversation
        return self.conversations[0]
        # raise Exception("Too many conversations")

    """切换对话上下文"""

    def switch(self, index: int) -> bool:
        if len(self.conversations) > index:
            self.current_conversation = self.conversations[index]
            return True
        return False

    @classmethod
    async def get_handler(cls, session_id: str):
        if session_id not in handlers:
            handlers[session_id] = ConversationHandler()
        return handlers[session_id]
