import React, { useState } from "react";
import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

const Private = () => {
    const backend_url = import.meta.env.VITE_BACKEND_URL;
    const navigate = useNavigate();
    const [isValid, setIsValid] = useState(null);


    useEffect (() => {
        const fetchPrivate = async () =>{
            const token = sessionStorage.getItem("token")
            if (!token){
                navigate("/login");
                return;
            }

            try {
                
                const response = await fetch(`${backend_url}api/private`, {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                })
                if (!response.ok) throw new Error("Invalid token, pass denied")
                    const data = await response.json();
                    setIsValid(true);
            } catch(error) {
                console.error("error", error);
                navigate("/login")
            }
        }
        fetchPrivate();
    }, [navigate, backend_url]);

    return (
        isValid === null ? (
            <div>Loading..</div>
        ) : isValid ? (
            <div className="container"> 
            <h1>SI ESTAS VIENDO ESTO ES QUE FUNCIONA</h1>
            </div>
        ) : null
    )
}



export default Private;