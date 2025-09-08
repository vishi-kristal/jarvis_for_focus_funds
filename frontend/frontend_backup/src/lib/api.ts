import { QuestionRequest, AnswerResponse, ErrorResponse } from '@/types'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export class ApiError extends Error {
  constructor(
    message: string,
    public status: number,
    public detail?: string
  ) {
    super(message)
    this.name = 'ApiError'
  }
}

export async function askQuestion(question: string): Promise<{ answer: string; images: string[] }> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/ask`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ question } as QuestionRequest),
    })

    if (!response.ok) {
      const errorData: ErrorResponse = await response.json()
      throw new ApiError(
        errorData.error || 'Failed to get answer',
        response.status,
        errorData.detail
      )
    }

    const data: AnswerResponse = await response.json()
    return {
      answer: data.answer,
      images: data.images || []
    }
  } catch (error) {
    if (error instanceof ApiError) {
      throw error
    }
    
    // Network or other errors
    throw new ApiError(
      'Network error. Please check if the backend server is running.',
      0,
      error instanceof Error ? error.message : 'Unknown error'
    )
  }
}

export async function checkHealth(): Promise<boolean> {
  try {
    const response = await fetch(`${API_BASE_URL}/health`)
    if (!response.ok) {
      return false
    }
    const data = await response.json()
    return data.status === 'healthy' && data.files_configured === true
  } catch {
    return false
  }
}
