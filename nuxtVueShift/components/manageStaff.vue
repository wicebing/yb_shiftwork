<script setup>
import { NButton, NTabs, NTabPane, NSwitch } from 'naive-ui'
import { NFormItemRow, NInput, NForm, NDatePicker } from 'naive-ui'
const useStore = useUserStore()

const data = ref([])
const columns = ref([
    // {
    //   title: 'id',
    //   key: 'id'
    // },
    {
      title: 'NTUHid',
      key: 'NTUHid'
    },
    {
      title: 'name',
      key: 'name'
    },
    {
      title: 'birthday',
      key: 'birthday'
    },
    {
      title: 'AUTHid',
      key: 'AUTHid'
    },
    {
      title: 'Edit',
      key: 'Edit',
      render: () => 'Edit'
    },
    {
      title: 'Delete',
      key: '刪',
      render: () => 'Delete'
    }
])


const errors = ref([])
let result = reactive ([])
let editing = reactive([])
const active= ref(false)

async function getUset () {
    console.log('getUset')
    errors.value = []

    const { data, pending, refresh, error } = await useFetch('/api/staff/', {
        method: 'GET',
        baseURL:'http://localhost:8000',
        headers: {
            Authorization: `JWT ${useStore.token}` 
        }
    })
    // const { data } = await useFetch(() => `/api/hello/${count.value}`, { params: { token: 123 } })
    console.log('data',data.value)
    console.log('error',error)
    
    // errors.value.push(data.value.results)
    errors.value.push(error)
    errors.value.push(data.value.results)

    Object.assign(result, data.value.results)
}

async function play (row) {
    console.log('play', row)
    const { data, pending, refresh, error } = await useFetch(`/api/staff/${row.id}`, {
        method: 'GET',
        baseURL:'http://localhost:8000',
        headers: {
            Authorization: `JWT ${useStore.token}` 
        }
    })
    console.log('PLAYdata',data.value)
    console.log('PLAYerror',error)
}

// function computedDate(rowIndex, colKey) {
//   return computed({
//     get: () => new Date(result[rowIndex][colKey]),
//     set: (newValue) => (result[rowIndex][colKey] = newValue.toISOString().substring(0, 10)),
//   });
// }

function computedDate(rowIndex, colKey) {
  return computed({
    get: () => new Date(result[rowIndex][colKey]),
    set: (newValue) => (result[rowIndex][colKey] = newValue),
  });
}

async function updateData(rowIndex, key, value) {
    console.log("Row:", rowIndex, "Key:", key, "Value:", value);
    // Perform your API call here to update the data
}


onMounted(() => {
    getUset()
})

</script>

<template>
    <div v-if=useStore.isAuthenticated class="flex items-center space-x-4 font-bold font-mono text-left">
        <n-tabs
        class="card-tabs"
        default-value="signin"
        size="small"
        animated
        pane-style="padding-left: 4px; padding-right: 4px; box-sizing: border-box;"
        >
            <n-tab-pane name="allStaff" tab="人員總覽">
                <table class="table-auto min-w-full divide-y divide-gray-200">
                    <thead class="bg-gray-50">
                        <tr>
                            <th v-for="col in columns" class="px-2 py-4 text-xs font-bold text-gray-500" scope="col">{{ col.title }}</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-gray-200">
                        <tr v-for="(res, rowIndex) in result">
                            <td v-for="col in columns" class="px-2 py-2 text-sm font-medium text-gray-800 whitespace-nowrap">
                                <template v-if="!res[col.key]">
                                    <n-button secondary
                                    :strong="col.title === 'Delete'"
                                    :type="col.title === 'Delete' ? 'error' : 'info'">
                                        {{ col.key }}
                                    </n-button>
                                    <n-switch v-if="col.key==='Edit'" v-model:value="editing[rowIndex]" />
                                </template>
                                <template v-else>
                                    <template v-if="col.key==='birthday'">
                                        <n-date-picker 
                                        type="date"
                                        :disabled="!editing[rowIndex]"
                                        v-model:value="computedDate(rowIndex, col.key).value"
                                        />
                                    </template>
                                    <template v-else>  
                                        <n-input
                                        type="text"
                                        size="small"
                                        :readonly="!editing[rowIndex]"
                                        v-model:value="res[col.key]"
                                        @change="updateData(rowIndex, col.key, res[col.key])"
                                        />                                    
                                    </template>

                                </template>
                            </td>
                        </tr>
                    </tbody>
                </table>
            <div>
                <input :v-model="editing" :value="editing"/>
            </div>
            </n-tab-pane>
            <n-tab-pane name="addStaff" tab="新增">
                <n-form>
                    <n-form-item-row label="NTUHid">
                        <n-input placeholder="NTUHid" />
                    </n-form-item-row>
                    <n-form-item-row label="name">
                        <n-input placeholder="姓名"/>
                    </n-form-item-row>
                    <n-form-item-row label="birthday">
                        <n-date-picker type="date" />
                    </n-form-item-row>
                    <n-button type="primary" block secondary strong>
                    新增
                    </n-button>
                </n-form>
            </n-tab-pane>
        </n-tabs>
    </div>
</template>