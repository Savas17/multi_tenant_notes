import React, { useState, useEffect } from "react";
import { useAuth } from "../../context/AuthContext.jsx";
import { useTenant } from "../../context/TenantContext.jsx";
import { useNavigate } from "react-router-dom";
import {
  fetchMemberCount,
  fetchMembers,
  changeMemberPlan,
  inviteUser,
} from "../../api/api.js";

export default function Navbar() {
  const { user, token, logout } = useAuth();
  const { tenant, upgradePlan } = useTenant();
  const navigate = useNavigate();

  const [memberCount, setMemberCount] = useState(0);
  const [members, setMembers] = useState([]);
  const [inviteEmail, setInviteEmail] = useState("");
  const [inviteRole, setInviteRole] = useState("member");
  const [selectedMemberId, setSelectedMemberId] = useState("");
  const [selectedPlan, setSelectedPlan] = useState("free");

  useEffect(() => {
    if (user?.role === "admin" && tenant?.id) {
      fetchMemberCount(token, tenant.id)
        .then((res) => setMemberCount(res.member_count))
        .catch(() => setMemberCount(0));
      fetchMembers(token)
        .then(setMembers)
        .catch(() => setMembers([]));
    }
  }, [user, tenant, token]);

  function handleLogout() {
    logout();
    navigate("/login");
  }

  async function handleChangePlan() {
    if (!selectedMemberId) {
      alert("Please select a member");
      return;
    }
    try {
      await changeMemberPlan(token, selectedMemberId, selectedPlan);
      alert(`Member plan updated to ${selectedPlan}`);
      const updatedMembers = await fetchMembers(token);
      setMembers(updatedMembers);
    } catch (error) {
      alert("Failed to update member plan: " + error.message);
    }
  }

  async function handleInvite() {
    try {
      await inviteUser(token, {
        email: inviteEmail,
        role: inviteRole,
        tenant_id: tenant.id,
      });
      alert("User invited");
      setInviteEmail("");
    } catch (error) {
      alert("Invite failed: " + error.message);
    }
  }

  return (
    <nav className="bg-white shadow-md sticky top-0 z-50">
      <div className="max-w-6xl mx-auto px-4 py-3 flex justify-between items-center">
        {/* Left: Brand + Tenant */}
        <div className="flex items-center gap-4">
          <h1 className="text-xl font-extrabold text-indigo-700">NotesApp</h1>
          {tenant && (
            <span className="px-3 py-1 bg-indigo-100 text-indigo-700 text-sm rounded-full">
              {tenant.name.toUpperCase()} • {tenant.plan === "pro" ? "PRO 🚀" : "FREE"}
            </span>
          )}
        </div>

        {/* Right: User Info + Actions */}
        <div className="flex items-center gap-4">
          {user && (
            <div className="text-sm text-gray-700">
              👋 <span className="font-semibold">{user.name}</span> ({user.role})
            </div>
          )}

          {user?.role === "admin" && tenant?.id && (
            <>
              <div className="text-sm text-gray-700">Members: {memberCount}</div>

              {/* Invite Form */}
              <input
                type="email"
                placeholder="Invite email"
                value={inviteEmail}
                onChange={(e) => setInviteEmail(e.target.value)}
                className="border p-1 rounded text-xs"
              />
              <select
                className="border p-1 rounded text-xs"
                value={inviteRole}
                onChange={(e) => setInviteRole(e.target.value)}
              >
                <option value="member">Member</option>
                <option value="admin">Admin</option>
              </select>
              <button
                onClick={handleInvite}
                className="bg-green-600 text-white px-2 py-1 rounded text-xs"
              >
                Invite
              </button>

              {/* Change Plan */}
              <select
                value={selectedMemberId}
                onChange={(e) => setSelectedMemberId(e.target.value)}
                className="border p-1 rounded text-xs"
              >
                <option value="">Select member</option>
                {members.map((m) => (
                  <option key={m.id} value={m.id}>
                    {m.name || m.username} ({m.plan})
                  </option>
                ))}
              </select>
              <select
                value={selectedPlan}
                onChange={(e) => setSelectedPlan(e.target.value)}
                className="border p-1 rounded text-xs"
              >
                <option value="free">Free</option>
                <option value="pro">Pro</option>
              </select>
              <button
                onClick={handleChangePlan}
                className="bg-blue-600 text-white px-2 py-1 rounded text-xs"
              >
                Change Plan
              </button>
            </>
          )}

          {/* Logout */}
          {user && (
            <button
              onClick={handleLogout}
              className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-xl text-sm shadow transition"
            >
              Logout
            </button>
          )}
        </div>
      </div>
    </nav>
  );
}
