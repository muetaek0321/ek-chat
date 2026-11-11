import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import UserInput from '../UserInput'
import { AppThemeProvider } from '@AppThemeProvider'
import { postRequest } from '@lib/fetchData'

vi.mock('@lib/fetchData', () => ({
  postRequest: vi.fn(),
}))

describe('UserInput', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('renders input field and send button', () => {
    render(
      <AppThemeProvider initialTheme="light">
        <UserInput
          setChatHistory={() => {}}
          setChatInfoList={() => {}}
          isRunning={false}
          setIsRunning={() => {}}
        />
      </AppThemeProvider>
    )
    expect(screen.getByRole('textbox')).toBeInTheDocument()
    const sendButton = screen.getByRole('button', { name: '送信' })
    expect(sendButton).toBeInTheDocument()
    expect(sendButton).toBeDisabled() // disabled when input is empty
    expect(screen.getByText('option')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'オプションを開く' })).toBeInTheDocument()
  })

  it('enables button when text is entered and calls API on click', async () => {
    const setIsRunningMock = vi.fn()
    const setChatHistoryMock = vi.fn()
    const setChatInfoListMock = vi.fn()

    // Mock successful API response
    vi.mocked(postRequest).mockResolvedValue({
      success: true,
      data: {
        assistantMessage: { role: 'assistant', content: 'Hello' },
      },
    })

    render(
      <AppThemeProvider initialTheme="light">
        <UserInput
          setChatHistory={setChatHistoryMock}
          setChatInfoList={setChatInfoListMock}
          isRunning={false}
          setIsRunning={setIsRunningMock}
        />
      </AppThemeProvider>,
    )

    const input = screen.getByRole('textbox')
    const button = screen.getByRole('button', { name: '送信' })

    fireEvent.change(input, { target: { value: 'Hi' } })
    expect(button).not.toBeDisabled()

    fireEvent.click(button)

    expect(setIsRunningMock).toHaveBeenCalledWith(true)
    expect(postRequest).toHaveBeenCalledWith('/chat/generate', {
      userMessage: { role: 'user', content: 'Hi' },
      isRagEnabled: true,
    })

    await waitFor(() => {
      expect(setIsRunningMock).toHaveBeenCalledWith(false)
    })
  })

  it('renders circular progress overlaid on SendIcon when isRunning is true', () => {
    render(
      <AppThemeProvider initialTheme="light">
        <UserInput
          setChatHistory={() => {}}
          setChatInfoList={() => {}}
          isRunning={true}
          setIsRunning={() => {}}
        />
      </AppThemeProvider>,
    )
    expect(screen.getByRole('progressbar')).toBeInTheDocument()
    expect(screen.getByTestId('SendIcon')).toBeInTheDocument()
    const button = screen.getByRole('button', { name: '送信' })
    expect(button).toBeDisabled()
    const optionButton = screen.getByRole('button', { name: 'オプションを開く' })
    expect(optionButton).toBeDisabled()
  })

  it('toggles option area to show and hide control icon buttons', () => {
    render(
      <AppThemeProvider initialTheme="light">
        <UserInput
          setChatHistory={() => {}}
          setChatInfoList={() => {}}
          isRunning={false}
          setIsRunning={() => {}}
        />
      </AppThemeProvider>,
    )

    const optionButton = screen.getByRole('button', { name: 'オプションを開く' })
    expect(optionButton).toHaveAttribute('aria-expanded', 'false')
    expect(screen.getByText('option')).toBeInTheDocument()

    // オプションをクリックして展開（「option」文字は消え、アイコンが横並びになる）
    fireEvent.click(optionButton)
    expect(screen.queryByText('option')).not.toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'オプションを閉じる' })).toHaveAttribute(
      'aria-expanded',
      'true',
    )
    expect(screen.getByRole('button', { name: 'モード設定' })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'AI機能' })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: '思考モード' })).toBeInTheDocument()

    // もう一度クリックして折りたたみ（「option」文字が再表示される）
    fireEvent.click(screen.getByRole('button', { name: 'オプションを閉じる' }))
    expect(screen.getByText('option')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'オプションを開く' })).toHaveAttribute(
      'aria-expanded',
      'false',
    )
    expect(screen.queryByRole('button', { name: 'モード設定' })).not.toBeInTheDocument()
  })
})
