<script lang="ts" setup>
import { NIcon, NDropdown } from 'naive-ui'
import { CalendarSharp } from '@vicons/ionicons5'
const useStore = useUserStore()
const useRoute = useRouter()

const options= ref([
        {
          label: '人員',
          key: 'userStaff',
          props: {
            onClick: () => {
            //   message.success('Good!')
            useRoute.push('/manage')
            }
          }
        },
        {
          label: '班種組別',
          key: 'shiftworks',
          props: {
            onClick: () => {
            //   message.success('Good!')
            useRoute.push('/shiftworks')
            }
          }
        },
        {
          label: '專案',
          key: 'projects',
          props: {
            onClick: () => {
            //   message.success('Good!')
            useRoute.push('/projects')
            }
          }
        },
      ])

const optionsUser= ref([
        {
          label: '個人資料',
          key: 'userStaff',
          props: {
            onClick: () => {
            //   message.success('Good!')
            useRoute.push('/personal')
            }
          }
        },
      ])

</script>

<template>
    <div v-if=useStore.isAuthenticated class="flex items-center space-x-4 font-bold font-mono">
        <n-dropdown v-if=useStore.is_superuser trigger="hover" :options="options">
            <!-- <n-button text color="#0E366F">找个地方休息</n-button> -->
            <span class="text-sky-800 hover:text-white">管理</span>
        </n-dropdown>
        <n-dropdown v-if=useStore.isAuthenticated trigger="hover" :options="optionsUser">
            <!-- <n-button text color="#0E366F">找个地方休息</n-button> -->
            <span class="text-sky-800 hover:text-white">個人</span>
        </n-dropdown>
        <NuxtLink to="/" class="text-sky-800 hover:text-white">
        <n-icon size="20" color="#193F85">
            <calendar-sharp />
        </n-icon>
        </NuxtLink>
    </div>
</template>