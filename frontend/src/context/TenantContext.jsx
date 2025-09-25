import React, { createContext, useContext, useState } from "react";

const TenantContext = createContext();

export function TenantProvider({ children }) {
  const [tenant, setTenantState] = useState(null);

  function setTenant(data) {
    setTenantState(data);
  }

  function updateTenantPlan(plan) {
    setTenantState((prev) => ({ ...prev, plan }));
  }

  return (
    <TenantContext.Provider value={{ tenant, setTenant, updateTenantPlan }}>
      {children}
    </TenantContext.Provider>
  );
}

export function useTenant() {
  return useContext(TenantContext);
}
