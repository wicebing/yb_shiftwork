<script lang='ts' setup> 
import { NButton } from 'naive-ui'
const useStore = useUserStore()

const router = useRouter()

const errors = ref([])
async function signOut() {
    errors.value = []
    useStore.removeToken()
    useStore.removeUserDetail()
    router.push('/')
}

</script>

<template>
    <div v-if=!useStore.isAuthenticated class="flex mt-6 md:mt-0 items-center space-x-4 text-base">
        <NuxtLink to="/login" class="py-4 px-6 text-white hover:bg-sky-500 rounded-xl font-semibold">Login</NuxtLink>
    </div>
    <div v-if=useStore.isAuthenticated class="flex mt-6 md:mt-0 items-center space-x-4 text-base">
        <n-button class="py-4 px-6 text-white hover:bg-sky-500 rounded-xl font-semibold" :on-click="signOut">Sign out</n-button>
    </div>
</template>