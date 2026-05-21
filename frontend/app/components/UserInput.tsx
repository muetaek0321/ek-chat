'use client'

import React, { useState } from 'react'
import Stack from '@mui/material/Stack'
import TextField from '@mui/material/TextField'
import IconButton from '@mui/material/IconButton'
import SendIcon from '@mui/icons-material/Send'

import { ApiResponse, postRequest } from '@modules/fetchData'
import { ChatMessage, ChatInfo, GeneratedChatMessage } from '@types'

export interface UserInputProps {
  setChatHistory: React.Dispatch<React.SetStateAction<ChatMessage[]>>
  setChatInfoList: React.Dispatch<React.SetStateAction<ChatInfo[]>>
  isRunning: boolean
  setIsRunning: React.Dispatch<React.SetStateAction<boolean>>
}

export default function UserInput({
  setChatHistory,
  setChatInfoList,
  isRunning,
  setIsRunning,
}: UserInputProps) {
  const [inputText, setInputText] = useState<string>('')

  // 入力内容の送信時の処理
  const handleSendUserInput = async () => {
    // 生成中は各種機能を無効化する
    setIsRunning(true)

    // backendと通信して返答生成
    const userInput: ChatMessage = {
      role: 'user',
      content: inputText,
    }
    await postRequest<GeneratedChatMessage>('/chat', userInput)
      .then((res: ApiResponse<GeneratedChatMessage>) => {
        if (res.success && res.data !== undefined) {
          const response = res.data
          // チャット履歴に追加
          setChatHistory((prev) => [...prev, userInput, response.assistantMessage])
          // 新しいチャットからの実行の場合はチャット情報も更新
          if (response.newChatInfo !== undefined) {
            const newChatInfo = response.newChatInfo
            setChatInfoList((prev) =>
              prev.length === 0
                ? [newChatInfo]
                : prev.map((e) => (e.chatId === 'new' ? newChatInfo : e)),
            )
          }
          // 入力欄をクリア
          setInputText('')
          // 各種機能の有効化
          setIsRunning(false)
        } else {
          alert('返答の生成に失敗しました。')
          console.log('Error:', res.error)
        }
      })
      .catch((err) => console.log('Error:', err))
  }

  // Enterキーで送信
  const handleEnterKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      if (inputText.trim() !== '') handleSendUserInput()
    }
  }

  return (
    <Stack direction="row" spacing={1} sx={{ p: 0.5, height: '100%' }}>
      <TextField
        variant="outlined"
        size="small"
        fullWidth
        rows={2}
        value={inputText}
        onChange={(e) => setInputText(e.target.value)}
        onKeyDown={handleEnterKeyPress}
        disabled={isRunning}
      />
      <IconButton
        color="primary"
        sx={{ height: '100%' }}
        onClick={handleSendUserInput}
        disabled={inputText.trim() === '' || isRunning}
      >
        <SendIcon fontSize="large" />
      </IconButton>
    </Stack>
  )
}
