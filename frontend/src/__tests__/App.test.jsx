/**
 * Unit tests for App component - Life Story Game AI Interviewer
 */
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import App from '../App'

// Mock fetch globally
global.fetch = vi.fn()

describe('App Component', () => {
    beforeEach(() => {
        // Reset mocks before each test
        vi.clearAllMocks()
    })

    describe('Initial Render', () => {
        it('should render the main heading', () => {
            render(<App />)
            expect(screen.getByText('Life Story Game')).toBeInTheDocument()
        })

        it('should display initial greeting message', () => {
            render(<App />)
            expect(screen.getByText(/Welcome to the Life Story Game!/i)).toBeInTheDocument()
        })

        it('should show input field and send button', () => {
            render(<App />)
            expect(screen.getByPlaceholderText(/Digite sua mensagem/i)).toBeInTheDocument()
            expect(screen.getByRole('button', { name: /Enviar/i })).toBeInTheDocument()
        })

        it('should display GREETING phase initially', () => {
            render(<App />)
            expect(screen.getByText(/Phase: GREETING/i)).toBeInTheDocument()
        })
    })

    describe('Message Sending', () => {
        it('should send message when form is submitted', async () => {
            const mockResponse = {
                response: 'This is a test AI response',
                model: 'gemini-2.5-flash',
                attempts: 1,
                phase: 'GREETING'
            }

            global.fetch.mockResolvedValueOnce({
                ok: true,
                json: async () => mockResponse
            })

            render(<App />)
            const user = userEvent.setup()

            const input = screen.getByPlaceholderText(/Digite sua mensagem/i)
            const button = screen.getByRole('button', { name: /Enviar/i })

            await user.type(input, 'yes')
            await user.click(button)

            await waitFor(() => {
                expect(global.fetch).toHaveBeenCalledWith('/api/chat', expect.objectContaining({
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                }))
            })
        })

        it('should display AI response after sending message', async () => {
            const mockResponse = {
                response: 'Great! Let me help you tell your story.',
                model: 'gemini-2.5-flash',
                attempts: 1,
                phase: 'ROUTE_SELECTION'
            }

            global.fetch.mockResolvedValueOnce({
                ok: true,
                json: async () => mockResponse
            })

            render(<App />)
            const user = userEvent.setup()

            const input = screen.getByPlaceholderText(/Digite sua mensagem/i)
            await user.type(input, 'yes')
            await user.click(screen.getByRole('button', { name: /Enviar/i }))

            await waitFor(() => {
                expect(screen.getByText('Great! Let me help you tell your story.')).toBeInTheDocument()
            })
        })

        it('should clear input after sending', async () => {
            global.fetch.mockResolvedValueOnce({
                ok: true,
                json: async () => ({ response: 'Response', model: 'test', attempts: 1, phase: 'GREETING' })
            })

            render(<App />)
            const user = userEvent.setup()

            const input = screen.getByPlaceholderText(/Digite sua mensagem/i)
            await user.type(input, 'test message')
            await user.click(screen.getByRole('button', { name: /Enviar/i }))

            await waitFor(() => {
                expect(input.value).toBe('')
            })
        })
    })

    describe('Error Handling', () => {
        it('should display error message on API failure', async () => {
            global.fetch.mockRejectedValueOnce(new Error('Network error'))

            render(<App />)
            const user = userEvent.setup()

            const input = screen.getByPlaceholderText(/Digite sua mensagem/i)
            await user.type(input, 'test')
            await user.click(screen.getByRole('button', { name: /Enviar/i }))

            await waitFor(() => {
                expect(screen.getByText(/Sorry, an error occurred/i)).toBeInTheDocument()
            })
        })

        it('should display error on non-200 response', async () => {
            global.fetch.mockResolvedValueOnce({
                ok: false,
                status: 500,
                statusText: 'Internal Server Error',
                json: async () => ({ error: 'Server error occurred' })
            })

            render(<App />)
            const user = userEvent.setup()

            const input = screen.getByPlaceholderText(/Digite sua mensagem/i)
            await user.type(input, 'test')
            await user.click(screen.getByRole('button', { name: /Enviar/i }))

            await waitFor(() => {
                expect(screen.getByText(/Sorry, an error occurred/i)).toBeInTheDocument()
            })
        })
    })

    describe('Route Selection', () => {
        it('should show route selection after GREETING phase', async () => {
            const mockResponse = {
                response: 'Here are your storytelling options...',
                model: 'test',
                attempts: 1,
                phase: 'ROUTE_SELECTION'
            }

            global.fetch.mockResolvedValueOnce({
                ok: true,
                json: async () => mockResponse
            })

            render(<App />)
            const user = userEvent.setup()

            await user.type(screen.getByPlaceholderText(/Digite sua mensagem/i), 'yes')
            await user.click(screen.getByRole('button', { name: /Enviar/i }))

            await waitFor(() => {
                expect(screen.getByText(/Choose Your Storytelling Approach/i)).toBeInTheDocument()
            })
        })

        it('should display all 7 route options', async () => {
            global.fetch.mockResolvedValueOnce({
                ok: true,
                json: async () => ({ response: 'Routes', model: 'test', attempts: 1, phase: 'ROUTE_SELECTION' })
            })

            render(<App />)
            const user = userEvent.setup()

            await user.type(screen.getByPlaceholderText(/Digite sua mensagem/i), 'yes')
            await user.click(screen.getByRole('button', { name: /Enviar/i }))

            await waitFor(() => {
                expect(screen.getByText(/Chronological Steward/i)).toBeInTheDocument()
                expect(screen.getByText(/Thematic Explorer/i)).toBeInTheDocument()
                expect(screen.getByText(/Legacy Weaver/i)).toBeInTheDocument()
                expect(screen.getByText(/Personal Route/i)).toBeInTheDocument()
            })
        })
    })

    describe('Loading State', () => {
        it('should show loading indicator while waiting for response', async () => {
            global.fetch.mockImplementationOnce(() => new Promise(resolve => setTimeout(() => resolve({
                ok: true,
                json: async () => ({ response: 'Response', model: 'test', attempts: 1, phase: 'GREETING' })
            }), 100)))

            render(<App />)
            const user = userEvent.setup()

            await user.type(screen.getByPlaceholderText(/Digite sua mensagem/i), 'test')
            await user.click(screen.getByRole('button', { name: /Enviar/i }))

            expect(screen.getByText(/Digitando.../i)).toBeInTheDocument()

            await waitFor(() => {
                expect(screen.queryByText(/Digitando.../i)).not.toBeInTheDocument()
            }, { timeout: 2000 })
        })

        it('should disable input and button while loading', async () => {
            global.fetch.mockImplementationOnce(() => new Promise(resolve => setTimeout(() => resolve({
                ok: true,
                json: async () => ({ response: 'Response', model: 'test', attempts: 1, phase: 'GREETING' })
            }), 100)))

            render(<App />)
            const user = userEvent.setup()

            const input = screen.getByPlaceholderText(/Digite sua mensagem/i)
            const button = screen.getByRole('button', { name: /Enviar/i })

            await user.type(input, 'test')
            await user.click(button)

            expect(input).toBeDisabled()
            expect(button).toBeDisabled()

            await waitFor(() => {
                expect(input).not.toBeDisabled()
                expect(button).not.toBeDisabled()
            }, { timeout: 2000 })
        })
    })
})
