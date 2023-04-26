<script setup>
import {NButton, NDrawer, NDrawerContent, NForm, NFormItemRow, NInput, NSwitch } from 'naive-ui'

const useStore = useUserStore()

const data = ref([])
const columns = ref([
    {
      title: '專案名稱',
      key: 'name'
    },
    {
      title: 'Edit',
      key: 'Edit',
    },
    {
      title: 'Delete',
      key: '刪',
    }
])
const result = reactive ({})
const activeDrawerProjectEdit = ref(false)
const activeDrawerProjectAdd = ref(false)
const placementDrawer = ref('right')
const editing = reactive([])
const errors = ref([])

const newProject = reactive({
    name: "",
})

const originalProject = reactive({
    name: "",
    status: null,
});

const editProject = reactive({
    name: "",
    status: null,
})

async function getProject () {
    console.log('getProject')
    for (const key in result) {
        delete result[key];
    }
    try{
        const { data, pending, refresh, error } = await useFetch('/api/project/?status=false&ordering=name', {
            method: 'GET',
            baseURL:'http://localhost:8000',
            headers: {
                Authorization: `JWT ${useStore.token}` 
            }
        })
        console.log('data',data.value)
        console.log('error',error)

        Object.assign(result, data.value.results)
        console.log('result',result)
    } catch (err) {
        console.log('err',err)
    }
}

async function editData(row) {
    console.log("Row:", row)
    Object.assign(editProject, row)
    Object.assign(originalProject, row); // Store the original data before editing
    console.log("editProject:", editProject)
    activeDrawerProjectEdit.value = true
}

async function deleteData(row) {
    try {
        console.log('deleteData', row)
        const { data, pending, refresh, error } = await useFetch(`/api/project/${row.id}`, {
        method: 'DELETE',
        baseURL: 'http://localhost:8000',
        headers: {
            Authorization: `JWT ${useStore.token}`,
        },
        })

        console.log('deleteData', row)
        console.log('Deleted successfully')
        console.log('Error: ', error.value)
    } catch (error) {
        console.error('Error deleting data:', error);
    }
    getProject()
    editing = reactive([])
}

async function addData() {
    errors.value = []
    try {
        console.log('addData')
        console.log('NEWdate',newProject)
        const { data, pending, refresh, error } = await useFetch('/api/project/', {
            method: 'POST',
            baseURL:'http://localhost:8000',
            headers: {
            Authorization: `JWT ${useStore.token}`,
            },
            body: {
                name: newProject.name,
            }
        })

        if (data.value) {
            console.log("New staff added:", data.value)
            getProject()
        } else {
            console.log('error',error)
            console.log('errorName',error.value.data)
            errors.value.push(error.value.data)
        }

    } catch (error) {
        console.error('Error deleting data:', error);
    }
}

function switchactiveDrawerProjectAdd() {
    activeDrawerProjectAdd.value = !activeDrawerProjectAdd.value
}

async function updateData() {
    console.log("Updating staff data:", editProject);
    const updatedFields = {}
    for (const key in editProject) {

        if (editProject[key] !== originalProject[key]) {
            updatedFields[key] = editProject[key];
        }        
    }

    try {
        const { data, pending, refresh, error } = await useFetch(`/api/project/${editProject.id}/`, {
            method: 'PATCH',
            baseURL: 'http://localhost:8000',
            headers: {
                Authorization: `JWT ${useStore.token}`,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(updatedFields),
        });

        console.log("Updated successfully:", data.value);
        getProject(); // Refresh the staff list after the update is successful
    } catch (error) {
        console.error('Error updating data:', error);
    }
    activeDrawerProjectEdit.value = false;
}


onMounted(() => {
    getProject()
})

</script>

<template>
    <n-button dashed type="warning" strong
    @click=switchactiveDrawerProjectAdd
    >
        新增專案
    </n-button>
    <table class="table-auto min-w-full">
        <thead class="bg-gray-50">
            <tr>
                <th v-for="col in columns" class="px-2 py-4 text-xs font-bold text-gray-500 text-left" scope="col">{{ col.title }}</th>
            </tr>
        </thead>
        <tbody class="divide-y divide-gray-200">
            <tr v-for="(res, rowIndex) in result">
                <td v-for="col in columns" class="px-2 py-2 text-sm font-medium text-gray-800 whitespace-nowrap">
                    <n-button 
                    v-if="!res[col.key] && col.title === 'Edit'"
                    secondary
                    type='info'
                    @click= editData(res)
                    >
                        {{ col.key }}
                    </n-button>

                    <n-button 
                    v-if="!res[col.key]  && col.title === 'Delete'"
                    secondary strong type='error'
                    @click=deleteData(res)
                    :disabled="!editing[rowIndex]"
                    >
                        {{ col.key }}
                    </n-button>

                    <n-switch v-if="col.title==='Delete'" v-model:value="editing[rowIndex]" />

                    <div v-if=res[col.key]>
                        {{ res[col.key] }}
                    </div>                              
                </td>
            </tr>
        </tbody>
    </table>
    <n-drawer v-model:show="activeDrawerProjectEdit" :width="502" :placement="placementDrawer">
        <n-drawer-content title="專案名稱" closable>
            <n-form>
                <n-form-item-row label="專案名稱">  
                    <n-input placeholder="年-月(註記)" v-model:value="editProject.name" />
                </n-form-item-row>
                <n-form-item-row label="已完成"> 
                    {{ editProject.status }}
                    <n-switch v-model:value="editProject.status" />
                </n-form-item-row>
                <n-button type="primary" block secondary strong @click="updateData(editProject)">
                    更正
                </n-button>       
            </n-form>
        </n-drawer-content>
    </n-drawer>
    <n-drawer v-model:show="activeDrawerProjectAdd" :width="502" :placement="placementDrawer">
        <n-drawer-content title="新增專案" closable>
            <n-form>
                <n-form-item-row label="專案名稱">
                    <n-input placeholder="年-月(註記)" v-model:value="newProject.name" />
                </n-form-item-row>
                <div v-if="errors.length" class="mb-6 py-4 px-6 bg-rose-400 rounded-xl">
                    <p v-for="error in errors" :key="error">
                        {{ error }}
                    </p>
                </div>
                <n-button type="primary" block secondary strong @click="addData">
                新增
                </n-button>
            </n-form>
        </n-drawer-content>
    </n-drawer>
</template>
