create table if not exists subscriptions (
       user_id int primary key, 
       subscribed boolean
);

create table if not exists users (
       user_id int primary key,
       last_msg_time timestamp, 
       full_name text
);
