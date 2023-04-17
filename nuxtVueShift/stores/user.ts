export const useUserStore = definePiniaStore('userStore', ()=>{
    
    const isAuthenticated = ref(false)
    const token = ref('')

    // const initStore = () => {
    //     isAuthenticated.value = false
    //     if (localStorage.getItem('user.token')) {
    //         isAuthenticated.value = true
    //         token.value = localStorage.getItem('user.token')

    //         console.log('Initialized user:')
    //     }
    // }

    const setToken = (posttoken: string) => {
        console.log('Setting token:', posttoken)
        isAuthenticated.value = true
        token.value = posttoken
        // localStorage.setItem('token', posttoken)
    };

    const removeToken = () => {
        console.log('Removing token')
        isAuthenticated.value = false
        token.value = ''
        // localStorage.removeItem('user.token')
    }

    return {
        isAuthenticated,
        token,
        setToken,
        removeToken, 
    }
})
    
//     {
//     id: 'user',
//     state: () => ({
//         user:{
//             isAuthenticated: false,
//             email: null,
//             token: null
//         }
//     }),
//     getters: {
//         isAuthenticated: (state) => state.isAuthenticated,
//         name: (state) => state.name,
//         email: (state) => state.email,
//         token: (state) => state.token
//     },
//     actions: {
//         initStore() {
//             this.user.isAuthenticated false
//             if (localStorage.gerItem('user.token')) {
//                 this.user.isAuthenticated = true
//                 this.user.email = localStorage.getItem('user.email')
//                 this.user.token = localStorage.getItem('user.token')

//                 console.log('Initialized user:', this.user)
//             }
//         },
//         setToken(token, email) {
//             console.log('Setting token:', token, email)
//             this.user.isAuthenticated = true
//             this.user.email = email
//             this.user.token = token
//             localStorage.setItem('user.token', token)
//             localStorage.setItem('user.email', email)
//         },
//         removeToken() {
//             console.log('Removing token')
//             this.user.isAuthenticated = false
//             this.user.email = null
//             this.user.token = null
//             localStorage.removeItem('user.token')
//             localStorage.removeItem('user.email')
//         }
//     }
// })

