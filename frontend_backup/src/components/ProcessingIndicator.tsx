'use client'

import { useState, useEffect } from 'react'
import { Brain, Search, Calculator, BarChart3, CheckCircle } from 'lucide-react'
import { cn } from '@/lib/utils'

interface ProcessingIndicatorProps {
  stage: 'searching' | 'calculating' | 'analyzing' | 'complete'
  className?: string
}

const stageConfig = {
  searching: {
    icon: Search,
    title: 'Searching documents...',
    description: 'Looking through fund documents for context',
    color: 'text-blue-600',
    bgColor: 'bg-blue-50',
    iconColor: 'text-blue-600'
  },
  calculating: {
    icon: Calculator,
    title: 'Running calculations...',
    description: 'Processing financial metrics with code interpreter',
    color: 'text-purple-600',
    bgColor: 'bg-purple-50',
    iconColor: 'text-purple-600'
  },
  analyzing: {
    icon: BarChart3,
    title: 'Analyzing results...',
    description: 'Combining insights and formatting response',
    color: 'text-green-600',
    bgColor: 'bg-green-50',
    iconColor: 'text-green-600'
  },
  complete: {
    icon: CheckCircle,
    title: 'Complete!',
    description: 'Analysis finished',
    color: 'text-green-600',
    bgColor: 'bg-green-50',
    iconColor: 'text-green-600'
  }
}

export function ProcessingIndicator({ stage, className }: ProcessingIndicatorProps) {
  const [dots, setDots] = useState('')
  
  useEffect(() => {
    if (stage === 'complete') return
    
    const interval = setInterval(() => {
      setDots(prev => {
        if (prev === '...') return ''
        return prev + '.'
      })
    }, 500)
    
    return () => clearInterval(interval)
  }, [stage])
  
  const config = stageConfig[stage]
  const Icon = config.icon
  
  return (
    <div className={cn(
      'flex items-center gap-4 p-4 rounded-xl border',
      config.bgColor,
      'border-slate-200/60',
      className
    )}>
      <div className={cn(
        'w-10 h-10 rounded-xl flex items-center justify-center',
        config.iconColor === 'text-blue-600' ? 'bg-blue-100' :
        config.iconColor === 'text-purple-600' ? 'bg-purple-100' :
        'bg-green-100'
      )}>
        <Icon className={cn('w-5 h-5', config.iconColor)} />
      </div>
      
      <div className="flex-1">
        <div className={cn('text-sm font-medium', config.color)}>
          {config.title}{stage !== 'complete' && dots}
        </div>
        <div className="text-xs text-slate-600 mt-1">
          {config.description}
        </div>
      </div>
      
      {stage !== 'complete' && (
        <div className="flex space-x-1">
          <div className="w-2 h-2 bg-current rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
          <div className="w-2 h-2 bg-current rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
          <div className="w-2 h-2 bg-current rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
        </div>
      )}
    </div>
  )
}

export function ProcessingSteps({ currentStage }: { currentStage: string }) {
  const stages = [
    { key: 'searching', label: 'Document Search', completed: ['searching', 'calculating', 'analyzing', 'complete'].includes(currentStage) },
    { key: 'calculating', label: 'Code Interpreter', completed: ['calculating', 'analyzing', 'complete'].includes(currentStage) },
    { key: 'analyzing', label: 'Analysis', completed: ['analyzing', 'complete'].includes(currentStage) }
  ]
  
  return (
    <div className="flex items-center gap-2 mb-4">
      {stages.map((stage, index) => (
        <div key={stage.key} className="flex items-center">
          <div className={cn(
            'w-8 h-8 rounded-full flex items-center justify-center text-xs font-medium',
            stage.completed 
              ? 'bg-green-500 text-white' 
              : currentStage === stage.key
                ? 'bg-blue-500 text-white animate-pulse'
                : 'bg-slate-200 text-slate-500'
          )}>
            {index + 1}
          </div>
          <span className={cn(
            'ml-2 text-xs font-medium',
            stage.completed ? 'text-green-600' : 
            currentStage === stage.key ? 'text-blue-600' : 'text-slate-500'
          )}>
            {stage.label}
          </span>
          {index < stages.length - 1 && (
            <div className={cn(
              'w-8 h-0.5 mx-2',
              stage.completed ? 'bg-green-500' : 'bg-slate-200'
            )} />
          )}
        </div>
      ))}
    </div>
  )
}
