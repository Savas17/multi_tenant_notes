import React, { useState, useEffect } from "react";
import Navbar from "../components/Layout/Navbar.jsx";
import { useAuth } from "../context/AuthContext.jsx";
import { useTenant } from "../context/TenantContext.jsx";
import {
  fetchNotes,
  createNote,
  updateNote,
  deleteNote,
} from "../api/api.js";

export default function NotesPage() {
  const { user, token } = useAuth();
  const { tenant } = useTenant();

  const [notes, setNotes] = useState([]);
  const [title, setTitle] = useState("");
  const [body, setBody] = useState("");
  const [editingId, setEditingId] = useState(null);
  const [error, setError] = useState("");

  // Admins no note limit, members limited on free plan
  const canAddNote = user.role === "admin" || tenant?.plan === "pro" || notes.length < 3;

  useEffect(() => {
    if (!token || !tenant?.id) return;

    async function loadNotes() {
      try {
        const data = await fetchNotes(token, tenant.id);
        setNotes(data);
      } catch {
        setError("Failed to load notes from backend");
      }
    }
    loadNotes();
  }, [token, tenant?.id]);

  async function handleAddOrUpdate(e) {
    e.preventDefault();
    if (!title.trim()) {
      setError("⚠️ Title is required.");
      return;
    }
    if (!editingId && !canAddNote) {
      setError("🚫 Free plan limit reached (max 3 notes). Ask Admin to upgrade.");
      return;
    }
    setError("");
    try {
      if (editingId) {
        await updateNote(token, editingId, {
          title,
          content: body,
          tenant_id: tenant.id,
          owner: user.id,
        });
        setNotes((prev) =>
          prev.map((n) => (n.id === editingId ? { ...n, title, body } : n))
        );
        setEditingId(null);
      } else {
        const created = await createNote(token, {
          title,
          content: body,
          tenant_id: tenant.id,
          owner: user.id,
        });
        setNotes([{ id: created.id, title, body }, ...notes]);
      }
      setTitle("");
      setBody("");
    } catch (err) {
      setError(err.message);
    }
  }

  async function handleDelete(id) {
    try {
      await deleteNote(token, id);
      setNotes(notes.filter((n) => n.id !== id));
    } catch (err) {
      setError(err.message);
    }
  }

  function handleEdit(note) {
    setEditingId(note.id);
    setTitle(note.title);
    setBody(note.body);
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <div className="max-w-4xl mx-auto p-6">
        <h2 className="text-2xl font-bold mb-6 text-indigo-700">Notes</h2>

        <form
          onSubmit={handleAddOrUpdate}
          className="bg-white p-6 rounded-xl shadow-md space-y-4 mb-8"
        >
          <input
            type="text"
            placeholder="Note title"
            className="w-full p-3 border rounded-lg focus:ring-2 focus:ring-indigo-400 outline-none"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
          />
          <textarea
            placeholder="Write your note..."
            className="w-full p-3 border rounded-lg focus:ring-2 focus:ring-indigo-400 outline-none"
            rows={4}
            value={body}
            onChange={(e) => setBody(e.target.value)}
          />
          {error && <p className="text-red-600 text-sm">{error}</p>}

          {!canAddNote && !editingId && (
            <p className="text-yellow-600 font-semibold">
              You have reached the note limit for the free plan.
            </p>
          )}

          <button
            type="submit"
            disabled={!canAddNote && !editingId}
            className={`w-full py-3 rounded-lg font-semibold text-white ${
              !canAddNote && !editingId
                ? "bg-gray-400 cursor-not-allowed"
                : "bg-indigo-600 hover:bg-indigo-700"
            }`}
          >
            {editingId ? "Update Note ✏️" : "Add Note ➕"}
          </button>
        </form>

        <div className="grid gap-4">
          {notes.length === 0 && (
            <p className="text-gray-500 text-center">No notes yet. Add your first one above!</p>
          )}
          {notes.map((note) => (
            <div
              key={note.id}
              className="bg-white p-5 rounded-xl shadow hover:shadow-lg transition"
            >
              <div className="flex justify-between items-start">
                <div>
                  <h3 className="font-bold text-lg text-gray-800">{note.title}</h3>
                  <p className="text-xs text-gray-500">
                    by {note.createdBy || "Unknown"} •{" "}
                    {note.createdAt ? new Date(note.createdAt).toLocaleString() : ""}
                  </p>
                </div>
                <div className="flex gap-2">
                  <button
                    onClick={() => handleEdit(note)}
                    className="px-3 py-1 bg-yellow-200 text-yellow-900 rounded-lg text-sm hover:bg-yellow-300"
                  >
                    Edit
                  </button>
                  <button
                    onClick={() => handleDelete(note.id)}
                    className="px-3 py-1 bg-red-200 text-red-900 rounded-lg text-sm hover:bg-red-300"
                  >
                    Delete
                  </button>
                </div>
              </div>
              <p className="mt-3 text-gray-700">{note.body}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
