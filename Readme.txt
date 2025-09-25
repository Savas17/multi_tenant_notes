# Multi-Tenant Notes App

A full-stack multi-tenant notes application built with FastAPI backend and React frontend, featuring user roles, subscription plans, and data isolation per tenant.

## Features

- Multi-tenant architecture with complete tenant data isolation
- Role-based access control (Admins and Members)
- Subscription plans:
   - Free plan (max 3 notes per member)
   - Pro plan (unlimited notes)
- Admin capabilities:
   - Invite users to tenant
   - View tenant members and count
   - Change plan for tenant members
   - Upgrade own tenant plan from Free to Pro
- Secure JWT based authentication
- React frontend with Tailwind CSS styling
- FastAPI backend with SQLAlchemy and SQLite (configurable)
- Environment variable configuration for secure deployment
- Proper CORS handling for multi-domain support

## Project Structure

- `backend/` - FastAPI backend code
- `frontend/` - React frontend code (Vite)
- `.env` files for environment configs (ignored by git)

## Getting Started
FRONTEND_URL=https://multi-tenant-notes-one.vercel.app
