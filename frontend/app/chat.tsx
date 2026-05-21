'use client'

import { useState, useEffect } from 'react'
import Stack from '@mui/material/Stack'
import Box from '@mui/material/Box'

import NewChatButton from '@components/NewChatButton'
import ChatList from '@components/ChatList'
import ChatContentUser from '@components/ChatContentUser'
import ChatContentAssistant from '@components/ChatContentAssistant'
import UserInput from '@components/UserInput'
import { ApiResponse, getRequest, putRequest } from '@modules/fetchData'
import { ChatInfo, ChatMessage } from '@types'

export default function Chat() {
  const chatListWidth = 250
  const userInputHeight = 50

  const [isRunning, setIsRunning] = useState<boolean>(false)

  const [chatInfoList, setChatInfoList] = useState<ChatInfo[]>([])
  const [chatHistory, setChatHistory] = useState<ChatMessage[]>([])

  // アプリ立ち上げ時に保存済みチャットの情報の取得
  const getChatInfoList = async () => {
    await getRequest<ChatInfo[]>('/init')
      .then((res: ApiResponse<ChatInfo[]>) => {
        if (res.success && res.data !== undefined) {
          const chatInfoList = res.data
          if (chatInfoList.length === 0) {
            createNewChat()
          } else {
            setChatInfoList(chatInfoList)
            getChatHistory(chatInfoList[0].chatId)
          }
        } else {
          alert('チャット情報の取得に失敗しました。')
          console.log('Error:', res.error)
        }
      })
      .catch((err) => console.log('Error:', err))
  }

  // 新しいチャットの作成
  const createNewChat = async () => {
    // 新しいチャットの作成APIを呼び出し
    await putRequest<ChatInfo>('/new')
      .then((res: ApiResponse<ChatInfo>) => {
        if (res.success && res.data !== undefined) {
          const newChatInfo = res.data
          getChatHistory(newChatInfo.chatId)
          // 既に空のチャットが存在しない場合のみからのチャットを追加
          if (!chatInfoList.some((chat) => chat.chatId === 'new')) {
            setChatInfoList((prev) => [...prev, newChatInfo])
          }
        } else {
          alert('新しいチャットの作成に失敗しました。')
          console.log('Error:', res.error)
        }
      })
      .catch((err) => console.log('Error:', err))
  }

  // チャット履歴の取得
  const getChatHistory = async (chatId: string) => {
    const query = new URLSearchParams({
      chatId: chatId,
    }).toString()
    await getRequest<ChatMessage[]>(`/history?${query}`)
      .then((res: ApiResponse<ChatMessage[]>) => {
        if (res.success && res.data !== undefined) {
          setChatHistory(res.data)
        } else {
          alert('チャット履歴の取得に失敗しました。')
          console.log('Error:', res.error)
        }
      })
      .catch((err) => console.log('Error:', err))
  }

  // 立ち上げ時にチャット一覧の初期化
  useEffect(() => {
    if (chatInfoList.length === 0) getChatInfoList()
  }, [])

  return (
    <Stack direction="row" sx={{ height: '100vh' }}>
      {/* チャット一覧 */}
      <Stack spacing={1} sx={{ width: chatListWidth, borderRight: 1, borderColor: 'divider' }}>
        <NewChatButton createNewChat={createNewChat} isRunning={isRunning} />
        <ChatList
          chatInfoList={chatInfoList}
          setChatInfoList={setChatInfoList}
          getChatHistory={getChatHistory}
          createNewChat={createNewChat}
          isRunning={isRunning}
        />
      </Stack>

      {/* 入力とチャット履歴 */}
      <Box sx={{ width: `calc(100vw - ${chatListWidth}px)` }}>
        <Box
          sx={{
            height: `calc(100vh - ${userInputHeight}px)`,
            width: '100%',
            overflowY: 'auto',
            p: 1,
          }}
        >
          {chatHistory.map((message, i) => (
            <Box key={i} sx={{ width: '100%' }}>
              {message.role === 'user' ? (
                <ChatContentUser message={message} />
              ) : (
                <ChatContentAssistant message={message} />
              )}
            </Box>
          ))}
        </Box>
        <Box sx={{ height: userInputHeight, borderTop: 1, borderColor: 'divider' }}>
          <UserInput
            setChatHistory={setChatHistory}
            setChatInfoList={setChatInfoList}
            isRunning={isRunning}
            setIsRunning={setIsRunning}
          />
        </Box>
      </Box>
    </Stack>
  )
}
