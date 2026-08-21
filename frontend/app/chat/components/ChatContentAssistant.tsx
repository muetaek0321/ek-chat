'use client'

import ReactMarkdown from 'react-markdown'
import Image from 'next/image'
import Stack from '@mui/material/Stack'
import Box from '@mui/material/Box'
import IconButton from '@mui/material/IconButton'
import Tooltip from '@mui/material/Tooltip'
import InfoOutlinedIcon from '@mui/icons-material/InfoOutlined'
import { Theme } from '@mui/material/styles'

import { useTheme } from '../../ThemeProvider'
import { ChatMessage } from '@types'

export interface ChatContentAssistantProps {
  message: ChatMessage
}

// メタデータ表示用のダミーデータ
const dummyMetadata = {
  model: 'gemma4_12b',
  timestamp: '2026-08-21 12:00:00',
  tokens: '128',
  latency: '1.2s',
}

export default function ChatContentAssistant({ message }: ChatContentAssistantProps) {
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
      left: -8,
      width: 0,
      height: 0,
      borderTop: '8px solid transparent',
      borderBottom: '8px solid transparent',
      borderRight: (theme: Theme) => `8px solid ${theme.palette.background.paper}`,
    },

    '&::after': {
      content: '""',
      position: 'absolute',
      top: 11,
      left: -10,
      width: 0,
      height: 0,
      borderTop: '9px solid transparent',
      borderBottom: '9px solid transparent',
      borderRight: '9px solid',
      borderRightColor: '#505050',
      zIndex: -1,
    },
  }

  return (
    <Stack direction="row" sx={{ width: '100%', justifyContent: 'flex-start' }}>
      <Stack direction="row" spacing={1} sx={{ p: 0.5 }}>
        <Box>
          <Image src="/assistant.png" alt="assistant_icon" width={50} height={50} />
        </Box>
        <Box sx={{ position: 'relative', minHeight: 24 }}>
          <Box sx={chatBubbleStyle}>
            <ReactMarkdown>{message.content}</ReactMarkdown>
          </Box>
          <Tooltip title={JSON.stringify(dummyMetadata, null, 2)}>
            <IconButton
              aria-label="metadata"
              sx={{
                position: 'absolute',
                bottom: 4,
                right: 4,
                bgcolor: 'action.hover',
                '&:hover': { bgcolor: 'action.selected' },
              }}
            >
              <InfoOutlinedIcon fontSize="small" />
            </IconButton>
          </Tooltip>
        </Box>
      </Stack>
    </Stack>
  )
}
