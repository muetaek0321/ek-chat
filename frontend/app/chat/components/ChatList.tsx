'use client'

import Box from '@mui/material/Box'
import Stack from '@mui/material/Stack'
import IconButton from '@mui/material/IconButton'
import BackspaceIcon from '@mui/icons-material/Backspace'
import type { MouseEvent } from 'react'

import { ApiResponse, deleteRequest } from '@lib/fetchData'
import { ChatInfo } from '@types'

export interface ChatListProps {
  chatInfoList: ChatInfo[]
  setChatInfoList: React.Dispatch<React.SetStateAction<ChatInfo[]>>
  getChatHistory: (chatId: string) => void
  createNewChat: () => void
  isRunning: boolean
}

export default function ChatList({
  chatInfoList,
  setChatInfoList,
  getChatHistory,
  createNewChat,
  isRunning,
}: ChatListProps) {
  // チャットの切り替え
  const handleChatSwitch = (chatId: string) => {
    // 生成中はチャットの切り替えを無効化する
    if (isRunning) return
    // チャット履歴の取得
    getChatHistory(chatId)
  }

  // チャットの削除
  const handleDeleteButton = async (event: MouseEvent<HTMLButtonElement>, chatId: string) => {
    // 親要素のイベント発火を防止
    event.stopPropagation()

    const query = new URLSearchParams({
      chatId: chatId,
    }).toString()
    await deleteRequest<undefined>(`/delete?${query}`)
      .then((res: ApiResponse<undefined>) => {
        if (res.success) {
          // チャットリストから削除
          const deletedChatInfoList = chatInfoList.filter((e) => e.chatId !== chatId)
          setChatInfoList(deletedChatInfoList)
          // 削除後の対応
          const numChatInfoList = deletedChatInfoList.length
          if (numChatInfoList === 0) {
            createNewChat()
          } else {
            getChatHistory(deletedChatInfoList[numChatInfoList - 1].chatId)
          }
        } else {
          alert('チャットの削除に失敗しました。')
          console.log('Error:', res.error)
        }
      })
      .catch((err) => console.log('Error:', err))
  }

  return (
    <Box sx={{ height: '70vh', overflowY: 'auto' }}>
      {chatInfoList.map((chatInfo, i) => (
        <Box
          key={i}
          sx={{ border: 1, borderRadius: 1, borderColor: '#e0e0e0', my: 0.5 }}
          onClick={() => handleChatSwitch(chatInfo.chatId)}
        >
          <Box
            sx={{
              py: 0.5,
              px: 1,
              cursor: 'pointer',
              pointerEvents: isRunning ? 'none' : 'auto',
              '&:hover': { backgroundColor: '#f0f0f0' },
              whiteSpace: 'nowrap',
              overflow: 'hidden',
              textOverflow: 'ellipsis',
            }}
          >
            {chatInfo.title}
            <Stack direction="row" sx={{ justifyContent: 'flex-end' }}>
              <IconButton
                size="small"
                onClick={(e) => handleDeleteButton(e, chatInfo.chatId)}
                disabled={isRunning}
              >
                <BackspaceIcon fontSize="small" />
              </IconButton>
            </Stack>
          </Box>
        </Box>
      ))}
    </Box>
  )
}
