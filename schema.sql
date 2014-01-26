drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  Username text not null,
  Password text not null,
  currenttask text,
  currenttime integer,
  currentproperty text
);