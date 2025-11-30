import { render, screen, waitFor } from '@testing-library/react'
import { vi } from 'vitest'
import { describe, it, expect, beforeEach } from 'vitest'
import userEvent from '@testing-library/user-event'
import App from '../App'

// Mock fetch globally
global.fetch = vi.fn()

describe('App Component', () => {
    beforeEach(() => {
        vi.clearAllMocks()
    })

    describe('Initial Render', () => {
        it('should render the main heading', () => {
            render(<App />)
            expect(screen.getByText('Life Story Game')).toBeTruthy()
        })

        it('should display initial greeting message', () => {
            render(<App />)
            // Updated to match actual greeting in App.jsx
            expect(screen.getByText(/Welcome! I'm here to help you tell your life story/i)).toBeTruthy()
        })

        it('should show input field and send button', () => {
            render(<App />)
            expect(screen.getByPlaceholderText(/Digite sua mensagem/i)).toBeTruthy()
            expect(screen.getByRole('button', { name: /Enviar/i })).toBeTruthy()
        })
    })

    describe('Message Sending', () => {
        it('should send message when button clicked', async () => {
            const user = userEvent.setup()
            global.fetch.mockResolvedValueOnce({
                ok: true,
                json: async () => ({
                    response: 'Great! Let me help you tell your story.',
                    model: 'gemini-2.0-flash',
                    attempts: 1,
                    phase: 'AGE_SELECTION',
                }),
            })

            render(<App />)
            const input = screen.getByPlaceholderText(/Digite sua mensagem/i)
            const button = screen.getByRole('button', { name: /Enviar/i })

            await user.type(input, 'yes')
            await user.click(button)

            await waitFor(() => {
                expect(screen.getByText(/Great! Let me help you tell your story./i)).toBeTruthy()
            })
        })
    })

    describe('Error Handling', () => {
        it('should handle network errors gracefully', async () => {
            const user = userEvent.setup()
            global.fetch.mockRejectedValueOnce(new Error('Network error'))

            render(<App />)
            const input = screen.getByPlaceholderText(/Digite sua mensagem/i)
            const button = screen.getByRole('button', { name: /Enviar/i })

            await user.type(input, 'test')
            await user.click(button)

            await waitFor(() => {
                expect(screen.getByText(/Sorry, an error occurred/i)).toBeTruthy()
            })
        })

        it('should handle API error responses', async () => {
            const user = userEvent.setup()
            global.fetch.mockResolvedValueOnce({
                ok: false,
                status: 500,
                json: async () => ({ error: 'Server error' }),
            })

            render(<App />)
            const input = screen.getByPlaceholderText(/Digite sua mensagem/i)
            const button = screen.getByRole('button', { name: /Enviar/i })

            await user.type(input, 'test')
            await user.click(button)

            await waitFor(() => {
                expect(screen.getByText(/Sorry, an error occurred/i)).toBeTruthy()
            })
        })
    })

    describe('Age Selection Flow', () => {
        it('should show age selection UI after saying yes to greeting', async () => {
            const user = userEvent.setup()
            global.fetch.mockResolvedValueOnce({
                ok: true,
                json: async () => ({
                    response: '',
                    phase: 'AGE_SELECTION',
                }),
            })

            render(<App />)
            const input = screen.getByPlaceholderText(/Digite sua mensagem/i)
            const button = screen.getByRole('button', { name: /Enviar/i })

            await user.type(input, 'yes')
            await user.click(button)

            // App shows age selection UI after GREETING -> AGE_SELECTION transition
            await waitFor(() => {
                expect(screen.getByText(/Select Your Age Range/i)).toBeTruthy()
            })
        })
    })

    describe('Input Behavior', () => {
        it('should clear input after sending message', async () => {
            const user = userEvent.setup()
            global.fetch.mockResolvedValueOnce({
                ok: true,
                json: async () => ({
                    response: 'Response',
                    phase: 'GREETING',
                }),
            })

            render(<App />)
            const input = screen.getByPlaceholderText(/Digite sua mensagem/i)
            const button = screen.getByRole('button', { name: /Enviar/i })

            await user.type(input, 'yes')
            await user.click(button)

            await waitFor(() => {
                expect(input.value).toBe('')
            })
        })
    })
})
