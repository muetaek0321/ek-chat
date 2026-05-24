'use client'

import { ChangeEvent, useState } from 'react'
import Button from '@mui/material/Button'
import Modal from '@mui/material/Modal'
import Box from '@mui/material/Box'
import Stack from '@mui/material/Stack'
import Typography from '@mui/material/Typography'
import TextField from '@mui/material/TextField'
import SettingsIcon from '@mui/icons-material/Settings'
import CloseIcon from '@mui/icons-material/Close'

import { ApiResponse, getRequest, patchRequest } from '@modules/fetchData'
import { SystemPrompt } from '@types'
import { sidebarButtonStyle, commonModalStyle } from './commonStyles'

export interface SettingButtonProps {
  isRunning: boolean
}

export default function SettingButton({ isRunning }: SettingButtonProps) {
  const modalWidth = '50vw'
  const modalHeight = '400px'
  const [modalIsOpen, setModalIsOpen] = useState<boolean>(false)

  const [systemPromptText, setSystemPromptText] = useState<string>('')

  // SystemPromptの取得
  const getSystemPrompt = async () => {
    await getRequest<SystemPrompt>('/system_prompt')
      .then((res: ApiResponse<SystemPrompt>) => {
        if (res.success && res.data !== undefined) {
          setSystemPromptText(res.data.text)
        } else {
          alert('システムプロンプトの取得に失敗しました。')
          console.log('Error:', res.error)
        }
      })
      .catch((err) => console.log('Error:', err))
  }

  // SystemPromptの登録
  const registerSystemPrompt = async () => {
    const editedSystemPrompt: SystemPrompt = {
      text: systemPromptText,
    }
    await patchRequest<undefined>('/system_prompt', editedSystemPrompt)
      .then((res: ApiResponse<undefined>) => {
        if (res.success) {
          // 登録後にモーダルを閉じる
          setModalIsOpen(false)
        } else {
          alert('システムプロンプトの登録に失敗しました。')
          console.log('Error:', res.error)
        }
      })
      .catch((err) => console.log('Error:', err))
  }

  // モーダルウィンドウを開いたときの処理
  const openModal = () => {
    setModalIsOpen(true)
    getSystemPrompt()
  }

  // SystemPromptの編集時の処理
  const handleEditSystemPrompt = (event: ChangeEvent<HTMLInputElement>) => {
    setSystemPromptText(event.target.value)
  }

  // SystemPromptの登録ボタンの処理
  const handleRegisterSystemPromptButton = () => {
    // 未入力状態の場合はアラート表示
    if (systemPromptText === '') {
      alert('未入力のため登録できません。')
    } else {
      registerSystemPrompt()
    }
  }

  return (
    <Box>
      <Button
        variant="contained"
        color="inherit"
        startIcon={<SettingsIcon fontSize="small" />}
        fullWidth
        onClick={openModal}
        disabled={isRunning}
        sx={sidebarButtonStyle}
      >
        設定
      </Button>

      <Modal
        open={modalIsOpen}
        onClose={() => setModalIsOpen(false)}
        sx={{ justifyContent: 'center' }}
      >
        <Box
          sx={{
            ...commonModalStyle,
            width: modalWidth,
            height: modalHeight,
          }}
        >
          <Stack direction="row" sx={{ justifyContent: 'space-between', p: 2 }}>
            <Typography variant="h6">
              <b>設定</b>
            </Typography>
            <Button
              color="inherit"
              variant="contained"
              sx={{ minWidth: 0, width: 50 }}
              onClick={() => setModalIsOpen(false)}
            >
              <CloseIcon fontSize="small" />
            </Button>
          </Stack>

          <Stack direction="row" sx={{ justifyContent: 'center', px: 2.5 }}>
            <TextField
              value={systemPromptText}
              onChange={handleEditSystemPrompt}
              multiline
              rows={10}
              maxRows={10}
              fullWidth
              sx={{ bgcolor: '#ffffff' }}
            />
          </Stack>

          <Stack direction="row-reverse" sx={{ p: 2 }}>
            <Button variant="contained" color="inherit" onClick={handleRegisterSystemPromptButton}>
              登録
            </Button>
          </Stack>
        </Box>
      </Modal>
    </Box>
  )
}
