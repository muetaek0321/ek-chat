'use client'

import { useState } from 'react'
import Button from '@mui/material/Button'
import SettingsIcon from '@mui/icons-material/Settings'

import { sidebarButtonStyle } from './commonStyles'

export interface SettingButtonProps {
  isRunning: boolean
}

export default function SettingButton({ isRunning }: SettingButtonProps) {
  const [modalIsOpen, setModalIsOpen] = useState<boolean>(false)

  return (
    <Button
      variant="contained"
      color="inherit"
      startIcon={<SettingsIcon fontSize="small" />}
      fullWidth
      onClick={() => setModalIsOpen(true)}
      disabled={isRunning}
      sx={sidebarButtonStyle}
    >
      設定
    </Button>
  )
}
