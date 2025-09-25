import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext.jsx";
import { useTenant } from "../context/TenantContext.jsx";

const API_URL = import.meta.env.VITE_API_URL;

export default function LoginPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();
  const { login } = useAuth();
  const { setTenant } = useTenant();

  async function handleLogin(e) {
    e.preventDefault();
    setError("");
    try {
      // Only use backend login
      const res = await fetch(`${API_URL}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
      });

      if (!res.ok) {
        setError("❌ Invalid credentials. Try again.");
        return;
      }
      const data = await res.json();
      const { access_token, user } = data;

      login(access_token, user);
      setTenant({
        id: user.tenant_id,
        name: user.tenant_id, // or user.tenant_name if present
        plan: user.plan || "free"
      });
      navigate("/notes");
      return;
    } catch (err) {
      setError("❌ Server error: " + err.message);
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-indigo-100 to-indigo-300">
      <div className="bg-white shadow-xl rounded-2xl p-8 w-96">
        <h2 className="text-2xl font-bold text-center text-indigo-600 mb-6">
          Multi-Tenant Notes Login
        </h2>
        <form onSubmit={handleLogin} className="space-y-4">
          <input
            type="text"
            placeholder="Username"
            className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
          <input
            type="password"
            placeholder="Password"
            className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          {error && (
            <p className="text-red-600 text-sm font-medium">{error}</p>
          )}
          <button
            type="submit"
            className="w-full bg-indigo-600 text-white py-3 rounded-lg shadow hover:bg-indigo-700 transition"
          >
            Login
          </button>
        </form>
        <div className="mt-6 text-xs text-gray-500 text-center">
          <p>Use one of the sample accounts:</p>
          <p>
            <span className="font-semibold">acmeAdmin / 123</span> |{" "}
            <span className="font-semibold">acmeMember / 123</span>
          </p>
          <p>
            <span className="font-semibold">globexAdmin / 123</span> |{" "}
            <span className="font-semibold">globexMember / 123</span>
          </p>
        </div>
      </div>
    </div>
  );
}
