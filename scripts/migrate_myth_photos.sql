-- One-time migration for the myth-photo album feature (2026-07).
-- Run this ONCE against the live Postgres DB (e.g. the Supabase SQL editor).
-- Needed because app startup uses db.create_all(), which creates missing
-- tables but never ALTERs existing ones; fresh databases get the full shape
-- from the model automatically and do NOT need this script.

ALTER TABLE myth_photos ALTER COLUMN id TYPE VARCHAR(36);
ALTER TABLE myth_photos ADD COLUMN IF NOT EXISTS is_main BOOLEAN NOT NULL DEFAULT FALSE;
ALTER TABLE myth_photos ADD COLUMN IF NOT EXISTS sort_order INTEGER NOT NULL DEFAULT 0;
ALTER TABLE myth_photos ADD COLUMN IF NOT EXISTS created_at TIMESTAMPTZ NOT NULL DEFAULT NOW();
