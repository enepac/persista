ALTER TABLE conversations ADD COLUMN revision_id SERIAL;
ALTER TABLE conversations ADD COLUMN original_message TEXT;
ALTER TABLE conversations ADD COLUMN updated_message TEXT;
ALTER TABLE conversations ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
