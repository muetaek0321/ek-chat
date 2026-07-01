'use client'

import { createContext, useContext, ReactNode } from 'react'
import { ThemeProvider as MuiThemeProvider, Theme } from '@mui/material/styles'
import CssBaseline from '@mui/material/CssBaseline'
import { createAppTheme } from './theme'

type ThemeMode = 'light' | 'dark'

interface ThemeContextType {
  mode: ThemeMode
  fontSize: number
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined)

export const useTheme = () => {
  const context = useContext(ThemeContext)
  if (!context) {
    throw new Error('useTheme must be used within ThemeProvider')
  }
  return context
}

interface ThemeProviderProps {
  children: ReactNode
  initialTheme: ThemeMode
  initialFontSize?: number
}

export const AppThemeProvider = ({
  children,
  initialTheme,
  initialFontSize = 16,
}: ThemeProviderProps) => {
  const mode = initialTheme
  const fontSize = initialFontSize

  const theme: Theme = createAppTheme(mode, fontSize)

  return (
    <ThemeContext.Provider value={{ mode, fontSize }}>
      <MuiThemeProvider theme={theme}>
        <CssBaseline />
        {children}
      </MuiThemeProvider>
    </ThemeContext.Provider>
  )
}
