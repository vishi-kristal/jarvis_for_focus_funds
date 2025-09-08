'use client'

import { Message } from '@/types'
import { cn } from '@/lib/utils'
import { User } from 'lucide-react'
import Image from 'next/image'

interface MessageBubbleProps {
  message: Message
}

export function MessageBubble({ message }: MessageBubbleProps) {
  const isUser = message.role === 'user'
  
  return (
    <div className={cn(
      'flex gap-4 p-6',
      isUser ? 'justify-end' : 'justify-start'
    )}>
      {!isUser && (
        <div className="flex-shrink-0">
          <div className="w-10 h-10 rounded-xl bg-white border border-slate-200 flex items-center justify-center shadow-sm overflow-hidden">
            <Image
              src="/kristalai_logo.jpeg"
              alt="Kristal.AI Logo"
              width={32}
              height={32}
              className="object-contain"
            />
          </div>
        </div>
      )}
      
      <div className={cn(
        'max-w-[75%] rounded-2xl px-5 py-4 shadow-sm',
        isUser 
          ? 'bg-gradient-to-br from-blue-600 to-indigo-600 text-white' 
          : 'bg-white border border-slate-200/60 text-slate-900'
      )}>
        <div className={cn(
          "prose prose-sm max-w-none",
          isUser ? "prose-invert" : ""
        )}>
          <div 
            className={cn(
              "whitespace-pre-wrap leading-relaxed",
              isUser ? "text-white" : ""
            )}
            dangerouslySetInnerHTML={{ 
              __html: formatMessageContent(message.content, isUser) 
            }}
          />
          
          {/* Display images if any */}
          {message.images && message.images.length > 0 && (
            <div className="mt-4 space-y-3">
              {message.images.map((image, index) => (
                <div key={index} className="rounded-lg overflow-hidden border border-slate-200 shadow-sm">
                  <img
                    src={`data:image/png;base64,${image}`}
                    alt={`Generated chart ${index + 1}`}
                    className="w-full h-auto max-w-full"
                    style={{ maxHeight: '500px', objectFit: 'contain' }}
                  />
                </div>
              ))}
            </div>
          )}
        </div>
        <div className={cn(
          'text-xs mt-3 opacity-60 font-medium',
          isUser ? 'text-blue-100' : 'text-slate-500'
        )}>
          {message.timestamp.toLocaleTimeString([], { 
            hour: '2-digit', 
            minute: '2-digit' 
          })}
        </div>
      </div>
      
      {isUser && (
        <div className="flex-shrink-0">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-slate-200 to-slate-300 flex items-center justify-center shadow-sm">
            <User className="w-5 h-5 text-slate-600" />
          </div>
        </div>
      )}
    </div>
  )
}

function formatMessageContent(content: string, isUser: boolean = false): string {
  const textColor = isUser ? 'text-white' : 'text-slate-900'
  const textColorSecondary = isUser ? 'text-blue-100' : 'text-slate-700'
  const headingColor = isUser ? 'text-white' : 'text-slate-900'
  
  // Convert markdown-like formatting to HTML with better styling
  return content
    // Handle tables first (before other formatting)
    .replace(/([^\n]*\|[^\n]*\n?)+/g, (match) => {
      const lines = match.trim().split('\n').filter(line => line.trim())
      if (lines.length < 2) return match
      
      // Check if this looks like a table (has multiple lines with | separators)
      const hasTableStructure = lines.every(line => line.includes('|'))
      if (!hasTableStructure) return match
      
      let tableHtml = '<div class="overflow-x-auto my-6"><table class="min-w-full border-collapse border border-slate-300 bg-white rounded-lg shadow-sm">'
      
      lines.forEach((line, index) => {
        const cells = line.split('|').map(cell => cell.trim()).filter(cell => cell)
        if (cells.length === 0) return
        
        // Skip separator lines (like "-------|-------")
        if (cells.every(cell => /^[-=]+$/.test(cell))) return
        
        const isHeader = index === 0
        const tag = isHeader ? 'th' : 'td'
        const cellClass = isHeader 
          ? `border border-slate-300 px-4 py-3 bg-slate-50 font-semibold text-left ${headingColor}`
          : `border border-slate-300 px-4 py-3 ${textColor}`
        
        tableHtml += `<tr class="${isHeader ? 'bg-slate-50' : 'hover:bg-slate-25'}">`
        cells.forEach(cell => {
          // Clean up cell content (remove extra spaces, handle special characters)
          const cleanCell = cell.replace(/^[-=]+$/, '').trim()
          if (cleanCell) {
            tableHtml += `<${tag} class="${cellClass}">${cleanCell}</${tag}>`
          }
        })
        tableHtml += `</tr>`
      })
      
      tableHtml += '</table></div>'
      return tableHtml
    })
    // Handle headers (####, ###, ##, #)
    .replace(/^#### (.*$)/gim, `<h4 class="text-base font-semibold mt-4 mb-2 ${headingColor}">$1</h4>`)
    .replace(/^### (.*$)/gim, `<h3 class="text-lg font-semibold mt-5 mb-3 ${headingColor}">$1</h3>`)
    .replace(/^## (.*$)/gim, `<h2 class="text-xl font-semibold mt-6 mb-3 ${headingColor}">$1</h2>`)
    .replace(/^# (.*$)/gim, `<h1 class="text-2xl font-bold mt-6 mb-4 ${headingColor}">$1</h1>`)
    // Handle bold and italic
    .replace(/\*\*(.*?)\*\*/g, `<strong class="font-semibold ${textColor}">$1</strong>`)
    .replace(/\*(.*?)\*/g, `<em class="italic ${textColorSecondary}">$1</em>`)
    // Handle lists
    .replace(/^\d+\. (.*$)/gim, `<li class="ml-4 mb-2 list-decimal ${textColor}">$1</li>`)
    .replace(/^\* (.*$)/gim, `<li class="ml-4 mb-2 list-disc ${textColor}">$1</li>`)
    .replace(/^- (.*$)/gim, `<li class="ml-4 mb-2 list-disc ${textColor}">$1</li>`)
    // Handle line breaks and paragraphs
    .replace(/\n\n/g, `</p><p class="mb-3 leading-relaxed ${textColor}">`)
    .replace(/\n/g, '<br>')
    .replace(/^(.*)$/gim, `<p class="mb-3 leading-relaxed ${textColor}">$1</p>`)
}
