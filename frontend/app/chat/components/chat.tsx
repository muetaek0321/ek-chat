'use client'

import { useState, useEffect } from 'react'
import Stack from '@mui/material/Stack'
import Box from '@mui/material/Box'
import IconButton from '@mui/material/IconButton'
import ChevronLeftIcon from '@mui/icons-material/ChevronLeft'
import MenuIcon from '@mui/icons-material/Menu'

import NewChatButton from './NewChatButton'
import SettingButton from './SettingButton'
import ChatList from './ChatList'
import ChatContentUser from './ChatContentUser'
import ChatContentAssistant from './ChatContentAssistant'
import UserInput from './UserInput'
import { ApiResponse, getRequest, putRequest } from '@lib/fetchData'
import { ChatInfo, ChatMessage } from '@types'

export default function Chat() {
  const chatListWidth = 250
  const collapsedWidth = 48
  const userInputHeight = 50

  const [isRunning, setIsRunning] = useState<boolean>(false)
  const [isSidebarOpen, setIsSidebarOpen] = useState<boolean>(true)

  const [chatInfoList, setChatInfoList] = useState<ChatInfo[]>([])
  const [chatHistory, setChatHistory] = useState<ChatMessage[]>([])

  // サイドバーの開閉切り替え
  const toggleSidebar = () => {
    setIsSidebarOpen((prev) => !prev)
  }

  // 現在のサイドバー幅
  const currentSidebarWidth = isSidebarOpen ? chatListWidth : collapsedWidth

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
      {/* サイドバー（新規作成、設定、チャット一覧） */}
      <Box
        sx={{
          width: currentSidebarWidth,
          minWidth: currentSidebarWidth,
          borderRight: 1,
          borderColor: 'divider',
          transition: 'width 0.3s ease, min-width 0.3s ease',
          overflow: 'hidden',
          display: 'flex',
          flexDirection: 'column',
        }}
      >
        {/* サイドバー閉じる/開くボタン */}
        <Box
          sx={{
            display: 'flex',
            justifyContent: isSidebarOpen ? 'flex-end' : 'center',
            p: 0.5,
          }}
        >
          <IconButton onClick={toggleSidebar} size="small">
            {isSidebarOpen ? <ChevronLeftIcon /> : <MenuIcon />}
          </IconButton>
        </Box>

        {/* サイドバーのコンテンツ（開いているときのみ表示） */}
        <Box
          sx={{
            opacity: isSidebarOpen ? 1 : 0,
            visibility: isSidebarOpen ? 'visible' : 'hidden',
            transition: 'opacity 0.2s ease, visibility 0.2s ease',
            display: 'flex',
            flexDirection: 'column',
            gap: 1,
            flex: 1,
            overflow: 'hidden',
          }}
        >
          <NewChatButton createNewChat={createNewChat} isRunning={isRunning} />
          <SettingButton isRunning={isRunning} />
          <ChatList
            chatInfoList={chatInfoList}
            setChatInfoList={setChatInfoList}
            getChatHistory={getChatHistory}
            createNewChat={createNewChat}
            isRunning={isRunning}
          />
        </Box>
      </Box>

      {/* チャット内容（チャット履歴、入力欄） */}
      <Box
        sx={{
          width: `calc(100vw - ${currentSidebarWidth}px)`,
          transition: 'width 0.3s ease',
        }}
      >
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
