'use client'

import { useState, useEffect } from 'react'
import Dialog from '@mui/material/Dialog'
import DialogContent from '@mui/material/DialogContent'
import Stack from '@mui/material/Stack'
import Typography from '@mui/material/Typography'
import CircularProgress from '@mui/material/CircularProgress'

export interface LoadingDialogProps {
  open: boolean
  message?: string
}

export default function LoadingDialog({ open, message = '読み込み中...' }: LoadingDialogProps) {
  return (
    <Dialog open={open}>
      <DialogContent>
        <Stack spacing={3} sx={{ alignItems: 'center' }}>
          <CircularProgress color="inherit" size={48} />
          <Typography variant="body1" color="text.secondary">
            {message}
          </Typography>
        </Stack>
      </DialogContent>
    </Dialog>
  )
}
