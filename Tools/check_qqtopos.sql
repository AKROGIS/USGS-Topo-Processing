SELECT * FROM qq_data

-- Duplicates
select name, image, [date], Coalesce(revision, [date]) as revision, printed, count(*) as cnt from qq_data group by name, image, [date], Coalesce(revision, [date]), printed
having count(*) > 1

-- Update Dups field
update q set dups = c.cnt
FROM qq_data as q
left join (select name, image, [date], Coalesce(revision, [date]) as revision, printed, count(*) as cnt from qq_data group by name, image, [date], Coalesce(revision, [date]), printed having count(*) > 1) as c
on c.name = q.name and c.image = q.image and c.[date] = q.[date] and c.revision = Coalesce(q.revision, q.[date]) and c.printed = q.printed

-- Number of tiles in a series/cell (two series, one with an image the other without)
-- Using Name instead of cell_name, because two maps are in the wrong cell (I've fixed the name)
select name, image, count(*) as cnt from qq_data group by name, image

-- Update Count field
update q set [count] = c.cnt
FROM qq_data as q
left join (select name, image, count(*) as cnt from qq_data group by name, image) as c
on c.name = q.name and c.image = q.image


-- All the tiles that have only one file should be best in series by default
select name, image, best_topo, best_img from qq_data where count = 1 order by image, name

-- Topos with in best of groups
-- Using Name instead of cell_name, because two maps are in the wrong cell (I've fixed the name)
select name, count(*) from qq_data where Best_topo = 1 group by name having count(*) > 1
select name, count(*) from qq_data where Best_img = 1 group by name having count(*) > 1

-- Topos with an image, and no best in series selected
select t1.[name], t2.name from 
(select name from qq_data where image = 1 group by name) as t1
full outer join
(select name from qq_data where best_img = 1 group by name) as t2
on t1.name = t2.name where t1.name is null or t2.name is null

-- Topos with NO image, and no best in series selected
select t1.[name], t2.name from 
(select name from qq_data where image = 0 group by name) as t1
full outer join
(select name from qq_data where best_topo = 1 group by name) as t2
on t1.name = t2.name where t1.name is null or t2.name is null

-- images with multiple tiles but no dups (newest should be best)
select name, sn, printed, Coalesce(revision, [date]) as revision, date, best_img from qq_data where count > 1 and image = 1 and dups is NULL order by name, printed, Coalesce(revision, [date]), date
-- images with multiple tiles AND dups (best is choosen manually, notes or barcode may have been the decider)
select name, sn, printed, Coalesce(revision, [date]) as revision, date, best_img, priority, barcode, notes from qq_data where count > 1 and image = 1 and dups is not NULL order by name, printed, Coalesce(revision, [date]), date, priority
-- multiple tiles without image AND dups (best is choosen manually, notes or barcode may have been the decider)
select name, sn, printed, Coalesce(revision, [date]) as revision, date, best_topo, priority, count, dups, barcode, notes from qq_data where count > 1 and image = 0 order by name, printed, Coalesce(revision, [date]), date, priority


-- Fix Priority; priorities for image = 0/1 are separate; the second dup should always have the lowest priority; otherwise priority is in date order.

--Check
select sn, best_img, priority from qq_data where image = 1 and priority <> 1 and best_img = 1
select sn, best_topo, priority from qq_data where image = 0 and priority <> 1 and best_topo = 1
select sn, best_img, priority from qq_data where image = 1 and priority = 1 and best_img = 0
select sn, best_topo, priority from qq_data where image = 0 and priority = 1 and best_topo = 0
--Fix
update qq_data set priority = 1 where image = 1 and priority <> 1 and best_img = 1
update qq_data set priority = 1 where image = 0 and priority <> 1 and best_topo = 1
update qq_data set priority = 0 where image = 1 and priority = 1 and best_img = 0
update qq_data set priority = 0 where image = 0 and priority = 1 and best_topo = 0
