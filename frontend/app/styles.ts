import { Theme } from '@mui/material/styles'
import { CSSObject } from '@emotion/react'
import { colorTokens } from './theme'

// ===============================
// カラートークン
// ===============================
export const colors = colorTokens

// ===============================
// 共通スタイル
// ===============================

// サイドバーに設置するボタンの共通スタイル
export const sidebarButtonStyle = {
  justifyContent: 'center',
  height: 40,
  textTransform: 'none',
  fontSize: '1rem',
  position: 'relative',
  '& .MuiButton-startIcon': {
    position: 'absolute',
    left: 20,
    margin: 0,
  },
}

// モーダルウィンドウの共通スタイル
export const commonModalStyle = (theme: Theme): CSSObject => ({
  position: 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  borderRadius: 1,
  border: 1,
  bgcolor: theme.palette.background.paper,
  boxShadow: theme.shadows[5],
})

// ===============================
// レスポンシブ対応スタイル
// ===============================

// コンテナのパディング
export const containerPadding = {
  xs: '0.5rem',
  sm: '1rem',
  md: '1.5rem',
  lg: '2rem',
}

// セクションのマージン
export const sectionMargin = {
  xs: '0.5rem 0',
  sm: '1rem 0',
  md: '1.5rem 0',
  lg: '2rem 0',
}

// ===============================
// テキストスタイル
// ===============================

// フォントサイズに基づくrem値を計算するヘルパー
const calcFontSizeRem = (basePx: number, remValue: number): string => {
  const scale = basePx / 14
  return `${remValue * scale}rem`
}

// フォントサイズに応じたテキストバリアントを生成する関数
export const createTextVariants = (fontSize: number = 16) => ({
  heading1: {
    fontSize: calcFontSizeRem(fontSize, 2),
    fontWeight: 700,
    lineHeight: 1.2,
  },
  heading2: {
    fontSize: calcFontSizeRem(fontSize, 1.5),
    fontWeight: 600,
    lineHeight: 1.3,
  },
  heading3: {
    fontSize: calcFontSizeRem(fontSize, 1.25),
    fontWeight: 600,
    lineHeight: 1.4,
  },
  body: {
    fontSize: calcFontSizeRem(fontSize, 1),
    fontWeight: 400,
    lineHeight: 1.5,
  },
  bodySmall: {
    fontSize: calcFontSizeRem(fontSize, 0.875),
    fontWeight: 400,
    lineHeight: 1.5,
  },
  caption: {
    fontSize: calcFontSizeRem(fontSize, 0.75),
    fontWeight: 400,
    lineHeight: 1.4,
  },
})

// デフォルトのテキストバリアント（後方互換性のためにエクスポート）
export const textVariants = createTextVariants()

// ===============================
// ボーダースタイル
// ===============================

export const borderStyles = {
  light: {
    border: `1px solid ${colorTokens.light.border}`,
    borderRadius: '4px',
  },
  dark: {
    border: `1px solid ${colorTokens.dark.border}`,
    borderRadius: '4px',
  },
}

// ===============================
// シャドウスタイル
// ===============================

export const shadowStyles = {
  subtle: (theme: Theme): CSSObject => ({
    boxShadow: theme.shadows[1],
  }),
  medium: (theme: Theme): CSSObject => ({
    boxShadow: theme.shadows[3],
  }),
  elevated: (theme: Theme): CSSObject => ({
    boxShadow: theme.shadows[8],
  }),
}

// ===============================
// ホバー/フォーカススタイル
// ===============================

export const interactionStyles = {
  buttonHover: (theme: Theme): CSSObject => ({
    cursor: 'pointer',
    opacity: 0.8,
    transition: theme.transitions.create(['opacity', 'box-shadow'], {
      duration: theme.transitions.duration.short,
    }),
    '&:hover': {
      opacity: 1,
    },
  }),
  focusVisible: (theme: Theme): CSSObject => ({
    outline: `2px solid ${theme.palette.primary.main}`,
    outlineOffset: '2px',
  }),
}

// ===============================
// レイアウトスタイル
// ===============================

export const flexCenter = {
  display: 'flex',
  justifyContent: 'center',
  alignItems: 'center',
}

export const flexBetween = {
  display: 'flex',
  justifyContent: 'space-between',
  alignItems: 'center',
}

export const columnLayout = {
  display: 'flex',
  flexDirection: 'column',
}
