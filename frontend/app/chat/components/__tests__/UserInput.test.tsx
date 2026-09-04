import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import UserInput from '../UserInput'
import { AppThemeProvider } from '../../../ThemeProvider'
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
    const button = screen.getByRole('button')
    expect(button).toBeInTheDocument()
    expect(button).toBeDisabled() // disabled when input is empty
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
      </AppThemeProvider>
    )

    const input = screen.getByRole('textbox')
    const button = screen.getByRole('button')

    fireEvent.change(input, { target: { value: 'Hi' } })
    expect(button).not.toBeDisabled()

    fireEvent.click(button)

    expect(setIsRunningMock).toHaveBeenCalledWith(true)
    expect(postRequest).toHaveBeenCalledWith('/chat', { role: 'user', content: 'Hi' })

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
      </AppThemeProvider>
    )
    expect(screen.getByRole('progressbar')).toBeInTheDocument()
    expect(screen.getByTestId('SendIcon')).toBeInTheDocument()
    const button = screen.getByRole('button')
    expect(button).toBeDisabled()
  })
})

