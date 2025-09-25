const API_URL = import.meta.env.VITE_API_URL;

export const fetchNotes = async (token, tenant_id) => {
  const res = await fetch(`${API_URL}/notes?tenant_id=${tenant_id}`, {
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
    },
  });
  if (!res.ok) throw new Error("Failed to fetch notes");
  return res.json();
};

export const createNote = async (token, note) => {
  const res = await fetch(`${API_URL}/notes`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(note),
  });
  if (!res.ok) throw new Error("Failed to create note");
  return res.json();
};

export const updateNote = async (token, noteId, note) => {
  const res = await fetch(`${API_URL}/notes/${noteId}`, {
    method: "PUT",
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(note),
  });
  if (!res.ok) throw new Error("Failed to update note");
  return res.json();
};

export const deleteNote = async (token, noteId) => {
  const res = await fetch(`${API_URL}/notes/${noteId}`, {
    method: "DELETE",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  if (!res.ok) throw new Error("Failed to delete note");
  return res.json();
};

export const loginUser = async (credentials) => {
  const res = await fetch(`${API_URL}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(credentials),
  });
  if (!res.ok) throw new Error("Login failed");
  return res.json();
};

export const upgradeTenantPlan = async (token) => {
  const res = await fetch(`${API_URL}/tenants/upgrade`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || "Failed to upgrade tenant plan");
  }
  return res.json();
};

export const fetchMemberCount = async (token, tenant_id) => {
  const res = await fetch(`${API_URL}/users/count-members?tenant_id=${tenant_id}`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  if (!res.ok) throw new Error("Failed to fetch member count");
  return res.json();
};

export const fetchMembers = async (token) => {
  const res = await fetch(`${API_URL}/users/list-members`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  if (!res.ok) throw new Error("Failed to fetch members");
  return res.json();
};

export const changeMemberPlan = async (token, user_id, newPlan) => {
  const res = await fetch(`${API_URL}/users/change-plan/${user_id}`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ new_plan: newPlan }),
  });
  if (!res.ok) throw new Error("Failed to change member plan");
  return res.json();
};

export const inviteUser = async (token, userData) => {
  const res = await fetch(`${API_URL}/users/invite`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(userData),
  });
  if (!res.ok) throw new Error("Failed to invite user");
  return res.json();
};
