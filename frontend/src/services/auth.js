import API from "./api";

export const loginAPI = async (credentials, role) => { 
    try {
        console.log("role i get", role)
        if(!role){
            throw new Error("Role is required");
        }
        
        const response = await API.post(`/auth/login/${role}`, credentials);
        return [response.data, role];
    } catch (error) {
        throw new Error("Login Failed");
    }
}

export const registerAPI = async(userData) => {
    try{
        const res = await API.post("/auth/register/patient", userData);
        return res.data;
    } catch(error) {
        throw new Error("Registration Failed");
    }
}