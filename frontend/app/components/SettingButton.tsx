'use client'

import { ChangeEvent, useState } from 'react'
import Button from '@mui/material/Button'
import Modal from '@mui/material/Modal'
import Box from '@mui/material/Box'
import Stack from '@mui/material/Stack'
import Typography from '@mui/material/Typography'
import TextField from '@mui/material/TextField'
import Select, { SelectChangeEvent } from '@mui/material/Select'
import MenuItem from '@mui/material/MenuItem'
import Tabs from '@mui/material/Tabs'
import Tab from '@mui/material/Tab'
import SettingsIcon from '@mui/icons-material/Settings'
import CloseIcon from '@mui/icons-material/Close'

import { CustomTabPanel, a11yProps } from './TabPanel'
import { ApiResponse, getRequest, patchRequest } from '@modules/fetchData'
import { SystemPrompt, ChatModelInfo, Settings } from '@types'
import { sidebarButtonStyle, commonModalStyle } from './commonStyles'

export interface SettingButtonProps {
  isRunning: boolean
}

export default function SettingButton({ isRunning }: SettingButtonProps) {
  const modalWidth = '50vw'
  const modalHeight = '480px'
  const [modalIsOpen, setModalIsOpen] = useState<boolean>(false)
  const [tabNumber, setTabNumber] = useState<number>(0)
  const tabContentHeight = '290px'

  const [systemPromptText, setSystemPromptText] = useState<string>('')
  const [chatModelList, setChatModelList] = useState<ChatModelInfo[]>([])
  const [selectedChatModel, setSelectedChatModel] = useState<string>('')

  // SystemPromptの取得
  const getSystemPrompt = async () => {
    await getRequest<Settings>('/settings')
      .then((res: ApiResponse<Settings>) => {
        if (res.success && res.data !== undefined) {
          // システムプロンプトを取得
          setSystemPromptText(res.data.systemPrompt.text)
          // チャットモデルの情報を取得
          setChatModelList(res.data.chatModelInfoList)
          setSelectedChatModel(
            res.data.chatModelInfoList.find((model) => model.isSelected)?.modelName || '',
          )
        } else {
          alert('設定項目の取得に失敗しました。')
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

  // チャットモデル情報の登録
  const registerChatModel = async () => {
    const chatModelSetting = {
      model: selectedChatModel,
    }
    await patchRequest<undefined>('/model', chatModelSetting)
      .then((res: ApiResponse<undefined>) => {
        if (res.success) {
          // 登録後にモーダルを閉じる
          setModalIsOpen(false)
        } else {
          alert('チャットモデルの登録に失敗しました。')
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

  // チャットモデル選択プルダウンの処理
  const handleSelectChatModel = (event: SelectChangeEvent<string>) => {
    setSelectedChatModel(event.target.value)
  }

  // 登録ボタンの処理
  const handleRegisterButton = () => {
    if (tabNumber === 0) {
      // SystemPromptが未入力状態の場合はアラート表示
      if (systemPromptText === '') {
        alert('未入力のため登録できません。')
      } else {
        registerSystemPrompt()
      }
    } else if (tabNumber === 1) {
      // チャットモデルの登録
      registerChatModel()
    } else {
      alert('Error: このタブの登録機能が設定されていません。')
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

          <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
            <Tabs
              value={tabNumber}
              onChange={(event: React.SyntheticEvent, number: number) => setTabNumber(number)}
              variant="fullWidth"
            >
              <Tab label="システムプロンプトの編集" {...a11yProps(0)} />
              <Tab label="チャットモデルの設定" {...a11yProps(1)} />
            </Tabs>
          </Box>

          {/* システムプロンプトの編集タブ */}
          <CustomTabPanel value={tabNumber} index={0} sx={{ height: tabContentHeight }}>
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
          </CustomTabPanel>

          {/* チャットモデルの設定タブ */}
          <CustomTabPanel value={tabNumber} index={1} sx={{ height: tabContentHeight }}>
            <Stack direction="row" sx={{ justifyContent: 'center', px: 2.5 }}>
              <Box sx={{ px: 1, py: 2 }}>
                <Typography variant="body1">チャットモデル選択:</Typography>
              </Box>
              <Select
                value={selectedChatModel}
                onChange={handleSelectChatModel}
                sx={{ width: `calc(${modalWidth} - 280px)`, bgcolor: '#ffffff' }}
              >
                {chatModelList.map((model) => (
                  <MenuItem key={model.modelName} value={model.modelName} disabled={!model.isUse}>
                    {model.modelName}
                  </MenuItem>
                ))}
              </Select>
            </Stack>
          </CustomTabPanel>

          <Stack direction="row-reverse" sx={{ p: 2 }}>
            <Button variant="contained" color="inherit" onClick={handleRegisterButton}>
              登録
            </Button>
          </Stack>
        </Box>
      </Modal>
    </Box>
  )
}
