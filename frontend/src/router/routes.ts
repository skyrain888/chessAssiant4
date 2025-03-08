import { RouteRecordRaw } from 'vue-router'

// 布局组件
const DefaultLayout = () => import('../layouts/DefaultLayout.vue')
const AuthLayout = () => import('../layouts/AuthLayout.vue')

// 页面组件
const Home = () => import('../views/Home.vue')
const NotFound = () => import('../views/NotFound.vue')
const Profile = () => import('../views/Profile.vue')

// 认证页面
const Login = () => import('../views/auth/Login.vue')
const Register = () => import('../views/auth/Register.vue')
const ForgotPassword = () => import('../views/auth/ForgotPassword.vue')

// 工具页面
const ToolsIndex = () => import('../views/tools/ToolsIndex.vue')

// 国际象棋工具页面
const ChessIndex = () => import('../views/tools/chess/ChessIndex.vue')
const ChessList = () => import('../views/tools/chess/ChessList.vue')

// 路由配置
const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: DefaultLayout,
    children: [
      {
        path: '',
        name: 'home',
        component: Home,
        meta: { title: '首页' }
      },
      {
        path: 'profile',
        name: 'profile',
        component: Profile,
        meta: { title: '个人中心', requiresAuth: true }
      },
      {
        path: 'tools',
        name: 'tools',
        component: ToolsIndex,
        meta: { title: '工具中心' }
      },
      {
        path: 'chess',
        name: 'chess',
        component: ChessIndex,
        meta: { title: '国际象棋工具' }
      },
      {
        path: 'chess/list',
        name: 'chess-list',
        component: ChessList,
        meta: { title: '棋谱列表' }
      },
      {
        path: 'chess/detail/:id',
        name: 'ChessDetail',
        component: () => import('../views/tools/chess/ChessDetail.vue'),
        meta: { title: '棋谱详情', requiresAuth: true }
      },
      {
        path: 'chess/upload',
        name: 'ChessUpload',
        component: () => import('../views/tools/chess/ChessUpload.vue'),
        meta: { title: '上传棋谱', requiresAuth: true }
      },
      {
        path: 'chess/viewer/:id',
        name: 'ChessViewer',
        component: () => import('../views/tools/chess/ChessViewer.vue'),
        meta: { title: '棋谱查看器', requiresAuth: true }
      },
      {
        path: 'chess/practice/:id',
        name: 'ChessPractice',
        component: () => import('../views/tools/chess/ChessPractice.vue'),
        meta: { title: '棋谱练习', requiresAuth: true }
      }
    ]
  },
  {
    path: '/',
    component: AuthLayout,
    children: [
      {
        path: 'login',
        name: 'login',
        component: Login,
        meta: { title: '登录' }
      },
      {
        path: 'register',
        name: 'register',
        component: Register,
        meta: { title: '注册' }
      },
      {
        path: 'forgot-password',
        name: 'forgot-password',
        component: ForgotPassword,
        meta: { title: '忘记密码' }
      }
    ]
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: NotFound,
    meta: { title: '页面未找到' }
  }
]

export default routes 