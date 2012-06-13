drop table if exists userstory;
create table userstory (
    id integer primary key autoincrement,
    who string not null,
    what string not null,
    why string not null,
    ordinal integer not null
);
