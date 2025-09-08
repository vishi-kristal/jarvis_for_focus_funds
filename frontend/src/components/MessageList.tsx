'use client'

import { Message } from '@/types'
import { MessageBubble } from './MessageBubble'
import { LoadingIndicator } from './LoadingIndicator'
import { ProcessingIndicator, ProcessingSteps } from './ProcessingIndicator'

interface MessageListProps {
  messages: Message[]
  isLoading: boolean
}

export function MessageList({ messages, isLoading }: MessageListProps) {
  return (
    <div className="flex-1 overflow-y-auto">
      <div className="max-w-4xl mx-auto">
        {messages.map((message) => {
          if (message.isTyping) {
            return (
              <div key={message.id} className="flex gap-4 p-6">
                <div className="flex-shrink-0">
                  <div className="w-10 h-10 rounded-xl bg-white border border-slate-200 flex items-center justify-center shadow-sm overflow-hidden">
                    <img
                      src="/kristalai_logo.jpeg"
                      alt="Kristal.AI Logo"
                      className="w-8 h-8 object-contain"
                    />
                  </div>
                </div>
                <div className="flex-1">
                  <ProcessingSteps currentStage={message.processingStage || 'searching'} />
                </div>
              </div>
            )
          }
          return <MessageBubble key={message.id} message={message} />
        })}
        {isLoading && <LoadingIndicator />}
      </div>
    </div>
  )
}
