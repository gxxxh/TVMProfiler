-- CREATE DATABASE profile_data ;
\c profile_data;
DROP TABLE IF EXISTS op_record;
DROP TABLE IF EXISTS model_record;
CREATE TABLE model_record
(
    execution_id uuid,
    start_time   timestamptz,
    num_ops      integer,
    model_name   text,
    PRIMARY KEY (execution_id)
);
CREATE TABLE op_record
(
    execution_id    uuid references model_record (execution_id),
    node_id         integer,
    node_name       text,
    node_start_time timestamptz,
    time_list       numeric[],
    avg_time        numeric,
    PRIMARY KEY (execution_id, node_id)
);
set timezone = 'asia/shanghai';
-- INSERT INTO op_run_time(execution_id, node_id) VALUES (1,1) RETURNING (execution_id,node_id);