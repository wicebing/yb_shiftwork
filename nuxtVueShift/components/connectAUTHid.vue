<script setup>
import { NSelect } from 'naive-ui'
const useStore = useUserStore()


const options= ref([
    {
        label: "Everybody's Got Something to Hide Except Me and My Monkey",
        value: 'song0',
    },
    {
        label: 'Drive My Car',
        value: 'song1'
    }
])
const value= ref(null)

async function getAUTH () {
    console.log('getAUTH')
    errors.value = []
    const { data, pending, refresh, error } = await useFetch('/api/regist/',{
        method: 'GET',
        baseURL:'http://localhost:8000',
        headers: {
            Authorization: `JWT ${useStore.token}` 
        }
    })

    // const { data } = await useFetch(() => `/api/hello/${count.value}`, { params: { token: 123 } })
    errors.value.push(error)
    errors.value.push(error.value.data.detail)
    console.log('error',error)
    console.log('error',error._object.detail)
}


</script>
<template>
    <n-select v-model:value="value" :options="options" />
</template>