import React from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import { useAuth } from "./context/AuthContext.jsx";
import LoginPage from "./pages/LoginPage.jsx";
import NotesPage from "./pages/NotesPage.jsx";

export default function App() {
  const { user } = useAuth();

  return (
    <Router>
      <Routes>
        {/* Login Page */}
        <Route path="/login" element={<LoginPage />} />

        {/* Notes Page (protected) */}
        <Route
          path="/notes"
          element={user ? <NotesPage /> : <Navigate to="/login" replace />}
        />

        {/* Default redirect */}
        <Route
          path="*"
          element={<Navigate to={user ? "/notes" : "/login"} replace />}
        />
      </Routes>
    </Router>
  );
}
