import { useState } from 'react'

function App() {
  // Estado para armazenar as mensagens do chat
  const [messages, setMessages] = useState([
    { role: 'assistant', content: 'Olá! Bem-vindo à Pizzaria Delícia! 🍕\nVocê gostaria de fazer um pedido? (sim/não)' }
  ])
  
  // Estado para o texto do input
  const [input, setInput] = useState('')
  
  // Estado para loading
  const [isLoading, setIsLoading] = useState(false)
  
  // Estado para erros
  const [error, setError] = useState(null)

  // Função que é chamada quando o formulário é enviado
  const handleSubmit = async (e) => {
    e.preventDefault() // Previne o comportamento padrão do formulário
    
    // Se o input estiver vazio, não faz nada
    if (!input.trim() || isLoading) return

    const userMessage = input.trim()
    
    // Adiciona a mensagem do usuário ao array de mensagens
    const newUserMessage = { role: 'user', content: userMessage }
    const updatedMessages = [...messages, newUserMessage]
    setMessages(updatedMessages)
    
    // Limpa o input e erros anteriores
    setInput('')
    setError(null)
    setIsLoading(true)

    try {
      // Chama a API do backend enviando todo o histórico de mensagens
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ messages: updatedMessages }),
      })

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ error: 'Erro desconhecido' }))
        throw new Error(errorData.error || `Erro ${response.status}: ${response.statusText}`)
      }

      const data = await response.json()
      
      // Adiciona a resposta do assistente
      setMessages([...updatedMessages, { role: 'assistant', content: data.response }])
      
    } catch (err) {
      console.error('Erro ao chamar API:', err)
      setError(err.message || 'Erro ao conectar com o servidor. Verifique se o backend está rodando.')
      
      // Adiciona mensagem de erro ao chat
      setMessages([
        ...updatedMessages,
        { role: 'assistant', content: `Desculpe, ocorreu um erro: ${err.message || 'Erro desconhecido'}` }
      ])
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-900 text-white flex flex-col">
      <h1 className="text-2xl font-bold p-4 border-b border-gray-700">Chatbot</h1>
      
      {/* Área de mensagens - ocupa o espaço disponível */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                msg.role === 'user'
                  ? 'bg-blue-600'
                  : 'bg-gray-700'
              }`}
            >
              <div className="whitespace-pre-wrap break-words">
                {msg.content}
              </div>
            </div>
          </div>
        ))}
        
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-gray-700 px-4 py-2 rounded-lg">
              <span className="animate-pulse">Digitando...</span>
            </div>
          </div>
        )}
        
        {error && (
          <div className="flex justify-center">
            <div className="bg-red-900 border border-red-700 text-red-200 px-4 py-2 rounded-lg text-sm">
              {error}
            </div>
          </div>
        )}
      </div>

      {/* Formulário de input - fica fixo na parte inferior */}
      <form onSubmit={handleSubmit} className="p-4 border-t border-gray-700">
        <div className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Digite sua mensagem..."
            className="flex-1 p-3 rounded-lg bg-gray-800 border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500 text-white placeholder-gray-400 disabled:opacity-50"
            disabled={isLoading}
          />
          <button
            type="submit"
            disabled={isLoading || !input.trim()}
            className="px-6 py-3 bg-blue-600 rounded-lg font-semibold hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-600 disabled:cursor-not-allowed"
          >
            Enviar
          </button>
        </div>
      </form>
    </div>
  )
}

export default App