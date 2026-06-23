import { render, screen, fireEvent } from '@testing-library/react'
import { describe, it, expect, vi } from 'vitest'
import SelectToggleButton from '../SelectToggleButton'
import { AppThemeProvider } from '../../ThemeProvider'

describe('SelectToggleButton', () => {
  const buttonLabels = ['Option 1', 'Option 2', 'Option 3']

  it('renders correctly with label and buttons', () => {
    render(
      <AppThemeProvider initialTheme="light">
        <SelectToggleButton
          value="Option 1"
          setValue={() => {}}
          buttonLabels={buttonLabels}
          label="Select Option"
        />
      </AppThemeProvider>
    )
    expect(screen.getByText('Select Option')).toBeInTheDocument()
    buttonLabels.forEach(label => {
      expect(screen.getByText(label)).toBeInTheDocument()
    })
  })

  it('calls setValue when a button is clicked', () => {
    const setValueMock = vi.fn()
    render(
      <AppThemeProvider initialTheme="light">
        <SelectToggleButton
          value="Option 1"
          setValue={setValueMock}
          buttonLabels={buttonLabels}
        />
      </AppThemeProvider>
    )
    
    const button2 = screen.getByRole('button', { name: 'Option 2' })
    fireEvent.click(button2)
    
    expect(setValueMock).toHaveBeenCalledWith('Option 2')
  })
})
