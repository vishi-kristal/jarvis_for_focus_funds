'use client'

import { useState, useCallback } from 'react'
import { Message } from '@/types'
import { MessageList } from './MessageList'
import { UserInput } from './UserInput'
import { ProcessingIndicator, ProcessingSteps } from './ProcessingIndicator'
import { askQuestion, ApiError } from '@/lib/api'
import { AlertCircle, RefreshCw, TrendingUp } from 'lucide-react'
import Image from 'next/image'

export function ChatWindow() {
  const [messages, setMessages] = useState<Message[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [processingStage, setProcessingStage] = useState<'searching' | 'complete'>('searching')

  const handleSendMessage = useCallback(async (content: string) => {
    if (!content.trim()) return

    // Add user message
    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content,
      timestamp: new Date()
    }

    setMessages(prev => [...prev, userMessage])
    setIsLoading(true)
    setError(null)
    setProcessingStage('searching')

    // Add typing indicator message
    const typingMessage: Message = {
      id: (Date.now() + 1).toString(),
      role: 'assistant',
      content: '',
      timestamp: new Date(),
      isTyping: true,
      processingStage: 'searching'
    }
    setMessages(prev => [...prev, typingMessage])

    try {
      // Simulate document search processing
      setProcessingStage('searching')
      await new Promise(resolve => setTimeout(resolve, 1500))

      const result = await askQuestion(content)
      
      // Remove typing indicator and add real response
      setMessages(prev => prev.filter(msg => msg.id !== typingMessage.id))
      
      const assistantMessage: Message = {
        id: (Date.now() + 2).toString(),
        role: 'assistant',
        content: result.answer,
        timestamp: new Date(),
        processingStage: 'complete',
        images: result.images
      }

      setMessages(prev => [...prev, assistantMessage])
      setProcessingStage('complete')
    } catch (err) {
      // Remove typing indicator
      setMessages(prev => prev.filter(msg => msg.id !== typingMessage.id))
      
      let errorMessage = 'An unexpected error occurred. Please try again.'
      
      if (err instanceof ApiError) {
        if (err.status === 0) {
          errorMessage = 'Unable to connect to the backend server. Please check if the backend is running.'
        } else {
          errorMessage = err.message
        }
      }
      
      setError(errorMessage)
    } finally {
      setIsLoading(false)
      setProcessingStage('searching')
    }
  }, [])

  const handleRetry = useCallback(() => {
    setError(null)
  }, [])

  const showWelcome = messages.length === 0 && !isLoading

  return (
    <div className="flex flex-col h-full bg-gradient-to-br from-slate-50 to-blue-50">
      {/* Header */}
      <div className="bg-white/80 backdrop-blur-sm border-b border-slate-200/60 px-6 py-5">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-white flex items-center justify-center border border-slate-200 overflow-hidden">
              <Image
                src="/kristalai_logo.jpeg"
                alt="Kristal.AI Logo"
                width={32}
                height={32}
                className="object-contain"
              />
            </div>
            <div>
              <h1 className="text-xl font-bold text-slate-900">
                Kristal.AI's J.A.R.V.I.S
              </h1>
              <p className="text-sm text-slate-600">
                Intelligent fund analysis and insights
              </p>
            </div>
          </div>
          <div className="flex items-center gap-2 px-3 py-1.5 bg-green-50 rounded-full">
            <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
            <span className="text-xs font-medium text-green-700">Online</span>
          </div>
        </div>
      </div>

      {/* Error Banner */}
      {error && (
        <div className="bg-red-50/80 backdrop-blur-sm border-b border-red-200/60 px-6 py-3">
          <div className="flex items-center gap-3">
            <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0" />
            <div className="flex-1">
              <p className="text-sm text-red-800">{error}</p>
            </div>
            <button
              onClick={handleRetry}
              className="flex items-center gap-1 text-sm text-red-600 hover:text-red-800 transition-colors px-2 py-1 rounded-md hover:bg-red-100"
            >
              <RefreshCw className="w-4 h-4" />
              Retry
            </button>
          </div>
        </div>
      )}

      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {showWelcome ? (
          <div className="flex-1 flex items-center justify-center p-8">
            <div className="text-center max-w-md">
              <div className="w-16 h-16 mx-auto mb-6 rounded-2xl bg-white flex items-center justify-center border border-slate-200 shadow-sm overflow-hidden">
                <Image
                  src="/kristalai_logo.jpeg"
                  alt="Kristal.AI Logo"
                  width={48}
                  height={48}
                  className="object-contain"
                />
              </div>
              <h2 className="text-2xl font-bold text-slate-900 mb-3">
                Welcome to Kristal.AI's J.A.R.V.I.S
              </h2>
              <p className="text-slate-600 mb-6 leading-relaxed">
                Ask questions about investment funds, analyze strategies, compare performance metrics, 
                and get detailed insights from our AI-powered analysis system.
              </p>
              <div className="text-sm text-slate-500">
                Try asking: "What funds are available?" or "Compare the investment strategies"
              </div>
            </div>
          </div>
        ) : (
          <MessageList messages={messages} isLoading={isLoading} />
        )}
      </div>

      {/* Input */}
      <div className="bg-white/80 backdrop-blur-sm border-t border-slate-200/60">
        <UserInput 
          onSendMessage={handleSendMessage}
          disabled={isLoading}
        />
      </div>
    </div>
  )
}
