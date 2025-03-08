import { Message, Modal, Notification } from '@arco-design/web-vue'
import { h, VNode } from 'vue'

export interface NotificationOptions {
  title?: string
  content: string
  duration?: number
  closable?: boolean
}

export interface ConfirmOptions {
  title?: string
  content: string
  okText?: string
  cancelText?: string
}

/**
 * 通知提示管理
 * 统一消息通知样式，支持多种通知类型，简化消息提示调用
 */
export function useNotification() {
  /**
   * 显示成功通知
   * @param options 通知选项
   */
  const success = (options: NotificationOptions) => {
    Notification.success({
      title: options.title || '成功',
      content: options.content,
      closable: options.closable !== false,
      duration: options.duration || 3000,
    } as any)
  }

  /**
   * 显示错误通知
   * @param options 通知选项
   */
  const error = (options: NotificationOptions) => {
    Notification.error({
      title: options.title || '错误',
      content: options.content,
      closable: options.closable !== false,
      duration: options.duration || 5000,
    } as any)
  }

  /**
   * 显示警告通知
   * @param options 通知选项
   */
  const warning = (options: NotificationOptions) => {
    Notification.warning({
      title: options.title || '警告',
      content: options.content,
      closable: options.closable !== false,
      duration: options.duration || 4000,
    } as any)
  }

  /**
   * 显示信息通知
   * @param options 通知选项
   */
  const info = (options: NotificationOptions) => {
    Notification.info({
      title: options.title || '信息',
      content: options.content,
      closable: options.closable !== false,
      duration: options.duration || 3000,
    } as any)
  }

  /**
   * 显示确认对话框
   * @param options 确认选项
   * @returns Promise
   */
  const confirm = (options: ConfirmOptions): Promise<boolean> => {
    return new Promise((resolve) => {
      Modal.confirm({
        title: options.title || '确认',
        content: options.content,
        okText: options.okText || '确定',
        cancelText: options.cancelText || '取消',
        onOk: () => {
          resolve(true)
        },
        onCancel: () => {
          resolve(false)
        },
      })
    })
  }

  /**
   * 显示成功消息
   * @param content 消息内容
   */
  const successMessage = (content: string) => {
    Message.success(content)
  }

  /**
   * 显示错误消息
   * @param content 消息内容
   */
  const errorMessage = (content: string) => {
    Message.error(content)
  }

  return {
    notification: {
      success,
      error,
      warning,
      info,
    },
    message: {
      success: successMessage,
      error: errorMessage,
    },
    confirm,
  }
}

export default useNotification 