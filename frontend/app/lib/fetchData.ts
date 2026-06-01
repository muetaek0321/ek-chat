'use server'

const BACKEND_URL = process.env.BACKEND_URL

// APIレスポンスの型定義
export interface ApiResponse<T> {
  success: boolean
  data?: T
  error?: string
  status?: number
}

// 共通のリクエスト処理
const request = async <TResponse = unknown, TBody = unknown>(
  method: string,
  apiUrl: string,
  body?: TBody,
): Promise<ApiResponse<TResponse>> => {
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
export const getRequest = async <TResponse = unknown>(
  apiUrl: string,
): Promise<ApiResponse<TResponse>> => {
  return request<TResponse>('GET', apiUrl)
}

// POST リクエスト
export const postRequest = async <TResponse = unknown, TBody = unknown>(
  apiUrl: string,
  body?: TBody,
): Promise<ApiResponse<TResponse>> => {
  return request<TResponse>('POST', apiUrl, body)
}

// PUT リクエスト
export const putRequest = async <TResponse = unknown, TBody = unknown>(
  apiUrl: string,
  body?: TBody,
): Promise<ApiResponse<TResponse>> => {
  return request<TResponse>('PUT', apiUrl, body)
}

// DELETE リクエスト
export const deleteRequest = async <TResponse = unknown>(
  apiUrl: string,
): Promise<ApiResponse<TResponse>> => {
  return request<TResponse>('DELETE', apiUrl)
}

// PATCH リクエスト
export const patchRequest = async <TResponse = unknown, TBody = unknown>(
  apiUrl: string,
  body?: TBody,
): Promise<ApiResponse<TResponse>> => {
  return request<TResponse>('PATCH', apiUrl, body)
}
