import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

const Login = () =>{
    const backend_url = import.meta.env.VITE_BACKEND_URL;
    const [formData, setFormData] = useState({
        email: "",
        password: ""
    })
    const navigate = useNavigate()

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch(`${backend_url}api/login`, {
                method: "POST",
                headers: {
                    "Content-Type" : "application/json"
                },
                body : JSON.stringify(formData),
            })

            const data = await response.json()
            console.log(data.message)
            sessionStorage.setItem("token", data.access_token);
            navigate("/private")
        }   catch(error) {
            console.error("Login error ", error)
        }
    };

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        })
    };




    return (
        <div className="container">
            <form onSubmit={handleSubmit}> 
                <div className="mb-3">
                    <label for="exampleInputEmail1" className="form-label">Email </label>
                    <input type="email" className="form-control" id="exampleInputEmail1" aria-describedby="emailHelp" name="email" value={formData.email} onChange={handleChange}/>
                </div>
                <div className="mb-3">
                    <label for="exampleInputPassword1" className="form-label">Password</label>
                    <input type="password" className="form-control" id="exampleInputPassword1" name="password" value={formData.password} onChange={handleChange} />
                </div>
                <button type="submit" className="btn btn-primary">Submit</button>
            </form>
        </div>
    )
}

export default Login