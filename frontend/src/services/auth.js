import API from "./api";

export const loginAPI = async (credentials) => { 
    try {
        const response = await API.post(`/auth/login`, credentials);
        return response.data;
    } catch (error) {
        throw new Error("Login Failed", error);
    }
}

export const registerAPI = async(userData) => {
    try{
        const res = await API.post("/auth/register", userData);
        return res.data;
    } catch(error) {
        throw new Error("Registration Failed");
    }
}