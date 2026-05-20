'use server'

const BACKEND_URL = process.env.BACKEND_URL

// APIレスポンスの型定義
export interface ApiResponse<T = any> {
  success: boolean
  data?: T
  error?: string
  status?: number
}

// 共通のリクエスト処理
const request = async <T = any>(
  method: string,
  apiUrl: string,
  body?: Record<string, any>,
): Promise<ApiResponse<T>> => {
  try {
    const url = `${BACKEND_URL}${apiUrl}`
    const options: RequestInit = {
      method,
      headers: {
        'Content-Type': 'application/json',
      },
    }

    if (body) {
      options.body = JSON.stringify(body)
    }

    const response = await fetch(url, options)

    let data
    if (response.status === 204) {
      // レスポンスデータが無いので空
      data = {}
    } else {
      // レスポンスデータの取得
      data = await response.json()
    }

    if (!response.ok) {
      return {
        success: false,
        error: `HTTP error! status: ${response.status}`,
        status: response.status,
      }
    }

    return {
      success: true,
      data,
      status: response.status,
    }
  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : 'Unknown error'
    console.error(`Error in ${method} request:`, error)
    return {
      success: false,
      error: errorMessage,
    }
  }
}

// GET リクエスト
export const getRequest = async <T = any>(apiUrl: string): Promise<ApiResponse<T>> => {
  return request<T>('GET', apiUrl)
}

// POST リクエスト
export const postRequest = async <T = any>(
  apiUrl: string,
  body: Record<string, any> = {},
): Promise<ApiResponse<T>> => {
  return request<T>('POST', apiUrl, body)
}

// PUT リクエスト
export const putRequest = async <T = any>(
  apiUrl: string,
  body: Record<string, any> = {},
): Promise<ApiResponse<T>> => {
  return request<T>('PUT', apiUrl, body)
}

// DELETE リクエスト
export const deleteRequest = async <T = any>(apiUrl: string): Promise<ApiResponse<T>> => {
  return request<T>('DELETE', apiUrl)
}

// PATCH リクエスト
export const patchRequest = async <T = any>(
  apiUrl: string,
  body: Record<string, any> = {},
): Promise<ApiResponse<T>> => {
  return request<T>('PATCH', apiUrl, body)
}

// 汎用fetchData（後方互換性のため）
export const fetchData = async (apiUrl: string) => {
  return getRequest(apiUrl)
}
