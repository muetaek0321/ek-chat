import { render, screen } from '@testing-library/react'
import { describe, it, expect } from 'vitest'
import LoadingDialog from '../LoadingDialog'

describe('LoadingDialog', () => {
  it('renders correctly when open', () => {
    render(<LoadingDialog open={true} />)
    expect(screen.getByText('読み込み中...')).toBeInTheDocument()
    expect(screen.getByRole('progressbar')).toBeInTheDocument()
  })

  it('renders custom message when provided', () => {
    render(<LoadingDialog open={true} message="カスタムメッセージ" />)
    expect(screen.getByText('カスタムメッセージ')).toBeInTheDocument()
  })

  it('does not render when closed', () => {
    render(<LoadingDialog open={false} />)
    expect(screen.queryByText('読み込み中...')).not.toBeInTheDocument()
  })
})
