'use client'

import Button from '@mui/material/Button'
import ChatIcon from '@mui/icons-material/Chat'

import { sidebarButtonStyle } from './commonStyles'

export interface NewChatButtonProps {
  createNewChat: () => void
  isRunning: boolean
}

export default function NewChatButton({ createNewChat, isRunning }: NewChatButtonProps) {
  return (
    <Button
      variant="contained"
      color="inherit"
      startIcon={<ChatIcon fontSize="small" />}
      fullWidth
      onClick={createNewChat}
      disabled={isRunning}
      sx={sidebarButtonStyle}
    >
      新しいチャット
    </Button>
  )
}
