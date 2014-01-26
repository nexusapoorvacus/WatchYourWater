drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  Username text not null,
  Password text not null,
  -- DishwasherTime integer,
  -- DishwasherCycle text,
  -- WaterGardenTime integer,
  -- WaterGardenLevel text,
  -- ShowerTime integer,
  -- WasherTime integer,
  -- WasherCycle text
  currenttask text,
  currenttime text,
  currentproperty text
);