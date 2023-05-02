<script setup>
import { NInput, NButton, NForm, NFormItemRow,NFormItem, NDatePicker, NSwitch, NDrawer, NDrawerContent, NTransfer } from 'naive-ui'

const route = useRoute()
const useStore = useUserStore()

const props = defineProps({
    projectId: {
        type: String,
        required: true
    }
})

const result = reactive ({})
const errors = ref([])
const editing = reactive([])
const resultGroups = reactive ({})
const optionsSelectGroups = ref([]);
const oldSelectGroups = ref([]);
const newAddGroup = ref([]);
const activeDrawerProjectEdit = ref(false);

const originalProject = reactive({
    id: "",
    constraint: null

});

const editProject = reactive({
    id: "",
    constraint: null
})

const columns = ref([
    {
      title: 'id',
      key: 'id'
    },
    {
      title: 'project',
      key: 'project'
    },
    {
      title: '組名',
      key: 'groupname_name'
    },
    {
      title: 'group_members',
      key: 'group_members'
    },
    {
      title: '填班規則',
      key: 'related_rules'
    },
    {
      title: 'sequence',
      key: 'sequence'
    },
    {
      title: 'Edit',
      key: '更新',
    },
    {
      title: 'Delete',
      key: '刪',
    }
])

function formatGroups(groups) {
  return groups.map((group) => `${group.staff_name}-${group.staff}`);
}

function formatRule(related_rules) {
  return related_rules.map((related_rules) => `${related_rules.description}`);
}

const optionsGroup = computed(() => {
    console.log('optionsGroup', resultGroups);

    return Object.values(resultGroups).map((Group) => {
        const inoldSelectStaff = oldSelectGroups.value.includes(Group.id);

        return {
            label: Group.name,
            value: Group.id,
            disabled: inoldSelectStaff, // set disabled to true if groups array has elements or if the user is in optionsSelectStaff, otherwise false
        };
    });
});

async function getProject () {
    console.log('getProjectAttend')
    for (const key in result) {
        delete result[key];
    }
    try{
        const { data, pending, refresh, error } = await useFetch(`/api/projectAttend/?project_id=${props.projectId}&ordering=sequence`, {
            method: 'GET',
            baseURL:'http://localhost:8000',
            headers: {
                Authorization: `JWT ${useStore.token}` 
            }
        })

        if (data.value) {
            console.log('data getProjectAttend',data.value)

            Object.assign(result, data.value.results)
            optionsSelectGroups.value = data.value.results.map((group) => group.groupname) // update optionsSelectStaff with the staff ids   
            oldSelectGroups.value = data.value.results.map((group) => group.groupname) // update optionsSelectStaff with the staff ids
            console.log('result getProjectAttend',result)
        } else {
            console.log('error',error)
        }
    } catch (err) {
        console.log('err',err)
    }
}

async function getGroup () {
    console.log('getGroup')
    errors.value = []
    for (const key in resultGroups) {
        delete resultGroups[key];
    }
    try {
        const { data, pending, refresh, error } = await useFetch('/api/groupname/?ordering=priority', {
            method: 'GET',
            baseURL:'http://localhost:8000',
            headers: {
                Authorization: `JWT ${useStore.token}` 
            }
        })

        if (data.value) {
            console.log('data resultGroups',data.value)
            Object.assign(resultGroups, data.value.results)        
        } else {
            console.log('error resultGroups',error)
            errors.value.push(error)
            errors.value.push(data.value.results)
        }
    } catch {
        console.log('error Group',error)
        errors.value.push(error)
    }
}


async function editData(row) {
    console.log("Row:", row)
    console.log("Rowid:", row.id)
    await getGroup()
    Object.assign(editProject, row)
    console.log("editProject:", editProject)
    updateData()
}

async function deleteData(row) {
    try {
        console.log('deleteData', row)
        const { data, pending, refresh, error } = await useFetch(`/api/projectAttend/${row.id}`, {
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

async function AddGroup() {
    console.log("Updating AddGroupmenber");
    errors.value = []
    for (const member of newAddGroup.value) {
        try {
            console.log('addData')
            console.log('NEWgroup to group',member)
            const { data, pending, refresh, error } = await useFetch('/api/projectAttend/', {
                method: 'POST',
                baseURL:'http://localhost:8000',
                headers: {
                Authorization: `JWT ${useStore.token}`,
                },
                body: {
                    project: props.projectId,
                    groupname: member,
                }
            })

            if (data.value) {
                console.log("New staff added:", data.value)

            } else {
                console.log('error',error)
                console.log('errorName',error.value.data)
                errors.value.push(error.value.data)
            }

        } catch (error) {
            console.error('Error deleting data:', error);
        }        
        getProject()
        getGroup()
        getUser()
    }
}

async function updateData() {
    console.log("Updating group data:", editProject);
    const updatedFields = {}
    for (const key in editProject) {

        if (editProject[key] !== originalProject[key]) {
            updatedFields[key] = editProject[key];
        }        
    }
    console.log("Updating updatedFields:", JSON.stringify(updatedFields));
    try {
        const { data, pending, refresh, error } = await useFetch(`/api/projectAttend/${editProject.id}/`, {
            method: 'PATCH',
            baseURL: 'http://localhost:8000',
            headers: {
                Authorization: `JWT ${useStore.token}`,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(updatedFields),
        });
        
        if (data.value) {
            console.log("Updated successfully:", data.value);
            getProject(); // Refresh the staff list after the update is successful
        } else {
            console.log('error',error)
            console.log('errorName',error.value.data)
            errors.value.push(error.value.data)
        }
    } catch (error) {
        console.error('Error updating data:', error);
    }
}

watch(optionsSelectGroups, (newVal, oldVal) => {
    newAddGroup.value = newVal.filter(member => !oldSelectGroups.value.includes(member))
    console.log("New Groups: ", newAddGroup);  
});

onMounted(() => {
    getProject()
    getGroup()
})

</script>
<!-- //v-if=useStore.is_superuser -->
<template>
    <n-transfer ref="transfer" v-if="!specialGroup"
        :options="optionsGroup" v-model:value="optionsSelectGroups"
        source-filterable
        />
    <n-button type="primary" block secondary strong @click="AddGroup()">
        加入填班編組
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

                    <n-input placeholder="..." v-model:value="res[col.key]" v-if="col.key==='constraint'" />

                    <div v-if="res[col.key] !== null && res[col.key] !== undefined && col.key!=='group_members'">
                        <div v-if="col.key!=='related_rules'">
                            {{ res[col.key] }}
                        </div>    
                        <div v-if="col.key==='related_rules'">
                            <tr v-for="member in formatRule(res[col.key])">
                                <td>{{ member }}</td>
                            </tr>
                        </div>
                    </div>
                    <div v-if="res[col.key] !== null && res[col.key] !== undefined && col.key==='group_members'">
                        <tr v-for="member in formatGroups(res[col.key])">
                            <td>{{ member }}</td>
                        </tr>
                    </div>              
                </td>
            </tr>
        </tbody>
    </table>
</template>

<style scoped>
</style>