from modules.schema import (
    ChatHistory,
    ChatId,
    ChatInfo,
    ChatInfoList,
    ChatMessage,
    ChatModel,
    ChatModelInfo,
    ChatModelParameter,
    GenerateChatResponse,
    Role,
    SelectedChatModel,
    SettingsResponse,
    SystemPromptText,
    Thinking,
)


class TestSchema:
    """schema.pyのテスト"""

    def test_role_enum(self):
        """Role Enumのテスト"""
        assert Role.USER == "user"
        assert Role.ASSISTANT == "assistant"
        assert Role.SYSTEM == "system"

    def test_chat_model_enum(self):
        """ChatModel Enumのテスト"""
        assert ChatModel.GEMINI == "Gemini(API)"
        assert ChatModel.GEMMA4_E2B == "Gemma4:E2B"
        assert ChatModel.GEMMA4_12B == "Gemma4:12B"
        assert ChatModel.OLLAMA == "Ollama(cloud)"

    def test_thinking_enum(self):
        """Thinking Enumのテスト"""
        assert Thinking.LOW == "low"
        assert Thinking.MEDIUM == "medium"
        assert Thinking.HIGH == "high"

    def test_chat_info(self):
        """ChatInfoモデルのテスト"""
        chat_info = ChatInfo(chat_id="test_id", title="Test Chat")
        assert chat_info.chat_id == "test_id"
        assert chat_info.title == "Test Chat"

    def test_chat_info_list(self):
        """ChatInfoListモデルのテスト"""
        chat_info_list = ChatInfoList(
            [
                ChatInfo(chat_id="test_id_1", title="Test Chat 1"),
                ChatInfo(chat_id="test_id_2", title="Test Chat 2"),
            ]
        )
        assert len(chat_info_list.root) == 2
        assert chat_info_list.root[0].chat_id == "test_id_1"
        assert chat_info_list.root[1].title == "Test Chat 2"

    def test_system_prompt_text(self):
        """SystemPromptTextモデルのテスト"""
        system_prompt_text = SystemPromptText(text="You are a helpful assistant.")
        assert system_prompt_text.text == "You are a helpful assistant."

    def test_chat_model_parameter(self):
        """ChatModelParameterモデルのテスト"""
        chat_model_parameter = ChatModelParameter(temperature=0.5, thinking=Thinking.MEDIUM)
        assert chat_model_parameter.temperature == 0.5
        assert chat_model_parameter.thinking == Thinking.MEDIUM

    def test_selected_chat_model(self):
        """SelectedChatModelモデルのテスト"""
        selected_chat_model = SelectedChatModel(
            model=ChatModel.GEMINI,
            parameters=ChatModelParameter(temperature=0.5, thinking=Thinking.MEDIUM),
        )
        assert selected_chat_model.model == ChatModel.GEMINI
        assert selected_chat_model.parameters.temperature == 0.5

    def test_chat_model_info(self):
        """ChatModelInfoモデルのテスト"""
        chat_model_info = ChatModelInfo(
            model_name=ChatModel.GEMINI,
            is_use=True,
            is_selected=True,
            parameters=ChatModelParameter(temperature=0.5, thinking=Thinking.MEDIUM),
        )
        assert chat_model_info.model_name == ChatModel.GEMINI
        assert chat_model_info.is_use == True
        assert chat_model_info.is_selected == True
        assert chat_model_info.parameters.temperature == 0.5

    def test_settings_response(self):
        """SettingsResponseモデルのテスト"""
        settings_response = SettingsResponse(
            system_prompt=SystemPromptText(text="You are a helpful assistant."),
            chat_model_info_list=[
                ChatModelInfo(
                    model_name=ChatModel.GEMINI,
                    is_use=True,
                    is_selected=True,
                    parameters=ChatModelParameter(temperature=0.5, thinking=Thinking.MEDIUM),
                )
            ],
        )
        assert settings_response.system_prompt.text == "You are a helpful assistant."
        assert len(settings_response.chat_model_info_list) == 1

    def test_chat_message(self):
        """ChatMessageモデルのテスト"""
        chat_message = ChatMessage(role=Role.USER, content="Hello")
        assert chat_message.role == Role.USER
        assert chat_message.content == "Hello"

    def test_chat_history(self):
        """ChatHistoryモデルのテスト"""
        chat_history = ChatHistory(
            [
                ChatMessage(role=Role.USER, content="Hello"),
                ChatMessage(role=Role.ASSISTANT, content="Hi"),
            ]
        )
        assert len(chat_history.root) == 2
        assert chat_history.root[0].role == Role.USER
        assert chat_history.root[1].content == "Hi"

    def test_chat_id(self):
        """ChatIdモデルのテスト"""
        chat_id = ChatId(chat_id="test_id")
        assert chat_id.chat_id == "test_id"

        chat_id_none = ChatId()
        assert chat_id_none.chat_id is None

    def test_generate_chat_response(self):
        """GenerateChatResponseモデルのテスト"""
        generate_chat_response = GenerateChatResponse(
            assistant_message=ChatMessage(role=Role.ASSISTANT, content="Hi"),
            new_chat_info=ChatInfo(chat_id="new_id", title="New Chat"),
        )
        assert generate_chat_response.assistant_message.content == "Hi"
        assert generate_chat_response.new_chat_info.chat_id == "new_id"

        generate_chat_response_none = GenerateChatResponse(
            assistant_message=ChatMessage(role=Role.ASSISTANT, content="Hi"),
        )
        assert generate_chat_response_none.new_chat_info is None
