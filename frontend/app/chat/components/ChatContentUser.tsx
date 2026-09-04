'use client'

import ReactMarkdown from 'react-markdown'
import Image from 'next/image'
import Stack from '@mui/material/Stack'
import Box from '@mui/material/Box'
import { Theme } from '@mui/material/styles'

import { useTheme } from '../../ThemeProvider'
import { ChatMessage } from '@types'

/**
 * ユーザー発言の吹き出しを描画するコンポーネントの Props。
 *
 * @param message - 表示対象のチャットメッセージ。`role` が `'user'` であることを前提とする。
 */
export interface ChatContentUserProps {
  message: ChatMessage
}

/**
 * ユーザー発言をチャット吹き出し形式で表示するコンポーネント。
 *
 * メッセージ本文を Markdown としてレンダリングし、右寄せの吹き出し＋ユーザーアイコンとして描画する。
 * 吹き出しの三角形は CSS 疑似要素（`::before` / `::after`）で構成される。
 *
 * @param props - {@link ChatContentUserProps}
 * @returns ユーザー発言の吹き出し UI
 */
export default function ChatContentUser({ message }: ChatContentUserProps) {
  const { fontSize } = useTheme()

  const chatBubbleStyle = {
    position: 'relative',
    border: 1.5,
    borderRadius: 1,
    borderColor: '#505050',
    p: 1,
    bgcolor: 'background.paper',
    fontSize: `${fontSize}px`,

    '&::before': {
      content: '""',
      position: 'absolute',
      top: 12,
      right: -8,
      width: 0,
      height: 0,
      borderTop: '8px solid transparent',
      borderBottom: '8px solid transparent',
      borderLeft: (theme: Theme) => `8px solid ${theme.palette.background.paper}`,
    },

    '&::after': {
      content: '""',
      position: 'absolute',
      top: 11,
      right: -10,
      width: 0,
      height: 0,
      borderTop: '9px solid transparent',
      borderBottom: '9px solid transparent',
      borderLeft: '9px solid',
      borderLeftColor: '#505050',
      zIndex: -1,
    },
  }

  return (
    <Stack direction="row" sx={{ width: '100%', justifyContent: 'flex-end' }}>
      <Stack direction="row" spacing={1} sx={{ p: 0.5 }}>
        <Box sx={chatBubbleStyle}>
          <ReactMarkdown>{message.content}</ReactMarkdown>
        </Box>
        <Box>
          <Image src="/user.png" alt="user_icon" width={50} height={50} />
        </Box>
      </Stack>
    </Stack>
  )
}
