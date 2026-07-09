import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { loginUser } from "../../services/authService";
import { jwtDecode } from "jwt-decode";
import {toast} from "react-toastify";
import "/src/styles/indexbg.css";

function Login() {

    const navigate = useNavigate();

    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");

    const handleLogin = async (e) => {
    e.preventDefault();

    try {

        const response = await loginUser({
            email,
            password
        });

        localStorage.setItem(
            "token",
            response.data.access_token
        );

        toast.success("Login successful");
        navigate("/dashboard");

    } catch (error) {
        toast.error("Login failed! ");
    }
};
    return (
        
    <div className="login-bg">
        <div className="container d-flex justify-content-center align-items-center vh-100" id = "login-bg">

            <div className="card shadow p-4" style={{ width: "400px" }}>

                <h3 className="text-center mb-3">Login</h3>

                <form onSubmit={handleLogin}>

                    <div className="mb-3">
                        <label className="form-label">Email</label>
                        <input
                            type="email"
                            className="form-control"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                        />
                    </div>

                    <div className="mb-3">
                        <label className="form-label">Password</label>
                        <input
                            type="password"
                            className="form-control"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                        />
                    </div>

                    <button className="btn btn-primary w-100">
                        Login
                    </button>

                </form>

                <p className="text-center mt-3">
                    Don't have an account?{" "}
                    <span
                        style={{ cursor: "pointer", color: "blue" }}
                        onClick={() => navigate("/register")}
                    >
                        Register
                    </span>
                </p>

            </div>

        </div>

    </div>    
    );
}

export default Login;