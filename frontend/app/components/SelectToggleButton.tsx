'use client'

import React, { MouseEvent } from 'react'
import Box from '@mui/material/Box'
import Typography from '@mui/material/Typography'
import ToggleButton from '@mui/material/ToggleButton'
import ToggleButtonGroup from '@mui/material/ToggleButtonGroup'

export interface SelectToggleButtonProps {
  value: string
  setValue: React.Dispatch<React.SetStateAction<string | undefined>>
  buttonLabels: string[]
  label?: string
}

export default function SelectToggleButton({
  value,
  setValue,
  buttonLabels,
  label = '',
}: SelectToggleButtonProps) {
  return (
    <Box sx={{ px: 2, py: 2 }}>
      <Typography variant="body1">{label}</Typography>
      <ToggleButtonGroup
        color="primary"
        value={value}
        exclusive
        onChange={(event: MouseEvent<HTMLElement>, newValue: string) => setValue(newValue)}
        fullWidth
        sx={{ bgcolor: '#ffffff' }}
      >
        {buttonLabels.map((buttonLabel) => (
          <ToggleButton key={buttonLabel} value={buttonLabel}>
            <b>{buttonLabel}</b>
          </ToggleButton>
        ))}
      </ToggleButtonGroup>
    </Box>
  )
}
