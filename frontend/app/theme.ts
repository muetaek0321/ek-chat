import { createTheme, Theme } from '@mui/material/styles'

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

// フォントサイズに基づくrem値を計算するヘルパー
// MUIのデフォルトベースは14px。スケール比率を計算して適用する。
const calcFontSizeRem = (basePx: number, remValue: number): string => {
  const scale = basePx / 14
  return `${remValue * scale}rem`
}

// テーマ生成関数
export const createAppTheme = (mode: 'light' | 'dark', fontSize: number = 16): Theme => {
  const palette = mode === 'light' ? lightPalette : darkPalette

  return createTheme({
    palette: {
      mode,
      primary: {
        main: palette.primary,
      },
      secondary: {
        main: palette.secondary,
      },
      background: {
        default: palette.background,
        paper: palette.surface,
      },
      text: {
        primary: palette.text,
        secondary: palette.textSecondary,
      },
      divider: palette.divider,
      custom: {
        input: palette.input,
        hover: palette.hover,
      },
    },
    typography: {
      fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
      fontSize,
      body1: {
        fontSize: calcFontSizeRem(fontSize, 1),
        color: palette.text,
      },
      body2: {
        fontSize: calcFontSizeRem(fontSize, 0.875),
        color: palette.textSecondary,
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
            backgroundColor: palette.surface,
          },
        },
      },
    },
  })
}

// デフォルトのテーマ（後方互換性のためにエクスポート）
export const lightTheme = createAppTheme('light')
export const darkTheme = createAppTheme('dark')

export const colorTokens = {
  light: lightPalette,
  dark: darkPalette,
}
