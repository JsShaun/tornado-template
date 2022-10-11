CREATE OR REPLACE FUNCTION operat_time()
RETURNS TRIGGER AS $$
BEGIN
   NEW.operat_time = NOW(); 
   RETURN NEW;
END;
$$ language 'plpgsql';


CREATE SCHEMA "super";
