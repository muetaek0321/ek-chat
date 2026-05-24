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
export const commonModalStyle = {
  position: 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  bgcolor: '#F0F0F0',
  border: 1,
  borderRadius: 1,
}
