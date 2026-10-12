'use client'

import type { ReactNode } from 'react'
import { useRouter } from 'next/navigation'
import Box from '@mui/material/Box'
import Button from '@mui/material/Button'
import ChatOutlinedIcon from '@mui/icons-material/ChatOutlined'
import StorageSharpIcon from '@mui/icons-material/StorageSharp'

import { sidebarButtonStyle } from '@styles'

interface TargetContentItem {
  title: string
  icon: ReactNode
}

interface TargetContent {
  [key: string]: TargetContentItem
}

export interface SwitchPageButtonProps {
  target: string
  isRunning?: boolean
}

export default function SwitchPageButton({ target, isRunning = false }: SwitchPageButtonProps) {
  const router = useRouter()

  // 遷移先ページ指定に応じて表示を変更
  const targetContent: TargetContent = {
    chat: {
      title: 'チャット',
      icon: <ChatOutlinedIcon fontSize="small" />,
    },
    database: {
      title: 'データベース',
      icon: <StorageSharpIcon fontSize="small" />,
    },
  }

  return (
    <Box sx={{ py: 0.5 }}>
      <Button
        variant="outlined"
        color="inherit"
        startIcon={targetContent[target]?.icon}
        fullWidth
        onClick={() => router.push(`/${target}`)}
        disabled={isRunning}
        sx={sidebarButtonStyle}
      >
        <b>{targetContent[target]?.title}</b> へ移動
      </Button>
    </Box>
  )
}
