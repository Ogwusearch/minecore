# MineCore

Mining Operations & Management Platform.

A production-oriented, multi-tenant mining operations system covering
exploration through sales, with an emphasis on traceability, tenant
isolation, and auditability.

## Architecture

- React / Vite frontend
- FastAPI backend
- PostgreSQL database
- Docker development environment

## Core Domains

Organizations · Mine Sites · Mining · Production · Stockpiles · Inventory ·
Weighbridge · Processing · Equipment · Exploration · Laboratory · Logistics ·
Sales · Finance · Safety · Environment · Compliance · Audit

## Operational Flow

    Exploration
        ↓
    Geology
        ↓
    Mine Site
        ↓
    Deposit
        ↓
    Pit
        ↓
    Mining Operation
        ↓
    Production
        ↓
    Stockpile
        ↓
    Processing
        ↓
    Inventory
        ↓
    Weighbridge
        ↓
    Shipment
        ↓
    Customer
        ↓
    Sales / Finance

## Documentation

- docs/architecture.md
- docs/database.md
- docs/api.md
- docs/security.md
- docs/testing.md
- docs/development-roadmap.md

## Quick Start

    make setup
    make docker-up
    make dev

## Development Commands

    make help
