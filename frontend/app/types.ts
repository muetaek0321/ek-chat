// チャットの概要情報
export interface ChatInfo {
  chatId: string
  title: string
}

// チャットメッセージ
export interface ChatMessage {
  role: 'user' | 'assistant'
  content: string
}

// チャット生成のレスポンスデータ
export interface GeneratedChatMessage {
  assistantMessage: ChatMessage
  newChatInfo?: ChatInfo
}

// SystemPrompt
export interface SystemPrompt {
  text: string
}
