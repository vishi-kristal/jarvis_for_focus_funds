export interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  timestamp: Date
  isTyping?: boolean
  processingStage?: 'searching' | 'calculating' | 'analyzing' | 'complete'
  images?: string[]
}

export interface QuestionRequest {
  question: string
}

export interface AnswerResponse {
  answer: string
  images?: string[]
}

export interface ErrorResponse {
  error: string
  detail?: string
}

export interface SampleQuestion {
  id: string
  question: string
  category: string
}
