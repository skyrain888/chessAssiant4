import { ref } from 'vue'

/**
 * 加载状态管理
 * 统一管理加载状态，提供加载文本控制，简化异步操作的加载状态处理
 */
export function useLoading(initialState = false) {
  // 加载状态
  const loading = ref(initialState)
  // 加载文本
  const loadingText = ref('加载中...')

  // 设置加载状态
  const setLoading = (value: boolean) => {
    loading.value = value
  }

  // 设置加载文本
  const setLoadingText = (text: string) => {
    loadingText.value = text
  }

  // 包装异步函数，自动处理加载状态
  const withLoading = async <T>(fn: () => Promise<T>, text?: string): Promise<T> => {
    try {
      if (text) {
        setLoadingText(text)
      }
      setLoading(true)
      return await fn()
    } finally {
      setLoading(false)
    }
  }

  return {
    loading,
    loadingText,
    setLoading,
    setLoadingText,
    withLoading
  }
}

export default useLoading 