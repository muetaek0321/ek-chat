import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import ChatList from '../ChatList'
import { AppThemeProvider } from '../../../ThemeProvider'
import { deleteRequest } from '@lib/fetchData'

vi.mock('@lib/fetchData', () => ({
  deleteRequest: vi.fn(),
}))

describe('ChatList', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  const mockChatInfoList = [
    { chatId: '1', title: 'Chat 1' },
    { chatId: '2', title: 'Chat 2' },
  ]

  it('renders chat list correctly', () => {
    render(
      <AppThemeProvider initialTheme="light">
        <ChatList
          chatInfoList={mockChatInfoList}
          setChatInfoList={() => {}}
          getChatHistory={() => {}}
          createNewChat={() => {}}
          isRunning={false}
        />
      </AppThemeProvider>
    )
    expect(screen.getByText('Chat 1')).toBeInTheDocument()
    expect(screen.getByText('Chat 2')).toBeInTheDocument()
  })

  it('calls getChatHistory on chat click', () => {
    const getChatHistoryMock = vi.fn()
    render(
      <AppThemeProvider initialTheme="light">
        <ChatList
          chatInfoList={mockChatInfoList}
          setChatInfoList={() => {}}
          getChatHistory={getChatHistoryMock}
          createNewChat={() => {}}
          isRunning={false}
        />
      </AppThemeProvider>
    )
    
    fireEvent.click(screen.getByText('Chat 1'))
    expect(getChatHistoryMock).toHaveBeenCalledWith('1')
  })

  it('calls deleteRequest and updates list on delete button click', async () => {
    const setChatInfoListMock = vi.fn()
    const getChatHistoryMock = vi.fn()
    vi.mocked(deleteRequest).mockResolvedValue({ success: true })

    render(
      <AppThemeProvider initialTheme="light">
        <ChatList
          chatInfoList={mockChatInfoList}
          setChatInfoList={setChatInfoListMock}
          getChatHistory={getChatHistoryMock}
          createNewChat={() => {}}
          isRunning={false}
        />
      </AppThemeProvider>
    )

    // Two chats, so two delete buttons
    const deleteButtons = screen.getAllByRole('button')
    fireEvent.click(deleteButtons[1]) // click delete on Chat 2

    expect(deleteRequest).toHaveBeenCalledWith('/delete?chatId=2')

    await waitFor(() => {
      expect(setChatInfoListMock).toHaveBeenCalled()
    })
  })
})
