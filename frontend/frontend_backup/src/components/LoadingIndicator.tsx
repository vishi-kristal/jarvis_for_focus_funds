'use client'

import { Loader2, Brain } from 'lucide-react'

export function LoadingIndicator() {
  return (
    <div className="flex items-center justify-center p-6">
      <div className="flex items-center gap-4">
        <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-600 to-indigo-600 flex items-center justify-center shadow-sm">
          <Brain className="w-5 h-5 text-white" />
        </div>
        <div className="flex items-center gap-3">
          <Loader2 className="w-5 h-5 animate-spin text-blue-600" />
          <div className="text-slate-600">
            <div className="text-sm font-medium">AI is analyzing...</div>
            <div className="text-xs text-slate-500">This may take a few moments</div>
          </div>
        </div>
      </div>
    </div>
  )
}
