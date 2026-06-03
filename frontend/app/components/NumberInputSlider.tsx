'use client'

import React from 'react'
import Box from '@mui/material/Box'
import Stack from '@mui/material/Stack'
import Typography from '@mui/material/Typography'
import Slider from '@mui/material/Slider'
import TextField from '@mui/material/TextField'

export interface NumberInputSliderProps {
  value: number
  setValue: React.Dispatch<React.SetStateAction<number | undefined>>
  min: number
  max: number
  step: number
  label?: string
  marks?: boolean
}

export default function NumberInputSlider({
  value,
  setValue,
  min,
  max,
  step,
  label = '',
  marks = false,
}: NumberInputSliderProps) {
  return (
    <Box sx={{ px: 2, py: 2 }}>
      <Typography variant="body1">{label}</Typography>
      <Stack direction="row" spacing={2} sx={{ alignItems: 'center', px: 2, py: 0.5 }}>
        <TextField
          value={value}
          onChange={(event) => setValue(Number(event.target.value))}
          type="number"
          min={min}
          max={max}
          step={step}
          size="small"
          sx={{ width: 80, bgcolor: '#ffffff' }}
        />
        <Slider
          value={value}
          onChange={(event, newValue) => setValue(newValue as number)}
          min={min}
          max={max}
          step={step}
          valueLabelDisplay="auto"
          marks={marks}
        />
      </Stack>
    </Box>
  )
}
