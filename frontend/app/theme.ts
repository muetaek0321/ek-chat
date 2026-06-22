import { createTheme } from '@mui/material/styles'

// パレットの型拡張
declare module '@mui/material/styles' {
  interface Palette {
    custom: {
      input: string
      hover: string
    }
  }

  interface PaletteOptions {
    custom?: {
      input?: string
      hover?: string
    }
  }
}

// カラーパレット定義
const lightPalette = {
  primary: '#1976D2',
  secondary: '#DC004E',
  background: '#FFFFFF',
  surface: '#F5F5F5',
  text: '#000000',
  textSecondary: '#666666',
  border: '#E0E0E0',
  divider: '#BDBDBD',
  input: '#FFFFFF',
  hover: '#F0F0F0',
}

const darkPalette = {
  primary: '#90CAF9',
  secondary: '#F48FB1',
  background: '#121212',
  surface: '#1E1E1E',
  text: '#FFFFFF',
  textSecondary: '#B0B0B0',
  border: '#424242',
  divider: '#616161',
  input: '#2E2E2E',
  hover: '#252525',
}

// ライトテーマ
export const lightTheme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: lightPalette.primary,
    },
    secondary: {
      main: lightPalette.secondary,
    },
    background: {
      default: lightPalette.background,
      paper: lightPalette.surface,
    },
    text: {
      primary: lightPalette.text,
      secondary: lightPalette.textSecondary,
    },
    divider: lightPalette.divider,
    custom: {
      input: lightPalette.input,
      hover: lightPalette.hover,
    },
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
    fontSize: 14,
    body1: {
      fontSize: '1rem',
      color: lightPalette.text,
    },
    body2: {
      fontSize: '0.875rem',
      color: lightPalette.textSecondary,
    },
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: 'none',
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          backgroundColor: lightPalette.surface,
        },
      },
    },
  },
})

// ダークテーマ
export const darkTheme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: darkPalette.primary,
    },
    secondary: {
      main: darkPalette.secondary,
    },
    background: {
      default: darkPalette.background,
      paper: darkPalette.surface,
    },
    text: {
      primary: darkPalette.text,
      secondary: darkPalette.textSecondary,
    },
    divider: darkPalette.divider,
    custom: {
      input: darkPalette.input,
      hover: darkPalette.hover,
    },
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
    fontSize: 14,
    body1: {
      fontSize: '1rem',
      color: darkPalette.text,
    },
    body2: {
      fontSize: '0.875rem',
      color: darkPalette.textSecondary,
    },
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: 'none',
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          backgroundColor: darkPalette.surface,
        },
      },
    },
  },
})

export const colorTokens = {
  light: lightPalette,
  dark: darkPalette,
}
