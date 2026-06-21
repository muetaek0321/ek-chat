'use client'

import { createContext, useContext, ReactNode } from 'react'
import { ThemeProvider as MuiThemeProvider, Theme } from '@mui/material/styles'
import CssBaseline from '@mui/material/CssBaseline'
import { lightTheme, darkTheme } from './theme'

type ThemeMode = 'light' | 'dark'

interface ThemeContextType {
  mode: ThemeMode
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
}

const getInitialTheme = (): ThemeMode => {
  const defaultTheme = (process.env.NEXT_PUBLIC_DEFAULT_THEME as ThemeMode) || 'light'
  return defaultTheme
}

export const AppThemeProvider = ({ children }: ThemeProviderProps) => {
  const mode = getInitialTheme()

  const theme: Theme = mode === 'light' ? lightTheme : darkTheme

  return (
    <ThemeContext.Provider value={{ mode: mode }}>
      <MuiThemeProvider theme={theme}>
        <CssBaseline />
        {children}
      </MuiThemeProvider>
    </ThemeContext.Provider>
  )
}
