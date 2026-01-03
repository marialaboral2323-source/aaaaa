import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/',
            redirect: '/slot'
        },
        {
            path: '/login',
            name: 'login',
            component: () => import('@/views/LoginView.vue'),
            meta: { guest: true }
        },
        {
            path: '/register',
            name: 'register',
            component: () => import('@/views/RegisterView.vue'),
            meta: { guest: true }
        },
        {
            path: '/slot',
            name: 'slot',
            component: () => import('@/views/SlotView.vue'),
            meta: { requiresAuth: true }
        },
        {
            path: '/mypage',
            name: 'mypage',
            component: () => import('@/views/MyPageView.vue'),
            meta: { requiresAuth: true }
        },
        {
            path: '/wallet',
            name: 'wallet',
            component: () => import('@/views/WalletView.vue'),
            meta: { requiresAuth: true }
        },
        {
            path: '/:pathMatch(.*)*',
            redirect: '/login'
        }
    ]
})

router.beforeEach((to, from, next) => {
    const authStore = useAuthStore()

    if (to.meta.requiresAuth && !authStore.isAuthenticated) {
        next('/login')
    } else if (to.meta.guest && authStore.isAuthenticated) {
        next('/slot')
    } else {
        next()
    }
})

export default router
