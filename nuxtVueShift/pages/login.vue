<script setup>
import { NTabPane, NCard, NTabs, NForm, NFormItemRow, NInput, NButton } from 'naive-ui'
import { NIcon } from 'naive-ui'
import { GlassesOutline, Glasses } from '@vicons/ionicons5'

// import { useUserStore } from '../composables/user.js'

const staff = reactive({
    name: '',
    password:'',
    email:'',
    AUTHid:null
})
const errors = ref([])
const repeatPW = ref('')

const useStore = useUserStore()

async function commitSignup () {
    console.log('commitSignup')
    errors.value = []
    // const { data: count } = await useFetch('/regist',{
    // method: 'GET',
    //     // pick: ["username", "email"],
    // baseURL:'http://localhost:8000',})
    if (staff.password !== repeatPW.value) {
        errors.value.push('Password does not match')
        return
    }
    try{
        const { data, pending, refresh, error } = await useFetch('/api/regist/', {
            method: 'POST',
            baseURL:'http://localhost:8000',
            body: {
                username: staff.name,
                email: staff.email,
                password: staff.password,
            }
        })
        // const { data } = await useFetch(() => `/api/hello/${count.value}`, { params: { token: 123 } })
        // errors.value.push(error)
        // errors.value.push(error.value)
        if (error.value){
            console.log('error',error.value.data)
            errors.value.push(error.value.data)
        }
        // errors.value.push('please input username or email')
        commitLogin ()
    } catch (error) {
        console.log('ALLerror',error)
        errors.value.push('please try again')
    }

}

async function commitLogin () {
    console.log('commitLogin')
    errors.value = []
    const { data, pending, refresh, error } = await useFetch('/token/', {
        method: 'POST',
        baseURL:'http://localhost:8000',
        body: {
            username: staff.name,
            password: staff.password,
        }
    })
    // const { data } = await useFetch(() => `/api/hello/${count.value}`, { params: { token: 123 } })
    console.log('data',data.value)
    console.log('error',error)

    if (error.value){
        console.log('error',error.value.data.detail)
        errors.value.push(error.value)
    }
    if (data.value){
        useStore.setToken(data.value.access)
        console.log('useStore',useStore.token,useStore.$state.isAuthenticated)
        getCurrentUser()
        navigateTo('/')
    }

}

async function getCurrentUser() {
    errors.value = []
    try{
        const { data, error } = await useFetch('/api/whoami/', {
            method: 'GET',
            baseURL: 'http://localhost:8000',
            headers: {
                Authorization: `JWT ${useStore.token}`,
            },
        });

        if (error.value) {
            console.log('Error:', error.value);
        } else {
            console.log('Current user:', data.value);
            useStore.setUserDetail(data.value.id,
            data.value.username,
            data.value.email,
            data.value.is_staff,
            data.value.is_superuser,
            data.value.table_staff
            ) 
            console.log('getUser',useStore.getUserDetail())
        }        
    } catch (error) {
        console.log('ALLerror',error)
        errors.value.push('please try again')
    }
}


</script>

<template>
  <div class="py-10 px-6">
    <div class="space-y-4">
        <n-card>
            <n-tabs
            class="card-tabs"
            default-value="signin"
            size="large"
            animated
            style="margin: 0 -4px"
            pane-style="padding-left: 4px; padding-right: 4px; box-sizing: border-box;"
            >
                <n-tab-pane name="signin" tab="Sign in">
                    <n-form>
                        <n-form-item-row label="Username">
                            <n-input placeholder="Your name or email" v-model:value="staff.name"/>
                        </n-form-item-row>
                        <n-form-item-row label="Password">
                            <n-input
                            type="password"
                            show-password-on="click"
                            placeholder="Your password"
                            v-model:value="staff.password"
                            >
                            <template #password-visible-icon>
                                <n-icon :size="16" :component="GlassesOutline" />
                            </template>
                            <template #password-invisible-icon>
                                <n-icon :size="16" :component="Glasses" />
                            </template>
                            </n-input>
                        </n-form-item-row>
                        <div v-if="errors.length" class="mb-6 py-4 px-6 bg-rose-400 text-white rounded-xl">
                            <p v-for="error in errors" :key="error">
                                {{ error }}
                            </p>
                        </div>
                        <n-button type="primary" block secondary strong :on-click="commitLogin">
                        Sign In
                        </n-button>
                    </n-form>
                </n-tab-pane>
                <n-tab-pane name="signup" tab="Sign up">
                    <n-form>
                        <n-form-item-row label="Username">
                            <n-input placeholder="Your name" v-model:value="staff.name"/>
                        </n-form-item-row>
                        <n-form-item-row label="Email">
                            <n-input placeholder="Your email" v-model:value="staff.email"/>
                        </n-form-item-row>
                        <n-form-item-row label="Password">
                            <n-input
                            type="password"
                            show-password-on="click"
                            placeholder="Your password"
                            v-model:value="staff.password"
                            >
                            <template #password-visible-icon>
                                <n-icon :size="16" :component="GlassesOutline" />
                            </template>
                            <template #password-invisible-icon>
                                <n-icon :size="16" :component="Glasses" />
                            </template>
                            </n-input>
                        </n-form-item-row>
                        <n-form-item-row label="Re-enter Password">
                            <n-input
                            type="password"
                            show-password-on="click"
                            placeholder="Confirm your password"
                            v-model:value="repeatPW"
                            >
                            <template #password-visible-icon>
                                <n-icon :size="16" :component="GlassesOutline" />
                            </template>
                            <template #password-invisible-icon>
                                <n-icon :size="16" :component="Glasses" />
                            </template>
                            </n-input>
                        </n-form-item-row>
                        <div v-if="errors.length" class="mb-6 py-4 px-6 bg-rose-400 text-white rounded-xl">
                            <p v-for="error in errors" :key="error">
                                {{ error }}
                            </p>
                        </div>
                        <n-button type="primary" block secondary strong :on-click="commitSignup">
                        Sign up
                        </n-button>
                    </n-form>

                </n-tab-pane>
            </n-tabs>
        </n-card> 
    </div>
  </div>
</template>

<style scoped>
.card-tabs .n-tabs-nav--bar-type {
  padding-left: 4px;
}
</style>